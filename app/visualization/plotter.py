import pandas as pd
import plotly.express as px


def plot_chart(columns, rows):

    df = pd.DataFrame(rows, columns=columns)

    if len(columns) < 2:
        return None

    x = columns[0]
    y = columns[1]

    # detect chart type
    if "date" in x.lower() or "time" in x.lower():
        fig = px.line(df, x=x, y=y, markers=True, title=f"{y} over {x}")

    elif df[y].nunique() < 10:
        fig = px.pie(df, names=x, values=y, title=f"{y} Distribution")

    else:
        fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    return fig
