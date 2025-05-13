

from app.data_ingestion.google_maps_puller import GoogleMapsDataPull
from app.data_ingestion.tripadviser_puller import TripAdviserDataPull
from app.preprocessing import CleanAndSaveToChromaDBC
from app.recommender import retrive_generate , check_dB_data
from utils.common_utils import trig_retriver

import streamlit as st

# Session state to store conversation flow
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.place = ""
    st.session_state.location = ""
    st.session_state.question = ""


if st.session_state.step == 3: 
    foodPlace = st.session_state.place + st.session_state.location

    st.session_state.retriver = check_dB_data(foodPlace=foodPlace)


st.title("🍽️ Your Great Food buddie 🥗")

# Step 1: Ask for food place
if st.session_state.step == 1:
    st.session_state.place = st.text_input("What's the name of the food place?")
    if st.session_state.place:
        st.session_state.step = 2
        st.rerun()

# Step 2: Ask for location
elif st.session_state.step == 2:
    st.session_state.location = st.text_input(f"Where is '{st.session_state.place}' located?")
    if st.session_state.location:
        st.session_state.step = 3
        st.rerun()

# Step 3: Ask for the user's question
elif st.session_state.step == 3:
    st.session_state.question = st.text_input("What would you like to ask?")
    if st.session_state.question:
        st.session_state.step = 4
        st.rerun()

# Step 4: Show the answer
elif st.session_state.step == 4:
    _,answer = retrive_generate(retriever = st.session_state.retriver,
                              question = st.session_state.question)

    st.markdown(f"**Q:** {st.session_state.question[0].upper()+st.session_state.question[1:]}?")
    st.markdown(f"{answer}")

    if st.button("Ask another question"):
        st.session_state.step = 3
        st.session_state.question = ""
        st.rerun()

    if st.button("Start Over"):
        for key in ["step", "place", "location", "question"]:
            st.session_state[key] = ""
        st.session_state.step = 1
        st.rerun()
 