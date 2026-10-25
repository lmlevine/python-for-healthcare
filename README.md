# Python for Healthcare

**Stanford Technology Training · ITS-2519 · Dr. Lionel Levine · October 2026**

Read it, run it, check it: the Python you need to direct an AI assistant, read what it wrote, and verify the result,
using synthetic healthcare data. Everything runs in your browser in Google Colab. There's nothing to install.

## Before the first session (5 minutes)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmlevine/python-for-healthcare/blob/main/notebooks/00_setup_check.ipynb) **Setup check.** Open it, sign in with a personal Google account,
choose **File → Save a copy in Drive**, and run the cell.

Step-by-step guide: [Setup Guide (PDF)](handouts/setup-guide.pdf)

## Session 1 · Monday, October 26 · From two messy files to a defensible result

| | Notebook | Open in Colab |
|---|---|---|
| 01 | Python you need to read | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmlevine/python-for-healthcare/blob/main/notebooks/session1/01_python_you_need_to_read.ipynb) |
| 02 | Lab 1: Two files, one truth | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmlevine/python-for-healthcare/blob/main/notebooks/session1/02_lab1_two_files_one_truth.ipynb) |
| 03 | Lab 2: Ask for the analysis, then check it | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmlevine/python-for-healthcare/blob/main/notebooks/session1/03_lab2_ask_then_check.ipynb) |

Handout: [Python You Need to Read + Check It Before You Trust It (PDF)](handouts/session1-handout.pdf)

## Session 2 · Wednesday, October 28 · Prediction and operations

| | Notebook | Open in Colab |
|---|---|---|
| 04 | Lab 3: Build it, then try to break it | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmlevine/python-for-healthcare/blob/main/notebooks/session2/04_lab3_build_then_break.ipynb) |
| 05 | Lab 4: The what-if machine | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lmlevine/python-for-healthcare/blob/main/notebooks/session2/05_lab4_what_if_machine.ipynb) |

Handout: [Check a Model Before You Trust It + Check a Simulation (PDF)](handouts/session2-handout.pdf)

Demo app: [apps/ld_dashboard](apps/ld_dashboard) has the Lab 4 model as a small web app (Streamlit).

## Using these notebooks

- Each link opens a read-only copy. Choose **File → Save a copy in Drive** before you start; your copy is private to you.
- Run a cell with **Shift + Enter**. If Colab warns that the notebook wasn't authored by Google, choose **Run anyway**.
- The notebooks load their data from this repository automatically. If loading fails more than once, download the CSV
  files from [data/session1](data/session1) or [data/session2](data/session2) and drag them into Colab's Files panel
  (the folder icon on the left); the notebooks use your uploaded copy automatically.

## About the data

Every dataset here is synthetic. Kestrel Valley Health, its clinics, the Home BP Coaching Trial, its prediabetes
registry, and its birth center are fictional, and no record describes a real person. Please don't add real patient
data to these notebooks.

Lab 4's birth-center model follows the structure of Mark Isken's teaching model of an obstetrics unit
(triage, labor and delivery, postpartum).

## Rights

© 2026 Lionel Levine. All rights reserved. See [LICENSE.md](LICENSE.md).
