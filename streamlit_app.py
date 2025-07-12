import streamlit as st
import pandas as pd

--- Conversion Tiers ---
TIERS = [
    {"tier": "Tier 1", "diamonds": 3045, "beans": 10999},
    {"tier": "Tier 2", "diamonds": 1105, "beans": 3999},
    {"tier": "Tier 3", "diamonds": 275, "beans": 999},
    {"tier": "Tier 4", "diamonds": 29, "beans": 109},
    {"tier": "Tier 5", "diamonds": 2, "beans": 8},
]

--- Forward Conversion ---
def convertbeans(inputbeans):
    beansleft = inputbeans
    diamonds = 0
    total_used = 0
    breakdown = []

    for t in TIERS:
        count = beans_left // t["beans"]
        if count > 0:
            used = count * t["beans"]
            gained = count * t["diamonds"]
            beans_left -= used
            diamonds += gained
            total_used += used
            breakdown.append({
                "Tier": t["tier"],
                "Count": count,
                "Used Beans": used,
                "Gained Diamonds": gained,
                "Efficiency (💎/🫘)": round(t["diamonds"] / t["beans"], 4)
            })

    metrics = {
        "Conversion Efficiency": round(diamonds / totalused, 4) if totalused else 0,
        "Beans Usage Rate (%)": round((totalused / inputbeans) * 100, 2) if input_beans else 0,
        "Unused Beans": beans_left,
        "Total Diamonds": diamonds
    }

    return breakdown, metrics

--- Reverse Conversion ---
def reverseconvert(targetdiamonds):
    sorted_tiers = sorted(TIERS, key=lambda x: x["diamonds"] / x["beans"], reverse=True)
    required_beans = 0
    breakdown = []

    for t in sorted_tiers:
        count = target_diamonds // t["diamonds"]
        if count > 0:
            used_diamonds = count * t["diamonds"]
            used_beans = count * t["beans"]
            requiredbeans += usedbeans
            targetdiamonds -= useddiamonds
            breakdown.append({
                "Tier": t["tier"],
                "Count": count,
                "Used Beans": used_beans,
                "Gained Diamonds": used_diamonds,
                "Efficiency (💎/🫘)": round(t["diamonds"] / t["beans"], 4)
            })

    return breakdown, requiredbeans, targetdiamonds

--- Strategy Tip Generator ---
def generatetip(efficiency, usagerate):
    if efficiency >= 0.3 and usage_rate > 80:
        return "✅ You're maximizing your beans smartly."
    elif efficiency < 0.2 and usage_rate > 70:
        return "⚠️ Consider prioritizing higher tiers next time."
    elif usage_rate < 50:
        return "💡 Try saving more beans to access better tiers."
    return "🔍 Mixed strategy detected. A tier overview might help."

--- UI ---
st.setpageconfig(pagetitle="Tactical Bean Calculator", pageicon="🧠")
st.title("🧠 Bean-to-Diamond Tactical Dashboard")

mode = st.radio("Choose Mode", ["Forward Conversion", "Reverse Target"])

if mode == "Forward Conversion":
    beans = st.numberinput("Enter beans:", minvalue=0, step=1)
    if st.button("Convert"):
        breakdown, metrics = convert_beans(beans)
        st.subheader("📊 Conversion Metrics")
        st.metric("💎 Conversion Efficiency", metrics["Conversion Efficiency"])
        st.metric("📈 Beans Usage Rate", f"{metrics['Beans Usage Rate (%)']}%")
        st.metric("🗑️ Beans Left", metrics["Unused Beans"])
        st.metric("💎 Total Diamonds", metrics["Total Diamonds"])

        st.info(generate_tip(metrics["Conversion Efficiency"], metrics["Beans Usage Rate (%)"]))
        df = pd.DataFrame(breakdown)
        st.subheader("📦 Tier Breakdown")
        st.dataframe(df)
        st.barchart(df.setindex("Tier")[["Gained Diamonds"]])

elif mode == "Reverse Target":
    diamondsgoal = st.numberinput("Target Diamonds:", min_value=1, step=1)
    if st.button("Calculate Required Beans"):
        breakdown, beansneeded, shortfall = reverseconvert(diamonds_goal)
        st.subheader("📐 Reverse Strategy Breakdown")
        st.metric("🫘 Beans Needed", beans_needed)
        st.metric("💎 Diamonds Remaining", shortfall)
        df = pd.DataFrame(breakdown)
        st.dataframe(df)

        st.barchart(df.setindex("Tier")[["Used Beans"]])