import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        /* ----------------------------------------------------------------------- */
        /* Title */

        .block-container {
            padding-left: 17rem;
            padding-right: 17rem;
        }

        .stock-title {
            margin-top: -5px !important;
            padding: 0 !important;
        }

        #exchange-caption {
            margin: 0;
            padding: 0;
            color: #9D9E9D;
        }

        /* ----------------------------------------------------------------------- */
        /* News */

        .news_article {
            margin-bottom: 0.9rem;
        }

        .news_article_link {
            text-decoration: none;
        }

        .news_article_publisher {
            color: #9aa0a6;
            font-size: 0.8rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def percent_badge(value, tooltip="Daily Change"):
    """
    Returns a green percentage badge with a hover tooltip.
    """
    arrow = "▲" if value >= 0 else "▼"
    bg = "#123d2a" if value >= 0 else "#3d1212"
    color = "#7CFFB2" if value >= 0 else "#FF7C7C"

    return f"""
    <span
        title="{tooltip}"
        style="
            display:inline-block;
            padding:0.25rem 0.6rem;
            border-radius:999px;
            background:{bg};
            color:{color};
            font-weight:600;
            font-size:0.85rem;
            cursor: help;
        ">
        {arrow} {value:.2f}%
    </span>
    """