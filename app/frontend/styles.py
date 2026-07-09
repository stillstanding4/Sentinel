from __future__ import annotations

import streamlit as st


def apply_enterprise_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --sentinel-ink: #101828;
            --sentinel-muted: #667085;
            --sentinel-line: #d0d7e2;
            --sentinel-panel: #ffffff;
            --sentinel-bg: #f4f7fb;
            --sentinel-teal: #0f766e;
            --sentinel-blue: #1d4ed8;
            --sentinel-red: #b42318;
            --sentinel-amber: #b54708;
            --sentinel-green: #067647;
            --sentinel-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }
        .stApp {
            background: var(--sentinel-bg);
            color: var(--sentinel-ink);
        }
        section[data-testid="stSidebar"] {
            background: #0f172a;
            border-right: 1px solid #1e293b;
        }
        section[data-testid="stSidebar"] * {
            color: #eef2ff;
        }
        section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
            color: #e2e8f0;
        }
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2.25rem;
            max-width: 1440px;
        }
        .hero-shell {
            border: 1px solid var(--sentinel-line);
            background: #ffffff;
            padding: 24px 28px;
            margin-bottom: 20px;
            box-shadow: var(--sentinel-shadow);
        }
        .hero-title {
            font-size: 30px;
            line-height: 1.15;
            font-weight: 760;
            color: var(--sentinel-ink);
        }
        .hero-subtitle {
            color: var(--sentinel-muted);
            font-size: 15px;
            margin-top: 4px;
        }
        .metric-card {
            background: var(--sentinel-panel);
            border: 1px solid var(--sentinel-line);
            border-left: 5px solid #64748b;
            padding: 17px 18px 15px;
            min-height: 128px;
            box-shadow: var(--sentinel-shadow);
        }
        .metric-good { border-left-color: var(--sentinel-green); }
        .metric-watch { border-left-color: var(--sentinel-amber); }
        .metric-risk { border-left-color: var(--sentinel-red); }
        .metric-neutral { border-left-color: var(--sentinel-blue); }
        .metric-label {
            color: var(--sentinel-muted);
            font-size: 12px;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0;
            display: flex;
            align-items: center;
            gap: 7px;
        }
        .metric-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: var(--sentinel-blue);
            border: 1px solid rgba(15, 23, 42, 0.12);
        }
        .metric-good .metric-dot { background: var(--sentinel-green); }
        .metric-watch .metric-dot { background: var(--sentinel-amber); }
        .metric-risk .metric-dot { background: var(--sentinel-red); }
        .metric-neutral .metric-dot { background: var(--sentinel-blue); }
        }
        .metric-value {
            color: var(--sentinel-ink);
            font-size: 27px;
            line-height: 1.2;
            font-weight: 780;
            margin-top: 8px;
            overflow-wrap: anywhere;
        }
        .metric-detail {
            color: var(--sentinel-muted);
            font-size: 13px;
            margin-top: 6px;
        }
        .section-title {
            font-size: 18px;
            font-weight: 740;
            color: var(--sentinel-ink);
            margin: 0;
        }
        .section-subtitle {
            color: var(--sentinel-muted);
            font-size: 13px;
            margin-top: 4px;
        }
        .section-divider {
            border-top: 1px solid var(--sentinel-line);
            padding-top: 16px;
            margin: 22px 0 12px;
        }
        .page-header {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            padding: 22px 24px;
            margin-bottom: 18px;
            box-shadow: var(--sentinel-shadow);
        }
        .page-eyebrow {
            color: var(--sentinel-teal);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0;
        }
        .page-title {
            color: var(--sentinel-ink);
            font-size: 29px;
            line-height: 1.15;
            font-weight: 780;
            margin-top: 4px;
        }
        .page-subtitle {
            color: var(--sentinel-muted);
            font-size: 15px;
            margin-top: 8px;
            max-width: 960px;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 9px;
            font-size: 12px;
            font-weight: 700;
            border: 1px solid var(--sentinel-line);
            background: #eef2ff;
            color: #1e40af;
        }
        .status-fail, .status-critical, .status-at-risk {
            background: #fee2e2;
            color: #991b1b;
            border-color: #fecaca;
        }
        .status-warn, .status-needs-review, .status-watch, .status-medium {
            background: #fef3c7;
            color: #92400e;
            border-color: #fde68a;
        }
        .status-pass, .status-approve, .status-trusted, .status-low {
            background: #dcfce7;
            color: #166534;
            border-color: #bbf7d0;
        }
        .audit-step {
            border-left: 3px solid var(--sentinel-teal);
            padding: 7px 0 7px 12px;
            margin-bottom: 4px;
            background: #f8fafc;
        }
        .executive-panel {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            padding: 18px;
            margin: 10px 0 16px;
            box-shadow: var(--sentinel-shadow);
        }
        .executive-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
        }
        .executive-item {
            border-left: 4px solid var(--sentinel-blue);
            background: #f8fafc;
            padding: 13px;
            min-height: 96px;
        }
        .executive-item-risk-critical { border-left-color: var(--sentinel-red); }
        .executive-item-risk-high { border-left-color: #ea580c; }
        .executive-item-risk-medium { border-left-color: var(--sentinel-amber); }
        .executive-item-risk-low { border-left-color: var(--sentinel-green); }
        .executive-label {
            color: var(--sentinel-muted);
            font-size: 11px;
            font-weight: 760;
            text-transform: uppercase;
        }
        .executive-value {
            color: var(--sentinel-ink);
            font-size: 14px;
            font-weight: 680;
            margin-top: 6px;
        }
        .recommendation-card {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            border-left: 5px solid var(--sentinel-blue);
            padding: 16px 18px;
            margin-bottom: 12px;
            box-shadow: var(--sentinel-shadow);
        }
        .recommendation-card-critical { border-left-color: var(--sentinel-red); }
        .recommendation-card-high { border-left-color: #ea580c; }
        .recommendation-card-medium { border-left-color: var(--sentinel-amber); }
        .recommendation-card-low { border-left-color: var(--sentinel-green); }
        .recommendation-title {
            font-size: 17px;
            font-weight: 760;
            color: var(--sentinel-ink);
            margin-bottom: 9px;
        }
        .recommendation-row {
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 12px;
            padding: 5px 0;
            border-top: 1px solid #edf2f7;
        }
        .recommendation-key {
            color: var(--sentinel-muted);
            font-size: 12px;
            font-weight: 740;
            text-transform: uppercase;
        }
        .recommendation-value {
            color: var(--sentinel-ink);
            font-size: 13px;
        }
        .timeline-row {
            display: grid;
            grid-template-columns: 180px 24px 1fr;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }
        .timeline-dot {
            height: 12px;
            width: 12px;
            background: var(--sentinel-teal);
            border: 2px solid #ccfbf1;
        }
        .timeline-event {
            font-weight: 720;
            color: var(--sentinel-ink);
        }
        .timeline-time {
            color: var(--sentinel-muted);
            font-size: 13px;
        }
        @media (max-width: 900px) {
            .executive-grid {
                grid-template-columns: 1fr;
            }
            .recommendation-row {
                grid-template-columns: 1fr;
            }
            .timeline-row {
                grid-template-columns: 1fr;
            }
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            padding: 14px 16px;
            box-shadow: var(--sentinel-shadow);
        }
        .empty-state {
            background: #ffffff;
            border: 1px dashed var(--sentinel-line);
            padding: 18px;
            color: var(--sentinel-muted);
        }
        .empty-state-title {
            color: var(--sentinel-ink);
            font-size: 15px;
            font-weight: 760;
        }
        .empty-state-message {
            margin-top: 5px;
            font-size: 13px;
        }
        .sidebar-panel {
            border: 1px solid #334155;
            background: #111c30;
            padding: 13px;
            margin-top: 12px;
        }
        .sidebar-panel-title {
            font-size: 13px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
        }
        .sidebar-step {
            border-top: 1px solid #253349;
            padding-top: 8px;
            margin-top: 8px;
        }
        .sidebar-step-name {
            font-size: 12px;
            font-weight: 760;
            color: #f8fafc;
        }
        .sidebar-step-text {
            font-size: 12px;
            color: #cbd5e1;
            margin-top: 2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
