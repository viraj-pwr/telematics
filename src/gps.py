import gps
import time

import gps
import time

def main():
    # Connect to the gpsd running on localhost at port 2947
    session = gps.gps("localhost", "2947")
    # Start streaming data without additional flags
    session.stream()
    print("Connected to gpsd. Waiting for GPS data...")
    try:
        while True:
            report = session.next()
            if report['class'] == 'TPV':
                # Safely retrieve latitude, longitude, and altitude if available
                latitude = getattr(report, 'lat', None)
                longitude = getattr(report, 'lon', None)
                altitude = getattr(report, 'alt', None)
                if latitude is not None and longitude is not None:
                    print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")
                else:
                    print("No valid GPS fix yet.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting GPS reader.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
