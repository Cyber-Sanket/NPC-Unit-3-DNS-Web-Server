# Screenshot Checklist and Practical Verification Guide
**Student Name:** Sanket Aher  
**PRN:** 2125UCSM1080  
**Department:** Computer Science and Engineering – Cyber Security  
**University:** Sanjivani University, Kopargaon  
**Subject:** Networking Protocols and Communication (NPC – Unit 3)  
**Project:** Configure a DNS Server and Web Server Using Cisco Packet Tracer  

---

## 1. Overview and Academic Integrity Policy

This directory contains standardized placeholders and will house the verified practical screenshots captured directly by **Sanket Aher** from Cisco Packet Tracer. 

To maintain strict academic integrity:
1. Previous student screenshots from the reference repository have been archived to `original_reference/screenshots_original/` for attribution and comparison only.
2. The report generators (`build_pdf.py` and `build_docx.py`) link directly to the 10 files in this directory (`screenshots/`).
3. You can replace each placeholder file with your actual screenshot from Packet Tracer using the exact filenames listed below.
4. Once you replace any or all images, re-run `python build_pdf.py` and `python build_docx.py` to automatically update the official submission PDF and DOCX reports.

---

## 2. Screenshot Checklist & Capture Instructions

| Fig # | Filename | Target Window / Screen | What to Capture in Cisco Packet Tracer |
| :--- | :--- | :--- | :--- |
| **01** | `01_topology.png` | **Logical Workspace** | Switch0 (2960), DNS Server, Web Server, PC0, PC1. Ensure all 4 links show green link lights and interface labels (`Fa0/1` through `Fa0/4`). |
| **02** | `02_dns_ip_config.png` | **DNS Server > Desktop > IP Configuration** | Static IP: `192.168.1.2`, Subnet Mask: `255.255.255.0`. |
| **03** | `03_dns_service_config.png` | **DNS Server > Services > DNS** | DNS Service radio button set to **On**, and the Resource Record table showing Name: `www.npcunit3.com`, Type: `A Record`, Address: `192.168.1.3`. |
| **04** | `04_web_ip_config.png` | **Web Server > Desktop > IP Configuration** | Static IP: `192.168.1.3`, Subnet Mask: `255.255.255.0`, DNS Server: `192.168.1.2`. |
| **05** | `05_http_service_config.png` | **Web Server > Services > HTTP** | HTTP and HTTPS services **On**, and the `index.html` file in the File Manager displaying custom webpage code for Sanket Aher. |
| **06** | `06_pc0_ip_config.png` | **PC0 > Desktop > IP Configuration** | Static IP: `192.168.1.10`, Subnet Mask: `255.255.255.0`, DNS Server: `192.168.1.2`. |
| **07** | `07_pc1_ip_config.png` | **PC1 > Desktop > IP Configuration** | Static IP: `192.168.1.11`, Subnet Mask: `255.255.255.0`, DNS Server: `192.168.1.2`. |
| **08** | `08_ping_tests.png` | **PC0 > Desktop > Command Prompt** | Execution and output of: <br>1. `ping 192.168.1.2` (DNS Server) - 4 replies, 0% loss.<br>2. `ping 192.168.1.3` (Web Server) - 4 replies, 0% loss. |
| **09** | `09_dns_lookup.png` | **PC0 > Desktop > Command Prompt** | Execution and output of: <br>`nslookup www.npcunit3.com` showing Server `192.168.1.2` and Address `192.168.1.3`. |
| **10** | `10_website_browser.png` | **PC0 > Desktop > Web Browser** | Browser URL bar with `http://www.npcunit3.com` loaded, rendering the personalized HTML welcome page showing Sanket Aher and PRN 2125UCSM1080. |

---

## 3. Best Practices for Taking Screenshots in Packet Tracer

1. **Resolution:** Capture at standard 1080p (or use the Windows Snipping Tool: `Win + Shift + S`).
2. **Window Cropping:** Capture the dialog window cleanly with its title bar visible (e.g., showing "PC0", "DNS Server", or "Web Server").
3. **Format:** Save in standard `.png` format.
4. **Dimensions:** Standard aspect ratio (16:9 or 4:3), minimum width 900px for sharp printing in A4 reports.
5. **Rebuilding Reports:** After pasting your images into `screenshots/`, run:
   ```bash
   python build_pdf.py
   python build_docx.py
   ```
   Both documents will immediately render your actual captures!
