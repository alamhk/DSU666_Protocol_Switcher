# DDSU666 Protocol Switcher

This repository provides tools and documentation for managing the **Chint (Zhengtai) DSU666** single-phase smart meter. Specifically, it addresses the common issue where Chinese domestic versions of the meter default to the **DL/T 645** protocol, making them incompatible with standard **Modbus RTU** industrial systems.

## Key Features
- **Protocol Migration**: Bidirectional switching between DL/T 645 and Modbus RTU.
- **Auto-Discovery**: Automatic scanning of baud rates and addresses to find the meter.
- **Energy Management**: Utility to reset energy counters via Modbus.
- **Comprehensive Documentation**: Detailed guides in English and Traditional Chinese.

## Why this tool?
The Chinese version of the **DDSU666** predominantly uses the DL/T 645-2007 protocol. Most home automation and industrial gateways (like Home Assistant, ESPHome, or PLC) require Modbus RTU. This utility allows you to "unlock" the Modbus capability using simple Python scripts.

> [!WARNING]
> This tool has not been tested with any specific brands of PV Inverters. Use it at your own risk and perform your own research before connecting to your solar system.

## Quick Start
1. **Switch Protocol**:
   ```powershell
   python dsu666_protocol_tool.py
   ```
   The tool will scan for your meter and prompt you to switch modes.
2. **Reset Energy**:
   ```powershell
   python reset_meter_modbus.py
   ```

## Documentation
- [Management Guide (English)](docs/DDSU666_Guide.md)
- [管理指南 (繁體中文)](docs/DDSU666_guide_TC.md)

---

## 鳴謝 (Acknowledgments)
- 特別鳴謝 **Ahchor 師兄** 提供 DSU666 協議切換的關鍵研究資料 ([參考鏈接](https://www.alihai5.com/post/IOT%2FDDSU666%E5%9E%8B%E5%8D%95%E7%9B%B8%E7%94%B5%E5%AD%90%E5%BC%8F%E7%94%B5%E8%83%BD%E8%A1%A8%E5%88%87%E6%8D%A2%E9%80%9A%E8%AE%AF%E5%8D%8F%E8%AE%AE))。
- 代碼與文檔的優化及研究由 **Google Antigravity AI** 協助完成。

Special thanks to **Ahchor** for providing the critical research for DSU666 protocol switching. Much appreciation also to **Google Antigravity AI** for the assistance in research and code refinement for this project.

---

# 正泰 DSU666 協議切換工具 (DSU666 Protocol Switcher)

本倉庫提供了管理 **正泰 (Chint) DSU666** 單相智能電錶的工具與文檔。它主要解決了一個常見問題：中國國內版本的電錶預設使用 **DL/T 645** 協議，導致無法直接與標準的 **Modbus RTU** 工業系統兼容。

## 主要功能
- **協議轉換**：支援 DL/T 645 與 Modbus RTU 之間的雙向切換。
- **自動偵測**：自動掃描波特率與地址以尋找電錶。
- **能量管理**：透過 Modbus 重置電量計數器的工具。
- **完整文檔**：提供英文與繁體中文的詳細操作指南。

## 開發背景
**DDSU666** 的中國版通常預設為 DL/T 645-2007 協議。而大多數智能家居與工業網關（如 Home Assistant、ESPHome 或 PLC）通常要求使用 Modbus RTU。本工具讓您可以使用簡單的 Python 腳本「解鎖」電錶的 Modbus 功能。

> [!WARNING]
> **免責聲明**：本工具尚未在任何品牌的太陽能逆變器 (PV Inverter) 上進行過實際測試。請在連接到您的太陽能系統前自行研究並承擔風險。

## 快速開始
1. **切換協議**：
   ```powershell
   python dsu666_protocol_tool.py
   ```
   工具將掃描您的電錶並提示您切換模式。
2. **重置電量**：
   ```powershell
   python reset_meter_modbus.py
   ```

## 項目文檔
- [Management Guide (English)](docs/DDSU666_Guide.md)
- [管理指南 (繁體中文)](docs/DDSU666_guide_TC.md)
