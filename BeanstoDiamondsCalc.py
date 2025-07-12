#!/usr/bin/env python3
"""
Beans to Diamonds Calculator (Streamlit version)
"""

import math
from typing import Dict, Optional
from dataclasses import dataclass
import streamlit as st

@dataclass
class ConversionTier:
    min_beans: int
    max_beans: float
    diamonds_per_bean: float
    efficiency: float
    fixed_diamonds: Optional[int] = None

class BeansToDiamondsCalculator:
    def __init__(self):
        self.conversion_tiers = [
            ConversionTier(1, 8, 0.25, 25.00, 2),
            ConversionTier(9, 109, 0.2661, 26.61, 29),
            ConversionTier(110, 999, 0.2753, 27.53, 275),
            ConversionTier(1000, 3999, 0.2763, 27.63, 1105),
            ConversionTier(4000, 10999, 0.2768, 27.68, 3045),
            ConversionTier(11000, float('inf'), 0.2767, 27.67, None)
        ]

    def find_tier(self, beans: int) -> Optional[ConversionTier]:
        for tier in self.conversion_tiers:
            if tier.min_beans <= beans <= tier.max_beans:
                return tier
        return None

    def calculate_diamonds(self, beans: int) -> Optional[Dict]:
        if not beans or beans <= 0:
            return None

        tier = self.find_tier(beans)
        if not tier:
            return None

        if tier.fixed_diamonds and beans == tier.max_beans:
            diamonds = tier.fixed_diamonds
        else:
            diamonds = math.floor(beans * tier.diamonds_per_bean)

        remainder = beans % math.ceil(1 / tier.diamonds_per_bean)
        tier_number = self.conversion_tiers.index(tier) + 1

        return {
            'diamonds': diamonds,
            'remainder': remainder,
            'efficiency': tier.efficiency,
            'diamonds_per_bean': tier.diamonds_per_bean,
            'tier': tier_number
        }

    def get_efficiency_tip(self, beans: int) -> str:
        if beans < 109:
            return "💡 Tip: Efficiency increases significantly after 109 beans!"
        elif beans < 4000:
            return "💡 Tip: Maximum efficiency is reached at 4000+ beans!"
        else:
            return "💡 Great! You're at maximum efficiency tier!"

    def get_tier_table(self):
        rows = []
        for tier in self.conversion_tiers:
            max_beans_str = "∞" if tier.max_beans == float('inf') else f"{int(tier.max_beans):,}"
            range_str = f"{tier.min_beans:,} - {max_beans_str}"
            rate = f"{tier.diamonds_per_bean:.4f}"
            efficiency = f"{tier.efficiency:.2f}%"
            if tier.fixed_diamonds and tier.max_beans < float('inf'):
                example = f"{int(tier.max_beans):,} beans = {tier.fixed_diamonds} diamonds"
            else:
                example = efficiency
            rows.append((range_str, rate, efficiency, example))
        return rows

def main():
    st.set_page_config(page_title="Beans to Diamonds Calculator", page_icon="💎")

    st.title("💎 Beans to Diamonds Calculator")
    st.caption("Convert your beans to diamonds with tier-based efficiency rates")

    calculator = BeansToDiamondsCalculator()

    beans = st.number_input("Enter number of beans", min_value=1, step=1)

    if st.button("Calculate"):
        result = calculator.calculate_diamonds(beans)

        if result:
            st.success("✅ Conversion Result")
            st.metric("Diamonds", result['diamonds'])
            st.metric("Efficiency", f"{result['efficiency']}%")
            st.metric("Rate", f"{result['diamonds_per_bean']:.4f} per bean")
            if result['remainder'] > 0:
                st.info(f"Beans remainder: {result['remainder']} (may not convert)")
            st.info(f"Tier: {result['tier']}")
            st.markdown(f"**{calculator.get_efficiency_tip(beans)}**")
        else:
            st.error("❌ Unable to calculate conversion.")

    with st.expander("📊 View Conversion Tier Table"):
        tier_data = calculator.get_tier_table()
        st.table(
            {
                "Beans Range": [row[0] for row in tier_data],
                "Rate": [row[1] for row in tier_data],
                "Efficiency": [row[2] for row in tier_data],
                "Example": [row[3] for row in tier_data],
            }
        )

if __name__ == "__main__":
    main()
