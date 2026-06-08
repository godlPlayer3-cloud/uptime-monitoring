import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd

from storage.repository import RunRepository

from components.gauge import render_gauge
from components.kpi_cards import render_kpi
from components.trend_chart import render_trend
from components.agent_status import render_agent_status
from components.vitals import render_vitals


st.set_page_config(
    layout="wide",
    page_title="Premier League+ Monitor"
)

css = (
    Path(__file__).parent /
    "assets" /
    "styles.css"
).read_text()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

repo = RunRepository()

latest = repo.latest()

st.markdown(
    """
    <div class='hero-title'>
        ⚽ Premier League+ Monitoring Center
    </div>
    """,
    unsafe_allow_html=True
)

if not latest:

    st.warning(
        "No monitoring data found"
    )

    st.stop()

#
# Score
#
score = max(
    0,
    100
    - int(latest.load_time * 8)
    - int(latest.ttfb / 100)
)

#
# Sidebar
#
with st.sidebar:

    st.markdown(
        "## ⚽ PL+ Monitor"
    )

    st.markdown("---")

    st.markdown(
        f"""
        **Location**

        {latest.location}
        """
    )

    st.markdown("---")

    st.markdown("Overview")
    st.markdown("Performance")
    st.markdown("Core Web Vitals")
    st.markdown("Screenshots")
    st.markdown("History")
    st.markdown("Settings")

#
# Hero Row
#
hero1, hero2 = st.columns(
    [1, 2]
)

with hero1:

    render_gauge(
        score
    )

    render_agent_status(
    latest.location,
    "India-Agent-01"
)

with hero2:

    st.markdown(
        "### Latest Browser Screenshot"
    )

    try:

        st.image(
            latest.screenshot,
            use_container_width=True
        )

    except:

        st.info(
            "Screenshot not available"
        )

#
# KPI Row
#
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:

    render_kpi(
        "Load Time",
        f"{latest.load_time}s",
        ""
    )

with c2:

    render_kpi(
        "QR Ready",
        f"{latest.qr_ready_time}s",
        ""
    )

with c3:

    render_kpi(
        "TTFB",
        f"{latest.ttfb}ms",
        ""
    )

with c4:

    render_kpi(
        "LCP",
        f"{latest.lcp}s",
        ""
    )

with c5:

    render_kpi(
        "Requests",
        latest.requests,
        ""
    )

with c6:

    render_kpi(
        "Status",
        latest.status_code,
        "Healthy"
    )

#
# History
#
hist = repo.history(100)

df = pd.DataFrame([
    {
        "time": r.timestamp,
        "load": r.load_time,
        "qr": r.qr_ready_time,
        "ttfb": r.ttfb
    }
    for r in hist
])

#
# Trend
#
st.markdown(
    "### Performance Trend"
)

render_trend(df)

#
# Core Web Vitals
#
st.markdown(
    "### Core Web Vitals"
)

render_vitals(
    latest
)

#
# Recent Runs
#
st.markdown(
    "### Recent Runs"
)

st.dataframe(
    df.tail(20),
    use_container_width=True
)