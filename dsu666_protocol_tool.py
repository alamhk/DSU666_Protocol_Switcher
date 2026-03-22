# DDSU666 Protocol Migrator
# Refined and researched by Antigravity AI (Google DeepMind)

import serial
import time
import minimalmodbus
import sys

# Configuration
PORT = "COM4"
BAUD_RATES = [9600, 4800, 2400, 1200]

def dlt645_checksum(data):
    return sum(data) % 256

def safe_serial_open(port, baud, parity, stopbits, timeout, retries=2):
    for i in range(retries):
        try:
            return serial.Serial(port, baud, parity=parity, stopbits=stopbits, timeout=timeout)
        except Exception:
            time.sleep(0.5)
    return None

def find_meter_dlt645(port):
    """Scan all baud rates and parities for DL/T 645."""
    print("[*] Searching for DL/T 645...")
    for baud in BAUD_RATES:
        for parity in ['E', 'N']:
            stops = 1 if parity == 'E' else 2
            ser = safe_serial_open(port, baud, parity, stops, 0.6)
            if not ser: continue
            
            # Broadcast Read Address
            frame_body = bytes.fromhex("68AAAAAAAAAAAA681300")
            cs = dlt645_checksum(frame_body)
            frame = frame_body + bytes([cs, 0x16])
            
            ser.write(bytes([0xFE] * 4) + frame)
            res = ser.read(50)
            ser.close()
            
            if res:
                clean = res
                while len(clean) > 0 and clean[0] == 0xFE: clean = clean[1:]
                if len(clean) >= 12 and clean[0] == 0x68 and clean[8] in [0x93, 0x13]:
                    addr_bytes = clean[1:7]
                    addr_str = "".join([f"{b:02X}" for b in addr_bytes[::-1]])
                    print(f"  [+] Found (645) at {baud} {parity}, Addr: {addr_str}")
                    return addr_bytes, addr_str, baud, parity, stops
    return None, None, None, None, None

def find_meter_modbus(port):
    """Scan common IDs and baud rates for Modbus."""
    print("[*] Searching for Modbus RTU...")
    for baud in BAUD_RATES:
        for mid in [64, 1, 3]:
            try:
                instrument = minimalmodbus.Instrument(port, mid)
                instrument.serial.baudrate = baud
                instrument.serial.stopbits = 2
                instrument.serial.timeout = 0.4
                instrument.read_float(0x2000, functioncode=3, number_of_registers=2)
                print(f"  [+] Found (Modbus) at {baud} 8N2, ID: {mid}")
                return mid, baud
            except:
                pass
    return None, None

def main():
    print("=== DDSU666 Protocol Migrator ===")
    
    # 1. State Discovery
    addr_bytes, addr_str, baud_645, p_645, s_645 = find_meter_dlt645(PORT)
    modbus_id, baud_modbus = (None, None)
    
    if not addr_bytes:
        modbus_id, baud_modbus = find_meter_modbus(PORT)

    if not addr_bytes and not modbus_id:
        print("[-] Error: No meter detected on COM4. Check wiring and port.")
        return

    # 2. Perform Single Migration
    if addr_bytes:
        print(f"\n[!] Meter is currently in DL/T 645 mode.")
        print(f"[*] Migrating to Modbus RTU...")
        with safe_serial_open(PORT, baud_645, p_645, s_645, 1) as ser:
            payload = bytes.fromhex("3333353D33333333333333333333")
            frame_body = bytes([0x68]) + addr_bytes + bytes([0x68, 0x14, 0x0E]) + payload
            cs = dlt645_checksum(frame_body)
            frame = frame_body + bytes([cs, 0x16])
            ser.write(bytes([0xFE]*4) + frame)
        
        print("[*] Command sent. Waiting 5s for reboot and verifying...")
        time.sleep(5)
        
        final_id, final_baud = find_meter_modbus(PORT)
        if final_id:
            print(f"\n[SUCCESS] Migrated to Modbus RTU (ID {final_id}, Baud {final_baud})")
        else:
            print("[-] Verification failed: Meter did not respond in Modbus mode.")
            
    elif modbus_id:
        print(f"\n[!] Meter is currently in Modbus RTU mode.")
        print(f"[*] Migrating to DL/T 645...")
        try:
            instrument = minimalmodbus.Instrument(PORT, modbus_id)
            instrument.serial.baudrate = baud_modbus
            instrument.serial.stopbits = 2
            instrument.write_register(0x0005, 1)
            instrument.serial.close()
            
            print("[*] Command sent. Waiting 5s for reboot and verifying...")
            time.sleep(5)
            
            addr_b, addr_s, b_645, p_6, s_6 = find_meter_dlt645(PORT)
            if addr_b:
                print(f"\n[SUCCESS] Migrated to DL/T 645 (Addr {addr_s}, Baud {b_645})")
            else:
                print("[-] Verification failed: Meter did not respond in 645 mode.")
        except Exception as e:
            print(f"[-] Migration failed: {e}")

if __name__ == "__main__":
    main()
