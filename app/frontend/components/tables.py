from __future__ import annotations

import pandas as pd
import streamlit as st

from app.frontend.components.layout import empty_state


def dataframe(records: list[dict], columns: list[str] | None = None) -> None:
    if not records:
        empty_state("No records available", "Sentinel will populate this section after Demo Mode or Live Agent Audit activity.")
        return
    frame = pd.DataFrame(records)
    if columns:
        visible = [column for column in columns if column in frame.columns]
        frame = frame[visible]
    st.dataframe(frame, width="stretch", hide_index=True)
