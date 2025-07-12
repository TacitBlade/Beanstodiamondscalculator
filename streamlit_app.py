import streamlit as st
import pandas as pd
import numpy as np

# 🌟 Page setup
st.set_page_config(
    page_title="Bean Converter Dashboard",
    page_icon="🫘",
    layout="wide"
)

# 🧾 Tier Definitions & Constants
TIER_RATES = {
    "Tier 1": 1.0,
    "Tier 2": 1.2,
    "Tier 3": 1.5
}

AGENT_NAMES = ["Alice", "Bob", "Charlie"]

# 📥 Sidebar: User inputs
with st.sidebar:
    st.header("Input Parameters")
    selected_agent = st.selectbox("Select Agent", AGENT_NAMES)
    selected_tier = st.selectbox("Select Tier", list(TIER_RATES.keys()))
    beans_input = st.number_input("Enter Beans", min_value=0)

# 🔍 Conversion Logic
def convert_beans(beans, tier):
    rate = TIER_RATES.get(tier, 1.0)
    return beans * rate

converted_beans = convert_beans(beans_input, selected_tier)

# 📊 Display Output
st.title("Bean Converter Dashboard")
st.subheader(f"Results for {selected_agent}")
st.write(f"Tier Selected: **{selected_tier}**")
st.write(f"Original Beans: **{beans_input}**")
st.write(f"Converted Beans: 🫘 **{converted_beans:.2f}**")

# 📤 Export to Excel
def export_to_excel(agent, tier, beans, converted):
    df = pd.DataFrame({
        "Agent": [agent],
        "Tier": [tier],
        "Input Beans": [beans],
        "Converted Beans": [converted]
    })
    with pd.ExcelWriter("bean_conversion_output.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    st.success("Excel file exported successfully!")

if st.button("Export to Excel"):
    export_to_excel(selected_agent, selected_tier, beans_input, converted_beans)