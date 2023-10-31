# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code


def animation_demo() -> None:
# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

    st.set_page_config(
      
    )

# Mock data for ticket details
games = [
    {"team": "SAINTS", "condition": "OV 43½", "status": "In Progress"},
    {"team": "STEELERS", "condition": "UN 42½", "status": "win"},
    {"team": "COMMANDERS", "condition": "+7½", "status": "win"},
    {"team": "PATRIOTS", "condition": "OV 47½", "status": "win"},
    {"team": "BENGALS", "condition": "+5½", "status": "win"},
    {"team": "CHARGERS", "condition": "-8½", "status": "win"},
    {"team": "BEARS", "condition": "OV 46½", "status": "win"},
    #... add other games
]

# UI for the ticket
st.title("Parlay Ticket")
st.write("##### PF4DF3EAB7A0C")

st.write("## Parlay Card Week 8")

# Iterating over games to display each row
for game in games:
    status_color = "gray"
    border_style = "none"
    
    if game["status"] == "win":
        status_color = "green"
        border_style = "2px solid white"
    elif game["status"] == "lose":
        status_color = "red"
        border_style = "2px solid white"
    
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.write(game["team"])
    with col2:
        st.write(game["condition"])
    with col3:
        st.markdown(f"<div style='background-color: {status_color}; border: {border_style}; padding: 10px;'>{game['status'].capitalize()}</div>", unsafe_allow_html=True)

st.write("#### Ticket Cost: US$5.00")
st.write("#### To Win: US$370.00")
st.write("#### To Collect: US$375.00")