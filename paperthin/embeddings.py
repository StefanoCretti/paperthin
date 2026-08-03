import io

import polars as pl
from matplotlib import figure

PNG_DPI = 300


def svg_plot_string(fig: figure.Figure) -> str:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="svg", bbox_inches="tight")
    return buffer.getvalue().decode("utf-8")


def png_plot_bytes(fig: figure.Figure) -> bytes:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=PNG_DPI)
    return buffer.getvalue()


def df_to_tsv(df: pl.DataFrame) -> str:
    return df.write_csv(separator="\t")


def df_to_csv(df: pl.DataFrame) -> str:
    return df.write_csv(separator=",")
