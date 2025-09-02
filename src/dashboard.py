#!/usr/bin/env python3

import tkinter as tk
from gps3.agps3threaded import AGPS3mechanism
import obd
import datetime
import csv
import os



def save_data_to_csv(lat, lon, gps_speed, timestamp, obd_value, obd_type="RPM"):
    """
    Save GPS and OBD data to a CSV file on external drive.
    
    Args:
        lat: Latitude value
        lon: Longitude value  
        gps_speed: GPS speed value
        timestamp: Timestamp string
        obd_value: OBD sensor value
        obd_type: Type of OBD sensor (default: RPM)
    """
    # External drive path - adjust if your mount point is different
    external_drive_path = "/media/viraj"  # Common default mount point for Raspberry Pi
    csv_filename = os.path.join(external_drive_path, "telematics_data.csv")
    
    # Check if external drive is accessible
    if not os.path.exists(external_drive_path):
        print(f"External drive not found at {external_drive_path}")
        # Fallback to local directory if external drive is not available
        csv_filename = "telematics_data.csv"
        print("Falling back to local directory for CSV storage")
    
    file_exists = os.path.exists(csv_filename)
    
    try:
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'latitude', 'longitude', 'gps_speed', 'obd_type', 'obd_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write data row
            writer.writerow({
                'timestamp': timestamp if timestamp else '--',
                'latitude': lat if lat else '--',
                'longitude': lon if lon else '--',
                'gps_speed': gps_speed if gps_speed else '--',
                'obd_type': obd_type,
                'obd_value': obd_value if obd_value is not None else '--'
            })
            
    except Exception as e:
        print(f"Error saving data to CSV: {e}")
        print(f"Attempted to save to: {csv_filename}")

def convert_utc_to_local(utc_time_str):
    """
    Convert a UTC ISO8601 time string (e.g., "2025-04-06T12:30:40.000Z")
    to local time string in format "DD Month YYYY HH:MM:SS".
    """
    try:
        # Try parsing with microseconds
        utc_dt = datetime.datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # Fallback if microseconds are missing
        utc_dt = datetime.datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
    # Set timezone info to UTC and convert to local time
    utc_dt = utc_dt.replace(tzinfo=datetime.timezone.utc)
    local_dt = utc_dt.astimezone()  # uses system local timezone
    return local_dt.strftime("%d %B %Y %H:%M:%S")  # e.g., "06 April 2025 12:30:40"

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

# Bind the Escape key to exit the dashboard completely
def exit_dashboard(event):
    root.destroy()
root.bind("<Escape>", exit_dashboard)

# --- Layout using grid ---
# Row 0: GPS Time Label (spans all 3 columns)
time_label = tk.Label(root, text="Time: --", font=("Helvetica", 32), bg="black", fg="white")
time_label.grid(row=0, column=0, columnspan=3, pady=10)

# Row 1: Three columns layout:
#   Column 0: (spacer)
#   Column 1: OBD Speed (center)
#   Column 2: GPS Info (right side)
obd_speed_label = tk.Label(root, text="Speed: -- MPH", font=("Helvetica", 72), bg="black", fg="white")
obd_speed_label.grid(row=1, column=1, padx=20, pady=20)

# GPS Info Frame (to hold latitude, longitude, GPS speed, and course)
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

# Configure grid weights so the center column is larger
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
    
    if time_val and time_val != '--':
        local_time = convert_utc_to_local(time_val)
    else:
        local_time = '--'
    
    time_label.config(text=f"Time: {local_time}")
    lat_label.config(text=f"Lat: {lat if lat else '--'}")
    lon_label.config(text=f"Lon: {lon if lon else '--'}")
    gps_speed_label.config(text=f"GPS Speed: {gps_speed if gps_speed else '--'} MPH")
    course_label.config(text=f"Course: {track if track else '--'}")
    
    # --- Update OBD Data ---
    # response = connection.query(obd.commands.SPEED)
    # if response.value is not None:
    #     try:
    #         mph_speed = response.value.to("mph")
    #         speed_value = mph_speed.magnitude
    #     except Exception:
    #         speed_value = response.value
    #     obd_speed_label.config(text=f"Speed: {speed_value:.1f} MPH")
    # else:
    #     obd_speed_label.config(text="Speed: No Data")
        
    # Display RPM Test
    response_rpm = connection.query(obd.commands.RPM).value.magnitude
    obd_speed_label.config(text=f"Speed: {response_rpm:.1f} RPM")
    
    # Save data to CSV file
    save_data_to_csv(lat, lon, gps_speed, time_val, response_rpm, "RPM")


    
    # Schedule next update after 1 second (1000 ms)
    root.after(1000, update_dashboard)

# Start the update loop
update_dashboard()
print("Dashboard started")
# Run the GUI event loop
root.mainloop()
