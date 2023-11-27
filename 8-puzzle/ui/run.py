import streamlit as st
import pandas as pd
import numpy as np
import time

from src.main import HillClimbing

def get_puzzle_input() -> np.array:
    # getting the puzzle input 
    initial_state = np.array(
        [
            [4, 1, 3],
            [2, np.nan, 5],
            [6, 7, 8],
        ],
    )
    df = pd.DataFrame(initial_state, columns=["c1", "c2", "c3"])

    # Create three columns for input
    # col1, col2, col3 = st.columns(3)


    # # Inputs for the first column
    # with col1:
    #     st.write("c1 Inputs")
    #     input_1 = st.text_input("Input 1", value=df['c1'][0])
    #     input_2 = st.text_input("Input 2", value=df['c1'][1])
    #     input_3 = st.text_input("Input 3", value=df['c1'][2])

    # # Inputs for the second column
    # with col2:
    #     st.write("c2 Inputs")
    #     input_4 = st.text_input("Input 4", value=df['c2'][0])
    #     input_5 = st.text_input("Input 5", value=df['c2'][1])
    #     input_6 = st.text_input("Input 6", value=df['c2'][2])

    # # Inputs for the third column
    # with col3:
    #     st.write("c3 Inputs")
    #     input_7 = st.text_input("Input 7", value=df['c3'][0])
    #     input_8 = st.text_input("Input 8", value=df['c3'][1])
    #     input_9 = st.text_input("Input 9", value=df['c3'][2])


    # with col2 :
    #     df = pd.DataFrame({
    #         'c1': [input_1, input_2, input_3],
    #         'c2': [input_4, input_5, input_6],
    #         'c3': [input_7, input_8, input_9]
    #     })

    df = df.to_numpy()
    return df

def show_state(state: np.array, placeholder=st) -> pd.DataFrame:
    placeholder.dataframe(
        pd.DataFrame(state, columns=["c1", "c2", "c3"]),
        hide_index=True,
    )

def run(initial_state: np.array) :
    hc = HillClimbing(initial_state)
    epoch = 0
    placeholder = st.empty()
    while not hc.end :
        if epoch >= 50 : # restarting after 50 iterations
            hc = HillClimbing(initial_state)
            epoch = 0
        for s in hc.run() :
            show_state(s, placeholder)
            # time.sleep(1)



def main() :
    col1, col2, col3 = st.columns(3)
    initial_state = get_puzzle_input()
    with col2 :
        st.header(":red[Starting State: ]")
        show_state(initial_state)
        if st.button(":blue[Start]") :
            run(initial_state)


main()