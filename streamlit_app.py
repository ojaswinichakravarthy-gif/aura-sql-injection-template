"""Streamlit frontend for live SQL injection detection demos."""

from __future__ import annotations

import streamlit as st

from aura_sqli import DetectionEngine


st.set_page_config(page_title="Aura SQLi Detector", layout="wide")
engine = DetectionEngine()

st.title("Aura SQL Injection Detection")
query = st.text_area("SQL query or request payload", "SELECT * FROM users WHERE id = 1 OR 1=1 --", height=120)
if st.button("Analyze", type="primary"):
    result = engine.detect(query).as_dict()
    st.metric("Decision", result["decision"], f'{result["confidence"]}% confidence')
    st.metric("Threat level", result["threat_level"], f'{result["latency_ms"]} ms')
    st.code(result["normalized_query"], language="sql")
    st.subheader("Explanation")
    st.write(result["reason"])
    st.dataframe(result["influential_features"], use_container_width=True)
    st.subheader("Component scores")
    st.json(result["component_scores"])

