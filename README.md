# Website Uptime Checker (ROSPL_WUC)

A beginner-friendly Python Flask mini-project for the Recent Open-Source Project Lab.

## Features
- Check a public website on demand
- Display online/offline status
- Display HTTP status code and response time
- Basic validation for URL format and local/private network hosts
- Responsive HTML/CSS interface

## Requirements
- Python 3.10 or later
- pip
- Internet connection to check public websites

## Run on Windows (PowerShell)

Open this folder in VS Code and run:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

If Python is launched using `py`, use `py -m venv venv` to create the environment.

Open http://127.0.0.1:5000 in your browser.

PowerShell activation is optional; using `.\venv\Scripts\python.exe` directly avoids execution-policy issues.

## Project structure

```text
ROSPL_WUC/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

Do not upload the `venv` folder to GitHub. Create it locally after extracting the project.

## Important notes
- Checks run only after a user submits a URL; this is not continuous monitoring.
- Network restrictions, DNS failures, redirects, or a site's own protections can affect results.
- This is an educational starter project, not a production security scanner.
- Before publishing, choose an appropriate open-source license and follow your instructor's contribution requirements.
