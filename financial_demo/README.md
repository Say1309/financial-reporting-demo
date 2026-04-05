# Financial Reporting Demo

A Django-based financial reporting system for trust management (fideicomisos), built as a portfolio demonstration.

**Live demo →** [financial-reporting-demo.onrender.com](https://financial-reporting-demo.onrender.com) *(deploy in progress)*

---

## Overview

This system replicates the architecture of a real-world financial reporting platform used to manage structured finance clients (fideicomisos). It demonstrates an 8-step workflow for period-end processing, role-based access control, and multi-department checklists.

> Built with: **Python · Django · SQLite · HTML/CSS · WhiteNoise**  
> Deployed on: **Render** (free tier)

---

## Features

### 8-step workflow engine (`procesoejecucion`)
Each reporting period goes through a controlled 8-step process:

| Step | Name |
|------|------|
| 1 | Source data verification |
| 2 | Data load |
| 3 | Balance validation |
| 4 | Yield calculation |
| 5 | Report generation |
| 6 | Supervisor review |
| 7 | Authorization |
| 8 | Process close |

### Role-based access
- **Capturista** — data entry, checklist updates
- **Ejecutivo Mesa** — checklist approval/rejection
- **Supervisor** — full access, process oversight

### Three-checklist system
Parallel validation across departments before process close:
- **ChecklistCuentas** — bank reconciliation, balance validation
- **ChecklistData** — data integrity, format validation  
- **ChecklistExpedientes** — documentation, legal powers, dictamen

### Financial data capture
Per-period capture of: opening balance, contributions, withdrawals, yields, fees, reference rate (TIIE). Computed closing balance with full audit trail.

### Printable reports
HTML-based period reports with full movement detail and step history, ready for PDF printing.

---

## Demo credentials

| User | Password | Role |
|------|----------|------|
| `capturista` | `demo123` | Data entry |
| `ejecutivo` | `demo123` | Mesa executive |
| `supervisor` | `demo123` | Supervisor |

---

## Local setup

```bash
git clone https://github.com/Say1309/financial-reporting-demo.git
cd financial-reporting-demo
pip install -r requirements.txt
python manage.py migrate
python seed.py          # loads demo fideicomisos, users, and sample processes
python manage.py runserver
```

Open `http://localhost:8000` and log in with any demo credential above.

---

## Project structure

```
financial_demo/
├── core/           # Fideicomiso and Role models
├── reporteo/       # Workflow engine, data capture, reports
├── checklist/      # Three-checklist validation system
├── templates/      # HTML templates
├── static/         # CSS
├── seed.py         # Demo data loader
└── render.yaml     # One-click Render deploy
```

---

## Deploy on Render (free)

1. Fork this repo
2. Go to [render.com](https://render.com) → New Web Service → connect your fork
3. Render auto-detects `render.yaml` — click **Deploy**
4. First deploy runs migrations and seed automatically

---

## About

# Financial Reporting System — Project Brief

## The problem

Financial institutions that manage multiple trust accounts (or any recurring client portfolios) face a common operational challenge at period-end: **several departments need to complete interdependent tasks in a specific order, with full accountability at each step.**

Without a structured system, this process typically looks like:

- Spreadsheets passed around by email with no version control
- No clear record of who validated what, or when
- Steps completed out of order, causing downstream errors
- No single view of which clients are done and which are blocked
- Audit trails that exist only in someone's inbox

The result is delays, rework, and compliance risk.

---

## The solution

A web-based workflow engine that enforces a structured 8-step process for each client account, per reporting period. Every action is logged, every department has a defined role, and nothing moves forward until the previous step is complete.

```
Step 1 → Verify source data
Step 2 → Load information
Step 3 → Validate balances
Step 4 → Calculate yields
Step 5 → Generate reports
Step 6 → Supervisor review
Step 7 Authorization
Step 8 → Close process
```

Three parallel checklists run alongside the workflow, owned by different departments:

| Checklist | Owner | Validates |
|-----------|-------|-----------|
| **Accounts** | Operations | Bank reconciliation, balance validation |
| **Data** | DataOps | Source data integrity, format compliance |
| **Records** | Legal/Compliance | Documentation, signatures, legal powers |

Only when all checklists are approved and all 8 steps are logged can a period be closed.

---

## Who uses it

| Role | What they do in the system |
|------|---------------------------|
| **Data Entry** | Captures financial figures, updates checklists |
| **Desk Executive** | Reviews and approves/rejects checklists |
| **Supervisor** | Full visibility, closes processes, generates reports |

---

## Technical architecture

```
financial_demo/
├── core/          ← Client accounts + role management
│                    Models: Account, Role (4 access levels)
│
├── reporteo/      ← Workflow engine
│                    Models: Process, StepLog, FinancialData
│                    8-step state machine per client/period
│
├── checklist/     ← Parallel validation system
│                    Models: ChecklistAccounts, ChecklistData,
│                            ChecklistRecords
│                    Independent approval flow per department
│
└── templates/     ← HTML UI (dark theme, print-ready reports)
```

**Stack:** Python 3.11 · Django 5 · SQLite · WhiteNoise · Gunicorn  
**Deploy:** Render (free tier) — auto-migrates and seeds on first deploy

---

## Key design decisions

**Why Django over a simpler framework?**  
The role-based access, relational data model (processes → steps → checklists), and admin panel made Django the right fit. The ORM handles complex queries across 6+ related models cleanly.

**Why SQLite for the demo?**  
Zero configuration for reviewers cloning the repo. The architecture is database-agnostic — swapping to PostgreSQL or SQL Server requires changing one line in `settings.py`. The original production system runs on SQL Server with stored procedures for complex financial calculations.

**Why three separate checklist models instead of one?**  
Each checklist has different fields, different owners, and a different approval lifecycle. Separate models make role-based visibility straightforward and keep the business logic clean.

**Audit trail by design**  
Every step completion writes a `StepLog` record with timestamp and user. Checklists store both who requested and who reviewed. Reports are generated from this log — not from a snapshot — so they always reflect what actually happened.

---

## What this demonstrates

- Designing a **multi-step state machine** with role-based transitions
- **Relational data modeling** across interdependent entities
- **Role-based access control** without third-party packages
- Django patterns: class-free views, `get_or_create`, `select_related`, decorators
- Clean separation of concerns across three Django apps
- Production-ready setup: static files, environment variables, one-click deploy

---

## Note on data

All accounts, figures, and names in this demo are **entirely synthetic**, generated by `seed.py`. No real client data was used. The system architecture is adapted from real financial operations experience, with domain-specific details generalized for public use.

---

*Built by [Sayuri Mota](https://github.com/Say1309) — Physics & Mathematics (ESFM-IPN) · DataOps Engineer · Mexico City*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sayuri_Mota-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/ingrid-sayuri-mota-de-la-rosa)
