# Productivity Tracker (Flask + Google Sheets)

Admin login: `/admin/login`  |  Employee login: `/employee/login`
Admin-only Team page: `/admin/team`

## Project files (repo root)
- `app_design.py`   - the application (Flask variable: `app`)
- `requirements.txt`, `render.yaml`, `.gitignore`, `README.md`
- NEVER commit `credentials.json`, `.env` or `.secret_key`

## 1. Push to GitHub
```bash
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
   (`app_design` = the file name without `.py`; `app` = the Flask variable)
4. Environment tab -> add:
   - `PYTHON_VERSION` = `3.12.3`
   - `GOOGLE_CREDS` = `/etc/secrets/credentials.json`
   - `SECRET_KEY`   = any long random string
   - `ADMIN_USER`   = your admin username
   - `ADMIN_PASS`   = a strong password
   - `SHEET_ID`     = your Google Sheet ID
   - `PHOTO_DIR`    = `/var/data/employee_photos` (only with a paid plan + Disk mounted at `/var/data`)
5. Environment tab -> **Secret Files** -> Add:
   filename `credentials.json`, paste the full contents of your service-account JSON.
6. Share your Google Sheet (Editor) with the `client_email` from the JSON.
7. Manual Deploy -> Deploy latest commit. Open `https://<your-service>.onrender.com/admin/login`.

## Notes
- Free plan sleeps after ~15 min idle; first load may take ~30-60 s.
- Employee profile pictures are saved as files in `PHOTO_DIR` (default: `employee_photos/` next to the app).
  The free plan has no persistent disk, so pictures are lost on redeploy/restart there; use a paid plan with a Disk to keep them.
- Do not add `--preload` to gunicorn (background loops start at import).
