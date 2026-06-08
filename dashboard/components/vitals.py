import streamlit as st


def get_status(metric, value):

    if metric == "LCP":

        if value <= 2.5:
            return "Good"

        elif value <= 4:
            return "Needs Improvement"

        return "Poor"

    if metric == "FCP":

        if value <= 1.8:
            return "Good"

        elif value <= 3:
            return "Needs Improvement"

        return "Poor"

    if metric == "CLS":

        if value <= 0.1:
            return "Good"

        elif value <= 0.25:
            return "Needs Improvement"

        return "Poor"

    return ""


def render_vitals(latest):

    c1, c2, c3 = st.columns(3)

    lcp_status = get_status(
        "LCP",
        latest.lcp
    )

    fcp_status = get_status(
        "FCP",
        latest.fcp
    )

    cls_status = get_status(
        "CLS",
        latest.cls
    )

    c1.metric(
        "LCP",
        f"{latest.lcp}s",
        lcp_status
    )

    c2.metric(
        "FCP",
        f"{latest.fcp}s",
        fcp_status
    )

    c3.metric(
        "CLS",
        latest.cls,
        cls_status
    )