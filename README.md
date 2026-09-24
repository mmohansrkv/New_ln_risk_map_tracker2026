# Productivity Tracker (Flask + Google Sheets)

Admin login: `/admin/login`  |  Employee login: `/employee/login`

## 1. Push to GitHub
```bash
cd productivity-tracker
git init
git add .
git status          # make sure credentials.json is NOT listed
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/productivity-tracker.git
git push -u origin main
```
(Create the empty repo on github.com first. Make it **Private**.)

## 2. Deploy on Render
1. render.com -> New -> Web Service -> connect the GitHub repo
   (or New -> Blueprint to use `render.yaml`).
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app_design:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
4. Environment tab -> add:
   - `GOOGLE_CREDS` = `/etc/secrets/credentials.json`
   - `SECRET_KEY`   = any long random string
   - `ADMIN_USER`   = your admin username
   - `ADMIN_PASS`   = a strong password
   - `SHEET_ID`     = your Google Sheet ID
5. Environment tab -> **Secret Files** -> Add:
   filename `credentials.json`, paste the full contents of your service-account JSON.
6. Share your Google Sheet (Editor) with the `client_email` from the JSON.
7. Deploy. Open `https://<your-service>.onrender.com/admin/login`.

Note: the free plan sleeps after ~15 min idle; first load may take ~30-60 s.
