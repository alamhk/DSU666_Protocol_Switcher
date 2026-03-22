# Chint DDSU666 Meter Management Guide

This guide details how to interact with the Chint **DDSU666** single-phase smart meter, from initial DL/T 645 reading to Modbus RTU switching and advanced operations.

> [!WARNING]
> **Compatibility Note**: This tool and guide have not been tested with any specific brands of PV Inverters. Users are advised to perform their own research and testing before integration with solar energy systems.

---

## 1. Initial Reading (DL/T 645 Protocol)
By default, the meter uses the **DL/T 645-2007** protocol, common in Chinese electricity systems.

### Communication Settings:
- **Baud Rate**: 2400 bps
- **Parity**: Even (E)
- **Data Bits**: 8
- **Stop Bits**: 1 (8E1)

### Identification:
- **Address**: A 12-digit BCD address (e.g., `123456789012`), usually derived from the serial number.
- **Broadcast Address**: `AAAAAAAAAAAA` can be used for reading if only one meter is on the bus.

### Reading Data:
Use `read_ddsu666_645.py` to fetch basic data like voltage and energy in this mode.

---

## 2. Switching to Modbus RTU
To use the meter with standard industrial systems, you must switch it to **Modbus RTU** mode.

### Steps to Switch:
1. **Prepare the Command**: You must send a specialized DL/T 645 "Write" command while the meter is still in 645 mode.
2. **Command Format (Hex)**:
   `68 [ADDR_REV] 68 14 0E 33 33 35 3D 35 33 33 33 33 33 33 33 33 33 [CS] 16`
   - `[ADDR_REV]`: Your meter address in reversed byte order.
   - `[CS]`: Checksum of the frame.
3. **Execution**: Run `ddsu666_protocol_tool.py`.
4. **Verification**: 
   - Observe the meter display. The text **"DL/T 645"** should change to **"Modbus"**.
   - The next screen will show the new **Modbus ID** (e.g., `064`) and **Baud Rate** (e.g., `baud-3` for 9600).

---

## 3. Modbus RTU Communication
Once switched, the meter follows standard Modbus RTU rules.

### Communication Settings:
- **Baud Rate**: 9600 bps (default after switch)
- **Parity**: None (N)
- **Data Bits**: 8
- **Stop Bits**: 2 (8N2) — *Crucial: 8N2 is standard for Modbus without parity.*

### Register Map (Partial):
All values below use **Function Code 03** and are **Float32** (2 registers each).

| Register (Hex) | Parameter | Unit |
| :--- | :--- | :--- |
| `0x2000` | Voltage (U) | V |
| `0x2002` | Current (I) | A |
| `0x2004` | Active Power (P) | kW |
| `0x200E` | Frequency (F) | Hz |
| `0x4000` | Active Energy (Import) | kWh |
| `0x400A` | Reverse Energy | kWh |

---

## 4. Advanced Configuration (Modbus)

### Reset Energy Counter:
To clear the total energy count (Active and Reverse) to zero:
- **Target**: Write `1` to Register `0x0002`.
- **Method**: Use **Function Code 16** (Write Multiple Registers).
- **Script**: `ddsu666_reset_meter_modbus.py`.

### Change Modbus ID:
- **Target**: Register `0x0006`.
- **Value**: New ID (1-247).
- **Method**: Write (Function 10H/16).

### Change Baud Rate:
- **Target**: Register `0x000C`.
- **Settings**: 
  - `0`: 1200
  - `1`: 2400
  - `2`: 4800
  - `3`: 9600 (Default)

### Switch Back to DL/T 645:
If you need to revert the meter for testing or verification:
- **Target**: Write `1` to Register `0x0005`.
- **Script**: `ddsu666_protocol_tool.py`.
- **Effect**: The meter will immediately stop responding to Modbus and return to DL/T 645 mode.

---
## 5. References & Credits
- **Research on Protocol Switching**: Special thanks to **Ahchor** for providing the foundational research and method for switching the DDSU666 protocol. 
  - [Reference Article (Chinese)](https://www.alihai5.com/post/IOT%2FDDSU666%E5%9E%8B%E5%8D%95%E7%9B%B8%E7%94%B5%E5%AD%90%E5%BC%8F%E7%94%B5%E8%83%BD%E8%A1%A8%E5%88%87%E6%8D%A2%E9%80%9A%E8%AE%AF%E5%8D%8F%E8%AE%AE)
- **Tool Refinement**: Research and code optimization by **Antigravity AI**.
