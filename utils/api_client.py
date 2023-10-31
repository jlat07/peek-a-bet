import streamlit as st
import requests

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    @st.cache(ttl=60)  # Cache for 1 minute
    def get_game_data(self, team_name: str):
        """
        Fetch real-time game data for a given team.
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        endpoint = f"{self.base_url}/getGameData?team={team_name}"
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to retrieve data for {team_name}.")
            return None

    # @st.cache(ttl=60)  # Cache for 1 minute
    # def get_team_data(self, team_name: str):
    #     """
    #     Fetch overall data for a given team.
    #     """
    #     headers = {
    #         'Authorization': f'Bearer {self.api_key}'
    #     }
    #     endpoint = f"{self.base_url}/getTeamData?team={team_name}"
    #     response = requests.get(endpoint, headers=headers)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         st.error(f"Failed to retrieve team data for {team_name}.")
    #         return None
