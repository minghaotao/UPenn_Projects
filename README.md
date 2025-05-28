
# 🛠️ Penn Engineering Online: Project Collection

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Slack Bot](https://img.shields.io/badge/Slack-Bot-4A154B?logo=slack)](https://api.slack.com/)
[![Canvas API](https://img.shields.io/badge/Canvas-API-FFA500?logo=instructure)](https://canvas.instructure.com/)

This repository contains a collection of automation and reporting tools developed for operational efficiency at **Penn Engineering Online**. These scripts streamline data workflows across our courses, helping us better serve students, instructors, and TAs.

---

## 📚 Table of Contents

- [📊 Ed Discussion Analytics](#-ed-discussion-analytics)
- [📝 Entering Zeros for Missing Assignments](#-entering-zeros-for-missing-assignments)
- [📂 Extension File Tracker](#-extension-file-tracker)
- [⏱️ Gradescope Late Submissions Sync](#️-gradescope-late-submissions-sync)
- [🤖 Slack Bot Integration](#-slack-bot-integration)
- [📅 WaitWhile (TA Office Hours Platform)](#-waitwhile-ta-office-hours-platform)

---

### 📊 Ed Discussion Analytics

We pull data from **Ed Discussion** across all courses in the program. Each week, a script calculates:

- Response rate  
- Number of unresolved posts  
- Number of resolved posts  
- Posts not answered within 24 hours  

A weekly report is posted to the team Slack channel to help monitor TA responsiveness across courses.

---

### 📝 Entering Zeros for Missing Assignments

To ensure advisors have accurate data from the **Canvas Gradebook**, this script enters zeros for students who missed assignments, based on these criteria:

- The due date passed more than 9 days ago  
- Some grades have been entered  
- Some students still show no grades  

The script supports third-party tools like **Gradescope** and **Codio** by identifying relevant assignments and entering zeros accordingly.

---

### 📂 Extension File Tracker

Each semester, we process over **2,000 extension requests**. This script:

- Tracks weekly extensions  
- Summarizes how many were approved or denied  
- Provides a per-course overview of extension trends

---

### ⏱️ Gradescope Late Submissions Sync

Some courses apply **daily late penalties**. This script automates the process by:

- Accessing **Gradescope Gradebook**  
- Capturing late submission data  
- Uploading late timestamps to Canvas  

Canvas’s built-in late policy then automatically calculates penalties — saving instructors time and ensuring consistency.

---

### 🤖 Slack Bot Integration

All reports are sent via a custom **Slack Bot**, which uses the **Slack API** to:

- Post summaries and analytics  
- Send graphs and data images  

The bot is tightly integrated with all other scripts in this repository.

---

### 📅 WaitWhile (TA Office Hours Platform)

We use **WaitWhile** to manage TA office hours across all courses. This script:

- Tracks how many OHs were offered per course each week  
- Provides a snapshot of TA availability program-wide  

This helps leadership monitor and optimize TA staffing levels.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
