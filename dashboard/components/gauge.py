import streamlit as st
import streamlit.components.v1 as components


def get_score_status(score):
    if score >= 90: return "Excellent"
    if score >= 75: return "Good"
    if score >= 60: return "Needs Improvement"
    return "Poor"


def get_score_color(score):
    if score >= 90: return "#00FF87"
    if score >= 75: return "#05F0FF"
    if score >= 60: return "#FFB800"
    return "#FF4D4D"


def render_gauge(score):
    status = get_score_status(score)
    color = get_score_color(score)

    components.html(f"""
        <style>
            body {{ margin: 0; background: transparent; }}
            .gauge-card {{
                background: #1A1035;
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                border: 1px solid rgba(255,255,255,.08);
                font-family: sans-serif;
            }}
            .gauge-label {{
                font-size: 18px;
                color: #AAAAAA;
                margin-bottom: 20px;
            }}
            .gauge-score {{
                font-size: 72px;
                font-weight: 700;
                color: {color};
                line-height: 1;
            }}
            .gauge-status {{
                margin-top: 15px;
                font-size: 24px;
                font-weight: 600;
                color: {color};
            }}
        </style>
        <div class="gauge-card">
            <div class="gauge-label">Performance Score</div>
            <div class="gauge-score">{score}</div>
            <div class="gauge-status">{status}</div>
        </div>
    """, height=220)