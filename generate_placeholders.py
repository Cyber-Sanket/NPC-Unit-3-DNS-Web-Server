# -*- coding: utf-8 -*-
"""
generate_placeholders.py
Generates clean, standardized placeholder graphics for the 10 required screenshots
in the NPC Unit 3 practical assignment for Sanket Aher (PRN 2125UCSM1080).
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(HERE, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

PLACEHOLDERS = [
    {
        "filename": "01_topology.png",
        "num": "1",
        "title": "Complete Packet Tracer Network Topology",
        "device": "Cisco Packet Tracer Logical Workspace",
        "guidance": "Capture the full logical workspace showing Switch0 (2960), DNS Server, Web Server, PC0, and PC1 with all green link lights active and interface labels visible.",
        "expected": "All 4 copper straight-through connections showing active link state (green markers).",
    },
    {
        "filename": "02_dns_ip_config.png",
        "num": "2",
        "title": "DNS Server - IP Configuration Window",
        "device": "DNS Server > Desktop > IP Configuration",
        "guidance": "Capture the IP Configuration dialog on the DNS Server showing Static IP assignment: IP Address 192.168.1.2 and Subnet Mask 255.255.255.0.",
        "expected": "IP: 192.168.1.2 | Mask: 255.255.255.0 | Gateway: blank | DNS Server: blank (or 127.0.0.1)",
    },
    {
        "filename": "03_dns_service_config.png",
        "num": "3",
        "title": "DNS Server - DNS Service & A Record Configuration",
        "device": "DNS Server > Services > DNS",
        "guidance": "Capture the DNS service tab showing DNS Service radio set to 'On' and the Resource Records table containing Name: www.npcunit3.com, Type: A Record, Address: 192.168.1.3.",
        "expected": "Service: ON | Name: www.npcunit3.com | Type: A Record | IP: 192.168.1.3",
    },
    {
        "filename": "04_web_ip_config.png",
        "num": "4",
        "title": "Web Server - IP Configuration Window",
        "device": "Web Server > Desktop > IP Configuration",
        "guidance": "Capture the IP Configuration dialog on the Web Server showing Static IP assignment: IP Address 192.168.1.3, Subnet Mask 255.255.255.0, and DNS Server: 192.168.1.2.",
        "expected": "IP: 192.168.1.3 | Mask: 255.255.255.0 | DNS Server: 192.168.1.2",
    },
    {
        "filename": "05_http_service_config.png",
        "num": "5",
        "title": "Web Server - HTTP Service & index.html Editor",
        "device": "Web Server > Services > HTTP",
        "guidance": "Capture the HTTP service dialog showing HTTP and HTTPS radio buttons set to 'On', and the file manager showing index.html edited with Sanket Aher's details.",
        "expected": "HTTP: ON | HTTPS: ON | File: index.html customized for Sanket Aher",
    },
    {
        "filename": "06_pc0_ip_config.png",
        "num": "6",
        "title": "PC0 - IP Configuration Window",
        "device": "PC0 > Desktop > IP Configuration",
        "guidance": "Capture the IP Configuration dialog on PC0 showing Static IP assignment: IP Address 192.168.1.10, Subnet Mask 255.255.255.0, and DNS Server 192.168.1.2.",
        "expected": "IP: 192.168.1.10 | Subnet Mask: 255.255.255.0 | DNS Server: 192.168.1.2",
    },
    {
        "filename": "07_pc1_ip_config.png",
        "num": "7",
        "title": "PC1 - IP Configuration Window",
        "device": "PC1 > Desktop > IP Configuration",
        "guidance": "Capture the IP Configuration dialog on PC1 showing Static IP assignment: IP Address 192.168.1.11, Subnet Mask 255.255.255.0, and DNS Server 192.168.1.2.",
        "expected": "IP: 192.168.1.11 | Subnet Mask: 255.255.255.0 | DNS Server: 192.168.1.2",
    },
    {
        "filename": "08_ping_tests.png",
        "num": "8",
        "title": "PC0 - ICMP Ping Connectivity Tests",
        "device": "PC0 > Desktop > Command Prompt",
        "guidance": "Capture the Command Prompt window on PC0 showing successful ping commands: 'ping 192.168.1.2' (DNS Server) and 'ping 192.168.1.3' (Web Server) with 0% packet loss.",
        "expected": "4 packets transmitted, 4 received, 0% packet loss, RTT < 1ms, TTL = 128",
    },
    {
        "filename": "09_dns_lookup.png",
        "num": "9",
        "title": "PC0 - DNS Resolution via nslookup",
        "device": "PC0 > Desktop > Command Prompt",
        "guidance": "Capture the Command Prompt on PC0 showing 'nslookup www.npcunit3.com' successfully resolving to 192.168.1.3 via default server 192.168.1.2.",
        "expected": "Server: 192.168.1.2 | Address: 192.168.1.2 | Name: www.npcunit3.com | Address: 192.168.1.3",
    },
    {
        "filename": "10_website_browser.png",
        "num": "10",
        "title": "PC0 - Web Browser Accessing Domain URL",
        "device": "PC0 > Desktop > Web Browser",
        "guidance": "Capture the Packet Tracer Web Browser on PC0 with URL 'http://www.npcunit3.com' loaded, displaying the custom HTML welcome page for Sanket Aher.",
        "expected": "URL Bar: http://www.npcunit3.com | Status: 200 OK | Rendered HTML with student information",
    },
]

def create_placeholder_card(data):
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    # Background card
    bg = FancyBboxPatch((0.15, 0.15), 9.7, 5.5,
                        boxstyle="round,pad=0.04,rounding_size=0.15",
                        linewidth=2.0, facecolor="#F8FAFC", edgecolor="#CBD5E1")
    ax.add_patch(bg)

    # Header bar
    header = FancyBboxPatch((0.15, 4.75), 9.7, 0.9,
                           boxstyle="round,pad=0.04,rounding_size=0.12",
                           linewidth=0, facecolor="#1F3864")
    ax.add_patch(header)
    # Square bottom edges of header
    ax.add_patch(Rectangle((0.15, 4.75), 9.7, 0.4, facecolor="#1F3864", linewidth=0))

    # Header Text
    ax.text(0.4, 5.25, f"FIGURE {data['num']}: {data['title'].upper()}",
            fontsize=11.5, fontweight="bold", color="#FFFFFF", va="center")
    ax.text(9.5, 5.25, "[ PLACEHOLDER ]",
            fontsize=9.5, fontweight="bold", color="#FDBA74", ha="right", va="center")

    # Sub-header bar
    ax.add_patch(Rectangle((0.15, 4.3), 9.7, 0.45, facecolor="#EEF2F6", edgecolor="none"))
    ax.text(0.4, 4.52, f"Target Path: {data['device']}",
            fontsize=9.5, fontweight="bold", color="#2E5496", va="center")
    ax.text(9.5, 4.52, "Student: Sanket Aher | PRN: 2125UCSM1080",
            fontsize=8.5, color="#475569", ha="right", va="center")

    # Center placeholder box (simulating where the screenshot goes)
    inner_box = FancyBboxPatch((0.5, 1.3), 9.0, 2.75,
                              boxstyle="round,pad=0.03,rounding_size=0.08",
                              linewidth=1.2, facecolor="#FFFFFF", edgecolor="#94A3B8",
                              linestyle="--")
    ax.add_patch(inner_box)

    # Center icon and text
    ax.text(5.0, 3.25, "[ Screenshot Capture Placeholder ]",
            ha="center", va="center", fontsize=13, fontweight="bold", color="#1E293B")
    ax.text(5.0, 2.80, f"Filename: {data['filename']}",
            ha="center", va="center", fontsize=10.5, fontfamily="monospace", color="#0F766E",
            bbox=dict(boxstyle="round,pad=0.25", fc="#F0FDFA", ec="#CCFBF1"))

    # Instruction inside inner box
    ax.text(5.0, 2.25, data['guidance'],
            ha="center", va="center", fontsize=8.8, color="#334155", wrap=True,
            style="italic")

    # Expected value callout
    ax.text(5.0, 1.65, f"Required Verification Content:\n{data['expected']}",
            ha="center", va="center", fontsize=8.5, color="#1E3A8A", fontweight="semibold")

    # Bottom footer instruction
    ax.text(5.0, 0.75,
            f"REPLACEMENT INSTRUCTIONS: Save your Cisco Packet Tracer screenshot as '{data['filename']}'\n"
            f"in the 'screenshots/' folder and rebuild reports via 'python build_pdf.py' / 'python build_docx.py'.",
            ha="center", va="center", fontsize=8.2, color="#64748B", style="normal")

    out_path = os.path.join(SCREENSHOTS_DIR, data['filename'])
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {data['filename']}")

def main():
    print(f"Generating 10 standard placeholder cards in {SCREENSHOTS_DIR}...")
    for item in PLACEHOLDERS:
        create_placeholder_card(item)
    print("All placeholders generated successfully!")

if __name__ == "__main__":
    main()
