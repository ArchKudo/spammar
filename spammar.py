import serial, time

def get_dist(ser, timeout=1):
    # First clear buffer
    try:
        ser.reset_input_buffer()
    except AttributeError: # Ignore if not implemented
        pass
    
    stamp = time.monotonic()
    while (time.monotonic() - stamp) < timeout:
        recv  = ser.read(1)
        
        # First frame indicator
        if not x or x[0] != 0x59:
            continue
        
        # Get frame
        data = ser.read(8)
        frame, dist, strength, mode, _, checksum = struct.unpack("<BHHBBB", data)

        # Second frame indicator
        if frame != 0x59:
            continue

        # Calculate checksum
        if ((sum(data[0:7]) + 0x59) & 0xFF) != checksum:
            continue

        return dist

    raise RuntimeError("Timeout reached before ")


def dump(ser, filename):
    while(True):
        with open(filename, 'w') as f:
            f.write(f'{get_dist(ser)}\n')

if __name__ == '__main__':
    try:
        ser = serial.Serial("/dev/ttyAMA0", 115200)
        if not ser.is_open:
            ser.open()
        dump(ser, "dump.txt")
    except KeyboardInterrupt:
        if ser:
            ser.close()

