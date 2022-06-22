import requests
import pandas as pd
import json
import streamlit as st


def getOriginalRosters():
    rosters = requests.get('https://api.sleeper.app/v1/league/842175136839880704/rosters').text
    df = pd.read_json(rosters)
    df = df[['roster_id','players']]

    return df

def getOriginalFullPlayer():
    full_player = requests.get('https://api.sleeper.app/v1/players/nfl').text
    data = json.loads(full_player)

    columns = ['search_full_name', 'injury_status', 'full_name', 'pandascore_id',
        'weight', 'news_updated', 'high_school', 'rotowire_id', 'years_exp',
        'depth_chart_position', 'age', 'status', 'fantasy_data_id',
        'first_name', 'birth_state', 'practice_participation',
        'practice_description', 'position', 'birth_city', 'search_first_name',
        'college', 'team', 'sportradar_id', 'injury_start_date', 'number',
        'injury_notes', 'sport', 'injury_body_part', 'search_last_name',
        'swish_id', 'metadata', 'gsis_id', 'stats_id', 'last_name',
        'search_rank', 'fantasy_positions', 'birth_date', 'depth_chart_order',
        'hashtag', 'active', 'player_id', 'birth_country', 'rotoworld_id',
        'yahoo_id', 'espn_id', 'height', 'user_id']

    df_players_all = pd.DataFrame(data=None,columns=columns)

    for user_id,d in data.items():
        df_player_temp = pd.DataFrame([d])
        df_player_temp['user_id'] = user_id
        df_players_all = pd.concat([df_players_all,df_player_temp],axis=0)
    

    return df_players_all

def getDesiredRosters(df_rosters_original,df_players_all):
    rosters_all_data = []
    for index, row in df_rosters_original.iterrows():
        roster_id = row['roster_id']
        for user_id in row['players']:
            player_name_all_columns = df_players_all[df_players_all.user_id == user_id]
            player_name = player_name_all_columns['full_name'][0]
            status = player_name_all_columns['status'][0]
            rosters_all_data.append([roster_id,player_name,status])
    
    df_rosters_all = pd.DataFrame(data=rosters_all_data,columns=['roster_id','player_name','status'])
    df_rosters_all.dropna(inplace=True)

    return df_rosters_all


if __name__ == "__main__":
   
   
    st.markdown("<h1 style='text-align: center; color: black;'>Fiverr</h1>", unsafe_allow_html=True)

    result = st.button("Download Player Data")
    if result:
        st.title("Player Information:")
        df_rosters_original = getOriginalRosters()
        df_players_all = getOriginalFullPlayer()
        
        df_1 = getDesiredRosters(df_rosters_original,df_players_all)
        pivot = df_1.pivot(columns = 'roster_id',values = 'player_name').reset_index()
        df_2 = pivot.apply(lambda x: pd.Series(x.dropna().values)).fillna('')
        
        st.dataframe(df_1)
        st.dataframe(df_2)


    

