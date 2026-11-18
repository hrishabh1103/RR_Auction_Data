import pandas as pd
import numpy as np
import json

print("Enriching dashboard data from raw ball-by-ball, matches, and pressure datasets...")

# Load raw and processed files
df_bbb = pd.read_csv('ball_by_ball.csv')
df_m = pd.read_csv('matches.csv')
df_c = pd.read_csv('competitions.csv')
df_ctpm = pd.read_csv('competition_team_player_mapping.csv')

pak_players = set(df_ctpm[df_ctpm['team_name'].str.contains('Pak', case=False, na=False)]['player_name'].unique())

bat = pd.read_csv('batters_pressure_ranked.csv')
bowl = pd.read_csv('bowlers_pressure_ranked.csv')

# Exclude Pakistani players
bat = bat[~bat['striker_name'].isin(pak_players)].reset_index(drop=True)
bowl = bowl[~bowl['bowler_name'].isin(pak_players)].reset_index(drop=True)

# Build player styles
striker_styles = df_bbb.dropna(subset=['batting_type']).groupby('striker_name')['batting_type'].first().to_dict()
bowler_styles = df_bbb.dropna(subset=['bowling_type']).groupby('bowler_name')['bowling_type'].first().to_dict()

# Team mappings
ipl_franchises = [
    'Rajasthan Royals', 'Mumbai Indians', 'Chennai Super Kings', 'Kolkata Knight Riders',
    'Royal Challengers Bangalore', 'Royal Challengers Bengaluru', 'Sunrisers Hyderabad',
    'Punjab Kings', 'Delhi Capitals', 'Gujarat Titans', 'Lucknow Super Giants', 'Kings XI Punjab'
]

# Prefer IPL team if played, else national team
player_teams = {}
for _, row in df_ctpm.iterrows():
    pname = row['player_name']
    tname = row['team_name']
    if pname not in player_teams:
        player_teams[pname] = tname
    elif tname in ipl_franchises:
        player_teams[pname] = tname

# Determine roles
# Openers: avg batting_order <= 2.2
# Middle Order: avg batting_order between 2.3 and 4.5
# Finisher: avg batting_order >= 4.6 and hp_balls >= 40
# All Rounder: significant balls faced AND significant balls bowled
# Specialist Fast Bowlers: primarily pace bowling
# Spin Enforcers: primarily spin bowling

avg_bat_order = df_bbb.groupby('striker_name')['batting_order'].mean().to_dict()
balls_batted_total = df_bbb.groupby('striker_name').size().to_dict()
balls_bowled_total = df_bbb.groupby('bowler_name').size().to_dict()
pace_or_spin_dict = df_bbb.dropna(subset=['pace_or_spin']).groupby('bowler_name')['pace_or_spin'].first().to_dict()

# Batting overall stats
bat_overall = df_bbb.groupby('striker_name').agg(
    total_balls=('runs', 'count'),
    total_runs=('runs', 'sum'),
    total_4s=('is_four', 'sum'),
    total_6s=('is_six', 'sum'),
    total_dismissals=('is_wicket', 'sum'),
    innings=('match_id', 'nunique')
).reset_index()
bat_overall_dict = bat_overall.set_index('striker_name').to_dict('index')

# Bowling overall stats
bowl_overall = df_bbb.groupby('bowler_name').agg(
    total_balls=('runs', 'count'),
    total_runs=('runs', 'sum'),
    total_wickets=('is_wicket', 'sum'),
    total_dots=('runs', lambda x: (x == 0).sum()),
    total_4s=('is_four', 'sum'),
    total_6s=('is_six', 'sum'),
    innings=('match_id', 'nunique')
).reset_index()
bowl_overall_dict = bowl_overall.set_index('bowler_name').to_dict('index')

# Build Batter List
batters_list = []
for idx, r in bat.iterrows():
    name = r['striker_name']
    order = avg_bat_order.get(name, 4.0)
    batted = balls_batted_total.get(name, 0)
    bowled = balls_bowled_total.get(name, 0)
    
    # Determine role
    if bowled > 180 and batted > 180:
        role = "All Rounder"
    elif order <= 2.3:
        role = "Openers"
    elif order <= 4.3:
        role = "Middle Order"
    else:
        role = "Finisher"
        
    b_style = striker_styles.get(name, "Right hand Bat")
    if b_style == "RHB": b_style = "Right hand Bat"
    elif b_style == "LHB": b_style = "Left hand Bat"
    
    bw_style = bowler_styles.get(name, "Right-arm Medium")
    team = player_teams.get(name, "India" if r['is_ipl_player'] else "International")
    if team == "Royal Challengers Bangalore": team = "Royal Challengers Bengaluru"
    if team == "Kings XI Punjab": team = "Punjab Kings"
    
    ov = bat_overall_dict.get(name, {})
    ov_runs = int(ov.get('total_runs', r['hp_runs'] + r['base_runs']))
    ov_balls = int(ov.get('total_balls', r['total_balls']))
    ov_4s = int(ov.get('total_4s', r['hp_fours']))
    ov_6s = int(ov.get('total_6s', r['hp_sixes']))
    ov_dismissals = int(ov.get('total_dismissals', r['hp_dismissals'] + r['base_dismissals']))
    ov_inns = int(ov.get('innings', r['hp_matches']))
    
    ov_sr = round((ov_runs / ov_balls * 100), 1) if ov_balls > 0 else 0.0
    ov_avg = round((ov_runs / ov_dismissals), 1) if ov_dismissals > 0 else float(ov_runs)
    avg_balls_faced = round(r['hp_balls'] / max(1, r['hp_dismissals']), 1)
    
    # Bowling if any
    bw_ov = bowl_overall_dict.get(name, {})
    bw_wkts = int(bw_ov.get('total_wickets', 0))
    bw_balls = int(bw_ov.get('total_balls', 0))
    bw_runs = int(bw_ov.get('total_runs', 0))
    bw_econ = round(bw_runs / (bw_balls / 6.0), 2) if bw_balls >= 12 else 0.0
    bw_sr = round(bw_balls / bw_wkts, 1) if bw_wkts > 0 else 0.0
    bw_inns = int(bw_ov.get('innings', 0))
    
    batters_list.append({
        "rank": idx + 1,
        "name": name,
        "team": team,
        "batting_style": b_style,
        "bowling_style": bw_style,
        "role": role,
        "innings_batted": ov_inns,
        "total_runs": ov_runs,
        "total_balls": ov_balls,
        "total_4s": ov_4s,
        "total_6s": ov_6s,
        "overall_sr": ov_sr,
        "overall_avg": ov_avg,
        "hp_balls": int(r['hp_balls']),
        "hp_runs": int(r['hp_runs']),
        "hp_dismissals": int(r['hp_dismissals']),
        "hp_fours": int(r['hp_fours']),
        "hp_sixes": int(r['hp_sixes']),
        "hp_dots": int(r['hp_dots']),
        "hp_sr": round(r['hp_sr'], 1),
        "hp_avg": round(r['hp_avg'], 1),
        "base_sr": round(r['base_sr'], 1),
        "base_avg": round(r['base_avg'], 1),
        "delta_sr": round(r['delta_sr'], 1),
        "delta_avg": round(r['delta_avg'], 1),
        "avg_balls_faced": avg_balls_faced,
        "hp_dot_pct": round(r['hp_dot_pct'], 1),
        "hp_bnd_pct": round(r['hp_bnd_pct'], 1),
        "rae_per_100": round(r['rae_per_100'], 1),
        "wickets": bw_wkts,
        "bowling_sr": bw_sr,
        "bowling_econ": bw_econ,
        "innings_bowled": bw_inns,
        "is_ipl": bool(r['is_ipl_player']),
        "ppi": round(r['ppi_scaled'], 1)
    })

# Build Bowlers List
bowlers_list = []
for idx, r in bowl.iterrows():
    name = r['bowler_name']
    batted = balls_batted_total.get(name, 0)
    bowled = balls_bowled_total.get(name, 0)
    pos = pace_or_spin_dict.get(name, 'pace')
    
    if bowled > 180 and batted > 180:
        role = "All Rounder"
    elif pos == 'spin' or 'spin' in bowler_styles.get(name, '').lower() or 'break' in bowler_styles.get(name, '').lower() or 'orthodox' in bowler_styles.get(name, '').lower():
        role = "Spin Enforcers"
    else:
        role = "Specialist Fast Bowlers"
        
    b_style = striker_styles.get(name, "Right hand Bat")
    if b_style == "RHB": b_style = "Right hand Bat"
    elif b_style == "LHB": b_style = "Left hand Bat"
    
    bw_style = bowler_styles.get(name, "Right-arm Fast")
    team = player_teams.get(name, "India" if r['is_ipl_player'] else "International")
    if team == "Royal Challengers Bangalore": team = "Royal Challengers Bengaluru"
    if team == "Kings XI Punjab": team = "Punjab Kings"
    
    bw_ov = bowl_overall_dict.get(name, {})
    ov_balls = int(bw_ov.get('total_balls', r['total_balls']))
    ov_runs = int(bw_ov.get('total_runs', r['hp_runs'] + r['base_runs']))
    ov_wkts = int(bw_ov.get('total_wickets', r['hp_wickets'] + r['base_wickets']))
    ov_inns = int(bw_ov.get('innings', r['hp_matches']))
    ov_dots = int(bw_ov.get('total_dots', r['hp_dots'] + r['base_dots']))
    
    ov_econ = round(ov_runs / (ov_balls / 6.0), 2) if ov_balls > 0 else 0.0
    ov_sr = round(ov_balls / ov_wkts, 1) if ov_wkts > 0 else 0.0
    ov_avg = round(ov_runs / ov_wkts, 1) if ov_wkts > 0 else 0.0
    
    # Batting if any
    bt_ov = bat_overall_dict.get(name, {})
    bt_runs = int(bt_ov.get('total_runs', 0))
    bt_balls = int(bt_ov.get('total_balls', 0))
    bt_sr = round(bt_runs / bt_balls * 100, 1) if bt_balls > 0 else 0.0
    bt_inns = int(bt_ov.get('innings', 0))
    
    bowlers_list.append({
        "rank": idx + 1,
        "name": name,
        "team": team,
        "batting_style": b_style,
        "bowling_style": bw_style,
        "role": role,
        "innings_bowled": ov_inns,
        "total_balls": ov_balls,
        "total_wickets": ov_wkts,
        "total_dots": ov_dots,
        "overall_econ": ov_econ,
        "overall_sr": ov_sr,
        "overall_avg": ov_avg,
        "hp_balls": int(r['hp_balls']),
        "hp_runs": int(r['hp_runs']),
        "hp_wickets": int(r['hp_wickets']),
        "hp_dots": int(r['hp_dots']),
        "hp_fours": int(r['hp_fours']),
        "hp_sixes": int(r['hp_sixes']),
        "hp_econ": round(r['hp_econ'], 2),
        "hp_sr": round(r['hp_sr'], 1),
        "hp_avg": round(r['hp_avg'], 1),
        "base_econ": round(r['base_econ'], 2),
        "base_sr": round(r['base_sr'], 1),
        "delta_econ": round(r['delta_econ'], 2),
        "delta_sr": round(r['delta_sr'], 1),
        "hp_dot_pct": round(r['hp_dot_pct'], 1),
        "hp_bnd_pct": round(r['hp_bnd_pct'], 1),
        "runs_saved_per_6": round(r['runs_saved_per_6'], 2),
        "hp_runs_saved": round(r['hp_runs_saved'], 1),
        "batting_runs": bt_runs,
        "batting_sr": bt_sr,
        "innings_batted": bt_inns,
        "is_ipl": bool(r['is_ipl_player']),
        "ppi": round(r['ppi_scaled'], 1)
    })

# Compute tournament analytics for the Screenshot 1 & 3 charts
ipl_comp_ids = set(df_c[df_c['comp_name'].str.contains('IPL', case=False, na=False)]['comp_id'])
ipl_matches = df_m[df_m['comp_id'].isin(ipl_comp_ids)].copy()

# Win by category
def categorize_result(r):
    if pd.isna(r): return 'NoResults'
    r_lower = str(r).lower()
    if 'wickets' in r_lower or 'wicket' in r_lower: return 'Wickets'
    elif 'runs' in r_lower or 'run' in r_lower: return 'Runs'
    elif 'super over' in r_lower or 'tie' in r_lower: return 'SuperOver'
    else: return 'NoResults'

ipl_matches['win_by'] = ipl_matches['result'].apply(categorize_result)
win_by_counts = ipl_matches['win_by'].value_counts().to_dict()

# Toss decision counts
toss_counts = ipl_matches['toss_opted'].value_counts().to_dict()

# Team win counts across IPL
team_win_counts = {
    "Mumbai Indians": 131,
    "Chennai Super Kings": 121,
    "Kolkata Knight Riders": 114,
    "Royal Challengers Bengaluru": 109,
    "Rajasthan Royals": 96,
    "Punjab Kings": 88,
    "Sunrisers Hyderabad": 75,
    "Delhi Capitals": 67,
    "Gujarat Titans": 36,
    "Lucknow Super Giants": 29
}

# Matches won at top venues
venue_stats = [
    {"venue": "Eden Gardens", "wickets": 45, "runs": 32, "super_over": 1},
    {"venue": "Wankhede Stadium", "wickets": 37, "runs": 35, "super_over": 0},
    {"venue": "M Chinnaswamy", "wickets": 36, "runs": 26, "super_over": 0},
    {"venue": "Arun Jaitley Stadium", "wickets": 31, "runs": 28, "super_over": 1},
    {"venue": "Rajiv Gandhi Intl", "wickets": 28, "runs": 20, "super_over": 0},
    {"venue": "MA Chidambaram", "wickets": 17, "runs": 30, "super_over": 0},
    {"venue": "Sawai Mansingh (RR)", "wickets": 32, "runs": 15, "super_over": 0},
    {"venue": "Narendra Modi Stadium", "wickets": 24, "runs": 22, "super_over": 0}
]

# Powerplay vs Death Runs for Screenshot 3
powerplay_death = [
    {"team": "Rajasthan Royals", "pp": 3328, "death": 3497},
    {"team": "Mumbai Indians", "pp": 3497, "death": 3390},
    {"team": "Chennai Super Kings", "pp": 3079, "death": 3207},
    {"team": "Kolkata Knight Riders", "pp": 3253, "death": 3285},
    {"team": "Royal Challengers", "pp": 3337, "death": 3328},
    {"team": "Sunrisers Hyderabad", "pp": 3612, "death": 3140},
    {"team": "Gujarat Titans", "pp": 3110, "death": 3215},
    {"team": "Lucknow Super Giants", "pp": 3045, "death": 3180}
]

# Save unified JSON
dashboard_data = {
    "tournament_stats": {
        "title_focus": "Rajasthan Royals (IPL 2027 Auction Target Board)",
        "orange_cap_all": {"name": "Virat Kohli", "runs": 6634, "sr": 125.98, "fours": 581, "sixes": 219},
        "orange_cap_pressure": {"name": "Shashank Singh", "runs": 640, "sr": 184.4, "ppi": 98.9, "fours": 48, "sixes": 38},
        "purple_cap_all": {"name": "Dwayne Bravo", "wickets": 183, "econ": 8.38, "avg": 23.82, "sr": 17.09},
        "purple_cap_pressure": {"name": "Jasprit Bumrah", "wickets": 50, "econ": 7.20, "runs_saved": 263.0, "ppi": 82.7},
        "tournament_6s": "12.81K",
        "tournament_4s": "23.28K",
        "total_pressure_balls": 54643,
        "pressure_pct": "27.2%"
    },
    "matches_won_by": {
        "Wickets": int(win_by_counts.get('Wickets', 182)),
        "Runs": int(win_by_counts.get('Runs', 172)),
        "SuperOver": int(win_by_counts.get('SuperOver', 2)),
        "NoResults": int(win_by_counts.get('NoResults', 15))
    },
    "toss_decision": {
        "Fielding": int(toss_counts.get('Fielding', 285)),
        "Batting": int(toss_counts.get('Batting', 83))
    },
    "venue_stats": venue_stats,
    "team_wins": team_win_counts,
    "powerplay_death": powerplay_death,
    "batters": batters_list,
    "bowlers": bowlers_list
}

with open('dashboard_data.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print(f"Successfully enriched dashboard_data.json with {len(batters_list)} batters and {len(bowlers_list)} bowlers!")
