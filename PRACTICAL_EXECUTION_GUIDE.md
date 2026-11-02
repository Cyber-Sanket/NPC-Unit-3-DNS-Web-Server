# Cisco Packet Tracer Practical Execution & Verification Guide
**Course:** Networking Protocols and Communication (NPC – Unit 3)  
**Project Title:** Configure a DNS Server and Web Server Using Cisco Packet Tracer  
**Student Name:** Sanket Aher  
**PRN:** 2125UCSM1080  
**Department:** Computer Science and Engineering – Cyber Security  
**University:** Sanjivani University, Kopargaon  

---

## 1. Overview & File Integrity

This guide provides exhaustive, step-by-step instructions for opening, configuring, and verifying the Cisco Packet Tracer simulation for Unit 3.

- **Primary Project File:** `NPC_Unit_3_DNS_Web_Server.pkt` (Ready to open in Cisco Packet Tracer 8.x / 9.x)
- **Unmodified Backup File:** `backup/NPC_Unit_3_DNS_Web_Server_ORIGINAL.pkt` (Preserved intact to ensure zero file corruption)
- **Report Compilers:** `python generate_reports.py` (Compiles both PDF and DOCX reports automatically)

---

## 2. Network Topology & Addressing Architecture

### 2.1 Topology Overview
- **Central Device:** Cisco Catalyst 2960-24TT Layer-2 Switch (`Switch0`)
- **End Devices:** 2 Client PCs (`PC0`, `PC1`), 1 DNS Server (`DNS Server`), 1 Web Server (`Web Server`)
- **Subnet:** Classless IPv4 Private Subnet `192.168.1.0/24` (Subnet Mask: `255.255.255.0`)
- **Cables:** Category 5e Copper Straight-Through Cables (EIA/TIA 568B)

### 2.2 Master IP Addressing Table
| Device ID | Interface | IPv4 Address | Subnet Mask | Default Gateway | DNS Server Pointer | Switch Port |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Switch0** | VLAN 1 | *Unmanaged (L2)* | *N/A* | *N/A* | *N/A* | – |
| **DNS Server** | FastEthernet0 | `192.168.1.2` | `255.255.255.0` | *None (Blank)* | `127.0.0.1` | `Fa0/1` |
| **Web Server** | FastEthernet0 | `192.168.1.3` | `255.255.255.0` | *None (Blank)* | `192.168.1.2` | `Fa0/2` |
| **PC0** | FastEthernet0 | `192.168.1.10` | `255.255.255.0` | *None (Blank)* | `192.168.1.2` | `Fa0/3` |
| **PC1** | FastEthernet0 | `192.168.1.11` | `255.255.255.0` | *None (Blank)* | `192.168.1.2` | `Fa0/4` |

---

## 3. Step-by-Step Configuration Guide

### Step 1: Open the Project in Cisco Packet Tracer
1. Launch **Cisco Packet Tracer** (version 8.0, 8.2, 9.0 or higher).
2. Click **File > Open** (or press `Ctrl + O`).
3. Select `NPC_Unit_3_DNS_Web_Server.pkt` from this project directory.
4. Verify that all 4 links display green triangle indicators (indicating active Spanning Tree Protocol forwarding).

---

### Step 2: Configure the DNS Server
1. Click on the **DNS Server** icon in the logical workspace.
2. Select the **Desktop** tab, then click **IP Configuration**:
   - **IP Configuration:** Select `Static`
   - **IPv4 Address:** `192.168.1.2`
   - **Subnet Mask:** `255.255.255.0`
   - **Default Gateway:** *Leave blank*
   - **DNS Server:** `127.0.0.1` (or leave blank)
3. Navigate to the **Services** tab in the top menu:
   - Select **DNS** from the left navigation panel.
   - Set **DNS Service** to **ON**.
   - In the **Name** input box: enter `www.npcunit3.com`
   - In the **Type** dropdown: select `A Record`
   - In the **Address** input box: enter `192.168.1.3`
   - Click the **Add** button.
   - Confirm that the record `www.npcunit3.com -> 192.168.1.3` appears in the table below.

---

### Step 3: Configure the Web Server
1. Click on the **Web Server** icon in the logical workspace.
2. Select the **Desktop** tab, then click **IP Configuration**:
   - **IP Configuration:** Select `Static`
   - **IPv4 Address:** `192.168.1.3`
   - **Subnet Mask:** `255.255.255.0`
   - **Default Gateway:** *Leave blank*
   - **DNS Server:** `192.168.1.2`
3. Navigate to the **Services** tab:
   - Select **HTTP** from the left panel.
   - Verify that both **HTTP** and **HTTPS** radio buttons are set to **ON**.
   - Under the file manager list, find `index.html` and click **(edit)**.
   - Replace the default code with the customized student webpage code below:

```html
<!DOCTYPE html>
<html>
<head>
    <title>NPC Unit 3 - DNS and Web Server Configuration</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f0f4f8; color: #1e293b; margin: 0; padding: 25px; }
        .card { max-width: 750px; margin: 30px auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.08); border-top: 5px solid #1F3864; }
        h1 { color: #1F3864; font-size: 24px; margin-bottom: 6px; }
        h2 { color: #2E5496; font-size: 16px; margin-top: 0; font-weight: 600; }
        .status-badge { display: inline-block; background-color: #dcfce7; color: #15803d; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; margin-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; font-size: 13px; }
        th { background-color: #1F3864; color: #ffffff; }
        tr:nth-child(even) { background-color: #f8fafc; }
        .footer { margin-top: 25px; font-size: 11px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <span class="status-badge">&#10004; SERVICE OPERATIONAL</span>
        <h1>Welcome to My Web Server!</h1>
        <h2>NPC Unit 3: DNS and Web Server Configuration Practical</h2>
        <p>This website is hosted on <b>Web Server (192.168.1.3)</b> over HTTP Port 80 and resolved via <b>DNS Server (192.168.1.2)</b> using the domain name <b>www.npcunit3.com</b>.</p>
        
        <h3>Student Information & Verification</h3>
        <table>
            <tr><th>Field</th><th>Verification Details</th></tr>
            <tr><td><b>Student Name</b></td><td>Sanket Aher</td></tr>
            <tr><td><b>PRN</b></td><td>2125UCSM1080</td></tr>
            <tr><td><b>Department</b></td><td>Computer Science and Engineering – Cyber Security</td></tr>
            <tr><td><b>Semester / Year</b></td><td>Second Year / Third Semester</td></tr>
            <tr><td><b>Course / Subject</b></td><td>Networking Protocols and Communication (NPC)</td></tr>
            <tr><td><b>University</b></td><td>Sanjivani University, Kopargaon</td></tr>
            <tr><td><b>Configured Domain</b></td><td>www.npcunit3.com</td></tr>
        </table>
        
        <div class="footer">
            Sanjivani University &bull; School of Computing, Engineering & Technology &bull; CSE Cyber Security
        </div>
    </div>
</body>
</html>
```
4. Click **Save** and confirm overwrite (`Yes`).

---

### Step 4: Configure the Client Workstations (PC0 and PC1)
1. Click **PC0**:
   - Go to **Desktop > IP Configuration**.
   - Set **IPv4 Address:** `192.168.1.10`
   - Set **Subnet Mask:** `255.255.255.0`
   - Set **DNS Server:** `192.168.1.2`
2. Click **PC1**:
   - Go to **Desktop > IP Configuration**.
   - Set **IPv4 Address:** `192.168.1.11`
   - Set **Subnet Mask:** `255.255.255.0`
   - Set **DNS Server:** `192.168.1.2`

---

## 4. Verification and Empirical Testing Procedure

### Test 1: Layer-3 ICMP Connectivity (PC0)
1. On **PC0**, go to **Desktop > Command Prompt**.
2. Run the ping test to the DNS Server:
   ```cmd
   ping 192.168.1.2
   ```
   *Expected Output:* 4 packets sent, 4 received, 0% loss, round-trip time `<1ms`, TTL = 128.
3. Run the ping test to the Web Server:
   ```cmd
   ping 192.168.1.3
   ```
   *Expected Output:* 4 packets sent, 4 received, 0% loss, round-trip time `<1ms`, TTL = 128.

### Test 2: Layer-3 ICMP Connectivity (PC1)
1. On **PC1**, open **Desktop > Command Prompt**.
2. Run:
   ```cmd
   ping 192.168.1.2
   ping 192.168.1.3
   ```
   *Expected Output:* 4 replies from each server with 0% packet loss.

### Test 3: DNS Name Resolution Testing (nslookup)
1. On **PC0**, open **Desktop > Command Prompt**.
2. Execute:
   ```cmd
   nslookup www.npcunit3.com
   ```
   *Expected Output:*
   ```text
   Server:  192.168.1.2
   Address: 192.168.1.2

   Name:    www.npcunit3.com
   Address: 192.168.1.3
   ```

### Test 4: End-to-End Web Access via Domain Name
1. On **PC0**, open **Desktop > Web Browser**.
2. In the URL bar, type:
   ```text
   http://www.npcunit3.com
   ```
   (or simply `www.npcunit3.com`)
3. Click **Go** (or press Enter).
4. *Expected Result:* The browser renders the styled welcome webpage displaying **Sanket Aher** and **PRN: 2125UCSM1080**.

---

## 5. Capturing and Updating Personal Screenshots

Follow the [Screenshot Guide](screenshots/SCREENSHOT_GUIDE.md) to take the 10 verified practical captures from Packet Tracer:
1. `01_topology.png` - Full workspace topology with active green lights.
2. `02_dns_ip_config.png` - DNS Server IP config dialog.
3. `03_dns_service_config.png` - DNS service tab showing A-record.
4. `04_web_ip_config.png` - Web Server IP config dialog.
5. `05_http_service_config.png` - HTTP service tab and `index.html`.
6. `06_pc0_ip_config.png` - PC0 IP config dialog.
7. `07_pc1_ip_config.png` - PC1 IP config dialog.
8. `08_ping_tests.png` - PC0 command prompt ping outputs.
9. `09_dns_lookup.png` - PC0 command prompt nslookup output.
10. `10_website_browser.png` - PC0 web browser showing the loaded webpage.

After saving your `.png` files into `screenshots/`, re-run the build script:
```bash
python generate_reports.py
```
This automatically updates both `NPC_Unit_3_Sanket_Aher.pdf` and `NPC_Unit_3_Sanket_Aher.docx` with your captures.
