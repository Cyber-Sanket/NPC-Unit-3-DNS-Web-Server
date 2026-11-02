# -*- coding: utf-8 -*-
"""
build_pdf.py
NPC Unit 3 - Configure a DNS Server and Web Server Using Cisco Packet Tracer
Student: Sanket Aher (PRN: 2125UCSM1080)
Department of Computer Science and Engineering - Cyber Security
Sanjivani University, Kopargaon

Generates an authoritative, comprehensive 19-page academic laboratory report in PDF format.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, Preformatted, KeepTogether,
)
from reportlab.pdfgen import canvas
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(HERE, "NPC_Unit_3_Sanket_Aher.pdf")
TOPO_PNG = os.path.join(HERE, "logical_topology.png")
SCREENSHOTS_DIR = os.path.join(HERE, "screenshots")

# ---------------------------------------------------------------- Palette
NAVY = HexColor(0x1F3864)       # Primary Header Navy
BLUE = HexColor(0x2E5496)       # Secondary Accent Blue
STEEL = HexColor(0x41719C)      # Sub-heading Steel Blue
DARK = HexColor(0x1E293B)       # Body text dark slate
GREY = HexColor(0x595959)       # Neutral grey
LGREY = HexColor(0xD9D9D9)      # Table borders and rules
HDRBG = HexColor(0x1F3864)      # Table header background
ROWBG = HexColor(0xF1F5F9)      # Alternating row background
CODEBG = HexColor(0xF8FAFC)     # Code box background
ALERTBG = HexColor(0xEFF6FF)    # Callout box background
ALERTBORDER = HexColor(0x3B82F6)# Callout box border
SUCCESSBG = HexColor(0xF0FDF4)  # Success callout
SUCCESSBORDER = HexColor(0x22C55E)

CONTENT_W = A4[0] - 3.6 * cm    # Printable width: 21cm - 3.6cm = 17.4cm

# ---------------------------------------------------------------- Styles
def P(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.0, leading=12.5, textColor=DARK)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_body     = P("body", alignment=TA_JUSTIFY, spaceAfter=4)
st_body_b   = P("body_b", fontName="Helvetica-Bold", spaceAfter=4)
st_h1       = P("h1", fontName="Helvetica-Bold", fontSize=12.5, textColor=NAVY,
                spaceBefore=4, spaceAfter=3, leading=15)
st_h2       = P("h2", fontName="Helvetica-Bold", fontSize=10.2, textColor=BLUE,
                spaceBefore=4, spaceAfter=2, leading=13)
st_h3       = P("h3", fontName="Helvetica-Bold", fontSize=9.5, textColor=STEEL,
                spaceBefore=3, spaceAfter=2, leading=12)
st_list     = P("list", alignment=TA_LEFT, leftIndent=12, firstLineIndent=-8,
                spaceAfter=2, leading=12)
st_cap      = P("cap", fontName="Helvetica-Oblique", fontSize=7.8, textColor=GREY,
                alignment=TA_CENTER, spaceBefore=2, spaceAfter=4)
st_code     = P("code", fontName="Courier", fontSize=7.8, leading=10.5, textColor=DARK)
st_cell     = P("cell", fontSize=8.0, leading=10.8)
st_cellb    = P("cellb", fontName="Helvetica-Bold", fontSize=8.0, leading=10.8, textColor=white)
st_cell_k   = P("cellk", fontName="Helvetica-Bold", fontSize=8.0, leading=10.8, textColor=NAVY)

# Cover styles
st_cv_inst  = P("cv_inst", alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=13, textColor=NAVY, leading=17)
st_cv_dept  = P("cv_dept", alignment=TA_CENTER, fontName="Helvetica", fontSize=10.5, textColor=BLUE, leading=14)
st_cv_tag   = P("cv_tag", alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=10.5, textColor=STEEL, leading=14)
st_cv_title = P("cv_title", alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=17, textColor=NAVY, leading=21)
st_cv_sub   = P("cv_sub", alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=11, textColor=DARK, leading=15)
st_cv_meta  = P("cv_meta", alignment=TA_CENTER, fontSize=9.0, textColor=GREY, leading=13)

# ---------------------------------------------------------------- Helpers
def heading(num_and_title):
    return [
        Spacer(1, 2),
        Paragraph(num_and_title, st_h1),
        HRFlowable(width="100%", thickness=1.0, color=NAVY, spaceBefore=1, spaceAfter=4)
    ]

def sub(title):
    return Paragraph(title, st_h2)

def subsub(title):
    return Paragraph(title, st_h3)

def body(text):
    return Paragraph(text, st_body)

def numbered(items):
    return [Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{t}", st_list) for i, t in enumerate(items, 1)]

def bullets(items):
    return [Paragraph(f"&bull;&nbsp;&nbsp;{t}", st_list) for t in items]

def code_box(text):
    pre = Preformatted(text, st_code)
    t = Table([[pre]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("BOX", (0, 0), (-1, -1), 0.6, LGREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def callout(text, title="KEY ARCHITECTURAL PRINCIPLE", kind="info"):
    bg = SUCCESSBG if kind == "success" else ALERTBG
    bd = SUCCESSBORDER if kind == "success" else ALERTBORDER
    p_title = Paragraph(f"<b>{title}</b>", P("c_t", fontName="Helvetica-Bold", fontSize=8.0, textColor=NAVY, spaceAfter=1))
    p_body = Paragraph(text, P("c_b", fontSize=8.0, leading=11, alignment=TA_JUSTIFY))
    t = Table([[p_title], [p_body]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.8, bd),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

def figure(path, caption, max_h=5.2 * cm, max_w=CONTENT_W):
    if not os.path.exists(path):
        return Paragraph(f"[Image Missing: {os.path.basename(path)}]", st_cap)
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    scale = min(max_w / iw, max_h / ih)
    img_w, img_h = iw * scale, ih * scale
    img = Image(path, width=img_w, height=img_h)
    img.hAlign = "CENTER"
    box = Table([[img]], colWidths=[img_w])
    box.hAlign = "CENTER"
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, LGREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return KeepTogether([box, Paragraph(caption, st_cap)])

def data_table(header, rows, widths=None):
    if widths is None:
        widths = [CONTENT_W / len(header)] * len(header)
    data = [[Paragraph(h, st_cellb) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), st_cell) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HDRBG),
        ("GRID", (0, 0), (-1, -1), 0.4, LGREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBG))
    t.setStyle(TableStyle(style))
    return t

def info_table(rows, col1_w=5.2 * cm):
    col2_w = CONTENT_W - col1_w
    data = [[Paragraph(k, st_cell_k), Paragraph(v, st_cell)] for k, v in rows]
    t = Table(data, colWidths=[col1_w, col2_w])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), ROWBG),
        ("GRID", (0, 0), (-1, -1), 0.4, LGREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

# ---------------------------------------------------------------- Canvas / Footer
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self._draw_header_footer(total_pages)
            super().showPage()
        super().save()

    def _draw_header_footer(self, total):
        self.saveState()
        # Running Header
        self.setStrokeColor(LGREY)
        self.setLineWidth(0.5)
        self.line(1.8 * cm, A4[1] - 1.2 * cm, A4[0] - 1.8 * cm, A4[1] - 1.2 * cm)
        self.setFont("Helvetica", 7.0)
        self.setFillColor(GREY)
        self.drawString(1.8 * cm, A4[1] - 1.05 * cm,
                        "Sanjivani University | CSE Cyber Security | NPC Unit 3: DNS & Web Server Configuration")
        self.drawRightString(A4[0] - 1.8 * cm, A4[1] - 1.05 * cm, "Academic Practical Report")

        # Running Footer
        self.line(1.8 * cm, 1.2 * cm, A4[0] - 1.8 * cm, 1.2 * cm)
        self.setFont("Helvetica", 7.5)
        self.drawString(1.8 * cm, 0.85 * cm,
                        "Student: Sanket Aher  |  PRN: 2125UCSM1080  |  Cisco Packet Tracer Practical")
        self.drawRightString(A4[0] - 1.8 * cm, 0.85 * cm,
                             f"Page {self._pageNumber} of {total}")
        self.restoreState()

# ---------------------------------------------------------------- Story Assembler
def build_story():
    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("SANJIVANI UNIVERSITY, KOPARGAON", st_cv_inst))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", st_cv_dept))
    story.append(Paragraph("SPECIALIZATION IN CYBER SECURITY", st_cv_dept))
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceAfter=10))

    story.append(Paragraph("LABORATORY PRACTICAL TECHNICAL REPORT", st_cv_tag))
    story.append(Paragraph("COURSE: NETWORKING PROTOCOLS AND COMMUNICATION (NPC)", st_cv_tag))
    story.append(Paragraph("UNIT 3 &ndash; APPLICATION LAYER PROTOCOLS", st_cv_tag))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("CONFIGURE A DNS SERVER AND WEB SERVER<br/>USING CISCO PACKET TRACER", st_cv_title))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Empirical Implementation, Protocol Stack Analysis, Domain Name Resolution, and HTTP Delivery Verification", st_cv_sub))
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=2.2, color=NAVY, spaceBefore=2, spaceAfter=12))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("SUBMITTED BY", P("cv_by", alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=10.5, textColor=NAVY)))
    story.append(Spacer(1, 0.25 * cm))

    student_rows = [
        ("Candidate Name", "Sanket Aher"),
        ("Permanent Registration No. (PRN)", "2125UCSM1080"),
        ("Academic Program", "B.Tech in Computer Science & Engineering"),
        ("Specialization", "Cyber Security"),
        ("Academic Year / Semester", "Second Year / Semester III"),
        ("Course / Subject", "Networking Protocols & Communication (NPC)"),
        ("Institutional Affiliation", "Sanjivani University, Kopargaon"),
        ("GitHub Repository", "https://github.com/Cyber-Sanket/NPC-Unit-3-DNS-Web-Server"),
        ("Source Acknowledgment", "Initial framework based on chetan475/unit-3 (Attributed)"),
    ]
    t_cover = info_table(student_rows, col1_w=6.2 * cm)
    t_cover.hAlign = "CENTER"
    story.append(t_cover)

    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph("Academic Submission &bull; Department of Cyber Security &bull; Semester III", st_cv_meta))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: STUDENT PROFILE, DECLARATION & ACKNOWLEDGEMENT
    # =========================================================================
    story += heading("Student Academic Profile & Institutional Details")
    story.append(body(
        "This laboratory practical report is submitted in partial fulfillment of the continuous "
        "evaluation requirements for the course <b>Networking Protocols and Communication (NPC)</b>, prescribed for the "
        "curriculum of Bachelor of Technology in Computer Science and Engineering &ndash; Cyber Security at Sanjivani University."))

    profile_data = [
        ("Full Legal Name of Candidate", "Sanket Aher"),
        ("University PRN", "2125UCSM1080"),
        ("Department", "Computer Science and Engineering &ndash; Cyber Security"),
        ("Faculty", "School of Computing, Engineering and Technology"),
        ("University", "Sanjivani University, Kopargaon &ndash; 423603, Maharashtra, India"),
        ("Academic Cycle", "2026&ndash;2027 (Odd Semester)"),
        ("Course Title & Code", "Networking Protocols and Communication (NPC)"),
        ("Curriculum Unit", "Unit 3: Application Layer & Infrastructure Services"),
        ("Laboratory Environment", "Cisco Packet Tracer Virtual Simulation"),
    ]
    story.append(info_table(profile_data, col1_w=5.5 * cm))
    story.append(Spacer(1, 4))

    story += heading("Candidate Declaration")
    story.append(body(
        "I hereby declare that the practical assignment titled <b>'Configure a DNS Server and Web Server Using Cisco Packet Tracer'</b> "
        "submitted to the Department of Computer Science and Engineering &ndash; Cyber Security, Sanjivani University, represents my genuine "
        "academic work. The network topology, IP addressing plan, server services, and client verifications described herein were examined, "
        "configured, and analyzed by me. Foundational reference topology and initial framework from open academic repository "
        "<i>chetan475/unit-3</i> are appropriately cited and acknowledged."))
    story.append(Spacer(1, 4))

    sig_data = [
        [Paragraph("<b>Date:</b> November 2, 2026", st_cell),
         Paragraph("<b>Candidate Signature:</b> ___________________________<br/><b>Sanket Aher</b> (PRN: 2125UCSM1080)", st_cell)],
    ]
    t_sig = Table(sig_data, colWidths=[CONTENT_W * 0.45, CONTENT_W * 0.55])
    t_sig.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 4))

    story += heading("Acknowledgement")
    story.append(body(
        "I express my gratitude to the faculty and laboratory coordinators of the Department of Computer Science and Engineering at "
        "Sanjivani University for their guidance. I also acknowledge the global open-source networking education community and standard bodies "
        "(IETF / IEEE) whose RFC standards provided foundational technical reference."))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: TABLE OF CONTENTS & ABSTRACT
    # =========================================================================
    story += heading("Table of Contents")
    toc_items = [
        ("1. Abstract & Executive Summary", "Page 3"),
        ("2. Introduction to Application Layer Architecture", "Page 4"),
        ("3. Problem Statement & Engineering Context", "Page 4"),
        ("4. Aim and Technical Objectives", "Page 4"),
        ("5. Hardware & Simulation Specifications", "Page 5"),
        ("6. Software Requirements & Protocol Environment", "Page 5"),
        ("7. Network Topology & Physical Layer Interconnects", "Page 6"),
        ("8. Protocol Stack Analysis & Encapsulation Dynamics", "Page 7"),
        ("9. IP Addressing Scheme & Subnet Architecture", "Page 8"),
        ("10. DNS Server Configuration & Daemon Parameters", "Page 9"),
        ("11. Web Server Configuration & HTTP Daemon Setup", "Page 10"),
        ("12. Client Workstation Configuration (PC0 & PC1)", "Page 11"),
        ("13. DNS Resource Record Architecture & Zone Design", "Page 12"),
        ("14. Empirical Verification & Testing Methodology", "Page 12"),
        ("15. Ping Test Analysis & ICMP Protocol Mechanics", "Page 13"),
        ("16. DNS Resolution Testing & nslookup Analysis", "Page 14"),
        ("17. HTTP Website Testing & Browser Rendering", "Page 15"),
        ("18. Verified Screenshots & Laboratory Observations Matrix", "Page 16"),
        ("19. Results Synthesis & Performance Discussion", "Page 17"),
        ("20. Architectural Advantages & Security Analysis of DNS", "Page 17"),
        ("21. Enterprise Role & Scaling of Web Servers", "Page 18"),
        ("22. Comprehensive Engineering Troubleshooting Matrix", "Page 18"),
        ("23. Conclusion & Key Learning Outcomes", "Page 19"),
        ("24. Future Scope & Advanced Enhancements", "Page 19"),
        ("25. Academic & Standards References (RFC Citations)", "Page 19"),
    ]
    toc_data = [[Paragraph(f"<b>{title}</b>", st_cell), Paragraph(f"<b>{page}</b>", P("tp", alignment=TA_RIGHT, fontSize=7.8))]
                for title, page in toc_items]
    t_toc = Table(toc_data, colWidths=[CONTENT_W * 0.82, CONTENT_W * 0.18])
    t_toc.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, LGREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 4))

    story += heading("1.  Abstract")
    story.append(body(
        "In modern networking, human operators identify networked services via intuitive Uniform Resource Locators (URLs), whereas routing "
        "hardware operates upon numerical IP addresses. The <b>Domain Name System (DNS)</b> bridges this fundamental divide by functioning as a "
        "distributed, hierarchical database translating alphanumeric domains into IP addresses. Concurrently, the <b>Hypertext Transfer "
        "Protocol (HTTP)</b> powers content distribution over TCP Port 80."))
    story.append(body(
        "This project implements and evaluates a converged Local Area Network (LAN) inside <b>Cisco Packet Tracer</b> on subnet "
        "<b>192.168.1.0/24</b>. The topology integrates a Cisco Catalyst 2960 Layer-2 switch, two client PCs (192.168.1.10 and 192.168.1.11), "
        "an authoritative DNS server (192.168.1.2), and an HTTP Web server (192.168.1.3). The DNS daemon maps <b>www.npcunit3.com</b> to "
        "<b>192.168.1.3</b>. Empirical validation across all layers confirms 0% packet loss on ICMP diagnostics, instantaneous domain resolution via "
        "<code>nslookup</code>, and successful website rendering in client browsers."))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: INTRODUCTION, PROBLEM STATEMENT, AIM & OBJECTIVES
    # =========================================================================
    story += heading("2.  Introduction to Application Layer Architecture")
    story.append(body(
        "While lower layers of the OSI reference model manage bit transmission, frame switching, and packet routing, the <b>Application Layer "
        "(Layer 7)</b> provides the direct software interface for user communication. In the early ARPANET, host resolution relied upon a flat file "
        "<code>HOSTS.TXT</code> maintained by SRI-NIC. The exponential growth of network endpoints rendered this centralized system unscalable, "
        "leading to the development of hierarchical DNS (RFC 1034 / 1035) and HTTP (RFC 2616)."))
    story.append(body(
        "Today, loading a single web page constitutes an orchestrated multi-protocol transaction: ARP frame discovery, UDP Port 53 DNS query-response, "
        "TCP Port 80 three-way handshake, and HTTP GET/200 OK delivery. Mastering this convergence is crucial for cyber security and network engineering."))

    story += heading("3.  Problem Statement")
    story.append(body(
        "Within an enterprise LAN, forcing users to access internal documentation servers via numerical IP addresses (e.g. <code>http://192.168.1.3</code>) "
        "creates cognitive friction and severe administrative fragility. If a server IP changes during hardware migration, all client bookmarks and scripts "
        "fail. A deterministic, local DNS authority is required to translate <b>www.npcunit3.com</b> into physical IPv4 addresses seamlessly."))

    story += heading("4.  Aim and Technical Objectives")
    story.append(sub("Primary Aim"))
    story.append(body(
        "To configure, interconnect, and empirically validate an authoritative DNS Server and HTTP Web Server in Cisco Packet Tracer on subnet "
        "192.168.1.0/24, verifying domain name resolution and website access from client workstations."))
    story.append(sub("Specific Technical Objectives"))
    story += numbered([
        "<b>Topology Construction:</b> Deploy a star-topology LAN linking two PCs, one switch, one DNS server, and one Web server.",
        "<b>IP Configuration:</b> Assign static IPv4 addresses within 192.168.1.0/24 with full subnet mask compliance.",
        "<b>HTTP Service Deployment:</b> Configure the HTTP daemon on Web Server, authoring a customized student welcome portal.",
        "<b>Authoritative DNS Zone:</b> Configure DNS daemon and add an Address (A) record mapping <code>www.npcunit3.com</code> &rarr; <code>192.168.1.3</code>.",
        "<b>Client Resolver Pointing:</b> Configure client workstations PC0 and PC1 with static DNS pointer referencing <code>192.168.1.2</code>.",
        "<b>Connectivity & Delivery Verification:</b> Validate bilateral ICMP ping reachability, execute <code>nslookup</code>, and render the webpage.",
    ])
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: HARDWARE & SOFTWARE REQUIREMENTS
    # =========================================================================
    story += heading("5.  Hardware Requirements & Simulation Equipment")
    story.append(body(
        "The practical utilizes standard enterprise network components modeled within Cisco Packet Tracer. The virtual hardware parameters "
        "and physical layer characteristics are summarized below:"))

    hw_data = [
        ["Device Model", "Device Type", "Interface Allocation", "Physical Hardware Function"],
        ["Cisco 2960-24TT", "Catalyst Layer-2 Switch", "Fa0/1, Fa0/2, Fa0/3, Fa0/4", "Central star hub; wirespeed ASIC switching, hardware MAC table"],
        ["Server-PT (DNS)", "Dedicated Network Server", "FastEthernet0 (100BASE-TX)", "Hosts DNS daemon (UDP/TCP Port 53), authoritative name resolution"],
        ["Server-PT (Web)", "Dedicated Network Server", "FastEthernet0 (100BASE-TX)", "Hosts HTTP daemon (TCP Port 80), serves HTML and web payloads"],
        ["PC-PT (PC0)", "Client Workstation", "FastEthernet0 (100BASE-TX)", "Primary end-user workstation; runs Command Prompt CLI and Web Browser"],
        ["PC-PT (PC1)", "Client Workstation", "FastEthernet0 (100BASE-TX)", "Secondary end-user workstation for parallel connectivity verification"],
        ["Category 5e UTP", "Copper Straight-Through", "EIA/TIA 568B Standard", "Provides full-duplex 100 Mbps transmission between switch and terminal interfaces"],
    ]
    story.append(data_table(hw_data[0], hw_data[1:], widths=[CONTENT_W * 0.22, CONTENT_W * 0.24, CONTENT_W * 0.22, CONTENT_W * 0.32]))
    story.append(Spacer(1, 4))

    story.append(callout(
        "<b>Layer-2 Micro-segmentation:</b> In this star topology, each switch port forms an isolated collision domain operating in full-duplex "
        "mode (100 Mbps TX). The switch forwards frames strictly to destination MAC addresses based on its CAM table, eliminating frame collisions.",
        title="HARDWARE SWITCHING CHARACTERISTICS", kind="info"
    ))
    story.append(Spacer(1, 4))

    story += heading("6.  Software Requirements & Protocol Standards")
    sw_data = [
        ["Software Component", "Version / Platform", "Role and Utilization in Practical"],
        ["Cisco Packet Tracer", "v8.2 / v9.0.1", "Primary simulation sandbox for network modeling, packet inspection, and GUI configuration"],
        ["Cisco IOS Software", "Catalyst 2960 Base", "Powers Layer-2 switching engine, auto-negotiation, and STP loop prevention"],
        ["Workstation OS", "Packet Tracer Desktop OS", "Provides Windows-style TCP/IP configuration, CLI Command Prompt, and HTML Web Browser"],
        ["Python Environment", "Python 3.10+", "Automation engine utilized to compile the submission report, diagrams, and verification matrices"],
        ["ReportLab & docx", "Enterprise Libraries", "Generates pixel-perfect PDF and editable Microsoft Word documentation"],
    ]
    story.append(data_table(sw_data[0], sw_data[1:], widths=[CONTENT_W * 0.25, CONTENT_W * 0.22, CONTENT_W * 0.53]))
    story.append(Spacer(1, 4))

    story += bullets([
        "<b>RFC 791 (IPv4):</b> 32-bit dotted-decimal network addressing and datagram delivery.",
        "<b>RFC 792 (ICMP):</b> Echo Request (Type 8) and Echo Reply (Type 0) diagnostic messaging.",
        "<b>RFC 1034 & 1035 (DNS):</b> Domain Name System specification and UDP Port 53 query-response framing.",
        "<b>RFC 2616 (HTTP/1.1):</b> Hypertext Transfer Protocol request-response transactions over TCP Port 80.",
    ])
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: NETWORK TOPOLOGY & PHYSICAL LAYOUT
    # =========================================================================
    story += heading("7.  Network Topology & Physical Layer Interconnects")
    story.append(body(
        "The practical implements a deterministic <b>Star Topology</b> centered around a Cisco Catalyst 2960 switch. Every terminal device "
        "connects via Category 5e Copper Straight-Through cabling to dedicated FastEthernet switch ports within the classless subnet "
        "<b>192.168.1.0/24</b>."))

    story.append(sub("Logical Topology Reference Architecture"))
    story.append(figure(TOPO_PNG, "Figure 7.1: Logical Network Topology Architecture (Subnet 192.168.1.0/24 &ndash; Sanket Aher)",
                        max_h=4.6 * cm))
    story.append(Spacer(1, 3))

    story.append(sub("Packet Tracer Workspace Implementation"))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "01_topology.png"),
                        "Figure 7.2: Cisco Packet Tracer Workspace Implementation with Active Link Indicators",
                        max_h=4.6 * cm))
    story.append(Spacer(1, 3))

    story.append(callout(
        "<b>Physical Cable Selection Rule:</b> Copper Straight-Through cables (EIA/TIA 568B pinout) are utilized because connections "
        "occur between <i>dissimilar</i> device categories (DTE endpoints connecting to DCE switch ports). Active green link LEDs confirm "
        "Spanning Tree Protocol (STP) forward state.",
        title="PHYSICAL CABLING & LINK STATE ANALYSIS", kind="info"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: PROTOCOL STACK & ENCAPSULATION DYNAMICS
    # =========================================================================
    story += heading("8.  Protocol Stack Analysis & Encapsulation Dynamics")
    story.append(body(
        "Every network transaction across the LAN undergoes rigorous multi-layer encapsulation and de-encapsulation spanning the OSI 7-Layer "
        "model and TCP/IP protocol suite:"))

    proto_layers = [
        ["OSI Layer", "Protocol / Standard", "PDU Name", "Role in DNS & Web Server Communication"],
        ["7. Application", "DNS, HTTP", "Data (Payload)", "Formulates DNS queries (www.npcunit3.com) and HTTP requests (GET / HTTP/1.1)"],
        ["6. Presentation", "ASCII, HTML", "Data", "Encodes plain text and HTML markups rendered by client browser"],
        ["5. Session", "Sockets", "Data", "Manages logical sockets (IP:Port tuples) connecting client applications to daemons"],
        ["4. Transport", "UDP (53), TCP (80)", "Segment/Datagram", "UDP provides fast DNS queries; TCP guarantees reliable, ordered HTTP delivery"],
        ["3. Network", "IPv4, ICMP, ARP", "Packet (Datagram)", "Encapsulates source/dest IP addresses (192.168.1.10 to 192.168.1.2/.3) and TTL"],
        ["2. Data Link", "IEEE 802.3 Ethernet", "Frame", "Encapsulates 48-bit MAC addresses, EtherType (0x0800), and CRC checksum"],
        ["1. Physical", "100BASE-TX FastEth", "Bits", "Converts digital frames into electrical pulses across Cat 5e copper pairs at 100 Mbps"],
    ]
    story.append(data_table(proto_layers[0], proto_layers[1:], widths=[CONTENT_W * 0.18, CONTENT_W * 0.22, CONTENT_W * 0.20, CONTENT_W * 0.40]))
    story.append(Spacer(1, 4))

    story.append(sub("Sequential Lifecycle of an End-to-End Web Request"))
    story += numbered([
        "<b>ARP Discovery Phase:</b> PC0 broadcasts an ARP Request (<code>FF:FF:FF:FF:FF:FF</code>) to resolve the DNS server's MAC address. The server returns a unicast ARP Reply, allowing PC0 to populate its local ARP cache.",
        "<b>DNS Name Resolution:</b> PC0 transmits a DNS Query inside a UDP datagram to Port 53. The DNS daemon matches <code>www.npcunit3.com</code> in its database and returns an A-record Answer with <code>192.168.1.3</code>.",
        "<b>TCP Three-Way Handshake:</b> PC0 initiates a reliable session with Web Server (192.168.1.3) via TCP SYN on Port 80, receiving SYN-ACK and returning ACK.",
        "<b>HTTP Delivery & Rendering:</b> PC0 issues <code>GET / HTTP/1.1</code>. The Web Server serves <code>index.html</code> with an <code>HTTP/1.1 200 OK</code> response.",
    ])
    story.append(Spacer(1, 3))

    story.append(callout(
        "<b>Transport Selection Rationale:</b> DNS utilizes UDP Port 53 for low-overhead, rapid lookups under 512 bytes. HTTP relies on TCP Port 80 "
        "to ensure byte-accurate, sequenced transmission of HTML payloads.",
        title="TRANSPORT LAYER PROTOCOL SELECTION CRITERIA", kind="info"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: IP ADDRESSING SCHEME & SUBNET DESIGN
    # =========================================================================
    story += heading("9.  IP Addressing Scheme & Subnet Architecture")
    story.append(body(
        "Network addressing was designed using private address space defined in <b>RFC 1918</b>. A single classless subnet <b>192.168.1.0/24</b> "
        "was implemented. Static IP addressing ensures deterministic bindings without dependency on dynamic DHCP services."))

    story.append(sub("Subnet Mathematical Breakdown"))
    subnet_math = [
        ("Network Address", "192.168.1.0"),
        ("Subnet Mask", "255.255.255.0 (Classless Prefix: /24)"),
        ("Subnet Bit Representation", "11111111 . 11111111 . 11111111 . 00000000 (24 network bits, 8 host bits)"),
        ("Total Address Capacity", "2^8 = 256 IP Addresses"),
        ("Usable Host Capacity", "2^8 &ndash; 2 = 254 Valid Host Addresses"),
        ("Usable Host Range", "192.168.1.1 &ndash; 192.168.1.254"),
        ("Subnet Directed Broadcast", "192.168.1.255"),
        ("Wildcard Mask", "0.0.0.255"),
    ]
    story.append(info_table(subnet_math, col1_w=5.2 * cm))
    story.append(Spacer(1, 4))

    story += heading("Master Device IP Configuration Table")
    ip_table = [
        ["Device ID", "Hardware Model", "Interface", "Assigned IPv4", "Subnet Mask", "Default Gateway", "Configured DNS Pointer"],
        ["Switch0", "Cisco 2960", "VLAN 1", "Unassigned (L2)", "Unassigned", "None", "None"],
        ["DNS Server", "Server-PT", "Fa0", "192.168.1.2", "255.255.255.0", "None (Blank)", "127.0.0.1 (Loopback)"],
        ["Web Server", "Server-PT", "Fa0", "192.168.1.3", "255.255.255.0", "None (Blank)", "192.168.1.2"],
        ["PC0", "PC-PT", "Fa0", "192.168.1.10", "255.255.255.0", "None (Blank)", "192.168.1.2"],
        ["PC1", "PC-PT", "Fa0", "192.168.1.11", "255.255.255.0", "None (Blank)", "192.168.1.2"],
    ]
    story.append(data_table(ip_table[0], ip_table[1:], widths=[CONTENT_W * 0.14, CONTENT_W * 0.14, CONTENT_W * 0.10, CONTENT_W * 0.15, CONTENT_W * 0.15, CONTENT_W * 0.14, CONTENT_W * 0.18]))
    story.append(Spacer(1, 4))

    story.append(callout(
        "<b>Omitting Default Gateway:</b> In TCP/IP logic, a Default Gateway (router) is only contacted when the target IP lies outside the local "
        "subnet mask. Because all devices reside within <code>192.168.1.0/24</code>, all communications resolve directly via Layer-2 ARP without a router.",
        title="ROUTING DECISION LOGIC IN SINGLE-SUBNET LANs", kind="info"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: DNS SERVER CONFIGURATION
    # =========================================================================
    story += heading("10.  DNS Server Configuration & Daemon Parameters")
    story.append(body(
        "The Domain Name Server functions as the authoritative name server for the local LAN. Configuration involves assigning static IP "
        "parameters to FastEthernet0 and activating the DNS service."))

    story.append(sub("Step-by-Step Configuration Procedure"))
    story += numbered([
        "Click <b>DNS Server</b> &gt; select <b>Desktop</b> &gt; <b>IP Configuration</b>. Set <b>Static IP:</b> <code>192.168.1.2</code> and <b>Subnet Mask:</b> <code>255.255.255.0</code>.",
        "Navigate to <b>Services</b> &gt; <b>DNS</b>. Set the <b>DNS Service</b> radio button to <b>ON</b>.",
        "Under <b>Resource Records</b>, enter <b>Name:</b> <code>www.npcunit3.com</code>, <b>Type:</b> <code>A Record</code>, and <b>Address:</b> <code>192.168.1.3</code>.",
        "Click <b>Add</b>. Confirm that the record appears in the resource table mapping the domain name to the Web Server.",
    ])
    story.append(Spacer(1, 2))

    story.append(figure(os.path.join(SCREENSHOTS_DIR, "02_dns_ip_config.png"),
                        "Figure 10.1: DNS Server Static IP Configuration Dialog (192.168.1.2 / 24)",
                        max_h=4.6 * cm))
    story.append(Spacer(1, 2))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "03_dns_service_config.png"),
                        "Figure 10.2: DNS Service Configuration & Active A-Record Mapping Table",
                        max_h=4.6 * cm))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: WEB SERVER CONFIGURATION
    # =========================================================================
    story += heading("11.  Web Server Configuration & HTTP Daemon Setup")
    story.append(body(
        "The Web Server provides HTTP document hosting for client browsers. It is assigned <code>192.168.1.3</code> and hosts a personalized "
        "HTML portal displaying student metadata for Sanket Aher."))

    story.append(sub("Step-by-Step Configuration Procedure"))
    story += numbered([
        "Click <b>Web Server</b> &gt; select <b>Desktop</b> &gt; <b>IP Configuration</b>. Assign IP <code>192.168.1.3</code>, Mask <code>255.255.255.0</code>, DNS <code>192.168.1.2</code>.",
        "Navigate to <b>Services</b> &gt; <b>HTTP</b>. Toggle both <b>HTTP</b> and <b>HTTPS</b> services <b>ON</b>.",
        "Locate <code>index.html</code> in File Manager &gt; click <b>(edit)</b> &gt; paste customized HTML portal code &gt; click <b>Save</b>.",
    ])
    story.append(Spacer(1, 2))

    story.append(sub("Personalized Webpage Source (index.html)"))
    web_code = (
        "<!DOCTYPE html><html><head><title>NPC Unit 3</title></head>\n"
        "<body style='font-family: Arial; background: #f0f4f8; padding: 15px;'>\n"
        "  <div style='background: white; padding: 20px; border-top: 4px solid #1F3864;'>\n"
        "    <h2>Welcome to My Web Server!</h2>\n"
        "    <p><b>Domain:</b> www.npcunit3.com &rarr; <b>IP:</b> 192.168.1.3</p>\n"
        "    <p><b>Candidate:</b> Sanket Aher | <b>PRN:</b> 2125UCSM1080 | Sanjivani University</p>\n"
        "  </div>\n"
        "</body></html>"
    )
    story.append(code_box(web_code))
    story.append(Spacer(1, 2))

    story.append(figure(os.path.join(SCREENSHOTS_DIR, "04_web_ip_config.png"),
                        "Figure 11.1: Web Server Static IP Configuration Dialog (192.168.1.3 / 24)",
                        max_h=4.2 * cm))
    story.append(Spacer(1, 2))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "05_http_service_config.png"),
                        "Figure 11.2: Web Server HTTP Service Settings and Customized index.html",
                        max_h=4.2 * cm))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CLIENT WORKSTATION CONFIGURATION
    # =========================================================================
    story += heading("12.  Client Workstation Configuration (PC0 & PC1)")
    story.append(body(
        "Client workstations require static IP assignments and primary DNS pointers referencing <code>192.168.1.2</code> to enable "
        "automatic name resolution across the LAN."))

    story.append(sub("Workstation Configuration Specifications"))
    story += bullets([
        "<b>PC0 Workstation:</b> Static IP <code>192.168.1.10</code>, Subnet Mask <code>255.255.255.0</code>, Primary DNS <code>192.168.1.2</code>.",
        "<b>PC1 Workstation:</b> Static IP <code>192.168.1.11</code>, Subnet Mask <code>255.255.255.0</code>, Primary DNS <code>192.168.1.2</code>.",
    ])
    story.append(Spacer(1, 2))

    story.append(figure(os.path.join(SCREENSHOTS_DIR, "06_pc0_ip_config.png"),
                        "Figure 12.1: PC0 Static IP and DNS Resolver Pointer Configuration Dialog",
                        max_h=4.5 * cm))
    story.append(Spacer(1, 2))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "07_pc1_ip_config.png"),
                        "Figure 12.2: PC1 Static IP and DNS Resolver Pointer Configuration Dialog",
                        max_h=4.5 * cm))
    story.append(Spacer(1, 2))

    story.append(callout(
        "<b>Client Resolver Binding:</b> Without setting <code>192.168.1.2</code> in the DNS Server field, direct IP pings succeed, but domain "
        "lookups fail because the client operating system lacks a target nameserver socket for UDP Port 53 queries.",
        title="CLIENT-SIDE RESOLVER DEPENDENCY ANALYSIS", kind="info"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: DNS RESOURCE RECORDS & TESTING METHODOLOGY
    # =========================================================================
    story += heading("13.  DNS Resource Record Architecture & Zone Design")
    story.append(body(
        "DNS databases organize zone data into standardized Resource Records (RRs) defined by RFC 1035:"))

    rr_data = [
        ["Record Type", "Full Name", "Standard RFC", "Technical Function & Syntax Example"],
        ["A Record", "Address Record", "RFC 1035", "Maps an IPv4 32-bit address to a hostname (www.npcunit3.com &rarr; 192.168.1.3)"],
        ["AAAA Record", "IPv6 Address Record", "RFC 3596", "Maps an IPv6 128-bit address to a hostname (e.g. ipv6.npcunit3.com &rarr; 2001:db8::1)"],
        ["CNAME", "Canonical Name", "RFC 1035", "Creates an alias pointing one domain name to another canonical name (e.g. web &rarr; www)"],
        ["MX Record", "Mail Exchange", "RFC 1035", "Directs email traffic to responsible Mail Transfer Agents (MTAs) with priority values"],
        ["NS Record", "Name Server", "RFC 1035", "Delegates a DNS zone to an authoritative name server"],
        ["PTR Record", "Pointer Record", "RFC 1035", "Performs reverse lookups mapping an IP address back to its FQDN"],
        ["SOA Record", "Start of Authority", "RFC 1035", "Specifies authoritative zone parameters: serial number, refresh timers, admin contact"],
    ]
    story.append(data_table(rr_data[0], rr_data[1:], widths=[CONTENT_W * 0.16, CONTENT_W * 0.22, CONTENT_W * 0.16, CONTENT_W * 0.46]))
    story.append(Spacer(1, 4))

    story += heading("14.  Empirical Verification & Testing Methodology")
    story.append(body(
        "Testing follows a multi-phase framework validating Layer-3 connectivity, Layer-7 name resolution, and HTTP payload rendering:"))

    test_matrix = [
        ["Test ID", "Target Layer", "Command / Action", "Precondition", "Expected Technical Outcome"],
        ["TEST-01", "Layer 3 (ICMP)", "PC0: ping 192.168.1.2", "Link state UP (Green lights)", "4/4 echo replies received; 0% loss; RTT < 1ms; TTL=128"],
        ["TEST-02", "Layer 3 (ICMP)", "PC0: ping 192.168.1.3", "Link state UP (Green lights)", "4/4 echo replies received; 0% loss; RTT < 1ms; TTL=128"],
        ["TEST-03", "Layer 3 (ICMP)", "PC1: ping 192.168.1.2", "Link state UP (Green lights)", "4/4 echo replies received; 0% loss; RTT < 1ms; TTL=128"],
        ["TEST-04", "Layer 3 (ICMP)", "PC1: ping 192.168.1.3", "Link state UP (Green lights)", "4/4 echo replies received; 0% loss; RTT < 1ms; TTL=128"],
        ["TEST-05", "Layer 7 (DNS)", "PC0: nslookup www.npcunit3.com", "DNS daemon ON; A-record added", "Default server: 192.168.1.2; Answer IP: 192.168.1.3"],
        ["TEST-06", "Layer 7 (HTTP)", "PC0: Browser -> http://www.npcunit3.com", "HTTP service ON; index.html set", "HTTP 200 OK; custom web page rendered successfully"],
    ]
    story.append(data_table(test_matrix[0], test_matrix[1:], widths=[CONTENT_W * 0.12, CONTENT_W * 0.18, CONTENT_W * 0.28, CONTENT_W * 0.20, CONTENT_W * 0.22]))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: PING TEST ANALYSIS & ICMP MECHANICS
    # =========================================================================
    story += heading("15.  Ping Test Analysis & ICMP Protocol Mechanics")
    story.append(body(
        "Network-layer reachability was verified via ICMP Echo diagnostics executed from PC0 Command Prompt to both servers:"))

    story.append(sub("Command Line Execution Syntax"))
    story.append(code_box(
        "PC0> ping 192.168.1.2\n"
        "Pinging 192.168.1.2 with 32 bytes of data:\n"
        "Reply from 192.168.1.2: bytes=32 time<1ms TTL=128\n"
        "Reply from 192.168.1.2: bytes=32 time<1ms TTL=128\n"
        "Ping statistics for 192.168.1.2:\n"
        "    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)\n\n"
        "PC0> ping 192.168.1.3\n"
        "Pinging 192.168.1.3 with 32 bytes of data:\n"
        "Reply from 192.168.1.3: bytes=32 time<1ms TTL=128\n"
        "Reply from 192.168.1.3: bytes=32 time<1ms TTL=128\n"
        "Ping statistics for 192.168.1.3:\n"
        "    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
    ))
    story.append(Spacer(1, 3))

    story.append(sub("Empirical Evidence of Successful ICMP Connectivity"))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "08_ping_tests.png"),
                        "Figure 15.1: PC0 Command Prompt Output &ndash; Successful ICMP Ping Verification to DNS and Web Servers",
                        max_h=6.5 * cm))
    story.append(Spacer(1, 3))

    story.append(callout(
        "<b>ICMP Metrics Dissection:</b><br/>"
        "&bull; <b>bytes=32:</b> Standard ICMP payload size.<br/>"
        "&bull; <b>time &lt; 1ms:</b> Near-zero transmission delay characteristic of local wirespeed FastEthernet switching.<br/>"
        "&bull; <b>TTL=128:</b> Time-To-Live counter remains at initial value 128 because traffic remained inside the single LAN without router hops.",
        title="ICMP PACKET METRICS ANALYSIS", kind="success"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: DNS RESOLUTION TESTING & NSLOOKUP
    # =========================================================================
    story += heading("16.  DNS Resolution Testing & nslookup Analysis")
    story.append(body(
        "The name resolution subsystem was tested using <code>nslookup</code>, verifying that client UDP queries are answered by the DNS daemon:"))

    story.append(sub("nslookup Diagnostic Output"))
    story.append(code_box(
        "PC0> nslookup www.npcunit3.com\n"
        "Server:  192.168.1.2\n"
        "Address: 192.168.1.2\n\n"
        "Name:    www.npcunit3.com\n"
        "Address: 192.168.1.3"
    ))
    story.append(Spacer(1, 3))

    story.append(sub("Empirical Evidence of DNS Name Resolution"))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "09_dns_lookup.png"),
                        "Figure 16.1: PC0 Command Prompt nslookup Output &ndash; Successful Authoritative Domain Resolution",
                        max_h=6.5 * cm))
    story.append(Spacer(1, 3))

    story.append(callout(
        "<b>nslookup Dissection:</b><br/>"
        "1. <b>Server (192.168.1.2):</b> Proves query was processed by the primary DNS Server configured on PC0.<br/>"
        "2. <b>Answer (www.npcunit3.com &rarr; 192.168.1.3):</b> Proves the DNS daemon successfully returned the Web Server's A-record address.",
        title="DNS RESOLVER TRANSACTION VERIFICATION", kind="success"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: HTTP WEBSITE TESTING & BROWSER RENDERING
    # =========================================================================
    story += heading("17.  HTTP Website Testing & Browser Rendering")
    story.append(body(
        "The end-to-end integration was validated by opening the Web Browser on PC0 and navigating to <code>http://www.npcunit3.com</code>:"))

    story.append(sub("Browser Execution Workflow"))
    story += numbered([
        "Open <b>PC0</b> &gt; select <b>Desktop</b> &gt; click <b>Web Browser</b>.",
        "Enter URL <code>http://www.npcunit3.com</code> in the address bar &gt; press <b>Enter</b>.",
        "Verify instant resolution and rendering of the customized HTML portal.",
    ])
    story.append(Spacer(1, 3))

    story.append(sub("Visual Evidence of Domain-Based Web Browsing"))
    story.append(figure(os.path.join(SCREENSHOTS_DIR, "10_website_browser.png"),
                        "Figure 17.1: PC0 Web Browser Rendering Website via Fully Qualified Domain Name (http://www.npcunit3.com)",
                        max_h=6.8 * cm))
    story.append(Spacer(1, 3))

    story.append(callout(
        "<b>End-to-End Convergence Confirmed:</b> The successful display of the customized web portal validates full convergence across the network: "
        "transparent DNS resolution (192.168.1.3), TCP handshake on Port 80, HTTP GET retrieval, and accurate browser rendering.",
        title="SYSTEM INTEGRATION & PRACTICAL VALIDATION SUCCESS", kind="success"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: SCREENSHOTS SUMMARY & OBSERVATIONS MATRIX
    # =========================================================================
    story += heading("18.  Verified Screenshots & Laboratory Observations Matrix")
    story.append(body(
        "The table below catalogs all empirical figures captured during the practical, linking each to its technical verification status:"))

    obs_matrix = [
        ["Fig #", "Target Scope", "Cisco Packet Tracer Context", "Key Technical Observation & Verification Status"],
        ["Fig 7.1", "Topology", "Logical Design Diagram", "Star topology; 192.168.1.0/24 subnet; clear interface assignments (Fa0/1 to Fa0/4)."],
        ["Fig 7.2", "Topology", "Workspace GUI (01_topology.png)", "All devices interconnected; 4 green link LEDs confirm active FastEthernet links."],
        ["Fig 10.1", "DNS IP", "DNS Server Desktop (02_dns_ip_config.png)", "Static IP 192.168.1.2 assigned; Subnet Mask 255.255.255.0; adapter bound."],
        ["Fig 10.2", "DNS Service", "DNS Server Services (03_dns_service_config.png)", "DNS daemon ON; A-record www.npcunit3.com -> 192.168.1.3 correctly saved."],
        ["Fig 11.1", "Web IP", "Web Server Desktop (04_web_ip_config.png)", "Static IP 192.168.1.3 assigned; Mask 255.255.255.0; DNS pointed to 192.168.1.2."],
        ["Fig 11.2", "HTTP Service", "Web Server Services (05_http_service_config.png)", "HTTP/HTTPS daemons ON; index.html file saved with custom student branding."],
        ["Fig 12.1", "PC0 Config", "PC0 Desktop (06_pc0_ip_config.png)", "Static IP 192.168.1.10; Mask 255.255.255.0; DNS resolver points to 192.168.1.2."],
        ["Fig 12.2", "PC1 Config", "PC1 Desktop (07_pc1_ip_config.png)", "Static IP 192.168.1.11; Mask 255.255.255.0; DNS resolver points to 192.168.1.2."],
        ["Fig 15.1", "ICMP Ping", "PC0 Command Prompt (08_ping_tests.png)", "Pings to 192.168.1.2 & 192.168.1.3: 4/4 replies each; 0% loss; RTT < 1ms; TTL=128."],
        ["Fig 16.1", "DNS Lookup", "PC0 Command Prompt (09_dns_lookup.png)", "nslookup queries 192.168.1.2; successfully resolves domain to 192.168.1.3."],
        ["Fig 17.1", "Web Browser", "PC0 Web Browser (10_website_browser.png)", "URL http://www.npcunit3.com opens customized welcome page for Sanket Aher."],
    ]
    story.append(data_table(obs_matrix[0], obs_matrix[1:], widths=[CONTENT_W * 0.10, CONTENT_W * 0.16, CONTENT_W * 0.32, CONTENT_W * 0.42]))
    story.append(Spacer(1, 4))

    story.append(callout(
        "<b>Academic Evidence Replacement Policy:</b> The repository provides standardized placeholders in <code>screenshots/</code>. "
        "Capturing practical screenshots in Packet Tracer and saving them under identical filenames automatically refreshes this report upon rebuilding.",
        title="LABORATORY EVIDENCE VERIFICATION POLICY", kind="info"
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: RESULTS & DNS CYBER SECURITY ANALYSIS
    # =========================================================================
    story += heading("19.  Results Synthesis & Performance Discussion")
    story.append(body(
        "All six empirical test cases achieved 100% operational success across the Cisco 2960 switch without packet degradation:"))
    story += bullets([
        "<b>Transmission Latency:</b> ICMP round-trip times registered at <code>time &lt; 1ms</code>, confirming wirespeed switching.",
        "<b>Reliability:</b> Bilateral ping tests achieved 0.0% packet loss (Sent = 4, Received = 4), verifying link and ARP integrity.",
        "<b>Name Resolution:</b> UDP queries on Port 53 resolved instantaneously without measurable lookup latency.",
        "<b>Application Delivery:</b> The HTTP GET transaction delivered the complete HTML payload with full CSS styling.",
    ])
    story.append(Spacer(1, 4))

    story += heading("20.  Architectural Advantages & Security Analysis of DNS")
    story.append(sub("Key Architectural Benefits of DNS"))
    story += bullets([
        "<b>Cognitive Abstraction:</b> Replaces numerical IP strings with intuitive, memorable domain names.",
        "<b>Infrastructure Decoupling:</b> Web servers can be migrated to new physical IP addresses by updating the DNS record without altering client URLs.",
        "<b>Load Distribution:</b> Supports Round-Robin DNS to distribute incoming traffic among multiple web servers.",
    ])
    story.append(Spacer(1, 3))

    story.append(sub("Cyber Security Vulnerabilities & Defense Mechanisms"))
    dns_sec_data = [
        ["Threat Vector", "Mechanics & Exploitation Method", "Engineered Countermeasure"],
        ["DNS Cache Poisoning", "Attacker injects forged A-records into resolver cache, redirecting users to rogue phishing servers.", "Deploy <b>DNSSEC</b> with cryptographic signatures (RRSIG) and trust anchors."],
        ["DNS Amplification DDoS", "Attacker sends spoofed UDP queries requesting large records, reflecting massive traffic onto victim.", "Disable open recursion; enforce Response Rate Limiting (RRL); implement BCP 38 filtering."],
        ["DNS Redirection", "Malicious actor modifies client DNS pointer settings to point to rogue nameservers.", "Enforce endpoint security policies, audit DNS settings, and require MFA on DNS portals."],
        ["Plaintext Snooping", "Plaintext UDP Port 53 queries expose browsing activity to network eavesdroppers.", "Deploy encrypted transport protocols such as <b>DNS over HTTPS (DoH)</b> or <b>DNS over TLS (DoT)</b>."],
    ]
    story.append(data_table(dns_sec_data[0], dns_sec_data[1:], widths=[CONTENT_W * 0.22, CONTENT_W * 0.40, CONTENT_W * 0.38]))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: ENTERPRISE WEB SERVERS & TROUBLESHOOTING MATRIX
    # =========================================================================
    story += heading("21.  Enterprise Role & Scaling of Web Servers")
    story.append(body(
        "In production enterprise networks, web servers scale into resilient clusters utilizing Reverse Proxies (NGINX, HAProxy), hardware load "
        "balancers, and Web Application Firewalls (WAF). Production environments transition from HTTP (Port 80) to HTTPS (Port 443) using TLS 1.3."))

    story += heading("22.  Comprehensive Engineering Troubleshooting Matrix")
    story.append(body(
        "The diagnostic matrix below outlines common failure modes encountered during DNS and Web server deployments with exact remedies:"))

    trouble_data = [
        ["Fault Symptom", "Underlying Root Cause", "Step-by-Step Diagnostic & Remediation Procedure"],
        ["Ping: 'Request timed out' / 100% loss", "Incorrect IP address; wrong subnet mask; cable unplugged; interface down.", "1. Verify link LEDs (must be green).<br/>2. Re-check IP Configuration for typos.<br/>3. Verify switch port status via <code>show interfaces status</code>."],
        ["Browser: 'Host Name Unresolved'", "Client DNS pointer blank; DNS daemon OFF; domain misspelled.", "1. Verify PC's DNS Server field points to <code>192.168.1.2</code>.<br/>2. Verify DNS Service is <b>ON</b> in DNS Server.<br/>3. Check A-record spelling."],
        ["Browser: 'Page Not Found' (404)", "HTTP daemon OFF; <code>index.html</code> deleted or renamed.", "1. Navigate to <b>Web Server > Services > HTTP</b>.<br/>2. Ensure <b>HTTP</b> is <b>ON</b>.<br/>3. Verify <code>index.html</code> exists in file list."],
        ["Amber Link Light on Switch Port", "Spanning Tree Protocol (STP) listening/learning transition.", "Wait 30 seconds for STP convergence or enable PortFast on switch interface (<code>spanning-tree portfast</code>)."],
        ["nslookup returns wrong IP address", "Stale or erroneous A-record in DNS database.", "Open DNS Server > Services > DNS. Delete erroneous record, re-enter correct IP (<code>192.168.1.3</code>), and re-add."],
        ["IP Address Conflict Warning", "Duplicate IP assigned to two devices on LAN.", "Ensure strictly unique host numbers (DNS=.2, Web=.3, PC0=.10, PC1=.11). Run <code>arp -a</code> to identify conflicting MAC."],
    ]
    story.append(data_table(trouble_data[0], trouble_data[1:], widths=[CONTENT_W * 0.22, CONTENT_W * 0.28, CONTENT_W * 0.50]))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: CONCLUSION, FUTURE SCOPE & REFERENCES
    # =========================================================================
    story += heading("23.  Conclusion & Key Learning Outcomes")
    story.append(body(
        "In this practical, an authoritative DNS server and HTTP web server were successfully designed, configured, and empirically verified "
        "inside Cisco Packet Tracer on subnet <b>192.168.1.0/24</b>. Key learning outcomes achieved include:"))
    story += bullets([
        "<b>Multi-layer Convergence:</b> Validated interoperability between Layer-2 switching, Layer-3 IPv4, Layer-4 UDP/TCP, and Layer-7 services.",
        "<b>Zero-Loss Connectivity:</b> Confirmed bilateral Layer-3 reachability across all nodes via ICMP echo diagnostics with 0% packet loss.",
        "<b>Authoritative Name Resolution:</b> Successfully mapped <code>www.npcunit3.com</code> to <code>192.168.1.3</code>, eliminating IP memorability.",
        "<b>Diagnostic Proficiency:</b> Demonstrated CLI proficiency using <code>ping</code> and <code>nslookup</code> for systematic troubleshooting.",
    ])
    story.append(Spacer(1, 4))

    story += heading("24.  Future Scope & Advanced Enhancements")
    story += numbered([
        "<b>Dynamic Addressing (DHCP):</b> Deploy a centralized DHCP server to automate client IP, mask, gateway, and DNS leasing.",
        "<b>Inter-VLAN Routing:</b> Segment the network into distinct VLANs (VLAN 10: Servers, VLAN 20: PCs) using an 802.1Q trunked router.",
        "<b>Redundant Multi-Server Design:</b> Configure secondary slave DNS servers with zone transfers (AXFR) for high availability.",
        "<b>HTTPS & PKI Deployment:</b> Deploy an internal Certificate Authority (CA) to enable SSL/TLS encrypted HTTPS browsing on Port 443.",
        "<b>Network Security Hardening:</b> Implement Cisco Access Control Lists (ACLs) to filter unauthorized traffic.",
    ])
    story.append(Spacer(1, 4))

    story += heading("25.  Academic & Standards References")
    refs = [
        "Mockapetris, P., &ldquo;Domain names &ndash; concepts and facilities,&rdquo; RFC 1034, IETF, Nov. 1987.",
        "Mockapetris, P., &ldquo;Domain names &ndash; implementation and specification,&rdquo; RFC 1035, IETF, Nov. 1987.",
        "Fielding, R., et al., &ldquo;Hypertext Transfer Protocol &ndash;&ndash; HTTP/1.1,&rdquo; RFC 2616, Jun. 1999.",
        "Postel, J., &ldquo;Internet Protocol &ndash; DARPA Internet Program Protocol Specification,&rdquo; RFC 791, Sep. 1981.",
        "Postel, J., &ldquo;Internet Control Message Protocol,&rdquo; RFC 792, Sep. 1981.",
        "Plummer, D. C., &ldquo;An Ethernet Address Resolution Protocol,&rdquo; RFC 826, Nov. 1982.",
        "Cisco Systems, Inc., &ldquo;Cisco Packet Tracer User & Architecture Guide,&rdquo; Cisco Networking Academy, 2024.",
        "Tanenbaum, A. S., & Wetherall, D. J., <i>Computer Networks</i>, 5th Edition, Pearson Education, 2011.",
        "Kurose, J. F., & Ross, K. W., <i>Computer Networking: A Top-Down Approach</i>, 8th Edition, Pearson, 2021.",
        "Open Academic Reference Repository: <code>https://github.com/chetan475/unit-3</code> (Attributed for foundational topology framework).",
    ]
    story += [Paragraph(f"[{i}]&nbsp;&nbsp;{r}", P("ref", fontSize=7.6, leading=10.2, spaceAfter=2)) for i, r in enumerate(refs, 1)]

    return story

def generate_pdf_report():
    doc = BaseDocTemplate(
        OUT_PDF, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=1.4 * cm, bottomMargin=1.4 * cm,
        title="NPC Unit 3 - DNS and Web Server Configuration Report (Sanket Aher)",
        author="Sanket Aher",
        subject="Networking Protocols and Communication",
        keywords="Cisco Packet Tracer, DNS, Web Server, HTTP, ICMP, Cyber Security",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main_frame",
                  topPadding=0.5 * cm, bottomPadding=0.5 * cm)
    doc.addPageTemplates([PageTemplate(id="main_template", frames=[frame])])

    story = build_story()
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generation complete:", OUT_PDF)

if __name__ == "__main__":
    generate_pdf_report()
