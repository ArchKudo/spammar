import serial, time

def dump_coord(ser):
    with open("dump.txt", "w") as f:
        while(True):
            recv = bytes()
            if ser.in_waiting > 8:
                recv = ser.read(9)
                ser.reset_input_buffer()
            
            if recv[0:2] == b'YY':
                dist = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                f.write(f"RX: {recv} Dist: {dist}, Strength: {strength}\n")

if __name__ == '__main__':
    try:
        ser = serial.Serial("/dev/ttyAMA0", 115200)
        if not ser.is_open:
            ser.open()
        dump_coord(ser)
    except KeyboardInterrupt:
        if ser:
            ser.close()

