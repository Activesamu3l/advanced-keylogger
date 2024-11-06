<div align="center">
  <img widtht="1000" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzNnMHFxdDIzbmJ3bjkzNXB5ZW1vOGN6cHV6bW56em81MHRlbDdlZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VAG0Ct1MbUCju/giphy.gif"  />
</div>


# Python Keylogger

This is a Python-based keylogger application that captures and logs keystrokes, system information, clipboard data, audio input, and screenshots. The captured data is encrypted and emailed to a specified recipient. The program is designed to run persistently on a Windows machine by adding itself to the system startup folder, ensuring it runs automatically after each system reboot.

> **Important Note**: This project is for educational purposes only. Unauthorized use or distribution of keyloggers may be illegal and unethical. Always obtain proper consent before using or deploying software that collects user data.

## Features

- **Keystroke Logging**: Captures all keystrokes and logs them into a file.
- **System Information**: Collects details about the system, including the machine's IP address, processor, and OS details.
- **Clipboard Data**: Logs clipboard contents when copied.
- **Audio Recording**: Records audio for a specified duration and stores it in a `.wav` file.
- **Screenshot Capture**: Takes screenshots and saves them as image files.
- **File Encryption**: Encrypts log files using the `Fernet` encryption scheme before sending them via email.
- **Auto Startup**: Adds the executable to the Windows Startup folder, ensuring it runs on every system login.
- **Email Notification**: Sends the encrypted log files to a specified email address.

## Requirements

Before running the keylogger, make sure you have the following installed:

- Python 3.x
- Required Python packages (can be installed via `requirements.txt`):

```bash
pip install pynput pywin32 scikit-learn scipy requests pillow sounddevice cryptography python-dotenv
```

You will also need to set up the environment variables for the email functionality.

### Environment Variables

Create a `.env` file in the root directory of your project with the following content:

```env
EMAIL_ADDRESS=your_email@example.com
PASSWORD=your_email_password
TO_ADDR=recipient_email@example.com
```

Ensure that you use an email service that allows you to send emails via SMTP. For example, Gmail requires you to enable **less secure apps** or create an **App Password** for better security.

## How It Works

1. **Keystroke Logging**: Every key pressed by the user is logged into a file. Special keys like space, enter, backspace, shift, and others are recorded with a specific notation (e.g., `[BACKSPACE]` for backspace, `[SHIFT]` for shift).
   
2. **System Information**: The script collects system details like the hostname, IP address (both private and public), processor details, and OS version, then writes this information to a file.

3. **Clipboard Logging**: If any data is copied to the clipboard, it is logged into a separate file.

4. **Audio Recording**: The script records audio from the microphone for a predefined duration and saves it as a `.wav` file.

5. **Screenshot Capturing**: The script takes a screenshot and saves it as a `.png` file.

6. **Emailing Logs**: After collecting the data, the log files are encrypted using `Fernet` encryption. The encrypted files are then emailed to the recipient.

7. **Auto Start on Boot**: The script adds itself to the Windows Startup folder so that it runs automatically every time the machine restarts.

## Usage

1. **Run the Script**: Simply execute the script as a regular Python program or convert it into an executable using a tool like **PyInstaller**.

2. **Converting to an Executable**: To convert the script into an executable `.exe` file for easier deployment, you can use **PyInstaller**:

   ```bash
   pyinstaller --onefile --add-data "path_to_your_files;." script_name.py
   ```

   This will generate an `.exe` file that you can distribute or deploy.

3. **After Running**:
   - The program will log keystrokes, system information, clipboard data, audio, and screenshots.
   - It will encrypt the log files and send them via email to the recipient you specified.
   - The program will add itself to the Windows Startup folder, ensuring it runs automatically after a reboot.

## Code Walkthrough

### Main Functions

- `send_email`: Sends an email with the collected log files attached.
- `computer_information`: Collects system information (hostname, IP address, OS version, etc.).
- `copy_clipboard`: Collects the current clipboard content.
- `microphone`: Records audio for a specified duration and saves it to a `.wav` file.
- `screenshot`: Captures a screenshot of the screen and saves it as a `.png` file.
- `keylogger`: Listens to keystrokes and logs them to a file.
- `write_keys_to_file`: Writes the captured keystrokes to a log file, converting special keys into readable strings.
- `encrypt_files`: Encrypts the log files and sends them via email.
- `delete_files`: Deletes sensitive log files after they are encrypted and sent.
- `add_to_startup`: Adds the executable to the Windows Startup folder to ensure auto-start on system login.
- `main`: Orchestrates the overall flow of the program, including calling the functions above.

### File Paths

The file paths are dynamically determined based on whether the script is running as a normal Python script or bundled as a standalone `.exe` file using PyInstaller. If the script is running as a bundled executable, it will use the `sys._MEIPASS` directory, otherwise, it will use the current working directory.

## Security Warning

This project is for educational purposes only. **Using keyloggers to capture personal data without the knowledge and consent of the user is illegal and unethical**. Ensure that you have proper authorization before running this type of software on any system. Always respect privacy and obtain consent when collecting data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Conclusion

This keylogger script demonstrates several techniques including keylogging, file encryption, screenshot capture, and email sending. However, it’s important to stress that keylogging is often illegal without explicit consent from the person being monitored. Always be ethical and responsible when developing or using such software.

---

Let me know if you'd like any adjustments or additional sections!