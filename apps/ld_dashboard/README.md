# Birth center what-if (Streamlit demo)

The Lab 4 model as a small web app: choose triage beds, LDR rooms, postpartum beds, the average postpartum stay, and
births per day, then compare your scenario with the baseline on the same simulated patients. A teaching model with
synthetic numbers: not for real staffing decisions.

## Run it on your own computer

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Put it on the web (free)

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with a GitHub account.
2. Choose **Create app**, then deploy from this repository: branch `main`, main file `apps/ld_dashboard/app.py`.
3. Wait for the build (a few minutes the first time). An idle app goes to sleep; the first visit afterwards wakes it.

`ld_model.py` is the same model as in the Lab 4 notebook.
