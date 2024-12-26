# Autotyper Project

This project is a Python-based tool that enables remote text input automation. You can send text to be typed in any text editor or input field on the target machine. The server receives commands and processes them to perform typing actions, control typing speed, pause/resume typing, and clear text input.

---

## Features

- **Remote Typing**: Send text to the target machine and have it typed in any editor.
- **Typing Control**: Start, stop, pause, and resume typing at any time.
- **Speed Adjustment**: Dynamically adjust the typing speed (characters per second).
- **Text Clearing**: Clear the queued text.
- **Cross-Origin Support**: Uses Flask-CORS to handle cross-origin requests.
- **Fail-Safe Mechanism**: Incorporates PyAutoGUI's fail-safe to prevent accidental misuse.

---

## Requirements

### Python Packages

Install the required Python libraries using pip:

```bash
pip install flask flask-cors paramiko pyautogui
```

### Other Requirements

- Python 3.7+
- A target machine with SSH enabled for remote command execution (if using SSH commands).

---

## Project Structure

```
.
├── app.py           # Flask server implementation
├── templates
│   └── index.html   # Frontend for controlling the autotyper
├── README.md        # Project documentation
```

---

## Usage

### 1. Run the Server

Start the Flask server:

```bash
python app.py
```

### 2. Access the Frontend

Open the following URL in your web browser:

```
http://<server-ip>:5000
```

### 3. Interact with the Application

- Enter the target machine's IP address.
- Input the text to be typed.
- Adjust typing speed.
- Use the provided buttons to control the typing process:
  - **Start Typing**
  - **Stop Typing**
  - **Resume Typing**
  - **Set Speed**
  - **Clear Text**

---

## Important Notes

1. **Fail-Safe Mechanism**: PyAutoGUI's fail-safe is triggered if the mouse moves to a corner of the screen. This is a safety feature to prevent unintended typing actions. You can disable it, but this is **not recommended**.

2. **Security Considerations**: Ensure the server is secured when exposing it over a network. Use proper authentication and limit access to trusted users.

3. **Compatibility**: The application works on any OS where PyAutoGUI and Flask are supported.

---

## Example Workflow

1. **Start Typing**: Send text to be typed at the specified speed.
2. **Pause/Resume**: Control the typing process as needed.
3. **Clear Text**: Remove any queued text and reset typing.

---

## Troubleshooting

### Common Issues

- **FailSafeException**: Ensure the mouse does not move to the screen corners during typing. If unavoidable, disable the fail-safe by adding this line in the code:

  ```python
  pyautogui.FAILSAFE = False
  ```

- **SSH Connectivity**: Check network and SSH configurations if using SSH commands to interact with the target machine.

---

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
