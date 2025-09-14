from flask import Flask, render_template, request, jsonify
from praisonaiagents import Agent, MCP
import os
from datetime import datetime

app = Flask(__name__)

# Paths
python_path = os.getenv("PYTHON_PATH")
server_path = os.getenv("SERVER_PATH")

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Agent setup
agent = Agent(
    instructions=f"You are a helpful assistant that can check stock prices using 'get_stock_price'. Today's date is {current_date}.",
    llm="ollama/qwen3:1.7b",
    tools=MCP(f"{python_path} {server_path}")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    response = agent.start(user_msg)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
