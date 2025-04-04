import gps
import time

def main():
    # Connect to the gpsd running on localhost at port 2947
    session = gps.gps("localhost", "2947")
    session.stream()
    try:
        while True:
            report = session.next()
            if report['class'] == 'TPV':
                if hasattr(report, 'lat'):
                    print(report.lat, report.lon)
                    time.sleep(2)
    except KeyboardInterrupt:
        quit()
    finally:
        session.stop()

if __name__ == '__main__':
    main()