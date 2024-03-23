import streamlit as st
import pandas as pd
import os


header=st.container()
ratios=st.container()


def read_files_starting_with_update(directory):
    try:
        # Get a list of files in the specified directory
        files = os.listdir(directory)
        
        update_files = [file for file in files if file.startswith("Pending_Updates")]
        return update_files

    except OSError as err:
        print(f"Error: {err}")




with header:
    st.title("Linux Pending Updates")


with ratios:
    for file in read_files_starting_with_update("."):
        df=pd.read_json(file)
        st.write(df)





