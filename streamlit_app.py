import streamlit as st
import pandas as pd
import requests
import json
import re
from datetime import datetime
from pandas import json_normalize

# pull player data from draftkings
contest_response = json.loads(requests.get("https://www.draftkings.com/lobby/getcontests?sport=nba&gametype=classic").text)
contest_dg = contest_response["Contests"][0]["dg"]
contest_date = contest_response["Contests"][0]["sd"]
extract_date = re.findall('\d{13}', contest_date)
extract_date_int = int(''.join(str(i) for i in extract_date))
current_date = datetime.fromtimestamp(extract_date_int/1000)

player_extract = json.loads(requests.get(f"https://api.draftkings.com/draftgroups/v1/draftgroups/{contest_dg}/draftables").text)
df = json_normalize(player_extract, "draftables")
player_data = df[["displayName", "position", "salary", "teamAbbreviation"]].drop_duplicates()

st.write(f"Daily Player Extract {current_date}")
st.dataframe(player_data)

def convert_df(player_data):
    return player_data.to_csv(index=False).encode('utf-8')

csv = convert_df(player_data)

st.download_button("CSV", csv, f"player_extract_{extract_date}.csv", "text/csv", key='download-csv')


