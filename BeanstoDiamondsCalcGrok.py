#!/usr/bin/env python3
"""
Beans to Diamonds Calculator (Streamlit version)
A tool to convert beans to diamonds using tier-based rates, with optimization and tier table display.
"""

import math
from typing import Dict, Optional, List
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
        """Find the conversion tier for a given number of beans."""
        for tier in self.conversion_tiers:
            if tier.min_beans <= beans <= tier.max_beans:
                return tier
        return None

    def calculate_diamonds(self, beans: int) -> Optional[Dict]:
        """
        Calculate diamonds from beans based on the applicable tier.
        Args:
            beans: Number of beans to convert (must be a positive integer).
        Returns:
            Dictionary with diamonds, remainder, efficiency, rate, and tier, or None if invalid input.
        """
        if not isinstance(beans, int) or beans <= 0:
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

    def optimize_beans(self, beans: int) -> tuple[List[Dict], int]:
        """
        Optimize bean distribution across tiers to maximize diamonds.
        Prioritizes higher tiers for better efficiency, except Tier 6 (27.67%) which is slightly
        less efficient than Tier 5 (27.68%) but handles larger inputs.
        Args:
            beans: Number of beans to optimize (must be a positive integer).
        Returns:
            Tuple of (breakdown list, total diamonds), or empty list and 0 if invalid input.
        """
        if not isinstance(beans, int) or beans <= 0:
            return [], 0

        breakdown = []
        total_diamonds = 0
        remaining_beans = beans

        for tier in reversed(self.conversion_tiers):
            if remaining_beans >= tier.min_beans:
                max_beans = tier.max_beans if tier.max_beans != float('inf') else remaining_beans
                beans_in_tier = min(remaining_beans, int(max_beans))
                if tier.fixed_diamonds and beans_in_tier == tier.max_beans:
                    diamonds = tier.fixed_diamonds
                else:
                    diamonds = math.floor(beans_in_tier * tier.diamonds_per_bean)
                breakdown.append({
                    'tier': self.conversion_tiers.index(tier) + 1,
                    'beans': beans_in_tier,
                    'diamonds': diamonds,
                    'rate': tier.diamonds_per_bean,
                    'efficiency': tier.efficiency
                })
                total_diamonds += diamonds
                remaining_beans -= beans_in_tier

        if remaining_beans > 0:
            tier = self.conversion_tiers[0]
            diamonds = math.floor(remaining_beans * tier.diamonds_per_bean)
            breakdown.append({
                'tier': 1,
                'beans': remaining_beans,
                'diamonds': diamonds,
                'rate': tier.diamonds_per_bean,
                'efficiency': tier.efficiency
            })
            total_diamonds += diamonds

        breakdown = sorted(breakdown, key=lambda x: x['tier'])
        return breakdown, total_diamonds

    def get_efficiency_tip(self, beans: int) -> str:
        """
        Provide a tip based on the number of beans to encourage optimal conversion.
        Args:
            beans: Number of beans.
        Returns:
            A string with an efficiency tip.
        """
        if not isinstance(beans, int) or beans <= 0:
            return "💡 Tip: Please enter a positive number of beans."
        if beans < 109:
            return "💡 Tip: Efficiency increases significantly after 109 beans!"
        elif beans < 4000:
            return "💡 Tip: Maximum efficiency is reached at 4000+ beans!"
        else:
            return "💡 Great! You're at maximum efficiency tier!"

    def get_tier_table(self) -> List[tuple]:
        """
        Generate a table of conversion tiers with ranges, rates, efficiencies, and examples.
        Returns:
            List of tuples containing (range, rate, efficiency, example) for each tier.
        """
        rows = []
        for tier in self.conversion_tiers:
            max_beans_str = "∞" if tier.max_beans == float('inf') else f"{int(tier.max_beans):,}"
            range_str = f"{tier.min_beans:,} - {max_beans_str}"
            rate = f"{tier.diamonds_per_bean:.4f}"
            efficiency = f"{tier.efficiency:.2f}%"
            if tier.fixed_diamonds and tier.max_beans < float('inf'):
                example = f"{int(tier.max_beans):,} beans = {tier.fixed_diamonds:,} diamonds"
            else:
                example = efficiency
            rows.append((range_str, rate, efficiency, example))
        return rows

def main():
    st.set_page_config(page_title="Beans to Diamonds Calculator", page_icon="💎")

    st.title("💎 Beans to Diamonds Calculator")
    st.caption("Convert your beans to diamonds with tier-based efficiency rates")

    calculator = BeansToDiamondsCalculator()

    # Use session state to manage input and allow reset
    if 'beans' not in st.session_state:
        st.session_state.beans = 1

    beans = st.number_input(
        "Enter number of beans",
        min_value=1,
        step=1,
        value=st.session_state.beans,
        format="%d"
    )
    st.session_state.beans = beans

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Calculate"):
            result = calculator.calculate_diamonds(beans)
            if result:
                st.session_state.result = result
                st.session_state.breakdown, st.session_state.total_diamonds = calculator.optimize_beans(beans)
            else:
                st.session_state.result = None
    with col2:
        if st.button("Reset"):
            st.session_state.beans = 1
            st.session_state.result = None
            st.session_state.breakdown = None
            st.session_state.total_diamonds = None

    if hasattr(st.session_state, 'result') and st.session_state.result:
        result = st.session_state.result
        st.success("✅ Conversion Result")
        st.metric("Diamonds", f"{result['diamonds']:,}")
        st.metric("Efficiency", f"{result['efficiency']}%")
        st.metric("Rate", f"{result['diamonds_per_bean']:.4f} per bean")
        if result['remainder'] > 0:
            st.info(f"Beans remainder: {result['remainder']:,} (may not convert)")
        st.info(f"Tier: {result['tier']}")
        st.markdown(f"**{calculator.get_efficiency_tip(beans)}**")

        # Optimization breakdown
        st.subheader("🔎 Optimized Conversion Breakdown")
        st.write(f"**Total Diamonds (Optimized): {st.session_state.total_diamonds:,}**")
        st.table({
            "Tier": [b['tier'] for b in st.session_state.breakdown],
            "Beans Used": [f"{b['beans']:,}" for b in st.session_state.breakdown],
            "Diamonds Earned": [f"{b['diamonds']:,}" for b in st.session_state.breakdown],
            "Rate": [f"{b['rate']:.4f}" for b in st.session_state.breakdown],
            "Efficiency": [f"{b['efficiency']}%" for b in st.session_state.breakdown],
        })
    elif hasattr(st.session_state, 'result') and st.session_state.result is None:
        st.error("❌ Unable to calculate conversion. Please enter a positive integer.")

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

    st.markdown(
        "<div style='text-align: center; font-size: 14px; margin-top: 32px;'>© 2025 Alpha Agency & T Star Agency. All rights reserved.</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()