import pandas as pd
import numpy as np
import json

print("Enriching dashboard data with official IPL 2027 Retentions & Releases...")

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

# Official IPL 2027 Retentions and Releases
retained_dict = {
    'Chennai Super Kings': ['Ruturaj Gaikwad', 'Sanju Samson', 'Ayush Mhatre', 'Urvil Patel', 'Dewald Brevis', 'Liam Livingstone', 'Jack Edwards', 'Akeal Hosein', 'Noor Ahmad', 'Kartik Sharma', 'Shivam Dube', 'Gurjapneet Singh', 'Anshul Kamboj', 'Sarfaraz Khan', 'Jamie Overton', 'Mukesh Choudhary', 'Rahul Chahar', 'Ramakrishna Ghosh', 'Shreyas Gopal'],
    'Lucknow Super Giants': ['Abdul Samad', 'Aiden Markram', 'Akash Singh', 'Akshat Raghuwanshi', 'Arjun Tendulkar', 'Arshin Kulkarni', 'Ayush Badoni', 'Digvesh Rathi', 'Josh Inglis', 'Kuldeep Yadav', 'Mayank Yadav', 'Mitchell Marsh', 'Mohsin Khan', 'Mukul Choudhary', 'Nicholas Pooran', 'Prince Yadav', 'Sam Curran', 'Shahbaz Ahmed'],
    'Royal Challengers Bengaluru': ['Rajat Patidar', 'Virat Kohli', 'Jitesh Sharma', 'Bhuvneshwar Kumar', 'Krunal Pandya', 'Josh Hazlewood', 'Phil Salt', 'Tim David', 'Romario Shepherd', 'Devdutt Padikkal', 'Nuwan Thushara', 'Venkatesh Iyer', 'Jacob Duffy', 'Jordan Cox', 'Rasikh Dar', 'Suyash Sharma', 'Vicky Ostwal', 'Abhinandan Singh', 'Kanishk Chouhan', 'Yash Dayal'],
    'Mumbai Indians': ['Rohit Sharma', 'Suryakumar Yadav', 'Jasprit Bumrah', 'Tilak Varma', 'Naman Dhir', 'Arshdeep Singh', 'Corbin Bosch', 'Mitchell Santner', 'Sherfane Rutherford', 'Will Jacks', 'Ryan Rickelton', 'Quinton de Kock', 'Shardul Thakur', 'Ashwani Kumar', 'Raj Angad Bawa', 'Raghu Sharma'],
    'Sunrisers Hyderabad': ['Pat Cummins', 'Abhishek Sharma', 'Ishan Kishan', 'Heinrich Klaasen', 'Nitish Kumar Reddy', 'Brydon Carse', 'Salil Arora', 'Aniket Verma', 'Harsh Dubey', 'Smaran Ravichandran', 'Praful Hinge', 'Sakib Hussain', 'Shivang Kumar', 'Krains Fuletra', 'Eshan Malinga', 'T Natarajan', 'Nathan Ellis', 'Khaleel Ahmed'],
    'Punjab Kings': ['Shreyas Iyer', 'Marcus Stoinis', 'Hardik Pandya', 'Marco Jansen', 'Shashank Singh', 'Prabhsimran Singh', 'Priyansh Arya', 'Yuzvendra Chahal', 'Azmatullah Omarzai', 'Vishnu Vinod', 'Xavier Bartlett', 'Vijaykumar Vyshak', 'Yash Thakur', 'Cooper Connolly', 'Musheer Khan', 'Ben Dwarshuis', 'Harpreet Brar', 'Suryansh Shedge', 'Harnoor Singh'],
    'Rajasthan Royals': ['Aman Rao Perala', 'Brijesh Sharma', 'Dasun Shanaka', 'Dhruv Jurel', 'Donovan Ferreira', 'Jofra Archer', 'Lhuan-dre Pretorius', 'Manimaran Siddharth', 'Mohd. Shami', 'Nandre Burger', 'Ravi Bishnoi', 'Ravindra Jadeja', 'Riyan Parag', 'Sandeep Sharma', 'Shubham Dubey', 'Sushant Mishra', 'Vaibhav Sooryavanshi', 'Yash Raj Punja', 'Yashasvi Jaiswal'],
    'Delhi Capitals': ['Ashutosh Sharma', 'Madhav Tiwari', 'Vipraj Nigam', 'Auqib Nabi', 'Mukesh Kumar', 'Zeeshan Ansari', 'Axar Patel', 'Prithvi Shaw', 'David Miller', 'Rishabh Pant', 'KL Rahul', 'Sameer Rizvi', 'Kyle Jamieson', 'Tripurana Vijay', 'Lungi Ngidi', 'Tristan Stubbs'],
    'Gujarat Titans': ['Anuj Rawat', 'Kagiso Rabada', 'Rahul Tewatia', 'Ashok Sharma', 'Kumar Kushagra', 'Rashid Khan', 'Glenn Phillips', 'Manav Suthar', 'Sai Sudharsan', 'Gurnoor Brar', 'Mohammed Siraj', 'Shubman Gill', 'Harshal Patel', 'Arshad Khan', 'Tom Banton', 'Jason Holder', 'Nishant Sindhu', 'Washington Sundar', 'Jayant Yadav', 'Prasidh Krishna', 'Jos Buttler', 'R Sai Kishore'],
    'Kolkata Knight Riders': ['Anukul Roy', 'Angkrish Raghuvanshi', 'Cameron Green', 'Finn Allen', 'Harshit Rana', 'Kartik Tyagi', 'Manish Pandey', 'Prashant Solanki', 'Ramandeep Singh', 'Rinku Singh', 'Rovman Powell', 'Sarthak Ranjan', 'Saurabh Dubey', 'Sunil Narine', 'Tim Seifert', 'Vaibhav Arora', 'Varun Chakaravarthy']
}

released_dict = {
    'Chennai Super Kings': ['MS Dhoni', 'Prashant Veer', 'Spencer Johnson', 'Akash Madhwal', 'Aman Khan', 'Dian Forrester', 'Kuldip Yadav', 'Macneil Noronha', 'Matt Henry', 'Matt Short', 'Zak Foulkes'],
    'Lucknow Super Giants': ['Avesh Khan', 'Matthew Breetzke', 'Wanindu Hasaranga', 'George Linde', 'Anrich Nortje', 'Naman Tiwari', 'Himmat Singh'],
    'Royal Challengers Bengaluru': ['Jacob Bethell', 'Richard Gleeson', 'Mangesh Yadav', 'Vihaan Malhotra', 'Satvik Deswal', 'Swapnil Singh'],
    'Mumbai Indians': ['Trent Boult', 'Deepak Chahar', 'AM Ghazanfar', 'Atharva Ankolekar', 'Keshav Maharaj', 'Mohammed Izhar', 'Danish Malewar', 'Mayank Markande', 'Mayank Rawat', 'Krish Bhagat', 'Mahipal Lomror', 'Robin Minz', 'Ruchit Ahir'],
    'Sunrisers Hyderabad': ['Travis Head', 'Jaydev Unadkat', 'Gerald Coetzee', 'Dilshan Madushanka', 'David Payne', 'Amit Kumar', 'Kamindu Mendis', 'Onkar Tarmale', 'RS Ambrish', 'Shivam Mavi'],
    'Punjab Kings': ['Nehal Wadhera', 'Lockie Ferguson', 'Lockie Ferugson', 'Pyla Avinash', 'Mitchell Owen', 'Praveen Dube', 'Vishal Nishad'],
    'Rajasthan Royals': ['Adam Milne', 'Emanjot Chahal', 'Kuldeep Sen', 'Kwena Maphaka', 'Ravi Singh', 'Shimron Hetmyer', 'Tushar Deshpande', 'Vignesh Puthur', 'Yudhvir Singh Charak'],
    'Delhi Capitals': ['Mitchell Starc', 'Nitish Rana', 'Abishek Porel', 'Pathum Nissanka', 'Karun Nair', 'Sahil Parakh', 'Ajay Mandal', 'Rehan Ahmed', 'Dushmantha Chameera'],
    'Gujarat Titans': ['Shahrukh Khan', 'Ishant Sharma', 'Luke Wood', 'Kulwant Khejroliya', 'Connor Esterhuizen', 'Prithviraj Yarra'],
    'Kolkata Knight Riders': ['Ajinkya Rahane', 'Akash Deep', 'Blessing Muzarabani', 'Daksh Kamra', 'Luvnith Sisodia', 'Matheesha Pathirana', 'Mustafizur Rahman', 'Navdeep Saini', 'Rachin Ravindra', 'Rahul Tripathi', 'Tejasvi Singh', 'Umran Malik']
}

purse_and_slots = [
    {"team": "Lucknow Super Giants", "purse_cr": 47.45, "slots": 7, "overseas": 3},
    {"team": "Kolkata Knight Riders", "purse_cr": 41.65, "slots": 8, "overseas": 3},
    {"team": "Sunrisers Hyderabad", "purse_cr": 40.15, "slots": 7, "overseas": 3},
    {"team": "Delhi Capitals", "purse_cr": 39.50, "slots": 9, "overseas": 4},
    {"team": "Mumbai Indians", "purse_cr": 32.60, "slots": 9, "overseas": 2},
    {"team": "Chennai Super Kings", "purse_cr": 28.05, "slots": 6, "overseas": 2},
    {"team": "Rajasthan Royals", "purse_cr": 27.05, "slots": 6, "overseas": 3},
    {"team": "Punjab Kings", "purse_cr": 18.60, "slots": 6, "overseas": 2},
    {"team": "Royal Challengers Bengaluru", "purse_cr": 14.15, "slots": 5, "overseas": 1},
    {"team": "Gujarat Titans", "purse_cr": 8.75, "slots": 3, "overseas": 2}
]

# Build lookup maps
ret_map = {}
for team, plist in retained_dict.items():
    for p in plist:
        ret_map[p.lower().strip()] = team

rel_map = {}
for team, plist in released_dict.items():
    for p in plist:
        rel_map[p.lower().strip()] = team

def get_2027_status(player_name):
    nl = player_name.lower().strip()
    for k, v in ret_map.items():
        if k == nl or (len(k) > 4 and k in nl) or (len(nl) > 4 and nl in k):
            return "Retained", v, f"Retained by {v}"
    for k, v in rel_map.items():
        if k == nl or (len(k) > 4 and k in nl) or (len(nl) > 4 and nl in k):
            return "Released", v, f"Released by {v}"
    return "Auction Pool", "Auction Pool", "Available in Auction"

# Build player styles
striker_styles = df_bbb.dropna(subset=['batting_type']).groupby('striker_name')['batting_type'].first().to_dict()
bowler_styles = df_bbb.dropna(subset=['bowling_type']).groupby('bowler_name')['bowling_type'].first().to_dict()

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

avg_bat_order = df_bbb.groupby('striker_name')['batting_order'].mean().to_dict()
balls_batted_total = df_bbb.groupby('striker_name').size().to_dict()
balls_bowled_total = df_bbb.groupby('bowler_name').size().to_dict()
pace_or_spin_dict = df_bbb.dropna(subset=['pace_or_spin']).groupby('bowler_name')['pace_or_spin'].first().to_dict()

player_teams = {}
for _, row in df_ctpm.iterrows():
    pname = row['player_name']
    tname = row['team_name']
    if pname not in player_teams:
        player_teams[pname] = tname
    elif tname in retained_dict:
        player_teams[pname] = tname

# Batters
batters_list = []
for idx, r in bat.iterrows():
    name = r['striker_name']
    order = avg_bat_order.get(name, 4.0)
    batted = balls_batted_total.get(name, 0)
    bowled = balls_bowled_total.get(name, 0)
    
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
    team = player_teams.get(name, "International")
    
    status_type, status_team, status_label = get_2027_status(name)
    is_available_in_auction = (status_type != "Retained")
    
    ov = bat_overall_dict.get(name, {})
    ov_runs = int(ov.get('total_runs', r['hp_runs'] + r['base_runs']))
    ov_balls = int(ov.get('total_balls', r['total_balls']))
    ov_4s = int(ov.get('total_4s', r['hp_fours']))
    ov_6s = int(ov.get('total_6s', r['hp_sixes']))
    ov_inns = int(ov.get('innings', r['hp_matches']))
    ov_sr = round((ov_runs / ov_balls * 100), 1) if ov_balls > 0 else 0.0
    ov_avg = round((ov_runs / max(1, r['hp_dismissals'] + r['base_dismissals'])), 1)
    avg_balls_faced = round(r['hp_balls'] / max(1, r['hp_dismissals']), 1)
    
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
        "ppi": round(r['ppi_scaled'], 1),
        "status_2027": status_type,
        "status_team": status_team,
        "status_label": status_label,
        "is_auction_eligible": is_available_in_auction
    })

# Bowlers
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
    team = player_teams.get(name, "International")
    
    status_type, status_team, status_label = get_2027_status(name)
    is_available_in_auction = (status_type != "Retained")
    
    bw_ov = bowl_overall_dict.get(name, {})
    ov_balls = int(bw_ov.get('total_balls', r['total_balls']))
    ov_runs = int(bw_ov.get('total_runs', r['hp_runs'] + r['base_runs']))
    ov_wkts = int(bw_ov.get('total_wickets', r['hp_wickets'] + r['base_wickets']))
    ov_inns = int(bw_ov.get('innings', r['hp_matches']))
    ov_dots = int(bw_ov.get('total_dots', r['hp_dots'] + r['base_dots']))
    ov_econ = round(ov_runs / (ov_balls / 6.0), 2) if ov_balls > 0 else 0.0
    ov_sr = round(ov_balls / ov_wkts, 1) if ov_wkts > 0 else 0.0
    ov_avg = round(ov_runs / ov_wkts, 1) if ov_wkts > 0 else 0.0
    
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
        "ppi": round(r['ppi_scaled'], 1),
        "status_2027": status_type,
        "status_team": status_team,
        "status_label": status_label,
        "is_auction_eligible": is_available_in_auction
    })

# Add other datasets from previous configuration
with open('dashboard_data.json') as f:
    prev = json.load(f)

dashboard_data = {
    "tournament_stats": prev['tournament_stats'],
    "matches_won_by": prev['matches_won_by'],
    "toss_decision": prev['toss_decision'],
    "venue_stats": prev['venue_stats'],
    "team_wins": prev['team_wins'],
    "powerplay_death": prev['powerplay_death'],
    "purse_and_slots": purse_and_slots,
    "retained_dict": retained_dict,
    "released_dict": released_dict,
    "rr_war_room_2027": {
        "purse_cr": 27.05,
        "slots_total": 6,
        "slots_overseas": 3,
        "retained_players": retained_dict['Rajasthan Royals'],
        "released_players": released_dict['Rajasthan Royals']
    },
    "batters": batters_list,
    "bowlers": bowlers_list
}

with open('dashboard_data.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print(f"Updated dashboard_data.json successfully with 2027 retentions & releases.")
