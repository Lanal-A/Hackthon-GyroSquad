
import tkinter as tk
from tkinter import messagebox
import serial
import threading

# === Global serial object ===
ser = None

# === UI Functions ===
def connect_serial():
    global ser
    try:
        ser = serial.Serial("/dev/tty.usbserial-1234", 115200)
        status_label.config(text="✅ Serial connected.")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect: {e}")
        status_label.config(text="❌ Failed to connect serial.")

def send_cmd(command):
    if ser and ser.is_open:
        ser.write((command + "\n").encode())
        status_label.config(text=f"Sent: {command}")
    else:
        status_label.config(text="❗ Serial not connected.")

def read_serial():
    while True:
        if ser and ser.in_waiting:
            try:
                line = ser.readline().decode().strip()
                status_label.config(text=f"Received: {line}")
            except:
                status_label.config(text="⚠️ Read error")

# === UI Setup ===
root = tk.Tk()
root.title("Adaptive Gripper Web UI")
root.geometry("500x300")
root.configure(bg="white")

title = tk.Label(root, text="Adaptive Gripper Web UI", font=("Helvetica", 20, "bold"), bg="white")
title.pack(pady=10)

connect_button = tk.Button(root, text="🔌 Connect Serial", font=("Helvetica", 14), command=connect_serial, width=20)
connect_button.pack(pady=10)

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="🤏 Close Gripper", font=("Helvetica", 14), command=lambda: send_cmd("CLOSE"), width=16)
btn2 = tk.Button(button_frame, text="👐 Open Gripper", font=("Helvetica", 14), command=lambda: send_cmd("OPEN"), width=16)
btn3 = tk.Button(button_frame, text="✋ Stop Gripper", font=("Helvetica", 14), command=lambda: send_cmd("STOP"), width=16)

btn1.grid(row=0, column=0, padx=5)
btn2.grid(row=0, column=1, padx=5)
btn3.grid(row=0, column=2, padx=5)

status_label = tk.Label(root, text="Waiting for serial data...", font=("Courier", 12), bg="white")
status_label.pack(pady=20)

# Start serial reading thread
threading.Thread(target=read_serial, daemon=True).start()

root.mainloop()
