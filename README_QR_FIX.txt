AXinfo Ultimate — QR PC ↔ iPhone pairing fix

1) On Windows, connect the PC and iPhone to the SAME Wi‑Fi network.
2) Run START_AXinfo_PC.bat.
3) Open the displayed /bridge.html address on the PC.
4) The QR code is generated LOCALLY by the PC. Internet is NOT required for QR generation.
5) On iPhone, use the normal Camera app to scan the QR code. Tap the AXinfo link that appears.
6) Open AXinfo from that link. The pairing token is saved automatically.
7) Return to AXinfo and the PC status should become connected when both devices are on the same Wi‑Fi.

Important:
- Do NOT use a mobile-data connection between the devices; they must be on the same local network.
- Windows Firewall must allow Python/port 8765 on the Private network.
- If Windows asks about Firewall access, allow it for Private networks.
- The QR image no longer depends on an online QR CDN.
- The QR scanner inside AXinfo is still available for normal product/barcode scanning.
