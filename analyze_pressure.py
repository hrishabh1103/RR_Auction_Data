import pandas as pd
import numpy as np
import json
import os

print("--- Starting RR Pressure Analytics Engine ---")

# 1. Load Data
df_bbb = pd.read_csv('ball_by_ball.csv')
df_m = pd.read_csv('matches.csv')
df_c = pd.read_csv('competitions.csv')
df_map = pd.read_csv('competition_team_player_mapping.csv')

df_m = df_m.merge(df_c[['comp_id', 'match_format', 'season', 'comp_name']], on='comp_id', how='left')

# Ball level base columns
df_bbb['total_ball_runs'] = df_bbb['runs'] + df_bbb['extras1_runs'] + df_bbb['extras_2_runs']
df_bbb['is_legal'] = ~df_bbb['extras_type'].isin(['wide', 'Overstep'])
df_bbb['bowler_runs'] = df_bbb['runs'] + np.where(df_bbb['extras_type'].isin(['wide', 'Overstep']), df_bbb['extras1_runs'] + df_bbb['extras_2_runs'], 0)
df_bbb['is_bowler_wicket'] = df_bbb['is_wicket'] & df_bbb['dismissal_type'].isin(['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'])

# Match targets
inn1_runs = df_bbb[df_bbb['innings'] == 1].groupby('match_id')['total_ball_runs'].sum().rename('inn1_runs')
df_m = df_m.merge(inn1_runs, on='match_id', how='left')
df_m['target'] = np.where(df_m['revised_target'].notna(), df_m['revised_target'], df_m['inn1_runs'] + 1)

df_bbb = df_bbb.merge(df_m[['match_id', 'target', 'first_inn_revised_overs', 'second_inn_revised_overs', 'knock_out', 'stage', 'match_format', 'season', 'comp_name']], on='match_id', how='left')

# Cumulative tracking
df_bbb['cum_legal_balls'] = df_bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - df_bbb['is_legal']
df_bbb['cum_runs'] = df_bbb.groupby(['match_id', 'innings'])['total_ball_runs'].cumsum() - df_bbb['total_ball_runs']
df_bbb['cum_wickets'] = df_bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - df_bbb['is_wicket']

df_bbb['total_balls'] = np.where(
    df_bbb['innings'] == 1,
    np.where(df_bbb['first_inn_revised_overs'].notna(), df_bbb['first_inn_revised_overs'], 120),
    np.where(df_bbb['second_inn_revised_overs'].notna(), df_bbb['second_inn_revised_overs'], 120)
)
df_bbb['balls_remaining'] = np.maximum(0, df_bbb['total_balls'] - df_bbb['cum_legal_balls'])
df_bbb['wickets_in_hand'] = 10 - df_bbb['cum_wickets']
df_bbb['runs_needed'] = np.where(df_bbb['innings'] == 2, np.maximum(0, df_bbb['target'] - df_bbb['cum_runs']), np.nan)
df_bbb['rrr'] = np.where(
    (df_bbb['innings'] == 2) & (df_bbb['balls_remaining'] > 0),
    (df_bbb['runs_needed'] / df_bbb['balls_remaining']) * 6.0,
    np.nan
)

# Pressure Index Computation
ko_mult = np.where(df_bbb['knock_out'] == 1, 1.25, 1.0)
rrr_norm = np.clip(df_bbb['rrr'] / 8.5, 0.2, 3.0)
wkt_factor = 1.0 + np.clip((10 - df_bbb['wickets_in_hand']) / 10.0, 0, 1.0) * 0.6
death_factor = 1.0 + np.where(df_bbb['balls_remaining'] <= 36, (36 - df_bbb['balls_remaining']) / 36.0 * 0.5, 0.0)
inn2_pressure = rrr_norm * wkt_factor * death_factor * ko_mult

death_p1 = np.where(df_bbb['overid'] >= 16, 1.4 + (df_bbb['overid'] - 16) * 0.15, 0.8)
collapse_p1 = np.where(
    (df_bbb['overid'] <= 6) & (df_bbb['cum_wickets'] >= 3), 1.5,
    np.where((df_bbb['overid'] <= 10) & (df_bbb['cum_wickets'] >= 4), 1.4, 1.0)
)
inn1_pressure = death_p1 * collapse_p1 * ko_mult

df_bbb['pressure_score'] = np.where(
    df_bbb['innings'] >= 3, 3.5,
    np.where(df_bbb['innings'] == 2, inn2_pressure, inn1_pressure)
)
df_bbb['is_high_pressure'] = df_bbb['pressure_score'] >= 1.50
df_bbb['is_ipl'] = df_bbb['comp_name'].str.contains('IPL', case=False, na=False)
df_bbb['phase'] = np.where(df_bbb['overid'] <= 6, 'Powerplay', np.where(df_bbb['overid'] <= 15, 'Middle', 'Death'))

# Context Baselines
context_means = df_bbb.groupby(['is_ipl', 'phase', 'is_high_pressure'])[['runs', 'bowler_runs', 'is_bowler_wicket']].transform('mean')
df_bbb['exp_runs'] = context_means['runs']
df_bbb['exp_bowler_runs'] = context_means['bowler_runs']
df_bbb['exp_wkt'] = context_means['is_bowler_wicket']

df_bbb['runs_above_exp'] = df_bbb['runs'] - df_bbb['exp_runs']
df_bbb['runs_saved'] = df_bbb['exp_bowler_runs'] - df_bbb['bowler_runs']
df_bbb['wkts_above_exp'] = df_bbb['is_bowler_wicket'].astype(float) - df_bbb['exp_wkt']

# Recency & League Weighting
season_year = df_bbb['season'].astype(str).str[:4].astype(int)
df_bbb['weight'] = (1.0 + (season_year - 2022) * 0.05) * np.where(df_bbb['is_ipl'], 1.25, 1.0)

print(f"Total Deliveries: {len(df_bbb):,}")
print(f"High-Pressure Deliveries: {df_bbb['is_high_pressure'].sum():,} ({df_bbb['is_high_pressure'].mean()*100:.1f}%)")

# Player mapping sets
ipl_players = set(df_map[df_map['comp_name'].str.contains('IPL', case=False, na=False)]['player_name'].unique())

# --- BATTING MODEL ---
hp_bat = df_bbb[df_bbb['is_high_pressure']].groupby(['striker_id', 'striker_name']).agg(
    hp_balls=('runs', 'count'),
    hp_runs=('runs', 'sum'),
    hp_dismissals=('is_wicket', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum'),
    hp_dots=('runs', lambda x: (x == 0).sum()),
    hp_matches=('match_id', 'nunique'),
    hp_ipl_balls=('is_ipl', 'sum'),
    hp_runs_above_exp=('runs_above_exp', 'sum')
).reset_index()

base_bat = df_bbb[~df_bbb['is_high_pressure']].groupby(['striker_id', 'striker_name']).agg(
    base_balls=('runs', 'count'),
    base_runs=('runs', 'sum'),
    base_dismissals=('is_wicket', 'sum'),
    base_dots=('runs', lambda x: (x == 0).sum()),
    base_boundaries=('is_four', lambda x: (x | df_bbb.loc[x.index, 'is_six']).sum())
).reset_index()

bat_df = hp_bat.merge(base_bat, on=['striker_id', 'striker_name'], how='inner')
bat_df['total_balls'] = bat_df['hp_balls'] + bat_df['base_balls']

bat_df['hp_sr'] = (bat_df['hp_runs'] / bat_df['hp_balls']) * 100.0
bat_df['hp_avg'] = bat_df['hp_runs'] / np.maximum(1, bat_df['hp_dismissals'])
bat_df['hp_bnd_pct'] = ((bat_df['hp_fours'] + bat_df['hp_sixes']) / bat_df['hp_balls']) * 100.0
bat_df['hp_dot_pct'] = (bat_df['hp_dots'] / bat_df['hp_balls']) * 100.0

bat_df['base_sr'] = (bat_df['base_runs'] / bat_df['base_balls']) * 100.0
bat_df['base_avg'] = bat_df['base_runs'] / np.maximum(1, bat_df['base_dismissals'])
bat_df['base_dot_pct'] = (bat_df['base_dots'] / bat_df['base_balls']) * 100.0

bat_df['delta_sr'] = bat_df['hp_sr'] - bat_df['base_sr']
bat_df['delta_avg'] = bat_df['hp_avg'] - bat_df['base_avg']
bat_df['delta_dot'] = bat_df['base_dot_pct'] - bat_df['hp_dot_pct']
bat_df['rae_per_100'] = (bat_df['hp_runs_above_exp'] / bat_df['hp_balls']) * 100.0
bat_df['is_ipl_player'] = bat_df['striker_name'].isin(ipl_players)

# Qualification: min 100 HP balls, min 250 total balls
q_bat = bat_df[(bat_df['hp_balls'] >= 100) & (bat_df['total_balls'] >= 250)].copy()

def zscore(s):
    return (s - s.mean()) / (s.std() + 1e-6)

z_sr = zscore(q_bat['hp_sr'])
z_avg = zscore(np.clip(q_bat['hp_avg'], 10, 60))
z_bnd = zscore(q_bat['hp_bnd_pct'])
z_dot = zscore(-q_bat['hp_dot_pct'])
z_delta_sr = zscore(np.clip(q_bat['delta_sr'], -30, 70))
z_delta_avg = zscore(np.clip(q_bat['delta_avg'], -30, 40))
z_rae = zscore(q_bat['rae_per_100'])

q_bat['shrinkage'] = np.sqrt(q_bat['hp_balls'] / (q_bat['hp_balls'] + 80.0))
q_bat['raw_ppi'] = (
    0.25 * z_sr +
    0.20 * z_avg +
    0.15 * z_rae +
    0.15 * z_bnd +
    0.15 * z_delta_sr +
    0.10 * z_delta_avg
)
q_bat['ppi_score'] = q_bat['raw_ppi'] * q_bat['shrinkage']
q_bat['ppi_scaled'] = 50.0 + (q_bat['ppi_score'] / q_bat['ppi_score'].std()) * 16.0
q_bat['ppi_scaled'] = np.clip(q_bat['ppi_scaled'], 10, 99.9)

# --- BOWLING MODEL ---
hp_bowl = df_bbb[df_bbb['is_high_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    hp_balls=('is_legal', 'sum'),
    hp_total_balls=('runs', 'count'),
    hp_runs=('bowler_runs', 'sum'),
    hp_wickets=('is_bowler_wicket', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum'),
    hp_dots=('runs', lambda x: (x == 0).sum()),
    hp_matches=('match_id', 'nunique'),
    hp_ipl_balls=('is_ipl', 'sum'),
    hp_runs_saved=('runs_saved', 'sum'),
    hp_wkts_above_exp=('wkts_above_exp', 'sum')
).reset_index()

base_bowl = df_bbb[~df_bbb['is_high_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    base_balls=('is_legal', 'sum'),
    base_total_balls=('runs', 'count'),
    base_runs=('bowler_runs', 'sum'),
    base_wickets=('is_bowler_wicket', 'sum'),
    base_dots=('runs', lambda x: (x == 0).sum()),
    base_fours=('is_four', 'sum'),
    base_sixes=('is_six', 'sum')
).reset_index()

bowl_df = hp_bowl.merge(base_bowl, on=['bowler_id', 'bowler_name'], how='inner')
bowl_df['total_balls'] = bowl_df['hp_balls'] + bowl_df['base_balls']

bowl_df['hp_econ'] = (bowl_df['hp_runs'] / np.maximum(1, bowl_df['hp_balls'])) * 6.0
bowl_df['hp_sr'] = bowl_df['hp_balls'] / np.maximum(1, bowl_df['hp_wickets'])
bowl_df['hp_avg'] = bowl_df['hp_runs'] / np.maximum(1, bowl_df['hp_wickets'])
bowl_df['hp_dot_pct'] = (bowl_df['hp_dots'] / bowl_df['hp_total_balls']) * 100.0
bowl_df['hp_bnd_pct'] = ((bowl_df['hp_fours'] + bowl_df['hp_sixes']) / bowl_df['hp_total_balls']) * 100.0

bowl_df['base_econ'] = (bowl_df['base_runs'] / np.maximum(1, bowl_df['base_balls'])) * 6.0
bowl_df['base_sr'] = bowl_df['base_balls'] / np.maximum(1, bowl_df['base_wickets'])
bowl_df['base_dot_pct'] = (bowl_df['base_dots'] / bowl_df['base_total_balls']) * 100.0

bowl_df['delta_econ'] = bowl_df['base_econ'] - bowl_df['hp_econ']
bowl_df['delta_sr'] = bowl_df['base_sr'] - bowl_df['hp_sr']
bowl_df['runs_saved_per_6'] = (bowl_df['hp_runs_saved'] / bowl_df['hp_balls']) * 6.0
bowl_df['is_ipl_player'] = bowl_df['bowler_name'].isin(ipl_players)

# Qualification: min 100 HP balls, min 250 total balls
q_bowl = bowl_df[(bowl_df['hp_balls'] >= 100) & (bowl_df['total_balls'] >= 250)].copy()

z_econ = zscore(-q_bowl['hp_econ'])
z_sr = zscore(-np.clip(q_bowl['hp_sr'], 8, 30))
z_dot = zscore(q_bowl['hp_dot_pct'])
z_bnd = zscore(-q_bowl['hp_bnd_pct'])
z_delta_econ = zscore(np.clip(q_bowl['delta_econ'], -4, 3))
z_rs = zscore(q_bowl['runs_saved_per_6'])
z_wickets = zscore(np.sqrt(q_bowl['hp_wickets']))

q_bowl['shrinkage'] = np.sqrt(q_bowl['hp_balls'] / (q_bowl['hp_balls'] + 80.0))
q_bowl['raw_ppi'] = (
    0.20 * z_econ +
    0.20 * z_sr +
    0.15 * z_rs +
    0.15 * z_dot +
    0.15 * z_bnd +
    0.15 * z_delta_econ
)
q_bowl['ppi_score'] = q_bowl['raw_ppi'] * q_bowl['shrinkage']
q_bowl['ppi_scaled'] = 50.0 + (q_bowl['ppi_score'] / q_bowl['ppi_score'].std()) * 16.0
q_bowl['ppi_scaled'] = np.clip(q_bowl['ppi_scaled'], 10, 99.9)

# Export rankings
q_bat = q_bat.sort_values(by='ppi_score', ascending=False).reset_index(drop=True)
q_bowl = q_bowl.sort_values(by='ppi_score', ascending=False).reset_index(drop=True)

q_bat.to_csv('batters_pressure_ranked.csv', index=False)
q_bowl.to_csv('bowlers_pressure_ranked.csv', index=False)

print("\n=== TOP 10 OVERALL BATTERS (UNIVERSAL MODEL) ===")
print(q_bat.head(10)[['striker_name', 'hp_balls', 'hp_runs', 'hp_sr', 'base_sr', 'delta_sr', 'hp_avg', 'hp_bnd_pct', 'ppi_scaled']])

print("\n=== TOP 10 IPL-ELIGIBLE / RR AUCTION BATTERS ===")
print(q_bat[q_bat['is_ipl_player']].head(10)[['striker_name', 'hp_balls', 'hp_runs', 'hp_sr', 'base_sr', 'delta_sr', 'hp_avg', 'hp_bnd_pct', 'ppi_scaled']])

print("\n=== TOP 10 OVERALL BOWLERS (UNIVERSAL MODEL) ===")
print(q_bowl.head(10)[['bowler_name', 'hp_balls', 'hp_wickets', 'hp_econ', 'base_econ', 'delta_econ', 'hp_sr', 'hp_dot_pct', 'ppi_scaled']])

print("\n=== TOP 10 IPL-ELIGIBLE / RR AUCTION BOWLERS ===")
print(q_bowl[q_bowl['is_ipl_player']].head(10)[['bowler_name', 'hp_balls', 'hp_wickets', 'hp_econ', 'base_econ', 'delta_econ', 'hp_sr', 'hp_dot_pct', 'ppi_scaled']])

