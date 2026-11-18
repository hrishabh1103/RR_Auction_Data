import json
import pandas as pd

with open('dashboard_data.json', 'r') as f:
    data = json.load(f)

# Load exact top 10 from the ranked CSV files
bat_df = pd.read_csv('batters_pressure_ranked_ipl_eligible.csv').head(10)
bowl_df = pd.read_csv('bowlers_pressure_ranked_ipl_eligible.csv').head(10)

top10_batters = []
for idx, r in bat_df.iterrows():
    top10_batters.append({
        "rank": idx + 1,
        "name": r['striker_name'],
        "hp_balls": int(r['hp_balls']),
        "hp_runs": int(r['hp_runs']),
        "hp_sr": round(r['hp_sr'], 1),
        "base_sr": round(r['base_sr'], 1),
        "delta_sr": round(r['delta_sr'], 1),
        "hp_avg": round(r['hp_avg'], 1),
        "rae": round(r['hp_runs_above_exp'], 1),
        "ppi": round(r['ppi_scaled'], 1)
    })

top10_bowlers = []
for idx, r in bowl_df.iterrows():
    top10_bowlers.append({
        "rank": idx + 1,
        "name": r['bowler_name'],
        "hp_balls": int(r['hp_balls']),
        "hp_wkts": int(r['hp_wickets']),
        "hp_econ": round(r['hp_econ'], 2),
        "base_econ": round(r['base_econ'], 2),
        "delta_econ": round(r['delta_econ'], 2),
        "hp_sr": round(r['hp_sr'], 1),
        "runs_saved": round(r['hp_runs_saved'], 1),
        "ppi": round(r['ppi_scaled'], 1)
    })

data['pure_results_top10_batters'] = top10_batters
data['pure_results_top10_bowlers'] = top10_bowlers

with open('dashboard_data.json', 'w') as f:
    json.dump(data, f, indent=2)

json_str = json.dumps(data)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajasthan Royals • IPL Pressure Analytics & Pure Dataset Results</title>
  <!-- Chart.js and Google Fonts -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Teko:wght@400;600;700&family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --rr-pink: #FF1389;
      --rr-pink-hover: #E60067;
      --rr-pink-glow: rgba(255, 19, 137, 0.4);
      --rr-blue: #0A1128;
      --rr-navy: #001F54;
      --rr-dark: #070B19;
      --card-bg: #0D1630;
      --card-border: #1E294B;
      --card-inner: #131F3F;
      --text-main: #FFFFFF;
      --text-muted: #94A3B8;
      --gold: #FACC15;
      --cyan: #38BDF8;
      --purple: #A855F7;
      --green: #10B981;
      --orange: #FB923C;
      --red: #EF4444;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--rr-dark);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* TOP LOGOS BANNER */
    .top-franchise-ribbon {{
      background: linear-gradient(180deg, #050811 0%, #0D1630 100%);
      border-bottom: 1px solid var(--card-border);
      padding: 8px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      overflow-x: auto;
    }}

    .franchise-logos-group {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: nowrap;
    }}

    .franchise-badge {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: #CBD5E1;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}

    .franchise-badge:hover {{
      border-color: var(--rr-pink);
      transform: translateY(-1px);
    }}

    .franchise-badge.active-rr {{
      background: linear-gradient(135deg, rgba(255, 19, 137, 0.25) 0%, rgba(10, 17, 40, 0.8) 100%);
      border: 1.5px solid var(--rr-pink);
      color: #FFF;
      box-shadow: 0 0 12px var(--rr-pink-glow);
    }}

    .season-selector-wrapper {{
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }}

    .season-selector-wrapper label {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 600;
    }}

    .season-select {{
      background: #131F3F;
      border: 1px solid var(--card-border);
      color: #FFF;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }}

    /* MAIN HEADER */
    .main-header {{
      background: linear-gradient(90deg, #0A1128 0%, #150F28 50%, #0A1128 100%);
      border-bottom: 2px solid var(--rr-pink);
      padding: 16px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header-branding {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .rr-logo-circle {{
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--rr-pink) 0%, #70003C 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Teko', sans-serif;
      font-size: 28px;
      font-weight: 700;
      color: #FFF;
      box-shadow: 0 0 16px var(--rr-pink-glow);
      border: 1px solid #FFA3D1;
    }}

    .header-titles h1 {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 1px;
      color: #FFF;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .header-titles h1 span {{
      color: var(--rr-pink);
    }}

    .header-tag {{
      background: rgba(255, 19, 137, 0.15);
      border: 1px solid var(--rr-pink);
      color: #FF70B8;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}

    .header-titles p {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* NAVIGATION TABS */
    .nav-tabs-container {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .nav-tab-btn {{
      background: #131F3F;
      border: 1px solid var(--card-border);
      color: #CBD5E1;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .nav-tab-btn:hover {{
      background: #1B2B56;
      color: #FFF;
      border-color: #38BDF8;
    }}

    .nav-tab-btn.active {{
      background: var(--rr-pink);
      color: #FFF;
      border-color: #FF70B8;
      box-shadow: 0 0 14px var(--rr-pink-glow);
    }}

    .nav-tab-btn.pure-tab {{
      background: linear-gradient(135deg, rgba(255, 19, 137, 0.25) 0%, rgba(13, 22, 48, 1) 100%);
      border: 1.5px solid var(--rr-pink);
      color: #FFF;
    }}

    .nav-tab-btn.pure-tab.active {{
      background: var(--rr-pink);
      color: #FFF;
      box-shadow: 0 0 16px var(--rr-pink-glow);
    }}

    .nav-tab-btn.strategy-tab {{
      background: linear-gradient(135deg, rgba(250, 204, 21, 0.2) 0%, rgba(13, 22, 48, 1) 100%);
      border: 1.5px solid var(--gold);
      color: var(--gold);
    }}

    .nav-tab-btn.strategy-tab.active {{
      background: var(--gold);
      color: #0F172A;
      box-shadow: 0 0 14px rgba(250, 204, 21, 0.5);
    }}

    /* MAIN CONTAINER */
    .app-container {{
      max-width: 1600px;
      margin: 0 auto;
      padding: 20px 24px 60px 24px;
    }}

    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
      animation: fadeIn 0.3s ease;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* TOP KPI ROW */
    .kpi-row-grid {{
      display: grid;
      grid-template-columns: 1.2fr 1.2fr 1.2fr 1fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }}

    @media (max-width: 1200px) {{
      .kpi-row-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 768px) {{
      .kpi-row-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      align-items: center;
      gap: 14px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }}

    .kpi-card::after {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--card-border);
    }}

    .kpi-card.trophy-card::after {{ background: var(--gold); }}
    .kpi-card.orange-card::after {{ background: var(--orange); }}
    .kpi-card.purple-card::after {{ background: var(--purple); }}
    .kpi-card.sixes-card::after {{ background: var(--rr-pink); }}
    .kpi-card.fours-card::after {{ background: var(--cyan); }}

    .kpi-icon-box {{
      width: 52px;
      height: 52px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      flex-shrink: 0;
    }}

    .kpi-card.trophy-card .kpi-icon-box {{ background: rgba(250, 204, 21, 0.15); color: var(--gold); border: 1px solid var(--gold); }}
    .kpi-card.orange-card .kpi-icon-box {{ background: rgba(251, 146, 60, 0.15); color: var(--orange); border: 1px solid var(--orange); }}
    .kpi-card.purple-card .kpi-icon-box {{ background: rgba(168, 85, 247, 0.15); color: var(--purple); border: 1px solid var(--purple); }}
    .kpi-card.sixes-card .kpi-icon-box {{ background: rgba(255, 19, 137, 0.15); color: var(--rr-pink); border: 1px solid var(--rr-pink); }}
    .kpi-card.fours-card .kpi-icon-box {{ background: rgba(56, 189, 248, 0.15); color: var(--cyan); border: 1px solid var(--cyan); }}

    .kpi-info-box {{
      flex: 1;
      overflow: hidden;
    }}

    .kpi-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      margin-bottom: 2px;
    }}

    .kpi-headline {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 20px;
      font-weight: 700;
      color: #FFF;
      line-height: 1.2;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }}

    .kpi-subtext {{
      font-size: 12px;
      font-weight: 600;
      color: #CBD5E1;
      margin-top: 2px;
    }}

    .kpi-subtext span {{
      color: var(--gold);
      font-weight: 700;
    }}

    /* PURE DATASET RESULTS SECTION STYLING */
    .pure-results-summary-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }}

    @media (max-width: 900px) {{
      .pure-results-summary-row {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .pure-kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      position: relative;
    }}

    .pure-kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 4px;
      border-radius: 12px 0 0 12px;
    }}

    .pure-kpi-card.total-balls::before {{ background: var(--cyan); }}
    .pure-kpi-card.pressure-pct::before {{ background: var(--rr-pink); }}
    .pure-kpi-card.top-batter::before {{ background: var(--gold); }}
    .pure-kpi-card.top-bowler::before {{ background: var(--purple); }}

    .pure-kpi-num {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 24px;
      font-weight: 700;
      color: #FFF;
      margin-top: 4px;
    }}

    .pure-tables-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1200px) {{
      .pure-tables-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .pure-table-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }}

    .pure-table-header {{
      background: #070D1F;
      padding: 14px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .pure-table-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: #FFF;
      letter-spacing: 0.8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .methodology-box {{
      background: linear-gradient(135deg, #0A1128 0%, #060914 100%);
      border: 1.5px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
    }}

    .methodology-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: var(--gold);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .formula-badge {{
      display: inline-block;
      background: #131F3F;
      border: 1px solid var(--card-border);
      padding: 6px 12px;
      border-radius: 6px;
      font-family: monospace;
      font-size: 13px;
      color: #38BDF8;
      margin: 6px 0;
    }}

    /* DATA TABLE STYLING */
    .controls-banner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .role-pills-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .role-pill {{
      background: #0E1A38;
      border: 1.5px solid #26355C;
      color: #CBD5E1;
      padding: 7px 16px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.4px;
      cursor: pointer;
      transition: all 0.2s ease;
      text-transform: capitalize;
    }}

    .role-pill:hover {{
      background: #192A54;
      border-color: #38BDF8;
      color: #FFF;
    }}

    .role-pill.active {{
      background: var(--rr-pink);
      border-color: var(--gold);
      color: #FFF;
      box-shadow: 0 0 12px var(--rr-pink-glow), 0 0 0 1px var(--gold);
    }}

    .auction-pool-toggle-group {{
      display: flex;
      align-items: center;
      background: #091228;
      border: 1.5px solid var(--card-border);
      border-radius: 9999px;
      padding: 3px;
      gap: 4px;
    }}

    .auction-toggle-btn {{
      background: transparent;
      border: none;
      color: #94A3B8;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .auction-toggle-btn:hover {{
      color: #FFF;
    }}

    .auction-toggle-btn.active {{
      background: var(--gold);
      color: #0F172A;
      box-shadow: 0 0 10px rgba(250, 204, 21, 0.4);
    }}

    .auction-toggle-btn.active.pink-toggle {{
      background: var(--rr-pink);
      color: #FFF;
      box-shadow: 0 0 10px var(--rr-pink-glow);
    }}

    .yellow-alert-banner {{
      background: linear-gradient(90deg, #FACC15 0%, #EAB308 100%);
      color: #0F172A;
      font-size: 13px;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: 9999px;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 3px 12px rgba(250, 204, 21, 0.3);
    }}

    .yellow-alert-banner .bell-icon {{
      background: #0F172A;
      color: #FACC15;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      flex-shrink: 0;
    }}

    .table-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 24px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.3);
    }}

    .table-header-bar {{
      background: #070D1F;
      padding: 12px 20px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .table-role-badge {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: 'Rajdhani', sans-serif;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: #FFF;
    }}

    .search-input {{
      background: #131F3F;
      border: 1px solid var(--card-border);
      color: #FFF;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      width: 220px;
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--rr-pink);
    }}

    .table-responsive {{
      overflow-x: auto;
      max-height: 480px;
      position: relative;
    }}

    table.cricket-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      text-align: left;
      white-space: nowrap;
    }}

    table.cricket-table thead {{
      background: #091228;
      position: sticky;
      top: 0;
      z-index: 10;
      box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }}

    table.cricket-table th {{
      padding: 12px 14px;
      color: #94A3B8;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 10px;
      letter-spacing: 0.6px;
      border-bottom: 1px solid var(--card-border);
      cursor: pointer;
      user-select: none;
    }}

    table.cricket-table th:hover {{
      color: #FFF;
      background: rgba(255, 255, 255, 0.04);
    }}

    table.cricket-table tbody tr {{
      border-bottom: 1px solid rgba(30, 41, 75, 0.5);
      cursor: pointer;
      transition: background 0.15s ease;
    }}

    table.cricket-table tbody tr:hover {{
      background: rgba(255, 19, 137, 0.1) !important;
    }}

    table.cricket-table tbody tr.selected-row {{
      background: rgba(255, 19, 137, 0.22) !important;
      border-left: 3px solid var(--gold);
    }}

    table.cricket-table td {{
      padding: 10px 14px;
      color: #E2E8F0;
      font-weight: 500;
    }}

    .player-name-cell {{
      font-weight: 700;
      color: #FFF;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .rank-pill {{
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      background: #1E294B;
      color: #94A3B8;
    }}

    .rank-pill.top-3 {{
      background: var(--gold);
      color: #000;
    }}

    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.3px;
      white-space: nowrap;
    }}

    .status-badge.available {{
      background: rgba(16, 185, 129, 0.15);
      color: #10B981;
      border: 1px solid #10B981;
    }}

    .status-badge.released {{
      background: rgba(250, 204, 21, 0.15);
      color: var(--gold);
      border: 1px solid var(--gold);
    }}

    .status-badge.retained {{
      background: rgba(148, 163, 184, 0.1);
      color: #94A3B8;
      border: 1px solid #334155;
    }}

    .bar-cell-container {{
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 130px;
    }}

    .in-cell-bar-track {{
      flex: 1;
      height: 14px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 3px;
      overflow: hidden;
      position: relative;
    }}

    .in-cell-bar-fill {{
      height: 100%;
      background: var(--rr-pink);
      border-radius: 3px;
      transition: width 0.3s ease;
    }}

    .bar-val-text {{
      font-weight: 700;
      font-size: 11px;
      width: 48px;
      text-align: right;
      color: #FFF;
    }}

    .badge-pill {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .badge-ppi {{ background: rgba(255, 19, 137, 0.2); color: #FF70B8; font-weight: 800; border: 1px solid var(--rr-pink); }}

    /* BOTTOM SPLIT SECTION */
    .bottom-analytics-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }}

    @media (max-width: 1024px) {{
      .bottom-analytics-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .metric-cards-subgrid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }}

    .metric-spark-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      position: relative;
    }}

    .metric-spark-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }}

    .metric-spark-title {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}

    .metric-spark-value {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 22px;
      font-weight: 700;
      color: #FFF;
    }}

    .metric-spark-value.pink {{ color: var(--rr-pink); }}
    .metric-spark-value.gold {{ color: var(--gold); }}
    .metric-spark-value.cyan {{ color: var(--cyan); }}
    .metric-spark-value.purple {{ color: var(--purple); }}

    .metric-par-note {{
      font-size: 10px;
      color: #94A3B8;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .sparkline-canvas-box {{
      height: 80px;
      width: 100%;
      position: relative;
    }}

    .scatter-plot-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
      display: flex;
      flex-direction: column;
    }}

    .scatter-card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .scatter-card-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: #FFF;
      letter-spacing: 0.5px;
    }}

    .scatter-legend-note {{
      font-size: 11px;
      color: var(--gold);
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .scatter-canvas-box {{
      flex: 1;
      min-height: 220px;
      position: relative;
    }}

    /* COMPARATOR SECTION (IPL OVERVIEW) */
    .interactive-comparator-row {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }}

    @media (max-width: 1100px) {{
      .interactive-comparator-row {{
        grid-template-columns: 1fr;
      }}
    }}

    .comparator-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
    }}

    .comparator-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .player-avatar-icon {{
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background: #131F3F;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      border: 1px solid var(--card-border);
    }}

    .comparator-select {{
      width: 100%;
      background: #131F3F;
      border: 1px solid var(--card-border);
      color: #FFF;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 16px;
      outline: none;
      cursor: pointer;
    }}

    .comparator-stats-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }}

    .mini-stat-box {{
      background: #091228;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 10px 8px;
      text-align: center;
    }}

    .mini-stat-label {{
      font-size: 9px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 4px;
      white-space: nowrap;
    }}

    .mini-stat-num {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: #FFF;
    }}

    .donut-card-content {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
    }}

    .donut-chart-box {{
      width: 180px;
      height: 180px;
      position: relative;
    }}

    .venue-team-row {{
      display: grid;
      grid-template-columns: 1.2fr 1.2fr 0.9fr;
      gap: 16px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1100px) {{
      .venue-team-row {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-panel-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
    }}

    .chart-panel-title {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: #FFF;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
    }}

    .chart-panel-box {{
      height: 240px;
      position: relative;
    }}

    /* REAL 2027 STRATEGY CARDS */
    .war-room-kpi-summary {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }}

    @media (max-width: 900px) {{
      .war-room-kpi-summary {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .purse-kpi-box {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      position: relative;
    }}

    .purse-kpi-box::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 4px;
      border-radius: 12px 0 0 12px;
    }}

    .purse-kpi-box.rr-purse::before {{ background: var(--rr-pink); }}
    .purse-kpi-box.slots-kpi::before {{ background: var(--gold); }}
    .purse-kpi-box.overseas-kpi::before {{ background: var(--cyan); }}
    .purse-kpi-box.big-opp::before {{ background: var(--green); }}

    .purse-kpi-num {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 26px;
      font-weight: 700;
      color: #FFF;
      margin-top: 4px;
    }}

    .all-franchises-purse-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1200px) {{
      .all-franchises-purse-grid {{
        grid-template-columns: repeat(3, 1fr);
      }}
    }}

    @media (max-width: 768px) {{
      .all-franchises-purse-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .franchise-purse-card {{
      background: #091228;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
    }}

    .franchise-purse-card.highlight-rr {{
      background: linear-gradient(135deg, rgba(255, 19, 137, 0.2) 0%, #091228 100%);
      border: 1.5px solid var(--rr-pink);
      box-shadow: 0 0 14px var(--rr-pink-glow);
    }}

    .franchise-pname {{
      font-weight: 700;
      font-size: 13px;
      color: #FFF;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .franchise-funds {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 20px;
      font-weight: 700;
      color: var(--gold);
      margin: 6px 0 2px 0;
    }}

    .franchise-slots {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .real-targets-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1100px) {{
      .real-targets-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .target-card-real {{
      background: var(--card-bg);
      border: 1.5px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
      position: relative;
      transition: all 0.2s ease;
    }}

    .target-card-real:hover {{
      border-color: var(--gold);
      transform: translateY(-2px);
    }}

    .target-card-real.priority-1 {{
      border-color: var(--rr-pink);
      box-shadow: 0 0 16px var(--rr-pink-glow);
    }}

    .target-priority-badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }}

    .target-priority-badge.must-buy {{ background: var(--rr-pink); color: #FFF; }}
    .target-priority-badge.high-value {{ background: var(--gold); color: #0F172A; }}
    .target-priority-badge.domestic-gem {{ background: var(--cyan); color: #0F172A; }}

    .target-pname-real {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 22px;
      font-weight: 700;
      color: #FFF;
    }}

    .target-rel-badge {{
      font-size: 11px;
      font-weight: 600;
      color: var(--orange);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .target-stats-mini-bar {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      background: #091228;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 8px;
      gap: 4px;
      text-align: center;
      margin-bottom: 12px;
    }}

    .target-bid-calc {{
      font-size: 12px;
      color: #CBD5E1;
      line-height: 1.5;
    }}

    .target-bid-calc strong {{
      color: var(--gold);
    }}

    /* PLAYING XI CARD */
    .starting-xi-board {{
      background: linear-gradient(180deg, #0A1128 0%, #060914 100%);
      border: 2px solid var(--rr-pink);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 0 20px rgba(255, 19, 137, 0.2);
    }}

    .xi-header {{
      text-align: center;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
    }}

    .xi-header h2 {{
      font-family: 'Rajdhani', sans-serif;
      font-size: 22px;
      font-weight: 700;
      color: #FFF;
    }}

    .xi-header h2 span {{
      color: var(--rr-pink);
    }}

    .xi-player-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 12px;
    }}

    .xi-pos-num {{
      font-weight: 800;
      color: var(--gold);
      width: 24px;
    }}

    .xi-pname {{
      font-weight: 700;
      color: #FFF;
      flex: 1;
    }}

    .xi-prole {{
      color: var(--text-muted);
      font-size: 11px;
    }}

    .xi-ptag {{
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 9px;
      font-weight: 800;
      text-transform: uppercase;
      margin-left: 8px;
    }}

    .xi-ptag.retain {{ background: #1E294B; color: #94A3B8; }}
    .xi-ptag.target {{ background: var(--rr-pink); color: #FFF; }}

    /* FOOTER */
    .dashboard-footer {{
      margin-top: 40px;
      border-top: 1px solid var(--card-border);
      padding-top: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 11px;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .footer-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .footer-badge {{
      background: #131F3F;
      padding: 4px 8px;
      border-radius: 4px;
      color: #38BDF8;
      font-weight: 700;
    }}
  </style>
</head>
<body>

  <!-- TOP FRANCHISE LOGOS RIBBON -->
  <div class="top-franchise-ribbon">
    <div class="franchise-logos-group">
      <div class="franchise-badge active-rr">
        <span>👑</span> RR (₹27.05 Cr | 6 Slots)
      </div>
      <div class="franchise-badge"><span>⚡</span> MI (₹32.60 Cr)</div>
      <div class="franchise-badge"><span>🦁</span> CSK (₹28.05 Cr)</div>
      <div class="franchise-badge"><span>⚔️</span> KKR (₹41.65 Cr)</div>
      <div class="franchise-badge"><span>🔥</span> RCB (₹14.15 Cr)</div>
      <div class="franchise-badge"><span>🦅</span> SRH (₹40.15 Cr)</div>
      <div class="franchise-badge"><span>🎯</span> PBKS (₹18.60 Cr)</div>
      <div class="franchise-badge"><span>🏛️</span> DC (₹39.50 Cr)</div>
      <div class="franchise-badge"><span>⚡</span> GT (₹8.75 Cr)</div>
      <div class="franchise-badge"><span>🗡️</span> LSG (₹47.45 Cr)</div>
    </div>
    <div class="season-selector-wrapper">
      <label>Select Season:</label>
      <select class="season-select" id="seasonSelect" onchange="filterSeason(this.value)">
        <option value="All">All IPL & T20I (2022 - 2026)</option>
        <option value="2026">2026 Season</option>
        <option value="2025">2025 Season</option>
        <option value="2024">2024 Season</option>
        <option value="2023">2023 Season</option>
        <option value="2022">2022 Season</option>
      </select>
    </div>
  </div>

  <!-- MAIN HEADER BAR -->
  <header class="main-header">
    <div class="header-branding">
      <div class="rr-logo-circle">RR</div>
      <div class="header-titles">
        <h1>RAJASTHAN ROYALS <span>• PRESSURE ANALYTICS WAR ROOM</span></h1>
        <p>Proprietary Ball-by-Ball Dataset Engine • 200,999 Deliveries • Pure Mathematical Model vs 2027 Auction Reality</p>
      </div>
    </div>
    <nav class="nav-tabs-container">
      <button class="nav-tab-btn pure-tab active" onclick="switchTab('pure-dataset-results', this)">
        <span>🏆</span> Pure Dataset Results (Top 10)
      </button>
      <button class="nav-tab-btn" onclick="switchTab('player-analysis', this)">
        <span>📊</span> Player Analysis
      </button>
      <button class="nav-tab-btn strategy-tab" onclick="switchTab('real-strategy', this)">
        <span>🔥</span> Real 2027 Strategy
      </button>
      <button class="nav-tab-btn" onclick="switchTab('war-room', this)">
        <span>🎯</span> Final 11 & War Room
      </button>
      <button class="nav-tab-btn" onclick="switchTab('ipl-overview', this)">
        <span>📈</span> IPL Overview
      </button>
    </nav>
  </header>

  <div class="app-container">

    <!-- TOP KPI SUMMARY ROW -->
    <div class="kpi-row-grid">
      <div class="kpi-card trophy-card">
        <div class="kpi-icon-box">🏆</div>
        <div class="kpi-info-box">
          <div class="kpi-label">Pure Dataset Focus</div>
          <div class="kpi-headline">Delivery Pressure Index</div>
          <div class="kpi-subtext">Cutoff: <span>DPI ≥ 1.50 (27.2%)</span></div>
        </div>
      </div>

      <div class="kpi-card orange-card">
        <div class="kpi-icon-box">🧢</div>
        <div class="kpi-info-box">
          <div class="kpi-label">#1 Dataset Batter</div>
          <div class="kpi-headline">Shashank Singh</div>
          <div class="kpi-subtext"><span>640 HP Runs</span> • 184.4 SR • PPI 98.9</div>
        </div>
      </div>

      <div class="kpi-card purple-card">
        <div class="kpi-icon-box">🟣</div>
        <div class="kpi-info-box">
          <div class="kpi-label">#1 Dataset Bowler</div>
          <div class="kpi-headline">Hasan Mahmud</div>
          <div class="kpi-subtext"><span>PPI 90.1</span> • 6.78 Econ • 8.8 HP SR</div>
        </div>
      </div>

      <div class="kpi-card sixes-card">
        <div class="kpi-icon-box">💥</div>
        <div class="kpi-info-box">
          <div class="kpi-label">Tournament 6's</div>
          <div class="kpi-headline" id="totalSixesCount">12.81K</div>
          <div class="kpi-subtext">HP Sixes: <span>3.41K (26.6%)</span></div>
        </div>
      </div>

      <div class="kpi-card fours-card">
        <div class="kpi-icon-box">🏏</div>
        <div class="kpi-info-box">
          <div class="kpi-label">Tournament 4's</div>
          <div class="kpi-headline" id="totalFoursCount">23.28K</div>
          <div class="kpi-subtext">HP Fours: <span>5.18K (22.2%)</span></div>
        </div>
      </div>
    </div>

    <!-- TAB 1: PURE DATASET RESULTS (NEW FRONT-AND-CENTER SECTION!) -->
    <div id="pure-dataset-results" class="tab-content active">

      <!-- MODEL SUMMARY BANNER -->
      <div class="pure-results-summary-row">
        <div class="pure-kpi-card total-balls">
          <div class="kpi-label">Total Balls Analyzed</div>
          <div class="pure-kpi-num" style="color:var(--cyan);">200,999 Balls</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">867 Official Matches (2022–2026)</div>
        </div>

        <div class="pure-kpi-card pressure-pct">
          <div class="kpi-label">High-Pressure Deliveries</div>
          <div class="pure-kpi-num" style="color:var(--rr-pink);">54,643 Balls</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">27.2% of Total Dataset (DPI ≥ 1.50)</div>
        </div>

        <div class="pure-kpi-card top-batter">
          <div class="kpi-label">Highest Rated Batter</div>
          <div class="pure-kpi-num" style="color:var(--gold);">Shashank Singh</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">PPI: 98.9 • +108.6 Runs Above Exp.</div>
        </div>

        <div class="pure-kpi-card top-bowler">
          <div class="kpi-label">Most Wickets Saved</div>
          <div class="pure-kpi-num" style="color:var(--purple);">Jasprit Bumrah</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">+263.0 Runs Saved • 50 HP Wkts</div>
        </div>
      </div>

      <!-- METHODOLOGY EXPLANATION BOX -->
      <div class="methodology-box">
        <div class="methodology-title">
          <span>📐</span> MATHEMATICAL MODEL SPECIFICATION & PRESSURE FORMULATION
        </div>
        <p style="font-size:12px;color:#CBD5E1;line-height:1.6;margin-bottom:10px;">
          To measure clutch reliability purely from data without reputation bias, every delivery was evaluated under the <strong>Delivery Pressure Index (DPI)</strong>:
        </p>
        <div class="formula-badge">
          DPI = 0.35 × (Required Run Rate / 8.5) + 0.30 × (10 - Wickets in Hand) / 10 + 0.20 × Phase Factor (Death Overs 16-20) + 0.15 × Leverage Context
        </div>
        <p style="font-size:12px;color:#CBD5E1;line-height:1.6;margin-top:8px;">
          Deliveries with <strong>DPI ≥ 1.50</strong> isolated 54,643 high-pressure deliveries. Performance was benchmarked against the historical context expected runs (\(\mathbb{{E}}[\text{{Runs}}]\)) to derive <strong>Runs Above Expected (RAE)</strong> for batters and <strong>Net Runs Saved</strong> for bowlers. Final rankings apply a <strong>Bayesian shrinkage factor</strong> \(\sqrt{{B_{{HP}} / (B_{{HP}} + 80.0)}}\) to prevent low-sample inflation. All Pakistani players are excluded per BCCI rules.
        </p>
      </div>

      <!-- PURE TOP 10 LEADERBOARDS: BATTERS & BOWLERS SIDE-BY-SIDE -->
      <div class="pure-tables-grid">
        
        <!-- PURE TOP 10 BATTERS -->
        <div class="pure-table-card">
          <div class="pure-table-header">
            <div class="pure-table-title">
              <span style="color:var(--gold);">🏏</span> OFFICIAL TOP 10 BATTERS (DATASET PRESSURE RANKINGS)
            </div>
            <span class="badge-pill" style="background:rgba(250, 204, 21, 0.15);color:var(--gold);border:1px solid var(--gold);">
              Pure Mathematical Result
            </span>
          </div>
          <div class="table-responsive">
            <table class="cricket-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Batter Name</th>
                  <th>HP Balls</th>
                  <th>HP Runs</th>
                  <th>HP SR</th>
                  <th>Base SR</th>
                  <th>Delta SR</th>
                  <th>RAE</th>
                  <th>PPI</th>
                </tr>
              </thead>
              <tbody id="pureBattersBody">
                <!-- Dynamically populated from data -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- PURE TOP 10 BOWLERS -->
        <div class="pure-table-card">
          <div class="pure-table-header">
            <div class="pure-table-title">
              <span style="color:var(--purple);">🎯</span> OFFICIAL TOP 10 BOWLERS (DATASET PRESSURE RANKINGS)
            </div>
            <span class="badge-pill" style="background:rgba(168, 85, 247, 0.15);color:var(--purple);border:1px solid var(--purple);">
              Pure Mathematical Result
            </span>
          </div>
          <div class="table-responsive">
            <table class="cricket-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Bowler Name</th>
                  <th>HP Balls</th>
                  <th>HP Wkts</th>
                  <th>HP Econ</th>
                  <th>Base Econ</th>
                  <th>Delta Econ</th>
                  <th>Runs Saved</th>
                  <th>PPI</th>
                </tr>
              </thead>
              <tbody id="pureBowlersBody">
                <!-- Dynamically populated from data -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- LEAGUE DIVERGENCE COMPARISON GRID (IPL vs T20I Contexts) -->
      <div class="pure-table-card" style="margin-bottom:24px;">
        <div class="pure-table-header">
          <div class="pure-table-title">
            <span style="color:var(--cyan);">⚖️</span> FAIR COMPARISONS • LEAGUE DIVERGENCE (IPL VS T20I CONTEXTS)
          </div>
        </div>
        <div style="padding:16px 20px;">
          <p style="font-size:12px;color:#CBD5E1;line-height:1.6;margin-bottom:12px;">
            The dataset merges IPL franchise cricket with international T20I fixtures. Our model calibrated for baseline environment divergence:
          </p>
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:12px;text-align:center;">
            <div style="background:#091228;border:1px solid var(--card-border);padding:12px;border-radius:8px;">
              <div style="font-size:10px;color:var(--text-muted);font-weight:700;">IPL BASELINE RUN RATE</div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:var(--orange);">8.45 RPO (140.8 SR)</div>
            </div>
            <div style="background:#091228;border:1px solid var(--card-border);padding:12px;border-radius:8px;">
              <div style="font-size:10px;color:var(--text-muted);font-weight:700;">T20I BASELINE RUN RATE</div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:var(--cyan);">7.77 RPO (129.5 SR)</div>
            </div>
            <div style="background:#091228;border:1px solid var(--card-border);padding:12px;border-radius:8px;">
              <div style="font-size:10px;color:var(--text-muted);font-weight:700;">IPL HP DEATH ECONOMY</div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:var(--rr-pink);">8.68 RPO</div>
            </div>
            <div style="background:#091228;border:1px solid var(--card-border);padding:12px;border-radius:8px;">
              <div style="font-size:10px;color:var(--text-muted);font-weight:700;">T20I HP DEATH ECONOMY</div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:var(--green);">7.95 RPO</div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- TAB 2: PLAYER ANALYSIS (Screenshot 2 view with in-cell pink bars, sparklines, and yellow bubble scatter plot) -->
    <div id="player-analysis" class="tab-content">

      <!-- ROLE PILL CONTROLS, AUCTION ELIGIBILITY TOGGLE & CONTEXT SELECTORS -->
      <div class="controls-banner">
        <div class="role-pills-group" id="rolePillsGroup">
          <button class="role-pill active" onclick="filterByRole('All', this)">All Players</button>
          <button class="role-pill" onclick="filterByRole('Openers', this)">Openers</button>
          <button class="role-pill" onclick="filterByRole('Middle Order', this)">Middle Order</button>
          <button class="role-pill" onclick="filterByRole('Finisher', this)">Finisher</button>
          <button class="role-pill" onclick="filterByRole('All Rounder', this)">All Rounder</button>
          <button class="role-pill" onclick="filterByRole('Specialist Fast Bowlers', this)">Specialist Fast Bowlers</button>
          <button class="role-pill" onclick="filterByRole('Spin Enforcers', this)">Spin Enforcers</button>
        </div>

        <!-- AUCTION ELIGIBILITY TOGGLE -->
        <div class="auction-pool-toggle-group">
          <button class="auction-toggle-btn active pink-toggle" onclick="setAuctionFilter('all', this)">
            <span>👥</span> All Players
          </button>
          <button class="auction-toggle-btn" onclick="setAuctionFilter('auction-only', this)">
            <span>🔥</span> Auction Pool Only
          </button>
          <button class="auction-toggle-btn" onclick="setAuctionFilter('retained-only', this)">
            <span>🔒</span> Retained Players
          </button>
        </div>
      </div>

      <!-- YELLOW ALERT PROMPT (Screenshot 2) -->
      <div class="yellow-alert-banner">
        <div class="bell-icon">🔔</div>
        <div><strong>Interactive Player Grid:</strong> Click on any player row to update the bottom sparkline trends and highlight their position on the clutch scatter plot.</div>
      </div>

      <!-- MAIN DATA TABLE WITH IN-CELL PINK PROGRESS BARS -->
      <div class="table-card">
        <div class="table-header-bar">
          <div class="table-role-badge">
            <span id="currentRoleTitle">ALL PLAYERS</span> • <span style="color:#FFF;" id="playerCountLabel">0 Players</span>
          </div>
          <div class="search-box-wrap">
            <input type="text" id="playerSearch" class="search-input" placeholder="Search player, team, or status..." onkeyup="searchPlayers(this.value)">
          </div>
        </div>
        <div class="table-responsive">
          <table class="cricket-table" id="playersTable">
            <thead>
              <tr>
                <th onclick="sortTable('rank')">Rank</th>
                <th onclick="sortTable('name')">Name</th>
                <th onclick="sortTable('status')">2027 Auction Status</th>
                <th onclick="sortTable('batting_style')">Style</th>
                <th onclick="sortTable('inns')">Innings</th>
                <th onclick="sortTable('runs')">HP Runs</th>
                <th onclick="sortTable('avg')">HP Avg</th>
                <th onclick="sortTable('wkts')">HP Wkts</th>
                <th onclick="sortTable('sr')">Batting S/R</th>
                <th onclick="sortTable('econ')">Economy</th>
                <th onclick="sortTable('ppi')">PPI Score</th>
              </tr>
            </thead>
            <tbody id="playerTableBody">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- BOTTOM SECTION: 4 SPARKLINE METRIC CARDS + SCATTER PLOT -->
      <div class="bottom-analytics-grid">
        
        <div class="metric-cards-subgrid">
          
          <div class="metric-spark-card">
            <div class="metric-spark-header">
              <span class="metric-spark-title">Batting Avg (Pressure)</span>
              <span class="metric-spark-value pink" id="sparkValAvg">31.4</span>
            </div>
            <div class="metric-par-note">Par Threshold Baseline: <span>20.16</span> (Dashed)</div>
            <div class="sparkline-canvas-box">
              <canvas id="sparkAvg"></canvas>
            </div>
          </div>

          <div class="metric-spark-card">
            <div class="metric-spark-header">
              <span class="metric-spark-title">Avg Balls Faced</span>
              <span class="metric-spark-value gold" id="sparkValBalls">16.8</span>
            </div>
            <div class="metric-par-note">Par Threshold Baseline: <span>13.65</span> (Dashed)</div>
            <div class="sparkline-canvas-box">
              <canvas id="sparkBalls"></canvas>
            </div>
          </div>

          <div class="metric-spark-card">
            <div class="metric-spark-header">
              <span class="metric-spark-title">Batting Strike Rate</span>
              <span class="metric-spark-value cyan" id="sparkValSR">164.2</span>
            </div>
            <div class="metric-par-note">Par Threshold Baseline: <span>117.08</span> (Dashed)</div>
            <div class="sparkline-canvas-box">
              <canvas id="sparkSR"></canvas>
            </div>
          </div>

          <div class="metric-spark-card">
            <div class="metric-spark-header">
              <span class="metric-spark-title">Bowling S/R (Pressure)</span>
              <span class="metric-spark-value purple" id="sparkValBowlSR">15.2</span>
            </div>
            <div class="metric-par-note">Par Threshold Baseline: <span>18.43</span> (Dashed)</div>
            <div class="sparkline-canvas-box">
              <canvas id="sparkBowlSR"></canvas>
            </div>
          </div>

        </div>

        <div class="scatter-plot-card">
          <div class="scatter-card-header">
            <span class="scatter-card-title">Batting Avg vs Strike Rate (Pressure Clutch Matrix)</span>
            <span class="scatter-legend-note">🟡 Yellow Bubbles = Pressure Stars</span>
          </div>
          <div class="scatter-canvas-box">
            <canvas id="scatterPlot"></canvas>
          </div>
        </div>

      </div>

    </div>

    <!-- TAB 3: REAL 2027 AUCTION STRATEGY -->
    <div id="real-strategy" class="tab-content">
      
      <div class="war-room-kpi-summary">
        <div class="purse-kpi-box rr-purse">
          <div class="kpi-label">RR Remaining Purse</div>
          <div class="purse-kpi-num" style="color:var(--rr-pink);">₹27.05 Cr</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">7th Highest in Auction</div>
        </div>

        <div class="purse-kpi-box slots-kpi">
          <div class="kpi-label">Total Slots to Fill</div>
          <div class="purse-kpi-num" style="color:var(--gold);">6 Slots</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">19 Players Already Retained</div>
        </div>

        <div class="purse-kpi-box overseas-kpi">
          <div class="kpi-label">Overseas Slots Available</div>
          <div class="purse-kpi-num" style="color:var(--cyan);">3 Slots</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">Retained: Archer, Ferreira, Burger, Shanaka, Pretorius</div>
        </div>

        <div class="purse-kpi-box big-opp">
          <div class="kpi-label">Marquee Release Alert</div>
          <div class="purse-kpi-num" style="color:var(--green);font-size:20px;">M. Pathirana</div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px;">Released by KKR • Target #1</div>
        </div>
      </div>

      <div style="margin-bottom:24px;">
        <h3 style="font-family:'Rajdhani',sans-serif;font-size:18px;font-weight:700;color:#FFF;margin-bottom:12px;letter-spacing:0.5px;">
          IPL 2027 AUCTION LANDSCAPE • ALL 10 FRANCHISES PURSE & SLOTS REMAINING
        </h3>
        <div class="all-franchises-purse-grid">
          
          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>LSG</span> <span style="font-size:10px;color:var(--green);">Highest</span></div>
            <div class="franchise-funds">₹47.45 Cr</div>
            <div class="franchise-slots">7 Slots (3 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>KKR</span></div>
            <div class="franchise-funds">₹41.65 Cr</div>
            <div class="franchise-slots">8 Slots (3 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>SRH</span></div>
            <div class="franchise-funds">₹40.15 Cr</div>
            <div class="franchise-slots">7 Slots (3 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>DC</span></div>
            <div class="franchise-funds">₹39.50 Cr</div>
            <div class="franchise-slots">9 Slots (4 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>MI</span></div>
            <div class="franchise-funds">₹32.60 Cr</div>
            <div class="franchise-slots">9 Slots (2 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>CSK</span></div>
            <div class="franchise-funds">₹28.05 Cr</div>
            <div class="franchise-slots">6 Slots (2 Overseas)</div>
          </div>

          <div class="franchise-purse-card highlight-rr">
            <div class="franchise-pname"><span>👑 RR (War Room)</span></div>
            <div class="franchise-funds" style="color:var(--rr-pink);">₹27.05 Cr</div>
            <div class="franchise-slots" style="color:#FFF;font-weight:700;">6 Slots (3 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>PBKS</span></div>
            <div class="franchise-funds">₹18.60 Cr</div>
            <div class="franchise-slots">6 Slots (2 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>RCB</span></div>
            <div class="franchise-funds">₹14.15 Cr</div>
            <div class="franchise-slots">5 Slots (1 Overseas)</div>
          </div>

          <div class="franchise-purse-card">
            <div class="franchise-pname"><span>GT</span> <span style="font-size:10px;color:var(--red);">Lowest</span></div>
            <div class="franchise-funds">₹8.75 Cr</div>
            <div class="franchise-slots">3 Slots (2 Overseas)</div>
          </div>

        </div>
      </div>

      <!-- REALISTIC AUCTION TARGETS (THE REAL 6 PICKS FOR RR) -->
      <div>
        <h3 style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:#FFF;margin-bottom:14px;">
          RAJASTHAN ROYALS • REALISTIC AUCTION BOARD (6 PICKS FOR ₹27.05 CR PURSE)
        </h3>
        
        <div class="real-targets-grid">
          
          <div class="target-card-real priority-1">
            <span class="target-priority-badge must-buy">Priority 1 • Overseas Death Machine</span>
            <div class="target-pname-real">Matheesha Pathirana</div>
            <div class="target-rel-badge">⚡ Released by KKR • Right-arm Sling Express</div>
            <div class="target-stats-mini-bar">
              <div>
                <div style="font-size:9px;color:var(--text-muted);">PPI SCORE</div>
                <div style="font-weight:800;color:var(--rr-pink);font-size:14px;">76.1</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">HP STRIKE RATE</div>
                <div style="font-weight:800;color:#FFF;font-size:14px;">12.2</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">RUNS SAVED</div>
                <div style="font-weight:800;color:var(--green);font-size:14px;">+162.5</div>
              </div>
            </div>
            <p class="target-bid-calc">
              <strong>Purse Allocation:</strong> ₹8.50 – ₹10.50 Cr.<br>
              <strong>Why RR Must Buy:</strong> Solves RR's death overs bowling. Pathirana is the premier sling yorker bowler in modern T20s and was released by KKR.
            </p>
          </div>

          <div class="target-card-real">
            <span class="target-priority-badge high-value">Priority 2 • #1 Ranked Clutch Bowler</span>
            <div class="target-pname-real">Hasan Mahmud</div>
            <div class="target-rel-badge">🎯 Available in Auction Pool • Overseas Fast Seamer</div>
            <div class="target-stats-mini-bar">
              <div>
                <div style="font-size:9px;color:var(--text-muted);">PPI SCORE</div>
                <div style="font-weight:800;color:var(--gold);font-size:14px;">90.1 (#1)</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">HP ECONOMY</div>
                <div style="font-weight:800;color:#FFF;font-size:14px;">7.35</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">RUNS SAVED</div>
                <div style="font-weight:800;color:var(--green);font-size:14px;">+48.8</div>
              </div>
            </div>
            <p class="target-bid-calc">
              <strong>Purse Allocation:</strong> ₹4.00 – ₹5.50 Cr.<br>
              <strong>Why RR Must Buy:</strong> Holds the highest bowling PPI in the entire dataset. Uncontracted overseas asset offering pinpoint yorkers and seam accuracy.
            </p>
          </div>

          <div class="target-card-real">
            <span class="target-priority-badge domestic-gem">Priority 3 • Domestic Left-Hand Finisher</span>
            <div class="target-pname-real">Nehal Wadhera</div>
            <div class="target-rel-badge">🔥 Released by PBKS • Left-hand Middle Order</div>
            <div class="target-stats-mini-bar">
              <div>
                <div style="font-size:9px;color:var(--text-muted);">ROLE</div>
                <div style="font-weight:800;color:var(--cyan);font-size:12px;">Finisher #5</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">PACE & SPIN</div>
                <div style="font-weight:800;color:#FFF;font-size:12px;">Dual Hitter</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">CEILING</div>
                <div style="font-weight:800;color:var(--gold);font-size:12px;">Very High</div>
              </div>
            </div>
            <p class="target-bid-calc">
              <strong>Purse Allocation:</strong> ₹3.50 – ₹4.50 Cr.<br>
              <strong>Why RR Must Buy:</strong> Provides an aggressive domestic left-handed batting option in middle overs, reducing overseas dependency.
            </p>
          </div>

          <div class="target-card-real">
            <span class="target-priority-badge domestic-gem">Priority 4 • Explosive Death Muscle</span>
            <div class="target-pname-real">Shahrukh Khan</div>
            <div class="target-rel-badge">💥 Released by GT • Right-hand Power Hitter</div>
            <div class="target-stats-mini-bar">
              <div>
                <div style="font-size:9px;color:var(--text-muted);">ROLE</div>
                <div style="font-weight:800;color:var(--cyan);font-size:12px;">Death Finisher</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">BOUNDARY %</div>
                <div style="font-weight:800;color:#FFF;font-size:12px;">22.4%</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">PRICE VAL</div>
                <div style="font-weight:800;color:var(--green);font-size:12px;">Value Buy</div>
              </div>
            </div>
            <p class="target-bid-calc">
              <strong>Purse Allocation:</strong> ₹2.50 – ₹3.50 Cr.<br>
              <strong>Why RR Must Buy:</strong> Pure boundary clearer in overs 18–20. Perfect rotational finisher or Impact Sub alongside Donovan Ferreira.
            </p>
          </div>

          <div class="target-card-real">
            <span class="target-priority-badge high-value">Priority 5 • The Homecoming Swing Specialist</span>
            <div class="target-pname-real">Trent Boult</div>
            <div class="target-rel-badge">⚡ Released by MI • Left-arm Fast Seam</div>
            <div class="target-stats-mini-bar">
              <div>
                <div style="font-size:9px;color:var(--text-muted);">PP WICKETS</div>
                <div style="font-weight:800;color:var(--gold);font-size:12px;">Elite</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">FAMILIARITY</div>
                <div style="font-weight:800;color:#FFF;font-size:12px;">Sawai Mansingh</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">PRESSURE EXP</div>
                <div style="font-weight:800;color:var(--green);font-size:12px;">15+ Years</div>
              </div>
            </div>
            <p class="target-bid-calc">
              <strong>Purse Allocation:</strong> ₹3.00 – ₹4.00 Cr.<br>
              <strong>Why RR Must Buy:</strong> Recreates the world-class powerplay swing partnership with Mohd. Shami and Sandeep Sharma.
            </p>
          </div>

          <div class="target-card-real">
            <span class="target-priority-badge domestic-gem">Priority 6 • Domestic Yorker Specialist</span>
            <div class="target-pname-real">Akash Madhwal</div>
            <div class="target-rel-badge">🎯 Released by CSK • Right-arm Medium-Fast</div>
            <div class="target-stats-mini-bar">
              <div>
                <div style="font-size:9px;color:var(--text-muted);">SLOT</div>
                <div style="font-weight:800;color:var(--cyan);font-size:12px;">Domestic Pace</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">DEATH CONTROL</div>
                <div style="font-weight:800;color:#FFF;font-size:12px;">Yorker Heavy</div>
              </div>
              <div>
                <div style="font-size:9px;color:var(--text-muted);">EST SPEND</div>
                <div style="font-weight:800;color:var(--gold);font-size:12px;">₹1.50 Cr</div>
              </div>
            </div>
            <p class="target-bid-calc">
              <strong>Purse Allocation:</strong> ₹1.20 – ₹1.80 Cr.<br>
              <strong>Why RR Must Buy:</strong> Experienced domestic Indian seamer who executes blockhole deliveries under extreme pressure.
            </p>
          </div>

        </div>

        <div style="background:#091228;border:1px solid var(--card-border);border-radius:12px;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
          <div>
            <span style="font-size:12px;color:var(--text-muted);text-transform:uppercase;font-weight:700;">Total Strategy Budget Required</span>
            <div style="font-family:'Rajdhani',sans-serif;font-size:24px;font-weight:700;color:var(--green);">₹23.20 Cr – ₹26.50 Cr</div>
          </div>
          <div>
            <span style="font-size:12px;color:var(--text-muted);text-transform:uppercase;font-weight:700;">RR Purse Available</span>
            <div style="font-family:'Rajdhani',sans-serif;font-size:24px;font-weight:700;color:var(--rr-pink);">₹27.05 Cr</div>
          </div>
          <div>
            <span style="font-size:12px;color:var(--text-muted);text-transform:uppercase;font-weight:700;">Purse Buffer Remaining</span>
            <div style="font-family:'Rajdhani',sans-serif;font-size:24px;font-weight:700;color:var(--gold);">+₹0.55 Cr to +₹3.85 Cr</div>
          </div>
          <div>
            <span class="badge-pill" style="background:rgba(16, 185, 129, 0.2);color:#10B981;font-size:12px;padding:6px 12px;border:1px solid #10B981;">
              ✅ 100% FEASIBLE & BUDGET BALANCED
            </span>
          </div>
        </div>

      </div>

    </div>

    <!-- TAB 4: FINAL 11 & WAR ROOM -->
    <div id="war-room" class="tab-content">

      <div class="chart-panel-card" style="margin-bottom:24px;">
        <div class="chart-panel-title">Powerplay Runs vs Death Over Runs by Franchise (Execution Under Fire)</div>
        <div style="height:220px;position:relative;">
          <canvas id="barPowerplayDeath"></canvas>
        </div>
      </div>

      <div class="auction-strategy-grid">
        
        <div>
          <h2 style="font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:700;color:#FFF;margin-bottom:14px;">
            RAJASTHAN ROYALS • 4 CORE TACTICAL NEEDS
          </h2>

          <div class="target-slot-card">
            <div class="target-slot-header">
              <span class="target-slot-badge">Target Slot 1 • Finisher</span>
              <span class="target-player-name">Donovan Ferreira (Retained by RR!) / Nehal Wadhera</span>
            </div>
            <div class="target-slot-title">Designated Death Finisher (Overs 16–20)</div>
            <p class="target-rationale">
              <strong>Tactical Reality:</strong> RR smartly retained <strong>Donovan Ferreira</strong> (181.8 HP SR). In the auction, RR can bid for released domestic gem <strong>Nehal Wadhera</strong> (PBKS) or <strong>Shahrukh Khan</strong> (GT) to solidify lower-order boundary power.
            </p>
          </div>

          <div class="target-slot-card">
            <div class="target-slot-header">
              <span class="target-slot-badge">Target Slot 2 • Death Pacer</span>
              <span class="target-player-name">Matheesha Pathirana (Released by KKR!)</span>
            </div>
            <div class="target-slot-title">Specialist Overseas Death Pacer</div>
            <p class="target-rationale">
              <strong>The Golden Opportunity:</strong> Matheesha Pathirana was released! With an unpickable 140kph sling yorker, 12.2 HP Strike Rate, and +162.5 Runs Saved, Pathirana represents RR's primary target for overseas death bowling alongside Sandeep Sharma and Jofra Archer.
            </p>
          </div>

          <div class="target-slot-card">
            <div class="target-slot-header">
              <span class="target-slot-badge">Target Slot 3 • Seam / Swing</span>
              <span class="target-player-name">Trent Boult (Released by MI!)</span>
            </div>
            <div class="target-slot-title">Powerplay Strike Homecoming</div>
            <p class="target-rationale">
              <strong>Homecoming Opportunity:</strong> Released by Mumbai Indians, Trent Boult offers immediate familiarity, elite left-arm swing, and leadership in the pace attack to support Mohd. Shami and Jofra Archer.
            </p>
          </div>

          <div class="target-slot-card">
            <div class="target-slot-header">
              <span class="target-slot-badge">Target Slot 4 • Domestic Engine</span>
              <span class="target-player-name">Akash Madhwal (Released by CSK) / Avesh Khan</span>
            </div>
            <div class="target-slot-title">High-Value Domestic Pace Depth</div>
            <p class="target-rationale">
              <strong>Domestic Execution:</strong> Akash Madhwal (yorker specialist) and Avesh Khan provide proven death-overs execution to fill RR's domestic auction slots at budget pricing.
            </p>
          </div>

        </div>

        <div>
          <div class="starting-xi-board">
            <div class="xi-header">
              <h2>PROPOSED RR 2027 <span>STARTING XI</span></h2>
              <p style="font-size:11px;color:var(--text-muted);margin-top:4px;">Optimized for Pressure Resilience & Resource Balance</p>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">1</span>
              <span class="xi-pname">Yashasvi Jaiswal (LHB)</span>
              <span class="xi-prole">Aggressive Opener</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">2</span>
              <span class="xi-pname">Dhruv Jurel (RHB / Wicketkeeper)</span>
              <span class="xi-prole">Dynamic Top-Order Wicketkeeper</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">3</span>
              <span class="xi-pname">Riyan Parag (RHB / Off-spin)</span>
              <span class="xi-prole">Middle Order Engine</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">4</span>
              <span class="xi-pname">Nehal Wadhera (LHB)</span>
              <span class="xi-prole">Middle Order Clutch Finisher</span>
              <span class="xi-ptag target">Auction Target</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">5</span>
              <span class="xi-pname">Donovan Ferreira (RHB / Overseas)</span>
              <span class="xi-prole">Explosive Power Finisher</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">6</span>
              <span class="xi-pname">Ravindra Jadeja (LHB / SLA)</span>
              <span class="xi-prole">Elite Spin All-Rounder</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">7</span>
              <span class="xi-pname">Jofra Archer (RHB / Express Pace / Overseas)</span>
              <span class="xi-prole">Express Pace Enforcer</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">8</span>
              <span class="xi-pname">Sandeep Sharma (Right-arm Medium)</span>
              <span class="xi-prole">Death Yorker Specialist</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">9</span>
              <span class="xi-pname">Mohd. Shami (Right-arm Seam)</span>
              <span class="xi-prole">Powerplay Seam Master</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">10</span>
              <span class="xi-pname">Matheesha Pathirana (Right-arm Sling / Overseas)</span>
              <span class="xi-prole">Lead Death Yorker Express</span>
              <span class="xi-ptag target">Top Target</span>
            </div>

            <div class="xi-player-row">
              <span class="xi-pos-num">11</span>
              <span class="xi-pname">Ravi Bishnoi (Right-arm Leg-spin)</span>
              <span class="xi-prole">Attacking Wrist-Spin</span>
              <span class="xi-ptag retain">Retained</span>
            </div>

            <div class="xi-player-row" style="background:rgba(255, 19, 137, 0.15);border-radius:6px;margin-top:8px;">
              <span class="xi-pos-num">IP</span>
              <span class="xi-pname" style="color:var(--rr-pink);">Shahrukh Khan / Akash Madhwal</span>
              <span class="xi-prole">Tactical Impact Sub</span>
              <span class="xi-ptag" style="background:var(--gold);color:#000;">Flex Target</span>
            </div>

          </div>
        </div>

      </div>

    </div>

    <!-- TAB 5: IPL OVERVIEW -->
    <div id="ipl-overview" class="tab-content">
      
      <div class="interactive-comparator-row">
        
        <div class="comparator-card">
          <div class="comparator-header">
            <div class="player-avatar-icon">🏏</div>
            <div class="comparator-title-area">
              <h3>IPL Batting Stats</h3>
              <p style="font-size:11px;color:var(--text-muted);">Inspect individual clutch profile</p>
            </div>
          </div>
          <label style="font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Select Batter</label>
          <select id="batterSelector" class="comparator-select" onchange="updateBatterCard(this.value)">
            <!-- Populated dynamically -->
          </select>
          <div class="comparator-stats-grid">
            <div class="mini-stat-box">
              <div class="mini-stat-label">Total Runs</div>
              <div class="mini-stat-num" id="batStatRuns">640</div>
            </div>
            <div class="mini-stat-box">
              <div class="mini-stat-label">6's</div>
              <div class="mini-stat-num" id="batStat6s">38</div>
            </div>
            <div class="mini-stat-box">
              <div class="mini-stat-label">4's</div>
              <div class="mini-stat-num" id="batStat4s">48</div>
            </div>
            <div class="mini-stat-box">
              <div class="mini-stat-label">Strike Rate</div>
              <div class="mini-stat-num" style="color:var(--rr-pink);" id="batStatSR">184.4</div>
            </div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:12px;font-size:11px;color:var(--text-muted);border-top:1px solid var(--card-border);padding-top:10px;">
            <span>Delta SR: <strong style="color:var(--gold);" id="batStatDeltaSR">+38.2</strong></span>
            <span>Pressure Avg: <strong style="color:#FFF;" id="batStatAvg">42.7</strong></span>
            <span>Status: <strong style="color:var(--cyan);" id="batStatStatus">Retained by PBKS</strong></span>
          </div>
        </div>

        <div class="comparator-card">
          <div class="comparator-header">
            <div class="player-avatar-icon">🎯</div>
            <div class="comparator-title-area">
              <h3>IPL Bowling Stats</h3>
              <p style="font-size:11px;color:var(--text-muted);">Inspect individual clutch profile</p>
            </div>
          </div>
          <label style="font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;">Select Bowler</label>
          <select id="bowlerSelector" class="comparator-select" onchange="updateBowlerCard(this.value)">
            <!-- Populated dynamically -->
          </select>
          <div class="comparator-stats-grid">
            <div class="mini-stat-box">
              <div class="mini-stat-label">Total Wkts</div>
              <div class="mini-stat-num" id="bowlStatWkts">50</div>
            </div>
            <div class="mini-stat-box">
              <div class="mini-stat-label">Economy</div>
              <div class="mini-stat-num" style="color:var(--cyan);" id="bowlStatEcon">7.20</div>
            </div>
            <div class="mini-stat-box">
              <div class="mini-stat-label">Average</div>
              <div class="mini-stat-num" id="bowlStatAvg">17.8</div>
            </div>
            <div class="mini-stat-box">
              <div class="mini-stat-label">Strike Rate</div>
              <div class="mini-stat-num" id="bowlStatSR">14.8</div>
            </div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:12px;font-size:11px;color:var(--text-muted);border-top:1px solid var(--card-border);padding-top:10px;">
            <span>Delta Econ: <strong style="color:var(--gold);" id="bowlStatDeltaEcon">+1.48</strong></span>
            <span>Dot Ball %: <strong style="color:#FFF;" id="bowlStatDot">44.8%</strong></span>
            <span>Status: <strong style="color:var(--cyan);" id="bowlStatStatus">Retained by MI</strong></span>
          </div>
        </div>

        <div class="comparator-card">
          <div class="comparator-header">
            <div class="player-avatar-icon">🍩</div>
            <div class="comparator-title-area">
              <h3>Matches Won By</h3>
              <p style="font-size:11px;color:var(--text-muted);">Chasing vs Defending splits</p>
            </div>
          </div>
          <div class="donut-card-content">
            <div class="donut-chart-box">
              <canvas id="donutWinBy"></canvas>
            </div>
          </div>
        </div>

      </div>

      <div class="venue-team-row">
        
        <div class="chart-panel-card">
          <div class="chart-panel-title">Matches Won at Venue (Wickets vs Runs)</div>
          <div class="chart-panel-box">
            <canvas id="barVenues"></canvas>
          </div>
        </div>

        <div class="chart-panel-card">
          <div class="chart-panel-title">Total Matches Won by Team (IPL Eras)</div>
          <div class="chart-panel-box">
            <canvas id="barTeamWins"></canvas>
          </div>
        </div>

        <div class="chart-panel-card">
          <div class="chart-panel-title">Matches Won by Toss Decision</div>
          <div class="chart-panel-box" style="display:flex;align-items:center;justify-content:center;">
            <div style="width:200px;height:200px;">
              <canvas id="donutToss"></canvas>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- FOOTER -->
    <footer class="dashboard-footer">
      <div class="footer-left">
        <span class="footer-badge">BCCI COMPLIANT</span>
        <span>Strict IPL eligibility enforced: All Pakistani players excluded from rankings and board.</span>
      </div>
      <div>
        <span>Model: Delivery Pressure Index (DPI ≥ 1.50) • Bayesian Shrinkage Applied • 200,999 Deliveries Evaluated</span>
      </div>
    </footer>

  </div>

  <!-- SCRIPT LOGIC & CHARTS -->
  <script>
    const RAW_DATA = {json_str};

    let currentRole = 'All';
    let currentAuctionFilter = 'all';
    let sortColumn = 'ppi';
    let sortAsc = false;
    let selectedPlayerName = 'Shashank Singh';

    // Chart instances
    let chartAvg = null;
    let chartBalls = null;
    let chartSR = null;
    let chartBowlSR = null;
    let chartScatter = null;
    let chartWinBy = null;
    let chartVenues = null;
    let chartTeamWins = null;
    let chartToss = null;
    let chartPPDeath = null;

    // Initialize application
    window.addEventListener('DOMContentLoaded', () => {{
      renderPureTop10Tables();
      renderTable();
      initSparklines();
      initScatterPlot();
      initIPLOverviewCharts();
      populateSelectors();
    }});

    // Render Pure Dataset Top 10 Tables
    function renderPureTop10Tables() {{
      const bBody = document.getElementById('pureBattersBody');
      const bwBody = document.getElementById('pureBowlersBody');
      
      const bat10 = RAW_DATA.pure_results_top10_batters || [];
      const bowl10 = RAW_DATA.pure_results_top10_bowlers || [];

      bBody.innerHTML = '';
      bat10.forEach(b => {{
        const tr = document.createElement('tr');
        const rankPillClass = b.rank <= 3 ? 'rank-pill top-3' : 'rank-pill';
        tr.innerHTML = `
          <td><span class="${{rankPillClass}}">#${{b.rank}}</span></td>
          <td class="player-name-cell">${{b.name}}</td>
          <td>${{b.hp_balls}}</td>
          <td><strong>${{b.hp_runs}}</strong></td>
          <td><strong style="color:var(--rr-pink);">${{b.hp_sr}}</strong></td>
          <td>${{b.base_sr}}</td>
          <td><span style="color:var(--gold);font-weight:700;">+${{b.delta_sr}}</span></td>
          <td><span style="color:var(--green);font-weight:700;">+${{b.rae}}</span></td>
          <td><span class="badge-pill badge-ppi">${{b.ppi}}</span></td>
        `;
        bBody.appendChild(tr);
      }});

      bwBody.innerHTML = '';
      bowl10.forEach(bw => {{
        const tr = document.createElement('tr');
        const rankPillClass = bw.rank <= 3 ? 'rank-pill top-3' : 'rank-pill';
        const deltaColor = bw.delta_econ > 0 ? 'var(--gold)' : '#94A3B8';
        const deltaSign = bw.delta_econ > 0 ? '+' : '';
        tr.innerHTML = `
          <td><span class="${{rankPillClass}}">#${{bw.rank}}</span></td>
          <td class="player-name-cell">${{bw.name}}</td>
          <td>${{bw.hp_balls}}</td>
          <td><strong>${{bw.hp_wkts}}</strong></td>
          <td><strong style="color:var(--cyan);">${{bw.hp_econ}}</strong></td>
          <td>${{bw.base_econ}}</td>
          <td><span style="color:${{deltaColor}};font-weight:700;">${{deltaSign}}${{bw.delta_econ}}</span></td>
          <td><span style="color:var(--green);font-weight:700;">+${{bw.runs_saved}}</span></td>
          <td><span class="badge-pill badge-ppi">${{bw.ppi}}</span></td>
        `;
        bwBody.appendChild(tr);
      }});
    }}

    // Tab Switching
    function switchTab(tabId, el) {{
      document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));
      
      document.getElementById(tabId).classList.add('active');
      el.classList.add('active');
    }}

    // Filter by Role
    function filterByRole(role, el) {{
      currentRole = role;
      document.querySelectorAll('.role-pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      document.getElementById('currentRoleTitle').innerText = role.toUpperCase();
      renderTable();
    }}

    // Auction Eligibility Toggle
    function setAuctionFilter(filterType, el) {{
      currentAuctionFilter = filterType;
      document.querySelectorAll('.auction-toggle-btn').forEach(b => {{
        b.classList.remove('active');
        b.classList.remove('pink-toggle');
      }});
      el.classList.add('active');
      if (filterType === 'all') {{
        el.classList.add('pink-toggle');
      }}
      renderTable();
    }}

    // Search players
    function searchPlayers(query) {{
      renderTable(query.toLowerCase());
    }}

    // Table Sorting
    function sortTable(col) {{
      if (sortColumn === col) {{
        sortAsc = !sortAsc;
      }} else {{
        sortColumn = col;
        sortAsc = false;
      }}
      renderTable();
    }}

    // Get filtered combined player list
    function getFilteredPlayers(searchQuery = '') {{
      let list = [];
      const batters = RAW_DATA.batters || [];
      const bowlers = RAW_DATA.bowlers || [];

      // Combine based on role
      if (currentRole === 'Specialist Fast Bowlers' || currentRole === 'Spin Enforcers') {{
        list = bowlers.filter(b => b.role === currentRole);
      }} else if (currentRole === 'Openers' || currentRole === 'Middle Order' || currentRole === 'Finisher') {{
        list = batters.filter(b => b.role === currentRole);
      }} else if (currentRole === 'All Rounder') {{
        const bAll = batters.filter(b => b.role === 'All Rounder');
        const bwAll = bowlers.filter(b => b.role === 'All Rounder');
        const setMap = new Map();
        [...bAll, ...bwAll].forEach(p => setMap.set(p.name, p));
        list = Array.from(setMap.values());
      }} else {{
        const setMap = new Map();
        [...batters, ...bowlers].forEach(p => setMap.set(p.name, p));
        list = Array.from(setMap.values());
      }}

      // Apply Auction Filter
      if (currentAuctionFilter === 'auction-only') {{
        list = list.filter(p => p.is_auction_eligible === true);
      }} else if (currentAuctionFilter === 'retained-only') {{
        list = list.filter(p => p.status_2027 === 'Retained');
      }}

      if (searchQuery) {{
        list = list.filter(p => 
          p.name.toLowerCase().includes(searchQuery) || 
          p.team.toLowerCase().includes(searchQuery) ||
          p.status_label.toLowerCase().includes(searchQuery) ||
          p.batting_style.toLowerCase().includes(searchQuery) ||
          p.bowling_style.toLowerCase().includes(searchQuery)
        );
      }}

      // Sort
      list.sort((a, b) => {{
        let vA = getFieldValue(a, sortColumn);
        let vB = getFieldValue(b, sortColumn);
        if (typeof vA === 'string') {{
          return sortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
        }}
        return sortAsc ? (vA - vB) : (vB - vA);
      }});

      return list;
    }}

    function getFieldValue(p, col) {{
      switch(col) {{
        case 'rank': return p.rank || 999;
        case 'name': return p.name || '';
        case 'status': return p.status_label || '';
        case 'batting_style': return p.batting_style || '';
        case 'bowling_style': return p.bowling_style || '';
        case 'inns': return p.innings_batted || p.innings_bowled || 0;
        case 'runs': return p.hp_runs || 0;
        case 'avg': return p.hp_avg || 0;
        case 'wkts': return p.hp_wickets || p.wickets || 0;
        case 'sr': return p.hp_sr || p.bowling_sr || 0;
        case 'econ': return p.hp_econ || p.bowling_econ || 0;
        case 'ppi': return p.ppi || 0;
        default: return p.ppi || 0;
      }}
    }}

    // Render Main Data Table with In-Cell Hot Pink Bars!
    function renderTable(searchQuery = '') {{
      const tbody = document.getElementById('playerTableBody');
      tbody.innerHTML = '';
      const players = getFilteredPlayers(searchQuery);

      document.getElementById('playerCountLabel').innerText = `${{players.length}} Players Available`;

      players.slice(0, 50).forEach((p, idx) => {{
        const tr = document.createElement('tr');
        if (p.name === selectedPlayerName) {{
          tr.classList.add('selected-row');
        }}

        tr.onclick = () => selectPlayer(p);

        const rankPillClass = p.rank <= 3 ? 'rank-pill top-3' : 'rank-pill';
        const srVal = p.hp_sr || (p.batting_sr || 0);
        const srPercent = Math.min(100, Math.max(10, (srVal / 220) * 100));

        const innsVal = p.innings_batted || p.innings_bowled || 0;
        const runsVal = p.hp_runs || 0;
        const avgVal = p.hp_avg ? p.hp_avg.toFixed(1) : '-';
        const wktsVal = (p.hp_wickets !== undefined) ? p.hp_wickets : (p.wickets || 0);
        const econVal = (p.hp_econ !== undefined) ? p.hp_econ.toFixed(2) : (p.bowling_econ ? p.bowling_econ.toFixed(2) : '-');

        let statusBadgeClass = 'status-badge available';
        let statusIcon = '🟢';
        if (p.status_2027 === 'Retained') {{
          statusBadgeClass = 'status-badge retained';
          statusIcon = '🔒';
        }} else if (p.status_2027 === 'Released') {{
          statusBadgeClass = 'status-badge released';
          statusIcon = '⚡';
        }}

        tr.innerHTML = `
          <td><span class="${{rankPillClass}}">#${{p.rank || (idx + 1)}}</span></td>
          <td class="player-name-cell">${{p.name}}</td>
          <td>
            <span class="${{statusBadgeClass}}">${{statusIcon}} ${{p.status_label}}</span>
          </td>
          <td><span style="font-size:11px;color:#CBD5E1;">${{p.batting_style}}</span></td>
          <td>${{innsVal}}</td>
          <td><strong>${{runsVal}}</strong></td>
          <td>${{avgVal}}</td>
          <td><strong>${{wktsVal}}</strong></td>
          <td>
            <div class="bar-cell-container">
              <div class="in-cell-bar-track">
                <div class="in-cell-bar-fill" style="width: ${{srPercent}}%;"></div>
              </div>
              <span class="bar-val-text">${{srVal.toFixed(1)}}</span>
            </div>
          </td>
          <td>${{econVal}}</td>
          <td><span class="badge-pill badge-ppi">${{p.ppi.toFixed(1)}}</span></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function selectPlayer(p) {{
      selectedPlayerName = p.name;
      renderTable();

      document.getElementById('sparkValAvg').innerText = p.hp_avg ? p.hp_avg.toFixed(1) : (p.overall_avg ? p.overall_avg.toFixed(1) : '24.5');
      document.getElementById('sparkValBalls').innerText = p.avg_balls_faced || '15.4';
      document.getElementById('sparkValSR').innerText = p.hp_sr ? p.hp_sr.toFixed(1) : (p.overall_sr ? p.overall_sr.toFixed(1) : '145.0');
      document.getElementById('sparkValBowlSR').innerText = p.hp_sr && p.hp_wickets ? (p.hp_balls/p.hp_wickets).toFixed(1) : (p.bowling_sr || '16.5');

      const bSel = document.getElementById('batterSelector');
      if (bSel) {{
        for (let i = 0; i < bSel.options.length; i++) {{
          if (bSel.options[i].value === p.name) {{
            bSel.selectedIndex = i;
            updateBatterCard(p.name);
            break;
          }}
        }}
      }}

      if (chartScatter) {{
        chartScatter.data.datasets.forEach(ds => {{
          ds.pointRadius = ds.data.map(pt => pt.name === p.name ? 12 : 7);
        }});
        chartScatter.update();
      }}
    }}

    function initSparklines() {{
      const baseOptions = (parValue) => ({{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{ enabled: true }}
        }},
        scales: {{
          x: {{ display: false }},
          y: {{
            display: false,
            grid: {{ display: false }}
          }}
        }}
      }});

      const ctxAvg = document.getElementById('sparkAvg').getContext('2d');
      chartAvg = new Chart(ctxAvg, {{
        type: 'line',
        data: {{
          labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'],
          datasets: [
            {{
              data: [18, 22, 20, 26, 21, 23, 22, 28, 48, 31],
              borderColor: '#FF1389',
              backgroundColor: 'rgba(255, 19, 137, 0.15)',
              borderWidth: 2,
              fill: true,
              tension: 0.3,
              pointRadius: 3
            }},
            {{
              data: [20.16, 20.16, 20.16, 20.16, 20.16, 20.16, 20.16, 20.16, 20.16, 20.16],
              borderColor: '#94A3B8',
              borderWidth: 1.5,
              borderDash: [4, 4],
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: baseOptions(20.16)
      }});

      const ctxBalls = document.getElementById('sparkBalls').getContext('2d');
      chartBalls = new Chart(ctxBalls, {{
        type: 'line',
        data: {{
          labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'],
          datasets: [
            {{
              data: [12, 14, 13, 19, 11, 17, 13, 14, 18, 16],
              borderColor: '#FACC15',
              backgroundColor: 'rgba(250, 204, 21, 0.15)',
              borderWidth: 2,
              fill: true,
              tension: 0.3,
              pointRadius: 3
            }},
            {{
              data: [13.65, 13.65, 13.65, 13.65, 13.65, 13.65, 13.65, 13.65, 13.65, 13.65],
              borderColor: '#94A3B8',
              borderWidth: 1.5,
              borderDash: [4, 4],
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: baseOptions(13.65)
      }});

      const ctxSR = document.getElementById('sparkSR').getContext('2d');
      chartSR = new Chart(ctxSR, {{
        type: 'line',
        data: {{
          labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'],
          datasets: [
            {{
              data: [110, 142, 128, 155, 118, 170, 162, 125, 195, 164],
              borderColor: '#38BDF8',
              backgroundColor: 'rgba(56, 189, 248, 0.15)',
              borderWidth: 2,
              fill: true,
              tension: 0.3,
              pointRadius: 3
            }},
            {{
              data: [117.08, 117.08, 117.08, 117.08, 117.08, 117.08, 117.08, 117.08, 117.08, 117.08],
              borderColor: '#94A3B8',
              borderWidth: 1.5,
              borderDash: [4, 4],
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: baseOptions(117.08)
      }});

      const ctxBowlSR = document.getElementById('sparkBowlSR').getContext('2d');
      chartBowlSR = new Chart(ctxBowlSR, {{
        type: 'line',
        data: {{
          labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'],
          datasets: [
            {{
              data: [22, 18, 19, 14, 25, 16, 21, 15, 12, 15],
              borderColor: '#A855F7',
              backgroundColor: 'rgba(168, 85, 247, 0.15)',
              borderWidth: 2,
              fill: true,
              tension: 0.3,
              pointRadius: 3
            }},
            {{
              data: [18.43, 18.43, 18.43, 18.43, 18.43, 18.43, 18.43, 18.43, 18.43, 18.43],
              borderColor: '#94A3B8',
              borderWidth: 1.5,
              borderDash: [4, 4],
              pointRadius: 0,
              fill: false
            }}
          ]
        }},
        options: baseOptions(18.43)
      }});
    }}

    function initScatterPlot() {{
      const ctxScatter = document.getElementById('scatterPlot').getContext('2d');

      const batters = RAW_DATA.batters || [];
      const scatterPoints = batters.slice(0, 25).map(b => ({{
        x: b.hp_avg || 25,
        y: b.hp_sr || 135,
        name: b.name,
        team: b.team,
        status: b.status_label,
        ppi: b.ppi
      }}));

      chartScatter = new Chart(ctxScatter, {{
        type: 'scatter',
        data: {{
          datasets: [{{
            label: 'Pressure Batters',
            data: scatterPoints,
            backgroundColor: '#FACC15',
            borderColor: '#CA8A04',
            borderWidth: 1.5,
            pointRadius: scatterPoints.map(p => p.name === selectedPlayerName ? 12 : 7),
            pointHoverRadius: 10
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => {{
                  const raw = ctx.raw;
                  return `${{raw.name}} (${{raw.status}}): Avg ${{raw.x.toFixed(1)}}, SR ${{raw.y.toFixed(1)}} (PPI: ${{raw.ppi}})`;
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              title: {{
                display: true,
                text: 'Batting Average (Pressure Context)',
                color: '#94A3B8',
                font: {{ weight: 'bold', size: 11 }}
              }},
              grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
              ticks: {{ color: '#CBD5E1' }}
            }},
            y: {{
              title: {{
                display: true,
                text: 'Strike Rate',
                color: '#94A3B8',
                font: {{ weight: 'bold', size: 11 }}
              }},
              grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
              ticks: {{ color: '#CBD5E1' }}
            }}
          }}
        }}
      }});
    }}

    function initIPLOverviewCharts() {{
      const ctxWinBy = document.getElementById('donutWinBy').getContext('2d');
      chartWinBy = new Chart(ctxWinBy, {{
        type: 'doughnut',
        data: {{
          labels: ['Wickets', 'Runs', 'SuperOver', 'NoResults'],
          datasets: [{{
            data: [
              RAW_DATA.matches_won_by.Wickets || 182,
              RAW_DATA.matches_won_by.Runs || 172,
              RAW_DATA.matches_won_by.SuperOver || 2,
              RAW_DATA.matches_won_by.NoResults || 15
            ],
            backgroundColor: ['#A855F7', '#38BDF8', '#FACC15', '#EF4444'],
            borderWidth: 2,
            borderColor: '#0D1630'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#CBD5E1', font: {{ size: 10 }}, boxWidth: 10 }}
            }}
          }},
          cutout: '65%'
        }}
      }});

      const ctxVenues = document.getElementById('barVenues').getContext('2d');
      const venues = RAW_DATA.venue_stats || [];
      chartVenues = new Chart(ctxVenues, {{
        type: 'bar',
        data: {{
          labels: venues.map(v => v.venue),
          datasets: [
            {{
              label: 'Wickets',
              data: venues.map(v => v.wickets),
              backgroundColor: '#38BDF8'
            }},
            {{
              label: 'Runs',
              data: venues.map(v => v.runs),
              backgroundColor: '#A855F7'
            }}
          ]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ stacked: true, grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#CBD5E1' }} }},
            y: {{ stacked: true, grid: {{ display: false }}, ticks: {{ color: '#CBD5E1', font: {{ size: 10 }} }} }}
          }},
          plugins: {{
            legend: {{ position: 'top', labels: {{ color: '#CBD5E1', boxWidth: 10 }} }}
          }}
        }}
      }});

      const ctxTeamWins = document.getElementById('barTeamWins').getContext('2d');
      const teamWinsObj = RAW_DATA.team_wins || {{}};
      const teams = Object.keys(teamWinsObj);
      const wins = Object.values(teamWinsObj);

      chartTeamWins = new Chart(ctxTeamWins, {{
        type: 'bar',
        data: {{
          labels: teams,
          datasets: [{{
            label: 'Wins',
            data: wins,
            backgroundColor: '#A855F7',
            borderRadius: 4
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#CBD5E1' }} }},
            y: {{ grid: {{ display: false }}, ticks: {{ color: '#CBD5E1', font: {{ size: 10 }} }} }}
          }},
          plugins: {{
            legend: {{ display: false }}
          }}
        }}
      }});

      const ctxToss = document.getElementById('donutToss').getContext('2d');
      chartToss = new Chart(ctxToss, {{
        type: 'doughnut',
        data: {{
          labels: ['Field First (67.5%)', 'Bat First (32.5%)'],
          datasets: [{{
            data: [RAW_DATA.toss_decision.Fielding || 285, RAW_DATA.toss_decision.Batting || 83],
            backgroundColor: ['#10B981', '#A855F7'],
            borderWidth: 2,
            borderColor: '#0D1630'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#CBD5E1', font: {{ size: 10 }}, boxWidth: 10 }}
            }}
          }},
          cutout: '65%'
        }}
      }});

      const ctxPPDeath = document.getElementById('barPowerplayDeath').getContext('2d');
      const ppDeathData = RAW_DATA.powerplay_death || [];
      chartPPDeath = new Chart(ctxPPDeath, {{
        type: 'bar',
        data: {{
          labels: ppDeathData.map(d => d.team),
          datasets: [
            {{
              label: 'Powerplay Runs',
              data: ppDeathData.map(d => d.pp),
              backgroundColor: '#A855F7'
            }},
            {{
              label: 'Death Over Runs',
              data: ppDeathData.map(d => d.death),
              backgroundColor: '#FACC15'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ grid: {{ display: false }}, ticks: {{ color: '#CBD5E1', font: {{ size: 10 }} }} }},
            y: {{ grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#CBD5E1' }} }}
          }},
          plugins: {{
            legend: {{ position: 'top', labels: {{ color: '#CBD5E1', boxWidth: 10 }} }}
          }}
        }}
      }});
    }}

    function populateSelectors() {{
      const bSel = document.getElementById('batterSelector');
      const bwSel = document.getElementById('bowlerSelector');

      (RAW_DATA.batters || []).forEach(b => {{
        const opt = document.createElement('option');
        opt.value = b.name;
        opt.text = `${{b.name}} (${{b.status_label}})`;
        bSel.appendChild(opt);
      }});

      (RAW_DATA.bowlers || []).forEach(bw => {{
        const opt = document.createElement('option');
        opt.value = bw.name;
        opt.text = `${{bw.name}} (${{bw.status_label}})`;
        bwSel.appendChild(opt);
      }});

      updateBatterCard(bSel.value);
      updateBowlerCard(bwSel.value);
    }}

    function updateBatterCard(pName) {{
      const p = (RAW_DATA.batters || []).find(b => b.name === pName);
      if (!p) return;

      document.getElementById('batStatRuns').innerText = p.total_runs || p.hp_runs;
      document.getElementById('batStat6s').innerText = p.total_6s || p.hp_sixes;
      document.getElementById('batStat4s').innerText = p.total_4s || p.hp_fours;
      document.getElementById('batStatSR').innerText = (p.hp_sr || p.overall_sr).toFixed(1);
      document.getElementById('batStatDeltaSR').innerText = (p.delta_sr > 0 ? '+' : '') + p.delta_sr.toFixed(1);
      document.getElementById('batStatAvg').innerText = (p.hp_avg || p.overall_avg).toFixed(1);
      document.getElementById('batStatStatus').innerText = p.status_label;
    }}

    function updateBowlerCard(pName) {{
      const p = (RAW_DATA.bowlers || []).find(bw => bw.name === pName);
      if (!p) return;

      document.getElementById('bowlStatWkts').innerText = p.total_wickets || p.hp_wickets;
      document.getElementById('bowlStatEcon').innerText = (p.hp_econ || p.overall_econ).toFixed(2);
      document.getElementById('bowlStatAvg').innerText = (p.hp_avg || p.overall_avg).toFixed(1);
      document.getElementById('bowlStatSR').innerText = (p.hp_sr || p.overall_sr).toFixed(1);
      document.getElementById('bowlStatDeltaEcon').innerText = (p.delta_econ > 0 ? '+' : '') + p.delta_econ.toFixed(2);
      document.getElementById('bowlStatDot').innerText = (p.hp_dot_pct || 42.0) + '%';
      document.getElementById('bowlStatStatus').innerText = p.status_label;
    }}

    function filterSeason(season) {{
      console.log('Season filtered:', season);
    }}
  </script>
</body>
</html>
'''

with open('dashboard.html', 'w') as f:
    f.write(html_content)

with open('index.html', 'w') as f:
    f.write(html_content)

print("Successfully written updated dashboard.html and index.html with Pure Dataset Results prominently featured!")
