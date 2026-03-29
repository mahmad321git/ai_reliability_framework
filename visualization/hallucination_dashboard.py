import streamlit as st
import json
import pandas as pd
import glob
import os


st.set_page_config(
    page_title="Hallucination Detection Dashboard",
    layout="wide"
)

st.title("LLM Hallucination Detection Dashboard")


# Locate hallucination reports
report_path = os.path.join(
    "reports",
    "hallucination",
    "*.json"
)

files = glob.glob(report_path)


if not files:

    st.warning(
        "No hallucination reports found. Run test_hallucination.py first."
    )

    st.stop()


# Select report
selected_file = st.sidebar.selectbox(

    "Select Report",

    sorted(files)

)


st.sidebar.write("Selected:")
st.sidebar.write(selected_file)


# Load report
with open(
    selected_file,
    "r",
    encoding="utf-8"
) as f:

    report = json.load(f)


# Metrics section
st.header("Hallucination Metrics")


col1, col2, col3 = st.columns(3)


col1.metric(

    "Hallucination Rate",

    f"{report['hallucination_rate']*100:.2f}%"

)


col2.metric(

    "Total Cases",

    report["total_cases"]

)


col3.metric(

    "Hallucinated Cases",

    report["hallucination_count"]

)


# Convert to dataframe
df = pd.DataFrame(

    report["results"]

)


st.header("Detailed Results")


# Color highlighting
def highlight(val):

    if val == "Hallucinated":

        return "background-color:#ffcccc"

    if val == "Grounded":

        return "background-color:#ccffcc"

    return "background-color:#fff3cd"


styled_df = df.style.applymap(

    highlight,

    subset=["label"]

)


st.dataframe(

    styled_df,

    use_container_width=True

)


# Distribution chart
st.header("Grounding Distribution")

label_counts = df["label"].value_counts()

st.bar_chart(label_counts)


# Similarity distribution
st.header("Similarity Scores")

st.bar_chart(

    df["similarity"]

)


# Show hallucinated cases only
st.header("Hallucinated Responses")


hallucinated_df = df[

    df["hallucinated"] == True

]


if len(hallucinated_df) > 0:

    st.dataframe(

        hallucinated_df,

        use_container_width=True

    )

else:

    st.success(

        "No hallucinations detected"

    )