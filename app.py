import math
from typing import Dict, List

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Global Market Intelligence Assistant",
    page_icon="📈",
    layout="wide",
)

SYSTEM_PROMPT = """
You are an advanced AI-powered Global Market Intelligence Assistant designed to analyze financial markets and provide structured, data-driven insights.
You do NOT execute trades and you are NOT a licensed financial advisor.
""".strip()

ASSET_DATA: Dict[str, Dict[str, Dict[str, object]]] = {
    "Cryptocurrency": {
        "Bitcoin": {
            "market": "Cryptocurrency",
            "opportunity": "Large-cap crypto with strong institutional interest and macro sensitivity.",
            "key_insight": "Momentum remains attractive when risk appetite improves, but short-term swings can be sharp.",
            "expected_return": 16,
            "risk_level": "High",
            "volatility": "High",
            "confidence": 0.74,
            "short_term": "Volatile but opportunity-rich if momentum holds.",
            "long_term": "Constructive if adoption and ETF flows remain healthy.",
            "recommendation": "Monitor",
            "risks": [
                "Macro-driven selloffs",
                "Regulatory headlines",
                "High daily price swings",
            ],
        },
        "Ethereum": {
            "market": "Cryptocurrency",
            "opportunity": "Smart-contract leader with ecosystem-driven upside.",
            "key_insight": "Network utility and developer activity support long-term relevance.",
            "expected_return": 18,
            "risk_level": "High",
            "volatility": "High",
            "confidence": 0.71,
            "short_term": "Can outperform in bullish crypto cycles, but remains unstable.",
            "long_term": "Positive if usage growth and ecosystem expansion continue.",
            "recommendation": "Monitor",
            "risks": [
                "Layer-1 competition",
                "Fee pressure / network narrative shifts",
                "High volatility during market stress",
            ],
        },
        "Solana": {
            "market": "Cryptocurrency",
            "opportunity": "High-beta crypto play with ecosystem and retail momentum.",
            "key_insight": "Offers higher upside potential, but carries elevated execution and sentiment risk.",
            "expected_return": 24,
            "risk_level": "High",
            "volatility": "High",
            "confidence": 0.64,
            "short_term": "Strong upside in momentum phases, weak in risk-off periods.",
            "long_term": "Potentially strong, but less predictable than larger networks.",
            "recommendation": "Monitor",
            "risks": [
                "Sentiment reversals",
                "Ecosystem concentration",
                "Execution / reliability concerns",
            ],
        },
    },
    "Stocks": {
        "Nasdaq 100": {
            "market": "Stocks",
            "opportunity": "Growth-heavy equity exposure tied to technology leadership.",
            "key_insight": "Benefits from AI enthusiasm and earnings growth, but valuation sensitivity matters.",
            "expected_return": 12,
            "risk_level": "Medium",
            "volatility": "Medium",
            "confidence": 0.78,
            "short_term": "Positive if earnings and risk appetite stay supportive.",
            "long_term": "Strong structural theme driven by innovation and AI spending.",
            "recommendation": "Invest",
            "risks": [
                "Valuation compression",
                "Rates remaining higher for longer",
                "Concentration in mega-cap names",
            ],
        },
        "S&P 500": {
            "market": "Stocks",
            "opportunity": "Broad US equity exposure with diversified sector participation.",
            "key_insight": "More balanced than pure tech exposure and useful as a core allocation.",
            "expected_return": 9,
            "risk_level": "Medium",
            "volatility": "Medium",
            "confidence": 0.82,
            "short_term": "Stable unless macro data deteriorates sharply.",
            "long_term": "Constructive for diversified long-term investors.",
            "recommendation": "Invest",
            "risks": [
                "Economic slowdown",
                "Earnings disappointments",
                "Policy or rate shocks",
            ],
        },
        "Goldman Sachs Tech Basket": {
            "market": "Stocks",
            "opportunity": "Higher-growth equity basket with stronger upside than broad index exposure.",
            "key_insight": "Works well in bullish growth environments but carries higher valuation risk.",
            "expected_return": 14,
            "risk_level": "Medium",
            "volatility": "High",
            "confidence": 0.69,
            "short_term": "Potentially strong if tech leadership persists.",
            "long_term": "Attractive but cyclical and valuation-sensitive.",
            "recommendation": "Monitor",
            "risks": [
                "Growth-stock drawdowns",
                "Crowded positioning",
                "Rate-sensitive multiples",
            ],
        },
    },
    "Forex": {
        "USD/JPY": {
            "market": "Forex",
            "opportunity": "Policy divergence trade sensitive to interest-rate expectations.",
            "key_insight": "Moves sharply when central bank expectations change.",
            "expected_return": 7,
            "risk_level": "Medium",
            "volatility": "Medium",
            "confidence": 0.67,
            "short_term": "Tradable on macro and policy events.",
            "long_term": "Dependent on yield differentials and intervention risk.",
            "recommendation": "Monitor",
            "risks": [
                "Central bank intervention",
                "Policy surprises",
                "Fast intraday reversals",
            ],
        },
        "EUR/USD": {
            "market": "Forex",
            "opportunity": "Major FX pair useful for lower-beta macro exposure.",
            "key_insight": "Highly liquid, but upside is usually more moderate than crypto or growth stocks.",
            "expected_return": 5,
            "risk_level": "Low",
            "volatility": "Low",
            "confidence": 0.76,
            "short_term": "Range-bound unless macro divergence widens.",
            "long_term": "Best suited to disciplined macro positioning.",
            "recommendation": "Monitor",
            "risks": [
                "Unexpected inflation / rate shifts",
                "Political shocks",
                "Lower return profile",
            ],
        },
    },
    "Commodities": {
        "Gold": {
            "market": "Commodities",
            "opportunity": "Defensive asset with safe-haven characteristics.",
            "key_insight": "Useful during uncertainty, inflation concerns, and periods of weaker real yields.",
            "expected_return": 8,
            "risk_level": "Low",
            "volatility": "Low",
            "confidence": 0.84,
            "short_term": "Supportive if uncertainty remains elevated.",
            "long_term": "Solid diversification asset rather than aggressive growth play.",
            "recommendation": "Invest",
            "risks": [
                "Stronger real yields",
                "USD strength",
                "Lower upside than high-beta assets",
            ],
        },
        "Crude Oil": {
            "market": "Commodities",
            "opportunity": "Macro-sensitive commodity tied to supply, demand, and geopolitics.",
            "key_insight": "Can generate strong tactical moves but is vulnerable to sharp reversals.",
            "expected_return": 11,
            "risk_level": "High",
            "volatility": "High",
            "confidence": 0.61,
            "short_term": "Event-driven and highly tactical.",
            "long_term": "Useful only for selective exposure, not stable core allocation.",
            "recommendation": "Avoid",
            "risks": [
                "Geopolitical headline risk",
                "Demand slowdowns",
                "Sudden price collapses",
            ],
        },
    },
}

RISK_MAP = {"Low": 20, "Medium": 50, "High": 80}
VOL_MAP = {"Low": 20, "Medium": 50, "High": 80}
MODE_RULES = {
    "Balanced": {"return_boost": 0, "risk_penalty": 0, "cash_weight": 10},
    "Aggressive": {"return_boost": 10, "risk_penalty": -8, "cash_weight": 5},
    "Conservative": {"return_boost": -5, "risk_penalty": 8, "cash_weight": 18},
}


def normalize_return(expected_return: float) -> float:
    return max(0, min(100, expected_return * 4))



def compute_ai_score(expected_return: float, confidence: float, risk_level: str, volatility: str, mode: str) -> int:
    normalized_return = normalize_return(expected_return)
    confidence_100 = confidence * 100
    risk_value = RISK_MAP[risk_level]
    vol_value = VOL_MAP[volatility]
    rule = MODE_RULES[mode]

    score = (
        (normalized_return + rule["return_boost"]) * 0.4
        + confidence_100 * 0.3
        - (risk_value + rule["risk_penalty"]) * 0.2
        - vol_value * 0.1
    )
    return max(0, min(100, int(round(score))))



def score_label(score: int) -> str:
    if score >= 80:
        return "Strong Opportunity"
    if score >= 60:
        return "Good Opportunity"
    if score >= 40:
        return "Moderate"
    return "Weak / Avoid"



def recommendation_from_score(score: int) -> str:
    if score >= 70:
        return "Invest"
    if score >= 45:
        return "Monitor"
    return "Avoid"



def enrich_asset(asset_name: str, market: str, mode: str) -> Dict[str, object]:
    item = ASSET_DATA[market][asset_name].copy()
    score = compute_ai_score(
        expected_return=float(item["expected_return"]),
        confidence=float(item["confidence"]),
        risk_level=str(item["risk_level"]),
        volatility=str(item["volatility"]),
        mode=mode,
    )
    item["asset"] = asset_name
    item["ai_score"] = score
    item["verdict"] = score_label(score)
    item["recommendation"] = recommendation_from_score(score)
    return item



def find_market_from_asset(asset_name: str) -> str:
    for market, assets in ASSET_DATA.items():
        if asset_name in assets:
            return market
    raise KeyError(f"Unknown asset: {asset_name}")



def generate_portfolio(mode: str) -> pd.DataFrame:
    candidates = []
    for market, assets in ASSET_DATA.items():
        for asset_name in assets:
            candidates.append(enrich_asset(asset_name, market, mode))
    ranked = sorted(candidates, key=lambda x: x["ai_score"], reverse=True)

    if mode == "Aggressive":
        chosen_names = ["Nasdaq 100", "Bitcoin", "Ethereum", "Gold"]
    elif mode == "Conservative":
        chosen_names = ["S&P 500", "Gold", "EUR/USD", "Nasdaq 100"]
    else:
        chosen_names = ["S&P 500", "Nasdaq 100", "Gold", "Bitcoin"]

    chosen = [enrich_asset(name, find_market_from_asset(name), mode) for name in chosen_names]

    if mode == "Aggressive":
        alloc = [35, 30, 20, 10]
        cash = 5
    elif mode == "Conservative":
        alloc = [30, 28, 24, 0]
        cash = 18
    else:
        alloc = [32, 28, 20, 10]
        cash = 10

    rows = []
    for entry, weight in zip(chosen, alloc):
        if weight > 0:
            rows.append(
                {
                    "Asset": entry["asset"],
                    "Market": entry["market"],
                    "Allocation %": weight,
                    "AI Score": entry["ai_score"],
                    "Risk": entry["risk_level"],
                    "Reason": entry["key_insight"],
                }
            )
    rows.append(
        {
            "Asset": "Cash / Reserve",
            "Market": "Liquidity",
            "Allocation %": cash,
            "AI Score": "—",
            "Risk": "Low",
            "Reason": "Reserve capital for flexibility and drawdown control.",
        }
    )
    return pd.DataFrame(rows)



def render_analysis_card(item: Dict[str, object]) -> None:
    st.markdown("### Structured Analysis")
    st.markdown(f"**Market:** {item['market']}")
    st.markdown(f"**Opportunity:** {item['opportunity']}")
    st.markdown(f"**Key Insight:** {item['key_insight']}")
    st.markdown(f"**Expected Return:** {item['expected_return']}%")
    st.markdown(f"**Risk Level:** {item['risk_level']}")
    st.markdown(f"**Volatility:** {item['volatility']}")
    st.markdown(f"**Confidence Score:** {item['confidence']:.2f}")
    st.markdown(f"**AI Score:** {item['ai_score']} ({item['verdict']})")
    st.markdown(f"**Short-Term Outlook:** {item['short_term']}")
    st.markdown(f"**Long-Term Outlook:** {item['long_term']}")
    st.markdown(f"**Recommendation:** {item['recommendation']}")
    st.markdown(
        "**Reasoning:** "
        + f"This demo combines expected return, confidence, risk, and volatility for a {item['recommendation'].lower()} verdict in {item['market'].lower()}."
    )
    st.markdown("**Risks:**")
    for risk in item["risks"]:
        st.markdown(f"- {risk}")


st.title("📈 Global Market Intelligence Assistant")
st.caption("Demo-ready Streamlit project for GitHub + Streamlit Community Cloud deployment.")

with st.sidebar:
    st.header("Controls")
    investor_mode = st.selectbox("Investor Mode", ["Balanced", "Aggressive", "Conservative"], index=0)
    market_choice = st.selectbox("Primary Market", list(ASSET_DATA.keys()), index=0)
    asset_choice = st.selectbox("Asset", list(ASSET_DATA[market_choice].keys()), index=0)
    st.markdown("---")
    st.info(
        "This demo uses built-in sample market intelligence data. "
        "You can replace it later with live APIs."
    )

col1, col2 = st.columns([1.4, 1])
with col1:
    user_question = st.text_area(
        "Ask a market question",
        value=f"Analyze {asset_choice} for a {investor_mode.lower()} investor.",
        height=110,
    )
with col2:
    st.markdown("### Project Mode")
    st.write("- Demo-ready")
    st.write("- No paid APIs required")
    st.write("- GitHub + Streamlit compatible")
    st.write("- Client preview friendly")

analyze_tab, compare_tab, portfolio_tab, about_tab = st.tabs([
    "Single Analysis",
    "Comparison",
    "Portfolio",
    "About",
])

with analyze_tab:
    if st.button("Run Analysis", use_container_width=True):
        item = enrich_asset(asset_choice, market_choice, investor_mode)
        st.success(f"Analysis generated for: {asset_choice}")
        render_analysis_card(item)

with compare_tab:
    assets_for_market = list(ASSET_DATA[market_choice].keys())
    default_assets = assets_for_market[: min(3, len(assets_for_market))]
    compare_assets = st.multiselect(
        "Select assets to compare",
        assets_for_market,
        default=default_assets,
        max_selections=3,
        key="compare_assets",
    )
    if st.button("Compare Opportunities", use_container_width=True):
        if len(compare_assets) < 2:
            st.warning("Please select at least 2 assets.")
        else:
            rows: List[Dict[str, object]] = []
            for asset in compare_assets:
                item = enrich_asset(asset, market_choice, investor_mode)
                rows.append(
                    {
                        "Asset": asset,
                        "Return %": item["expected_return"],
                        "Risk": item["risk_level"],
                        "Confidence": round(float(item["confidence"]), 2),
                        "AI Score": item["ai_score"],
                        "Verdict": item["verdict"],
                    }
                )
            df = pd.DataFrame(rows).sort_values(by="AI Score", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
            best = df.iloc[0]
            st.success(f"👉 Best Option: {best['Asset']} (AI Score: {best['AI Score']})")

with portfolio_tab:
    st.markdown("### Suggested Portfolio")
    st.write(f"Mode selected: **{investor_mode}**")
    portfolio_df = generate_portfolio(investor_mode)
    st.dataframe(portfolio_df, use_container_width=True, hide_index=True)
    st.markdown("#### Allocation Reasoning")
    if investor_mode == "Aggressive":
        st.write("Higher exposure to growth assets with a small cash reserve for flexibility.")
    elif investor_mode == "Conservative":
        st.write("Focus on stability, diversification, and stronger capital preservation.")
    else:
        st.write("Balanced exposure across equities, commodities, and selective crypto risk.")

with about_tab:
    st.markdown("### System Prompt Summary")
    st.code(SYSTEM_PROMPT)
    st.markdown("### Notes")
    st.markdown(
        "- This app is a **demo MVP** for client presentation.\n"
        "- It uses **sample data**, not live market feeds.\n"
        "- You can later connect free or paid APIs for real market data.\n"
        "- Streamlit Community Cloud can deploy this app directly from GitHub."
    )
    st.markdown("### Suggested Next Upgrade")
    st.markdown(
        "1. Add live crypto/stocks/news APIs.\n"
        "2. Save chat history and signals.\n"
        "3. Add charts and market heatmaps.\n"
        "4. Plug into an LLM backend for natural-language reasoning."
    )
