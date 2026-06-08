import streamlit.components.v1 as components
from datetime import datetime


def render_agent_status(
    location="India",
    agent_name="India-Agent-01"
):
    now = datetime.now().strftime("%H:%M:%S")

    components.html(f"""
        <style>
            body {{ margin: 0; background: transparent; }}
            .agent-card {{
                background: #1A1035;
                border-radius: 18px;
                padding: 20px;
                border: 1px solid rgba(255,255,255,.08);
                margin-top: 10px;
                font-family: sans-serif;
            }}
            .agent-card h4 {{
                color: #00FF87;
                margin: 0 0 15px 0;
                font-size: 16px;
            }}
            .agent-card p {{
                color: white;
                margin: 6px 0;
                font-size: 14px;
            }}
            .agent-healthy {{
                color: #00FF87;
                font-weight: bold;
                margin-top: 10px;
            }}
        </style>
        <div class="agent-card">
            <h4>Agent Health</h4>
            <p><b>Agent:</b> {agent_name}</p>
            <p><b>Location:</b> {location}</p>
            <p><b>Last Seen:</b> {now}</p>
            <p class="agent-healthy">● Healthy</p>
        </div>
    """, height=200)