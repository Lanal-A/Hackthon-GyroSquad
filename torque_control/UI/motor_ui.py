import tkinter as tk
import serial
import threading

# 修改为你实际的串口，比如 "/dev/tty.usbserial-XXXXX"
SERIAL_PORT = "/dev/tty.usbserial-1234"
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
except Exception as e:
    print("串口连接失败：", e)
    ser = None

def read_serial():
    while ser and ser.is_open:
        if ser.in_waiting:
            line = ser.readline().decode().strip()
            output_label.config(text=line)

def send_torque():
    val = torque_entry.get()
    if ser and ser.is_open:
        ser.write(f"T:{val}\n".encode())

root = tk.Tk()
root.title("Motor Control UI")

tk.Label(root, text="Set Torque:").pack()
torque_entry = tk.Entry(root)
torque_entry.pack()

tk.Button(root, text="Send", command=send_torque).pack()

tk.Label(root, text="Sensor Output:").pack()
output_label = tk.Label(root, text="...")
output_label.pack()

# 启动串口读取线程
threading.Thread(target=read_serial, daemon=True).start()

root.mainloop()