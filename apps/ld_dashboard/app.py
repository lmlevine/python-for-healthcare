"""Birth center what-if dashboard (Python for Healthcare, Session 2 demo).

The same model as Lab 4, as a web app. Run it on your own computer:
    pip install -r requirements.txt
    streamlit run app.py
"""
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats

from ld_model import BASELINE, run_many, summarize

KEY_METRICS = {                          # result column: short label for the tiles
    "mean wait for a triage bed, all patients (h)": "Triage wait, hours",
    "waited for an LDR room (%)": "Waited for an LDR room, %",
    "mean wait for an LDR room, all patients (h)": "LDR wait, hours",
    "blocked in LDR, waiting for PP (%)": "Blocked in LDR, %",
}

st.set_page_config(page_title="Birth center what-if", layout="wide")
st.title("Birth center what-if")
st.caption("Kestrel Valley Health (fictional). A teaching model: steady arrivals, exponential stays, "
           "synthetic numbers. Not for real staffing decisions.")

with st.sidebar:
    st.header("Your scenario")
    params = dict(BASELINE)
    params["obs_beds"] = st.slider("Triage beds", 2, 6, BASELINE["obs_beds"])
    params["ldr_rooms"] = st.slider("LDR rooms", 5, 10, BASELINE["ldr_rooms"])
    params["pp_beds"] = st.slider("Postpartum beds", 20, 32, BASELINE["pp_beds"])
    params["pp_hours"] = st.slider("Average postpartum stay (hours)", 36, 56, BASELINE["pp_hours"], step=2)
    params["arrivals_per_day"] = round(st.slider("Births per day", 7.0, 12.0, BASELINE["arrivals_per_day"],
                                                 step=0.2), 1)        # round(): avoid 9.600000000000001
    reps = st.slider("Replications (simulated years)", 20, 50, 30, step=10)
    run = st.button("Run", type="primary")


@st.cache_data(show_spinner=False)
def simulate(param_items, n):
    return run_many(dict(param_items), n=n)


if not run:
    st.info("Choose a scenario in the sidebar, then click **Run**. Each scenario is compared with the baseline "
            "on the same simulated patients.")
    st.stop()

try:
    with st.spinner(f"Simulating {reps} years, twice (your scenario and the baseline)..."):
        scenario = simulate(tuple(sorted(params.items())), reps)
        base = simulate(tuple(sorted(BASELINE.items())), reps)
    scenario_summary = summarize(scenario)                # applies the model's refusal rules
except ValueError as refusal:
    st.error(str(refusal))
    st.stop()

diff = scenario - base                                   # paired: same seeds, same patients
half = stats.t.ppf(0.975, reps - 1) * diff.std() / np.sqrt(reps)

st.subheader("Your scenario compared with the baseline")
for col, (name, label) in zip(st.columns(len(KEY_METRICS)), KEY_METRICS.items()):
    col.metric(label, f"{scenario[name].mean():.1f}", f"{diff[name].mean():+.1f}", delta_color="inverse")

table = pd.DataFrame({
    "your scenario": scenario.mean().round(1),
    "baseline": base.mean().round(1),
    "change (95% interval)": [f"{m:+.1f} ({m - h:+.1f} to {m + h:+.1f})" for m, h in zip(diff.mean(), half)],
})
st.dataframe(table)

with st.expander("Your scenario: mean and 95% interval"):
    st.dataframe(scenario_summary)
st.caption(f"{reps} replications. Waits are averaged over all patients, including the many who don't wait. "
           "Lower is better for every measure shown; green arrows mean an improvement.")
