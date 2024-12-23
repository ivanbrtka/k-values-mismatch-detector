'''
-----------------------------------------------------------
| GUI tool for correcting EIGRP K-Values mismatch problem |
|                                                         |
| This tool works with packet monitor directly on router  |
-----------------------------------------------------------
'''

import tkinter as tk
from netmiko import ConnectHandler
from tkinter import messagebox
import time

# Setup monitor capture on Router 
def start_capture():

    # Define router connection details
    router = {
        'device_type': 'cisco_ios',
        'host': '192.168.0.1',  
        'username': 'ivan',        
        'password': 'Ivan2002',
        'secret': 'Ivan2002'    
    }

    # Commands for each step of configuring monitor
    commands = [
        # Remove monitor if exists
        "do no monitor capture buffer firewallcx_cap",

        # Define the linear Capture Buffer with fixed size
        "do monitor capture buffer firewallcx_cap size 1024 linear",

        # Define Access List for Capturing EIGRP Traffic
        "access-list 187 permit eigrp any any",

        # Apply Access List to Capture Buffer
        "do monitor capture buffer firewallcx_cap filter access-list 187",

        # Define Capture Point and Parameters
        "do monitor capture point ip cef CPoint-FE0 FastEthernet0/0 in",

        # Associate the Capture Point with the Capture Buffer
        "do monitor capture point associate CPoint-FE0 firewallcx_cap",
        
        # Start Capturing Packets
        "do monitor capture point start CPoint-FE0"
    ]

    # Connect to the router
    try:
        net_connect = ConnectHandler(**router)
        net_connect.enable()
        net_connect.config_mode()

        # Execute each command step-by-step
        for cmd in commands:
            output = net_connect.send_command(cmd)
            print(f"Executed command: {cmd}")
            print(output)
            

        print("Packet capture started successfully.")

        # Optional: Stop capturing after a delay
        time.sleep(20)  # Capture packets for 10 seconds; adjust as needed
        stop_output = net_connect.send_command("do monitor capture point stop CPoint-FE0")
        print("Packet capture stopped.")
        print(stop_output)

        packets = net_connect.send_command("do show monitor capture buffer firewallcx_cap dump")
        print(packets)

        # Disconnect from the router
        net_connect.disconnect()

    except Exception as e:
        print(f"An error occurred: {e}")
        

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
