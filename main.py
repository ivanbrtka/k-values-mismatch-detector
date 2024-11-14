import tkinter as tk
from netmiko import ConnectHandler
from tkinter import messagebox
import time

def start_capture():
    # Define router connection details
    router = {
        'device_type': 'cisco_ios',
        'host': '192.168.56.101',  # Change to your router's IP
        'username': 'cisco',        # Replace with your router's username
        'password': 'cisco123!',    # Replace with your router's password
    }

    # Commands for each step
    commands = [
        
        # Define the Capture Buffer
        "do monitor capture buffer firewallcx_cap size 1024 linear",

        # Define Access List for Capturing Specific Traffic
        "access-list 100 permit ip any any"

        # Apply Access List to Capture Buffer
        "do monitor capture buffer firewallcx_cap filter access-list selected-traffic",

        # Define Capture Point and Parameters
        "do monitor capture point ip cef CPoint-FE0 FastEthernet0 both",

        # Associate the Capture Point with the Capture Buffer
        "do monitor capture point associate CPoint-FE0 firewallcx_cap",
        
        # Start Capturing Packets
        "do monitor capture point start CPoint-FE0"
    ]

    # Connect to the router
    try:
        net_connect = ConnectHandler(**router)
        print("Connected to the router.")

        # Execute each command step-by-step
        for cmd in commands:
            output = net_connect.send_config_set(cmd)
            print(f"Executed command: {cmd}")
            print(output)
            # Adding a small delay to ensure command processing in sequence
            time.sleep(1)

        print("Packet capture started successfully.")

        # Optional: Stop capturing after a delay
        time.sleep(10)  # Capture packets for 10 seconds; adjust as needed
        stop_output = net_connect.send_command("monitor capture point stop CPoint-FE0")
        print("Packet capture stopped.")
        print(stop_output)

        packets = net_connect.send_command("do show monitor capture buffer firewallcx_cap dump")
        print(packets)

        # Disconnect from the router
        net_connect.disconnect()

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the function to start Netmiko connection
def connect_to_router():
    
    # Get connect informations from form input 
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Basic input arguments check
    if not ip or not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    # Try to establish a connection
    try:
        '''
        device = {
            "device_type": "cisco_ios",
            "host": ip,
            "username": username,
            "password": password,
        }
        '''
        device = {
            "device_type": "cisco_ios",
            "host": '192.168.56.101',
            "username": 'cisco',
            "password": 'cisco123!',
        }
        # Establish a connection using Netmiko
        net_connect = ConnectHandler("192.168.56.101", username="cisco", password="cisco123!", device_type="cisco_ios")
        interf = net_connect.send_command("show ip int br", use_textfsm=True)
        print(interf)
        messagebox.showinfo("Connection Status", message='interf')
        net_connect.disconnect()
    except Exception as e:
        messagebox.showerror("Connection Failed", f"Failed to connect to device:\n{e}")

# Set up the main application window
root = tk.Tk()
root.title("EIGRP K-Values Mismatch Monitor")

# Labels and entry fields
header_label = tk.Label(root, text="EIGRP K-Values Mismatch Monitor", font=("Arial", 16, "bold"))
header_label.pack(pady=10)

ip_label = tk.Label(root, text="Router IP Address:")
ip_label.pack()
ip_entry = tk.Entry(root, width=30)
ip_entry.pack(pady=5)

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

# Connect button
connect_button = tk.Button(root, text="Connect to Router", command=start_capture)
connect_button.pack(pady=20)

# Run the application
root.mainloop()
