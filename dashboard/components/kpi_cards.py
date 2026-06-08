import streamlit as st

# Inject once at module level — ensures styles are always present
_CSS_INJECTED = False

def _inject_styles():
    global _CSS_INJECTED
    if not _CSS_INJECTED:
        st.markdown("""
            <style>
            /* Fix: Streamlit wraps markdown in <p> which blocks div rendering */
            [data-testid="stMarkdownContainer"] p {
                margin: 0;
                padding: 0;
            }
            [data-testid="stMarkdownContainer"] > div {
                display: block;
            }
            .metric-card {
                background: rgba(26, 16, 53, .95);
                backdrop-filter: blur(12px);
                border-radius: 18px;
                padding: 22px;
                border: 1px solid rgba(255, 255, 255, .08);
                min-height: 140px;
                transition: .2s;
                text-align: center;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                border: 1px solid rgba(0, 255, 135, .35);
            }
            .metric-title {
                color: #B0B0B0;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .metric-value {
                font-size: 36px;
                font-weight: 700;
                margin-top: 10px;
            }
            .metric-delta {
                color: #00FF87;
                margin-top: 12px;
                font-size: 14px;
            }
            </style>
        """, unsafe_allow_html=True)
        _CSS_INJECTED = True


def render_kpi(title, value, delta=""):
    _inject_styles()

    color = "#FFFFFF"

    if title == "Status":
        color = "#00FF87" if str(value) == "200" else "#FF4D4D"

    elif title == "Load Time":
        try:
            v = float(str(value).replace("s", ""))
            color = "#00FF87" if v <= 2 else "#FFB800" if v <= 4 else "#FF4D4D"
        except:
            pass

    elif title == "QR Ready":
        try:
            v = float(str(value).replace("s", ""))
            color = "#00FF87" if v <= 4 else "#FFB800" if v <= 7 else "#FF4D4D"
        except:
            pass

    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value" style="color:{color};">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>""",
        unsafe_allow_html=True
    )