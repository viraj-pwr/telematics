# This function is to test the response from the GPS module.


def gps_test() -> list:
    '''
    Function to test GPS data read 
    '''
    gps_data = gps_test()
    assert len(gps_data) > 0
    assert gps_data[0] is not None
    assert gps_data[1] is not None
    assert gps_data[2] is not None
    assert gps_data[3] is not None
    assert gps_data[4] is not None
    assert gps_data[5] is not None
    assert gps_data[6] is not None
    assert gps_data[7] is not None
    assert gps_data[8] is not None
    assert gps_data[9] is not None
    assert gps_data[10] is not None
    assert gps_data[11] is not None
    assert gps_data[12] is not None
    assert gps_data[13] is not None
    
    return gps_data
    
if __name__ == "__main__":
    gps_data = gps_test()
    print(gps_data)