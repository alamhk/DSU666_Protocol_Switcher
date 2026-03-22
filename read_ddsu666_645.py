# DDSU666 DL/T 645 Reader Utility
# Refined and researched by Antigravity AI (Google DeepMind)

import serial
import time

def dlt645_checksum(data):
    return sum(data) % 256

def format_hex(data):
    return "".join([f"{b:02X}" for b in data])

def bcd_to_float(bcd_bytes, scale=1.0):
    val_str = "".join([f"{b:02X}" for b in bcd_bytes[::-1]])
    try:
        return float(val_str) * scale
    except ValueError:
        return None

def read_dlt645_data(ser, addr_bytes, data_id_hex):
    # Data ID: 4 bytes, reversed and offset by 0x33
    did = bytes.fromhex(data_id_hex)[::-1]
    data_field = bytes([(b + 0x33) % 256 for b in did])
    
    # Frame parts
    # addr_bytes is already reversed BCD
    frame_body = bytes([0x68]) + addr_bytes + bytes([0x68, 0x11, 0x04]) + data_field
    cs = dlt645_checksum(frame_body)
    frame = frame_body + bytes([cs, 0x16])
    
    wakeup = bytes([0xFE, 0xFE, 0xFE, 0xFE])
    ser.write(wakeup + frame)
    
    response = ser.read(100)
    if not response:
        return None
        
    # Strip FE
    while len(response) > 0 and response[0] == 0xFE:
        response = response[1:]
        
    if len(response) < 12 or response[0] != 0x68 or response[-1] != 0x16:
        return None
        
    if response[8] != 0x91:
        return None

    data_len = response[9]
    raw_payload = response[10:10+data_len]
    decoded_payload = bytes([(b - 0x33) % 256 for b in raw_payload])
    
    # Result data (skip DID)
    return decoded_payload[4:]

def main():
    port = "COM4"
    try:
        ser = serial.Serial(port, 2400, parity='E', timeout=1)
    except Exception as e:
        print(f"Error: {e}")
        return

    # 1. Use broadcast to get address and initial voltage
    print("Connecting to DDSU666 (DL/T 645-2007)...")
    broadcast_addr = bytes([0xAA] * 6)
    
    # Phase A Voltage ID: 02010100
    res = read_dlt645_data(ser, broadcast_addr, "02010100")
    if res:
        # Re-read full response to get exact address from framing if we wanted, 
        # but let's just stick to broadcast for simplicity or get it from first frame.
        pass

    # Actually, let's just use broadcast for all requests in this session.
    targets = {
        "Voltage (V)": ("02010100", 0.1),
        "Current (A)": ("02020100", 0.001),
        "Active Power (kW)": ("02030000", 0.0001),
        "Total Energy (kWh)": ("00010000", 0.01),
    }
    
    print("-" * 30)
    for name, (did, scale) in targets.items():
        res = read_dlt645_data(ser, broadcast_addr, did)
        if res:
            val = bcd_to_float(res, scale)
            if val is not None:
                print(f"{name:20}: {val}")
            else:
                print(f"{name:20}: Parse Error")
        else:
            print(f"{name:20}: Timeout")
    print("-" * 30)
    ser.close()

if __name__ == "__main__":
    main()
