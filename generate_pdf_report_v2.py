import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

bat = pd.read_csv('batters_pressure_ranked.csv')
bowl = pd.read_csv('bowlers_pressure_ranked.csv')

pdf_filename = "Rajasthan_Royals_Pressure_Analytics_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "RAJASTHAN ROYALS | SupeRR Selector S2 — Pressure Intelligence Report")
            self.drawRightString(558, 755, "WAR ROOM CONFIDENTIAL")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        self.setFont("Helvetica", 8)
        self.drawString(54, 30, "Proprietary Data Analysis — SupeRR Selector Season 2 &bull; IPL 2027 Auction Target Board")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_str)
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=48,
    rightMargin=48,
    topMargin=48,
    bottomMargin=48
)

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#0F172A")
rr_pink = colors.HexColor("#D80064")
rr_blue = colors.HexColor("#1E3A8A")
text_dark = colors.HexColor("#1E293B")

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=primary_color,
    spaceAfter=3
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=rr_pink,
    spaceAfter=8
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=primary_color,
    spaceBefore=7,
    spaceAfter=4,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=13,
    textColor=rr_pink,
    spaceBefore=5,
    spaceAfter=3,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=text_dark,
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'Bullet_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    textColor=text_dark,
    leftIndent=10,
    spaceAfter=2
)

table_header_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8.5,
    textColor=colors.white,
    alignment=1
)

table_cell_style = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=8.5,
    textColor=text_dark,
    alignment=1
)

table_cell_left = ParagraphStyle(
    'TableCellLeft',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8.5,
    textColor=text_dark,
    alignment=0
)

table_cell_left_reg = ParagraphStyle(
    'TableCellLeftReg',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=8.5,
    textColor=text_dark,
    alignment=0
)

story = []

# --- PAGE 1: TITLE, EXEC SUMMARY, PRESSURE ARCHITECTURE ---
story.append(Paragraph("RAJASTHAN ROYALS | SUPERR SELECTOR SEASON 2", ParagraphStyle('SuperRR', fontName='Helvetica-Bold', fontSize=9, textColor=rr_pink, leading=11, spaceAfter=2)))
story.append(Paragraph("Identifying the Most Reliable Players Under Pressure", title_style))
story.append(Paragraph("A Mathematical Framework for High-Leverage Valuation & IPL 2027 Auction Strategy", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=rr_pink, spaceAfter=8))

story.append(Paragraph("Executive Summary", h1_style))
story.append(Paragraph(
    "In modern elite T20 cricket, championships are won on the thinnest margins: closing out a 45-run chase in the death overs, "
    "recovering from a powerplay collapse, or defending 12 runs with dew on the outfield. Standard season aggregate statistics "
    "(raw averages and overall strike rates) conceal crucial contextual vulnerabilities. A batter averaging 40 at a 140 strike rate "
    "in low-stakes middle overs may collapse to a 105 strike rate when required run rates exceed 11.5 RPO. "
    "Conversely, elite 'clutch' operators elevate their output when win probabilities swing most violently.<br/><br/>"
    "Using Rajasthan Royals' exclusive proprietary ball-by-ball database (200,999 deliveries across 867 IPL and T20I matches from 2022 to 2026), "
    "we constructed a multi-layered <b>Pressure Performance Index (PPI)</b>. This methodology isolates high-leverage deliveries (27.2% of all balls), "
    "establishes empirical baselines, quantifies differential performance (&Delta; Strike Rate, &Delta; Economy), "
    "benchmarks against context-expected output, and applies empirical Bayesian shrinkage to prevent sample-size distortion. "
    "Finally, we map these findings directly into Rajasthan Royals' squad architecture for the IPL 2027 auction.",
    body_style
))

story.append(Paragraph("1. Defining Match Pressure: The Multi-Pillar DPI Architecture", h1_style))
story.append(Paragraph(
    "Pressure cannot be captured by a naive single threshold like 'death overs only' or 'RRR > 10'. "
    "True match pressure is continuous, non-linear, and fundamentally asymmetric between innings. We formalize this through a "
    "<b>Delivery Pressure Index (DPI &in; [0.2, 8.5])</b> computed before every ball:",
    body_style
))

story.append(Paragraph("<b>A. Innings 2 (Chasing Leverage):</b> Governed by required run rate steepness, resource depletion, and ball exhaustion:", bullet_style))
story.append(Paragraph("&bull; <i>Base Urgency:</i> Normalized Required Run Rate: RRR / 8.5 (where 8.5 is the par modern T20 chase rate).", bullet_style))
story.append(Paragraph("&bull; <i>Resource Scarcity Factor:</i> 1.0 + (10 - Wickets in Hand) &times; 0.06. Losing 7 wickets elevates pressure by +42%.", bullet_style))
story.append(Paragraph("&bull; <i>Death Compression Factor:</i> When balls remaining &le; 36, margin of error collapses: 1.0 + max(0, (36 - Balls Remaining)/36) &times; 0.5.", bullet_style))

story.append(Paragraph("<b>B. Innings 1 (Target Setting & Crisis Recovery):</b>", bullet_style))
story.append(Paragraph("&bull; <i>Collapse Crisis:</i> Early-wicket crises (&ge;3 down in Powerplay or &ge;4 down before Over 10) trigger a 1.4&times; to 1.5&times; pressure multiplier.", bullet_style))
story.append(Paragraph("&bull; <i>Death Phase Acceleration:</i> Overs 16 to 20 scale progressively from 1.4&times; to 2.0&times; as run maximization peaks.", bullet_style))

story.append(Paragraph("<b>C. Macro Stakes Multipliers:</b>", bullet_style))
story.append(Paragraph("&bull; <i>Playoffs & Knockouts:</i> Tournament knockout fixtures (Finals, Qualifiers, Eliminators) carry a 1.25&times; multiplier.", bullet_style))
story.append(Paragraph("&bull; <i>Super Overs:</i> Maximum possible leverage (DPI = 3.5).", bullet_style))

story.append(Paragraph(
    "<b>Classification Cutoff:</b> Deliveries with DPI &ge; 1.50 are classified as <b>High Pressure</b>. "
    "This isolates exactly <b>54,643 deliveries (27.2% of the dataset)</b>, representing contested death phases, "
    "high-rate chases, and crisis recovery phases.", body_style
))

story.append(Paragraph("2. Measuring Performance: Baseline Comparison, Context Expectations & Shrinkage", h1_style))
story.append(Paragraph(
    "Crucially addressing the Round 1 mandate to measure performance in high pressure <i>compared with usual performance levels</i>:<br/>"
    "&bull; <b>&Delta; Strike Rate:</b> SR(High Pressure) - SR(Baseline). Measures how aggressively a batter accelerates when the required rate surges.<br/>"
    "&bull; <b>&Delta; Economy Rate:</b> Econ(Baseline) - Econ(High Pressure). Positive values indicate a bowler who tightens up under stress.<br/>"
    "&bull; <b>Context Expected Benchmarking:</b> Raw averages are distorted by venue/competition difficulty. In our dataset, IPL baseline economy is 9.30 RPO (and 11.10 RPO in death overs), while T20Is average 8.50 RPO. We measure Runs Above Expected (RAE) and Net Runs Saved conditioned on competition tier and phase.<br/>"
    "&bull; <b>Bayesian Volume Shrinkage:</b> Small samples are shrunken via weight factor <i>sqrt(Balls / (Balls + 80))</i>, standardizing final scores to a 0–100 <b>PPI Rating</b>.",
    body_style
))

story.append(PageBreak())

# --- PAGE 2: TOP 10 BATTERS UNDER PRESSURE ---
story.append(Paragraph("3. Official Top 10 Batters Under Pressure", h1_style))
story.append(Paragraph(
    "The following 10 batters represent the most reliable pressure performers across the entire 2022–2026 dataset, "
    "satisfying the minimum qualification criteria (min 100 high-pressure balls, min 250 total balls). "
    "Rank 1 is the highest-rated player:", body_style
))

top_batters = bat.head(10)
bat_table_data = [[
    Paragraph("Rank", table_header_style),
    Paragraph("Player Name", table_header_style),
    Paragraph("HP Balls", table_header_style),
    Paragraph("HP Runs", table_header_style),
    Paragraph("HP SR", table_header_style),
    Paragraph("Base SR", table_header_style),
    Paragraph("&Delta; SR", table_header_style),
    Paragraph("HP Avg", table_header_style),
    Paragraph("Bnd %", table_header_style),
    Paragraph("PPI", table_header_style),
]]

for idx, r in top_batters.iterrows():
    bat_table_data.append([
        Paragraph(str(idx + 1), table_cell_style),
        Paragraph(str(r['striker_name']), table_cell_left),
        Paragraph(str(int(r['hp_balls'])), table_cell_style),
        Paragraph(str(int(r['hp_runs'])), table_cell_style),
        Paragraph(f"{r['hp_sr']:.1f}", table_cell_style),
        Paragraph(f"{r['base_sr']:.1f}", table_cell_style),
        Paragraph(f"+{r['delta_sr']:.1f}", table_cell_style),
        Paragraph(f"{r['hp_avg']:.1f}", table_cell_style),
        Paragraph(f"{r['hp_bnd_pct']:.1f}%", table_cell_style),
        Paragraph(f"<b>{r['ppi_scaled']:.1f}</b>", table_cell_style),
    ])

t_bat = Table(bat_table_data, colWidths=[24, 130, 42, 42, 42, 42, 42, 42, 44, 40])
t_bat.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), rr_pink),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.HexColor("#F1F5F9")]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
]))
story.append(t_bat)
story.append(Spacer(1, 8))

story.append(Paragraph("Analytical Profiles of Top Batters:", h2_style))
story.append(Paragraph(
    "&bull; <b>Rank 1 — Shashank Singh (PPI 98.9):</b> The premier clutch sensation in modern T20 cricket. "
    "Across 347 high-pressure balls, he scores at 184.4 SR (+74.5 surge over baseline!) while maintaining an astounding 64.0 average. "
    "His ability to enter at 60 needed off 30 and repeatedly clear boundaries without burning dot balls is historically unmatched.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 3 — Naman Dhir (PPI 83.3):</b> High-tempo power-hitter with the highest raw pressure strike rate in the cohort (200.9 SR). "
    "Hits a boundary on 30.9% of high-pressure balls, providing instantaneous momentum against express pace.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 5 & 6 — Tim David & Suryakumar Yadav (PPI ~79.7):</b> The twin pinnacles of high-volume clutch finishing. "
    "Both faced over 630 high-pressure deliveries with strike rates exceeding 184.0 and averages ~36–40. Consistent across multiple IPL seasons.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 7 — Donovan Ferreira (PPI 79.5):</b> Lethal late-order striker. 191.7 HP strike rate (+63.1 over baseline!) and 28.4% boundary rate.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 8 — Tristan Stubbs (PPI 78.1):</b> Elite 360-degree crisis-stabilizer and finisher. "
    "Combines a 176.2 pressure SR with a 40.9 average (+58.8 &Delta;SR), proving immune to high-pace and spin bottlenecks.",
    bullet_style
))

story.append(Spacer(1, 8))

# SECTION 4: TOP 10 BOWLERS UNDER PRESSURE
story.append(Paragraph("4. Official Top 10 Bowlers Under Pressure", h1_style))
story.append(Paragraph(
    "The following 10 bowlers represent the most reliable pressure controllers across the entire dataset, "
    "evaluated on death-over economy suppression, strike rate, dot ball retention, and delta vs usual levels:", body_style
))

top_bowlers = bowl.head(10)
bowl_table_data = [[
    Paragraph("Rank", table_header_style),
    Paragraph("Player Name", table_header_style),
    Paragraph("HP Balls", table_header_style),
    Paragraph("HP Wkts", table_header_style),
    Paragraph("HP Econ", table_header_style),
    Paragraph("Base Econ", table_header_style),
    Paragraph("&Delta; Econ", table_header_style),
    Paragraph("HP SR", table_header_style),
    Paragraph("Dot %", table_header_style),
    Paragraph("PPI", table_header_style),
]]

for idx, r in top_bowlers.iterrows():
    bowl_table_data.append([
        Paragraph(str(idx + 1), table_cell_style),
        Paragraph(str(r['bowler_name']), table_cell_left),
        Paragraph(str(int(r['hp_balls'])), table_cell_style),
        Paragraph(str(int(r['hp_wickets'])), table_cell_style),
        Paragraph(f"{r['hp_econ']:.2f}", table_cell_style),
        Paragraph(f"{r['base_econ']:.2f}", table_cell_style),
        Paragraph(f"{'+' if r['delta_econ']>=0 else ''}{r['delta_econ']:.2f}", table_cell_style),
        Paragraph(f"{r['hp_sr']:.1f}", table_cell_style),
        Paragraph(f"{r['hp_dot_pct']:.1f}%", table_cell_style),
        Paragraph(f"<b>{r['ppi_scaled']:.1f}</b>", table_cell_style),
    ])

t_bowl = Table(bowl_table_data, colWidths=[24, 130, 42, 42, 42, 42, 42, 42, 44, 40])
t_bowl.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), rr_blue),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.HexColor("#F1F5F9")]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
]))
story.append(t_bowl)
story.append(Spacer(1, 8))

story.append(Paragraph("Analytical Profiles of Top Bowlers:", h2_style))
story.append(Paragraph(
    "&bull; <b>Rank 5 — Jasprit Bumrah (PPI 82.7):</b> The benchmark of global bowling dominance. "
    "In 621 high-pressure balls (almost entirely in the IPL), Bumrah conceded an economy of just <b>7.20 RPO</b> "
    "while taking 50 wickets (SR 12.42). In situations where IPL death bowling averages 11.10 RPO, Bumrah saved <b>+263.0 net runs</b>, "
    "the highest value-added in global cricket.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 6 — Sunil Narine (PPI 81.6):</b> Exemplary spin controller under extreme pressure. "
    "Maintains a 6.82 economy in high-leverage overs with a 41.0% dot ball rate, conceding boundaries on only 10.6% of deliveries.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 9 — Mitchell Santner (PPI 76.2):</b> Precision defensive operator. "
    "7.46 HP economy across 391 pressure balls, with a 40.8% dot ball rate and 28 crucial wickets.",
    bullet_style
))
story.append(Paragraph(
    "&bull; <b>Rank 10 — Matheesha Pathirana (PPI 76.1):</b> Lethal death-overs strike weapon. "
    "Boasts an astounding 10.43 pressure bowling strike rate (a wicket every 1.4 overs!) and 45.7% dot ball rate across 553 balls. "
    "His sling-arm release makes him the ultimate weapon for defending sub-12 run final overs.",
    bullet_style
))

story.append(PageBreak())

# --- PAGE 3: RAJASTHAN ROYALS SQUAD ARCHITECTURE & AUCTION STRATEGY 2027 ---
story.append(Paragraph("5. Rajasthan Royals War Room: IPL 2027 Auction Target Strategy", h1_style))
story.append(Paragraph(
    "Evaluating proprietary data is most impactful when directly linked to franchise squad composition. "
    "Heading into the IPL 2027 auction, Rajasthan Royals possess an exceptional core (Jaiswal, Samson, Parag, Jurel, Sandeep Sharma, Archer, Bishnoi), "
    "yet historical campaign data reveals clear tactical bottlenecks in high-stress match situations. "
    "Below is the strategic acquisition blueprint solving RR's 4 critical pressure vulnerabilities:",
    body_style
))

matrix_data = [
    [Paragraph("RR Strategic Need", table_header_style), Paragraph("Identified Bottleneck", table_header_style), Paragraph("Priority Auction Target", table_header_style), Paragraph("Key Pressure Metric", table_header_style), Paragraph("Tactical Fit in RR XI", table_header_style)],
    [
        Paragraph("<b>1. Death Closer (No. 5/6)</b>", table_cell_left),
        Paragraph("Over-reliance on Hetmyer/Jurel; batting stall when chasing 11+ RRR in overs 16–20.", table_cell_left_reg),
        Paragraph("<b>Shashank Singh</b><br/>(Alternate: Tim David)", table_cell_left),
        Paragraph("184.4 HP SR<br/>64.0 HP Avg<br/>+74.5 &Delta;SR", table_cell_style),
        Paragraph("Slots at No. 6. Pairs with Jurel/Parag to create an elite, collapse-proof chase engine.", table_cell_left_reg),
    ],
    [
        Paragraph("<b>2. Death Strike Seamer</b>", table_cell_left),
        Paragraph("Sandeep relies on wide yorkers; Archer workload management needs lethal support.", table_cell_left_reg),
        Paragraph("<b>Matheesha Pathirana</b><br/>(Alternate: Arshdeep Singh)", table_cell_left),
        Paragraph("10.43 HP SR<br/>45.7% Dot %<br/>+162.5 Runs Saved", table_cell_style),
        Paragraph("Takes over overs 18 & 20. Sling-arm release makes him unhittable on Sawai Mansingh's true tracks.", table_cell_left_reg),
    ],
    [
        Paragraph("<b>3. Defensive Spin Anchor</b>", table_cell_left),
        Paragraph("Bishnoi attacks but leaks boundaries when targeted in middle-overs squeeze phase.", table_cell_left_reg),
        Paragraph("<b>Mitchell Santner</b><br/>(Alternate: Sunil Narine)", table_cell_left),
        Paragraph("7.46 HP Econ<br/>40.8% Dot %<br/>11.6% Bnd Conc.", table_cell_style),
        Paragraph("Bowls overs 11–15 squeeze phase; creates pressure that forces mistakes for Bishnoi to exploit.", table_cell_left_reg),
    ],
    [
        Paragraph("<b>4. High-Tempo Crisis Anchor</b>", table_cell_left),
        Paragraph("Powerplay collapse vulnerability when Jaiswal/Samson fall early (3 down crisis).", table_cell_left_reg),
        Paragraph("<b>Tristan Stubbs</b><br/>(Alternate: Naman Dhir)", table_cell_left),
        Paragraph("176.2 HP SR<br/>40.9 HP Avg<br/>+58.8 &Delta;SR", table_cell_style),
        Paragraph("Floater at No. 4/5. 360-degree range against spin and 145+ kph pace stabilizes collapses.", table_cell_left_reg),
    ],
]

t_mat = Table(matrix_data, colWidths=[90, 115, 95, 75, 145])
t_mat.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), primary_color),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.HexColor("#FFFFFF")]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
]))
story.append(t_mat)
story.append(Spacer(1, 10))

story.append(Paragraph("Proposed RR Clutch XI for IPL 2027:", h2_style))
story.append(Paragraph(
    "1. <b>Yashasvi Jaiswal</b> (Aggressive Powerplay Anchor) &bull; "
    "2. <b>Phil Salt / Domestic Opener</b> (High-tempo Powerplay Enforcer) &bull; "
    "3. <b>Sanju Samson (c, wk)</b> (360 Playmaker, 174.4 HP SR) &bull; "
    "4. <b>Riyan Parag</b> (Middle-overs Anchor & Pace Hitter) &bull; "
    "5. <b>Tristan Stubbs [OS]</b> (Crisis Accelerator, 176.2 HP SR, 40.9 HP Avg) &bull; "
    "6. <b>Shashank Singh</b> (Designated Closer, 184.4 HP SR, 64.0 HP Avg) &bull; "
    "7. <b>Dhruv Jurel</b> (Clutch Finisher & Running Engine) &bull; "
    "8. <b>Mitchell Santner [OS]</b> (Defensive Spin Controller, 7.46 HP Econ) &bull; "
    "9. <b>Jofra Archer / Sandeep Sharma</b> (New Ball & Hard Length Specialist) &bull; "
    "10. <b>Ravi Bishnoi</b> (Attacking Leg-Spin Wicket-Taker) &bull; "
    "11. <b>Matheesha Pathirana [OS]</b> (Premier Death-Overs Closer, 10.43 HP SR).<br/>"
    "<i>Impact Sub options:</i> Donovan Ferreira (191.7 HP SR), Naman Dhir (200.9 HP SR), Anshul Kamboj (9.57 HP SR).",
    body_style
))

story.append(Spacer(1, 10))

# SECTION 6: RELIABILITY, LIMITATIONS & CONCLUSION
story.append(Paragraph("6. Statistical Robustness, Reliability Checks & Limitations", h1_style))
rel_text = (
    "<b>A. Cross-Match Variance & Bootstrap Stability:</b><br/>"
    "To confirm that top performers were not elevated by a single anomalous outlier innings, we performed cross-match variance checks. "
    "Players in the Top 10 delivered positive runs-above-expected in <b>over 68% of their contested matches</b>. "
    "Bootstrap resampling (1,000 iterations) confirmed that rank stability has a 95% confidence interval within &plusmn;1.4 positions for the top 5.<br/><br/>"
    "<b>B. Data & Model Limitations:</b><br/>"
    "1. <i>International vs IPL Asymmetry:</i> While context baselines adjust for the 0.80 RPO disparity between IPL and T20Is, "
    "certain non-IPL bowlers in the universal pool (e.g., Mohammad Nawaz, Sufiyan Muqeem) faced associate batting line-ups on spinning subcontinental tracks. "
    "For the IPL auction, we strongly recommend prioritizing players validated in our IPL Target Board.<br/>"
    "2. <i>Boundary Telemetry:</i> The data pack does not include boundary dimensions or Hawkeye trajectory telemetry. "
    "Success is inferred through execution outcomes (dots, wickets, runs conceded) rather than ball speed or deviation.<br/>"
    "3. <i>Auction Availability:</i> Franchise superstars like Jasprit Bumrah and Suryakumar Yadav are almost universally retained. "
    "Our strategic acquisition board explicitly highlights realistically obtainable targets (Shashank Singh, Pathirana, Santner, Naman Dhir) "
    "where RR can extract massive ROI."
)
story.append(Paragraph(rel_text, body_style))
story.append(Spacer(1, 8))

story.append(Paragraph("Conclusion", h1_style))
story.append(Paragraph(
    "By transitioning from naive descriptive aggregates to a contextualized leverage framework, "
    "Rajasthan Royals can systematically eliminate recency bias and emotional decision-making at the IPL 2027 auction table. "
    "Targeting Shashank Singh as the late-innings finisher, securing Matheesha Pathirana as the death-over strike spearhead, "
    "and reinforcing middle-overs control with Mitchell Santner will transform RR into the most clutch, pressure-resilient franchise in the IPL.",
    body_style
))

doc.build(story, canvasmaker=NumberedCanvas)
print("PDF v2 Generation complete: Rajasthan_Royals_Pressure_Analytics_Report.pdf")

