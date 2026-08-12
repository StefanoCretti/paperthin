import io
from html import escape

import polars as pl
from matplotlib import figure

PNG_DPI = 300


def svg_plot_string(fig: figure.Figure) -> bytes:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="svg", bbox_inches="tight")
    return buffer.getvalue()


def png_plot_bytes(fig: figure.Figure) -> bytes:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=PNG_DPI)
    return buffer.getvalue()


def df_to_html(df: pl.DataFrame) -> str:
    header = "".join(f"<th>{escape(str(col))}</th>" for col in df.columns)
    rows = "".join(
        "<tr>" + "".join(f"<td>{escape(str(value))}</td>" for value in row) + "</tr>"
        for row in df.iter_rows()
    )
    return f'<table class="dataframe"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table>'


def value_to_html(value: str | float) -> str:
    return escape(str(value))


def df_to_tsv(df: pl.DataFrame) -> bytes:
    return df.write_csv(separator="\t").encode("utf-8")


def df_to_csv(df: pl.DataFrame) -> bytes:
    return df.write_csv(separator=",").encode("utf-8")
