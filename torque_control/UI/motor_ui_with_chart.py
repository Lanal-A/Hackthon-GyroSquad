
import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from collections import deque

ser = None
angle_history = deque(maxlen=100)
time_history = deque(maxlen=100)
start_time = time.time()

def list_serial_ports():
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
                    angle_value = extract_angle(line)
                    if angle_value is not None:
                        t = time.time() - start_time
                        angle_history.append(angle_value)
                        time_history.append(t)
                        angle_label.config(text=f"Angle: {angle_value:.2f}")
                else:
                    status_label.config(text=f"Received: {line}")
            except:
                status_label.config(text="⚠️ Read error")

def extract_angle(line):
    # Attempt to extract a float value from something like "angle: 123.45"
    try:
        for part in line.split():
            if part.replace('.', '', 1).replace('-', '', 1).isdigit():
                return float(part)
    except:
        return None
    return None

def update_plot():
    if time_history and angle_history:
        ax.clear()
        ax.plot(time_history, angle_history, label="Angle")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Angle")
        ax.set_title("Real-time Angle Plot")
        ax.legend()
        ax.grid(True)
        canvas.draw()
    root.after(200, update_plot)

# === UI Setup ===
root = tk.Tk()
root.title("Adaptive Gripper UI with Angle Chart")
root.geometry("800x600")
root.configure(bg="white")

tk.Label(root, text="Adaptive Gripper UI", font=("Helvetica", 20, "bold"), bg="white").pack(pady=10)

port_var = tk.StringVar()
ports = list_serial_ports()
port_dropdown = ttk.Combobox(root, textvariable=port_var, values=ports, font=("Helvetica", 12), width=40)
port_dropdown.set("Select Serial Port")
port_dropdown.pack(pady=5)

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
status_label.pack(pady=10)

angle_label = tk.Label(root, text="Angle: --", font=("Courier", 16), fg="blue", bg="white")
angle_label.pack(pady=5)

# === Matplotlib chart ===
fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

# === Start threads and loops ===
threading.Thread(target=read_serial, daemon=True).start()
update_plot()

root.mainloop()
