from flask import Flask, request, render_template, jsonify
import pyautogui
from flask_cors import CORS
import threading
import time
import queue

app = Flask(__name__)
CORS(app)

# Global variables for typing control
text_queue = queue.Queue()
typing_thread = None
typing_active = False
typing_paused = False
current_position = 0
current_text = ""
current_speed = 0.1  # Default typing speed


def type_text():
    global typing_active, typing_paused, current_position, current_text, current_speed
    while True:
        if typing_active:
            if current_position < len(current_text):
                for char in current_text[current_position:]:
                    if not typing_active:
                        break
                    while typing_paused:
                        time.sleep(0.025)
                    pyautogui.typewrite(char)
                    current_position += 1
                    time.sleep(current_speed)
            else:
                typing_active = False  # Stop typing if the end of the text is reached


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/control-typing", methods=["POST"])
def control_typing():
    global typing_active, typing_paused, typing_thread, current_position, current_text, current_speed
    data = request.json
    action = data.get("action")
    text = data.get("text", "")
    speed = float(data.get("speed", 1000))  # Speed in characters per second
    ip = data.get("ip", "")

    if action == "start":
        current_speed = 1 / speed  # Convert speed to interval in seconds
        print(f"Starting typing with speed: {current_speed} seconds per char")
        current_position = 0  # Reset position
        current_text = text
        typing_active = True
        typing_paused = False
        if typing_thread is None or not typing_thread.is_alive():
            typing_thread = threading.Thread(target=type_text, daemon=True)
            typing_thread.start()
        return jsonify({"status": "success"}), 200

    elif action == "stop":
        typing_active = False
        return jsonify({"status": "success"}), 200

    elif action == "resume":
        typing_active = True
        typing_paused = False
        if typing_thread is None or not typing_thread.is_alive():
            typing_thread = threading.Thread(target=type_text, daemon=True)
            typing_thread.start()
        return jsonify({"status": "success"}), 200

    elif action == "set-speed":
        current_speed = 1 / speed  # Convert speed to interval in seconds
        print(f"Typing speed set to: {current_speed} seconds per char")
        return jsonify({"status": "success"}), 200

    elif action == "clear":
        text_queue.queue.clear()  # Clear the text queue
        typing_active = False  # Stop typing if it was active
        return jsonify({"status": "success"}), 200

    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
