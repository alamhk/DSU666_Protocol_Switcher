# DDSU666 Energy Reset Utility
# Refined and researched by Antigravity AI (Google DeepMind)

import minimalmodbus
import serial
import time

def reset_energy(port, addr=64):
    print(f"--- Resetting DSU666 Energy Counter (ID: {addr}, 8N2) ---")
    instrument = minimalmodbus.Instrument(port, addr)
    instrument.serial.baudrate = 9600
    instrument.serial.stopbits = 2
    instrument.serial.timeout = 1.0
    instrument.mode = minimalmodbus.MODE_RTU
    
    try:
        # Register 0x0002, write 1 (zero clearing)
        # Using Function 16 (Write Multiple Registers) as Function 06 might fail
        print("Sending Reset command (Write 1 to Register 0x0002)...")
        instrument.write_registers(0x0002, [1])
        print("SUCCESS! Energy counter should now be reset to zero.")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    # Performing the reset as requested by the user
    reset_energy("COM4", 64)
