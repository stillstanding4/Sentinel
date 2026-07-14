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
            --sentinel-shadow: 0 10px 24px rgba(15, 23, 42, 0.055);
            --sentinel-soft-shadow: 0 6px 16px rgba(15, 23, 42, 0.04);
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
            padding-top: 1rem;
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
            padding: 15px 16px 14px;
            min-height: 108px;
            box-shadow: var(--sentinel-soft-shadow);
        }
        .metric-good { border-left-color: var(--sentinel-green); }
        .metric-watch { border-left-color: var(--sentinel-amber); }
        .metric-high-risk { border-left-color: #ea580c; }
        .metric-critical { border-left-color: var(--sentinel-red); }
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
        .metric-high-risk .metric-dot { background: #ea580c; }
        .metric-critical .metric-dot { background: var(--sentinel-red); }
        .metric-risk .metric-dot { background: var(--sentinel-red); }
        .metric-neutral .metric-dot { background: var(--sentinel-blue); }
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
            padding-top: 14px;
            margin: 18px 0 10px;
        }
        .page-header {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            padding: 34px 40px;
            margin-bottom: 24px;
            min-height: 158px;
            box-shadow: var(--sentinel-soft-shadow);
            border-radius: 8px;
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
            font-size: 38px;
            line-height: 1.12;
            font-weight: 800;
            margin-top: 8px;
        }
        .page-subtitle {
            color: var(--sentinel-muted);
            font-size: 17px;
            line-height: 1.55;
            margin-top: 12px;
            max-width: 1040px;
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
        .status-high-risk, .status-high {
            background: #ffedd5;
            color: #9a3412;
            border-color: #fed7aa;
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
        section[data-testid="stSidebar"] div[data-testid="stExpander"] {
            border: 1px solid #334155;
            background: #111c30;
        }
        section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
            color: #f8fafc;
            font-size: 13px;
            font-weight: 800;
        }
        .sidebar-walkthrough {
            padding: 2px 0 4px;
        }
        .sidebar-walkthrough .sidebar-step:first-child {
            border-top: 0;
            margin-top: 0;
            padding-top: 2px;
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
        .control-room-live-note {
            color: var(--sentinel-muted);
            font-size: 14px;
            padding: 14px 0 8px;
        }
        .control-room-section-title {
            color: var(--sentinel-ink);
            font-size: 20px;
            font-weight: 780;
            margin: 20px 0 14px;
        }
        .agent-focus-card,
        .sentinel-tower-card,
        .audit-result-card,
        .event-stream-card {
            border-radius: 8px;
            box-shadow: var(--sentinel-soft-shadow);
        }
        .agent-focus-card {
            background: #ffffff;
            padding: 34px;
            margin-top: 22px;
            min-height: 560px;
        }
        .agent-focus-header {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 24px;
            align-items: start;
            padding-bottom: 26px;
            border-bottom: 1px solid #edf2f7;
        }
        .agent-focus-label,
        .result-label,
        .result-line-label {
            color: var(--sentinel-muted);
            font-size: 11px;
            font-weight: 780;
            text-transform: uppercase;
        }
        .agent-focus-name {
            color: var(--sentinel-ink);
            font-size: 34px;
            line-height: 1.15;
            font-weight: 800;
        }
        .agent-focus-meta {
            color: var(--sentinel-muted);
            font-size: 16px;
            font-weight: 680;
            margin-top: 8px;
        }
        .agent-focus-status {
            background: #eef6ff;
            color: #1d4ed8;
            border-radius: 999px;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 760;
            white-space: nowrap;
        }
        .conversation-panel {
            padding: 34px 0 24px;
        }
        .chat-row {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 26px;
        }
        .chat-row-ai {
            justify-content: flex-end;
        }
        .chat-avatar {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 999px;
            background: #dbeafe;
            color: #1d4ed8;
            font-size: 12px;
            font-weight: 800;
            flex: 0 0 auto;
        }
        .chat-avatar-ai {
            background: #ccfbf1;
            color: #0f766e;
        }
        .chat-bubble {
            border-radius: 14px;
            padding: 18px 20px;
            font-size: 16px;
            line-height: 1.65;
            max-width: 82%;
        }
        .chat-user {
            background: #eef6ff;
            color: #14315f;
        }
        .chat-ai {
            background: #f8fafc;
            color: var(--sentinel-ink);
            border: 1px solid #e6edf5;
            min-height: 126px;
        }
        .agent-status-rail {
            display: flex;
            align-items: center;
            gap: 10px;
            padding-top: 24px;
            border-top: 1px solid #edf2f7;
            color: var(--sentinel-muted);
            font-size: 13px;
            font-weight: 700;
            flex-wrap: wrap;
        }
        .status-step {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .status-complete {
            color: var(--sentinel-teal);
        }
        .status-active {
            color: var(--sentinel-blue);
        }
        .status-arrow {
            color: #cbd5e1;
        }
        .sentinel-tower-card,
        .audit-result-card {
            background: #0f172a;
            color: #e5eefc;
            padding: 34px;
            min-height: 660px;
            box-shadow: 0 22px 46px rgba(15, 23, 42, 0.18);
        }
        .tower-eyebrow {
            color: #7dd3fc;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .tower-title {
            color: #ffffff;
            font-size: 34px;
            line-height: 1.15;
            font-weight: 800;
            margin-bottom: 26px;
        }
        .tower-progress {
            height: 6px;
            border-radius: 999px;
            background: #1e293b;
            overflow: hidden;
            margin-bottom: 28px;
        }
        .tower-progress-fill {
            height: 100%;
            background: #2dd4bf;
            border-radius: 999px;
            transition: width 0.25s ease;
        }
        .tower-step {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 13px 14px;
            border-radius: 8px;
            color: #94a3b8;
            font-size: 15px;
            font-weight: 690;
        }
        .tower-active {
            background: #172554;
            color: #eff6ff;
            box-shadow: inset 3px 0 0 #2dd4bf;
        }
        .tower-complete {
            color: #ccfbf1;
        }
        .tower-step-marker {
            width: 20px;
            display: inline-block;
            color: #2dd4bf;
            font-weight: 900;
        }
        .pipeline-flow-arrow {
            color: #475569;
            margin: 0 0 0 21px;
            line-height: 1;
        }
        .policy-check-list {
            margin: 8px 0 12px 34px;
            padding-left: 14px;
            border-left: 1px solid #26364d;
        }
        .policy-check-row {
            display: grid;
            grid-template-columns: 18px 48px 1fr;
            gap: 8px;
            align-items: center;
            padding: 7px 0;
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.35;
        }
        .policy-check-active {
            color: #dbeafe;
        }
        .policy-check-pass {
            color: #ccfbf1;
        }
        .policy-check-fail {
            color: #fecdd3;
        }
        .policy-check-marker {
            font-weight: 900;
        }
        .policy-check-id {
            color: #cbd5e1;
            font-weight: 800;
        }
        .policy-alert {
            border-radius: 8px;
            background: #3b1d2b;
            border: 1px solid #be123c;
            padding: 16px;
            margin-bottom: 22px;
            animation: sentinelAlertPulse 0.9s ease-in-out;
        }
        .policy-alert-title {
            color: #fff1f2;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 12px;
        }
        .policy-alert-grid {
            display: grid;
            grid-template-columns: 0.8fr 1.5fr 0.8fr;
            gap: 12px;
        }
        .policy-alert-grid span {
            display: block;
            color: #fecdd3;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .policy-alert-grid strong {
            color: #ffffff;
            font-size: 13px;
            line-height: 1.35;
        }
        .policy-alert-explanation {
            color: #ffe4e6;
            font-size: 13px;
            line-height: 1.45;
            margin-top: 12px;
        }
        @keyframes sentinelAlertPulse {
            0% { transform: translateY(-6px); opacity: 0; }
            45% { transform: translateY(0); opacity: 1; box-shadow: 0 0 0 5px rgba(244, 63, 94, 0.18); }
            100% { transform: translateY(0); opacity: 1; box-shadow: none; }
        }
        .policy-violation-list {
            display: grid;
            gap: 12px;
        }
        .policy-violation-card {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            border-left: 5px solid #ef4444;
            border-radius: 8px;
            padding: 15px 16px;
            box-shadow: var(--sentinel-soft-shadow);
        }
        .policy-violation-compact {
            background: rgba(255, 255, 255, 0.04);
            border-color: #26364d;
            box-shadow: none;
            padding: 12px 13px;
            margin-top: 8px;
        }
        .policy-violation-medium {
            border-left-color: #f97316;
        }
        .policy-violation-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
        }
        .policy-violation-title {
            color: var(--sentinel-ink);
            font-size: 14px;
            font-weight: 800;
            line-height: 1.35;
        }
        .audit-result-card .policy-violation-title,
        .audit-result-card .policy-violation-explanation {
            color: #f8fafc;
        }
        .policy-violation-explanation {
            color: var(--sentinel-muted);
            font-size: 13px;
            line-height: 1.45;
            margin-top: 7px;
        }
        .policy-severity-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 4px 8px;
            font-size: 11px;
            font-weight: 800;
            white-space: nowrap;
        }
        .policy-severity-critical,
        .policy-severity-high {
            background: #fee2e2;
            color: #991b1b;
        }
        .policy-severity-medium {
            background: #ffedd5;
            color: #9a3412;
        }
        .policy-empty {
            color: var(--sentinel-muted);
            font-size: 13px;
        }
        .audit-result-card .policy-empty {
            color: #94a3b8;
        }
        .framework-policy-table {
            display: grid;
            gap: 12px;
            margin-top: 12px;
        }
        .framework-policy-row {
            display: grid;
            grid-template-columns: 86px 1fr;
            gap: 18px;
            align-items: start;
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            border-radius: 8px;
            padding: 18px 20px;
            box-shadow: var(--sentinel-soft-shadow);
        }
        .framework-policy-id {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 42px;
            border-radius: 8px;
            background: #eef6ff;
            color: var(--sentinel-blue);
            font-size: 14px;
            font-weight: 800;
        }
        .framework-policy-name {
            color: var(--sentinel-ink);
            font-size: 17px;
            font-weight: 800;
            line-height: 1.3;
        }
        .framework-policy-description {
            color: var(--sentinel-muted);
            font-size: 14px;
            line-height: 1.55;
            margin-top: 6px;
        }
        .framework-policy-items {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 8px;
            list-style: none;
            padding: 0;
            margin: 12px 0 0;
        }
        .framework-policy-items li {
            background: #f8fafc;
            border: 1px solid #e6edf5;
            border-radius: 999px;
            color: var(--sentinel-ink);
            font-size: 12px;
            font-weight: 700;
            padding: 7px 9px;
            text-align: center;
        }
        .formula-card {
            background: #0f172a;
            border-radius: 8px;
            padding: 24px;
            margin: 12px 0 16px;
            box-shadow: 0 16px 34px rgba(15, 23, 42, 0.12);
        }
        .formula-card-compact {
            margin: 18px 0 0;
            padding: 18px;
        }
        .formula-title {
            color: #7dd3fc;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .formula-expression {
            color: #ffffff;
            font-size: 22px;
            line-height: 1.45;
            font-weight: 800;
        }
        .score-weight-grid,
        .component-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin-top: 14px;
        }
        .score-weight-card,
        .component-card,
        .example-card {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            border-radius: 8px;
            padding: 20px;
            box-shadow: var(--sentinel-soft-shadow);
        }
        .score-weight-value {
            color: var(--sentinel-teal);
            font-size: 32px;
            line-height: 1;
            font-weight: 800;
        }
        .score-weight-name,
        .component-title {
            color: var(--sentinel-ink);
            font-size: 16px;
            font-weight: 800;
            margin-top: 10px;
        }
        .score-weight-detail,
        .component-body {
            color: var(--sentinel-muted);
            font-size: 13px;
            line-height: 1.5;
            margin-top: 7px;
        }
        .component-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            border-radius: 999px;
            background: #eef6ff;
            color: var(--sentinel-blue);
            font-size: 17px;
            font-weight: 800;
        }
        .component-example {
            background: #f8fafc;
            border-left: 3px solid var(--sentinel-teal);
            color: var(--sentinel-ink);
            font-size: 13px;
            line-height: 1.5;
            margin-top: 14px;
            padding: 10px 12px;
        }
        .example-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 18px;
            padding-bottom: 18px;
            border-bottom: 1px solid #edf2f7;
        }
        .example-eyebrow {
            color: var(--sentinel-teal);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .example-title {
            color: var(--sentinel-ink);
            font-size: 30px;
            line-height: 1.15;
            font-weight: 800;
            margin-top: 4px;
        }
        .example-score {
            color: var(--sentinel-green);
            font-size: 38px;
            line-height: 1;
            font-weight: 800;
        }
        .example-breakdown {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-top: 18px;
        }
        .example-breakdown div {
            background: #f8fafc;
            border: 1px solid #e6edf5;
            border-radius: 8px;
            padding: 13px;
        }
        .example-breakdown span {
            display: block;
            color: var(--sentinel-muted);
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .example-breakdown strong {
            display: block;
            color: var(--sentinel-ink);
            font-size: 22px;
            font-weight: 800;
            margin-top: 5px;
        }
        .audit-result-hero {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 18px;
            padding-bottom: 26px;
            border-bottom: 1px solid #26364d;
        }
        .result-score {
            color: #ffffff;
            font-size: 72px;
            line-height: 1;
            font-weight: 800;
            margin-top: 10px;
        }
        .result-score-trusted {
            color: #86efac;
        }
        .result-score-watch {
            color: #fde68a;
        }
        .result-score-high-risk {
            color: #fdba74;
        }
        .result-score-critical {
            color: #fca5a5;
        }
        .risk-chip {
            border-radius: 999px;
            background: #172554;
            color: #bfdbfe;
            padding: 10px 15px;
            font-size: 13px;
            font-weight: 800;
        }
        .risk-trusted {
            background: #103328;
            color: #bbf7d0;
        }
        .risk-watch {
            background: #382b16;
            color: #fde68a;
        }
        .risk-high-risk {
            background: #3b2312;
            color: #fed7aa;
        }
        .risk-critical {
            background: #3b1d2b;
            color: #fecdd3;
        }
        .result-detail-stack {
            margin-top: 24px;
        }
        .result-breakdown {
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid #26364d;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 8px;
        }
        .result-breakdown-title {
            color: #f8fafc;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 12px;
        }
        .result-breakdown-row {
            display: grid;
            grid-template-columns: 132px 1fr 58px;
            align-items: center;
            gap: 10px;
            color: #cbd5e1;
            font-size: 12px;
            font-weight: 720;
            margin-top: 9px;
        }
        .result-breakdown-bar {
            height: 7px;
            border-radius: 999px;
            background: #1e293b;
            overflow: hidden;
        }
        .result-breakdown-fill {
            height: 100%;
            border-radius: 999px;
            background: #2dd4bf;
        }
        .result-breakdown-final {
            color: #ffffff;
            font-size: 14px;
            font-weight: 800;
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px solid #26364d;
        }
        .result-line {
            padding: 16px 0;
            border-bottom: 1px solid #223047;
        }
        .result-line-final {
            padding-bottom: 24px;
            border-bottom: 0;
            margin-bottom: 6px;
        }
        .result-line-value {
            color: #f8fafc;
            font-size: 16px;
            line-height: 1.5;
            font-weight: 680;
            margin-top: 7px;
        }
        .result-line-caption {
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.45;
            margin-top: 5px;
        }
        .event-stream-card {
            background: #ffffff;
            padding: 22px;
            margin-top: 22px;
            max-height: 270px;
            overflow-y: auto;
        }
        .event-stream-title {
            color: var(--sentinel-ink);
            font-size: 17px;
            font-weight: 780;
            margin-bottom: 12px;
        }
        .event-stream-row {
            display: grid;
            grid-template-columns: 72px 1fr;
            gap: 10px;
            padding: 13px 0;
            border-top: 1px solid #edf2f7;
        }
        .event-time {
            color: var(--sentinel-muted);
            font-size: 12px;
            font-weight: 760;
        }
        .event-message {
            color: var(--sentinel-ink);
            font-size: 13px;
            line-height: 1.4;
            font-weight: 640;
        }
        @media (max-width: 1100px) {
            .agent-focus-header {
                grid-template-columns: 1fr;
            }
            .agent-focus-status {
                width: fit-content;
            }
            .chat-bubble {
                max-width: 100%;
            }
            .policy-alert-grid {
                grid-template-columns: 1fr;
            }
            .score-weight-grid,
            .component-grid,
            .example-breakdown {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .framework-policy-items {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        @media (max-width: 760px) {
            .agent-focus-card,
            .sentinel-tower-card,
            .audit-result-card {
                min-height: auto;
                padding: 22px;
            }
            .event-stream-row {
                grid-template-columns: 1fr;
                gap: 4px;
            }
            .result-score {
                font-size: 52px;
            }
            .page-header {
                padding: 26px;
                min-height: 0;
            }
            .page-title {
                font-size: 30px;
            }
            .framework-policy-row,
            .score-weight-grid,
            .component-grid,
            .example-breakdown,
            .framework-policy-items {
                grid-template-columns: 1fr;
            }
            .formula-expression {
                font-size: 18px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
