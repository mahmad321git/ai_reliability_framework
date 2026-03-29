import streamlit as st
import json
import pandas as pd
import glob
import os


st.title("AI Reliability Testing Dashboard")


# Locate report files
report_path = os.path.join("reports","accuracy","*.json")

files = glob.glob(report_path)


if not files:

    st.warning("No reports found. Run evaluation first.")

    st.stop()


# Load latest report
latest_file = sorted(files)[-1]


st.sidebar.write("Latest Report:")
st.sidebar.write(latest_file)


with open(latest_file,"r",encoding="utf-8") as f:

    report = json.load(f)


accuracy = report["accuracy"]


st.metric(

    label="Model Accuracy",

    value=f"{accuracy*100:.2f}%"

)


df = pd.DataFrame(report["results"])


st.subheader("Evaluation Results")

st.dataframe(df)


st.subheader("Correct vs Incorrect")

correct_counts = df["correct"].value_counts()

st.bar_chart(correct_counts)


st.subheader("Similarity Distribution")

st.histogram_chart = st.bar_chart(df["similarity"])