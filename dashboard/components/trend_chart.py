import streamlit as st
import plotly.graph_objects as go


def render_trend(df):

    if len(df) == 0:
        st.warning(
            "No trend data available"
        )
        return

    #
    # Moving averages
    #
    if len(df) > 5:

        df["load_ma"] = (
            df["load"]
            .rolling(5)
            .mean()
        )

        df["qr_ma"] = (
            df["qr"]
            .rolling(5)
            .mean()
        )

    else:

        df["load_ma"] = df["load"]

        if "qr" in df.columns:
            df["qr_ma"] = df["qr"]

    fig = go.Figure()

    #
    # Load Time
    #
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["load_ma"],
            mode="lines",
            name="Load Time",
            line=dict(
                width=3,
                color="#00FF87"
            )
        )
    )

    #
    # QR Ready Time
    #
    if "qr" in df.columns:

        fig.add_trace(
            go.Scatter(
                x=df["time"],
                y=df["qr_ma"],
                mode="lines",
                name="QR Ready Time",
                line=dict(
                    width=3,
                    color="#05F0FF"
                )
            )
        )

    fig.update_layout(

        title="Performance Trend",

        paper_bgcolor="#0D001F",

        plot_bgcolor="#1A1035",

        font_color="white",

        height=450,

        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        title="Seconds",
        gridcolor="rgba(255,255,255,0.08)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )