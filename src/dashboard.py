#!/usr/bin/env python3

import tkinter as tk
from gps3.agps3threaded import AGPS3mechanism
import obd

# Start the GPS thread
agps_thread = AGPS3mechanism()  # Instantiate AGPS3 mechanism
agps_thread.stream_data()       # Start streaming data from gpsd (defaults to localhost)
agps_thread.run_thread()        # Run the thread

# Try to connect to the OBD-II adapter
print("Connecting to OBD-II adapter...")
connection = obd.OBD()  # Auto-connects to available port

# Set up the main display window using Tkinter
root = tk.Tk()
root.title("Dashboard")
root.geometry("800x480")
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Optional: Bind the Escape key to exit fullscreen mode
def exit_fullscreen(event):
    root.attributes("-fullscreen", False)
root.bind("<Escape>", exit_fullscreen)

# --- Layout using grid ---
# Row 0: GPS Time Label (spans all 3 columns)
time_label = tk.Label(root, text="Time: --", font=("Helvetica", 32), bg="black", fg="white")
time_label.grid(row=0, column=0, columnspan=3, pady=10)

# Row 1: We'll use three columns:
#   Column 0: empty spacer
#   Column 1: OBD Speed (center)
#   Column 2: GPS Info (right side)

# OBD Speed Label (Large, centered)
obd_speed_label = tk.Label(root, text="Speed: -- MPH", font=("Helvetica", 72), bg="black", fg="white")
obd_speed_label.grid(row=1, column=1, padx=20, pady=20)

# GPS Info Frame (to hold lat, lon, GPS speed, and course)
gps_frame = tk.Frame(root, bg="black")
gps_frame.grid(row=1, column=2, padx=20, pady=20, sticky="n")

lat_label = tk.Label(gps_frame, text="Lat: --", font=("Helvetica", 24), bg="black", fg="white")
lat_label.pack(pady=5, anchor="w")
lon_label = tk.Label(gps_frame, text="Lon: --", font=("Helvetica", 24), bg="black", fg="white")
lon_label.pack(pady=5, anchor="w")
gps_speed_label = tk.Label(gps_frame, text="GPS Speed: -- MPH", font=("Helvetica", 24), bg="black", fg="white")
gps_speed_label.pack(pady=5, anchor="w")
course_label = tk.Label(gps_frame, text="Course: --", font=("Helvetica", 24), bg="black", fg="white")
course_label.pack(pady=5, anchor="w")

# Configure grid weights to help center the middle column
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)

def update_dashboard():
    # --- Update GPS Data ---
    time_val = agps_thread.data_stream.time
    lat = agps_thread.data_stream.lat
    lon = agps_thread.data_stream.lon
    gps_speed = agps_thread.data_stream.speed
    track = agps_thread.data_stream.track
    
    time_label.config(text=f"Time: {time_val if time_val else '--'}")
    lat_label.config(text=f"Lat: {lat if lat else '--'}")
    lon_label.config(text=f"Lon: {lon if lon else '--'}")
    gps_speed_label.config(text=f"GPS Speed: {gps_speed if gps_speed else '--'} MPH")
    course_label.config(text=f"Course: {track if track else '--'}")
    
    # --- Update OBD Data ---
    response = connection.query(obd.commands.SPEED)
    if response.value is not None:
        try:
            mph_speed = response.value.to("mph")
            speed_value = mph_speed.magnitude
        except Exception:
            speed_value = response.value
        obd_speed_label.config(text=f"Speed: {speed_value:.1f} MPH")
    else:
        obd_speed_label.config(text="Speed: No Data")
    
    # Schedule next update after 1 second (1000 ms)
    root.after(1000, update_dashboard)

# Start the update loop
update_dashboard()

# Run the GUI event loop
root.mainloop()

def exit_dashboard(event):
    root.destroy()

root.bind("<Escape>", exit_dashboard)
