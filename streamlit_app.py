import streamlit as st
import pandas as pd

Tier Definitions & Constants
TIERS = [
    {"name": "Tier 1", "beans": 10999, "diamonds": 3045},
    {"name": "Tier 2", "beans": 3999, "diamonds": 1105},
    {"name": "Tier 3", "beans": 999, "diamonds": 275},
    {"name": "Tier 4", "beans": 109, "diamonds": 29},
    {"name": "Tier 5", "beans": 8, "diamonds": 2}
]

Conversion Functions
def convertbeans(inputbeans):
    beansleft = inputbeans
    diamonds = 0
    used_beans = 0
    breakdown = []

    for tier in TIERS:
        count = beans_left // tier["beans"]
        if count > 0:
            used = count * tier["beans"]
            gained = count * tier["diamonds"]
            beans_left -= used
            diamonds += gained
            used_beans += used
            breakdown.append({
                "Tier": tier["name"],
                "Count": count,
                "Used Beans": used,
                "Gained Diamonds": gained,
                "Efficiency": round(tier["diamonds"] / tier["beans"], 4)
            })

    metrics = {
        "Efficiency": round(diamonds / usedbeans, 4) if usedbeans else 0,
        "Used %": round((usedbeans / inputbeans) * 100, 2) if input_beans else 0,
        "Unused Beans": beans_left,
        "Total Diamonds": diamonds
    }

    return breakdown, metrics

def reverseconvert(targetdiamonds):
    tiers_sorted = sorted(TIERS, key=lambda x: x["diamonds"] / x["beans"], reverse=True)
    beans_needed = 0
    breakdown = []

    for tier in tiers_sorted:
        count = target_diamonds // tier["diamonds"]
        if count > 0:
            used_diamonds = count * tier["diamonds"]
            used_beans = count * tier["beans"]
            beansneeded += usedbeans
            targetdiamonds -= useddiamonds
            breakdown.append({
                "Tier": tier["name"],
                "Count": count,
                "Used Beans": used_beans,
                "Gained Diamonds": used_diamonds,
                "Efficiency": round(tier["diamonds"] / tier["beans"], 4)
            })

    return breakdown, beansneeded, targetdiamonds

Strategy Helper
def generate_tip(eff, usage):
    if eff >= 0.3 and usage > 80:
        return "✅ You're squeezing great value from your beans!"
    elif eff < 0.2 and usage > 70:
        return "⚠️ Prioritize higher tiers for better yield."
    elif usage < 50:
        return "💡 Try saving up to unlock premium tiers."
    return "🔍 Mixed strategy detected. Tweak and explore options."

Streamlit UI
st.setpageconfig(pagetitle="Bean Converter Dashboard", pageicon="🫘")
st.title("💰 Bean-to-Diamond Conversion Lab")

mode = st.radio("Choose Mode", ["Forward Conversion", "Reverse Target"])

if mode == "Forward Conversion":
    beans = st.numberinput("Enter Bean Count:", minvalue=0, step=1)
    if st.button("Convert"):
        breakdown, metrics = convert_beans(beans)
        st.subheader("📊 Metrics")
        st.metric("Efficiency", metrics["Efficiency"])
        st.metric("Used %", f"{metrics['Used %']}%")
        st.metric("Unused Beans", metrics["Unused Beans"])
        st.metric("Total Diamonds", metrics["Total Diamonds"])
        st.info(generate_tip(metrics["Efficiency"], metrics["Used %"]))
        st.subheader("📦 Breakdown")
        df = pd.DataFrame(breakdown)
        st.dataframe(df)
        st.barchart(df.setindex("Tier")[["Gained Diamonds"]])

elif mode == "Reverse Target":
    target = st.numberinput("Target Diamonds:", minvalue=1)
    if st.button("Calculate Required Beans"):
        breakdown, beansneeded, shortfall = reverseconvert(target)
        st.metric("Beans Needed", beans_needed)
        st.metric("Remaining Diamonds", shortfall)
        df = pd.DataFrame(breakdown)
        st.dataframe(df)
        st.barchart(df.setindex("Tier")[["Used Beans"]])
