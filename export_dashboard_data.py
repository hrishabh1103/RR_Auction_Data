import pandas as pd
import json

df_m = pd.read_csv('competition_team_player_mapping.csv')
pak_players = set(df_m[df_m['team_name'].str.contains('Pak', case=False, na=False)]['player_name'].unique())

bat = pd.read_csv('batters_pressure_ranked.csv')
bowl = pd.read_csv('bowlers_pressure_ranked.csv')

# Filter out Pakistani players
bat = bat[~bat['striker_name'].isin(pak_players)].reset_index(drop=True)
bowl = bowl[~bowl['bowler_name'].isin(pak_players)].reset_index(drop=True)

bat.to_csv('batters_pressure_ranked_ipl_eligible.csv', index=False)
bowl.to_csv('bowlers_pressure_ranked_ipl_eligible.csv', index=False)

bat_data = []
for idx, r in bat.head(30).iterrows():
    bat_data.append({
        "rank": idx + 1,
        "name": r['striker_name'],
        "hp_balls": int(r['hp_balls']),
        "hp_runs": int(r['hp_runs']),
        "hp_sr": round(r['hp_sr'], 1),
        "base_sr": round(r['base_sr'], 1),
        "delta_sr": round(r['delta_sr'], 1),
        "hp_avg": round(r['hp_avg'], 1),
        "base_avg": round(r['base_avg'], 1),
        "delta_avg": round(r['delta_avg'], 1),
        "hp_bnd_pct": round(r['hp_bnd_pct'], 1),
        "hp_dot_pct": round(r['hp_dot_pct'], 1),
        "rae_per_100": round(r['rae_per_100'], 1),
        "is_ipl": bool(r['is_ipl_player']),
        "ppi": round(r['ppi_scaled'], 1)
    })

bowl_data = []
for idx, r in bowl.head(30).iterrows():
    bowl_data.append({
        "rank": idx + 1,
        "name": r['bowler_name'],
        "hp_balls": int(r['hp_balls']),
        "hp_wickets": int(r['hp_wickets']),
        "hp_econ": round(r['hp_econ'], 2),
        "base_econ": round(r['base_econ'], 2),
        "delta_econ": round(r['delta_econ'], 2),
        "hp_sr": round(r['hp_sr'], 1),
        "hp_dot_pct": round(r['hp_dot_pct'], 1),
        "hp_bnd_pct": round(r['hp_bnd_pct'], 1),
        "runs_saved_per_6": round(r['runs_saved_per_6'], 2),
        "is_ipl": bool(r['is_ipl_player']),
        "ppi": round(r['ppi_scaled'], 1)
    })

with open('dashboard_data.json', 'w') as f:
    json.dump({'batters': bat_data, 'bowlers': bowl_data}, f, indent=2)

print("Updated dashboard_data.json with Pakistani players excluded.")
