from flask import Flask, request, render_template, jsonify
import pyautogui
import threading
import time
import queue

app = Flask(__name__)

# Global variables for typing control
text_queue = queue.Queue()
typing_thread = None
typing_active = False
typing_paused = False
typing_speed = 0.1  # Default typing speed


def type_text():
    global typing_active, typing_paused, typing_speed
    while True:
        if typing_active:
            try:
                text, speed = text_queue.get(timeout=1)
                typing_speed = 1 / speed  # Convert speed to interval in seconds
                print(
                    f"Typing text: '{text}' with speed: {typing_speed} seconds per char"
                )
                for char in text:
                    if not typing_active:
                        break
                    while typing_paused:
                        time.sleep(0.025)
                    pyautogui.typewrite(char)
                    time.sleep(typing_speed)
            except queue.Empty:
                continue


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/control-typing", methods=["POST"])
def control_typing():
    global typing_active, typing_paused, typing_thread
    data = request.json
    action = data.get("action")
    text = data.get("text", "")
    speed = float(data.get("speed", 1000))  # Speed in characters per second
    ip = data.get("ip", "")

    if action == "start":
        print(f"Starting typing with speed: {1/speed} seconds per char")
        text_queue.queue.clear()  # Clear any existing text
        text_queue.put((text, speed))
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
        return jsonify({"status": "success"}), 200

    elif action == "set-speed":
        typing_speed = 1 / speed  # Convert speed to interval in seconds
        print(f"Typing speed set to: {typing_speed} seconds per char")
        return jsonify({"status": "success"}), 200

    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
