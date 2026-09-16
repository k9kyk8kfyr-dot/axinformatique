AXinfo Ultimate v19 — Dynamic iPhone + Windows PC Bridge

OFFLINE FIRST
- AXinfo on the phone works without Internet.
- AXinfo on the PC works without Internet.
- Live phone <-> PC sync uses local Wi-Fi only; both devices must be on the same local network for live sync.
- If they are far apart, use the backup/restore JSON file workflow instead of live sync.

WINDOWS
1) Extract the ZIP.
2) Double-click START_AXinfo_PC.bat.
3) It starts AXinfo_PC_Bridge.py with Python 3.
4) The bridge is compatible with older Python 3 versions and does not require third-party packages.
5) If Windows Firewall asks, allow Private networks.
6) The console shows PC address and Pairing token.

PHONE
- In AXinfo Settings, enter the PC address and Pairing token.
- Save connection.
- Use Send Phone -> PC or Get PC -> Phone.

SECURITY
- Keep the AXinfo folder private.
- The token is stored in axinfo_pc_token.txt.
- Sync is explicit; it does not silently overwrite data.
