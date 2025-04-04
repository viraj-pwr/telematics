#!/usr/bin/env python3

# from gps3 import gps3
# gps_socket = gps3.GPSDSocket()
# data_stream = gps3.DataStream()
# gps_socket.connect()
# gps_socket.watch()


# for new_data in gps_socket:
#     if new_data:
#         data_stream.unpack(new_data)
#         print('Altitude = ', data_stream.TPV['alt'])
#         print('Latitude = ', data_stream.TPV['lat'])
#         print('Long = ', data_stream.TPV['lon'])






from gps3.agps3threaded import AGPS3mechanism
agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second

improt time
while True:  # All data is available via instantiated thread data stream attribute.
    # line #140-ff of /usr/local/lib/python3.5/dist-packages/gps3/agps.py
    print('---------------------')
    print(                   agps_thread.data_stream.time)
    print('Lat:{}   '.format(agps_thread.data_stream.lat))
    print('Lon:{}   '.format(agps_thread.data_stream.lon))
    print('Speed:{} '.format(agps_thread.data_stream.speed))
    print('Course:{}'.format(agps_thread.data_stream.track))
    print('---------------------')
    time.sleep(1) # Sleep, or do other things for as long as you like.
