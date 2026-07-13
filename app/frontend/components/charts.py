from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.frontend.components.trust_scores import trust_score_state


COLOR_SEQUENCE = ["#0f766e", "#2563eb", "#dc2626", "#9333ea", "#ea580c", "#475569"]


def trust_score_gauge(score: int) -> go.Figure:
    state = trust_score_state(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"font": {"size": 38, "color": state["color"]}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": state["color"]},
                "steps": [
                    {"range": [0, 59], "color": "#fee2e2"},
                    {"range": [60, 74], "color": "#ffedd5"},
                    {"range": [75, 89], "color": "#fef3c7"},
                    {"range": [90, 100], "color": "#dcfce7"},
                ],
                "threshold": {"line": {"color": "#111827", "width": 3}, "value": score},
            },
        )
    )
    fig.add_annotation(
        text=state["label"],
        x=0.5,
        y=0.08,
        showarrow=False,
        font={"size": 14, "color": state["color"]},
    )
    fig.update_layout(height=260, margin=dict(l=24, r=24, t=24, b=12))
    return fig


def score_history(scores: list[dict]) -> go.Figure:
    if not scores:
        return empty_chart("No Trust Score data yet")
    frame = pd.DataFrame(scores)
    fig = px.line(
        frame,
        x="created_at",
        y="overall_score",
        color="agent_name",
        markers=True,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"created_at": "Run", "overall_score": "Trust Score", "agent_name": "Agent"},
    )
    fig.update_layout(height=330, margin=dict(l=12, r=12, t=24, b=12), legend_title_text="")
    return fig


def bar_chart(data: dict[str, int], title: str) -> go.Figure:
    if not data:
        return empty_chart("No data yet")
    frame = pd.DataFrame({"label": list(data.keys()), "value": list(data.values())})
    fig = px.bar(
        frame,
        x="label",
        y="value",
        color="label",
        color_discrete_sequence=COLOR_SEQUENCE,
        title=title,
    )
    fig.update_layout(height=320, showlegend=False, margin=dict(l=12, r=12, t=48, b=12))
    return fig


def empty_chart(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, x=0.5, y=0.5)
    fig.update_layout(height=260, margin=dict(l=12, r=12, t=24, b=12))
    return fig
