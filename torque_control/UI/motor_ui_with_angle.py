
import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import glob

ser = None

def list_serial_ports():
    """List available serial ports on macOS."""
    return glob.glob('/dev/tty.usb*') + glob.glob('/dev/tty.*usb*')

def connect_serial():
    global ser
    selected_port = port_var.get()
    try:
        ser = serial.Serial(selected_port, 115200)
        status_label.config(text=f"✅ Connected to {selected_port}")
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
                if "angle" in line.lower():
                    angle_label.config(text=f"Angle: {line}")
                else:
                    status_label.config(text=f"Received: {line}")
            except:
                status_label.config(text="⚠️ Read error")

# === UI Setup ===
root = tk.Tk()
root.title("Adaptive Gripper Web UI")
root.geometry("600x360")
root.configure(bg="white")

tk.Label(root, text="Adaptive Gripper Web UI", font=("Helvetica", 20, "bold"), bg="white").pack(pady=10)

# Serial port dropdown
port_var = tk.StringVar()
ports = list_serial_ports()
port_dropdown = ttk.Combobox(root, textvariable=port_var, values=ports, font=("Helvetica", 12), width=40)
port_dropdown.set("Select Serial Port")
port_dropdown.pack(pady=5)

connect_button = tk.Button(root, text="🔌 Connect Serial", font=("Helvetica", 14), command=connect_serial, width=20)
connect_button.pack(pady=10)

# Control buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="🤏 Close Gripper", font=("Helvetica", 14), command=lambda: send_cmd("CLOSE"), width=16)
btn2 = tk.Button(button_frame, text="👐 Open Gripper", font=("Helvetica", 14), command=lambda: send_cmd("OPEN"), width=16)
btn3 = tk.Button(button_frame, text="✋ Stop Gripper", font=("Helvetica", 14), command=lambda: send_cmd("STOP"), width=16)

btn1.grid(row=0, column=0, padx=5)
btn2.grid(row=0, column=1, padx=5)
btn3.grid(row=0, column=2, padx=5)

# Status and angle display
status_label = tk.Label(root, text="Waiting for serial data...", font=("Courier", 12), bg="white")
status_label.pack(pady=10)

angle_label = tk.Label(root, text="Angle: --", font=("Courier", 16), fg="blue", bg="white")
angle_label.pack(pady=5)

# Start reading thread
threading.Thread(target=read_serial, daemon=True).start()

root.mainloop()
