import plotly.graph_objects as go
import plotly.express as px

# Shared layout defaults (white theme)
CHART_LAYOUT = dict(
    font=dict(family="Inter, -apple-system, sans-serif", color="#1a1a2e"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor="#e5e7eb", gridwidth=0.5),
    yaxis=dict(gridcolor="#e5e7eb", gridwidth=0.5),
)

COLORS = {
    "primary": "#667eea",
    "accent": "#06d6a0",
    "danger": "#e63946",
    "warning": "#fb8500",
    "secondary": "#764ba2",
    "muted": "#6b7280",
}


def countryness_over_time(df):
    """Area chart: avg countryness by year (1997-2023)."""
    avg = df.groupby("year")["countryness"].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=avg["year"],
            y=avg["countryness"],
            mode="lines",
            fill="tozeroy",
            line=dict(color=COLORS["primary"], width=2.5),
            fillcolor="rgba(102, 126, 234, 0.12)",
            hovertemplate="%{x}: Avg countryness %{y:.1f}<extra></extra>",
        )
    )
    fig.update_layout(
        **CHART_LAYOUT,
        title=None,
        xaxis_title="Year",
        yaxis_title="Avg Countryness Score",
        height=380,
    )
    return fig
