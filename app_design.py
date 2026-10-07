"""Productivity Tracker - Flask + Google Sheets.
Admin link:    /admin/login
Employee link: /employee/login

Access rules (Update59):
  * Two separate logins. /admin/login accepts ONLY the admin account; /employee/login accepts ONLY employees.
  * /admin/* is reachable only with an admin session, /employee/* only with an employee session
    (enforced twice: by a URL-prefix guard on every request AND by @need(role) on each view).
  * A signed-in employee who opens any admin URL (or the admin login page) is sent back to their own
    page; a signed-in admin who opens an employee URL is sent to the Admin dashboard.
  * Audit Log (Update60): Admin ticks the exact PROCESSES each employee may audit. The employee sees only
    their OWN data: Productivity (only the ticked processes) and Attendance, as two separate sections.
  * Audit Log (Update61): Admin's Audit Log is PROCESS-FIRST: pick a process -> the employees who worked on it are
    found automatically -> Productivity, Productivity %, Attendance and audit details are shown. The old
    employee-wise list + access control stays under 'By Employee / Access'. Employees are unchanged (own data, ticked processes only).
  * Mahizhchi (Update62): Admin keeps multiple-choice questions (options A-D, ONE ✓ correct answer) in the "Mahizhchi Log"
    sheet or pastes them on Admin -> Mahizhchi, publishes it and shares it with all / selected employees.
    Employees ANSWER by ticking one option per question; the correct answer is never sent to them (only Admin sees it and
    the results). It shows for an employee only while it is published AND shared with them; otherwise it is hidden.
  * 8-hour process targets (Update63): Admin sets, per process, the count to be completed in a full 8-hour day
    (Processes -> "Target count / 8 hrs"; the per-hour rate is derived = target / 8, and vice versa). An employee whose
    entry is below the target for the hours logged gets a red alert when saving, a dashboard alert (last 7 days) and a live
    warning in the entry form.
  * Update66: Productivity log shows each entry's Target count, Completed count and a Target met / Not met badge (plus a
    met / not-met tally). Employee Info in the admin sidebar expands to Employees / Notifications / Mahizhchi.
  * Update67: Admin sidebar 'Employee Info' is a dropdown (Employees / Notifications / Mahizhchi). Login pages get a 3D data-packet
    animation (Employee: packets uploaded to the server; Admin: live feed arriving at the dashboard) and synthesised
    Tamil-style background music (Employee = raga Mohanam, Admin = raga Hamsadhwani) with a Music on/off button.
  * Update68: Welcome page (after Admin and Employee login) uses the same AI-style 3D scene + data-packet flow as the login
    pages (Employee = data sent to server, Admin = live data arriving). Overview no longer shows the "Employees" count card.
  * Update69: sidebar 'Employees' link removed; Processes list/form no longer shows 'Target count / hour' (still derived from the
    8-hour target internally). Welcome page never plays music by itself: the Tamil-style music starts when the mouse moves over it.
  * Update70: Employee pages play the Tamil-style music (Mohanam) only after the mouse moves on the page - never automatically,
    no button needed (the speaker button is just an optional mute). Replaces the old remote-file background music.
  * Update71: (1) Admin -> Overview has a live "Online Employees" log (employee + status; adds/removes itself as employees log in/out,
    refreshes every 5 s; heartbeat-based so a closed tab drops off). (2) Employee-page background music is now a soft solo
    Tamil bamboo flute (Pullangu Kuzhal, raga Mohanam) - no vocals, no drone, no percussion, no other instrument.
  * Update72: after employee login the Welcome Page starts the Tamil bamboo-flute music by itself (7 s welcome), instrumental only.
  * Update73: Employee login page has NO music. Employee Welcome Page = AI welcome voice first, then (after the voice ends) only the
    Tamil bamboo-flute instrumental. Admin pages unchanged.
  * Update74: Employee Chat (sidebar 'Chat'). Lists only employees who are online right now; pick one to chat. Messages arrive within ~2 s,
    unread badge + pop-up + tab-title alert on every employee page. Offline employees vanish from the list; their chat shows Offline.
  * Update75: Employee Welcome Page has no audio (no voice, no music). Fixed a JS syntax error that froze the Welcome Page (site would not open).
  * Update76: Chat = floating chat button on every employee page + sidebar link; messages live 1 hour only (auto-deleted every minute and on
    every access); Chat section has NO audio (the flute does not play there). New original Tamil bamboo-flute (Pullangu Kuzhal) instrumental
    for the Employee Page, flute only.
  * Update77: (1) The floating Chat button and the 1-to-1 chat are gone. Sidebar 'Group Chat': ONE group made of the employees who are online right
    now - joining on login/coming online, removed on logout/offline - messages auto-delete after 1 hour, no audio in the chat.
    (2) Music only on the Welcome Pages (employee + admin): after the welcome animation the Tamil bamboo flute (Pullangu Kuzhal) plays, flute only.
    No music on login pages, the Employee pages or the Admin pages.
  * Update78: Welcome Page opens first for Admin and Employee, no 'Continue' button, opens the Admin/Employee page by itself when it ends.
    Sidebar 'Group Chat' removed - only a round Chat icon (bottom-right) opens the Group Chat. NEW Tamil flute BGM (raga Kalyani, new
    melody, different from the earlier Mohanam tune), Welcome Page only.
  * Update104: compact Employee + Admin UI (smaller text/buttons) and a dashboard-style 3D Admin login (UI only; login logic unchanged).
  * Update105: View-Only Productivity for designations Senior Team Lead / Team Lead / Associate Manager (no entry, no %, no missed entries, no reminder e-mails; Leave & Permission unchanged).
  * Update106: 3D dashboard-style Employee login (UI only; login logic unchanged).
  * Update107: Mobius365 / LN_Map branding and logo removed from the Admin & Employee panels (sidebar, footer, login title bar, emblem, welcome page).
  * Update108: Admin login text removed, welcome page is a separate page (no panel behind it), 3D admin avatar, sidebar calendar for both panels.
  * Update109: "Admin Panel" / "Employee Panel" heading at the top of each sidebar; the Admin Panel / Productivity Dashboard text is back on the Admin login page only.
  * Update110: Admin welcome page - login text panel removed from it; subtle "© 2026 LN_MAP_AI" added at the bottom.
  * Update111: Group Chat retention is now 12 hours (was 1 hour): messages AND shared files/images are permanently auto-deleted by a background sweeper every 60 s (and on every chat poll/send).
  * Update127: the fixed shared picture in the Employee sidebar is replaced by a 3D animated profile avatar for the LOGGED-IN employee
    (male / female chosen from the employee's Gender; initials if Gender is blank), with the employee's name below it. It follows whoever is signed in
    (nothing is stored in the session or at login), is pure CSS-transform animation (gentle float + mouse tilt, paused for reduced-motion / hidden tabs).
    Login, authentication and every other Employee page function are unchanged.
  * Update126: the shared picture (employee_corner.png, embedded) now sits ABOVE the employee name in the sidebar profile block (same layout for every employee); the bottom-left copy is removed.
  * Update125: Employee page - the shared picture was shown at the bottom-left (moved in Update126);
    the 3D profile avatar at the top of the page and the Logout button at the top-right are REMOVED. Sidebar Logout and everything else unchanged.
  * Update124: 3D profile avatar (male / female from Gender) is back at the top of the Employee page, with a Logout button at the top of every Employee page (sidebar Logout unchanged).
    Automatic Email Enable/Disable + Admin-set send time (Update123) confirmed: Admin-only; Disabled = no automatic mail; time = the Admin's saved time.
  * Update123: (1) Admin > Email Controls > Automatic Email: Admin-selectable SEND TIME (saved in the Settings sheet, used by the daily background job; AUTO_MAIL_TIME env is only the default).
    (2) 3D profile image REMOVED from the Employee page (hero picture and sidebar picture); nothing else on the Employee page changed.
    (3) Footer "@2026_Mobius365 | LN_Map_AI" on ALL pages (Admin, Employee, login, welcome) - small, subtle, centred at the bottom, responsive.
  * Update122: Missed Entries - AUTOMATIC e-mail (Admin only). Admin > Email Controls > "Automatic Email" switch (Enable / Disable, saved in the Settings sheet,
    default OFF). When ON, a background job runs once a day (AUTO_MAIL_TIME, default 09:30, app timezone) and e-mails every employee who has missed
    Productivity Entries this month (only dates not e-mailed before): employee name, missed date(s) and the Productivity Tracker login link.
    Employees cannot see or call the switch (/admin/* is Admin-only + the route re-checks the Admin session). Missed Entries calculation is unchanged;
    manual sending is unchanged. Every send is logged in the "Missed Email Log" sheet (Mode = Auto, Sent by = System).
  * Update121: Admin > Employee Info > Employee Login Access: 'Add employee login' form (username/Employee ID, initial password, enable) + per-row Set Password.
  * Update120: large 3D profile avatar (male / female from the employee's Gender) on the Employee page.
  * Update119: Admin + Employee login pages redesigned to the fire-theme reference (dark crimson window, orange grid floor, logo in card, orange 3D button). UI only; login logic unchanged.
  * Update117: Admin > Employee Info > new "Employee Login Access" tab (ID, name, Office Email, status, Enable / Disable Login with confirmation). Admin only; uses the existing Account-locked flag, login logic unchanged.
  * Update116: E-mail templates (Leave/Permission approval + Missed Entries): the data is shown in ONE line (single row) on an orange highlight.
  * Update115: Automatic reminder e-mails REMOVED (daily 1:35 PM REMINDER_TIME scheduler + scheduled missed-entries e-mail + their Email Controls schedule). Reminder e-mails are manual and Admin-only
    (menu, buttons and every send route; employees get 403 / are redirected). All other e-mails (leave / permission approval etc.) are unchanged.
  * Update114: Welcome Page (Admin + Employee) has NO AI voice and NO audio/music of any kind - animation only, then the dashboard opens after 2.2 s.
    Faster Admin / Employee login: no dead audio code on the login pages, no per-keystroke animation, animations pause while signing in, double-click
    protection on Log in, Employee list pre-loaded while the login page is open, Admin dashboard data pre-loaded after login, and page templates are
    compiled once and reused (instead of on every request). Login / password / lock / session logic is unchanged.
  * Update113: Admin -> Employee Info -> Employees (all employees page): subtle centred footer text "@2026_Mobius365_LN_MAP_Ai" at the bottom of the page.
  * Update112: "© 2026 LN_MAP_AI" on the Admin welcome page made reliably visible (fixed at the bottom-centre, slightly clearer).
  * Update102: Admin -> Audit Log (By Process): after choosing a Process and a Month, the new "Productivity" button opens the
    Productivity report for exactly that Process + Month, with "Download Excel" and "Print" buttons. The Excel file (and the printout)
    contain ONLY that Process + Month. The per-employee Productivity page (opened from a process) gets the same two buttons.
  * Update101: the Leave / Permission approval e-mail no longer has the login sentence, button or link (missed-entry e-mails keep them).
  * Update100: (1) Email Controls > "Send a reminder manually" lists ONLY the current month's missed dates. (2) Leave / Permission: when Admin APPROVES
    a request an e-mail is sent automatically to the employee's Office Email ID (name, request type, date, duration/hours, status) in the same 3D
    template, via the Brevo API; nothing is sent on Reject, and re-approving an already approved request does not send again. Every mail appears
    in the Email Controls status board (Mode = Leave approval / Permission approval).
  * Update99: (1) Missed-entry e-mail uses ONE professional 3D-style HTML template (calendar tiles for the missed date(s), 3D login button) for
    Manual AND Automatic sending. (2) Admin > Email Controls: the automatic e-mail has a schedule - Enable/Disable, DATE, TIME and Repeat
    (only on that date / every day from that date); Admin can change it any time. (3) Admin > Productivity log: a "Missed Entries" section below
    the log (all employees, month filter) - Employee Info > Missed Entries still works.
  * Update98: NEW Admin menu item "Email Controls" (/admin/email-controls): (1) Enable/Disable the automatic missed-productivity e-mail and
    set its daily time; (2) pick an employee + one or more of their missed dates and send the reminder manually to the Office Email ID;
    (3) configure the sender name / sender e-mail (stored in the Settings sheet; the Brevo API key / SMTP password stay in Render environment
    variables); (4) status board of every e-mail - Pending / Sent / Failed (with the failure reason). Mails contain the missed date(s) and the
    Employee Login link (APP_URL, else Render's RENDER_EXTERNAL_URL). Mails are sent from this Render-hosted app.
  * Update93: (1) New Admin menu item "Missed Entries Log" (/admin/missed-log, reachable by the links on the Missed entries page; no longer in the menu): every employee with missed dates, a View page per employee (dates, which
    were already e-mailed, e-mail history) and the Send e-mail button + Automatic e-mail switch (moved here from the Missed entries page).
    (2) New process "Training": the employee enters Hours + Description only (no Count, none required); it adds its hours to productivity and never
    has a count target, even if a target is typed for it in Admin > Processes.
  * Update92: Admin > Missed entries has a "Missed entries e-mail" panel. (1) Manual: a Send e-mail button per employee (also on the employee's own
    Missed Entries tab) mails the missed dates to the employee's Office Email ID. (2) Automatic: Admin switches it ON/OFF and sets the time; every
    day at that time each employee with missed dates this month that were NOT e-mailed before gets one e-mail with only the NEW dates. Every send is
    recorded in the "Missed Email Log" sheet (employee, dates, time, Manual/Auto, status) - the record that prevents duplicates. Uses the same SMTP_* settings.
  * Update91: Productivity Info (Employee page) has a month picker - "<Month Year> - Productivity" - for the CURRENT and the PREVIOUS month. Picking
    e.g. September 2026 in October shows that month's complete log (totals + permission requests) with View / Edit / Delete on every entry; after
    an edit / delete the employee comes back to the same month. Employees can only ever open, edit or delete their OWN entries (get_sub -> 403).
  * Update90: (1) Process Entries: choosing the "Other" process shows a work-details Description box; Hours and Count are still entered, but "Other"
    is ALWAYS counted as 8 working hours (5, 6 or 7 entered = 8). Every other process keeps the hours actually entered. (2) Automatic reminder e-mail:
    every day at 1:35 PM (REMINDER_TIME, app timezone) each employee who may submit the Daily Productivity Entry and has NOT yet submitted it for
    today gets an e-mail on their Office Email ID. Needs SMTP_* environment variables (see REMINDER MAIL section). Sheets "Productivity Access"
    (optional switch-off list) and "Email Log" are created automatically.
  * Update89: Leave & Permission - (1) employees can EDIT their own Permission requests (hours + reason, this month's and later records; an edit of an
    Approved/Rejected request goes back to Pending for Admin). (2) Productivity now follows the hours actually available in the day: a 2-hr
    Permission = 6 working hrs, a Half-Day Leave = 4 working hrs (8-hr day). Leave has a new "Day type" column (Full day / Half day).
  * Update88: fixed "Method Not Allowed" when moving between Mahizhchi Sets (game POST routes now also accept GET and redirect; global 405 handler redirects);
    Admin pages auto-refresh every 2 minutes (admin browser only - employees are unaffected); Admin -> Mahizhchi "Connection Game" tab removed.
  * Update80: the old Chat button/page/routes are removed completely. NEW Group Chat icon (bottom-right, employee pages): opens a chat panel for the
    employees who are online right now; join on login, leave on logout/offline; messages auto-delete after 1 hour; no audio.
  * Update81: NEW Tamil BGM on the Employee Welcome Page (original raga Hamsadhwani instrumental: veena-style melody, tanpura, light mridangam) replacing the flute tune.
    Still starts only after the AI voice ends; no music on the Employee pages.
  * Update82: Group Chat can send files (5 MB max, programs/scripts blocked), images/photos (shown inline, click to enlarge) and emoji (picker + big emoji-only
    messages). Attachments are kept in memory only and deleted after 1 hour with the message.
  * Update87 (Fun Friday): EVERY Set is retryable by default (MZ_RETRY_SETS=all): an incomplete Set shows "Try again" and can be attempted again
    until all its questions are correct. All Sets won = "Completed". The FIRST employee to complete all Sets (earliest time their last Set was won) is the
    OVERALL WINNER, announced by toast to every logged-in employee and shown on the winner board / Admin Results. Only correct answers are shown, only after a Set is won.
  * Update86 (Fun Friday): Set 1 (MZ_RETRY_SETS) keeps showing the questions not yet answered correctly - fresh 2:30 timer each round - until all 10 are
    correct; after a Set is won ONLY the correct answers are shown to the employee (never wrong picks). The FIRST employee to win each Set is that Set's
    winner ("Set N Winner: name"); every logged-in employee (MZ_ANNOUNCE_TO=all) gets a live toast "<trophy> <name> has completed Set N first!" and the winner
    board refreshes by itself every 10 s (employee pages poll /employee/mahizhchi/winners). Admin Results shows the same board.
  * Update85: Mahizhchi Connection Game = BONUS round for employees who won all 5 Sets. 16 words, find 4 hidden groups of 4 (env MZ_CONN_SECONDS
    default 180, MZ_CONN_MISTAKES default 4). Puzzles live in sheet "Mahizhchi Connections" (or Admin -> Mahizhchi -> Connection Game paste). Guesses are
    judged on the server; groups are never sent to the browser until solved. Own random word order per employee. Admin Results shows a Connection
    column and Details can add time. New sheets are created automatically.
  * Update84: Mahizhchi quiz = 5 Sets x 10 questions (rows 1-10 of the Mahizhchi Log = Set 1, 11-20 = Set 2 ...). 2 min 30 s per Set, enforced
    on the server; the Set closes by itself at 0:00. A Set is WON by answering all 10 with >= MZ_WIN_CORRECT right (default 10); Set N+1 opens only after
    Set N is won; Winner = all 5 Sets won. Each employee gets their own random (seeded) question order per Set. Attempts sheet now has one row per
    employee per Set (columns Set / Answered / Correct / Result / Extra seconds added). Admin -> Results -> Details can ADD TIME to a Set
    (also after it expired or closed - it is re-opened; the employee gets the added time from that moment). Env: MZ_SETS, MZ_PER_SET, MZ_WIN_CORRECT, MZ_TIME_SECONDS.
  * Update83: Admin -> Mahizhchi (Share / Access tab and Employee Info -> Mahizhchi Log): when an employee has access, "Mahizhchi" is shown as an
    animated running-letter badge (wave + colour shimmer) with floating emoji. Sharing celebrates with a confetti banner and highlights the
    rows that were just shared. Respects "reduce motion" settings.
    Employee page: the sidebar "Mahizhchi" item is the same running-letter badge (white pill, gradient border, floating emoji) and the
    Mahizhchi page title uses the running-letter effect.
  * Update83 (cont.): the employee sidebar "Mahizhchi" pill sits at the BOTTOM of the menu, just above the profile block. The employee Mahizhchi
    page sits on a background PNG (file "mahizhchi_bg.png" next to this .py, or set MZ_BG_FILE); cards, timer and buttons are frosted white so
    text stays readable. If the PNG is missing a soft gradient is used instead.
  * SECRET_KEY must not be the well-known default, otherwise session cookies could be forged.
"""
import os, io, csv, uuid, hmac, time, random, threading, datetime as dt
from functools import wraps
import urllib.parse, re
import gspread
from gspread.exceptions import APIError
from google.oauth2.service_account import Credentials
from flask import Flask, request, redirect, session, render_template_string, flash, abort, jsonify, has_request_context, Response, send_file

from zoneinfo import ZoneInfo

# Load settings from a ".env" file placed next to this script (KEY=VALUE per line). Real environment variables always win.
def _load_dotenv():
    try:
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if not os.path.isfile(f): return
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except Exception as e:
        print("Could not read .env:", e)
_load_dotenv()
# The server clock is often UTC. All app times use this timezone instead (set APP_TZ to change it).
TZ = ZoneInfo(os.getenv("APP_TZ", "Asia/Kolkata"))
def now_local(): return dt.datetime.now(TZ).replace(tzinfo=None)
def today_local(): return now_local().date()

def t12(v):
    """Display a stored timestamp in 12-hour format with AM/PM: '2026-09-29 14:30:05' -> '2026-09-29 02:30:05 PM'.
    Sheets keep the sortable 24-hour text, so sorting/grouping is unaffected; only what people SEE changes.
    Values that are empty, date-only or already 12-hour are returned unchanged."""
    s = str(v if v is not None else "").strip()
    for fmt, out in (("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %I:%M:%S %p"), ("%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p"),
                     ("%H:%M:%S", "%I:%M:%S %p"), ("%H:%M", "%I:%M %p")):
        try: return dt.datetime.strptime(s, fmt).strftime(out)
        except ValueError: pass
    return s

SHEET_ID = os.getenv("SHEET_ID", "1zh_W-ZDLEa3XZCt_a0iw8m5V8VxrUg3pj55FG0ZFJJg")
CREDS_FILE = os.getenv("GOOGLE_CREDS", "credentials.json")
ADMIN_USER = os.getenv("ADMIN_USER", "Admin_Mobius")
# The fallback below only kicks in if the ADMIN_PASS environment variable is not set.
# For real deployments, set ADMIN_PASS as a server/host environment variable (or a secrets
# manager) instead of relying on this in-code fallback, so the password is never committed
# to source control.
ADMIN_PASS = os.getenv("ADMIN_PASS", "H*&hjuiAsi5")
DAY_HOURS = 8
LEAVE_MONTHLY_LIMIT = 2        # days of leave an employee may apply for per calendar month
PERMISSION_MONTHLY_LIMIT = 2   # hrs of permission an employee may apply for per calendar month
WEEKOFF = (5, 6)   # weekly off days: 5 = Saturday, 6 = Sunday - working week is Monday-Friday.
# Idle minutes of no activity before the system automatically logs someone out (recorded as "Auto (Inactivity)").
SESSION_IDLE_MINUTES = int(os.getenv("SESSION_IDLE_MINUTES", "30"))

_holidays_cache = None      # (fetched_at, {date: name}); reset whenever the Holidays sheet is written
def holiday_map():
    """{'YYYY-MM-DD': holiday name} read from the 'Holidays' sheet (short-lived cache so an admin change shows up quickly)."""
    global _holidays_cache
    c = _holidays_cache
    if c is None or time.monotonic() - c[0] > _ROWS_CACHE_TTL:
        try:
            m = {str(r["Date"]).strip(): str(r.get("Name") or "").strip() for r in rows("Holidays") if r.get("Date")}
        except Exception:
            m = c[1] if c else {}
        c = _holidays_cache = (time.monotonic(), m)
    return c[1]

def holidays():
    """Set of holiday date strings ('YYYY-MM-DD')."""
    return set(holiday_map())

def is_holiday(d):
    return str(d).strip() in holiday_map()

def holiday_name(d):
    return holiday_map().get(str(d).strip(), "")

def is_off(d):
    """True for weekly-off days AND declared holidays - both are excluded from working days."""
    ds = str(d)
    if ds in holiday_map(): return True
    try: return dt.date.fromisoformat(ds).weekday() in WEEKOFF
    except ValueError: return False

# Login pictures are embedded here, so no static folder is needed.
PHOTOS = {
    "admin": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wAARCAFoAWgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD6pooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKTdQWA60ALRSbxjOeKC2CPfvQAtFNEinJyMCl3CgBaKTPGcGgMMc8fWgBaKQMD0OaXIoAKKAc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",
    "employee": "data:image/jpeg;base64,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",
}

# Update125: picture shown at the bottom-left of the Employee pages (embedded, served at /employee_corner.png)
EMP_CORNER_B64 = "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"
# Update118: company logo shown on the Admin login page (embedded, served at /logo.png)
LOGO_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAnIAAAFHCAYAAAAlcaEWAAAQAElEQVR4AexdB3wcxdWf2ZMrNpgOxpINmCZLxpZk08F0sCXTIQECBEJCCUmAEJrBpvfyEUpCIJQECBAgWDI1gOm4yE2ywWDAkowpodu4Sbfz/d9Zd77d27vbvdu527t7+u1od2fevPKfsm9mducMwX8lgcC3B2yzQfvY6r3bGqqObW8YdlZHQ/XlbQ1Vd7Q3VD/aXl/1IsKctvqqz3GvbGFFW0P1B0h/sb2h6j7K195QfUpHfdWYjvGVQ0sCPDaSEWAEGAFGgBEIKALsyAW0YLJRq21c9YZwvA5qq6++COFJhI+X91nvexESr0shHxfCuEsJcYUU8hzI+bmQ8iCEnaWUW+DefvSRQuyA9IOEkKdRPiHEA0rK15QKfQSnrgv8m3G+rWNc1ZFLjthxY6TzwQgwAkWLABvGCDACQUKAHbkglUaGurSP32FgW0PVL9rqq/7WXl+9UBriWzheL0oprkM4GmGbDFm7yRYC/xoQ/kEZ8imzq8fXbZjBa6uvvrcNOn1+yI5DkMYHI8AIMAKMACPACGhAgB05DaDqZvnVmMp+5CQh/KO9vqpNqJ6fSSEfllL+SkixvW756fhLIXaQUpwuoVNnjx6fttdXt7TXDzub9E6X1ymd4xgBRoARYAQYAUbAGQF25JxxCVwsvePWNm7YyXDeGlf2M74mJwnhRCFlReCUtSskRZWQxp2r+oW+aKOZunHVtXYSvmcEGAFGgBFgBHxCoKTYsCMX8OLuqK8+ob2+6gV6x00axoNw3uqllL0CrrazelKsJyVm6gwxkxzSzw6rKncm5FhGgBFgBBgBRoARcIOA4YaIaXKLAL3z1t5QdU1bQ/WXSop/Ytbt4NxqoF8aOaThsPygo77qAjVGlOmXyBIYAY0IMGtGgBFgBPKEADtyeQLeSWzb+KoDMfv2jFA924WQl0ghNhPF/CdFXyXlje39q1uX1FfvVsymsm2MACPACDACjIAOBNiR04GqB57fHDp0/bb6qt9j9u0DqeRLmH07HNlDCKmOokqDw7qDKdTb7Q1V9313+JABRWUcG8MIMAKMACPACGhEgB05jeCmYq2OqewJ5+3C5aHeHVLK26UQO6SiL/o0gCCEPO3HcP9ZX42tdNrPTvAfI8AIMAKMQKYIcL5iRYAduTyUbPu4YT9rXxVaCOftevgv6+dBhcCKBCZbrzKMN5Y2bL9JYJVkxRgBRoARYAQYgYAgwI5cDguibVx1bXtD1QxhGI/BYRmSQ9GFJUrK7TpVzzdo2bmwFGdt4xHga0aAEWAEGAH9CLAjpx9jQdtstNdX/UsaYqYQsk7wX1oEMFO50/JQn1e/OGj4emmJmYARYAQYAUaAEShRBIrIkQteCf5v/A792+qrb+gKi4+ElMcFT8NgaySlqF3dU/012FqydowAI8AIMAKMQP4QYEdOE/YdYyt3WWH2WAhn5E+yUDfw1YSNF7ZSihOwJH2AlzxMywgwAoyAKwSYiBEoAgTYkfO5EJUQsq2+6mJlhN6SUm4p+C9rBKQUD/ISa9YwMgNGgBFgBBiBIkSAHTkfC3XJETtu3F5f9YqU8loh+dcKfINWiq1W91K3+sYvf4xYMiPACDACjAAj4CsC7Mj5BGf7uMq9wp1lrXDi9vWJpY9s1DdCqY/A8D2cpwslPsTM4Ve4L5hDCvHrjobqfQpGYVaUEWAEGAFGgBHIGoH0DNiRS49RWgo4GJcLI/QGnLgt0hLrIlBqLljfhnC4CKtRyhTb9g8t27CisUVWNLZuUtHUuj2ud8N5l4qmlh0GN7ZsjntZJr5Zz1zTNbDMVJWGErsj32/A4yGlxCc4B+owlfh7oBRiZRgBRoARYAQYgTwjwI5cFgXw5fiqzdvqq17F7NYVWbDJMKuaiYy3KWWOX69r5QZw0EbAMTsP4dmK51pnDp7S8smG/1n8PWhSHgMbl64Y8uL7nw+c0vr+oKaWd5HvXvA4ZXBTy7Y9V8vNlSmOxSzePUqptpSMcpAopdimY1zVkTkQxSIYgZJFgA1nBBiBwkKAHbkMy+vzQ3YcslrJWVLK3C2lKtGKZdHzycHCLNsoOFznDW6a37jx84t+zNCMlNm2eGneV3DsnoSTeBbCNiA+Ag7dazjn7VBS0Ixh3uSzYEaAEWAEGAFGIEgIsCOXQWl0jK8cuqZHj2nIOhBB76HUt3De7lSmqMOSaDXCreRg6RWayF0KYcJx/M/gptb9QlLuiFnIe6HXikRKrzGe6Q9cWl9Z4TkXZ2AEGAFGgBFgBIoQAXbkPBbq0nFVOyllvAfHZjOPWT2RY+brC2Q4T/b5fhCct3MwM9aM+0AcW02et3BwY8tvhLFmOyj0BkLuDilllzDOyJ1AlsQIMAKMACMQKARYGQsC7MhZ4Eh90zG2urrTkO8IITcWmv6UUF9iput8o8/322AG7LbyJ5es1CQqa7YVkxcuLW9sGSNM9UfovSZrhu4ZnK7GiDL35EzJCDACjAAjwAgUJwLsyLksV/qlBtNQb2EmboDLLJ7I4AitdeB6f781ZuBuDbIDF28Y8FAVU1pvkWa4Vin1fnyatmspN1nSf9hh2vgzY0bAigDfMQKMACMQWATYkXNRNG31lXuqUOg1rOqt74I8AxL1dK/VxraF5MDZjayY8n5rRR9zBOJvE/DocNZ6KCH5owetCDNzRoARYAQYgUJAgB25NKVEM3FCGC+DrA+Cv4cSP0kVPqGisfWoLV6a91OMeYFeyCcXrMFy8HlYGj5bvwnyQP0yWAIjwAgwAowAIxBsBNiRS1E+HfXbb6UMowkzcb1TkGWYpGaUiXBledOCRzNkENhsWGq9Rylxo24Fl9QP21m3DObPCDACjEAhIMA6li4C7MglKftPxwzpbYqeLwspN0lCknm0Ug+XN7buOrBpQXvmTIKdc3BTy4VCqcd1aqmEGqaTP/NmBBgBRoARYASCjgA7cklKyOjf70nMxO2UJDmz6Mi7Y2pCRVPryVIIMzMmhZOrfHnridBW2/YkShhV4M9HXhBgoYwAI8AIMAJBQIAdOYdSaG+oukYKWe+QlG3UzysaW6/Jlkmh5JdTRdd6XSsbhBIf6tFZ8oycHmCZKyPACDACjECBIFAwjlyu8OyorzxeCHmJ8PlPKrUvZuK0LjX6rLIv7OjnwwxlatnAVwnBM3K+lBIzYQQYAUaAEShUBNiRiyu5tnHVtaYw/h4X5cOlMg1T1Zc3tU71gVlBshg0Zf5rQqgn/FZeSrGNOqayp998mR8jwAgUBQJsBCNQEgiwI9ddzJ8dVlUuDfWilLJXd5Q/JyV/NWhK6xR/mBUwF9l5LrT3/Vcqlq5UPCsHYPlgBBgBRoARKE0E2JHrLvdwWD4pfP7pLaXExRVNLQ8I/hP0c15YXp7oNxRhZWzqN8+M+XFGRoARYAQYAUYgxwiwIwfAO+qHnS6k2AWX/h1K/WVwU8v1/jEsfE6DlrfeppT6wFdLpBzgKz9mxggwAowAI8AI5AgBP8SUvCP3xUHDNzOFcZMfYMZ4KDW9oqn1zNg9X0QQkFNFV5kSp0VufPqnlNzAJ1bMhhFgBBgBRoARKDgESt6RW91T3SWl8M0ZUEKtEWFxfMHVhBwpvNWU1neA0dt+iTOkyTNyfoHJfEoAATaREWAEig2Bknbk2sZVHwAn7mg/C9VQYkLF860f+8mz2HgZSj3ol01K8oycX1gyH0aAEWAEGIHCQ6BkHTksqa4HJ843h4KKXik1Z1BT6y10zWEtAk7/Q/K7R4HVKqc073Gyr/c8nIMRYAQYAUaAESgOBErWkVvTU10vpNjKt2JUoquHEsdLIUzfeBYpo4GNS1cA+3/7Y57q6Q8f5sIIMAKMACMQAARYBY8IlKQjt2Rs5Qgh1NkesUpNLtX9A6e0vp+aiFOjCISE6cu2LErJHlGefGYEGAFGgBFgBEoNgZJ05MKGcZeQEpNnPhU31gl7dHZd7xO3kmAzqHHBqzB0KUJWB0qRHbmsEOTMgiFgBBgBRqCAESg5R66joXofKeXu/paZbNzyhQ8W+8uz+LkpYd6XtZVK8NJq1iAyA0aAEWAEGIFCRaDkHDlMnvn+g/hChW/2UAGYNIaAeiJ2memFVGWZZuV8jAAjwAgwAoxAoSNQUo7cZ+MrR2JJ9SB/C03Nq5iy4E1/eZYGt8GNC+bDsf4xK2uV4KXVrADkzIwAIxB8BFhDRiA5AiXlyIVN47LkUGSYosS1GebkbEAAy9zv4JTxoYTsyjgzZ2QEGAFGgBFgBAocgZJx5DrGVw5FWR2O4NuB2aTV5X1afdpGwze1CoqRFOLdbBRG/s5s8nNeZwQ4lhFgBBgBRqAwECgZR85UxkQsq+K571/BgNlU+aQI+8ex9DiZUmXlyAkp2JErvWrDFjMCjAAjwAh0IxAQR65bG02nzw/ZcYgU8kTf2UvxX995lhjDPj+a2TlyQvn0CxElBjybywgwAowAI1AUCJSEI9dVFvqNjtIKqTDthaaDdcnw3GzqguVCiZZMDZZKfZdpXs7HCDACBYwAq84IMAIRBErCkVNSnhCx1sd/Sojvt2p6f5aPLEuXlVQZf/CAsv2mdIFjyxkBRoARYARKHYGid+Q6xlbuIoQsF77/qVd8Z1miDJWZxXtySubKkSvR0mGzGQFGgBFgBIKMQNE7cioUOk5HAUiheFnVJ2ANaWY+IyfMr31Sg9kwAowAI8AIMAI+IpAbVsXvyAl1vA4olRRzdfAtRZ7lTe9/pJTKbGNgQ3xbipixzYwAI8AIMAKMACFQ1I5c5HdVhdycDPU79FDfzfabZ0nzk+KNTOzvoQxeWs0EOM5TlAiwUYwAI1B6CBS1I4dZnp/pKFIlxFcDG5eu0MG7dHnK+ZnYLrtWsiOXCXCchxFgBBgBRqAoEChqRw4ldDSC74dUaoHvTAuSoX9KS2V2ZMJty+cX/S+TfJyHEWAEGAFGgBEoBgSK1pFrHzfsYCHlJpoK6X1NfEuXrVKeHTnMuH5euoCx5YwAI8AIFCACrLLvCBStI6ekcZTvaEUZKrEkeslnfxAIhYRnR04K2e6PdObCCDACjAAjwAgUJgJF68hJocZoKxKpftDGu0QZG51rPDvHSirPeUoU3lI2m21nBBgBRqCoEShKR67j4MqNsKy6na6Sk8L4XvCfrwhE3nVTossLU8zIeZ7F88KfaRkBRoARYAQYgaAjYARdwUz0Uz1De2eSz20eM9WMnFsmTJeIgFSLEyNTxCjvy7EpuHESI8AIMAKMACNQcAgUpSMnhNpDZ0lI0+SlVQ0AK4+OmVd6DSozS0aAEWAEskaAGTAC2SBQlI4cHvC7ZwNKurxShXhpNR1IGaRL6e3jBUOF+WOHDHDmLIwAI8AIMALFg0BROnJwCLQ6csII9ymeKhAkS7x9vCBV2WdB0r5wdGFNGQFGgBFgBIoFgaJz5NrqK/fUXThKyQ11yyhJ/t62dQkPen4ef7VakhWFjWYEGAFGgBGIIpATRy4qcPDTvAAAEABJREFULBdnQxi76ZajDLmBbhmlyN/w8o6c8vhhRCkCyjYzAowAI8AIFD0CRefIKSH20l5qphygXUYpCpDyW7dmKyG9feHqljHTMQKMQBAQYB0YAUbAJQLF58hJub1L2zMmM6TiGbmM0UueURruHTkh1KfJOXEKI8AIMAKMACNQGggUnSMnldhId9EpKXhGTvj/F1olvnPLFeXsryPnVjDTMQKMACPACDACAUKg6Bw5zNRsoh9fubV+GaUnYfOX5v3PtdUGz8i5xooJGQFGgBFgBHxHICgMi8qR+/aAbTYQUkrd4CqlRuqWUYr8UXAKjvhyN7YbIsQzcm6AYhpGgBFgBBiBokagqBy5NX16aF9Wpdogpdyx45hBfeiag88IKOHqg4ce0mRHzmfomV3QEWD9GAFGgBFIRKCoHLnVZs+cOHIEo7FiAM/KERD+h7TvyWFGdNXmk1u/9F80c2QEGAFGgBFgBAoLgaJy5KRUG+cKftMQtbmSlS85eZKb1pHDjOjHedKNxTICjAAjwAgwAoFCoKgcOaFUzmbklBBjBP/5j4B0sbSqBDty/iPPHBkBRoARyBYBzp8HBIrLkTP0bz0SKyMlD1G1tT1i93zhFwJpZ+SEFJ/4JYz5MAKMACPACDAChYxAcTlySpo5Kwwp+i7ZfOX+OZNXOoLSO3LKXFQ6cLClKRHgREaAEWAEShyBonLkpJDLclmeyjAOy6W8UpDlpgylMPiLVcF/jAAjwAgwAoyAEEXlyJnC/FFzoVrZSzneGsF32SKghEjrjBuG5HfksgWa8zMCjAAjwAgUBQJF5cgZ0sitIyfEwPaxVXVFURMCYoRUZlpHbuDkeR8FRF1WgxFgBBiBNAhwMiOgF4Eic+TCuXbkMKcpT9FbRKXFXaVdHlcdUojcvQtZWvCztYwAI8AIMAIFhkBROXJd4dAPOcdfilO/O3zIgJzLLVKBUsrUzjhvPZK25JmAEWAEGAFGoHQQKCpHroexOrUToKdc+ywL9ztbD+vS46rMcLrfWuUPHUqvWrDFjAAjwAgwAkkQ8MGRS8I5D9EDGz/8Wgm1JteilRDnqGMqe+ZabjHKM1S6jx0U7yFXjAXPNjECjAAjwAhkhEBROXKEgBRiLp1zGaSQm3esME7MpcxilWUqI/XHDpJ/1aFYy57tKiEE2FRGgBHwDYGic+SEEi2+oeOBkTLE+R7ImTQJAj3EqnTL47wZcBLsOJoRYAQYAUag9BAoPkdOytZ8FCNm5SrbGqp/kw/ZxSSzq9+qlO/IGWXhTJZWiwkitoURYAQYAUaAEYghUHSOnJIqL45cN6LXf3vANht0X/MpAwTKn1yyErOqXU5ZlVI/Dnrmg2+c0jiOEWAEGAFGgBHwD4HC4VR0jlyfLjMvS6tU5FKIAcv79L2FrjlkjoASaoVjbsm/6OCIC0cyAowAI8AIlCwCRefIbfbcgi+EUt/mr0TlafxrD1mj/5MjB95DzhEWjiwOBNgKRoARYAQyQaDoHDkCQUnxDp3zFgz5yNKGgX3zJr/ABWNm0/k9Of5itcBLltVnBBgBRoAR8BuBonTkhJJv+w2UJ35SbN8lNnrAU56cEwdXoBLiJyftDGV+7BTPcYwAI8AIMAKMQKkiUJyOnAi/lf8Clcd21A87Pf96FKAG0tmRk0rw1iMFWJysMiPACBQJAmxGIBEoSkeuos+Cd4USjl8+5rIUTCHvWDquaqdcyiwGWXDYnGfkpOIZuWIoYLaBEWAEGAFGwDcEitKRk0+KsJJqmm8oZchIStm7yxCTO44Z1CdDFqWazcmRCw9sWtBeqoCUqN1sNiPACDACjEAaBIrSkSObpRD/EYH4k0PNVRs2qUOH9gqEOgWghHJYWlVKfVgAqrOKjAAjwAgwAoxAThEoWkeuTKx5UCnR6QlNTcRwKvdrL+vzHDtz7gAGXokzcvzFqjvwmIoRYAQYAUagpBAoWkduYOOHX0upGoNSmnBO2JlzWxhKJThyUkj+0MEtfkzHCDACOUOABTEC+UagaB05AhYP//voHJQghdivo6z3m58fOnTToOgUTD2MBEdOKJMduWAWFmvFCDACjAAjkEcEitqRK29seV4INS+P+DqIlqM6y/rM+ax+pxqHRI4CAlKYCRsCS2l8giQ+BEPACDACjAAjwAisQ6CoHTkyUyp5MZ0DFgZ2idDbS+orjw6YXoFQx2lDYFOE+YvVQJQOK8EIMAKMACMQJATSOnJBUjYTXcqbWp4TSryZSV6deWhrElOGnuyoH3adTjkFyVsmLq32EN9/WpC2sNKMACPACDACjIBGBIrekSPslBLn0jmIQUnjovb6qjlth1ZWBlG/fOikTNsvOyj19cDGpSvyoQvLZAQYAc8IcAZGgBHIIQIl4cgNntLSLIS6P4e4ehMl5c6izJjdXj9sghojyrxlLj5qQ9ocOSkWC/5jBBiBokCgraFyWFt99UXtDVUvtddXL2yrr/qhvaF6RVtD9aft9VVv4v7GtvrKPdUxIlQUBrMRjIBmBErCkSMMe642fq+ECOzynBSyp5DGVe39q6e3oaMjnUs1YEbO/rFD6g8dShWoIrB7+PDh69XV1Y3REEYXATxFZUL72Kq6toaqt6QItUoprhNCHiik2F5Kub4Qoo8UYoiQck/cXyBl6M32VdUftY8b9jP020gS/McIMAJJECgZR26Ll+b9FFLiBMzMmUmwCEQ0eqyRQoVmdzRUX67GlOrsnLIvo/KHDoGonf4r0aNHj23QCb3md0A7+of/2jLHTBBYMnbH7dsbqh4XhpguhdzDLQ8pxNbCMB7raKia3jZ+mOt8bvkzXWkjUEzWo/8sJnNS2zKoqeVdpcRVqanynyql6KGEuKKjX/XsJfXDds6/RrnVoCwkrTNySvHSam6LgKUxAr4gsOSIHTcOG2UPCCGPFVLCNxMZ/Mk6YRoP83vEGUDHWUoCgZJy5KhEBze1TlJKPEnXgQ9SVIWFMaOtYdgVqra2R+D19UlBZSjLhsBSyKU+sWY2jECeECg9sR3HDOpjdpW9KqXcPVvrpRTbyFBo6mfjh++QLS/OzwgUGwIl58hRAVb0afm5UOotug56QAfWQwrj8o6Ba2Z3jK8aLkrgz1xlWhw5JdWSEjCbTWQEigYBJYRhrhqA5W3pX58lxaZdSj377QHbbFA0QLEhjIAPCJSkIyefFOHey81DhRKtPmCYKxbDlJKz2uurHuoYXzk0ndBCTh9krLE4cuYakx25Qi5Q1r3kEOgYN+xYKeRRfhsuhdhheZ++N/jNl/kxAoWMQEk6clRgm01dsFwpsbdS6l26L5AQElKepFTog/aG6geL1aGTzy9aDSe7K1ImSnQNefH9zyPX/I8RYAQCj4A6dGgvJeX1+hSVv2oft1OVPv4ly5kNL1AEStaRo/IaPKXlu4o+5hhcP4tQSEcIyp7c7dA98EXDDlvjvqgOJaJfrip+P66oSpaNKXYEOoxeR0gpB2u0MySM0G818mfWjEBBIWAUlLYalJVPLlhT0dhyOFjfjlBoBzl0p6wRPT/BDN0DbeOqtyk0A5LpiwdB5MtVJQQvqyYDqdDjWf/iRMAwfqbbMKymHIa+ASutuiUxf0Yg+AiUvCMXLSI4c+cqZY4XSn0bjSuw8ylSioXt9VX3F8cMnYrsJYee+ssCKwdWlxEoWQT+N36H/nCyxuoGQEq5xWcNw3fRLYf5MwKFgEApOXJpy2Nw0/zGMrlmB6HE5LTEQSSQokxIeeoa1fPD9oaq+wrZocPDIDIjJ3jrEcF/jEChILBa9RompcjJVklhM7xroeDCejICOhFgR86G7sDGD7+uaGo5TKrwCXAmvrMlF8athEMn5GlYcv0IM3ST2xqq6lWh/W5h9PdWleJ35Aqj1rGWjIAwhdoiZzAYRg5k5cwaFsQIZIwAO3JJoCtvWvCo0RkeKpS6RSm1KglZ0KNDmKFrkEI2dqysXtzWMOyKjvrttwq60qSfVGLtFiQGbwZMeHBgBAoCAaVy5lxJoQYUBCasJCOgGQF25FIAXP7igm8rmlr/qDrD2ygh7sWS69otMVLkCWySFIOkMC5Xsmd7W33VlPaG6sMDPksXceSUVJ+JEvpjUxmBQkZAmubiXOmPFZMvciWL5TACQUaAHTkXpUP7mA1ubPmN2dlVAfLzMEs3HecCPaQhpaSXkZ9pX1nV0d5QdfVnh1WVB80YJcXad+Q6TXbkglY4rA8jkAQBGSr7PkmS79FSCHbkfEeVGRYgAoIdOQ+lRg5dRWPLbZil28XokuWYpbsIYbYHFoEihUO3pRDy0nBYtLXXV724pL7yaDVGlIkA/KGTjny1KowQbwYcgPJgFRgBNwhs1bVitlJqtRvabGkMaczJlgfnZwSKAQGjGIzIhw2Dnp+3BLN0NyDUSNW1PRyPiUKoRfnQJWuZ8OiElAeZMvRke//qz9oaqq/P+550StCM3EratDlr+5gBI8AI+IdACk70qyzoC6emIPElCcuqP2zVOG+aL8yYCSNQ4AiwI+dDAZY3vf9ReWPLlRWNrdsJs6taKHEVRqVtPrDOOQt0wpshXCgN8XFbfdWrHeOqTsy5EhCoBDly/H4coOCDESgoBND3vaBbYSnUC+in0E3olsT8GYHgI8COnM9lVDHl/daKppbLBze1DgnJcA16mhsQcvYCsJ/mYKJuX2XIf7TVV3+Lpdf7EQ5SOdrGREr1FRxi+lUHP01iXowAI6AZgZ7m6keUUMu0ipHqFq38mTkjUEAIsCOnsbC2mrxgNpZeL0LYuqdYs41Q6mcIt8BBeRMh8lWmRvG+sZZSbCikPBXhxY6VVV+0N1T9Zcm4YfvCQcWg2DcxFkZg/KWSgh05Cyp8wwgEH4Etn1/0P2Gqy7VpqtTjFY3zZ2jjz4yLAIHSMoEduRyV9xaNCz+taGp9HOGPmLHbG6GfocwRUqhfCaH+ijAzR6pkJ0bKTYSQvzEN41XM0C1tr6++s62+ck/h859hys8NpdiR8xlXZscI5AKBiinz70Cf9rLvspT6qEyu+a3vfJkhI1DACLAjl8fCG9Q0f255Y+v9FY2tZyCMqmhskYYSuyulfo+liX9ixms2Zu7Wfr2ZRz2TiZZSbiGkOFvK0Jvt9dUd7Q3Vt3aMrfTl9w+VabTDfnbkkoHP8YFCgJWxIoAZdXO9rlVHw5mbZ03J4k6pr6UIjxvY+OHXWXDhrIxA0SHAjlzAinRQU8u7g5ta7xjc2PoLLMnWYOZuvZ6r5eYhU+2hlHkyHLurEB7FEu10hG8Do74Ug6DLuSoUeq+tofpThOs/G185EnEZHVs9P+8zOHLtGWXmTIwAI5B3BDZ+ftGPZWLN/uin3spWGfQFi8uk3Ku86f2PsuXF+RmBYkOAHbkCKNEtXpr31VZTWt8Z3DT/YTh2l1c0tZyAJdpdEDbut/KnATIc3lUI83ihzMuEUg8jvIUZvS/zZRpG40MQLgyr0Kz2hqqPEK5eOguPVWkAABAASURBVK5qJy/6IL/qv2rlG17yMC0jwAgECwGaPSvvY5Iz9wD6JfhjGeinxJuhss66gY0tH2SQm7MwAkWPgFH0Fha5gRv995Mfyp9bMK2icf5jFU3zr65oaj0ZYS/M6G1RJr5ZT0q1szTVUVKZF6IXvRfhVXSomOlSZm6gkUOFkJd2GXIBHLq5bfXVFy0du9Ng4eKPbHNBxiSMACMQYATkkwvWoE86VZhiNAaYb7tVFX3VQuq7ypta9hn0zAffuM3HdEkQ4OiiRYAduaItWiEGNi5dUT65dV75lNany5vm34il2t8g7F/R1Dq4orE11EuqLVRXeJhS4b2kUkdKZZ6ulLhYCHUzYHkQDl+jUupdLOV+iDgfOlI5XEpxXVeobHFbfdU7CL//4qDhm0EWH4wAI1DkCFQ81zoTA8w9y0xVCSftIvQpL1Pfgj7mR5i+EnGL0ee8hfibRVjsU9G7ZRj1XTQ7j3Q+GAFGIAkC7MglAaYUojef3Prl4OcXLBjctOCt8qbWZ8qb5t83uKnlejh5F1Q0tvyyoql1/OCm1t0rmlp2QNwmiJNGWecmISl3pHf2pBLjBJZ00QGfIZX6Ezrh6+AIPgLs3sD5E5yTHlLK3RBuX9NLfdlWX/3fjvphv/r2gG02SJqBEwoNAdaXEXBEYOCU1vcxoLwBfcpB1Legj9kAfUtfxG2NPmcvxF9Q8VzLG/JJuHOOHDiSEWAE4hFgRy4eDb5OiwAtcWw1ed5CemevvKnluQos6aID/mt5U+tNFU2tl8ARPBGd8j44b4uz7B9atqFUXdvT17jCDB9G263A8btIKAWnT92B0fh9GHF/qaRRv6x330c+O6yqPK0STMAIMAKMACPACDACEQSKx5GLmMP/gobAhv9Z/H150/sfDWpqebdiyoLJ5Y2t98Pxu2Gt09f6+8FNradXNLWcUNHYcjiu67d6trUj3oaOhup92uurnsas3UycX2xvqH60PbJ3XdWkjoaqczrqK49vr6866LP6nWro3bsvDhq+Xnx+vmYEGAFGgBFgBIoZAXbkirl0i8C28saW1+H0HSkMdbGQcn2Y9HMR2btOTlRC3qFk6BEh5YthWdZM795hqXZ5e301QtWH7fVVr611/Kpuxvlc3B/XVl+5Z/uhVduCDx+MACNQ4giw+YxAMSDAjlwxlGIJ2DB4cuvLmLXbTYbDhwolpqU0WYr14NxthzAGdHD85Pk434r7f0kZelOUyUVw7FRbQ/V3bQ1V89sbql5qb6h+sL2h6ur2hupTaFPjr8ZU9kMePhgBRoARYAQYgUAjwI5coIuHlbMjUP7cghewFLurFGKMUuo1e7qXe/AYIIWsFEIeKIQ4WQh5qRDiARUKvbeqf2hZO/1aRX3Vix31Vbe3jav+dRtm8zoOrtwINBkenI0RYAQYAUaAEfAXAXbk/MWTueUIgXIsuQ5uat1PSXNPodRLWsRKMUhIeZCS8vfSEH+VmM1TPUPftNdX/a+tvurV9nHVl7WNH7aHFtklwlRKqTSZqotvgrojRowYMnrkyN3q6upGI+xQW1u7JULfBEKOYAQYAUbAKwIu6AvSkRs1atQW6DBHIhw6urb2V+g9Lx1VWzsB1+cg7heja2rqa2pqal3YHziSHXbYof+oESN2hx3jR9XUnFhXU3M2wiWwcRJsvAjhTNh5PMI4PDzqAmeADwq1j6vc69MxQ3q7YTV48vy3K5paDzaE3E0p8V83ebKmkXITOCD7CkNcKZXxVvvad/Imw7n7fVtD5bCs+TODwCEAx+wgtMFr0O4eQnhxVF1dK+6/QVA9y8o+FaHQO4YQ0xA+CEm5FOEn0C0bVVf3Ns73IZw3auTI/QNnGCvECDACrhDAM/kAPH+vQJu/H+15Cq6bET7DvYoG3P8PYRFCM9r+8zhfi3w/x7N6Z1dCMiRCv5Nhzhxlg1N2MAC5E0DNAChLcVZSqc+h+CyE54SUf4MqV+PBehWu70Dcw8IwGssMYybRAvCZCPcRmOiMAzdKRue+N/S8BjY+j9C+Qf/+P8qysrdhx7PSMP5hGMadCNfAxomw8TqEu2EnveDfhIfHDORVsG8u8v4L53NGjhy5KWgL+pDC2LSsb19PFX9Q47z3Bje1HCiFGCOUaBW5/Fv7Tl4DyuZ2KUKtcOy+am+ofrRjXNWJX42t3ELwX8EhgL5iAxpIoV39G/3OcjhmL8KIS9D2TkI4CPWMHPbUy+xS9gPd7qA/DeEWGQr9F+11BXg+i/NpAW2rMJOPUkMAs8oD8IwcoyOMAvNCxHO3ysqN0E5PQnt9ivoAPJNfRh9/OWw5Fe15LK5rEAbiPnbgngb52+Jcg7Z/CM4XI9+jeFbPAa8fwedxYPyzXXbZhT7ci+XL9sIYNWrUPmDsawHC+9wtU8Wqq6s3hMEnwSn5D84r4JS9AEDOBr86gLIlzt4OKWsB+mkEJjpjGiU/AefwCG9M/KUm+bDtYRTqd+jcXwf3S2DjIQiZ7aEm5XDkPQ523tEjFPoqUvFqahrAtyAP0xBlypAZzTbSkmt5UwucQPNsLLl+K/LxJwU50z+HDf9YFQp9Dqfu3faGYWe1javeMB/qsEx3CAwfPnwztMtz0fe8ir7iexpIoV0dhX5nPXccXFH1Ac/xoLyvu61Ox4z7BX537OCf16OysrKf388V4gcHuyZfhlEZkQ5+h3zaFMWyrKxsBJ6Rr+kIoqzs9qicQjjvMnJkJfqBh8N9+9KvGT2E9nqkT31Af/A5Fhg/psLhH9DPTEE4xg9MDMxuTQVjXwsQzteTXpXD6PcUOCCv9+nVix6+D8EpOQw8+iD4e0h5DPR7GgB+inCyv8xTc0MHcCpkfkryQfkLFOoAnH0/IhXPMCbDUVwKeedRp+q7EL8YOvAJKdMUAg64yOwP9psVjfPvlp3mdkKou8EljJDPY1chjLuEob5or696pqO+6gh1TGXPfCrEstchMGTIkN5wpi7p1aPHp4ilr5v3xTknhxRiFGbcbzS7utrRXi8jZyEngjUL6du373Z+P1ci/KS8R7Pqydl3dlZGdBDC1+elkU+bkltbcimjR46sgw/ylAqF5sP4XyDoPaQcCz/nCTyjv62rrb1ll6qqzTMViHqZaVZ/8mHadXcYMhej3wfQqe3tD1cXXKQcAhAfRMG1w4k80kWOjEmiDhzAvh8yh2TMyGNGOIpbQt4t/fr2XYqKcj1Gfpt4ZJEXcqUMU0hRm63w8hcXfFvR2Hq26goPV0K9nS2/bPNLIXsKKQ9XUj7dsdL4HE7d3UvqqzOevc5WH84vBEbeJ2268cafwJm6Bu0lb69eQPYGCFdGHTqsRmkZ5HGZZ46AUkpmnptz+omAn7xoIAcf5B4RCs1AAWv1BRz1lnJDOPPnmb16TYceGc3QwbdwZK09Ek7FllD6UVlW9rbA0qB2gUkEoODK4UQ+BV0e8nvmCjbWYJTdDJBz6sA5mNofFeXCkJQL4VTSso4DSXCisCRpQpsqNUaU4Zz1Mfj5BQsGN7buqUxxLGboLL8ckTXzTBlIuRHq/ZmmFO+0N1R91NFQfTn9MkWm7Ao1n8aHI5p2clTQDvbAIK4FFA/BgdoS50Ac0CXi0PUoK1uEAWbhvh5hmuj2tECasly1SOxmaoZCWmyCQVr4dqsdhBNMDIIaiTqM2nnnYZtusskc9MVnJKbmNgZtvwJ6PIF+6S3MDu7sRXrOK9DQoUN7wbmZAMEfQemfe1FWK62UJ/Xr06eVZgizlUOjaYz0/wIbZ6Bw8vZOh4MdG0GnZ1FRHtutsnIjh/RgRJlhOHLSWNK3MutZuXiDBk9peVL2/n4HzM79WcCDiE/L77UcqoS4ossIfYpZumc+G185Mr/6FK/00TvvvD3q/2S0g7fwdKlyZ2nuqaDbxhhgToauf/d7gJl7a1giIxA8BOCH/F6UlTWjre0QJO2gzx6YHWyGDzEJeqGrwv80hyuiNDxcJ2OEedyGG2zwIZybqxD8fIHYtQ4pCaUcTDOE0POElHQpEjHSH92zrOwDkPwGNuYUX8h0daCi/Kyrb985tbW1gfypKmVgaRWWqJD01ZEDS1H+5JKVmJ37XUiJPeE8Laa4wARUGAxuDg+r0Ky2+qop7WOrMvrgIzD2uFAEJqMYXBB6J0ngi3Z9nOjRYyHqf8HMdEHXX67Xp898+ijNOwT5y6GxXPNmFMZ+KA7/xaOi4vCfb4A4Bso+WkqFE9eIOno7Qq8A4RSvSgg3E7FSOBXP6bQrBjlzNEbX1f0ZI8x/AbgKKBjsQ8p/wCE71auSAP0MqdSbyJfxS4vIK3IR0COVo6a8Q1/o5EKeFxmGkpiRQw7lvyMHrpFjqymt7xi9v6tEef0fllvXyoukBOMf2slYEZIz2uqr/4tl132CoZX/Wuh6OEJTVHH87z7QNi+Ek/xY921BnVAXKoRpvoaHz82YnetZCMprLNe8mR/S9I4cKiqOvJmVC8GBsW/MmDFlWEolJ64+F4ZnLUPKvfCcno/+a1wqXjlx5NAB3QslfotQEAc6Tglg7ofeZ7pRmJaLATTt7XYP8hZERxuxS8rNTMN4e5eaml0j9wH5p5QZ/crU9xm5eBNpdq68qfUPIVPsBWduUXxaUK6lFPtjODu1vb76jbbxVfRTYkFRrVD0MNCO74YTd73EX6EobdcTqtNx/np9+74GZ45/B9gOUA7ulSZHzifVmU16BIwVy5Y9Ca/ygPSkAaKQckP0X03ox5L6I/BX9CoM4fdKKU/XK0UPd+h9N2bmaBuUpALQqfbccMCAlwD08UmJApwAGwdgKfOlXYYPHxQUNVWoe0ZOSk8vfGaqP83OhZctrxbKvDVTHtrzSbGXVPKltvqq2R31VWO0y8uRANQ/+KlahKnIEkpdXRNkJO0AtUjWyBQPod3hzL26i88bimpUmVkzAoFAAKuCD+I5fXgglMlACfRjd9fV1PzBKatWRw7A/QXCC9KJi4IFgGiZdZvovf2MTpU8/Nxtm2JXwJ/7/mbPno/7wyp7LiHTjC11dtRXjs6eY3oOW09dvKqiaf75UoV3CersHFmB9jRCSflaW0PVw0uO2HFjistLCLhQLJn3wxLKG3B8Dg24qp7Vg02jVFfXq/RRlefMOcqANhydVfdVIso11jf4ytgFM6xe6JGtlBasXJiUKxJdgzXX+mPF7Fcg1r83HIToPAzDuA1+1bl2GfBT7FHZ36PUJM3EgdNvEAr96I+O899ORoyqq3sMaYHfzsNJd3sc7NgdZXatPT4v99F35CBcKUPr8ipEWI7ypgXTaXYOyyg3ISGwHawU8hfhzh4fddQPO53aG3TlIx4BKbeSQoyKjyqqaylre5SVvRZkZ66o8IYxGET5sh0SWPGRQwRGjhy5KfpI6s9zKFWrqFsjH27FidDiyKHCD0TwcyYuTuXcX+KBMBJOzuXxknF/HeJ/Fh9XBNcXYik5759iY6l33cjXEDl15KgMaXZucFPrnwwl9hIKqKG9AAAQAElEQVRK/I/ighikFBsqadyLpdb3lo6r2imIOqbTCQ4zmlE6Kk53QgDAjegZCj3ilJbvuLBhhHTogNloLc8sN7pqq6tSasHKjU05okFVzZEkBzE9QqFbpJTFtcG2lH+vra3dMWpu3hpFVIECOv+JfouR9MU07ThUjIvoupgCbKKfbLs53zapyD5ya7VQKveO3FrJQgxqanm3l6GqhVLTo3GBPEs5ukvKee0N1acEUj9WSh8CUo6tq6m5QJ+AQubMupc6AqNHjqRfzin4JVV7OeJZ3RfOWxOcuQ0oDdd04pAOAQC3Xq+ePa8CcLR9yr/S0RdqOuysh4175lP/kDBiS5rQZ0Q+ddl8cuuXFU2tu4ggfwhBAMnIr2A80F5fdTfdcigdBAzDuBYz6Tl5l7R0UE20VNf2I4mSOMYvBFQodJVfvALHR8pvV65cGXlWGoFTLsAKSSF+bUhJX6gW9ef/ISHOz2cxmJiSi5ffPrY67x+TVNCHEMI8GkutP8XrFn8diGspz2xvqJracXCAf7kjDig46iruli8zQ6DMUOqJESNGBGb5CM7lutcjMrMpWa681ZewlFpkg6kurJJhmOt4mJhrkUKMGjVqCzyz98+9ZP0SAeg7P61Ysd+CBQuWkzR25AgFDwEVI+/vkHlQN1NS2mcnb3VDxc3IRQwIqYMj5zz/K2+c/5Q0wiOEUh/lWZU04uU+qqcxp62hclgawrwna3vvKO+W5VgBKQcH6X05swh/axWDDoxx/S9XPFPy1tf6b40jR5joGK81UioVnJ8ATW6p5xQ4cTPgxB0cdeKIQbFXILKRg1cEpOxXU1Mz0ms2v+gNYXbZeB1ku8/bbfnkBYvK5Ldw5sTkvCnhSrAsF8J4t2N81XBX5ExU+AhIOXZUbe3vCt8QtoAR8AEBpTL+qU0fpGthASfOMhMXFRJoRw6j9aVQfDZmQN7E+Yuo0nzWj0CZYeRtOTMcEp1WC2Xd0obtN7HG5e9uYOPSFRVNLYcJU/0xf1qklyyF7K+UeHVpQ/WO6anzQ4FZDjTt/MguRqnA8/9GjRgxIqltOUooxqVVXdChAZi6eAeEL0zMrSajd955eyFlbW6l6pUGEN9evWbNQfEzcVGJgXLk4Lg9iBp9Ulip4dNnzpQzmpu3mjFzZs305ua9cd5y5erVGyFtPyh/Hpy793Au3EOpabD3HoQLlGn+QoXDB8D2fYVpNuD+VBh2IQquEef8HErl7fc9e5gGoLCa3WX2oOVea2Se7yqmtN4iw+FDUYar8qxKCvFyY0xvvrLk0OD8ckcKZQOfhDb5BcIMKDoT4UuE4B1lZX/Nt1Kyqwsw+a8Flsu08PVfU/cci9Em99broVSh0B56ONu4KtWG/r8JsdeiYt6uzS9R6k04cQfPmzfP8R3tvDtyAGEFQLhwTVfXhnDcfjlz5sx/NDc3tyAu4WhpafkOaa/BybsNzt1ueNrvCeCeTCAMaoRS5HyeDP0l9N8V9p6FcPOMWbP+OWP27Fdg+9Tps2Y14f4B0NwI53U8Oa+madLv1P6YS7NQKf34GaiMVDZVVzgho2EE4j05u17lzy14QSi5p1LiB3tagO4HhkPq9cUH77RlgHQKtCpKqRVoA8+jfzkfg8ddlZQVaJMSbXJLhNG4HoWwBYKkNGmauxEtwnOUN5/GSSFGj66pyWt7UWVlUMN/FIC1Fr4uNdUiO882uTS9wMik3EqXxugXvjGVukGsWbMNnuND8AxvQD9wKfqFc3G/G64l+oy90A9cAh0+RcjugBO3qrPz0GROHDHPqyMHQ18WhrEjDL9xzpw535NCXgIcn7cB3LEAbSfw+txL3lzSQrcVmGU7DrpSIT/sRTY5rzNnzboLjb0KFehtL3mzocUSzQZ1dXV5eU8uLHtgEsmqPWwfa40Jzt3gKS3NIbNztFBiSXC0smoipdjG6FFWMF+zWrXP4Z1Sf0Z/sh865/XQMY9Fm70Vg8dpM2bM6EimBaVNmzXrPaJFGEd5lZQ0ELotWR7d8cowJuqWUWr80Y/LUrM5P/ZmL1VKOSh7Lokc8BxqhRO37czm5oumz5uX1ElDn/EW+oHr4NtsE1llU+rlRG4uYlw4ccQln47ctTD0IOoESZFsAkD7AJ3v3mhoX2fDR0de6PQBOvUazLI9kQ1/wgkPFsz8qJzt5I7KQQ+jbNTOKG8Phxk59KCbtY/bqSojhjnINOi5Dz7sZag6iJqPEMxDiu1VD+OpYCqXX63QTh9c3dk5CI7Y79CfvJatNmivr6MTP494YpbO0+AtW9mUH+1lt9ra2n3pmoM/CBhKoUv0hxdz0YsA2rOOGbkvhZQHon/wtPoSWWVrbj5IdXZWoS94y7XlSr2VbiYuyivnFRMA03EWOrlLo0r4cZ41a9YiaZr0HtUyP/j5wQPe+9PoyOswc7jQD37E47sffjgNfOkdHbrVGlBQ9D6iVhlOzMNGOGFGLkInyw6KnAP6jzYP7r0svCtwezegKgp0RGPa6qt+LwLyB6zgc+RPGbSlp7tMczsMKn85d+7cz/zWhHjCOTwZMiohK6fvvBpSXu63PW75mUW4/QhmObXUVTDN+XPYbTn6RAcTfeLkkg0ElrskdU2GvuopDNAy/uhyxty589EX7G0KcQaEpnxVCn3FO6GePQ9KtZwKHrEj5xUIs1NnotO8J6aBjxfTZ8+eC5AOBcuVCHk9UOhXYQbtKLcF4VbZRYsWrcbU7lgUdNKlHre8XNDt5YLGd5JeZlniO3IRKcHYTy6iSpJ/m01dsNzo8/3+WGZ1fM8zSbbcRktx42fjhwdiP0QsgaAq59b8qDRlmidSG6VBYDRO1xky3oes8ZD5a10y7HzxMBtTV1eXm5e+bcJDppmkDdsIPd5KpdDFe8zkEzkmCvTUVaW0YOWT2X6w0YNbCs3gZ/RPkZxZklJvZJbRkkthYuevneEwvQ5GH0lYEukGYL1uKnXgu+++69qPyakjp5S6nowgZXUF8H8bcm7Xxd8VX6WehLOaZDTsikNKIkztfo0p2ptTEvmQiIfsBlieoZ8k84GbexZdoS7HGTlU8H3UMZU93XPKD2X5k0tWhkJqXFA/gJBC9gwr8wl1jNCywakX1JVS0gu9T7Qrw0odPGPWrJy9phDVGzL/Bk9kLOxeHY3TeYbjk5d35cKGoaVuKSlz+syKLxv0h1psElLq4RuvfH6vc97GUe+/89tkzMj65nDPnj17KXyEBjzH/xKvJ55x75T16HEonvH0EWh8Usrr3DUKrPdC8YtTauNTIpYx7vSJlWc2KIgZmD491nNGjxl+Wrny73gYOH6K7JFVSnJ0XhunJNCQ2Gn2cmww0KVXx0ojL+/teTVzq2dbO0IifBQaKqqE19y5oJfD21dWX5sLSalkoExzi49S38GJ2xcd5Uup9NKZhsHm8yIc3g/t1/MHXl71Ar4HYlYu57/DahiJWwh51T0JfW7rS5wSZj5/oitOjwK8zEeZfek3ToYQvn/8B1/hTDwj1r5Dq9SbpseZuKiN0C16qfeMRvArvRLWcSdvFzUnHy91r0JBHL1OE31XtCkgOukH9ElYy9kwzc3WXuXuf9/QGscZuW4NAv2eXLeOkdOgpgWvYCh6ReQmgP+kUBcsqa/eLYCqaVMJ/VADnLhp2gS4ZDxjzpx3sFR3oEvyrMgwO3FKVgwyyFyM+8ihL9TyvET54HGVAcicJSkCAPR/SRMzTzhn5MiRAzPP7pwTztzJGNRdGerZ82D0TZ5m4qIctVTMKPPoGUpOxCjUtxf+o3xTnVGQOZ+VM03zKhREeyq9/EzDzMJdfvJz4gUcN3WK1xm36eSFKT5YkQXjyBFG5U2tVyihHN+FoPS8BowETCn+5qBDUUahff4W/VDOtvBJB+L02bNnom88Kx1dtukYTByQLQ+v+Yt0HzmvMLiix3IxisgVKRO5RABdm+8fLkF0/7JQ6D+jRo3y/UMKrFZO9PJOHHSxHNodOXRUP5X17HmTRWoObtBhT4WYnO3rBYfnm6+//fZWyMzZAafxA0zLNusUKA0j547cWnvUN2vPtv9SVC8usI1t+3WtOgHtIOOvnWwI+H07rKNh2FF+Mw0cP6UenjlrlvaBj1e70YHfgzb8qNd8nuil3G6X4fzLHp4wcyBGH88OlwMugYwyTT8+TEgwDRVglDDNeXV1dYHqM7U7ckDiP2k9TRBpOZTS6uRYdFbqnsWLF+f+p5qkfMGih883cEByvrQaMUGJbyNnh39Gz7K87lrvoFLKqI2fX/SjIeQfUxLlMVEJI2/Lv6hf6Bv1Gg8Zs7794YecfS3q1ZqwEKfDmXvfaz4v9GZZWU6WcaM6YfbTiF77fNZeX5LpqwxDi2ww1YVVMlNyHQ8Tcyvy2x9/pImcVK/oZKwQZvsGoMD+Paq29t4hQ4b0zpiRjxmhj4/cnFgp9bhTdC7iMIKalQs5ERmGkZ/Rfjg8JSJf379N9LFOwVlK5xk5ZMGD+RicCuoob2p5BEusgVnWs4E3rH1c5XhbXE5u0SmimeoVFVbql7Rtj14pmXPHzPoKOHN6HU3DyOmekLn42CFzxDPLKU1TS10FUzMzjQomF0zMra6R9q7Umzqlou86fdONN/54dG1tzt7/T2aPdkduVWen+52Mk2mZYbySck6GWT1lQy2dgb8vPGXyiXj67NnvwrHR9vWbFCIvS6uwKakjJ6U4pNCWV6m4y6RxGs54ZuN/wA4lQ3nZpkI7DEo9OWvWrHna5WQpAM7cW+hHXsmSTfLsSu2fPJFT3CAgpSz2bULcwFBINM/oVhZ1YqCQ8m+YnVuE5dZTdctLxl+rI4eOaSH9Vmgy4brjAfJs3TKIv1TqPTrnK8DZ0vYVHpzhvCytouxS/NyaNIyyshyPgrIv3a0mz1sohHo2e07+c5BS1HSMrTzEf86pOcJhR/VNTZNpKnjTrrSXZ5o/1/kM05ygS6aUcstRO+88TBd/O1/TNHU9W7TVF7sNCfea9jyEQbqwSjAhTxEwMfeSMWK+H1JTfDiHVJ8OtK9tUYj3j6qr+3hUTc3pY8aMKfOJtSs2kO2KLjMipfL6U0WYJetAZ65ttioOlLw6cpiX1/f7nkrlxZETykw6I0e4K0P8ks6FF+TaPYMCqLhpGJcFUK2MVcLT41+Y6fogYwY5zjht1qz3hFL69rcrK+NZuRyXKYvLHwJo+yvw/L83lxqgz9lGGsa9Py1f/glm6c4aOnRor1zI1+rIAcS8OnLdAM7oPms7rQmH39HG3AVjzAjq/Dmo9V2o4D+JSv6OHAlDg9m6bVx1zrdVINnZhPJlLVOUEr7vOp6NTtG8GFXuvnRc1U7R+1ycIRMT93okYUSu5acA9Wi7liv6zL+uvfL/P7Cu9J+rM8difEfO2dLsY9EAMBbPnk+AOcDEPGlnGP+XD8l4PpWjvd214YABi+HQna/7owi9jpyUeXfkAKbW9+TQ8X49Z86cxfmoLFGZppT6vniT37R+0QAAEABJREFUEs/DqKTcnZUhU87IkSZSqoJbXpVTRZcUGmddCJgsQpcQY7PIHpisaJffY0Set/dzMwXix59+ejnTvEKI1FmV2jw1gX+pwF/6x83CSRdfixCnG3gjumTr4utkRknF0aocDL4RIS8HCnYL+CA3b7rxxh2ja2svHD58+Ho6FNHpyK1CR6pvyc8lGhjqaN2gFwWV9y8Ru7q6tO2Xh9m+3G+pgrINqXBaR04JeeS3B2yzAcgL7JDTg6qwkvLQXOqm64GPdvlcLu3wS9bChQuXKSFo6wTh9x/KNmcfLukqV78x8cJPYZrRC71bWtRVHG6pC5Iur/YtX7HiMqGUvskOF0UCZ24TIeX1vXv06BhdVzextrbW1+eW4UKHjEjQGdFoGH5URtn9zPSDn8wSeEmZ12VV0mfVqlU/0llTSP6TIZoERtimWVolGilFj2W9+55C14UUlAgH1pEDpmOWNgzsmys8JaZVdcjCLHWjDr454amUrl8CyZkjB59HV9+PR0tOSiFnQmCQLqxyZkMaQTAxDYXG5AULFqxR4fDJGkW4Zy3lhiCeFBJiCRy6a0aOHOlLm9TmyMEDzvuyKgAThlJ6v1oxzY9ITj4DjeI1ys/LaEqF0i+tks1SyD+qMSKnXwiR3GyCuXzFTCFUUDvvUJfYuKB+Bs2pLDBL/YJTfCHEhZXSMpsohdgkV/ZrnJGDGbmyIkFOj4QYfyLyaZM/FqTmYrEvName1Blz5sxAnQzOx1xS9oOll/QwjMhHEbjO6tDmyKHkPs5KM78yK6Vztoq0TLFNBiXnJqCS/pQbSbmR0mOV4a7+SDGovV+V9t+r9NPqracuXqWU+MpPnn7yUkLkbHkV9RZdhZ/aw0UW4pM5c+bk4mt1fxXv5jZr1qz3gQuKoTvCv9NGYOU73uCZcED/nMhJEKwxApMCWt5vAlA4NCqeZ9ZSKS24eTVrRnPz1UKpv3jNp5UeDp2U8q7RtbXv1tXVbZOpLG2OHJY2AvFlnjJNrTNyYSn/lyn4fuZDT7DGT3755rXFS/N+wsPgczd6wPaJuVwOdKNTWhop8/LuYVq9iECp0XQq1ID6EPfzboVqhdCywfioUaNy9sFDwSKfRHF41j2TJHF0CgSAWyAcOVJxenPzWdDnKboOVJByVzhj8+HQXQi9sPKK/x4O5PVA7YHUMM1AOHIYDeh9R06IYMzICaFrvxrUew8F7yupXOCKnZQbdaqN/uSKNihESgXXkZNySK5gwmjU9/oFhoFok9lgKIXQMkDE4Cgny6vF+I6cklLL8xL1NaivWWRThWN5UZcD8Xuk3QqpGTNnHg3Mg/gObW8h5fVw5l7brbKSZs+7VU5/0lIxSawKhwMxKlY9e2pdWm1ubrY8NMj2fAQ8EPvmQ65WmVK5c+SghBTygi8OGp6fzYsh3+uB8srLti5u9JRCDPju8CED3NAGkkaptF88B1LvOKXgNGhx5CAiJ44c5BTdgUkBbc/LogMr3iApA/cOM5y58UqIB+LVDMy1lHuF+/adWVtbu6NbnbRVzC7DCMSMXNlPP2lbcsToNhBOHJZLtnBb4F7p8EBBffeayx96qYRrR05I0Xd1L30/ceSPReu4oO4MXXcXvKsVXX0yfl8jANbonoXXbiKcBi0DYRkOh7QrDwGyq0tLvwFctPCFymkP9IXL0xJlQCCVKuoZOaFUIJek4cydin44OB9AWOvO1iEpp9XV1bna9F6bI4ep9UC8bPxTWVmZFR//7jBzoWvU7EnJcDhMX8B4ylMQxKbLpdWoMUqe8fkhOw6J3gb1/NXYStokUtdSuC9mm9LY2hdG+WAigzcDkAEM6F4yyJUmiwqFAjsTnEb1vCcbSml531pJqW2ywS1ocLy1fSwH+wLrqEY+gBAiGFuTJBbW+nDQXsZS6+GJSdYY0Fkj/LrDkmN+9h+zGdCjR4/etig/bwt+CcdPMPzm1UOt9LSJo5Six5qyHlf7rYff/FYaIr+zcW4MUrJwZ+SU6nJjYpBp8PBjhytgBYQC0TXTm7dZxijEqqxM57MsEL5A1Fb7efrMmQ+rrq7RmDnM+1Zidt0i91I+M7qmpj5yneSfHkdOqUAsq5LNmK3SYyOYo7MNxEijh2lqGb3DRCGV0sab+KcKWz6/CDOe3t53gjN3wpKGyv1S8c13mhSh7UTA//BkKdgZOSll/4DD60a9Pm6IvNIYpgl/xGsu7/RwDLT0GwqF610bf3KE9O2AsIE/GmbOZfXq1Tqf2Ssz1yw3OWmfua+++WY4llrz8tusaa00jMZRNTWHJKPT4+RYd2tPJrsY4rUt2xYDOP7YID3/zJupjMe/HF8V2G0WlFTj/MFGHxclReEu1+fwN0X1lYDQ8t5rULZL0oibNtbwTLXMyIFv3h25lpYWbY4c7Au8I0eVZvHixauw1PqHsFL7waHT+tOeJM9rkIbx/KiRI/d3yqfFkQMIvZyEFV2cUoEY+QNvtBVt6OrknV5ppdx/8BDlJuUmq03xb8wq5Vf3qD5x5/bxOwyEUkfERQX0UhZE5+sEnpKyYL5edtKf4jATrmUgsmbNmi+Jv+6QfZ+UVEM0n6RpWhPMsjIt78hhSW+AVsXzzBz9cKCXVu3wNDc3v7a6s7MSdfhylI2WD1zsMt3ey1Dov6NGjBhlp9fiyGH2OzAbANoN9vNeCqFl+cOrjsAbbcVrLtf0OnmnVUJKD1+uxnOTcs+O+uor4qMCca16XiCE1NLuhI9/hlIF68ih8y14R05IOdjH4oyx0jnzEhOCC6lvVSZv/ZFpmnq2slr7+5tArTgPDEoKri+ZN2/eT5iduyosBL1icluQSgbO3D12fQL/QLErHKR79Cjw5YKkUfHpYko1K3Or1IT2+qoz3OTPBc1XYyr7KaFOy4WsbGWYQf7liTTGwYkYmIYk0Mm1tbValtqUEB2BNjzgymGmRsvSKpk9fPjwvE5+7LLLLuuTHjoCZsi1fRGrQ994nijzr6fPnHnemq6urTFAfDQ+LW/XUtaOrq09Pl6+FkcOU5LoM+LFFOk1nhhBsCxcVqalHLtty6uzWvHj/GlKic5uXbydqHykvKe9ftgEbxn1UK/qF3pEisJ4ET9XM3LoK6QOtOvq6qp08M0FT1TbkTrkYGYkZ7/vi9krXX2SlvriFm/UVy1OCZZ2NnSrgw66rq6uATr4RngqpWVPxAjvHP2bM2fO4unNzSeYQuxIDh3qAS5FjqQnioGDddPQoUNjr7DpamyJkjmGEcgAATlVdGGVZm4GWddlkcZV7Q3VeZ0eb6+vvlNIMX6dUkG/KuClVUALpyXpF15IDvSBTvlQTQrm5P04TboHha2W5VXMgGuZhfUAmk75RTMTPHPmzIXk0GGWsRIO3WP5cugw2Bu44QYbXBAtX/QZ0Us+MwLBRACjj3d90OwPbfXV/wQv6QMvTyza6qsuhhN3tqdM+SaWhfuxA0GHQtblDBF7rQEPB2fds5Uq5RfZsij5/FJqceRUjx4VecZWnyOnVOC+AM0W626H7vh8OnRw5s6FHSEEocWRgwD0o8S+yAN63CBYaHR2wj8JgiZ6dJBC+eHICSnFCR0NVXM66qvG6NHUyvWbQ4euj5nAB6SU11pTCuIuJ1+aARs9dVfK/fL93lEmpVxbW7slMKnOJG+6POiucjYjBxv0lGs6I/Wna3lPDg9iLWXuFg6Ul7Z35DBzVTQzcnY84x06VPh/2dM1329UV1e3L8lA/aETh0JGAI0Qdch3C6IMdfKOykh5VqYxLSWBp0Q5HKOo19rrqya3H1q1raesHog7Gqr3+amsD/0yxSkesgWHVImPg6NMZpr0KisL9MbQTlahLeuZjYMwjK5n45STA3bo6jd08XWLixanBEbl1ZEzlNI2IwjeRTcjZ68s5NDNmDnz5yIcHoWy9GXiwS7D6R5t+hiK1+LIYeQHW4h9kQf0VkGwsJg/diB8B09p+QQVajFd+xakbBBlclFbQ/Vflxyx48Z+8f380KGbttVX3wt9p4JnwX492a9s+Rzor/1AX4G+SI8YNM/AfLHs1kKAQcslbsld0wFnFRbiJdcZsiQs1o8dMLvkfV9LN1gqtbMbMl00GNxW+cM7kUufAQM+TYwtzpjps2fPhEO3O6z7FeqKtk2WwT9ySCGOxkVIiyOHDhT8wb7YD/SOQTAx1NWl8wsa+CT5txIV6j86tADfX4c7y5Zghu6Ftvqq33fU7+T557PUMZU9l9RXHt3WUNXYGeqzVEpxug5dc8dTdWz4n8Xf50KelFJf/ZJy7KgRI6hTzYUpWcsYXVt7DOqjlgcq+L7V3NysZVnQyXDDMHT1Sfrqi5Mhtjjg2GKL8uUW7aDaF0YZMpFKVWaYNWU2FFbH1KlTu1ISFWHi9Jkz71/d1VUN+3XPzm00uqZmdy2OXBGWC5uUbwTC4hldKqAT7S2kPBjn25Us+7Ctvvrj9vrqR3C+qH3csIM7xlZXf3HQ8Mgms0vrKyuWNAzftWNc1ZEdDVXngObe9pXG/0wZelIKWS+kKNOlZ874KpGT2Tjhw19aFmVlN6WlCQ6BtncpTaVeCI6ZhauJNE3PPxno1tpRO+88zC2t73RS6poRLJ6+xCPoc+fO/Yxm5zDfc5/HrJ7IMWKqZUfOE2TBJEZFkRo108nbtdrlz7W8pZTIyYyClGIbIcXxOF8nDOMFFRLz1vRSX7Y3VKsuGWozhXpXGfIpJeQdoDldSqnvRWHXCPlHiAJ/0z9u+eUEW3YfVVMT+K1IMBt3hpByqC604IA8p4u3E1+NfRKK1ElibuKmzZ6tZ2kV6qsePYbjlPNjl6oq+jm4jbQIVqpkHbkonjOam09XQtwuNP1Jw2BHzhu2waSGI4F6ok03nbxdK43e25RCPes6AxNmjEBIiaaMMwcwIzq6u3fRuHN9tibX1tZuCyfuhmz5JM2v1Fcz5syZkzRdQ4LGPinv/REUaNUAmcCsipaNoNPpGu7duzYdTcbp7MhFoMPM3LmoN42RG5//YVl8KOqOz1yZXc4R0Dj6JVvgQ9Ep/wGzCo/lX4vi1gCdzeKBU1rpa9tiMnRr1dUVjJ/XsaG622679QkJMRnR2mZ1lZRTwD+nh8Y+Kf/9kVLeZuVcIg/MTqH64JLcNzIAqu2Xb8JCzPNNUQ2MRo0atY8Gto4sjVWrThdKLXdMzCZSys3ZkcsGwIDk1Tj6JQvxbKdT/kP5cwtegBZLEfjQhYBS5FTo4p4/vlKOq6upie2Enj9FrJK7Ojv/idk4LS+aRyVhxP589DpXZ419UhD6Iy0zcsBs0641a87KVRmRnLq6urFw5Hajaw1h5axZsxZp4OsLS9h+KtrG1NF1dTf6wjANk2mtrV+aQtybhiyT5C3YkcsENs6TPwSUuD9/wgtCcnZKGsW1rBoPhmEYN46uqdkrPi6f13iAXIqH6JFadcCy6lfffKNlSUer3gFmjoe/Fkeu2+QLczkrh/p3Tbdc/09KNfvP1IMdjzwAABAASURBVB+OcOIOg/MTfZZcUFdbe4s/nFNzwaqSjndV+8CW1II5lREIEgI9ujr/junpIIzKgwSLX7osrZjc+l+/mAWRD5YZG9GJ75Fv3eDETYQOVyPoPq5evHjxKt1CSok/HsbaHDmalQt3dp6RCzxH1dQcC0duhDZZUureeiMj1WkwB8fH8isMhpTnjaqt/b+MGHrIJMPhTzyQuyaFPa5pnQkdYrHWXxoPWrQ6B/NzHhUuK9NSjt2GoK13XwXgtOULHyxWQr4aAFWKTgW02xtR2CqXhkEmROZOIprsBphReQXO3GG5k2qRJOHE0UzAJEushhsU5BfLV678qwbWaVkW7YbAsHzanDmfoN6uxqWu4xrUT60/I1hTU1OLJX2tdQPLiC/rAihTvsC1ShgGvTPa284DfcPv4MzdbY/3816Vle3gJz/iRXVRpwNAMjgwAr4jIKVJD0Lf+ZYyQ6XEd+by5Vo79qDgiw67F5y5Z9Bpn5lLnYYOHdprdG0t7Yd4ai7kKtO8esGCBWtyIcurjAKnD2P08YFGG/qgfr4Ap+NAHTJoRiok5etSygE6+BNPci6+//77N+g6KIG+DofDQysO/ZPpBEzORBt9deTIkYOT0WQTLw3D958NlEJ8DbuyUcs5L8AAb+e0oopFbQ2CPaXwyw7xOJf3nv8EoG+Lj+Pr7BBAg71r66m5X4JDX4GJo+x0zyQ35NJxN5y5xhEjRgzJhIeXPHgoH7DRBhvMxixIbmYClfps5qxZd3nR0U9awyjOX3aIYoTZJvrwKnrr+xmVsxcezi9h+bPBT+aoh4diRupF8F/PT752XuhPXl+0aJHOWUu7yJT3tFce8HwRRLRnHk4pDin37REKfYCZc99/Lg+dnY6Z1g9hWwqDOIkRCCAC8kkRxgPxOveqMWUqBNC5fN9v1U83p6Ip1jQ80Op7lpV9ik776iFDhiQst2RrN43sMcJ/Bh3ty6izO2XLz21+U6kr3dIynXcE0GYe9J7Lew7M4EzGYOMmckS8516Xg/Kjjt+Iekgv2/dZl6LnCvi8rIezd6477LBDf7N37xfQ1rf1kJv6glvRdt/dZcQIzz/b6CSHvpqHgzvKKS2rOClnolyzYsGZGYG8IFDRu+U+npXzDfqLNvrvJzn51QzfNPaf0aWbbbLJl3jYPYwlmIOyYU8OIWZSjsVDoAkj+8Vw4A7Php/XvHiIdmA2Tsc2B15VKVr65ubmD4BzTl7mhwPyR9W79xdw6O6mgYEXUGm2GfnupfzIl7Ptd6RpBsKRo7a4Qb9+U+BAjYD93g6ilnJXVVb2IdryE6NGjMjYCUO/cgNmqfVsc6LUDHbkqLAKPHQaBvoUPUYoKbXxzkZjnpXLBr34vGre4MaWkng3Lt7qJNe0Ke8vQlK+iIffdwj30lIUwg6ptoSgNKJBGIs8D2y68cZfYyblcThw45LI0RqNBqv9Q4p0BsiuLqiRjsp7usTozXsuPTmgy9/1cHbmCofuTBoYwKlY61jU1l40uqbm4NGjR29MOTAA2RJ18FA4DZeC5knUxUU024x8p1N6rgKKaNb02bPn5kpeKjmbbbzxY2iH2W85JOUxsqxs+qi6ureB8VGpZEbThmCGH+VwDsqjA3F/QtBzdHbyjJweZJlrLhCIOCBKtedCVrHKMJTMyVYHhYYfHn4DEE7HSPc5hA/CnZ0r0CH/gI55ATrzqRTomuLCnZ0riAZhCvKcgpDJ+0f+QKTUizNnzsypg+GP4oXHBQ/2J6B17rd2kXI7OCfHoJ5dJwzjBWGaX6MeKgxAlqIO0tLp1Ug/GulelhJhij8HHFzaWscfZllwgSP7N+Dg62w4ZvZ2B8b/Bt4rEWagH3gMci6Hc/czONL7ok84GfdX4fwEZvhpNv4OmDAIQcuB0dI30+fN+xQ6+c8fHjn4+883cBzRUoKgE6ZsQ7r0QKPUUkf80lcKeYlfvEqOjxJXD2pqeTefdqOvkPmU71H2+ngw7ASF96FA18i/PkIgDnS6n4SFOC4IyoQNQ0ufhBWCwPRH06ZN+9FUSut2FUEoS086KDV3+qxZef+tZjhT1+Lx/CtPunsjpnfo6tAP/AxyrkClfAyO9KvoEx7E/QScjwG79B9WgCirQ6nIZt+QnxUbzlyoCBSJ3uVNLY8IJaYViTm5M0OpqcDu8twJZEmaEVgJR25sc3PzD5rlMPs4BEJlZVcIpb6LiyrpS1Pmf2BdV1NzNpypi0uhIEwh/kJ2siNHKHAoaAQMYf4GnSmeYwVtRs6UV0J9KTvNozCaZMxyhrpmQUodjyXVhZqlMHsbAjQrh0Y0wRZdtLcpDcNsHOogLe2mJNOZiCVNWnL+s04ZgeGt1AIM3CKTGOzIBaZUWJFMERjUNH+ukILfC3IFoFpuhOWB5S8u+NYVORMVAgLXTm9u/k8hKFqMOs5obv4rBpKLitE2DzZ1YTbulx7ofScdVVNziJDyUczGYYzqO/vAMcSy/v9FldLiyJUKkGi8GIxFoczfOdTVhRlWbfIDYWM66/qtXHE+llg/S0dXyulKqVUybB5Q/lxLS1BwQF+Ron4FRcvg6gHwnp8+c+alQdPQMIp7Q2Ab3uGwEGfb4krqFn3LxZiNm51Po9GXPAr5ZQhFfwDvz5WU/4waqsWRizLnMyOQKwQ2on3QTHW4UqIzVzILSo4SXSFh1pc/tyAyFV9QurOyzggo9ZERCv3MOZFjc4kAlrheglOdt1/SyKWtdlmw+xXMSuZ9Q3E4NyXzBT6cuN+hzq2IloUWRw6AomyjIgrn7FlTDAE859GQIVxWpqUcu1UtmGnqiudaZwqh/titN5/WIRAWUhw9qGnBK+uignGFvqJg6lcwEOvWQqnFsrNzP3pHqzsmUCfTNHX1SYGtLzNmzvw9VmleC1RB6FaGPvSQ8kTdYtzwnzFrFm0Hc40b2oKmWbvF0L/jbdDS2ODfBLaxxRuf9TWeQlnz8IGB0dmpfGBTFCwGN7Xegc408iVPURiUpRGYofxBhMV+FY0tz2bJSkt29BW66i69A0hBi955ZarUZ2vC4X2nzZu3JK96pBCusVxTSM1LUrzQsCwrw6qA+jg+soivVwrTHDdjxowvgmLj9JkzJ6BDiWzJERSdfNZjVViIX9t5anHk4N8AS7uoIrxHbxUEq8wePUrDcXYJdkVT65kgfQyhtA8lWspCqrriuZY3Sg0IdED/U1KOwLm1mGyHPV/Aidtzzpw5i4NsF54BJdkn0Qyp7Ooai7L5EaGYj1VhpQ6aPnt2XvehdAL4u++/PwbtJHCrD066eolDmzLhOB+DJdWETfC1OHJelGNaRkAHAuWNLScqofK+MaXvtrlkiJm4f5f3Cddt9Wwr/TyMy1zFRYaZgg5TqV0wQxvI2UivaOPh1CqkHB10J86rXcVGP33u3A9NIcagvL4pNtvIHjgUa+BQjIND8RbdBy0sWrRoNdr9ocXS7mP4KnVass2W2ZGLocQXxYQApgPMimWtRwglSu0F5KXKFMcObmo5Rj65YE3QyxQPBRSVFi0jfPGwWTG9uZl+pmcSZOHZqkWWfqZKPYeH0y7knOoXxhKyRYC+4Ayb5q6ocMU2kOqCg3QYHIpXs8VIZ360+060+yPR5h/RKSdXvGHHH2bMmvVgMnnpHLlk+VLGY8Ux0ommJCqGRKAbBDNCvP2IYzHIqaKroqnlt0j8JRy6LpyL+ID7psSdvZeFdxg8peXJQjEUfQWedVq0tfCdPnPmFVhqPQJNNvallxapGphC5+vwUKIZkILRvcS2H3Es9VmzZi0y1qzZHeX3gSNBgUXCjq8xE7cfHIoXCkR1c0Zz84nQ+4IC0ddRTeh/FeyI7RnnRKTFkYNgSyfqJLgo4vAUCoIdYf5qNWUxVDS2PCgNVQui+QjFdyj1H9VlVsNpPWezqQuWF5KB6CukJn0T+GKW5Fk4c7ugcyqUWZIlYaUORideYL8nLPC8L72vVp3q8bR585bIUGhP1Lm87rHmpJunOKXmGp2dIzET96anfAEgRvu5ucs061AGhdLuI6ihb/xemeZ46H95JCLFPy2OHPybhE40hQ6FmwSkg6A8z8ilL4Xyya3zypf2HCmVwhJbkew1p9RLIRmuqWhqPWLw8wsWpEcheBToK9C/atHLkS+cuVZTqWo03eu0SPWJKfS7edWaNTtiiegln1jmlA3PyK2De/r06d+sXrNmLyrTdbEFdKXUw5gRHjFt3rzAfiWdDk3MjjZ3dnUNx7JwQfwCCjqvqWu6uqow++nqC1wtjlw6UDmdEfATAbe8ZHNzZ3lT6xWGEa5UQv0D+cIIhXi8J8PhXeHAHbzV5AWFPdLPA/pwjn7AKPeS1Z2dg/BwTfreSR5UE+jAn0LZDoN+F8ybN++nfOjAMv1HgMqSyhQzrENR557xX4IGjkotNoU4CU7cyRq455zlnDlzvoctR8Cmo+HQteVcAZcCTdP804yZM/edO3eu618qYkfOJbhMVjwIlE9esGhwY+tJISmH4clJP+sSeOPwgP9eKfE3EVajsFS8G/9CQ/ZFRh0lHq6/xMN1OB6uL2fPMXMOkN8EPWrRgR89bfbsgpxdzdz60smJQcTHqHNHoqz3Q5tuDajln2JJ71Q4PVtjBpsGvAFVMzO1YNNT05ubh6DN/QHh+8y4aMil1MNwMredOWvWTV65G/BMX0OFet3PQDy9KqKLvkePHqv8tC2eF9aP+eeOdBVcDvhuNXnewoqmlhN6Lwv3l0qciHrbqIQKzpeeSnSho5liqPAxFUt7bja4qeXXa3+9Igfg5EiEsWbNT/Ftyq9rtM3pbk3Aw7UFD9eDVDh8AOQ/hXzLELQfKNvPIeQaJWUF5DdAj1m456MEEEBZvwanvRoO06HddS7/VivVBkfijOkzZ26DJb0H8q+QXg3Q5v7PKCsbjHZ4Acogb+/PQfa9cs2acjjOJ8PJ/CQTqw1k3g8VaoyfgXhmooyOPDNmzPjCT9viecHOE3To7Jmnaa5EZfDVGY/jN8OzPgWWYbOpC5aXN7U8UtHUOr7XamMjGQ4fitmvG4VQZHtul1+V+BBy75ZKHdlv1U+bDG5qrR/UtODftCxcYLC6Unf6vHmfxrcpv67xMDrJlQJxRDNmz34F8o9G3vWFae6PpNvg3C/COfujmwPa1Qw8OG4G/0PwIBkIWRPQR+XtIdKtlu+nUFfXctjqe5+EdlFUzi4cpheozslVq7ZAvbgYIae/CgF53yM8BAfuQDzPhsCR+KvvlSHADGkDZ7TDm1EGFXCqj0N7z9nHHMD9Hnq9A7J/M21edu8f8tJqgCuZW9WmzZu3BJXBV2c8xq+5+RS3ehQD3RYvzfsJy5YvYPbrworG1tFYxiyTUu2sTHGsMNWlmLH7Bxr7dDh6P2Rjr1LqRyzrtoAXzQL+WSrzdCHXbFXR1LID5J5d3tT6zEb//SQrGdnoV+p5p8+a9SqcrPPwcNuuyzQrUV4XoKzc/o7mp+RBQMQaAAAQAElEQVTEAMN/IN+VeED8WsAx/GHZsvXRrkbjwXEB+L+I9KI9ps2Z8xFs9b1PQnnQr7YUHW7TWlu/RL24HmGo6uysQr2h3239D+rcd74aq9Ry8HwT/O/A8i59Eb0hZJ4CB+6/vsopQGZwqp9A/do71KNHX3JsYcI13Vj58q4q+gSaGLgJvMcuX7GiP3A/i17vgJysD3bksoYwkAxYKR8RoC9eaW+2iimt19K7dZi52wWO3gBaki0Ldw0Jqa5aOHoHCmEejyXac7CsNxEd5RXRIJQ4Hw/zUwxT1YdkuAa0G2GmbYOKppbh4DUePH9X3jT/vorJC5f6qDaz8gmBWbNmvY9O92Z08vvBuZMyFNqgMxzeSnZ1bY9OuQZO2t4474IHI82wSdBsQ04Mzich30Q8IP4Gx+3VhQsXLvNJJWZTxAjMmDt3PurNHahvRyBshHpFWyedB5NvRJ9yN8JDcDD+DcfgeQTLrCfiX0XcZJwfA93fkOc2hEmon0dTfQW//gh7g//vsbxbkF9Ewx6tx7vvvruSHFu03wndWPUDftsq0xwPwROA7+0IDwDfZ3B+BSG+DOgr07+D7hqE85DnRJTffggD0CeMBs8/gffzCxb4u00UO3JAmw9GIBMEaEl24HPvt23V9P4sOHr/rWic/1h5U8ud5Y0tV8JRmxQNFU0ttw6eMv+hQVNap9BXpoOntPg7ys5Eec6TMQK0HDN79uylNOuETnk2nLQ3cUaf30zvvGXMlzMyAk4IwOGaBQfgNoQL4YCdjXAKKtsxcAzGIlhmPRG/P+IOw/l40P0aec5DuAL18ymqr07818XxVTIEgN8nGJA1AstrgO+5CKcC3yNxPgAhvgzGg+Y0hAkItyHPIyi/1xC0rq6wI5es5DieEWAEGAFGgBFgBBiBgCPAjlzAC4jVYwSKFQG2ixFgBBgBRiB7BNiRyx5D5sAIMAKMACPACDACjEBeECghRy4v+LJQRoARYAQYAUaAEWAEtCHAjpw2aJkxI8AIMAKMQEEjwMozAgWAADtyBVBIrCIjwAgwAowAI8AIMAJOCLAj54QKxzEC+UGApTICjAAjwAgwAp4QYEfOE1xMzAgwAowAI8AIMAKMQFAQEIIdueCUBWvCCDACjAAjwAgwAoyAJwTYkfMEFxMzAowAI1DaCLD1jAAjECwE2JELVnmwNowAI8AIMAKMACPACLhGgB0511AxYX4QYKmMACPACDACjAAjkAwBduSSIcPxjAAjwAgwAowAI1B4CJSYxuzIlViBs7mMACPACDACjAAjUDwIsCNXPGXJljACjEB+EGCpjAAjwAjkDQF25PIGPQtmBBgBRoARYAQYAUYgOwTYkcsOv/zkZqmMACPACDACjAAjwAgAAXbkAAIfjAAjwAgwAoxAMSPAthUvAuzIFW/ZsmWMACPACDACjAAjUOQIsCNX5AXM5jEC+UGApTICjAAjwAjkAgF25HKBMstgBBgBRoARYAQYAUZAAwJF48hpwIZZMgKMACPACDACjAAjEGgE2JELdPGwcowAI8AIMAKaEGC2jEBRIMCOXFEUIxvBCDACjAAjwAgwAqWIADtypVjqbHN+EGCpjAAjwAgwAoyAzwiwI+czoMyOEWAEGAFGgBFgBBgBPxBww4MdOTcoMQ0jwAgwAowAI8AIMAIBRIAduQAWCqvECDACjEB+EGCpjAAjUGgIsCNXaCXG+jICjAAjwAgwAowAI9CNADty3UDwKT8IsFRGgBFgBBgBRoARyBwBduQyx45zMgIFgcCkSZO2QKgpCGVZSUaAEShIBNDHbHPllVdW50B5FmFDgB05GyB+3V511VVj4gMqeW+/eDOftQhQp2HDeJu1Kfw/igAwus4wjM8Rmq+44opm1MONoml8ZgR0IYB2uQNCrA9EvavUJYv55h8B9DMPoY/5GJrMQz/z0q233toH13zkCAF25DQAfc0112yplHpNxYVQKLSlBlElzRL4XocQw1lK+euSBsRmPDrUwxB1EULkAD416GxvitzwP/cIMKVnBNAu/4QQa5uodxM9M+EMBYEAnLg/QNGTECIH+pkDly1bdmHkhv/lBIEER448aYye+l1//fUb4LzRtddeuynOW1x99dVbIZTjeghGWtvivD3OO+FchYLcGecanEfhvCvOeyDsheuhObGChTACjEACAuhQD7dH4uE61h7H94xAsSCAZ04/PJf2w/PnJAxkLkCYhOszEHcA0njGXkNBo08Z78B2nEMcR2lCIOLIobKfg8quKCxfvnyFYRjL1qxZ8z3O33R1dX2F8+emaS5BaMf1pyi4RTgvxHkBzi3QbQ7OzThPx/ldnN9CeAPXZ+LMhzcEmJoR8AUBtM/PHRh94RDHUYxAQSNw5ZVX/hphKp45y1DvX4ExD2EgcyMCzQTeg7iXkfYxnnX/QzgH6Xz4h8BSB1ZOfY8DGUf5gUDEkfODEfNgBBiBYCGAh9etCF/ZtJpku+dbRqBgEYDzNgqOGU0m/BVG7IOQ8oBjtwnCHcjzKcIxKYkLKjF/yqKPuRLSf0KIHYi7NnbDF9oRYEdOO8QsgBHIDwJYSvoas+ij0KnSQ24yHmCHTZw48dn8aMNSGQF/EUD9pg8oXkO9rvLKGXmGIDwBR/AUr3mZ3ooAyuFDxOyBfuYfOD+NPmcfxL2Haz5yhEDEkQuFQk+jUu+bKkCffyLEDhTae6nou9PujmUooYvOzk5lNzccDifE2Wn4nhHwGwHMOrTDeTvj8ssvP+yyyy6b7Bd/5sMIpEIAzwdLf2e/T5XXTRq9w41nTCNo10OIP/4HWdcgnIJwAMIhSPwNznchrMK1/XgAbeRAeyTfe0MA/cvciRMnnoTzUXDi3vCWm6mzRSDiyE2YMOEzdPJTUwU0gjabsO9S0Xen0efItmwlcRvB1WapU5yNhG8ZAUaAESgKBOz9nf0+KyNXr159Lhw5+8cLf8Fs0BA4FBMQHkJ4BeFFOBf34vxbPMMGIzxuFww+NGNtj+Z7RqBgEHDduFDZZbxV9vv4NP+vC4tjWVmZBavC0p61ZQQYAUbAXwT8fF5gxqc3+P3OpuFUOGxnIm2FLT52i7Sv4Mgdj/ByLHLtxdZIG732kv8zAoWHgGtHDpXfPlUe1mEuGlRvhDpMd/8c4VKEc6+66qqDrr766sE65BFPmqa/8sor94Cs0yBrIq7Pw3UDztW0HQvReAldXV1O2Jh2HpBxFMLtCPSuxmuQ9xTCXbinDml9O326++uuu25D6B/bhBO89rLnAbbrg//ZCH9BeiPOryLQy7+/xP3Odno/7sF3F8j4Dc43ITyP8AjCBMQdR3vu+SEjWx7AbVvo8wsEqHblkzhPRrgWgXAZli1/p/xUp8H/FxB4Dc7/QfgvwqMItyPuZ0nybAVdY2WM8kz5AEL63jb6AU583cSB12aY2dgT+p2OMAk6/gphD6p3bvK7pYGcLcD/YPAm/hNwvgT3h+Gc913joceB0OM8hL8hvIJAbeg+nK+A3o7bLSFtD1sZbJYMC+BbEU+LvCPttNRmoMfFSLsf5xcQXsI1ta1jocP2dno/7qHTdpBDfeKfIOtPuD4ZcbSlR98k/C39HZ4fTn1ikqypo0Oh0K6g2BAhdsCx+1XsJnrhcAY+JnQ51Z6E/I7tzU7ndA+e6wMTen78EpjQ8+MM3NP2W5s50buJA8+h4BXfzul9QEtWyKAPPa5HWfwT4QlKvOmmm9aLz0fX4LUFpWUaSA7xiQbcJ/SH0bToOZPnJulHz2LY0oBwMcLfEV6AvL/hTPfHwZaBROdnAM9+CLRt2kmQdTnCWZC3L7UzP+VQP0l8EU5GoPZLfdvxkD0aIVk7cqWCa0fOFbcMiWDEQID3O4SphmGsRJiBhvUowtUI9OXdi5gyX4z0LwDAHaDfO0NRsWyocDuA12UIc2mrFSS8BVn3oZHTV3234JreJ5pH27FA7iOg3w40vhyQSY5UG2T8G+H3CPT11BgwPxLhLNzfjfAl6O6FrZsgztXR1dVVC/1jm3Ai0/MIkQN8+sGOm4DtEvC+E+E3SKjHmd6NPAfnv+N+DmS2wVbSBbeZH5A3CPLIWaPl9ffA/y/g9keEQxCOR7gKcf8Kh8NLIfM5yDwacTk9oCNhcir0fAu4LYI+DyNcBiWOxrkB4WIEwqUVOjYjnI08GTtC4Bs5YOt+kPkM1WnwfxiRl+B8GML+CD9H+D3iHoM8+rLOsoUP8hwBXWNlbBgG5Qe584H01+Pp8RAc4UzpHAs96WFBDu1H4PUl8r8J/e5FmIgcf0N4q7Oz81vQzUK4BLZtjTjPB3XgyH8dAm1x9Dn4vwAmxP8qnK/B/X9wnod02ibpzyiHgbjPyXHttddujLK4FLKp7bwEobcgkOOwH87Uhk7D+XLg8xHonoBu9pfvn40vA9BRPmRJPIAvzRjFyhcUf0aIHOBL/eRD1GaAB30VeCrOByPQO17Uth4H74XQoRm0O0YyZfEPfMhpJWfxB+j/IeRQn3gDWN6A6wcRR1t6fAVc7oe8nP0EHOQOgQ6xA/c/XnbZZR/HItJcQNclyHMPyF6PC57qE2wehnA5MJoNzH8AH3p+/B186flBvN9A/JdXXnnlB6C5EjITHDHkSXoAX1oKjtUD3F8eJQavXcF3Ou6nI/5ChBMQIs/ECy644Cf0EY9Dj/i89FUpyL0fkEW/BDM9nh+47I8QO0CzSXw6Xf/4449bxQhcXACjQxH+Rc9i2EIfZl2L8y8RDkb2X+FM9/8Cpp/B9psgk/RCUmYH+qltweciyJwBnssQaNu0h8DtCoS7IO9VamdI/xR0N0BexvUbPH4PHguonyS+CA8iUPulvu0RyJ6G8BNoHoecjNpt3h05GHk+jPgM4P0fQrrPxzcHAOeA/nXkmwaj7e9IgEX6A3nvQGX7ALyuRBiePoegzvVDAP1ANl469N0esqdB5p0IFankIp2WD07HuQV5qKNORZ4yDfn3BWYLQESdfX+ckx6QVwFsXkOem5MSpUlAXirTDpCRs5a2jCDzUMikWbD3gfEw5NN+QEfCZBEE3Y+wB0LKAzrWINwJHNvRCTg5nSnzUyLKvx/kPg1baZ+rhM16iSY+QB59WXc38ryLvJaHVzydjmvIo5lbcp7oYUEOreNsU5xsmjmil8w/gb402HL9k3SQNRwdOD2I6VcoyuN4Jrv8LcrhM9SVa5IR+BWPsj4EA6SPURZXg2fahxPojoFu1GYvAL1vB2wlp+19MIztoI9rxwM61ECH91EONCBwpEkViZnicsibCT7ktJLcVKsD9LHBqZDXjDy5+tUQ+wzTV6nscUrDzOdZWIodEw24dz0jB1zvA89WhCuAUbqB0Q6guQz4zAc+j9GABfkyPiD7TPAip2NUCiYPxKdB/rFoY67bY3xeyKJBd3yU6NGjB32daonL9AZ60eCE+pjnoOdxLvn8EXpRP3OxS3oLGcrhNvTB1PdfB5l1lkTbDdKp3/0TcouqRgAAEABJREFU5NFAvgmDuk1tJElviRbltRA8bgfRTgjpjmMhh56BnvHN2JGDclm9B3bDDTf0h5H0tWxGDgPkj0aYCx4npEMnmk5OGOjfRb5MN4Q8BZ36G1RAUZ5OZ1R0J2wGopCmQnbKpTA7P9BvgfASOpo97Wnp7lFZJRoKLUM8B1o3D0iQrT0g83xgNRv5XU/5gnYAGkkj8mZapjtC5+mQ+4u1Wuj5j4fzROj4KrhvjuD16A8dn4SdsZkSNwwgc1vIpJnmI9zQx9Mg366oO/OAbyVkW+qW/T4+X6bXkFMFebMg97BMeCAfzfDOhs07pMuPNkmDsymg2xjB63EJysH+rpRXHknpwXsC8KVZ7Q2SEiVJAAY3oh5bvvSPkoKnpQyj8cnO4PNLpN0PnqkcKpBYD9DTaxv/tsamvoOs/TGjMxtUtQhejz8i/2xaVoNsi432e6+M4+mB3//i78E73SAjnjzja7SLIagTcyCPZmAz4fMzDFhawGOXdJkhIwE/tCdaKUi7EwTwIUczXsQGaM9Ov74QT+N4DV6Wvhj3j1188cXfORJ7jAQOe8HOuciWyilFsuOxAfJeCx40i+ZIYI9E+W0B+ncQTz8phpO3A/LGYVatFXV833Q5Ias3fIXnkSfNqw6OnE6EnrQa4ZjoFJmxI4cCtbwz58Q8Vdzq1avJiXN6qNGy4lEAoBKjJYmlhoHoWHYDr/MRaLkFp7UHaPoh/BOgRaaV18Y6/wdNXwD7KujJsYkn+hK2/BHhIMgpJ5k4b4pAMwznI96yEz7yD0VhvpRqZIX0BGzQkP4FoVsiCPBcjkCzVYciflC3zK0RR0urjg0VdP+g9x8ov9sAXfsikGMVHY3Rbts0Fb9/z549B3TLpRkwcoYTOnzkHYFAS4uuRELH/4KwHiF2wCb65P9RnA8HpjuQTJQpjajJob0U8fNixLiAPNL5YVTktDMPIPd8oBHeDJm0/GHJi7jXEHE6wgg44hv16dOnH66HI/4UBPvL0UgSvwUvKlO6ThlQ92jp4XXY5jRt3gL+JwGbYf369euLMzk0NMo/F0xpVhOnyNEf+emLu56Ru+5/iEuoa91JGZ0wYKgAzzeReVuE2AEdadbjUqQdjHKO1llyTmnp41qk04xvjB505JQ/TwO2WKTDBdrkLaAdFJ8EXrNwfxzit6H6AkzIkapDvNPXhf+HupJuJh/svB3gSbODtPThlJEelHtCr2h/sTV0peWmyHtK0QyIO+GKK66gthWNipwR76XMtgd9rA0CA5oJopm2Pam+dONDTtfpSKOHVERG9B/yHgVbLonepzqjntLgmNow1UE76QvgXw+bt+uWSX0ZtWEatC2LEkPeiGXLltFWHxYbkddyH6XP5Iz6Rys4lqyw8SxLhM839H4T5L4Btvb3iGlZlVZ2xgGbrQkb0NFMOr0mQf0M/eIRssUOGlBPAdYpl3Id8NoI/O+Kcem+AB193NGMc6zswZtmm6Z2k0ROSPfcn06aNInqHpVxhAf9g2330jnbAN60VPkG6ovl1SHoSf3MnTgfXVZWthnhCbsJs90h0+nZSO+10WoekpMfkEfPFerjd7NRrcT99ZA3HnK2JXlYUqX38ccgjgZylv3woO9mCI3gl3LwABrqv6ldgv3aA/yoXE6HnMhzEOf1EKg+OS19/wp9Bz2P1mZO8z9jRy4N35TJaHQTQHAAQvzxNm6qAOTZl1122dMItIwgLr300s8B2nuIvxXhUBi+DwD5BLSxA5XrUWposQiHCwD7FwT7g3QanIqREydOvAXhZchZQllx/hphDuTdivgtIc9SUcBnBBzR50DjerYKfKky4iT+C5lV4Hs5bHyBtn6hSPBajLhnIPNs3FOlpaUmXK49IHPIypUr/7T2zv1/5Is0FNjwD2BHzvGNkPvqRRddRB2QgNwFkPkowjGgoSXDb+K5I/9xGAmm/X1OVLoHkc9ecRvBczB4nwDbnoWsD0FDZfol4mYgXIt4qsjHge57SosLD4GeGntcVHaXqHfHwh4aEMQYQS41rtHQYz/ocx/CXBpx0rsmuG5BPG1jcBAykFNHD1Fcrj3A6zjYTQ12bUSS/6ifNGq0L8v9BPKfQ8ZwyPgHbF1w3nnnrcT5W8TNRbgdgZa5Y2UOefTuFS2PI6ueA7o+Djn29wD/Apyo87kWdeeluDr7Cd1Dz0thwzDQ2GfHtkY7Sdrxo15tB1l2R+d28KoFzyfA+1OyEpj8iPtmxJ+Be6eZ6dj7Q0jP+kA9oc7+Ojsj2PcK2tCW0OV0hLehV7S/WAxdX0XccaZpbgs6ckQj2WEfvS/lpZ+I5Iv7F1vKAd/LgUE15NyB8DbVF6KDHrNwfx/S6BUBpx8rvwZpkVc5iN4pgMcAlL3FESU6yFwCm3YB/0PBYwroqL1Qv/EF4qgNX4B0ckpiziZspneb0vYZxD+TgEEoPSvss0JXQzcaAGXCMm0ezKTRcle0D4/SP4q+nNrFRJQ/PQ8WUwLaRxvuX0W4AhjRAIQGgz9SWnfYGBg5ztZ2pzudDkCezSgBZUJ95WnkcKBM1iMZONMkACVHAmhosBG5pn/IOy7dShLRxQfUB/ts3CLYNDWeJpPrSZMmrQ/e/7bnhc7PIOwEe86BPU9dcsklkZlX0C9B3LsIZ5umSc/jmNPazYPer0/ZB8B+p+f/09BjO/C9GPLIOYv4FejT2xH3OuKo3ewGnX6G8G23LDqth3wJbYUSKEBfchrtr1Y8DX4k6z6kR56DOK9AmAdZtEK0vU2GgM7JBpIkxhJy7sihk6SHvV3BN2HMngjzLdo53MDwN2DwOCSRJ41T5NgKDe2GyJXDPzwwaEraUilBNhnydiVHEdcpDxQATcXSy4kxOoC8OwqTXniOxbm4oAf0gdTQU9FCr3fRQdAXp/E2Uha7DRSXNgCvx2DDScCOOoCk9KB5Cg0loQNGfnK8k+ZDxaeXbU+2EdADeTxk0gjLlmS9hb1PwF7qhC2dM/D9Dy3TWKkzu7v66qtpDynLuyOwi17ipQfjjHRcoSM5dfTVJL0gHSNHPbgVdTrp0gDSfg1iC6aQS7O8e4Bn2hk9lMlNoD8EYQX4UOOm2Uy69D2gHCfBHsuMNeReBD3PRDmmrDukDHT9M+h/S9dx4Wdofxb7o2moa2Oi193n7yArpWOMdHqI02CnO0vklHapKkLl/h/NfNqp/wL76CtNKjt7WuweOH0CDPZCiP6CBr2T2idGkPnFhZBv7zcTuAGfGxFpx0egLaUcAKDc70A+monAae0BG6h91MImerF+baTDf6Qvh9zTQB8bdICMZuxw8v+48MIL6fdUSd945hvChjfR3qivjo/P+ho8fw3e9MyJ50UDrRPw/PgyPtLpGuX2EPCn5fFYMvjtC75enx+U/1XMVNGAnL7obKcIp4CyeArB0mYx+/1zJ9pkcch/oi3N4hza0lzfwnZ6Z8zyURRknQecjkRdineYEngi/QvQ0jvjU22JV0yaNIneZ7NFC4H+x+n5/3fU2aPwLE6Y3bUzgF7UH9jfFRyJ8ouv77FsKGtazbN8VY0yo+dAjMZ+AQeZPiazl8/msCntO+bEK2NHDoVhWcMnZi6D3aAf0KHbQUrJCsZ9gMK0vOgIfU5EPC2HJeQFreXLPyIA2PYHDkUnDSh0Wga0dOLgS1+bJuTB0pwjNtDRdSeDDoKWQa+3Md8alYdmC2zRqW+BLy0TpSbqTgWG1GnbHYzdEO/YSCgb7LI8fIHLB8DrXCEo1V1Ag2oDpX1Gp3z58uWOGIPW04HR62+gp2VmBHXgFNhFS7+ueQFLGl3b86Qq14QlH+BzGPChd0NcyUVH8iIIHTt98HKsa6DP5KAvmePzvQrZSQdI8YTRa9DT8g+9fxiNEsDM3uYjaSiPIZGLdf8+WHeZ/Ar8aPY3nmA9lKMvs7fo9OkjFMvMCzCmTWUT+pB4BeKvocsK5KFRvOW1gSgN0ryWWRvqCzloURYpz6ClJajIikaUEFgnXVqDvhsh3T5I/Bz9WD3S0g7EojJQ9vSxw53R+/gz+Hu1OT57wnWvXr1uQ6SlDUFGP8TdhgHJd+gnH8f5F9B/fcRle9j7JRqQW/q8dALwoKaPnB6Jp0M9SLp0BlsS8AL9cjgEx3Y/G+JZJVzD7lXgYZ/1S1oH7AyQf2/kt7RPyLa3O3u2tPfdryRZHBbYNR11h8ozbX4igG40qE3oc9Gf04oSkVgC+Nvb7kfoQzy9Jw/9qA+mnRdivMHX3l9G0+wDoq8wu2hZ6YoSxp9RR14Cz8gsfzQeZUCz7NHbpOeMHTkIzPSdh+PitYGip6BgLMrHpye77t+//73QIX7E0cepIFEAFeBh/9z/RjgOHYj3elje0YHue0L3hBkSp3fkoGsjCmqqF4H9+vWj2Zil8XnAh5Zd46NSXoP+OnRoSUduTpnh9CQszwBbpyUtgQ6TlkZpljXGCrTnx248XOAB9E/oa3knAdkdHRjEez0sI2LI+T+Uh+Vh54bhpEmTFsM+u4N9vNPSPrCh9w8Jn3jWl4EHOcvxcWmvUY8fg86P2QlRBzNthxZWcGAOAq9YXYYs+p1W+7KnJU+yG+S1OB3ge1iSZR0arMTYIN92wCb6Pmcs3n4BGurIzwb9FdEAmi6ErA908PZZCNp6wx6XVg50XIV6YlnuimYCHp7KDDZ6bk+QYZ+B2wA60dJ8VI3YGXoeG7vpvkD+U/DwiSxtdUe5OqEN0wNyoZ0YNniy2Z7ffk+vhsCx2B9859jToDu9GkCvUTwM235A/0f77P0BdTztxzd2Xt2YUTuOJEHeCvDPaHCJvPZ2Mbq7j4jwjv8HWie8JqBM0joEcXzsrzXUwh7760Vx5OsugZvFsYc+z8CBTDv7uI6D8xVWzo4BfpY2Dt5Wp9g5qyUW9YyceJqdj49PcORg7yAQWJ7/aOPHIp76ECS5P6A3vQ8ay4D7bdAvJzwXEW95ZuN+M8jbLJYxxQVoLwAesX4N5WDpI5NlzdiRg8CEEUMyIdF4NChqAPTiciQKCrfjYUpbHETuvfyj90Ogg2WEAH729+5oScHyMALNtyjIa7zIitKi0CahAsn4gAKyzNIRLUayTtg8SWleQreNz9ny2N+1siVbb2FvwrsIVorEO5RTO/JZHCrcJ3u50zLbArqvUKZ2nROFJIlBmdJ2IPGpe2XSAcczgD20R1vMSaE06GmpOxTnNkDHhLxw3i0dH/GCDPtyM81O2TtXInUVwC9htgNxTnXNFb94IvCx6/qYU92Oz5PsGu3kRfCLvG8SpcHgIOGDBNDQLGyUhJaNN0HH5WpkjjZ4N+RMigbo6jj7FWPu4gI8BqBsj4onhY7/QvzX8XFur9EOPkZ++iLXkgVxnsoMNj5lYeDiBrIT2iBsS7YXpmWmBvpF3n10ISYZiWXmgogg25PNlCddIKcG2NAy1q2paCGbluJoy4kP0BfQV6Nndc8MpcoWSUPeUyIX6/5NAbYfrbt1f4V6NP+U7KgAABAASURBVA/YWt7vwr3FyYhyg9wEvEBrmdGL0iY7o420IM3y2gj42u0BifWAnr0h69j4WLRLX5ZVwdfST+L+GcizYBIvN9U17KPXseKfx5bXQigv7LXIQ9xLkJfg/CM+7YFyp/fWLR9cApcEnwOMLP0a7qlvc4UfbPoX6nSsX4NM+viIWKQMGTtyKbkmT7QsCwLkyEt/ycnTpkyzUVjW3SkNMiwzWLh/FQUZ/+IpkWkPKPBMRzOWdwagvydHDqPWTOVaRn6QS/tFJeCEhmj5Yhh09un8hDypIuBkJ7xEijiLjFT5ndKgkyU/dF6AOpBRYyb+mM2lhmpZPgRPiwyig1xL3QMNvSzueqmKeMQH6EwdHnUm8dF+XVvaJphm9LBCvsgB2y2zjijDhLYJPF5BsM8Wn4GHLXW2Fsc7wlTPvxjXUCiUsKcU9Etw2mMZXFwAh6zaA+RnXF+g3ucIsQO6JHtXz172WdkMHBNmjmNKaLjAw+982LYNsKIBespZRNDRrORdq1evpo3IJ6XbCQD0FucA9762C8Bh+Toc98mOH9D+MxlQ2B0Iy8SGkzA8q8bDzvgl6Q44FAkDA6e86eLA195PPpMuT5bp9rqdlc+BOmbxOWBPQr8GrOgjrdfj9QYd/SrKLExK7BQf79d1xo4cDHKa+k2nl316cRUMi/0MiddrgGOZKsd9QqOAnpGvNuMU+yLuWsslZmcSsMGMRKZyLQ4VFLZjiKjkB5yOtC9zOuUGlna5lunwaB7Q2fdis1T0KJ3bMzorcrItn+w7yHDLLkKHOmDXkTbUjKRl+g88LXZCx4RyAU3si0OSAxravoAuMw7g+VZ8ZvBMqGvx6W6vwdeOUT+v7TGeHnI3Qog/EtomypreJaMRs+WjHth0IB4mn5NDh6UnWhJLyBvP2K9rOJuW8iK+0NEyM01xXgLsoK1cLFlgn+syA63FGbMwSn9jefCjjBMcOaclbyed04taR0FLcJBled8R965tXsfJ/RU9PDGTMQFOHW0PQcuH9CU8vZriWH7Alb4snLhy5co3UcaWd2fjpUJve53oGV/PvV6Dt2WAAj0SHAHQ0BZVdrwyckB69epFTnWsfUHeIOjsOAtIcrsDtcnuS0G6xL5IjkVmcOE0C4q6lulEgysNYK+9XzZgfzY+R7lNsGPfhL6EfgbOPqgYifq0AH3aW+jbLka9ow/8bOwyu83YkctEHEC1N4p6GBb7KZEMrifZ9LA/jGhK0y5Ta8Wx6RN/Sw6KEPEx7q7ta/kJU+4p2PyUIi1lEsoi1viJEPfJ5FrwRRlbZhApbwbB4kRCtqXzy4CfPX/WOsJOy0MSOtk7DKp7lvoIO7J5KENE5Mh0QBDJ7PSPvgyGPZaHGe5pb7iM2ybk0JYtOMUOelc1dhO9QGf2Bjq9A4CNHU/CL7oktgidH/081+XohC2DtygfP86w2VJe4JnJe7TItu7IdCC1joNYHnft9dLSd8C+hDa8Zs0au80Cg07LOz5ehXbT+1HXu1l5O8GpWwiH7gk4dn9C2A31i2yk/SMteHRzHQlcHu2+djrZJwJoz9Fs2oX9FyQsL8Y7KUBxaB/2mWuKThvoC18QkTOH09oDeFiW0tfGrv3f7dhb9gIFvS+O3KpVqyzPCpKIupbNjDOxSBmAm13mWYjLpvzIQYvJBC/HFTL0a5+gXtHX9E7vYe+BtGvhxM6GQxf5CTD0b0l3PogJS3GRsSMHRRI6hRRyokmx9+OiEbrPANoiE/c/6Jbp9I4clhsywYtGQ5Z80N9yn8oWL7Sp+FCaU3l3N3pKjgXIzNh5jDIBj2XRazpDttMGpZTkNljyowFlrSMEWx6w0NkiA+l0WOoe5H5HkVkGu5Pruj4kk/vjjz9a9ExGl008ytA+wxBjh07vHeBHI1vaCNTpYUu0tPULvQQcec8JHSBtikvxfob45STi+z39yzbANgsf3GddZm50cinHbjOxtuhLEV4DytsyG4H7nNjspCfq11dw7C5Av0z7Mlr2BCV66HYYBgj0G9B0awlIs88sW9KzvUEZhZ14QK4FL9w70jnldYizL68eRYM3BzqB1SSLown9XkRby8iJtPNH/0db8dijs65rdobx98BNa98G/p3x8uKvMaD4FPWOfo1nAuIt/TbuIwfyD8EFbWMyHc5cO+rhxHTL/aBPODJ25BI4uYuwNG53WdxTodJZHq6UE0BZAMS9fXaGyDhkgMAl3Rs2xmdFGWTd8aGMLKNg8MxqFhX8LLM94Je1jrDZoiPuLTJwT4elvkOuPQ/ReAqwJWsedoF40Pk+y2eXAdst7dCeDh1o01/aCHQ92HgE6P+B4DiLjfQqhNvxgGlBvuF2XpneQ55dR1+whq70FWWmamnNhwGmpY52C/PDbj/aWLc6/pzQX32DGbo/oDwOs3NE2dPD1h5NA2mtM0YQ6MfgDmySH3Am6FWS2MwQ7O+3fPlyy0c90dxIsyyrwvnK+OOsKM/oGbyc+siElYwovR9nlKtT/faDdYQH+KedGEKduwZlsAmwpa+s6VdPks14l4PfJCz3L0SehK9hIwKT/MvYkYPApCPsJLIo2mIAeLwI4/b1K4Af/VwQyYkPlocUaBynQuMzZHuNUU0CNphCTohzIwfYWPLZ71Px8EKbig+lATeLHhTXHexLKH40TNopvpt95JTtEpe93tFSS4RxFv8sG54Ca6dRq0UuZGU9iEA52OUmKxeIc3+Ab9wDK5KPfnUi/ouwrK7RMSVdzolIi/uHkex/iB5hA+B6MHSjbX8SOmSkVeHhMBcO3bi47Blfgpe9LluwzoTx1VdfbX+nhpaMfSmzdPoAn7Ry0C8lvEML586PekrbPsRURBmm1SVGrPkC9Wsy9PmzTcweGBQkONzA0I7P7/FQzqotxOdHHXf66pEcSAte0Ndyb9M97S3yUxuK0eE+YUsd2E/vFsaW+EBDOxA8HcuU5cWECRMS+nHUNUs9yVJEQnaUn70PvgNxfvocpycITRKBekf7cv4WZU4+CH0IR9vROH28thVweROzc44bqTuxz9iRAxiWqV8n5vY4VAx7R7kxjJvqV0BFpK/67GLtMrVWHBKOKfwEbFAwCXFEmy4AM0s++32q/F5oU/GhtBTlbXGUQUvvBeCU2XHNNdeQk2XZJgGyEzoAL9yBg6UOgJ/l9wO98IrSgqd9xJSwFyJoLNjg3p4nys71Gbpbfg0BPC31wzUjGyH4WjACX1822LWJ8XyLvuEldHxn4OG3GXSifaLse0cRz7+g7Tt+jEOJbgP4WzCgfFju2I3OmQY4SgllDjm+lFk6ndzIAW60lG2ZVTBN09UmpMnkUxtGfSKnIEaC+5zYHBOY5gLYJGzlgyy0zIXTugN0ljaMFMuembjXctjxst97FQo76CfGYtnA72CUvWXAjDi7c0c/LRjL49OFZQYSdS1hoOOTnAgb2G1p07jvhT7FT58jo90P0J/RT45diPNQYEBbMyU4zIh/AGXk9OpDxLb4fxk7cgDE8wgBI177F3eRz/3jFfL7GnpanDtU1t0Bjh9LB0lVLaUZOeBr/xLTcco+KVi2hK6uroRf+YATnPDlny1bylt7vQMx/UJGxh0yRko7oR7Zvzh6DXwtB2jsdc/z7x3GM4RDQ06BpeODDM/tMJ5n9BrlaGmbiLfbh6j8HrD/KXR8hIFlFAwMBqGMycnLSsF+/fpRp2x5PxO42PfX8yojIT/09aXM0iniVg5stLRh5EvQOZ2s+HQ4rwlbXECGbzaj/65EG4x9eQhn2/PgETwSvgJFP5MwEwks7O2C9q2LN1fLtR0v+71XobD3W/CwfPSANmPva+3Lqn/zKicdPXSwf0XckC5PNun28sN9IAao8TahbN5Av3YUsKEPxGL9D3TdDGXk6heoMnbk4hVxew1P+L9Q1jLCQSO0bCjrlheM3whLKpPiA+ISZlowO2b/uak+AOg8t3Li6SDrOOg7NT44vfAfn6fYr4GlZdSG+03QyVKFzNR0+xJc06WXXmoZVXlljHrXhHpnXzq0d2Ku2YKXfVNN+pm5hI2XMaKy1z0BR9XihLgWCkI06jNw0nKg3Owj9gNRjhnteYR2uDvair1tJowswT/2MKZr5HO1LI9O7z6UQWM8ELhPtmF1PFnKa9qAG3ws+xgCl585/WpHSkbdiVhWHYz8Tq97dFME44R6Zf8qcVuUH30xnJGCwPC0jDK6zAR9f6OUin15iGzvoe70w9n1AfqEugYHNGFWHXH2fQCr0f9nNGMJmcOBq6VdoI7QMptrvbMhBG6Wjx5QTjGHndof6mr8l+Wvo9/Mas88J10hw/KFMO73By6Wvfqc8jnFActbURbxz+MH7HR4/j9uixsFeQl+go3G8Rb5hkKmpfwozk4MnXYhPKMBNAkzvfY8dI+B6ss4008c4rT2QBm5muzK2JFDAWQ0VY589oZxKwxNGAmtNSP5f1RK2gRyIvjFAqgTGuIla1/It+zGjDy/y7BzvhIyaBo0EgDymm7+iF53oPIkYIPRXkLcuhzJryDDks9+nzxnZP8fS95UtOnSgJkjLzxUZyNv7EVaXNOvF9yVyZc3aACXQI5lJgj2Wjof4p9JAF97vTsP8jyPrlFXqdOhr4zi1XgE8fbfXxWI+xD6z4onxD39RJdnpwOdwn6wwWmmw7Fc4mW6uUY5ToNull9jgCOa0YvO0POvCLF2ieuDgEXChwvg/xRkxh7IoHM9wAIt7Vofb5ovr0yAr2VgAgEbYIb9dpw9H7DP7iBFeMBmX8oswizFP7dy8MD+D2jtA52/JPuyMYVI+sm+i4BhpZ0GcX7anOBggP++dpmp7kHv1PYt9Z/y48FN775aNndFfEYzVZB5K0J8uzhxwoQJn4FfwgE6C172+4QMLiJQzq+inGM2gmcV2mWkv0W8ZTYO9/Zf2HEhIT1Jr169ngVvS1+JZ/kV6XNaKdAfbgf96ae9Is9ipNLZ3ieIiy++mJZyLb8eBXmO7RI8Uh6Qdz1CrPxAfCbwW4Sz/bgeNsb6Ncizv49pp4+/nx9/A3nxznV8kuU6Y0cOimY0VY7Ozd4I6Cs1Tx0lFSKsoELEKXY8CFDtLzZGEqGr/Sdj1kPnbH8YR2iT/UODvhagbh+fjgK6I/4+eg3eCdhgZJcQF6VPdYZMSz77vZe8qWjTpQFDix42egsO0HHoypUrPe0OD3zp59toZ/YYa8j8BKOUZ2MRWVxAJyen5MlrrrnG3QvtkI16twPK3NIpIJoOe/2iuEiAXEt9x31vhEdQVxNmqCIZHP6BdhDaTcJok0jBK1W5EImXYHlvCLz3hLNrn31MyQ/0v0U+2j0/RodyvCF2Y72wb6p8rAfnwSIDbBMGcYjzfMChpWV8+3t4J6F+JjjRqZiD/mKkO268Cnz8LDOIcT68yAHtLfFccL/NsmXLLLMD8elO1yh7ep/wOqc01AHfbIZuCT97BplXo524mpXrrmM0KEe2tQf0exn56X3OiCuQAAAQAElEQVTBtRFx/5F2T9wtXe4EWy+iC7cB9eEo6L2/jd7y253xaZBpwct+H0/r8doyMIZOJ8Juer+U+t8IK8j6HsHzT0pGMqf5R/vaQaZlVg5ZaKBHL//jMv1B5Yf+0D4wX9mzZ09H5xPy7PV4GMqD2md6Yd0UoKcPJOyvDVmee92k9KEKTW5Eb+lc72HmdRhliAufxV0nvczYkQM4lhFDUgm2BFQamqX4Y3w0eB0HoB5FWtpP1kFThUpGHa19l/KkjYKcAeSxvB8A+RdBZsrf6ANN5ADdmdDRUvDgR79H2BQhsP0rpRk5Mh0PP3JkXqLruHA0OrupKK+EL8HiaCKXoLsC+FqWtCgBcVm/90R8KGA0uhDn8xHij22x1DkT8neOj3S6hhN3CMqcfreQPsaIJzkX9ieMBKMESPsL8ll+rgp2jYZD+B54Ou7qHs1LZ+i2G+jnIkRGZuC1lOKjAfcZtcNo/vgz2gn9zik5MvHRD6D+2wdN8emRa5Rzb+hKzoB99PkR+Do647DJ3qFvvXz58ocjDFP8gxz6HcjxNhL6EW1bVGa30OsXwNXyUEfcPyHXcYsKuxTQ0YzktRQPPjQTuZKuowFxvpVZlKfT2Ysc1FP6gs7yAILNv4Qtz99www1O+39ZRIKOXomIvRMK2ZZ6Cl6+2Yy2/Cn4W5bMwH842tSz6V51QfrGqGNPg96yvIa8ZL/FpugN6u/jkGf/vdvr0C4szmCU3n4GNhMgz/LqBfh9Dcyp37STR+5Bb8HLfh8hyuAf5NoHhL+A7UeCVayMIeufaM+WWTOk+3bACaP+xPIBG2S+jP7wcDdCMMB4DPSW8oNdD1500UWWj3aivFBf6PdKLVgj/7UoF8vEQZTefkY502sGlp8ogzz6VRq7gx/JirSYkxmJwD9M5EwmBxSXSQ/oQwOhs+MJwMtVv5axIxcvzOs1GgZ1+ARuLCuA/TnCQoB2nNMsCXm0SLsdlY4emvbdmulhapmSjDHuvgAgZyDQNHl3jKBtAM4FeLTGXouKS6MSEf+HtFqEp6DX3fHxuF6GuIzfsUL+ojvQOGnGwv4u2z4or8XA8C6U3b4ow8gu5sB6IMKuiL8c8Z8CjMsRLAfK6tfo6CwPFgtBBjfgdyv4Ph+fFeVIX27NgS5PQZej0JlEfjkA+m2EuJ0Rfo34N7vzxTq7bh5Pg2fa2WTkJcfA3jHuhPhPwPufCA1RufQzNpBdhbhfQPaLkPMOdIwMcED/Hq5vQpy2A+V1AuRYNumETHoX5Q3osxt0s/wCBO6HIP6PoKGO2bI0SnxQLywbjMYrDuyow7O3WxoAzARf+28yCmByMGSRU2h5iEPOh+hTfPvNRnT8n8IeetjEq0vXV0EH2ol9AvQbHe2nUK/LodceSKOHAzkw8e/9ngj9LI4cMQposCyvdet4yKpVq9ph250I+6KeRgYfcIg2BQY1sPs8xNNP6sWWpGHv34CfpX/v5uXbCfyvAjP7xt77YWD2EXQ6A/pZNuiGrtSez0A6bfdg3/z3XyjzlPr27t37l7DL/vy4jGwHJmPszi7kbQE9zkJYAj1JV5xiB9WHpO0iRqXhAnrRO+qTo6yBI70raJ/QcFq9iGbJ+gwdfkS/YPlCFnr0Bb7PAM+rgadl14KoQGD5M4QFoLXsA4h8cxBSDrIgj9qz5RUg8L0E8ujXFfa3lx/SBPTYCekPQ95LCHb/gGYyHX8hCPbNgj4Wxx/5a+CAtoLfMcQ7PoB+d9hF7YcGQvHPmJXgY1klic8Xf50XR44UALD0lQY9qOg2EmAsbZr3L3ivS2HY9zD6XZyn4/wl6Jcg3Wk3d3Li0j5MAdaPeEjRnj3kOETkdf+jtfWZSFsJWZ8gkGPXijM9zGaChkYrOMUO6jwOxEPIsiwUSy3RC+D7NcqIlpLabBDQztpnoexeRTo5dQpYf4ZAm1TSTJzTi6Bn48FsWZK08cz4Fg3jWATLi/LdzI6Ejv9G2gcoe9KRNoelrxj/ivg9u2liJ9D9A3XAPtUeS4+/ADb0hRzNIFEHHp9Eg4kTwJ/2tYrIXbNmzffApgVxNDMV/9HId6FQ6GjIzWaHd4tsp5sJEyZ0QDaVo90p3wv070C3n4APlSO1ky9wT+3pJuSxfAkOPX9EoBeZLe8IgoflQJ2gB5p9JF0Lvq+j3X8HWdT+38R5BWTQu66Eo4UH5GT8AYmFUdwNyvZe8E14/QI6UH29CvpN6+6nFGygB/xbSLsYLOKX6q9HPXaqayDTcWTHEzbPh83k5FAfF2MGuwYgnI0QeccKZaHgEH0FDMiBuwXx8V8CtoDH72KZNV2QrmBNH5JYdEUc9Tf3QL+vUX8+hq5UTz+BrtSeaQaF0kEWO2b369fP8rNLsZS4C1oSBI/9YNsHcdHUfmsQ99rq1at/hKwlkEn1tg201H5oSS/hYwbgVY968Uo8n1xeQ769b42tMsCWmcCWJku0qoQ+8Q3IqkegGeuYLOh2KeI+BJYKYRYCDSDpJ/poqZlW1XaKEa+9mAt66mccnaq1JEJA3iq0U3r+WyYHIG8Ewn/jyw8y56AcvwFfchoTBjegPwLll3LgiFW5MyHb8i4n8m2D8AT4L0cgH4PqJvX3tMJIM9rIYjn+AL3t765aCKI3GTtyMJKAjfLxfIaCPwIM6jSSOWG0GSi9WD4KxtOowSID8qngTkelS5bfQk83GHV9hMKsQ9636N4h0GiTHDtap7Y3eCInj35/yEzpxJXgO3KEDTWWD4DvCNy8iuD5QLnQzt97A1/7DKhnXskyoN4tR70bD1mO7/Iky2eLPxc8nBqejWzdLehfBjbkECZsbLuOyvkKur6DvHVwsj5DW7C0O/u9MwdvscB/NpzGWsilgYxTZppZpXYSewDYiMgRHQOsUzpxAn+gaYVtB0EWlT1i1h2wjZblqf0TbvZXKehdlOXIdwh4WLbPWMchuyuU2U3gT5tyxrYE8MCRBpjk2NHDXnuZOekF/CxynWjscbCZBte0nYd9QGYndbr/F8pyDMpjFXCzyLbfCx/+UE/fhjx6t4oGhQkcYf82iKR6Sv06LhOOfyP/fvS1ckKKQwSeHx/36tWLnknJZu+2gsy9ESKvQTiwoNnAMeCTtn+042W/d+DtOgrym8CPZuac8midjYsXiLo2BfhXQ5dk/Qx9kEIDSPr5vvis0evJZWVlaZ24KDHq5VLIo77E6T1nIouUHy52RhlGVkFwHTug5xKEeuCXLH+Mlj6ChDNPv+Tg9DHEeiAkH4PqppOfgWRBG0+7LouMHTmS5EdAYzwX4NCDNWEfriT8aVlzEvJsjbyWFzeT0FuiUZjfogJR5SC5TiBb6OkGshYhnAh5lQgpnTiiL5XgZCfw/R4YUQU+C+muRnbA9msEemjujLz2d7TAxv8DdYC+kKURveXdhzSS6EG1C3R0PXiI5wdsZqFx0/519N6cfak1njR6TUu6p0BX2nU+9rVZNFHnmbZ86d+//94oF3qflWbd3Iij9xCPAz7DESwj31SZgct0yKpwKwt09H7KXRj1bgNsyPFIxT6rNPB/Hg8LepBMhNxkD7+IDKR/hUAzVENhf0Z1JMIoz/+g+3w88Og3In8LVcj5wCnlQe+cHYx8P0dZ0gA7JbGfiZA3D3LJmTsO2NNHEAmz3g7yqF/6BfIdg/y08uJA4hxF72Eh34GQdRZCqzOVNRZ07Qi/Qj6qF/YvYK3EObqDo+L07FyJJeSELZN0qoSZr3a0sVHAh1a+kjnIFhVAS21+NPA8DA4TzbRa0lPdoLxXIN8RoKGl8rQDTdDRgJHa/TnQsxyB6hhFpw0YeHeAnpaJSRat7qTNAwIaXOwAHR0/pEC64+HakcMD6H4UPn25EQ2R0aYjV4+RMLYRgbZXoN3AqcOknxOhl0NpKp8KjR58f0IBHo0OZgg84itQIJYpWY8iBYC6HTLpE+ZDkZc+F34A/GkZ5HXck8d9M+5/C5sPJjqERxDv6oBuXyBfFKfIGRmpMuDk7QDuz8Tzgv1/SMYBD5zmeFrQkW04eT9gO30qH9GdeEKP//PCBXjdA4zpdzBpBEQvflPHQbhOBR8aET4EGfSu5M9BuynCnyZNmkTvFyHZ3QG9LkaI6Qh+rkcwJAH16CXoOA6Y0oidpvRp6eUJ8HkFgerdozj/GeE80GwKWnpQWT5cID5eAjVu8DkTPGnJ5XzkvRPXjyG8jPAiAjm0p0AeDVT2Bi707gTIMjvAZ594jLAc6LZDETRTAfm3QF9aEqC65NhOoBktu9HrBjuCNuGjFaSnPeJlgZjqzYXAgvqByTjTII8eMDfClsOg03oIv0Un7nl2E7w9HyQHdl0JmVtCF5qhuwBM/o5r0ouWwC+AXvsjfXOEP6Je2Z2fw5Aeq6cok6QzMiifR+NpIecchIwOyKFXGmJyMcvq+iGEtrgCttwFu4eSPlCA9LgdNlM9pX7yasQfBRkbg+Yo2Gz52Al0tFVDTDbuXX0YADkZHdDhCehbjzO9a0VLoDQAoS/np0I22U3lRdtc1IGGBhr0fmZGsigTZN2DUA379wH/6xDuR6D3N6cinfo3+nDo94gbO3HixMETJ050/KIStI4H8t0JfLXhh0GQpX8nWbBld1pCdlQoReSkSZO+pvzxYf3110/2taUjJ+DzDMrlQPCgrZlOhv30IQK9y0flR0uqVyPjadBxJGgPAS19eIaozA7kfxB8asGPPjC4GvL+hkDLpSRvCq4j/T70acAgcxvQu3pXzUkb5CVZI/EMpdcyqE7Qkjv9ksNU0D/dLevUnj17DgAtDS7oVRwkuT9cO3JoqJ8ixH7aAgJpVONekgtK8F8IvtRh0k/yHINr6hyp0M4E6DchPDVp0iRfR3yQ+QLkXAzepyKMx/UYhCMQLsD9XUi3dFAuzIiQIF8MK7qG3m5mYCJ54//hwf8Z5Y8G8En6IKY9c6J0dIYNGc9uQc6HxCMuWNb743VMdQ0d3ka4FIGWwQnXfXHdAGxppumPuKYHdCoWSdOQtyVOP/pCNqNZK9i6GLyuhU5n4XwczgcgUL07AeffIdwGmoSlv6SKuUgAv28h61YEGukdDxkHIRyC8CeEh5C+2IkNGr3lXTTQLEdIeoDPGzaMPM1ARBmDR9J2AhvuRrqr0XSUX6oz+LUg3AgcqB84DOf9cE+//Xoh5FDnniq71jTo8jx0uRnhNFyTXifj+mboldQ5Q/rbSI/1ByiTpO+90AxFPC3yzs7UIMiZFc+LZlkz4UU8oMedCPRKAdVT6icRfdnTkPGtE0/EfwCCeJsXONHpiEO5vIZAA5BfQud9cU0OHpXXJNzTe32+iYWdb4D/JQi/Qjgc/KP923m4vgNxlo+r3AoG30U68bM/K0gWZCZ9tqTTm/LHBxqYpcvjlA4eHwO3h4HbBJwPQ6DyOx7nyxD+no2OTvLA7z3wvQzyfo1wJK5JHr3DGOn3oU9TprbY5eFZ3gb+VCd+i/NRCFRXjoJckvUARz30MQAAA9hJREFUzfba87i9d+3IuWXIdIwAI6APAYwQaZkvJkApRV/Fxe75woYA3zICjAAjUOQIsCNX5AXM5hUdAhZHDo6dpyWMokODDWIEGAFGoMQRYEfO3wrA3BgBCwJYKrvjyiuvpE/pIwH3jl/YWTIlucEyAP2yyOj4ZMzITY2/52tGgBFgBBiB0kKAHbnSKm+2NscIYMbsvXiRuN8Vzpz9p3riSZJeIy/tyh6KEsCJo6996QXdaBSfGQFGoOAQYIUZgewQYEcuO/w4NyOQEgHTNOnl/GU2oocnTZpEX2fZopPfYlbveDhytM1CjAj3xKcrFsEXjAAjwAgwAiWHADtyJVfkbHAuEYDDRpvWWjY4hgM2EGHaxIkTaWuWtOpgBu83IKLtW3CKHV+WlZVdH7vzcMGkjAAjwAgwAsWDADtyxVOWbElAEejfvz/tX2X5TVE4chuFQqE3MdP2HgL9bt8gu/qIp9/6nQLavyDN/ssGx9H+ZojngxFgBBgBRqCEEciBI1fC6LLpjAAQoH2IDMM4VCnltBM8/RzSP5DegZm3/8F5ewPnhTjTTxzRT9fQBrTgsu6AY0d7ENHG1esi+YoRYAQYAUagJBFgR64ki52NzjUCEyZM6Ojbt++ucObo1wocxcNBo81+98KZvk5NoEHe5Ujb97LLLqNdwRPSOYIRKBoE2BBGgBFwjQA7cq6hYkJGIDsELrjggp8mTpx4BpZUB4LTrXDMVuDs6gDtG3Di9oQTN9VVBiZiBBgBRoARKAkE2JEriWJmI9MgkNNk+qmkyy+//PyePXsOgoN2PMINCM8jfEGK4EwOXhuum3F9j2maw+AA7oM8cxHHByPACDACjAAjEEOAHbkYFHzBCOQWAfq9QzhojyFchDAWYUs4axLn9XAeglCH67MmTZqUs9+pzC0CLI0RYAQYgUJFIDh6syMXnLJgTRgBRoARYAQYAUaAEfCEADtynuBiYkaAEWAE8oMAS2UEGAFGwAkBduScUOE4RoARYAQYAUaAEWAECgABduQKoJDyoyJLZQQYAUaAEWAEGIGgI8COXNBLiPVjBBgBRoARYAQKAQHWMS8IsCOXF9hZKCPACDACjAAjwAgwAtkjwI5c9hgyB0aAEcgPAiyVEWAEGIGSR4AduZKvAgwAI8AIMAKMACPACBQqAuzIeSk5pmUEGAFGgBFgBBgBRiBACLAjF6DCYFUYAUaAEWAEigsBtoYR0I0AO3K6EWb+jAAjwAgwAowAI8AIaEKAHTlNwDJbRiA/CLBURoARYAQYgVJCgB25UipttpURYAQYAUaAEWAEigqB/wcAAP//5q+qBgAAAAZJREFUAwALHEYxg6JewgAAAABJRU5ErkJggg=="

HEADERS = {
    "Employees": ["Employee ID", "Name", "Band", "Email", "Password",
                  "Address Line_1", "Address Line_2", "City", "PIN", "Phone Number",
                  "Emergency no", "Personal Email ID", "Office Email ID", "Designation", "Profile updated at", "Gender",
                  "Account locked", "Joining date"],      # Update96: "Account locked" = Yes / blank; Update97: "Joining date" (YYYY-MM-DD, set by Admin in Employee Info)
    "Processes": ["Process name", "Target hours", "Target 100%", "Target count / hour", "Target count / 8 hrs"],
    "Productivity log": ["Submission ID", "Date", "Band", "Employee ID", "Employee name",
                         "Type", "Process / Description", "Hour", "Count", "Submitted at", "Description"],
    "Leave": ["Date", "Employee ID", "Employee name", "Band", "Reason", "Applied at",
              "Status", "Reviewed at", "Reviewed by", "Day type"],
    "Permissions": ["Permission ID", "Date", "Employee ID", "Employee name", "Band", "Hours", "Reason",
                     "Applied at", "Status", "Reviewed at", "Reviewed by"],
    "Holidays": ["Date", "Name"],
    # Admin-editable settings (currently: the daily productivity target in hours)
    "Settings": ["Key", "Value"],
    # Background login/logout tracking (never shown to employees)
    "Attendance": ["Session ID", "Date", "Employee ID", "Employee name", "Band",
                   "Login time", "Logout time", "Duration", "Logout type"],
    "Notifications": ["Notification ID", "Time", "Employee ID", "Employee name", "Event", "Seen",
                      "Section", "Action", "Details"],
    # Audit Log permissions set by Admin: one row per employee. Processes = the ticked process names "A | B | C".
    "Audit Access": ["Employee ID", "Employee name", "Enabled", "Processes", "Updated at", "Updated by"],
    # Mahizhchi (Update62): Admin's questions (A-D options, one ✓ correct answer) and which employees may view them.
    "Mahizhchi Log": ["Question", "A", "B", "C", "D", "Correct Answer"],
    "Mahizhchi Access": ["Employee ID", "Employee name", "Enabled", "Updated at", "Updated by"],
    "Mahizhchi Answers": ["Employee ID", "Employee name", "Question ID", "Question", "Answer", "Submitted at"],
    # Update84: one row per employee PER SET: when they pressed Start (timer runs from this SERVER time), when the Set closed, and its result
    "Mahizhchi Attempts": ["Employee ID", "Employee name", "Started at", "Closed at", "Set", "Answered", "Correct", "Result", "Extra seconds"],
    # Update85: Connection Game (bonus round after all 5 Sets are won). 4 rows per Game = 4 groups of 4 words.
    "Mahizhchi Connections": ["Game", "Group name", "Word 1", "Word 2", "Word 3", "Word 4"],
    # Update90: optional list to SWITCH OFF the Daily Productivity Entry for an employee (Enabled = No). No row / Enabled = Yes -> has access.
    "Productivity Access": ["Employee ID", "Employee name", "Enabled", "Updated at", "Updated by"],
    # Update90: one row per reminder e-mail (and one \"__RUN__\" row per day = the worker that sends that day's batch, so workers never double-send)
    "Email Log": ["Date", "Employee ID", "Employee name", "Email", "Sent at", "Status"],
    # Update92: one row per Missed Entries e-mail. "Dates" = the missed dates in that mail (used so the same date is never e-mailed twice by Auto).
    # A "__RUN__" row (Mode = Auto) claims one automatic run per day so several workers never double-send.
    "Missed Email Log": ["Date sent", "Employee ID", "Employee name", "Email", "Missed dates", "Count", "Sent at", "Mode", "Status", "Sent by"],
    "Mahizhchi Connection Attempts": ["Employee ID", "Employee name", "Game", "Started at", "Closed at", "Solved", "Mistakes", "Result", "Extra seconds"],
}
PERSONAL_FIELDS = ["Gender", "Address Line_1", "Address Line_2", "City", "PIN", "Phone Number",
                    "Emergency no", "Personal Email ID", "Office Email ID"]
# Office Email ID is not typed by anyone: it always mirrors the employee's login Email.
EDITABLE_PERSONAL = [f for f in PERSONAL_FIELDS if f != "Office Email ID"]
# Address Line_2 (flat / landmark / area) is genuinely optional, so a blank one must not make a profile
# "incomplete". Everything else the employee can edit is required.
OPTIONAL_PERSONAL = {"Address Line_2"}
REQUIRED_PERSONAL = [f for f in EDITABLE_PERSONAL if f not in OPTIONAL_PERSONAL]
# Gender is admin-only: employees never see or submit it on their own Personal details page,
# so it must not appear as an editable/required field there.
EMP_EDITABLE_PERSONAL = [f for f in EDITABLE_PERSONAL if f != "Gender"]
EMP_REQUIRED_PERSONAL = [f for f in REQUIRED_PERSONAL if f != "Gender"]

def missing_personal(emp_row):
    """Names of the required personal details that are actually blank (empty list = complete).
    Employee-facing, so Gender (admin-only) is excluded even if blank."""
    return [f for f in EMP_REQUIRED_PERSONAL if not str(emp_row.get(f) or "").strip()]
# Columns shown on Admin -> Employees, in this display order (personal fields live on the
# Personal details pages). Display order != sheet column order, so reads/writes map by name.
LIST_HEADERS = {"Employees": ["Employee ID", "Name", "Designation", "Band", "Email", "Password"],
                "Processes": ["Process name", "Target hours", "Target 100%", "Target count / hour"]}   # Update94: Admin sets the count per hour; the 8-hr figure is derived internally
def list_heads(sheet): return LIST_HEADERS.get(sheet, HEADERS[sheet])
OPTIONAL_FIELDS = set(PERSONAL_FIELDS) | {"Status", "Reviewed at", "Reviewed by", "Target count / 8 hrs"}   # Processes: fill EITHER target column   # not required when admin adds/edits an employee
LOCKED_FIELDS = {}   # nothing locked: admin can add/edit personal details; employees can also edit their own via /employee/profile
KINDS = {"employees": "Employees", "processes": "Processes", "leave": "Leave", "holidays": "Holidays"}

app = Flask(__name__)

# ---------------------------------------------------------------- performance: slow-network optimizations
# 1) Serve /static (e.g. the login background image) with a long cache lifetime, so it is only
#    downloaded once per browser rather than on every login-page view.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 604800  # 7 days

# 2) Gzip every response on the way out. Every page here is a single self-contained HTML document
#    with its CSS/JS inline, so compressing that text is the single biggest win on a slow link -
#    typically a 70-85% size cut for HTML/CSS/JS with zero effect on how the page looks or behaves.
import gzip as _gzip
@app.after_request
def _compress(resp):
    accepts = request.headers.get("Accept-Encoding", "")
    if ("gzip" not in accepts or resp.direct_passthrough or resp.status_code < 200
            or resp.status_code in (204, 304) or "Content-Encoding" in resp.headers):
        return resp
    mimetype = (resp.mimetype or "").lower()
    compressible = mimetype in ("text/html", "text/css", "application/javascript", "text/javascript",
                                 "application/json") or mimetype.startswith("text/")
    if not compressible or resp.calculate_content_length() is None or resp.content_length < 500:
        return resp
    resp.set_data(_gzip.compress(resp.get_data(), compresslevel=6))
    resp.headers["Content-Encoding"] = "gzip"
    resp.headers["Vary"] = "Accept-Encoding"
    resp.headers["Content-Length"] = resp.content_length
    return resp

@app.errorhandler(405)
def _method_not_allowed(e):
    """Update88: never show "Method Not Allowed" to a user - send them back to a page that works for their role."""
    if session.get("role") == "employee":
        return redirect("/employee/mahizhchi" if request.path.startswith("/employee/mahizhchi") else "/employee")
    if session.get("role") == "admin": return redirect("/admin/summary")
    return redirect("/")

@app.errorhandler(500)
def _server_error(e):
    import traceback; traceback.print_exc()
    try:
        if request.method == "POST" and session.get("role") in ("employee", "admin"):
            flash("Something went wrong and the request could not be completed. Please try again in a few seconds.", "error")
            return redirect(request.referrer or ("/employee" if session.get("role") == "employee" else "/admin/summary"))
    except Exception:
        pass
    return ("<h2>Something went wrong</h2><p>Please wait a few seconds and <a href='/'>try again</a>.</p>"), 500

@app.errorhandler(APIError)
def _handle_sheets_api_error(e):
    # Reached only if retries in _with_retry were exhausted (Sheets still
    # unavailable/rate-limited after ~6 attempts with backoff).
    return ("Google Sheets is temporarily busy handling everyone's requests. "
            "Please wait a few seconds and try again."), 503
def _load_secret_key():
    """Signing key for session cookies. Use the SECRET_KEY environment variable in production.
    If it is missing, a random key is created once and kept in a private '.secret_key' file next to
    this script (so every worker/restart shares it). The old hard-coded default 'change-me' is never
    used, because anyone who knows it could forge an 'admin' session cookie."""
    import secrets
    k = os.getenv("SECRET_KEY", "").strip()
    if k and k != "change-me":
        return k
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".secret_key")
    for _ in range(3):
        try:
            with open(path) as fh:
                k = fh.read().strip()
            if k: return k
        except OSError:
            pass
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as fh: fh.write(secrets.token_hex(32))
            print("WARNING: SECRET_KEY is not set - generated one in", path,
                  "- set the SECRET_KEY environment variable for production.")
        except FileExistsError:
            time.sleep(0.1)                     # another worker is creating it; read it on the next loop
        except OSError:
            break
    return secrets.token_hex(32)                # last resort (read-only disk): valid for this process only

app.secret_key = _load_secret_key()
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
                  SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1")   # set COOKIE_SECURE=1 when served over HTTPS
app.jinja_env.filters["t12"] = t12
app.jinja_env.filters["cnt"] = lambda x: "{:,.2f}".format(float(x or 0)).rstrip("0").rstrip(".")      # 8000 -> 8,000
app.jinja_env.filters["g"] = lambda x: "%g" % (float(x) if str(x).strip() else 0)
app.jinja_env.globals["PERMISSION_MONTHLY_LIMIT"] = PERMISSION_MONTHLY_LIMIT
app.jinja_env.globals["LEAVE_MONTHLY_LIMIT"] = LEAVE_MONTHLY_LIMIT

@app.before_request
def _idle_auto_logout():
    """If nobody has clicked anything for SESSION_IDLE_MINUTES, the system logs the
    user out itself. That gets saved as an automatic logout, distinct from a manual one."""
    if request.endpoint in (None, "static", "logout"):
        return
    if session.get("role"):
        now_ts = time.time()
        last = session.get("last_seen")
        if last and now_ts - last > SESSION_IDLE_MINUTES * 60:
            was_admin = session.get("role") == "admin"
            track_logout(auto=True, reason="Inactivity")
            session.clear()
            flash(f"You were logged out automatically after {SESSION_IDLE_MINUTES} minutes of inactivity.")
            return redirect("/admin/login" if was_admin else "/employee/login")
        if request.endpoint in ("employee_ping", "gc_state"):          # heartbeat: shows "online" but must NOT reset the idle timer
            online_set(session.get("att_id"), session.get("att_eid"), session.get("att_name"), active=last)
            return
        session["last_seen"] = now_ts
        if session.get("role") == "employee":
            online_set(session.get("att_id"), session.get("att_eid"), session.get("att_name"), active=now_ts)

# ---------------------------------------------------------------- role separation (Admin vs Employee)
LOGIN_URL = {"admin": "/admin/login", "employee": "/employee/login"}

def _area_of(path):
    """'admin' for /admin and /admin/..., 'employee' for /employee and /employee/..., else None."""
    p = path.rstrip("/") or "/"
    if p == "/admin" or p.startswith("/admin/"): return "admin"
    if p == "/employee" or p.startswith("/employee/"): return "employee"
    return None

def _wrong_area(area):
    """Someone signed in with the OTHER role: send them to their own page - never show them this area."""
    flash(f"Access denied: that page is for {area} users only.")
    return redirect("/admin/log" if session.get("role") == "admin" else "/employee")

@app.before_request
def _role_wall():
    """Every /admin/* URL needs an admin session and every /employee/* URL an employee session,
    so a route added later without @need() is still protected. The two login pages are handled
    by their own views."""
    area = _area_of(request.path)
    if area is None or request.path.rstrip("/") in LOGIN_URL.values():
        return
    role = session.get("role")
    if role == area:
        return
    if not role:
        return redirect(LOGIN_URL[area])
    return _wrong_area(area)

@app.after_request
def _no_store_private(resp):
    """Signed-in pages must not be kept by the browser/proxies, so the Back button after logout
    cannot show an Admin or Employee page."""
    if session.get("role") and request.endpoint not in ("static", "photo"):
        resp.headers["Cache-Control"] = "no-store"
    return resp

# ---------------------------------------------------------------- Google Sheets
#
# Under concurrent load (multiple users hitting the app at once) Google Sheets'
# API quota (per-minute read/write limits) gets exceeded quickly, since every
# page view previously made a fresh API call. That raised an unhandled
# gspread.exceptions.APIError -> Flask 500 "Internal Server Error".
#
# Fix: (1) every Sheets call is retried with exponential backoff+jitter on
# 429/500/503 instead of failing immediately, and (2) reads are cached for a
# few seconds so 20 people loading the same page doesn't mean 20 API calls.

_RETRYABLE_CODES = {429, 500, 502, 503, 504}

def _with_retry(fn, *args, **kwargs):
    """Call a gspread function, retrying on rate-limit / transient errors."""
    delay = 0.5
    for attempt in range(6):
        try:
            return fn(*args, **kwargs)
        except APIError as e:
            code = None
            try:
                code = e.response.status_code
            except Exception:
                pass
            if code in _RETRYABLE_CODES and attempt < 5:
                time.sleep(delay + random.uniform(0, 0.3))
                delay = min(delay * 2, 8)
                continue
            raise

_book = None
_book_lock = threading.Lock()

def book():
    global _book
    if _book is None:
        with _book_lock:
            if _book is None:
                creds = Credentials.from_service_account_file(
                    CREDS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"])
                client = gspread.authorize(creds)
                b = _with_retry(client.open_by_key, SHEET_ID)
                have = {w.title for w in _with_retry(b.worksheets)}
                for name, h in HEADERS.items():
                    if name not in have:
                        _with_retry(b.add_worksheet, title=name, rows=1000, cols=max(12, len(h)))
                    ws = _with_retry(b.worksheet, name)
                    if ws.col_count < len(h): _with_retry(ws.add_cols, len(h) - ws.col_count)
                    if _with_retry(ws.row_values, 1) != h:
                        _with_retry(ws.update, range_name="A1", values=[h])
                _book = b
    return _book

def ws_of(name):
    """Get a worksheet, with retry on transient/rate-limit errors."""
    return _with_retry(book().worksheet, name)

# Short-lived cache for reads: cuts repeated-page-load API calls under
# concurrent traffic. Any write (see invalidate_cache) clears the relevant
# entry immediately, so nobody sees stale data after their own action.
_ROWS_CACHE_TTL = float(os.getenv("ROWS_CACHE_TTL", "4"))
_rows_cache = {}
_rows_cache_lock = threading.Lock()

def invalidate_cache(name=None):
    # SAVE FIX: with several server workers each has its own cache, so after a save the redirect could
    # land on another worker still holding the old rows (looked like "not saved"). Mark this user's
    # session so their next reads go straight to the sheet.
    try:
        if has_request_context():      # Update96: only the sheet that was written is read live; every other sheet stays cached (much faster page after Save)
            now_ = time.time()
            fs = {k: v for k, v in (session.get("fresh") or {}).items() if v > now_}
            if name is None: session["fresh_all"] = now_ + 10
            else: fs[name] = now_ + 10
            session["fresh"] = fs
    except Exception:
        pass
    global _holidays_cache
    if name is None or name == "Holidays": _holidays_cache = None
    with _rows_cache_lock:
        if name is None:
            _rows_cache.clear()
        else:
            _rows_cache.pop(name, None)

_ROWS_STALE_TTL = float(os.getenv("ROWS_STALE_TTL", "90"))   # older than this -> wait for a fresh read
_refreshing = set()

def _fetch_rows(name):
    recs = _with_retry(ws_of(name).get_all_records, numericise_ignore=["all"])
    for i, r in enumerate(recs, start=2):
        r["_row"] = i
    with _rows_cache_lock:
        _rows_cache[name] = (time.monotonic(), recs)
        _refreshing.discard(name)
    return recs

def _refresh_bg(name):
    """Re-read one sheet in the background so the request that noticed stale data is not kept waiting."""
    with _rows_cache_lock:
        if name in _refreshing: return
        _refreshing.add(name)
    def run():
        try: _fetch_rows(name)
        except Exception as e:
            print("cache refresh error:", e)
            with _rows_cache_lock: _refreshing.discard(name)
    threading.Thread(target=run, daemon=True).start()

def rows(name):
    """Cached sheet read. Fresh (< TTL): served from memory. Slightly old: served instantly while a background
    refresh runs (so a page never waits on Google for data it already has). Own writes and 'fresh_until'
    sessions always read straight from the sheet, so nobody misses their own changes."""
    now = time.monotonic()
    try: bypass = has_request_context() and (session.get("fresh_all", 0) > time.time() or (session.get("fresh") or {}).get(name, 0) > time.time())
    except Exception: bypass = False
    with _rows_cache_lock:
        cached = _rows_cache.get(name)
    if cached and not bypass:
        age = now - cached[0]
        if age < _ROWS_CACHE_TTL:
            return [dict(r) for r in cached[1]]
        if age < _ROWS_STALE_TTL:
            _refresh_bg(name)
            return [dict(r) for r in cached[1]]
    return [dict(r) for r in _fetch_rows(name)]

EMP_PAGE_SHEETS = ("Employees", "Productivity log", "Processes", "Leave", "Permissions", "Settings", "Holidays", "Mahizhchi Access")

def _prewarm_employees():
    """Update114: while the Employee login page is open, refresh the Employees list in the background (only if it is not fresh already),
    so the password check after 'Log in' is served from memory instead of waiting for Google Sheets."""
    try:
        with _rows_cache_lock: c = _rows_cache.get("Employees")
        if c is None or time.monotonic() - c[0] > _ROWS_CACHE_TTL: _refresh_bg("Employees")
    except Exception:
        pass

def warm_employee_cache():
    """Read every sheet the Employee dashboard needs, all at once."""
    ths = [threading.Thread(target=_safe_fetch, args=(n,), daemon=True) for n in EMP_PAGE_SHEETS]
    for t in ths: t.start()
    for t in ths: t.join(timeout=25)

def prefetch(*names):
    """Load several sheets at the same time (instead of one after another) when they are not cached yet."""
    now = time.monotonic()
    with _rows_cache_lock:
        cold = [n for n in names if n not in _rows_cache or now - _rows_cache[n][0] >= _ROWS_STALE_TTL]
    if len(cold) < 2:
        return
    ths = [threading.Thread(target=lambda n=n: _safe_fetch(n), daemon=True) for n in cold]
    for t in ths: t.start()
    for t in ths: t.join(timeout=20)

def _safe_fetch(name):
    try: _fetch_rows(name)
    except Exception as e: print("prefetch error:", e)

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return 0.0

def parse_rate(x):
    """Update94: Target count / hour may be typed as 1000, 1,000 or '1000 / 1' (count / hours) - returns the count PER HOUR."""
    t = str(x if x is not None else "").replace(",", "").strip()
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*/\s*([0-9]*\.?[0-9]+)", t)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return a / b if b > 0 else 0.0
    m = re.match(r"^[0-9]*\.?[0-9]+", t)
    return float(m.group(0)) if m else 0.0

# ---------------------------------------------------------------- per-process 8-hour targets
TARGET_BASIS_HOURS = float(DAY_HOURS)          # Admin's per-process target is for a full 8-hour day
def _g4(x): return "%g" % round(float(x), 4)

def process_targets():
    """{process name: dict(rate=count per hour, daily=count per 8 hrs)}. Admin may fill either column; the other is derived,
    so processes set up before the 8-hour column existed keep working unchanged."""
    out = {}
    for r in rows("Processes"):
        hourly, daily = parse_rate(r.get("Target count / hour")), parse_rate(r.get("Target count / 8 hrs"))
        if hourly <= 0 < daily: hourly = daily / TARGET_BASIS_HOURS
        elif daily <= 0 < hourly: daily = hourly * TARGET_BASIS_HOURS
        if no_count(r["Process name"]): continue          # Update93/94: Training, Other(s) and POC_Sample never have a count target
        out[r["Process name"]] = dict(rate=hourly, daily=daily)
    return out

def process_rates():
    return {n: t["rate"] for n, t in process_targets().items()}

def proc_targets_sync(h, d, old_h="", old_d=""):
    """Keep 'per hour' and 'per 8 hrs' consistent when Admin saves a process. Returns (hourly, daily, error).
    If both are given and they disagree, whichever one Admin just CHANGED wins (the 8-hour figure if both changed)."""
    B = TARGET_BASIS_HOURS
    hn, dn, ohn, odn = parse_rate(h), parse_rate(d), parse_rate(old_h), parse_rate(old_d)
    if hn <= 0 and dn <= 0:
        return "", "", "Enter the Target count / hour - it must be more than 0."
    if hn > 0: dn = hn * B                  # Update94: Target count / hour is what Admin sets; the 8-hr figure follows it
    else: hn = dn / B                       # legacy rows that only have the 8-hr figure
    return _g4(hn), _g4(dn), None

def miss_lines(date, items):
    """items = (process, hours, count). A line is 'missed' when the count is below the Admin target for the hours logged
    (8-hour target, pro-rated to the hours actually booked on that process)."""
    tg, out = process_targets(), []
    for name, hour, count in items:
        t = tg.get(name)
        if not t or t["rate"] <= 0: continue
        need = hour * t["rate"]
        if need > 0 and count + 1e-9 < need:
            out.append(dict(date=date, name=name, hour=hour, count=count, target=round(need, 2),
                            pct=round(count / need * 100), daily=round(t["daily"], 2)))
    return out

def sub_misses(s):
    return [] if s.get("off") else miss_lines(s["date"], [(p["name"], p["hour"], p["count"]) for p in s["procs"]])

def target_alert_text(miss):
    return ("\u26A0 Target not achieved (target = count per hour \u00D7 hours worked) \u2013 "
            + "; ".join(f"{m['name']}: {_fmt_num(m['count'])} of {_fmt_num(m['target'])} ({m['pct']}%)" for m in miss)
            + ". Please complete the target for the hours worked.")

TARGET_KEY = "Daily productivity target (hours)"
def target_hours():
    """Daily productivity target in hours, set by Admin (Overview page). Productivity % = productive hrs / this.
    Falls back to DAY_HOURS until Admin sets one."""
    try:
        r = next((r for r in rows("Settings") if str(r.get("Key", "")).strip() == TARGET_KEY), None)
        v = float(str(r.get("Value", "")).strip()) if r else 0.0
    except Exception:
        v = 0.0
    return v if 0 < v <= 24 else float(DAY_HOURS)

def day_limit():
    """Most hours one day's entry may total: the normal working day, or the target if Admin set it higher."""
    return max(float(DAY_HOURS), target_hours())

def eq(a, b):
    return hmac.compare_digest(str(a).encode(), str(b).encode())

def delete_rows(idx):
    ws = ws_of("Productivity log")
    idx = sorted(idx)
    if idx[-1] - idx[0] + 1 == len(idx):
        ws.delete_rows(idx[0], idx[-1])
    else:
        for r in reversed(idx): ws.delete_rows(r)

def _key(x): return str(x).strip().upper()

def desig_map():
    """{EMPLOYEE ID (normalised): Designation} read live from the Employees sheet."""
    return {_key(e["Employee ID"]): str(e.get("Designation", "")).strip() for e in rows("Employees")}

def find_designation(emp_id, name="", band=""):
    """Designation for an employee: matched by Employee ID; if the ID is not found,
    fall back to Name + Band."""
    emps = rows("Employees")
    e = next((e for e in emps if _key(e["Employee ID"]) == _key(emp_id)), None)
    if e is None:
        e = next((e for e in emps if _key(e["Name"]) == _key(name) and _key(e["Band"]) == _key(band)), None)
    return str(e.get("Designation", "")).strip() if e else ""

# ---- Update105: View-Only productivity access, decided ONLY by the employee's Designation field ----
VIEW_ONLY_DESIGNATIONS = ("Senior Team Lead", "Team Lead", "Associate Manager")
def _norm_desig(d): return re.sub(r"[^a-z]+", " ", str(d or "").lower()).strip()      # case / spacing / punctuation insensitive
_VIEW_ONLY_SET = {_norm_desig(x) for x in VIEW_ONLY_DESIGNATIONS}
def desig_view_only(d): return _norm_desig(d) in _VIEW_ONLY_SET
_vo_cache = [0.0, frozenset()]
def view_only_ids():
    """Employee IDs (normalised) whose Designation is view-only. Re-read every few seconds, so a Designation change applies automatically."""
    if time.monotonic() - _vo_cache[0] > 8:
        ids = frozenset(_key(e.get("Employee ID", "")) for e in rows("Employees") if desig_view_only(e.get("Designation", "")))
        _vo_cache[0], _vo_cache[1] = time.monotonic(), ids
    return _vo_cache[1]
def is_view_only(eid): return _key(eid) in view_only_ids()
VIEW_ONLY_MSG = "Your designation has View Only access to Productivity - entries cannot be added or edited."

def load_subs(emp_id=None):
    """All submissions, or (emp_id given) only that employee's - far less work on a big Productivity log."""
    T = target_hours()
    dm = desig_map()
    tph = process_rates()
    ded = deduction_map(emp_id)
    subs = {}
    want = _key(emp_id) if emp_id is not None else None
    for r in rows("Productivity log"):
        if want is not None and _key(r["Employee ID"]) != want: continue
        s = subs.setdefault(r["Submission ID"], dict(
            id=r["Submission ID"], date=r["Date"], band=r["Band"], emp_id=r["Employee ID"],
            emp_name=r["Employee name"], designation=dm.get(_key(r["Employee ID"]), ""),
            procs=[], notes=[], rows=[]))
        s["rows"].append(r["_row"])
        h = num(r["Hour"])
        if r["Type"] == "Process":
            h = eff_hours(r["Process / Description"], h)          # Update90: "Other" always shows / counts as 8 hrs
            rate = tph.get(r["Process / Description"], 0)
            c = num(r["Count"]); t = h * rate
            s["procs"].append(dict(name=r["Process / Description"], hour=h, count=c, training=no_count(r["Process / Description"]),
                                   desc=str(r.get("Description", "")),
                                   target=round(t, 1), pct=round(c / t * 100) if t else None,
                                   earned=(c / rate) if rate else 0.0))
        else:
            s["notes"].append(dict(desc=r["Process / Description"], hour=h))
    for s in subs.values():
        s["prod"] = sum(p["hour"] for p in s["procs"])
        s["non"] = sum(n["hour"] for n in s["notes"])
        s["total"] = s["prod"] + s["non"]
        s["earned"] = sum(p["earned"] for p in s["procs"])     # hours' worth of standard output
        s["ded"] = ded.get((_key(s["emp_id"]), str(s["date"])), 0.0)          # approved permission / half-day leave hours that day
        s["avail"] = max(T - s["ded"], 0.0)                                   # working hours left = target hrs less those hours
        s["pct"] = (min(round(s["prod"] / s["avail"] * 100), 100) if s["avail"] > 0 else (100 if s["prod"] > 0 else 0))   # available hrs logged = 100%
        # Update94: when the entry has processes with an Admin target, productivity = completed count vs target count
        # (hours of processes without a target - Training, Other(s), POC_Sample - count as achieved). No target at all -> hours-based above.
        _tg_h = sum(p["hour"] for p in s["procs"] if tph.get(p["name"], 0) > 0)
        if _tg_h > 0 and s["prod"] > 0:
            _done = sum(p["count"] / tph[p["name"]] for p in s["procs"] if tph.get(p["name"], 0) > 0) + (s["prod"] - _tg_h)
            s["pct"] = round(min(_done / s["prod"] * 100, 100), 2)
        s["off"] = is_off(s["date"])                            # weekly-off entry: saved, not counted
        # Update66: Admin-set Target Count vs. what the employee completed (target pro-rated to the hours booked)
        s["tgt_total"] = round(sum(p["hour"] * tph.get(p["name"], 0) for p in s["procs"]), 2)
        s["cnt_total"] = round(sum(p["count"] for p in s["procs"] if tph.get(p["name"], 0) > 0), 2)
        s["tgt_miss"] = [p["name"] for p in s["procs"]
                         if tph.get(p["name"], 0) > 0 and p["count"] + 1e-9 < p["hour"] * tph[p["name"]]]
        s["tgt_state"] = ("off" if s["off"] else "none" if s["tgt_total"] <= 0
                          else "miss" if s["tgt_miss"] else "met")
    return sorted(subs.values(), key=lambda s: s["date"], reverse=True)

def get_sub(sid):
    s = next((s for s in load_subs() if s["id"] == sid), None)
    if not s: abort(404)
    if session["role"] == "employee" and s["emp_id"] != session["emp_id"]: abort(403)
    return s

TRAINING_PROCESS = "Training"      # Update93: Hours + Description only - no Count, no count target; its hours simply add to productivity
def is_training(name): return str(name or "").strip().lower() == TRAINING_PROCESS.lower()
def no_count(name):
    """Update94: Training, Other(s) and POC_Sample take Hour + Description only - no Count, no count target."""
    return is_training(name) or is_other(name) or is_poc(name) or is_genai(name)

OTHER_PROCESS = "Other"
OTHER_HOURS = 8.0          # Update90: the "Other" process always counts as a full 8-hour day, whatever hours were typed
def is_other(name): return str(name or "").strip().lower() in (OTHER_PROCESS.lower(), OTHER_PROCESS.lower() + "s")      # Update94: "Other" / "Others"
POC_SAMPLE_PROCESS = "POC_Sample"   # Update94: like "Other", POC_Sample needs Hour + Count + Description (all required); it keeps the hours entered
def is_poc(name): return str(name or "").strip().lower().replace(" ", "_") == POC_SAMPLE_PROCESS.lower()
GENAI_PROCESS = "GenAI"      # Update103: GenAI follows EXACTLY the same solution as POC_Sample / Others (Hour + Description, no Count, same productivity logic)
def is_genai(name): return str(name or "").strip().lower().replace(" ", "").replace("_", "").replace("-", "") == "genai"
def eff_hours(name, hours):
    """Hours that count for a process line: 8 for "Other" (as long as some hours were entered), the entered hours for every other process."""
    return hours      # Update96: "Other" uses the hours the employee typed - never overridden with 8

def approved_perm_hours(emp_id, date):
    """Approved permission hours for one employee on one date (they reduce the hours that must be logged)."""
    return sum(num(r.get("Hours")) for r in rows("Permissions")
               if str(r.get("Employee ID")) == str(emp_id) and str(r.get("Date")) == str(date)
               and str(r.get("Status", "")).strip() == "Approved")

HALF_DAY_HOURS = DAY_HOURS / 2.0          # a Half-Day Leave removes half of the 8-hour working day (4 hrs)

def leave_is_half(l):
    return str(l.get("Day type", "")).strip().lower().startswith("half")
app.jinja_env.filters["lhalf"] = leave_is_half

def deduction_map(emp_id=None):
    """{(EMPLOYEE ID key, 'YYYY-MM-DD'): hours taken OFF that working day} = APPROVED permission hours + 4 hrs for an APPROVED
    Half-Day Leave. One pass over the (cached) Permissions + Leave sheets; pass emp_id to look at one employee only."""
    want = _key(emp_id) if emp_id is not None else None
    out = {}
    for r in rows("Permissions"):
        if str(r.get("Status", "")).strip() != "Approved": continue
        k = _key(r.get("Employee ID", ""))
        if want is not None and k != want: continue
        key = (k, str(r.get("Date", "")))
        out[key] = out.get(key, 0.0) + num(r.get("Hours"))
    for l in rows("Leave"):
        if leave_status(l) != "Approved" or not leave_is_half(l): continue
        k = _key(l.get("Employee ID", ""))
        if want is not None and k != want: continue
        key = (k, str(l.get("Date", "")))
        out[key] = out.get(key, 0.0) + HALF_DAY_HOURS
    return {k: min(v, float(DAY_HOURS)) for k, v in out.items()}

def day_deduction(emp_id, date):
    return deduction_map(emp_id).get((_key(emp_id), str(date)), 0.0)

def required_hours(emp_id, date):
    """Hours that must be logged for a day to be complete: the 8-hour working day minus approved permission / half-day leave
    (2-hr permission = 6 hrs, half-day leave = 4 hrs)."""
    return max(float(DAY_HOURS) - day_deduction(emp_id, date), 0.0)

def parse_form(emp_id):
    f = request.form; g = f.getlist
    date = (f.get("date") or "").strip()
    err = None
    try: d = dt.date.fromisoformat(date)
    except ValueError: d = None
    rows_p = list(zip(g("pn"), g("ph"), g("pc"), g("pd")))
    procs = [(n, eff_hours(n, num(h)), (0.0 if no_count(n) else num(c)), desc.strip()) for n, h, c, desc in rows_p]     # Update90: "Other" = 8 hrs, others = hours entered
    notes = [(t.strip(), num(h)) for t, h in zip(g("nd"), g("nh")) if num(h) > 0]
    tot = sum(p[1] for p in procs) + sum(n[1] for n in notes)
    half = any(num(h) <= 0 and t.strip() for t, h in zip(g("nd"), g("nh")))
    if d is None: err = "Please choose a valid date."
    elif session.get("role") == "employee" and is_holiday(date):
        err = f"{date} is a holiday{(' (' + holiday_name(date) + ')') if holiday_name(date) else ''}. Productivity entries cannot be submitted or updated for a holiday."
    elif session.get("role") == "employee" and join_date(emp_id) and d < join_date(emp_id):
        err = f"Productivity entry is available only from your joining date ({join_date(emp_id).strftime('%d %b %Y')}). You cannot submit an entry for {date}."
    elif not procs: err = "Add at least one process entry."
    elif any(not str(n).strip() or (not str(h).strip() or num(h) <= 0) or (not str(c).strip() and not no_count(n)) or not desc.strip()
             for n, h, c, desc in rows_p):
        if any((is_other(n) or is_poc(n) or is_genai(n)) and (not str(h).strip() or num(h) <= 0 or not desc.strip()) for n, h, c, desc in rows_p):
            err = "For \u201cOthers\u201d, \u201cPOC_Sample\u201d and \u201cGenAI\u201d, Hour and Description are required (no Count) - please fill them before saving."
        else:
            err = "All Process Entry fields (Process, Hour, Count and Description) are mandatory - please fill every field before saving. (Training, Others, POC_Sample and GenAI need only Hour and Description.)"
    elif half: err = "Please enter the Hour for every note you filled in - a note without hours is not saved."
    elif sum(1 for p_ in procs if is_other(p_[0])) > 1: err = "\u201cOther\u201d can be added only once per day (enter all its hours in one line)."
    elif tot > day_limit():
        err = f"Total {tot:g} hrs is more than {day_limit():g} hrs."
    else:
        need_h = required_hours(emp_id, date)
        if tot + 1e-9 < need_h:
            cut = float(DAY_HOURS) - need_h
            why = f" ({DAY_HOURS:g}-hour day less {cut:g} hr approved permission / half-day leave)" if cut > 0 else ""
            err = (f"Entry incomplete: {tot:g} of the required {need_h:g} working hours logged{why} "
                   f"({need_h - tot:g} hrs remaining). Complete all {need_h:g} hours before saving.")
    return date, procs, notes, err

def live_rows_of(sid):
    """Update103: current sheet row numbers of one submission, read live (cached row numbers can be stale after another Add/Delete)."""
    return [r["_row"] for r in _fetch_rows("Productivity log") if str(r["Submission ID"]) == str(sid)]

def duplicate_entry(emp_id, date, skip_sid=None, fresh=False):
    """Update96: reads just the Productivity log (live from the sheet when fresh=True) instead of building every employee's submissions."""
    recs = _fetch_rows("Productivity log") if fresh else rows("Productivity log")
    k = _key(emp_id)
    return any(_key(r["Employee ID"]) == k and str(r["Date"]) == str(date) and str(r["Submission ID"]) != str(skip_sid) for r in recs)

def write_sub(sid, date, emp, procs, notes):
    if is_view_only(emp[1]): raise PermissionError("View Only designation: productivity entry is not allowed")      # Update105
    now = now_local().strftime("%Y-%m-%d %H:%M:%S")
    base = [sid, date, *emp]      # emp = (band, id, name)
    out = [base + ["Process", n, h, c, now, d] for n, h, c, d in procs] + \
          [base + ["Note", t, h, "", now, ""] for t, h in notes]
    last = None
    for attempt in range(3):          # Update96: retry a failed write, but first check the rows did not already land (no duplicates, no loss)
        try:
            if attempt:
                time.sleep(0.8 * attempt)
                if any(str(r["Submission ID"]) == str(sid) for r in _fetch_rows("Productivity log")):
                    invalidate_cache("Productivity log"); return
            ws_of("Productivity log").append_rows(out, value_input_option="RAW"); invalidate_cache("Productivity log"); return
        except Exception as ex:
            last = ex; print("save attempt", attempt + 1, "failed:", repr(ex))
    raise last

# ---------------------------------------------------------------- login / logout tracking
# Runs silently in a background thread: the employee never sees it and is never slowed down.
# Sheets used: "Attendance" (one row per login session) and "Notifications" (admin alerts).
TIME_FMT = "%I:%M:%S %p"
_att_lock = threading.Lock()
_notif_cache = [0.0, None]          # [fetched_at, rows] - keeps admin polling light on the Sheets quota

def _bg(fn, *a):
    def run():
        try: fn(*a)
        except Exception as e: print("login tracking error:", e)
    threading.Thread(target=run, daemon=True).start()

def _ts(date, t):
    try: return dt.datetime.strptime(f"{date} {t}", "%Y-%m-%d " + TIME_FMT)
    except ValueError: return dt.datetime.min

def _hms(sec):
    sec = int(sec); return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"

def _secs(s):
    try: h, m, x = map(int, str(s).split(":")); return h * 3600 + m * 60 + x
    except ValueError: return 0

def _nid(r):
    v = str(r.get("Notification ID", ""))
    return int(v) if v.isdigit() else 0

def _and_join(items):
    """['Phone Number','Address'] -> 'Phone Number and Address'; 3+ items get an Oxford comma."""
    items = list(items)
    if len(items) <= 1: return items[0] if items else ""
    if len(items) == 2: return items[0] + " and " + items[1]
    return ", ".join(items[:-1]) + ", and " + items[-1]

def notify(emp_id, name, event, now, section="", action="", details=""):
    """One row in the admin Notifications log. Login/logout alerts only use `event`; employee changes also
    fill Section / Action / Details (kept in their own columns so the admin can read and filter them)."""
    _notif_cache[1] = None
    if section and not event: event = f"{action} {section}".strip()
    ws_of("Notifications").append_row(
        [str(int(time.time() * 1_000_000)), now.strftime("%Y-%m-%d " + TIME_FMT), emp_id, name, event, "",
         section, action, str(details)[:1500]],
        value_input_option="RAW")

SEC_PROD, SEC_LEAVE, SEC_PERSONAL = "Daily Productivity Entry", "Leave & Permission", "Personal Details"

def log_change(section, action, details):
    """Record what the logged-in EMPLOYEE just did (Added / Updated / Deleted) for the admin's Notifications log.
    Runs in the background so the employee is never slowed down; admin's own edits are not logged here."""
    if session.get("role") != "employee": return
    _bg(notify, session["emp_id"], session["name"], "", now_local(), section, action, details)

def _short(v, n=60):
    v = str(v).strip()
    return v if len(v) <= n else v[:n - 1] + "\u2026"

def _fmt_num(x):
    return "%g" % x if isinstance(x, (int, float)) else str(x)

def _proc_txt(name, hour, count):
    return f"{_short(name)} ({_fmt_num(hour)} hr, count {_fmt_num(count)})"

def entry_added_details(date, procs, notes):
    parts = [_proc_txt(n, h, c) for n, h, c, _d in procs]
    parts += [f"Non-productive: {_short(t)} ({_fmt_num(h)} hr)" for t, h in notes]
    return f"Entry {date}: " + "; ".join(parts)

def entry_diff(old, date, procs, notes):
    """What changed between a saved entry (old, from load_subs) and the edited form (procs / notes tuples).
    Returns '' when nothing changed. Example: 'Count from 50 to 60 [Data Entry]'."""
    ch = []
    if str(old["date"]) != str(date): ch.append(f"Date from {old['date']} to {date}")
    op = old["procs"]
    for i in range(max(len(op), len(procs))):
        if i < len(op) and i < len(procs):
            o, (n, h, c, d) = op[i], procs[i]
            tag = f" [{_short(n)}]"
            if str(o["name"]).strip() != str(n).strip(): ch.append(f"Process from {_short(o['name'])} to {_short(n)}")
            if abs(o["hour"] - h) > 1e-9: ch.append(f"Hours from {_fmt_num(o['hour'])} to {_fmt_num(h)}{tag}")
            if abs(o["count"] - c) > 1e-9: ch.append(f"Count from {_fmt_num(o['count'])} to {_fmt_num(c)}{tag}")
            if str(o["desc"]).strip() != str(d).strip():
                ch.append(f"Description from \"{_short(o['desc'])}\" to \"{_short(d)}\"{tag}")
        elif i < len(procs):
            ch.append("Added process " + _proc_txt(procs[i][0], procs[i][1], procs[i][2]))
        else:
            ch.append("Removed process " + _proc_txt(op[i]["name"], op[i]["hour"], op[i]["count"]))
    on = old["notes"]
    for i in range(max(len(on), len(notes))):
        if i < len(on) and i < len(notes):
            if str(on[i]["desc"]).strip() != str(notes[i][0]).strip():
                ch.append(f"Note from \"{_short(on[i]['desc'])}\" to \"{_short(notes[i][0])}\"")
            if abs(on[i]["hour"] - notes[i][1]) > 1e-9:
                ch.append(f"Note hours from {_fmt_num(on[i]['hour'])} to {_fmt_num(notes[i][1])} [{_short(notes[i][0])}]")
        elif i < len(notes):
            ch.append(f"Added note {_short(notes[i][0])} ({_fmt_num(notes[i][1])} hr)")
        else:
            ch.append(f"Removed note {_short(on[i]['desc'])} ({_fmt_num(on[i]['hour'])} hr)")
    return f"Entry {date}: " + "; ".join(ch) if ch else ""

def field_change(label, old, new):
    old, new = str(old or "").strip(), str(new or "").strip()
    if not old: return f"{label} set to {_short(new, 80)}"
    if not new: return f"{label} cleared (was {_short(old, 80)})"
    return f"{label} from {_short(old, 80)} to {_short(new, 80)}"

def notif_rows():
    if _notif_cache[1] is None or time.time() - _notif_cache[0] > 8:
        _notif_cache[:] = [time.time(), rows("Notifications")]
    return _notif_cache[1]

def _clock(t):
    """'2026-09-29 10:30:05 AM' -> '10:30 AM' (time of day only, for the one-line summary)."""
    try: return dt.datetime.strptime(str(t).strip(), "%Y-%m-%d " + TIME_FMT).strftime("%I:%M %p")
    except ValueError: return t12(t)

def notif_view(r):
    """Any Notifications-sheet row -> dict(name, id, time, section, action, details, summary, kind, new).
    kind = 'change' for employee edits, 'session' for login/logout. Rows saved before the Section/Action/
    Details columns existed are read from their Event text."""
    ev = str(r.get("Event", "")).strip()
    name = str(r.get("Employee name", "")).strip() or str(r.get("Employee ID", ""))
    sec, act, det = (str(r.get(k, "") or "").strip() for k in ("Section", "Action", "Details"))
    kind = "change"
    if not (sec and act):
        if ev.startswith("Updated "):                       # older profile notifications
            head, _, d = ev.partition(" \u2013 ")
            sec, act, det = head[len("Updated "):].strip(), "Updated", d.strip()
        elif ev == "Changed password":
            sec, act, det = "Account", "Updated", "Password changed"
        else:                                               # Logged in / Logged out ...
            kind, sec, act, det = "session", "Login / Logout", ev, ""
    t = r.get("Time", "")
    if kind == "change":
        summary = f"{name} \u2013 {sec} \u2013 {act}" + (f" {det}" if det else "") + f" \u2013 {_clock(t)}."
    else:
        summary = f"{name} {ev.lower()} \u2013 {_clock(t)}."
    return dict(name=name, id=r.get("Employee ID", ""), time=t, section=sec, action=act, details=det,
                summary=summary, kind=kind, new=str(r.get("Seen", "")).strip() != "Yes", row=r.get("_row"))

def update_entry(r):
    v = notif_view(r)
    return v if v["kind"] == "change" else None

def update_log(limit=200):
    """Employee change entries (not login/logout) for the Employee Info log, newest first."""
    out = [e for e in (update_entry(r) for r in sorted(notif_rows(), key=_nid, reverse=True)) if e]
    return out[:limit]

def note_text(r):
    v = notif_view(r)
    if v["kind"] == "change": return v["summary"]
    return f"{r['Employee name']} ({r['Employee ID']}) {str(r['Event']).lower()} at {t12(r['Time'])}"

def _close_stale(emp_id, now):
    """Sessions from earlier days that never logged out (browser/computer closed, etc.)
    are marked so - the system closed these itself, so they're tagged as an automatic logout."""
    with _att_lock:
        ws = ws_of("Attendance")
        fixes = []
        for i, r in enumerate(ws.get_all_values()[1:], start=2):
            r = r + [""] * 9
            if r[2] == emp_id and r[1] < str(now.date()) and not r[6].strip():
                fixes.append({"range": f"G{i}:I{i}", "values": [["Not recorded", "", "Auto (Session left open)"]]})
        if fixes: ws.batch_update(fixes, value_input_option="RAW")

def _log_login(sid, emp_id, name, band, now):
    with _att_lock:
        ws_of("Attendance").append_row(
            [sid, str(now.date()), emp_id, name, band, now.strftime(TIME_FMT), "", "", ""], value_input_option="RAW")
    notify(emp_id, name, "Logged in", now)
    _close_stale(emp_id, now)

def _log_logout(sid, emp_id, name, band, now, logout_type="Manual"):
    """logout_type is "Manual" (the person clicked Logout) or an "Auto (...)" label
    describing why the system logged them out (inactivity, a fresh login elsewhere, etc.)."""
    with _att_lock:
        ws = ws_of("Attendance")
        ids = ws.col_values(1)
        if sid in ids:
            r = ids.index(sid) + 1
            v = ws.row_values(r) + [""] * 9
            if v[6].strip(): return                      # already closed
            dur = _hms(max((now - _ts(v[1], v[5])).total_seconds(), 0))
            ws.update(range_name=f"G{r}", values=[[now.strftime(TIME_FMT), dur, logout_type]], value_input_option="RAW")
        else:                                            # login row missing: still keep the logout
            ws.append_row([sid, str(now.date()), emp_id, name, band, "", now.strftime(TIME_FMT), "", logout_type],
                          value_input_option="RAW")
    notify(emp_id, name, "Logged out" if logout_type == "Manual" else f"Logged out — {logout_type}", now)

def track_login(emp_id, name, band):
    """Start the day's clock: called right after a successful login (Admin or Employee)."""
    session["att_id"] = uuid.uuid4().hex[:12]
    session["att_eid"], session["att_name"], session["att_band"] = emp_id, name, band
    session["last_seen"] = time.time()
    _bg(_log_login, session["att_id"], emp_id, name, band, now_local())
    online_set(session["att_id"], emp_id, name)

def track_logout(auto=False, reason=""):
    """Save the logout time for whoever is currently logged in (Admin or Employee); no-op otherwise.
    Pass auto=True with a short reason (e.g. "Inactivity") when the system - not the person - ended
    the session, so it's recorded distinctly from a manual logout."""
    if session.get("att_id"):
        logout_type = f"Auto ({reason})" if auto else "Manual"
        _bg(_log_logout, session["att_id"], session.get("att_eid", "ADMIN"),
            session.get("att_name", "Admin"), session.get("att_band", "-"), now_local(), logout_type)
        online_drop(session.get("att_id"))
        session.pop("att_id", None)

# ---------------------------------------------------------------- online employees (Update71)
ONLINE_TTL = 90     # seconds without a heartbeat before an employee counts as offline (tab closed / connection lost)
AWAY_AFTER = 300    # seconds with no clicks / page loads before the status reads "Away" instead of "Online"
_online, _online_lock = {}, threading.Lock()   # per server process; run one worker (threads are fine) so every request sees the same list

def online_set(att_id, emp_id, name, active=None):
    if not att_id or not emp_id or str(emp_id).upper() == "ADMIN": return
    now = time.time()
    with _online_lock:
        cur = _online.get(att_id) or {"since": now}
        cur.update(eid=str(emp_id), name=str(name or ""), seen=now, active=active or now)
        _online[att_id] = cur

def online_drop(att_id):
    with _online_lock: _online.pop(att_id, None)

def online_list():
    now = time.time()
    with _online_lock:
        for k in [k for k, v in _online.items() if now - v["seen"] > ONLINE_TTL]: del _online[k]
        best = {}
        for v in _online.values():                       # same employee in two browsers -> one row
            b = best.get(v["eid"])
            if not b or v["active"] > b["active"]: best[v["eid"]] = dict(v, since=min(v["since"], b["since"]) if b else v["since"])
        out = [dict(id=v["eid"], name=v["name"], status="Away" if now - v["active"] > AWAY_AFTER else "Online",
                    since=dt.datetime.fromtimestamp(v["since"], TZ).strftime("%I:%M %p")) for v in best.values()]
    return sorted(out, key=lambda r: r["name"].lower())

# ---------------------------------------------------------------- auth helpers
def need(role=None):
    def deco(f):
        @wraps(f)
        def w(*a, **k):
            r = session.get("role")
            if not r:
                return redirect(LOGIN_URL.get(role, "/employee/login"))
            if role and r != role:                      # signed in, but with the wrong role
                return _wrong_area(role)
            if r == "employee":                         # Update96: a locked or deleted account is signed out straight away
                try: st = emp_status(session.get("emp_id"))
                except Exception: st = "ok"
                if st != "ok":
                    session.clear()
                    flash("Your account is locked. Please contact the Admin." if st == "locked" else "Your account is no longer available. Please contact the Admin.", "error")
                    return redirect("/employee/login")
            return f(*a, **k)
        return w
    return deco

def home():
    return "/admin/log" if session.get("role") == "admin" else "/employee"

def next_url():
    """Update91: where View / Edit / Delete return to. Only an employee's own Productivity Info month page is accepted (no open redirect)."""
    n = (request.values.get("next") or "").strip()
    ok = (((session.get("role") == "employee" and n.startswith("/employee/productivity"))
           or (session.get("role") == "admin" and (n == "/admin/log" or n.startswith("/admin/log?"))))      # Update103: Admin returns to the Productivity Log
          and "//" not in n and "\\" not in n and "\n" not in n and "\r" not in n)
    return n if ok else ""


# ---------------------------------------------------------------- Update96: account lock / unlock / password reset / delete (Admin only)
def emp_locked(e): return str(e.get("Account locked", "")).strip().lower() in ("yes", "y", "true", "locked", "1")

def emp_status(emp_id):
    """'ok' | 'locked' | 'deleted' for a signed-in employee (uses the short-lived sheet cache, so it costs no extra Google call)."""
    k = _key(emp_id)
    for e in rows("Employees"):
        if _key(e["Employee ID"]) == k: return "locked" if emp_locked(e) else "ok"
    return "deleted"

def set_employee_cell(row, emp_id, col, value):
    """Write ONE cell of an Employees row (after re-checking the row still belongs to emp_id). Returns the previous value or None."""
    heads = HEADERS["Employees"]; ws = ws_of("Employees")
    cur = ws.row_values(row); cur += [""] * (len(heads) - len(cur))
    if _key(cur[heads.index("Employee ID")]) != _key(emp_id):
        invalidate_cache("Employees"); return None
    old = cur[heads.index(col)]
    _with_retry(ws.update, range_name=gspread.utils.rowcol_to_a1(row, heads.index(col) + 1), values=[[value]], value_input_option="RAW")
    invalidate_cache("Employees")
    return old or ""

def join_date(emp_id):
    """Update97: the employee's joining date set by Admin (a date), or None when none is set (no restriction)."""
    k = _key(emp_id)
    for e in rows("Employees"):
        if _key(e["Employee ID"]) == k:
            try: return dt.date.fromisoformat(str(e.get("Joining date", "")).strip())
            except ValueError: return None
    return None

def temp_password():
    return "".join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789") for _ in range(8))

# ---------------------------------------------------------------- templates
BASE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#1c2340;--mut:#6b7390;--pri:#4f46e5;--line:#e6e9f2}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:#f3f5fb;color:var(--ink);}
@keyframes pageFade{from{opacity:0}to{opacity:1}}
.app{display:flex;min-height:100vh}
aside{width:220px;background:#1c2340;color:#fff;padding:20px 12px;display:flex;flex-direction:column;gap:4px;flex:none}
.brand{font-weight:600;font-size:17px;padding:0 10px 16px}.brand small{display:block;font-weight:400;color:#9aa3c7;font-size:12px}
aside a{color:#c9d0ee;text-decoration:none;padding:9px 12px;border-radius:8px;font-size:14px;transition:background .2s ease,color .2s ease,transform .15s ease}
aside a:hover{background:#2b3560;transform:translateX(2px)}aside a.on{background:var(--pri);color:#fff}
.me{margin-bottom:14px;padding:0 10px 14px;border-bottom:1px solid #2b3560;font-size:13px;color:#9aa3c7;display:flex;justify-content:space-between;align-items:center;gap:8px}
.me a{padding:5px 12px;color:#fff;background:#2b3560;border-radius:7px;font-size:13px;transition:background .2s ease,transform .15s ease}
.me a:hover{background:#e5484d;transform:translateY(-1px)}
main{flex:1;display:flex;flex-direction:column;padding:24px 28px;min-width:0;animation:fadeInUp .45s cubic-bezier(.22,1,.36,1)}
.mbody{flex:1 0 auto;min-width:0}
/* Update95: colourful copyright footer (same on Admin and Employee pages) */
.site-ftr{flex:none;margin:22px auto 0;padding:6px 12px;text-align:center;font-weight:700;font-size:11.5px;color:var(--mut);background:none;border:0}
.site-ftr span{color:var(--mut)}
/* Update113: subtle page-bottom credit (Admin -> Employees page) */
.pg-ftr{flex:none;margin:26px auto 0;padding:8px 12px;text-align:center;font-size:11px;font-weight:400;letter-spacing:.2px;color:var(--mut);opacity:.75;background:none;border:0}
.center{max-width:420px;margin:12vh auto;padding:0 16px}
/* Update126: profile picture above the employee name (sidebar), same for every employee */
.prof-pic{display:block;width:96px;height:auto;margin:0 auto;user-select:none;-webkit-user-drag:none;filter:drop-shadow(0 8px 12px #0006)}
.prof-emp .prof-row{flex-direction:column;align-items:center;text-align:center;gap:10px}
.prof-emp .prof-info{text-align:center}
@media(max-width:800px){.prof-emp .prof-row{flex-direction:row;text-align:left}.prof-pic{width:44px;margin:0}}
/* Update123: global footer - same text and bottom-centre position on every page */
.site-foot{flex:none;margin:auto auto 0;padding:14px 12px calc(10px + env(safe-area-inset-bottom,0px));width:100%;text-align:center;font:400 11px/1.4 Poppins,system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.3px;color:var(--mut);opacity:.8;overflow-wrap:anywhere;pointer-events:none;user-select:none}
.lg{padding-bottom:44px}
.lg .site-foot,.wl .site-foot{position:absolute;left:0;right:0;bottom:0;margin:0;padding:10px 12px calc(10px + env(safe-area-inset-bottom,0px));width:auto}
.lg .site-foot{color:#6b4a43;opacity:.85}
.wl .site-foot{z-index:10001;color:#fff;opacity:.8;text-shadow:0 1px 2px #0008}
@media(max-width:800px){.site-foot{font-size:10.5px;padding-top:12px}}
@media print{.site-foot{display:none}}
h1{font-size:22px;margin:0}h2{font-size:17px;margin:22px 0 10px}h3{font-size:15px;margin:14px 0 6px}
.head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.mut{color:var(--mut);margin:2px 0 0;font-size:13px}
.card{background:#fff;padding:18px;border-radius:14px;border:1px solid var(--line);margin-bottom:16px;transition:box-shadow .2s ease,transform .2s ease;animation:fadeInUp .4s cubic-bezier(.22,1,.36,1) backwards}
.card:hover{box-shadow:0 8px 22px #1c234014;transform:translateY(-1px)}
input,select,button{padding:8px 10px;border:1px solid #cfd5e6;border-radius:8px;font-size:14px;margin:3px;background:#fff;color:var(--ink);transition:border-color .2s ease,box-shadow .2s ease}
input:focus,select:focus{outline:2px solid #c7c4fb;border-color:var(--pri)}
input[readonly]{background:#f1f3fa}
button,.primary,.btnl{cursor:pointer;transition:transform .18s cubic-bezier(.34,1.56,.64,1),box-shadow .2s ease,background .2s ease,color .2s ease,border-color .2s ease;position:relative}
button:hover,.primary:hover,.btnl:hover{transform:translateY(-2px);box-shadow:0 6px 16px #1c234026}
button:active,.primary:active,.btnl:active{transform:translateY(0) scale(.95);box-shadow:0 2px 6px #1c234022;transition-duration:.08s}
button:focus-visible,.primary:focus-visible,.btnl:focus-visible{outline:2px solid var(--pri);outline-offset:2px}
.primary,.btnl{background:var(--pri);color:#fff;border:0;padding:9px 18px;border-radius:8px;text-decoration:none;font-size:14px;display:inline-block}
.primary:hover,.btnl:hover{background:#4338ca}
.danger{color:#c62828;border-color:#f3c1c1}
.danger:hover{background:#fdeaea;border-color:#e5484d;box-shadow:0 6px 16px #e5484d26}
/* ---- subtle post-login animation for labels, buttons and log/table sections ---- */
/* perf: per-element entrance animations on every heading/label/table row removed - the page itself still fades in */
@keyframes rowIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
aside a{animation:navIn .35s ease backwards}
aside a:nth-child(1){animation-delay:.03s}aside a:nth-child(2){animation-delay:.06s}
aside a:nth-child(3){animation-delay:.09s}aside a:nth-child(4){animation-delay:.12s}
aside a:nth-child(5){animation-delay:.15s}aside a:nth-child(6){animation-delay:.18s}
aside a:nth-child(7){animation-delay:.21s}aside a:nth-child(8){animation-delay:.24s}
@keyframes navIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}
.pill{transition:transform .18s ease,box-shadow .2s ease}.pill:hover{transform:translateY(-1px)}
tbody tr:nth-child(even){background:#f9fafd}tbody tr:hover{background:#eef0ff!important}
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
.grid,.r{display:flex;flex-wrap:wrap;gap:6px;align-items:end}.grid label{display:flex;flex-direction:column;font-size:12px;color:var(--mut)}
table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:7px 10px;border-bottom:1px solid var(--line);text-align:left;font-size:12.5px;line-height:1.35}
th{background:#f7f8fc;color:var(--mut);font-weight:500;font-size:13px}tr:last-child td{border-bottom:0}
tbody tr{transition:background .15s ease}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:18px}
.kpi{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 16px;transition:box-shadow .2s ease,transform .2s ease}
.kpi:hover{box-shadow:0 8px 22px #1c234014;transform:translateY(-1px)}
.kpi span{font-size:13px;color:var(--mut)}.kpi b{display:block;font-size:26px;margin:4px 0 8px}
.bar{display:block;height:6px;background:#eceffa;border-radius:3px;overflow:hidden;min-width:70px;margin-top:4px}
.bar u{display:block;height:100%;background:#22a06b;transition:width .5s ease}.bar.a u{background:#e8a317}.bar.r u{background:#e5484d}
.flash{background:#eef0ff;border:1px solid #d6d9ff;padding:10px 14px;border-radius:10px;animation:fadeInUp .35s ease}
.flash.err{background:#fef2f2;border:1px solid #fca5a5;color:#991b1b;font-weight:600}
.flash.err::before{content:"\\26A0  "}
.warn{background:#fff4e5;border:1px solid #ffd59a;color:#7a4b00;padding:12px 16px;border-radius:10px;margin-bottom:16px;font-size:14px;animation:fadeInUp .35s ease}
.warn div{margin-top:4px}
.totals{background:#eef0ff;padding:10px 14px;border-radius:10px;margin:12px 0}
.act{display:flex;gap:8px;align-items:center}.act form{margin:0}.act a{color:var(--pri);text-decoration:none;transition:color .2s ease}.act a:hover{color:#4338ca}
@keyframes fadeInUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@media print{aside,.me,.flash,.warn,form,.btnl,.no-print{display:none!important}main{padding:0;animation:none}body{background:#fff}
.card{border:0;padding:0}table{border:1px solid #000}th,td{border-color:#000}.kpi{border:1px solid #000}}
@media(max-width:800px){.app{flex-direction:column}aside{width:auto;flex-direction:row;flex-wrap:wrap;align-items:center}.me{order:99;margin:0 0 0 auto;border:0;padding:0}main{padding:16px}}
.lg{position:relative;overflow:hidden;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;background:linear-gradient(135deg,#c9b8f6 0%,#fbd3e2 45%,#b9d2f8 100%);animation:fadeInUp .5s cubic-bezier(.22,1,.36,1)}
.blob{position:absolute;border-radius:50%;filter:blur(2px);opacity:.55;pointer-events:none;will-change:transform;z-index:0}
.blob.b1{width:340px;height:340px;left:-90px;top:-70px;background:radial-gradient(circle at 35% 35%,#fff9,#8b6fe8 70%);animation:blobFloat1 13s ease-in-out infinite}
.blob.b2{width:260px;height:260px;right:-70px;bottom:-60px;background:radial-gradient(circle at 35% 35%,#fff9,#f2789a 70%);animation:blobFloat2 16s ease-in-out infinite}
.blob.b3{width:150px;height:150px;right:12%;top:8%;background:radial-gradient(circle at 35% 35%,#fffb,#7fb7f2 70%);animation:blobFloat3 10s ease-in-out infinite}
@keyframes blobFloat1{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(30px,25px) scale(1.08)}}
@keyframes blobFloat2{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-25px,-20px) scale(1.1)}}
@keyframes blobFloat3{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-18px,16px) scale(.92)}}
.win{position:relative;z-index:1;width:min(880px,100%);box-shadow:0 20px 50px #5b3f9a33;border-radius:14px;animation:fadeInUp .6s .1s cubic-bezier(.22,1,.36,1) backwards}
.wbar{background:#f6a5a5;height:28px;border-radius:14px 14px 0 0;display:flex;align-items:center;gap:6px;padding:0 12px}
.wbar i{width:9px;height:9px;border-radius:50%;background:#fff}
.wbody{min-height:440px;border-radius:0 0 14px 14px;display:flex;align-items:center;justify-content:center;padding:32px;background:url(/static/login_bg.jpg) center/cover,linear-gradient(115deg,#4a2a7a 0%,#b4487c 40%,#f29a63 62%,#8b45a8 100%)}
.lcard{background:#fff;border-radius:12px;padding:26px 28px;width:340px;max-width:100%;text-align:center;box-shadow:0 10px 30px #0003}
.lcard img{width:112px;border-radius:22px}
.lav{display:flex;justify-content:center;margin:0 0 8px}
.lav .av3d{width:124px;height:124px;margin:0 0 8px}
.lcard h2{font-family:Georgia,serif;color:#5b4fb0;font-size:27px;margin:8px 0 2px}
.lcard p{margin:0 0 14px;color:var(--mut);font-size:13px}
.lcard input{width:100%;margin:4px 0;border:1px solid #f08c8c;border-radius:8px;padding:10px;transition:box-shadow .15s ease,border-color .15s ease}
.lcard .field{position:relative}
.lcard input.key-pulse{border-color:#c9448a;box-shadow:0 0 0 4px #f58a8a3a}
.lcard button{width:100%;background:#f58a8a;color:#fff;border:0;border-radius:20px;padding:11px;margin:12px 0 0;font-size:15px}
.fly-letter{position:absolute;top:10px;right:14px;font-weight:700;font-size:15px;color:#c9448a;pointer-events:none;z-index:2;animation:flyLetter .8s ease-out forwards}
@keyframes flyLetter{0%{opacity:0;transform:translate(0,0) scale(.5) rotate(-10deg)}18%{opacity:1;transform:translate(2px,-4px) scale(1.25) rotate(6deg)}100%{opacity:0;transform:translate(14px,-38px) scale(.85) rotate(-8deg)}}
.orb{object-fit:cover;position:absolute;left:-50px;bottom:-50px;width:230px;height:230px;border-radius:50%;border:6px solid #fff;background:#fff center/cover no-repeat;box-shadow:0 10px 30px #0003;will-change:transform;animation:orbFloat 4.5s ease-in-out infinite}
@keyframes orbFloat{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-14px) rotate(-3deg)}}
@media(max-width:800px){.orb{display:none}.wbody{padding:20px 10px}}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 18px}
.tabs a{padding:8px 14px;border-radius:8px;background:#fff;border:1px solid var(--line);color:var(--ink);text-decoration:none;font-size:14px;transition:background .2s ease}
.tabs a:hover{background:#eef0ff}.tabs a.on{background:var(--pri);color:#fff;border-color:var(--pri)}
.pill{display:inline-block;padding:2px 10px;border-radius:12px;font-size:12px;background:#eceffa;color:var(--mut)}
.pill.in{background:#e3f6ec;color:#146c43}.pill.out{background:#fdeaea;color:#a52a2a}.pill.act{background:#fff4e5;color:#7a4b00}
.emp-flag{color:#c62828;font-weight:700}
#toasts{position:fixed;top:16px;right:16px;z-index:99;display:flex;flex-direction:column;gap:8px;max-width:340px}
.toast{background:#1c2340;color:#fff;padding:12px 16px;border-radius:10px;font-size:14px;box-shadow:0 8px 24px #0004;animation:fadeInUp .3s ease}
@media print{ #toasts{display:none}}

/* ================= Print / export controls ================= */
.pbtn{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:38px;padding:0 18px;margin:3px;line-height:1;font-size:14px;font-weight:500;white-space:nowrap;border-radius:8px}
.ov-head{align-items:flex-start}
.ov-tools{display:flex;flex-direction:column;align-items:flex-end;gap:6px;margin-left:auto}
.ov-tools .grid{align-items:center;justify-content:flex-end}
/* Overview: compact, animated Print / Show buttons */
.ov-tools .pbtn{height:30px;padding:0 13px;font-size:13px;gap:5px;margin:2px;border-radius:7px;overflow:hidden;box-shadow:0 3px 0 #3730a3,0 6px 10px -4px #4f46e566,inset 0 1px 0 #ffffff45;animation:btnPop .45s cubic-bezier(.34,1.56,.64,1) backwards}
.ov-tools .grid .pbtn{animation-delay:.08s}
.ov-tools .grid input[type=month]{height:30px;padding:0 8px;font-size:13px;margin:2px}
.ov-tools .grid a{font-size:13px}
.ov-tools .pbtn::after{content:"";position:absolute;top:0;left:0;width:45%;height:100%;background:linear-gradient(100deg,transparent,#ffffff66,transparent);transform:translate3d(-130%,0,0) skewX(-20deg);pointer-events:none}
.ov-tools .pbtn:hover::after{transform:translate3d(330%,0,0) skewX(-20deg);transition:transform .7s ease}
.ov-tools .pbtn:hover{transform:translateY(-2px);box-shadow:0 5px 0 #3730a3,0 10px 14px -6px #4f46e577,inset 0 1px 0 #ffffff45}
.ov-tools .pbtn:active{transform:translateY(2px) scale(.96);box-shadow:0 1px 0 #3730a3,inset 0 1px 0 #ffffff30}
.ov-tools .pbtn span[aria-hidden]{display:inline-block;transform-origin:50% 80%}
.ov-tools .pbtn:hover span[aria-hidden]{animation:printWiggle .55s ease-in-out}
@keyframes btnPop{from{opacity:0;transform:translate3d(0,-8px,0) scale(.85)}to{opacity:1;transform:translate3d(0,0,0) scale(1)}}
@keyframes printWiggle{0%,100%{transform:rotate(0)}25%{transform:rotate(-14deg) translateY(-1px)}60%{transform:rotate(10deg)}}
@media(prefers-reduced-motion:reduce){.ov-tools .pbtn::after{display:none}.ov-tools .pbtn span[aria-hidden]{animation:none!important}}
.exp{position:relative;display:inline-block}
.exp summary{list-style:none;cursor:pointer;user-select:none}
.exp summary::-webkit-details-marker{display:none}
.exp .menu{position:absolute;right:0;top:calc(100% + 6px);z-index:20;min-width:280px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px;box-shadow:0 18px 36px -10px #1c234055,0 4px 10px #1c23401a;animation:fadeInUp .18s ease}
.exp .menu a{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14px;transition:background .15s ease}
.exp .menu a:hover{background:#eef0ff}
.exp .menu hr{border:0;border-top:1px solid var(--line);margin:4px 6px}
.exp .menu small{display:block;color:var(--mut);font-size:12px}
.loghead{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.loghead h2{margin:0}
.rep-title{margin:0 0 4px}.rep-meta{color:var(--mut);font-size:13px;margin:0 0 14px}
.rep-tools{display:flex;gap:8px;align-items:center;margin-bottom:14px}
@media print{.exp,.rep-tools,.ov-tools{display:none!important}.rep-title{font-size:20px}table{font-size:11px}thead{display:table-header-group}tr{page-break-inside:avoid}}
/* ================= Productivity-pending marquee ================= */
.mq{position:sticky;top:8px;z-index:6;overflow:hidden;border-radius:12px;margin-bottom:16px;background:linear-gradient(180deg,#fff8ec,#ffecc9);border:1px solid #f4c977;color:#7a4b00;font-weight:600;box-shadow:0 1px 0 #fff inset,0 3px 0 #f0c37a88,0 12px 22px -8px #b7791f44;contain:content}
.mq-track{display:flex;width:max-content;animation:mqScroll 44s linear infinite;will-change:transform;backface-visibility:hidden}
.mq:hover .mq-track{animation-play-state:paused}
.mq-group{display:flex;flex:none;min-width:100vw;justify-content:space-around}
.mq-item{display:inline-flex;align-items:center;padding:12px 64px 12px 0;white-space:nowrap;font-size:14px}
@keyframes mqScroll{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
@media(prefers-reduced-motion:reduce){.mq-track{animation:none!important;width:auto;flex-wrap:wrap}.mq-group[aria-hidden]{display:none}.mq-group{min-width:0}.mq-item{white-space:normal}}
/* ================= Animated welcome line ================= */
.hero{display:block}
.welcome{padding:16px 22px;border-radius:16px;background:linear-gradient(135deg,#fff 0%,#eef0ff 100%);border:1px solid #e2e6f3;box-shadow:0 1px 0 #fff inset,0 4px 0 #dfe3f7,0 18px 30px -14px #4f46e544}
.wt{font-size:26px;letter-spacing:-.2px;animation:none}
.wt-hi{display:inline-block;animation:segIn .6s cubic-bezier(.22,1,.36,1) both}
.wt-name{display:inline-block;background:linear-gradient(90deg,#4f46e5,#c026d3,#0ea5e9,#4f46e5);background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;animation:segIn .7s .12s cubic-bezier(.22,1,.36,1) both,shimmer 3s linear 1}
.wsub{margin-top:6px;font-size:14px}
.wsub .seg{display:inline-block;background:linear-gradient(100deg,#5b6384 35%,#4f46e5 50%,#5b6384 65%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;animation:segIn .6s cubic-bezier(.22,1,.36,1) both,sweep 3s ease-in-out 1}
.wsub .dot{display:inline-block;margin:0 8px;color:#a3aac6;animation:segIn .6s ease both}
.wsub .seg:nth-of-type(1){animation-delay:.25s,.9s}.wsub .seg:nth-of-type(2){animation-delay:.4s,1.1s}
.wsub .seg:nth-of-type(3){animation-delay:.55s,1.3s}.wsub .seg:nth-of-type(4){animation-delay:.7s,1.5s}
@keyframes segIn{from{opacity:0;transform:translate3d(0,12px,0)}to{opacity:1;transform:translate3d(0,0,0)}}
@keyframes shimmer{from{background-position:0 0}to{background-position:-200% 0}}
@keyframes sweep{0%,55%{background-position:120% 0}100%{background-position:-120% 0}}
@media(prefers-reduced-motion:reduce){.wt-name,.wsub .seg{animation:none!important;opacity:1}}
/* ================= 3D profile avatar (CSS 3D layers: light on CPU, transform-only animation) ================= */
.wflex{display:flex;align-items:center;gap:18px}.wtxt{min-width:0}
.av3d{position:relative;flex:none;width:96px;height:96px;perspective:520px;margin-bottom:6px}
.av3d::after{content:"";position:absolute;left:14%;right:14%;bottom:-8px;height:10px;border-radius:50%;background:radial-gradient(#1c234055,transparent 70%)}
.av-stage{position:relative;width:100%;height:100%;transform-style:preserve-3d;animation:avSway 7s ease-in-out 1}
.av3d.live .av-stage{animation:none;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .14s linear}
.av-l{position:absolute;inset:0;width:100%;height:100%;transform:translateZ(var(--z,0px));pointer-events:none}
.av-l:first-child{border-radius:50%;box-shadow:0 12px 22px -8px #4f46e577,0 0 0 3px #fff}
@keyframes avSway{0%,100%{transform:rotateX(2deg) rotateY(-11deg) translateY(0)}50%{transform:rotateX(-2deg) rotateY(11deg) translateY(-3px)}}
/* Update127: sidebar 3D avatar - smooth endless float (transform only, GPU-friendly); pointer tilt (.live) still takes over */
aside .prof .av3d{width:96px;height:96px;margin:0 0 6px}
.prof .av3d .av-stage{animation:avFloat 6s ease-in-out infinite;will-change:transform}
.prof .av3d.live .av-stage{animation:none}
@keyframes avFloat{0%,100%{transform:rotateX(2deg) rotateY(-14deg) translateY(0)}50%{transform:rotateX(-2deg) rotateY(14deg) translateY(-4px)}}
@media(max-width:800px){aside .prof .av3d{width:44px;height:44px;margin:0}}
@media(prefers-reduced-motion:reduce){.prof .av3d .av-stage{animation:none!important}}
/* employee profile block in the left panel */
aside.emp{position:sticky;top:0;height:100vh;overflow-y:auto;align-self:flex-start}
.prof{margin-top:auto;padding:14px 4px 6px;border-top:1px solid #2b3560;display:flex;flex-direction:column;gap:10px}
.prof-row{display:flex;align-items:center;gap:12px}
.prof-info{min-width:0;text-align:left}
.prof .av3d{width:84px;height:84px;margin:0 0 6px}
.prof-name{font-size:14.5px;font-weight:600;color:#fff;letter-spacing:.2px;text-shadow:0 2px 6px #0006;word-break:break-word;line-height:1.25}
.prof-sub{font-size:12px;color:#9aa3c7;line-height:1.4;margin-top:2px;word-break:break-word}
.prof-out{display:block;text-align:center;padding:6px 18px;color:#fff;background:#2b3560;border-radius:7px;font-size:13px;transition:background .2s ease,transform .15s ease}
.prof-out:hover{background:#e5484d;transform:translateY(-1px)}@media print{.prof{display:none!important}}
@media(max-width:800px){.av3d{width:72px;height:72px}.wflex{gap:12px}
aside.emp{position:static;height:auto;overflow:visible;align-self:auto}.prof-sub{display:none}.prof-row{gap:8px}.prof{order:99;margin:0 0 0 auto;border:0;padding:0;flex-direction:row;gap:10px}.prof .av3d{width:44px;height:44px;margin:0}.prof-name{font-size:13px}}
@media(prefers-reduced-motion:reduce){.av-stage{animation:none!important}}
/* Admin sidebar: flat, non-3D, non-animated avatar (kept the same size/spot as the old 3D one) */
.av-flat{position:relative;flex:none;width:96px;height:96px;border-radius:50%;display:flex;align-items:center;justify-content:center;
 background:radial-gradient(circle at 35% 28%,#dbeafe,#93c5fd 55%,#4f46e5);box-shadow:0 12px 22px -8px #4f46e577,0 0 0 3px #fff;margin-bottom:6px}
.av-flat span{font-family:system-ui,-apple-system,Segoe UI,sans-serif;font-size:34px;font-weight:700;color:#fff}
.prof .av-flat{width:84px;height:84px}
@media(max-width:800px){.prof .av-flat{width:44px;height:44px}.prof .av-flat span{font-size:18px}}
/* ================= Professional 3D look (Admin, Employee, Login) ================= */
body{background:radial-gradient(1100px 520px at 8% -8%,#e7eaff 0%,transparent 60%),radial-gradient(900px 480px at 100% 0%,#f4e9ff 0%,transparent 55%),#f3f5fb}
aside{background:linear-gradient(180deg,#252f5c 0%,#1c2340 55%,#151b34 100%);box-shadow:10px 0 28px -8px #1c234055,inset -1px 0 0 #ffffff14;position:relative;z-index:2}
.brand{text-shadow:0 2px 6px #0006}
aside a.on{background:linear-gradient(180deg,#6d70f5,#4f46e5);box-shadow:0 3px 0 #3730a3,0 10px 16px -4px #4f46e577,inset 0 1px 0 #ffffff45;transform:translateY(-1px)}
.card{border-color:#e2e6f3;box-shadow:0 1px 0 #fff inset,0 2px 4px #1c23400d,0 14px 28px -12px #1c234030}
.card:hover{transform:translateY(-3px);box-shadow:0 1px 0 #fff inset,0 4px 8px #1c234012,0 24px 40px -14px #1c234040}
.kpis{perspective:900px}
.kpi{background:linear-gradient(160deg,#fff 0%,#f4f5ff 100%);border-color:#e2e6f3;box-shadow:0 1px 0 #fff inset,0 3px 0 #e3e6f6,0 16px 26px -12px #1c234040;transition:transform .25s ease,box-shadow .25s ease}
.kpi:hover{transform:rotateX(5deg) rotateY(-6deg) translateY(-4px);box-shadow:0 1px 0 #fff inset,0 5px 0 #d9ddf3,0 26px 36px -14px #1c234055}
table{box-shadow:0 1px 0 #fff inset,0 14px 28px -14px #1c234040}
.primary,.btnl{background:linear-gradient(180deg,#6d70f5,#4f46e5);box-shadow:0 4px 0 #3730a3,0 10px 16px -6px #4f46e566,inset 0 1px 0 #ffffff45}
.primary:hover,.btnl:hover{background:linear-gradient(180deg,#7a7df8,#5249ea);transform:translateY(-2px);box-shadow:0 6px 0 #3730a3,0 16px 22px -8px #4f46e577,inset 0 1px 0 #ffffff45}
.primary:active,.btnl:active{transform:translateY(3px) scale(.99);box-shadow:0 1px 0 #3730a3,0 3px 6px #4f46e544,inset 0 1px 0 #ffffff30}
.warn,.flash{box-shadow:0 1px 0 #fff inset,0 10px 18px -10px #1c234033}
/* login page */
.lg{perspective:1400px}
.win{transform-style:preserve-3d;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .2s ease-out;will-change:transform;box-shadow:0 34px 60px -16px #3b1f7a66,0 18px 34px -18px #0007}
.wbody{transform-style:preserve-3d}
.wbar{transform:translateZ(12px);box-shadow:0 4px 10px #0002}
.lcard{transform:translateZ(46px);box-shadow:0 1px 0 #fff inset,0 30px 46px -14px #0006,0 8px 14px -6px #0003}
.lcard button{box-shadow:0 4px 0 #d46a6a,0 10px 16px -6px #d46a6a88,inset 0 1px 0 #ffffff55}
.lcard button:active{box-shadow:0 1px 0 #d46a6a}
.blob{box-shadow:inset -20px -24px 42px #0000002e,inset 14px 14px 30px #ffffff66,0 34px 44px -24px #0000004a}
@media(max-width:800px){.win{transform:none!important}.lcard{transform:none}}
@media(prefers-reduced-motion:reduce){.win{transform:none!important}.kpi:hover{transform:none}}
/* ---- compact, consistent text size for all Employee & Admin logs/tables ---- */
table th,table td{font-size:12px!important;line-height:1.3!important;padding:5px 8px!important;font-weight:400}
table th{font-weight:600!important;color:var(--mut)}
table td b,table td a,table td .pill,table td small,table th small{font-size:inherit!important}
table .pill{padding:1px 8px!important;font-size:11px!important}
table td small,table th small{font-size:10.5px!important}
/* ================= Login pages: HD 3D scene + show-password ================= */
.wbody{position:relative}
.win.admin .wbody{background:radial-gradient(900px 420px at 20% 0%,#3b5bdb55,transparent 60%),linear-gradient(120deg,#0b1230 0%,#182a6b 48%,#4f46e5 100%)}
.win.employee .wbody{background:radial-gradient(900px 420px at 80% 0%,#ffb37066,transparent 60%),linear-gradient(120deg,#3b1f6e 0%,#a3407f 48%,#f29a63 100%)}
.lcard{position:relative;z-index:2}
.scene{position:absolute;inset:0;overflow:hidden;border-radius:0 0 14px 14px;pointer-events:none;contain:layout paint;z-index:0}
.scene.admin{--c1:#7c9cffcc;--c2:#4f46e544;--g:#8ea8ff;--r:#a5b4fc}
.scene.employee{--c1:#ffc98acc;--c2:#f0609a44;--g:#ffd0a1;--r:#ffe1c2}
.gfw{position:absolute;left:0;right:0;bottom:0;height:60%;perspective:520px;overflow:hidden}
.gf{position:absolute;left:-60%;right:-60%;bottom:0;height:220%;transform-origin:50% 100%;transform:rotateX(72deg);overflow:hidden}
.gf::before{content:"";position:absolute;left:0;right:0;top:-64px;bottom:0;background-image:linear-gradient(var(--g) 1.5px,transparent 1.5px),linear-gradient(90deg,var(--g) 1.5px,transparent 1.5px);background-size:64px 64px;opacity:.45;animation:gridMove 2.4s linear infinite;will-change:transform}
@keyframes gridMove{to{transform:translate3d(0,64px,0)}}
.gfw::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#0000 0%,#0000 35%,#00000055 100%)}
.gfw::before{content:"";position:absolute;left:0;right:0;top:0;height:45%;z-index:1;background:linear-gradient(180deg,var(--vt,#0b1230) 0%,transparent 100%);opacity:.55}
.fl{position:absolute;perspective:700px;animation:bob var(--bt,7s) ease-in-out infinite;animation-delay:var(--d,0s);will-change:transform}
@keyframes bob{0%,100%{transform:translate3d(0,0,0)}50%{transform:translate3d(0,-16px,0)}}
.cube{position:relative;width:var(--s);height:var(--s);transform-style:preserve-3d;animation:cubeSpin var(--t,16s) linear infinite;will-change:transform}
.cube i{position:absolute;inset:0;border:1px solid #ffffffa0;background:linear-gradient(135deg,var(--c1),var(--c2));box-shadow:inset 0 0 20px #ffffff66,0 0 18px #ffffff22}
.cube i:nth-child(1){transform:translateZ(calc(var(--s) / 2))}
.cube i:nth-child(2){transform:rotateY(90deg) translateZ(calc(var(--s) / 2))}
.cube i:nth-child(3){transform:rotateY(180deg) translateZ(calc(var(--s) / 2))}
.cube i:nth-child(4){transform:rotateY(-90deg) translateZ(calc(var(--s) / 2))}
.cube i:nth-child(5){transform:rotateX(90deg) translateZ(calc(var(--s) / 2))}
.cube i:nth-child(6){transform:rotateX(-90deg) translateZ(calc(var(--s) / 2))}
@keyframes cubeSpin{from{transform:rotateX(-20deg) rotateY(0deg)}to{transform:rotateX(340deg) rotateY(360deg)}}
.ring3d{width:var(--s);height:var(--s);border-radius:50%;border:5px solid var(--r);box-shadow:0 0 22px var(--r),inset 0 0 18px #ffffff66;animation:ringSpin3 var(--t,10s) linear infinite;will-change:transform}
@keyframes ringSpin3{from{transform:rotateX(65deg) rotateY(0deg)}to{transform:rotateX(65deg) rotateY(360deg)}}
.sph{width:var(--s);height:var(--s);border-radius:50%;background:radial-gradient(circle at 32% 28%,#fff 0%,var(--g) 38%,var(--c2) 100%);box-shadow:inset -8px -10px 20px #0004,0 14px 28px -8px #0005}
.scene .sheen{position:absolute;inset:0;background:radial-gradient(600px 240px at 50% -10%,#ffffff2e,transparent 70%)}
.lcard{box-shadow:0 1px 0 #fff inset,0 30px 60px -16px #0009,0 0 0 1px #ffffff55,0 0 44px -6px #ffffff55}
.lcard .field.pw input{padding-right:78px}
.lcard .pw-toggle{position:absolute;right:6px;top:50%;transform:translateY(-50%);width:auto;margin:0;padding:5px 8px;border:0;border-radius:8px;background:transparent;color:#6b5fc7;font-size:12px;font-weight:600;display:inline-flex;align-items:center;gap:5px;cursor:pointer;box-shadow:none;transition:background .15s ease,color .15s ease}
.lcard .pw-toggle:hover{background:#f1efff;transform:translateY(-50%);box-shadow:none;color:#4338ca}
.lcard .pw-toggle:active{transform:translateY(-50%) scale(.96);box-shadow:none}
.lcard .pw-toggle:focus-visible{outline:2px solid #6d70f5;outline-offset:1px}
.pw-toggle svg{width:16px;height:16px;flex:none}
.pw-toggle .eye-off{display:none}
.pw-toggle[aria-pressed="true"] .eye{display:none}.pw-toggle[aria-pressed="true"] .eye-off{display:inline}
.lcard .field.pw .fly-letter{right:84px}
@media(max-width:800px){.scene .hm{display:none}}
@media(prefers-reduced-motion:reduce){.scene *,.scene *::before{animation:none!important}}
/* ---- compact text: admin Leave & Permission Log / Mark a Holiday, employee dashboard, tabs, info pages ---- */
.head h1,h1{font-size:19px}
.head .mut,.head p{font-size:12px}
.card>h2,.head h2,h2{font-size:14px;margin:10px 0 6px}
.wt{font-size:20px;line-height:1.25}
.wt .wt-hi{font-size:15px;font-weight:500}
.wt .wt-name{font-size:20px}
.wsub{font-size:11.5px}
.wsub .seg{white-space:nowrap}
.kpis .kpi span{font-size:11px}
.kpis .kpi b{font-size:17px}
.tabs a{font-size:12.5px;padding:6px 12px}
.totals{font-size:12px}
/* Update94: compact Save + Back buttons (all Save forms, Admin and Employee) */
.danger.sm{padding:5px 14px;font-size:13px;line-height:1.3;border-radius:6px;margin:4px 6px 4px 0;width:auto}
.primary.sm,.back.sm{padding:5px 14px;font-size:13px;line-height:1.3;border-radius:6px;margin:4px 6px 4px 0;display:inline-block;width:auto}
.primary.sm{box-shadow:0 2px 0 #3730a3,0 4px 8px -4px #4f46e566}
.back.sm{background:#fff;color:#4338ca;border:1px solid #c7c4fb;box-shadow:none;text-decoration:none}
.back.sm:hover{background:#eef0ff;border-color:#4f46e5;color:#3730a3}
/* ---- Daily Productivity Entry: red/green box vs the Admin-set Target Count/Hour ---- */
#entryCard{transition:background .35s ease,border-color .35s ease,box-shadow .35s ease;border:2px solid var(--line)}
#entryCard.tgt-met{background:#f2fbf5;border-color:#22c55e;box-shadow:0 0 0 3px #22c55e26}
#entryCard.tgt-miss{background:#fdf3f3;border-color:#ef4444;box-shadow:0 0 0 3px #ef444426}
#tgtBadge{display:inline-block;margin-left:8px;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;vertical-align:middle}
#tgtBadge.met{background:#d9f7e3;color:#146c43}
#tgtBadge.miss{background:#fbe0e0;color:#a52a2a}

/* ---- Update67: login data-flow animations (Employee = upload to server, Admin = incoming feed) ---- */
.dp{display:none}
@supports (width:1cqw){
.dp{display:block;position:absolute;inset:0;container-type:inline-size;pointer-events:none;--pk:#ffe2b8;--pk2:#ff9fd0}
.dp.adm{--pk:#a9c1ff;--pk2:#6fe7ff}
.dp-lab{position:absolute;top:12px;left:0;right:0;text-align:center;font:600 10px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.22em;color:#fff;opacity:.78;text-shadow:0 0 10px var(--pk2)}
.dp-lab b{display:inline-block;animation:dpBlink 1.4s steps(2,end) infinite;color:var(--pk2)}
.dp-lane{position:absolute;left:0;right:0;top:var(--y);height:0;--t:5.2s}
.dp-lane::before{content:"";position:absolute;left:11cqw;right:11cqw;top:0;height:1px;background:linear-gradient(90deg,transparent,var(--pk) 30%,var(--pk) 70%,transparent);opacity:.32}
.dp-pk{position:absolute;top:0;left:11cqw;width:15px;height:15px;will-change:transform,opacity;animation:dpGo var(--t) linear infinite;opacity:0}
.dp.adm .dp-pk{left:auto;right:11cqw;animation-name:dpCome}
.dp-pk::before{content:"";position:absolute;top:50%;right:100%;width:78px;height:3px;transform:translateY(-50%);background:linear-gradient(90deg,transparent,var(--pk2))}
.dp.adm .dp-pk::before{right:auto;left:100%;background:linear-gradient(270deg,transparent,var(--pk2))}
.dp-pk::after{content:"";position:absolute;inset:0;border-radius:3px;background:linear-gradient(135deg,#fff,var(--pk) 45%,var(--pk2));box-shadow:0 0 12px var(--pk2),0 0 3px #fff inset;animation:dpSpin 1.9s linear infinite}
.dp-pk:nth-child(2){animation-delay:calc(var(--t) * -.2)}.dp-pk:nth-child(3){animation-delay:calc(var(--t) * -.4)}
.dp-pk:nth-child(4){animation-delay:calc(var(--t) * -.6)}.dp-pk:nth-child(5){animation-delay:calc(var(--t) * -.8)}
.dp-lane:nth-child(3){--t:6.1s}.dp-lane:nth-child(4){--t:4.6s}
.dp-lane:nth-child(3) .dp-pk{width:11px;height:11px}
@keyframes dpGo{0%{transform:translate3d(0,-50%,0) scale(1.25);opacity:0}10%{opacity:1}86%{opacity:1}100%{transform:translate3d(72cqw,-50%,0) scale(.5);opacity:0}}
@keyframes dpCome{0%{transform:translate3d(0,-50%,0) scale(.5);opacity:0}14%{opacity:1}90%{opacity:1}100%{transform:translate3d(-72cqw,-50%,0) scale(1.25);opacity:0}}
@keyframes dpSpin{to{transform:rotate3d(1,1,0,360deg)}}
@keyframes dpBlink{50%{opacity:.25}}
.dp-node{position:absolute;top:50%;margin-top:-34px;width:78px;height:68px;transform-style:preserve-3d}
.dp-node.l{left:3cqw;transform:perspective(420px) rotateY(24deg)}
.dp-node.r{right:3cqw;transform:perspective(420px) rotateY(-24deg)}
.dp-node::after{content:"";position:absolute;inset:-6px;border-radius:14px;border:2px solid var(--pk2);opacity:0;animation:dpPulse 2.6s ease-out infinite}
/* Employee login has a round photo at the bottom-left: keep the EMPLOYEE label above its node so nothing is covered */
.dp.emp .dp-node.l{margin-top:-42px}.dp.emp .dp-node.l small{bottom:auto;top:-20px}
.dp-node small{white-space:nowrap;position:absolute;left:-30px;right:-30px;bottom:-22px;text-align:center;font:600 9px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;color:#fff;opacity:.85}
@keyframes dpPulse{0%{transform:scale(.85);opacity:.7}100%{transform:scale(1.5);opacity:0}}
.dp-scr{position:absolute;inset:0 0 14px;border:2px solid var(--pk);border-radius:8px;background:linear-gradient(140deg,#ffffff40,#ffffff0d);box-shadow:0 0 20px var(--pk2),inset 0 0 14px #ffffff33;overflow:hidden}
.dp-scr i{position:absolute;left:8px;height:4px;border-radius:2px;background:var(--pk);opacity:.85;animation:dpLine 2.4s ease-in-out infinite}
.dp-scr i:nth-child(1){top:10px;width:34px}.dp-scr i:nth-child(2){top:22px;width:50px;animation-delay:-.6s}.dp-scr i:nth-child(3){top:34px;width:26px;animation-delay:-1.2s}
@keyframes dpLine{50%{transform:scaleX(.55);transform-origin:left}}
.dp-stand{position:absolute;left:26px;right:26px;bottom:0;height:8px;border-radius:0 0 6px 6px;background:var(--pk);opacity:.8}
.dp-rack i{position:absolute;left:0;right:0;height:19px;border:2px solid var(--pk);border-radius:6px;background:linear-gradient(140deg,#ffffff40,#ffffff10);box-shadow:0 0 14px var(--pk2)}
.dp-rack i:nth-child(1){top:0}.dp-rack i:nth-child(2){top:24px}.dp-rack i:nth-child(3){top:48px}
.dp-rack i::after{content:"";position:absolute;right:7px;top:50%;width:6px;height:6px;margin-top:-3px;border-radius:50%;background:#7dffb0;box-shadow:0 0 8px #7dffb0;animation:dpLed 1.1s steps(2,end) infinite}
.dp-rack i:nth-child(2)::after{animation-delay:-.4s}.dp-rack i:nth-child(3)::after{animation-delay:-.8s}
@keyframes dpLed{50%{opacity:.25}}
.dp-dash{position:absolute;inset:0 0 14px;border:2px solid var(--pk);border-radius:8px;background:linear-gradient(140deg,#ffffff40,#ffffff0d);box-shadow:0 0 20px var(--pk2),inset 0 0 14px #ffffff33;display:flex;align-items:flex-end;gap:6px;padding:8px 9px}
.dp-dash i{flex:1;border-radius:3px 3px 0 0;background:linear-gradient(180deg,var(--pk),var(--pk2));transform-origin:bottom;animation:dpBar 2.2s ease-in-out infinite}
.dp-dash i:nth-child(1){height:40%}.dp-dash i:nth-child(2){height:75%;animation-delay:-.5s}.dp-dash i:nth-child(3){height:55%;animation-delay:-1s}.dp-dash i:nth-child(4){height:90%;animation-delay:-1.5s}
@keyframes dpBar{50%{transform:scaleY(.6)}}
.scene.dp-paused *,.scene.dp-paused *::before,.scene.dp-paused *::after{animation-play-state:paused!important}
/* the older decorative floats would sit on top of the data-flow nodes: keep only the two top cubes while the flow is shown */
.scene:has(.dp) .fl:nth-child(n+5){display:none}
@media(max-width:800px){.dp-node,.dp-lab{display:none}.dp-pk:nth-child(n+4){display:none}.dp-lane:nth-child(4){display:none}.dp-lane::before{left:0;right:0}.dp-pk{left:0}.dp.adm .dp-pk{right:0}}
@media(prefers-reduced-motion:reduce){.dp{display:none}}
}
#lgm{position:fixed;right:14px;bottom:14px;z-index:60;height:38px;padding:0 14px 0 11px;border-radius:19px;border:1px solid #ffffff66;background:#ffffffd9;color:#1c2340;font:600 12px/1 system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 12px #0003;display:flex;align-items:center;gap:7px;width:auto;margin:0}
#lgm:hover{background:#fff}#lgm[hidden]{display:none}
.tg-badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;white-space:nowrap}
.tg-badge.met{background:#d9f7e3;color:#146c43}.tg-badge.miss{background:#fbe0e0;color:#a52a2a}
/* Update66: expandable sidebar group (Employee Info > Employees / Notifications / Mahizhchi) */
aside .ng>a.ng-h{display:flex;justify-content:space-between;align-items:center;border:1px solid transparent}
aside .ng>a.ng-h .chev{font-size:11px;opacity:.85;transition:transform .2s;transform:rotate(180deg)}
aside .ng.open>a.ng-h{border:1.5px solid #fff;background:transparent;color:#fff;box-shadow:none;transform:none}
aside .ng.open>a.ng-h .chev{transform:rotate(0deg)}
aside .ng .kids{display:none;flex-direction:column;gap:2px;padding:4px 0 4px 14px}
aside .ng.open .kids{display:flex}
aside .ng .kids a{font-size:13px;padding:7px 12px}
aside .ng .kids a.on{background:transparent;color:#fff;font-weight:700;box-shadow:none;transform:none;border-left:3px solid #8ea8ff;border-radius:0 8px 8px 0}
/* Update103: Log group (reuses the Employee Info expandable-group style) */
aside .ng .kids a.on::before{content:"";}
aside .ng .kids a{transition:background .15s,padding-left .15s}
aside .ng .kids a:hover{padding-left:16px}
#bgm{position:fixed;right:14px;bottom:14px;z-index:60;width:38px;height:38px;border-radius:50%;border:1px solid var(--line,#d8dbe6);background:#fff;color:#1c2340;font-size:17px;line-height:1;cursor:pointer;box-shadow:0 2px 10px #0002;opacity:.85;padding:0}
#bgm:hover{opacity:1}
@media print{ #bgm{display:none}}
/* Update83: employee sidebar - animated "Mahizhchi" running-letter badge */
aside a.mzn{position:relative;align-self:flex-start;display:inline-flex;margin:auto 0 14px 4px;padding:6px 16px;border:1.5px solid transparent;border-radius:999px;font-weight:800;font-size:15px;letter-spacing:.3px;white-space:nowrap;color:#4f46e5;
background:linear-gradient(#fff,#fff) padding-box,linear-gradient(120deg,#4f46e5,#ec4899,#f59e0b,#10b981,#3b82f6,#4f46e5) border-box;background-size:100% 100%,300% 100%;
box-shadow:0 0 0 0 rgba(236,72,153,0);animation:mznGlow 2.4s ease-in-out infinite,mznBorder 5s linear infinite}
aside a.mzn:hover{background:linear-gradient(#fff,#fff) padding-box,linear-gradient(120deg,#4f46e5,#ec4899,#f59e0b,#10b981,#3b82f6,#4f46e5) border-box;background-size:100% 100%,300% 100%;transform:translateX(2px) scale(1.04)}
aside a.mzn.on{background:linear-gradient(#fff,#fff) padding-box,linear-gradient(120deg,#4f46e5,#ec4899,#f59e0b,#10b981,#3b82f6,#4f46e5) border-box;background-size:100% 100%,300% 100%;transform:none;box-shadow:0 0 0 3px rgba(109,112,245,.55),0 6px 16px -4px rgba(79,70,229,.6);color:#4f46e5}
.mzn-c{display:inline-block;animation:mznIn .45s ease both,mznWave 1.8s ease-in-out infinite;animation-delay:calc(var(--i)*.08s),calc(var(--i)*.08s + .7s)}
.mzn-c:nth-of-type(9n+4){color:#4f46e5}.mzn-c:nth-of-type(9n+5){color:#ec4899}.mzn-c:nth-of-type(9n+6){color:#f59e0b}.mzn-c:nth-of-type(9n+7){color:#10b981}
.mzn-c:nth-of-type(9n+8){color:#3b82f6}.mzn-c:nth-of-type(9n+9){color:#8b5cf6}.mzn-c:nth-of-type(9n+10){color:#ef4444}.mzn-c:nth-of-type(9n+11){color:#06b6d4}.mzn-c:nth-of-type(9n+12){color:#f97316}
.mzn-em{position:absolute;font-size:13px;line-height:1;pointer-events:none;opacity:0;animation:mznFloat 2.8s ease-in-out infinite}
.mzn-em.e1{left:-7px;top:-10px}.mzn-em.e2{right:16px;top:-13px;animation-delay:.9s}.mzn-em.e3{right:-8px;bottom:-9px;animation-delay:1.8s}
aside a.mzn ~ .prof{margin-top:0}
@keyframes mznIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes mznWave{0%,55%,100%{transform:translateY(0) scale(1)}25%{transform:translateY(-4px) scale(1.18)}}
@keyframes mznGlow{0%,100%{box-shadow:0 0 0 0 rgba(236,72,153,0)}50%{box-shadow:0 0 14px 2px rgba(236,72,153,.35)}}
@keyframes mznBorder{to{background-position:0 0,300% 0}}
@keyframes mznFloat{0%{opacity:0;transform:translateY(6px) scale(.5) rotate(0)}25%{opacity:1}70%{opacity:1;transform:translateY(-8px) scale(1.1) rotate(14deg)}100%{opacity:0;transform:translateY(-16px) scale(.6) rotate(-10deg)}}
@media(prefers-reduced-motion:reduce){aside a.mzn,.mzn-c{animation:none!important;opacity:1}.mzn-em{display:none}}
/* Update104: compact UI for Employee + Admin pages (login pages unaffected) */
body .app{font-size:12px}
body .app aside{width:176px;padding:12px 8px;gap:2px}
body .app .brand{font-size:14px;padding:0 8px 8px}body .app .brand small{font-size:10.5px}
body .app aside a{padding:5px 9px;font-size:12px;border-radius:6px}
body .app .me{font-size:11px;margin-bottom:8px;padding:0 8px 8px}body .app .me a{padding:3px 8px;font-size:11px}
body .app .prof{padding:10px 4px 4px;gap:7px}body .app .prof .av3d{width:56px;height:56px;margin:0 0 4px}
body .app .prof-name{font-size:12.5px}body .app .prof-sub{font-size:10.5px}
body .app .prof-out{padding:4px 12px;font-size:11.5px;border-radius:6px}
body .app main{padding:14px 18px}
body .app h1{font-size:17px}body .app h2{font-size:13.5px;margin:12px 0 7px}body .app h3{font-size:12.5px;margin:9px 0 5px}
body .app .mut,body .app p,body .app small{font-size:11px}
body .app .head{margin-bottom:9px;gap:7px}
body .app .card{padding:11px 13px;margin-bottom:11px;border-radius:11px}
body .app input,body .app select,body .app textarea,body .app button{padding:4px 8px;font-size:11.5px;margin:2px;border-radius:6px}
body .app .primary,body .app .btnl{padding:4px 11px;font-size:11.5px;border-radius:6px;box-shadow:0 2px 0 #3730a3,0 6px 10px -5px #4f46e566,inset 0 1px 0 #ffffff45}
body .app .primary:hover,body .app .btnl:hover{box-shadow:0 3px 0 #3730a3,0 8px 12px -6px #4f46e577,inset 0 1px 0 #ffffff45}
body .app label,body .app .grid label{font-size:10.5px}
body .app table th,body .app table td{font-size:11px!important;padding:4px 7px!important;line-height:1.3!important}
body .app table .pill,body .app .pill{font-size:10px!important;padding:1px 7px!important}
body .app .kpis{gap:8px;margin-bottom:11px;grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}
body .app .kpi{padding:8px 11px;border-radius:10px}body .app .kpi span{font-size:11px}body .app .kpi b{font-size:19px;margin:2px 0 4px}
body .app .flash{padding:6px 10px;font-size:11.5px}
body .app .site-ftr{font-size:10px;margin-top:12px}
/* Update104: Admin login - dashboard-style 3D panel */
.win.admin{width:min(940px,100%);border-radius:16px;box-shadow:0 40px 70px -20px #05081c99,0 20px 36px -18px #000a}
.win.admin .wbar{height:34px;border-radius:16px 16px 0 0;background:linear-gradient(180deg,#232c5c,#161d42);border-bottom:1px solid #2f3a74;position:relative}
.win.admin .wbar i{width:8px;height:8px;background:#5b67b5}.win.admin .wbar i:first-child{background:#ef6a6a}.win.admin .wbar i:nth-child(2){background:#f2c25b}.win.admin .wbar i:nth-child(3){background:#5fd39a}
.win.admin .wbody{min-height:420px;border-radius:0 0 16px 16px;gap:40px;padding:28px 36px;justify-content:space-between;
 background:radial-gradient(700px 380px at 15% 10%,#3b5bdb44,transparent 60%),radial-gradient(500px 300px at 90% 100%,#7c3aed33,transparent 60%),linear-gradient(135deg,#0a1030 0%,#111a4a 55%,#1d2470 100%)}
.win.admin .scene .fl,.win.admin .scene .dp{display:none}
.win.admin .scene .gfw{opacity:.55}
.adp{position:relative;z-index:2;flex:1;min-width:0;color:#fff;transform:translateZ(30px)}
.adp-t{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#8ea8ff;margin:0 0 6px}
.adp h3{font-size:24px;line-height:1.2;margin:0 0 6px;color:#fff}
.adp-s{font-size:12.5px;color:#aab3e6;margin:0 0 20px;max-width:330px;line-height:1.5}
.adp-3d{perspective:900px;height:200px;position:relative}
.adp-st{position:absolute;inset:0;transform-style:preserve-3d;transform:rotateX(14deg) rotateY(-18deg);animation:adpFloat 7s ease-in-out infinite}
@keyframes adpFloat{0%,100%{transform:rotateX(14deg) rotateY(-18deg) translateY(0)}50%{transform:rotateX(11deg) rotateY(-14deg) translateY(-8px)}}
.adp-c{position:absolute;border-radius:12px;background:linear-gradient(160deg,#ffffff1f,#ffffff0a);border:1px solid #ffffff2e;backdrop-filter:blur(4px);box-shadow:0 18px 30px -12px #000a,inset 0 1px 0 #ffffff33}
.adp-c.c1{left:0;top:0;width:210px;height:120px;transform:translateZ(10px);padding:12px 14px}
.adp-c.c2{left:190px;top:34px;width:128px;height:76px;transform:translateZ(46px);padding:10px 12px}
.adp-c.c3{left:70px;top:112px;width:200px;height:70px;transform:translateZ(80px);padding:10px 14px;background:linear-gradient(160deg,#6d70f5cc,#4f46e5cc)}
.adp-c small{display:block;font-size:10px;color:#c9d0ee;letter-spacing:.06em;text-transform:uppercase}
.adp-bars{display:flex;align-items:flex-end;gap:7px;height:70px;margin-top:10px}
.adp-bars i{flex:1;border-radius:4px 4px 0 0;background:linear-gradient(180deg,#a5b4fc,#4f46e5);box-shadow:0 4px 8px #0006}
.adp-ring{width:34px;height:34px;border-radius:50%;margin-top:8px;border:5px solid #ffffff2a;border-top-color:#8ea8ff;border-right-color:#8ea8ff}
.adp-ln{height:6px;border-radius:3px;background:#ffffff59;margin-top:9px}.adp-ln.s{width:60%}
.win.admin .lcard{width:310px;flex:none;padding:24px 26px;border-radius:14px;text-align:left;background:linear-gradient(180deg,#fff,#f4f6ff);
 box-shadow:0 1px 0 #fff inset,0 36px 54px -16px #000a,0 10px 18px -8px #0005}
.win.admin .lav{justify-content:flex-start;margin:0 0 4px}.win.admin .lav .av3d{width:64px;height:64px;margin:0 0 4px}
.win.admin .lcard h2{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:20px;color:#1c2340;margin:4px 0 2px}
.win.admin .lcard p{font-size:12px;margin:0 0 12px}
.win.admin .lcard input{border:1px solid #cfd5e6;border-radius:8px;padding:9px 11px;font-size:13px;background:#fff}
.win.admin .lcard input:focus{outline:2px solid #c7c4fb;border-color:#4f46e5}
.win.admin .lcard input.key-pulse{border-color:#4f46e5;box-shadow:0 0 0 4px #4f46e533}
.win.admin .lcard>form>button:not(.pw-toggle){border-radius:9px;padding:10px;font-size:13.5px;background:linear-gradient(180deg,#6d70f5,#4f46e5);box-shadow:0 4px 0 #3730a3,0 12px 18px -8px #4f46e5aa,inset 0 1px 0 #ffffff55}
.win.admin .lcard>form>button:not(.pw-toggle):active{transform:translateY(3px);box-shadow:0 1px 0 #3730a3}
/* Update118: company logo on the Admin login page (UI only) */
.adp-logo{display:inline-flex;align-items:center;justify-content:center;background:rgba(255,255,255,.96);padding:10px 18px;border-radius:14px;box-shadow:0 10px 26px -8px #0009;margin:0 0 20px}
.adp-logo img{display:block;width:clamp(110px,15vw,150px);height:auto}
@media(max-width:800px){
 .win.admin .wbody{flex-direction:column;justify-content:center;align-items:center;gap:18px}
 .adp{display:flex;flex:none;justify-content:center;width:100%}.adp-body{display:none}
 .adp-logo{margin:0;padding:8px 14px;border-radius:12px}.adp-logo img{width:clamp(100px,34vw,140px)}
}
@media(max-width:480px){.adp-logo{padding:6px 12px}}
@media(max-width:800px){.win.admin .wbody{justify-content:center;padding:20px 12px}.win.admin .lcard{width:100%}}
@media(prefers-reduced-motion:reduce){.adp-st{animation:none}}
/* Update106: Employee login - 3D dashboard-style panel (UI only; form, ids and login route untouched) */
.scene.employee{--c1:#67e8f9aa;--c2:#3b82f655;--g:#7dd3fc;--r:#93c5fd}
.win.employee{width:min(900px,100%);border-radius:18px;box-shadow:0 40px 70px -22px #020617b3,0 22px 38px -20px #000a}
.win.employee .wbar{height:34px;border-radius:18px 18px 0 0;background:linear-gradient(180deg,#1b3550,#12263b);border-bottom:1px solid #2a4a6b;position:relative}
.win.employee .wbar i{width:8px;height:8px;background:#5f7f9f}.win.employee .wbar i:first-child{background:#ef6a6a}.win.employee .wbar i:nth-child(2){background:#f2c25b}.win.employee .wbar i:nth-child(3){background:#5fd39a}
.win.employee .wbody{min-height:440px;border-radius:0 0 18px 18px;padding:30px 20px;
 background:radial-gradient(700px 360px at 20% 0%,#22d3ee33,transparent 60%),radial-gradient(520px 300px at 90% 100%,#6366f133,transparent 60%),linear-gradient(135deg,#08162b 0%,#0f2b4d 55%,#0e5a73 100%)}
.win.employee .scene{border-radius:0 0 18px 18px}
.win.employee .scene .gf::before{animation:none;opacity:.28}
.win.employee .scene .fl{opacity:.8;animation-duration:12s}
.win.employee .scene .cube{animation-duration:46s}
.win.employee .scene .ring3d{display:none}
.win.employee .orb{display:none}
.win.employee .scene .rb{position:absolute;border-radius:22%;background:linear-gradient(145deg,#ffffff38,#ffffff0d);border:1px solid #ffffff40;
 box-shadow:inset 0 1px 0 #ffffff55,0 16px 26px -10px #000a;animation:bob 13s ease-in-out infinite;will-change:transform}
.win.employee .lcard{width:330px;padding:24px 26px 26px;border-radius:20px;text-align:center;position:relative;
 background:linear-gradient(180deg,#ffffff,#eef3fb);
 box-shadow:0 1px 0 #fff inset,0 -2px 0 #d5deee inset,0 40px 60px -18px #000b,0 14px 22px -10px #0007,0 0 0 1px #9fd6ff55,0 0 46px -8px #38bdf855}
.win.employee .lcard h2{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:20px;color:#1c2340;margin:6px 0 2px}
.win.employee .lcard p{font-size:12px;margin:0 0 12px}
.win.employee .lcard input{border:1px solid #c5cfe3;border-radius:11px;padding:10px 12px;font-size:13px;background:#f6f8fd;
 box-shadow:inset 0 3px 6px #1c234026,inset 0 -1px 0 #fff,0 1px 0 #fff}
.win.employee .lcard input:focus{outline:0;border-color:#4f46e5;background:#fff;box-shadow:inset 0 2px 4px #1c23401a,0 0 0 3px #4f46e535}
.win.employee .lcard input.key-pulse{border-color:#4f46e5;box-shadow:inset 0 2px 4px #1c23401a,0 0 0 4px #4f46e533}
.win.employee .lcard>form>button:not(.pw-toggle){border-radius:12px;padding:11px;font-size:14px;font-weight:600;color:#fff;
 background:linear-gradient(180deg,#5b8cff,#4f46e5);
 box-shadow:0 5px 0 #3730a3,0 14px 20px -8px #4f46e5bb,inset 0 1px 0 #ffffff66;transition:transform .12s ease,box-shadow .12s ease}
.win.employee .lcard>form>button:not(.pw-toggle):hover{transform:translateY(-1px);box-shadow:0 6px 0 #3730a3,0 18px 24px -8px #4f46e5cc,inset 0 1px 0 #ffffff66}
.win.employee .lcard>form>button:not(.pw-toggle):active{transform:translateY(4px);box-shadow:0 1px 0 #3730a3,0 4px 8px -4px #4f46e588,inset 0 1px 0 #ffffff44}
@media(max-width:800px){.win.employee .wbody{padding:20px 12px;min-height:0}.win.employee .lcard{width:100%;max-width:360px}.win.employee .scene .rb.hm,.win.employee .scene .fl.hm{display:none}}
@media(prefers-reduced-motion:reduce){.win.employee .scene .rb,.win.employee .scene .fl,.win.employee .scene .cube{animation:none}}
/* Update119: Fire-theme login pages (Admin + Employee) - matches the shared reference design. UI only; form, ids and login routes untouched */
.lg{background:radial-gradient(520px 420px at 0% 0%,#ffb27a 0%,#ffc9a0 40%,transparent 70%),radial-gradient(420px 380px at 100% 12%,#ffc58f 0%,transparent 65%),radial-gradient(460px 400px at 100% 100%,#f4857f 0%,transparent 65%),radial-gradient(380px 320px at 6% 100%,#f8c768 0%,transparent 65%),linear-gradient(135deg,#fde3d8 0%,#fbd3df 50%,#fde7d3 100%);font-family:Poppins,"Segoe UI",system-ui,-apple-system,sans-serif}
.lg .blob{display:none}
.lg .win.admin,.lg .win.employee{width:min(1000px,100%);border-radius:22px;transform:perspective(1800px) rotateX(calc(2deg + var(--rx,0deg))) rotateY(calc(-1.5deg + var(--ry,0deg))) rotateZ(-.6deg);box-shadow:0 50px 80px -24px #5a1020aa,0 24px 40px -20px #000a}
.lg .win.admin .wbar,.lg .win.employee .wbar{height:36px;border-radius:22px 22px 0 0;background:#1d0b14;border-bottom:1px solid #8a5a3c;padding:0 18px;gap:8px}
.lg .win.admin .wbar i,.lg .win.employee .wbar i{width:10px;height:10px;background:#ff5f57}
.lg .win.admin .wbar i:nth-child(2),.lg .win.employee .wbar i:nth-child(2){background:#febc2e}
.lg .win.admin .wbar i:nth-child(3),.lg .win.employee .wbar i:nth-child(3){background:#28c840}
.lg .win.admin .wbody,.lg .win.employee .wbody{min-height:520px;border-radius:0 0 22px 22px;
 background:radial-gradient(620px 380px at 18% 100%,#e8801f 0%,#b4531a66 40%,transparent 72%),radial-gradient(560px 420px at 92% 0%,#c3102b 0%,#9a0f2c88 45%,transparent 75%),radial-gradient(500px 360px at 70% 85%,#7a2418aa,transparent 70%),linear-gradient(135deg,#240b17 0%,#2d0a1a 40%,#4e0e1b 75%,#5c0f1c 100%)}
.lg .win.admin .wbody{padding:36px 44px;gap:30px}
.lg .win.employee .wbody{padding:36px 20px}
/* orange perspective grid floor + fire palette for the animated scene */
.lg .scene.admin,.lg .scene.employee{--c1:#ffffff26;--c2:#ffffff0d;--g:#ff9a3c;--r:#ffb067;--vt:#240b17;--pk:#ffd9a0;--pk2:#ff9a3c}
.lg .win .scene .gfw{opacity:.8;height:34%}
.lg .win .scene .gf::before{opacity:.5;animation:none}
.lg .win .scene .cube i{border:1px solid #ffffff30;border-radius:18%;box-shadow:inset 0 0 18px #ffffff1c}
.lg .win .scene .ring3d,.lg .win .scene .sph{display:none}
.lg .win.employee .scene .fl,.lg .win.admin .scene .fl{opacity:.9}
.lg .win.employee .scene .rb{display:none}
.lg .win.employee .orb{display:none}
.lg .win.employee .scene .dp{display:block}
.lg .dp-lab{color:#ffe3c4;opacity:.9;letter-spacing:.3em;text-shadow:0 0 10px #ff9a3c88}
.lg .dp-lab b{color:#ff9a3c}
.lg .dp-scr{border:1.5px solid #ffb067;background:linear-gradient(140deg,#ffffff22,#ffffff08);box-shadow:0 0 16px #ff9a3c55}
.lg .dp-scr i{background:#ffd9a0}
.lg .dp-node small{color:#ffe3c4;letter-spacing:.3em}
/* fire card */
.lg .win.admin .lcard,.lg .win.employee .lcard{background:linear-gradient(180deg,#fff,#fdf3f0);border-radius:20px;box-shadow:0 1px 0 #fff inset,0 40px 60px -18px #000c,0 12px 20px -10px #0006}
.lg .win.employee .lcard{width:350px;padding:26px 30px 22px;text-align:center}
.lg .win.admin .lcard{width:360px;padding:26px 30px 28px;text-align:left}
.lg .lcard h2{font-family:Poppins,"Segoe UI",system-ui,sans-serif;font-weight:700;font-size:22px;color:#2a0f1a;margin:6px 0 0}
.lg .lcard>p{color:#8a6670;font-size:13px;margin:2px 0 14px}
.lg .lcard input{border:1px solid #f0d9d4;border-radius:12px;padding:11px 14px;font-size:14px;background:#fff;color:#2a0f1a;box-shadow:none}
.lg .lcard input::placeholder{color:#b49a9e}
.lg .lcard input:focus,.lg .lcard input.key-pulse{outline:0;border-color:#ff8a3c;box-shadow:0 0 0 4px #ff8a3c33}
.lg .lcard .pw-toggle{color:#e2531a;font-weight:700}
.lg .lcard .pw-toggle:hover{background:#fff1e8;color:#c13f0d}
.lg .lcard>form>button:not(.pw-toggle){border-radius:12px;padding:12px;font-size:15px;font-weight:700;color:#fff;background:linear-gradient(180deg,#ff8a2a,#e8501a);box-shadow:0 5px 0 #b3340f,0 14px 20px -8px #e8501acc,inset 0 1px 0 #ffffff66}
.lg .lcard>form>button:not(.pw-toggle):hover{transform:translateY(-1px);box-shadow:0 6px 0 #b3340f,0 18px 24px -8px #e8501add,inset 0 1px 0 #ffffff66}
.lg .lcard>form>button:not(.pw-toggle):active{transform:translateY(4px);box-shadow:0 1px 0 #b3340f}
.lcard-logo{display:block;margin:0 auto 4px;width:clamp(130px,42%,170px);height:auto}
.lcard-top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 6px}
.lcard-top .lav{margin:0}.lcard-top .lcard-logo{margin:0;width:clamp(100px,38%,128px)}
.win.admin .lcard-top .lav .av3d,.win.admin .lcard-top .lav{width:64px;height:64px}
.fgt{display:block;margin:12px 0 0;font-size:12.5px;color:#8a6670;text-align:center}
/* admin left text panel */
.lg .adp-t{color:#ffc58f;letter-spacing:.3em}
.lg .adp h3{font-size:34px;font-weight:700;line-height:1.15;margin:0 0 14px}
.lg .adp-s{color:#f3d3c6;font-size:14px;max-width:330px}
.lg .adp-c{background:linear-gradient(160deg,#ffffff26,#ffffff0d);border:1px solid #ffffff33}
.lg .adp-c small{color:#f0d3c6}
.lg .adp-bars i{background:linear-gradient(180deg,#ffb067,#e8501a)}
.lg .adp-ring{border-top-color:#ff9a3c;border-right-color:#ff9a3c}
.lg .adp-c.c3{background:linear-gradient(160deg,#f2542dee,#c8102ecc)}
.lg .adp-3d{height:230px}
@media(max-width:800px){.lg .win.admin,.lg .win.employee{transform:none!important}.lg .win.admin .wbody,.lg .win.employee .wbody{padding:22px 12px;min-height:0}.lg .win.admin .lcard,.lg .win.employee .lcard{width:100%;max-width:380px}}
/* Update108: admin 3D avatar + sidebar calendar */
.av-adm{position:relative;flex:none;width:64px;height:64px;border-radius:50%;overflow:hidden;border:3px solid #ffffffd9;
 box-shadow:inset 0 -6px 10px #0000004d,inset 0 4px 8px #ffffff59,0 10px 0 -4px #151b3f,0 14px 20px -4px #000a,0 0 0 3px #4f46e555,0 0 18px #6d70f566;transition:transform .25s ease}
.av-adm svg{display:block;width:100%;height:100%}
.prof:hover .av-adm{transform:translateY(-2px) rotate(-2deg)}
.prof .av-adm{width:64px;height:64px}
@media(max-width:800px){.prof .av-adm{width:40px;height:40px;border-width:2px}}
.cal{margin:10px 2px 8px;padding:7px 6px 8px;border:1px solid #2b3560;border-radius:10px;background:#ffffff0a;color:#c9d0ee;font-size:11px}
.cal summary{cursor:pointer;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#9aa3c7;list-style:none;padding:0 2px}
.cal summary::-webkit-details-marker{display:none}
.cal-h{display:flex;align-items:center;justify-content:space-between;margin:6px 0 4px}
.cal-h b{font-size:12px;color:#fff;font-weight:600}
.cal-h button{width:20px;height:20px;padding:0;margin:0;border:0;border-radius:6px;background:#2b3560;color:#fff;font-size:14px;line-height:1;box-shadow:none;cursor:pointer}
.cal-h button:hover{background:#4f46e5;transform:none}
.cal-g{display:grid;grid-template-columns:repeat(7,1fr);gap:1px;text-align:center}
.cal-g span{padding:3px 0;border-radius:6px;font-size:10.5px;line-height:1.2}
.cal-g .w{color:#7f89b8;font-size:9.5px}.cal-g .o{color:#5d6794}.cal-g .e{color:#aab3e0}
.cal-g .t{background:linear-gradient(180deg,#6d70f5,#4f46e5);color:#fff;font-weight:700;box-shadow:0 2px 0 #3730a3,0 0 10px #6d70f588}
.cal-today{display:block;width:100%;margin:6px 0 0;padding:3px 0;border:0;border-radius:6px;background:#2b3560;color:#fff;font-size:10.5px;box-shadow:none;cursor:pointer}
.cal-today:hover{background:#4f46e5;transform:none}
@media print{.cal{display:none!important}}
.panel-ttl{padding:2px 9px 9px;margin:0 0 4px;border-bottom:1px solid #2b3560;font-size:12.5px;font-weight:700;letter-spacing:.06em;color:#fff;text-transform:none}
@media(max-width:800px){.panel-ttl{border:0;padding:4px 8px;margin:0}}
</style></head><body>
{% if bare %}{{body|safe}}
{% elif session.role %}<div class="app"><aside class="emp">
<div class="panel-ttl">{{ 'Admin Panel' if session.role=='admin' else 'Employee Panel' }}</div>
{% for h,l,on,kids in nav %}{% if kids %}<div class="ng{{' open' if on else ''}}"><a class="ng-h" href="{{h}}" role="button" aria-expanded="{{'true' if on else 'false'}}" onclick="var g=this.parentNode;var o=g.classList.toggle('open');this.setAttribute('aria-expanded',o);return false">{{l}}<span class="chev">&#9650;</span></a>
<div class="kids">{% for kh,kl,kon in kids %}<a href="{{kh}}" class="{{'on' if kon else ''}}">{{kl}}</a>{% endfor %}</div></div>
{% elif h == '/employee/mahizhchi' %}<a href="{{h}}" class="mzn{{' on' if on else ''}}" aria-label="{{l}}"><span class="mzn-em e1" aria-hidden="true">✨</span><span class="mzn-em e2" aria-hidden="true">🎉</span><span class="mzn-em e3" aria-hidden="true">🌟</span>{% for ch in l %}<span class="mzn-c" aria-hidden="true" style="--i:{{loop.index0}}">{{ch}}</span>{% endfor %}</a>
{% else %}<a href="{{h}}" class="{{'on' if on else ''}}">{{l}}</a>{% endif %}{% endfor %}
<details class="cal" id="cal"><summary>Calendar</summary><div class="cal-h"><button type="button" id="cal_p" aria-label="Previous month">&lsaquo;</button><b id="cal_t"></b><button type="button" id="cal_n" aria-label="Next month">&rsaquo;</button></div><div class="cal-g" id="cal_g"></div><button type="button" class="cal-today" id="cal_td">Today</button></details>
<div class="prof{{' prof-emp' if session.role=='employee' else ''}}"><div class="prof-row">{{side_avatar|safe}}<div class="prof-info"><div class="prof-name">{{session.name}}</div></div></div>
<a class="prof-out" href="/logout">Logout</a></div>
</aside>
<main>{% for c,m in get_flashed_messages(with_categories=true) %}<p class="flash {{'err' if c=='error' else ''}}">{{m}}</p>{% endfor %}<div class="mbody">{{body|safe}}</div><div class="site-foot" role="contentinfo">@2026_Mobius365 | LN_Map_AI</div></main></div>
{% else %}<div class="lg"><div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div><div class="blob b3" aria-hidden="true"></div>{% for c,m in get_flashed_messages(with_categories=true) %}<p class="flash {{'err' if c=='error' else ''}}" style="{{'' if c=='error' else 'background:#fff'}}">{{m}}</p>{% endfor %}{{body|safe}}<div class="site-foot" role="contentinfo">@2026_Mobius365 | LN_Map_AI</div></div>{% endif %}
{% if session.role and not bare %}<script>
(function(){var g=document.getElementById('cal_g');if(!g)return;var d=document.getElementById('cal');
var M=['January','February','March','April','May','June','July','August','September','October','November','December'],W=['S','M','T','W','T','F','S'];
var now=new Date(),y=now.getFullYear(),m=now.getMonth();
if(window.matchMedia&&window.matchMedia('(min-width:801px)').matches)d.open=true;
function draw(){var h='',i,first=new Date(y,m,1).getDay(),n=new Date(y,m+1,0).getDate(),pn=new Date(y,m,0).getDate();
document.getElementById('cal_t').textContent=M[m].slice(0,3)+' '+y;
for(i=0;i<7;i++)h+='<span class="w">'+W[i]+'</span>';
for(i=first-1;i>=0;i--)h+='<span class="o">'+(pn-i)+'</span>';
for(i=1;i<=n;i++){var t=(i===now.getDate()&&m===now.getMonth()&&y===now.getFullYear());h+='<span class="'+(t?'t':'e')+'"'+(t?' aria-current="date"':'')+'>'+i+'</span>'}
var tail=(7-(first+n)%7)%7;for(i=1;i<=tail;i++)h+='<span class="o">'+i+'</span>';g.innerHTML=h}
document.getElementById('cal_p').onclick=function(){m--;if(m<0){m=11;y--}draw()};
document.getElementById('cal_n').onclick=function(){m++;if(m>11){m=0;y++}draw()};
document.getElementById('cal_td').onclick=function(){now=new Date();y=now.getFullYear();m=now.getMonth();draw()};
draw()})();
</script>{% endif %}
{% if session.role=='admin' %}<div id="toasts"></div><script>
(function(){var since="0",first=1;
function toast(t){var d=document.createElement('div');d.className='toast';d.textContent=t;
 document.getElementById('toasts').appendChild(d);setTimeout(function(){d.remove()},10000)}
function poll(){fetch('/admin/notify/poll?since='+since+'&first='+first,{credentials:'same-origin'})
 .then(function(r){return r.json()}).then(function(j){
 j.items.forEach(function(i){toast(i.text)});since=j.last;first=0}).catch(function(){})}
poll();setInterval(poll,15000)})();
</script>{% endif %}
{% if session.role=='employee' %}<div id="toasts"></div><script>(function(){var K='mzSeen',seen=null;
try{var raw=sessionStorage.getItem(K);seen=raw?JSON.parse(raw):null}catch(e){seen=null}
function toast(t){var d=document.createElement('div');d.className='toast';d.textContent=t;document.getElementById('toasts').appendChild(d);setTimeout(function(){d.remove()},12000)}
function board(j){var b=document.getElementById('mzboard');if(!b)return;b.textContent='';
 if(j.overall){var o=document.createElement('div');o.className='mz-win';o.style.fontWeight='700';o.textContent='🏆 Overall Winner: '+j.overall.name+' — first to complete all Sets';b.appendChild(o)}
 j.board.forEach(function(x){var d=document.createElement('div');d.className='mz-win'+(x.name?'':' none');
  d.textContent=x.name?('🏆 Set '+x.n+' Winner: '+x.name):('Set '+x.n+' — no winner yet');b.appendChild(d)})}
function poll(){fetch('/employee/mahizhchi/winners',{credentials:'same-origin',cache:'no-store'}).then(function(r){return r.json()}).then(function(j){
 if(!j.show)return;board(j);var cur=j.winners.map(function(w){return w.set});if(j.overall)cur.push('ALL');
 if(seen===null){seen=cur}else{j.winners.forEach(function(w){if(seen.indexOf(w.set)<0){seen.push(w.set);toast(w.text)}});
  if(j.overall&&seen.indexOf('ALL')<0){seen.push('ALL');toast(j.overall.text)}}
 try{sessionStorage.setItem(K,JSON.stringify(seen))}catch(e){}}).catch(function(){})}
poll();setInterval(poll,10000)})();</script>
<script>(function(){function p(){fetch('/employee/ping',{credentials:'same-origin',cache:'no-store'}).catch(function(){})}p();setInterval(p,15000)})();</script>{% endif %}
{% if session.role=='employee' and request.path!='/employee/welcome' %}<style>
#gcb{position:fixed;right:20px;bottom:20px;z-index:98;width:62px;height:62px;border-radius:50%;border:0;padding:0;cursor:pointer;display:flex;align-items:center;justify-content:center;
 background:radial-gradient(circle at 32% 26%,#5fe0c8 0%,#1f9fd8 46%,#4a3fd0 100%);box-shadow:0 10px 22px #2b3fa866,0 2px 0 #ffffff66 inset,0 -4px 8px #1b1f7a55 inset;transition:transform .15s ease}
#gcb:hover{transform:scale(1.08)}#gcb:focus-visible{outline:3px solid #9bb4ff;outline-offset:3px}
#gcn{display:none;position:absolute;top:-3px;right:-3px;background:#ff3b30;color:#fff;border:2px solid #fff;border-radius:11px;font:700 11px/1 system-ui,sans-serif;padding:3px 6px;min-width:10px;text-align:center}
#gcp{position:fixed;right:20px;bottom:96px;z-index:99;width:min(380px,calc(100vw - 24px));height:min(520px,calc(100vh - 120px));background:#fff;border:1px solid #d8dbe6;border-radius:16px;box-shadow:0 20px 50px #0003;display:flex;flex-direction:column;overflow:hidden;font-family:system-ui,-apple-system,Segoe UI,sans-serif}
#gcp[hidden]{display:none}
#gcp button,#gcp input{margin:0}
#gcp .gc-h{display:flex;align-items:center;gap:8px;padding:11px 14px;background:linear-gradient(120deg,#1f9fd8,#4a3fd0);color:#fff}
#gcp .gc-h b{font-size:15px;flex:1}#gcp .gc-h span{font-size:12px;background:#ffffff33;border-radius:10px;padding:2px 8px}
#gcp .gc-h button{background:none;border:0;color:#fff;font-size:20px;line-height:1;cursor:pointer;padding:0 2px;box-shadow:none}
#gcm{display:flex;gap:6px;overflow-x:auto;padding:8px 10px;border-bottom:1px solid #e6e8f0;background:#f6f8ff;flex:none}
#gcm i{font-style:normal;white-space:nowrap;font-size:12px;background:#fff;border:1px solid #d8dbe6;border-radius:12px;padding:3px 9px;color:#1c2340}
#gcm i:before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:#2fb26a;margin-right:5px}
#gcm i.away:before{background:#e0a020}
#gcl{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:7px;background:#f8f9fd}
#gcl .gc-b{max-width:82%;padding:7px 11px;border-radius:14px;font-size:13.5px;line-height:1.4;word-wrap:break-word;overflow-wrap:anywhere;white-space:pre-wrap}
#gcl .gc-b b{display:block;font-size:11px;color:#4a3fd0;margin-bottom:2px}#gcl .gc-b small{display:block;font-size:10px;opacity:.65;margin-top:3px}
#gcl .gc-b.me{align-self:flex-end;background:#4a3fd0;color:#fff;border-bottom-right-radius:4px}
#gcl .gc-b.th{align-self:flex-start;background:#fff;border:1px solid #d8dbe6;border-bottom-left-radius:4px}
#gcl .gc-b .gc-big{font-size:34px;line-height:1.15}
#gcl .gc-e{color:#6b7390;font-size:13px;text-align:center;padding:18px}
#gcl .gc-imgl{display:block;margin:2px 0 4px;line-height:0}
#gcl .gc-img{max-width:100%;max-height:220px;border-radius:10px;display:block;background:#e9ecf6;min-width:60px;min-height:40px}
#gcl .gc-file{display:flex;align-items:center;gap:9px;text-decoration:none;color:inherit;background:#0000000d;border-radius:10px;padding:7px 9px;margin:2px 0 4px;white-space:normal}
#gcl .gc-b.me .gc-file{background:#ffffff26}
#gcl .gc-file .gc-fi{font-size:24px;line-height:1}
#gcl .gc-file .gc-fn{min-width:0}#gcl .gc-file .gc-fn b{display:block;font-size:12.5px;color:inherit;margin:0;word-break:break-all}
#gcl .gc-file .gc-fn small{margin:0}
#gcl .gc-gone{font-size:12px;opacity:.7;font-style:italic;margin:2px 0 4px}
#gcpv{display:flex;align-items:center;gap:10px;padding:8px 12px;border-top:1px solid #e6e8f0;background:#f6f8ff;flex:none}
#gcpv[hidden]{display:none}
#gcpv img{width:44px;height:44px;object-fit:cover;border-radius:8px}
#gcpv .gc-pi{font-size:26px}
#gcpv .gc-pn{flex:1;min-width:0;font-size:12.5px}#gcpv .gc-pn b{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}#gcpv .gc-pn small{color:#6b7390}
#gcpv button{border:0;background:#e5e8f4;border-radius:50%;width:24px;height:24px;cursor:pointer;font-size:14px;line-height:1;padding:0}
#gcem{position:absolute;left:8px;right:8px;bottom:62px;height:210px;background:#fff;border:1px solid #d8dbe6;border-radius:12px;box-shadow:0 10px 30px #0003;display:flex;flex-direction:column;z-index:3}
#gcem[hidden]{display:none}
#gcem .gc-tabs{display:flex;gap:4px;padding:6px 8px;border-bottom:1px solid #e6e8f0}
#gcem .gc-tabs button{border:0;background:none;font-size:20px;cursor:pointer;border-radius:8px;padding:3px 9px}
#gcem .gc-tabs button.on{background:#e8e6fb}
#gcem .gc-grid{flex:1;overflow:auto;display:grid;grid-template-columns:repeat(8,1fr);gap:2px;padding:6px 8px;align-content:start}
#gcem .gc-grid button{border:0;background:none;font-size:22px;line-height:1;cursor:pointer;border-radius:8px;padding:5px 0}
#gcem .gc-grid button:hover{background:#eef0fb}
#gcp .gc-f{display:flex;align-items:center;gap:6px;padding:10px;border-top:1px solid #e6e8f0;flex:none}
#gcp .gc-f .gc-t{width:34px;height:34px;flex:none;border:0;background:#eef0fb;border-radius:50%;font-size:17px;line-height:1;cursor:pointer;padding:0;box-shadow:none;display:flex;align-items:center;justify-content:center}
#gcp .gc-f .gc-t:hover{background:#e0e3f7}
#gcp .gc-f input[type=text]{flex:1;padding:9px 11px;border:1px solid #d8dbe6;border-radius:10px;font-size:14px;min-width:0}
#gcp .gc-f #gcs{padding:9px 13px;border:0;border-radius:10px;background:#4a3fd0;color:#fff;font-weight:600;cursor:pointer;flex:none}
#gcp .gc-f #gcs:disabled{opacity:.6;cursor:default}
#gcp.gc-drop{outline:3px dashed #4a3fd0;outline-offset:-6px}
@media print{ #gcb,#gcp{display:none}}
</style>
<button id="gcb" type="button" title="Group Chat - employees online now" aria-label="Group Chat" aria-expanded="false"><svg viewBox="0 0 64 64" width="42" height="42" aria-hidden="true" focusable="false"><defs><linearGradient id="gc_l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bfe0ff"/></linearGradient></defs><circle cx="17" cy="26" r="5.500" fill="#d6ecff" opacity="0.85"/><path d="M5 47Q5 35 17 35Q21 35 24 37L24 47Z" fill="#d6ecff" opacity="0.85"/><circle cx="47" cy="26" r="5.500" fill="#d6ecff" opacity="0.85"/><path d="M59 47Q59 35 47 35Q43 35 40 37L40 47Z" fill="#d6ecff" opacity="0.85"/><circle cx="32" cy="23" r="8" fill="url(#gc_l)"/><path d="M18 49Q18 34 32 34Q46 34 46 49Z" fill="url(#gc_l)"/></svg><span id="gcn"></span></button>
<div id="gcp" hidden role="dialog" aria-label="Group Chat">
 <div class="gc-h"><b>Group Chat</b><span id="gcc">0 online</span><button id="gcx" type="button" aria-label="Close">&times;</button></div>
 <div id="gcm"></div>
 <div id="gcl"><div class="gc-e">No messages yet - say hello to everyone who is online.</div></div>
 <div id="gcpv" hidden></div>
 <div id="gcem" hidden></div>
 <div class="gc-f">
  <button class="gc-t" id="gcat" type="button" title="Send a file" aria-label="Send a file">&#128206;</button>
  <button class="gc-t" id="gcim" type="button" title="Send a photo / image" aria-label="Send a photo or image">&#128247;</button>
  <button class="gc-t" id="gcemb" type="button" title="Emoji" aria-label="Emoji">&#128522;</button>
  <input type="text" id="gci" maxlength="500" placeholder="Message everyone online..." autocomplete="off">
  <button id="gcs" type="button">Send</button>
 </div>
 <input type="file" id="gcfi" hidden>
 <input type="file" id="gcii" accept="image/*" hidden>
</div>
<script>
/* Update82: Group Chat with files, images/photos and emoji. One group = the employees online right now. Messages and attachments auto-delete after 1 hour. No audio. */
(function(){
var $=function(i){return document.getElementById(i)};
var btn=$('gcb'),pan=$('gcp'),listEl=$('gcl'),memEl=$('gcm'),inp=$('gci'),cnt=$('gcc'),bdg=$('gcn'),pv=$('gcpv'),emp=$('gcem'),
    fileIn=$('gcfi'),imgIn=$('gcii'),sendB=$('gcs'),
    open=false,busy=false,again=false,after=-1,shown={},base=document.title,pending=null,pendUrl=null,sending=false,MAXF=5*1024*1024;
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function cp(n){return String.fromCodePoint(n)}
function fmt(n){return n<1024?n+' B':(n<1048576?(n/1024).toFixed(1)+' KB':(n/1048576).toFixed(1)+' MB')}
function badge(n){bdg.textContent=n>99?'99+':n;bdg.style.display=n?'block':'none';document.title=(n?'('+n+') New message - ':'')+base}
function note(t){var e=el('div','gc-e',t);listEl.appendChild(e);listEl.scrollTop=listEl.scrollHeight;setTimeout(function(){e.remove()},4500)}
function members(list){memEl.textContent='';cnt.textContent=list.length+' online';
 list.forEach(function(m){memEl.appendChild(el('i',m.status==='Away'?'away':'',m.name+(m.me?' (You)':'')))})}
function emojiOnly(t){t=t.trim();if(!t||t.length>14)return false;for(var i=0;i<t.length;i++){if(t.charCodeAt(i)<128)return false}return true}

/* ---------- attachments inside a message ---------- */
function attach(a,stick){
 if(a.gone)return el('div','gc-gone',cp(0x1F4C4)+' '+a.name+' - no longer available');
 var url='/employee/gc/file/'+a.fid;
 if(a.kind==='image'){
  var l=el('a','gc-imgl');l.href=url;l.target='_blank';l.rel='noopener';
  var im=el('img','gc-img');im.alt=a.name;im.title=a.name;im.src=url;im.onload=function(){if(stick())listEl.scrollTop=listEl.scrollHeight};
  im.onerror=function(){l.replaceWith(el('div','gc-gone',cp(0x1F5BC)+' '+a.name+' - could not load'))};
  l.appendChild(im);return l}
 var f=el('a','gc-file');f.href=url+'?dl=1';f.setAttribute('download',a.name);
 f.appendChild(el('span','gc-fi',cp(0x1F4C4)));
 var n=el('div','gc-fn');n.appendChild(el('b','',a.name));n.appendChild(el('small','',fmt(a.size)+' \u00B7 tap to download'));f.appendChild(n);return f}

function msgs(list,now){
 Array.prototype.slice.call(listEl.querySelectorAll('.gc-b')).forEach(function(b){if(now-parseFloat(b.getAttribute('data-ts'))>43200)b.remove()});
 if(!list.length)return;
 var e0=listEl.querySelector('.gc-e');if(e0)e0.remove();
 var down=listEl.scrollHeight-listEl.scrollTop-listEl.clientHeight<80||after<0;
 list.forEach(function(x){if(shown[x.id])return;shown[x.id]=1;var b=el('div','gc-b '+(x.mine?'me':'th'));b.setAttribute('data-ts',x.ts);
  if(!x.mine)b.appendChild(el('b','',x.name));
  if(x.att)b.appendChild(attach(x.att,function(){return down}));
  if(x.text){var tx=el('div',emojiOnly(x.text)&&!x.att?'gc-big':'',x.text);b.appendChild(tx)}
  b.appendChild(el('small','',x.t));listEl.appendChild(b);after=Math.max(after,x.id)});
 if(down)listEl.scrollTop=listEl.scrollHeight}

/* ---------- polling ---------- */
function done(){busy=false;if(again){again=false;poll()}}
function poll(){if(busy){again=true;return}busy=true;
 fetch('/employee/gc/state?after='+after+'&open='+(open&&!document.hidden?1:0),{credentials:'same-origin',cache:'no-store'})
 .then(function(r){return r.json()}).then(function(j){badge(open?0:j.unread);members(j.members);msgs(j.messages,j.now);done()}).catch(function(){done()})}
function setOpen(v){open=v;pan.hidden=!v;btn.setAttribute('aria-expanded',v?'true':'false');if(!v)emp.hidden=true;
 if(v){badge(0);poll();setTimeout(function(){listEl.scrollTop=listEl.scrollHeight;inp.focus()},50)}}

/* ---------- pending attachment (preview before sending) ---------- */
function clearPending(){if(pendUrl){URL.revokeObjectURL(pendUrl);pendUrl=null}pending=null;pv.hidden=true;pv.textContent='';fileIn.value='';imgIn.value=''}
function setPending(f){
 if(!f)return;
 if(f.size>MAXF){note('That file is '+fmt(f.size)+' - the limit is 5 MB.');return}
 if(f.size===0){note('That file is empty.');return}
 clearPending();pending=f;pv.textContent='';
 if(f.type&&f.type.indexOf('image/')===0&&f.type!=='image/svg+xml'){pendUrl=URL.createObjectURL(f);var im=el('img');im.src=pendUrl;im.alt='';pv.appendChild(im)}
 else pv.appendChild(el('span','gc-pi',cp(0x1F4C4)));
 var n=el('div','gc-pn');n.appendChild(el('b','',f.name||'file'));n.appendChild(el('small','',fmt(f.size)));pv.appendChild(n);
 var x=el('button','','\u00D7');x.type='button';x.title='Remove';x.setAttribute('aria-label','Remove attachment');x.onclick=clearPending;pv.appendChild(x);
 pv.hidden=false;inp.focus()}

/* ---------- sending ---------- */
function send(){
 var t=inp.value.trim();if((!t&&!pending)||sending)return;
 sending=true;sendB.disabled=true;emp.hidden=true;
 var fd=new FormData();fd.append('text',t);if(pending)fd.append('file',pending,pending.name||'file');
 var keepT=t,keepF=pending;inp.value='';
 fetch('/employee/gc/send',{method:'POST',body:fd,credentials:'same-origin'})
 .then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j}},function(){return {ok:false,j:{error:'Not sent (server error).'}}})})
 .then(function(x){sending=false;sendB.disabled=false;
  if(x.ok){clearPending()}else{inp.value=keepT;if(keepF&&!pending)setPending(keepF);note(x.j.error||'Not sent.')}
  poll();inp.focus()})
 .catch(function(){sending=false;sendB.disabled=false;inp.value=keepT;note('Not sent - check your connection.')})}

/* ---------- emoji picker ---------- */
var SETS=[[0x1F600,[0x1F600,0x1F601,0x1F602,0x1F923,0x1F603,0x1F604,0x1F605,0x1F606,0x1F609,0x1F60A,0x1F60B,0x1F60E,0x1F60D,0x1F618,0x1F970,0x1F617,0x1F642,0x1F917,0x1F929,0x1F914,0x1F928,0x1F610,0x1F611,0x1F636,0x1F644,0x1F60F,0x1F623,0x1F625,0x1F62E,0x1F910,0x1F62F,0x1F62A,0x1F62B,0x1F634,0x1F60C,0x1F61B,0x1F61C,0x1F61D,0x1F924,0x1F612,0x1F613,0x1F614,0x1F615,0x1F643,0x1F911,0x1F632,0x1F641,0x1F616,0x1F61E,0x1F61F,0x1F624,0x1F622,0x1F62D,0x1F626,0x1F627,0x1F628,0x1F629,0x1F92F,0x1F62C,0x1F630,0x1F631,0x1F633,0x1F92A,0x1F635,0x1F621,0x1F620,0x1F637,0x1F912,0x1F915,0x1F922,0x1F607,0x1F920,0x1F973]],
 [0x1F44D,[0x1F44D,0x1F44E,0x1F44C,0x1F91E,0x1F91D,0x1F44F,0x1F64C,0x1F64F,0x1F4AA,0x1F44B,0x1F91A,0x1F449,0x1F448,0x1F446,0x1F447,0x1F44A,0x270A,0x1F91B,0x1F91C,0x1F450,0x1F64B,0x1F926,0x1F937,0x1F645,0x1F646,0x1F64D,0x1F481,0x1F440,0x1F442,0x1F9E0]],
 [0x2728,[0x1F496,0x1F495,0x1F49B,0x1F499,0x1F49A,0x1F49C,0x1F5A4,0x1F494,0x1F4AF,0x1F525,0x2728,0x1F389,0x1F38A,0x1F381,0x1F388,0x1F31F,0x2B50,0x1F4A1,0x1F4A5,0x1F4A4,0x1F680,0x1F3C6,0x2615,0x1F355,0x1F382,0x2705,0x274C,0x2753,0x2757,0x1F4CC,0x1F4CE,0x1F4C5,0x23F0,0x1F4BC,0x1F4BB,0x1F4DE,0x1F4CA,0x1F4C8,0x1F4DD,0x1F4E7]]];
var emBuilt=false,emTab=0;
function insertEmoji(ch){var s=inp.selectionStart,e=inp.selectionEnd,v=inp.value;if(typeof s!=='number'){s=e=v.length}
 if(v.length+ch.length>500)return;inp.value=v.slice(0,s)+ch+v.slice(e);var p=s+ch.length;inp.focus();try{inp.setSelectionRange(p,p)}catch(x){}}
function drawGrid(){var g=emp.querySelector('.gc-grid');g.textContent='';SETS[emTab][1].forEach(function(n){var b=el('button','',cp(n));b.type='button';b.onclick=function(){insertEmoji(cp(n))};g.appendChild(b)});
 Array.prototype.forEach.call(emp.querySelectorAll('.gc-tabs button'),function(b,i){b.className=i===emTab?'on':''})}
function buildEmoji(){if(emBuilt)return;emBuilt=true;var tabs=el('div','gc-tabs');
 SETS.forEach(function(s,i){var b=el('button','',cp(s[0]));b.type='button';b.onclick=function(){emTab=i;drawGrid()};tabs.appendChild(b)});
 emp.appendChild(tabs);emp.appendChild(el('div','gc-grid'));drawGrid()}
$('gcemb').onclick=function(){buildEmoji();emp.hidden=!emp.hidden;if(!emp.hidden)inp.focus()};

/* ---------- wiring ---------- */
btn.onclick=function(){setOpen(!open)};
$('gcx').onclick=function(){setOpen(false)};
$('gcat').onclick=function(){fileIn.click()};
$('gcim').onclick=function(){imgIn.click()};
fileIn.onchange=function(){if(fileIn.files&&fileIn.files[0])setPending(fileIn.files[0])};
imgIn.onchange=function(){if(imgIn.files&&imgIn.files[0])setPending(imgIn.files[0])};
sendB.onclick=send;
inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();send()}});
inp.addEventListener('paste',function(e){var it=(e.clipboardData&&e.clipboardData.items)||[];
 for(var i=0;i<it.length;i++){if(it[i].kind==='file'){var f=it[i].getAsFile();if(f){e.preventDefault();setPending(f);return}}}});
pan.addEventListener('dragover',function(e){e.preventDefault();pan.classList.add('gc-drop')});
pan.addEventListener('dragleave',function(e){if(e.target===pan)pan.classList.remove('gc-drop')});
pan.addEventListener('drop',function(e){e.preventDefault();pan.classList.remove('gc-drop');if(e.dataTransfer&&e.dataTransfer.files&&e.dataTransfer.files[0])setPending(e.dataTransfer.files[0])});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&open){if(!emp.hidden)emp.hidden=true;else setOpen(false)}});
document.addEventListener('visibilitychange',function(){if(!document.hidden)poll()});
poll();
(function loop(){setTimeout(function(){if(!document.hidden||open)poll();loop()},open?2000:6000)})();
})();
</script>{% endif %}
{% if session.role=='admin' and request.path not in ['/admin/welcome'] %}<script>/* Update88: Admin page auto-refresh every 2 minutes (same as F5), repeating. Admin browser only. */
setInterval(function(){location.reload()},120000);
</script>{% endif %}
{% if session.role and request.path not in ['/employee/welcome','/admin/welcome'] %}<script>
/* Update79: one short, identical click sound for every button / link / control on the Admin and Employee pages. No music here. */
(function(){
 var AC=window.AudioContext||window.webkitAudioContext,ctx=null;
 var SEL='a[href],button,input[type=button],input[type=submit],input[type=checkbox],input[type=radio],select,summary,[role=button],[onclick],.btn';
 function prime(){try{if(!AC)return;if(!ctx)ctx=new AC();if(ctx.state==='suspended')ctx.resume()}catch(e){}}
 function tick(){
  try{prime();if(!ctx)return;var t=ctx.currentTime,o=ctx.createOscillator(),g=ctx.createGain();
   o.type='sine';o.frequency.setValueAtTime(1400,t);o.frequency.exponentialRampToValueAtTime(700,t+0.05);
   g.gain.setValueAtTime(0.0001,t);g.gain.linearRampToValueAtTime(0.16,t+0.005);g.gain.exponentialRampToValueAtTime(0.0001,t+0.07);
   o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+0.08)}catch(e){}
 }
 ['pointerdown','keydown','touchstart'].forEach(function(n){document.addEventListener(n,prime,{capture:true,once:true,passive:true})});
 document.addEventListener('click',function(e){
  var t=e.target&&e.target.closest?e.target.closest(SEL):null;
  if(!t||t.disabled||t.getAttribute('aria-disabled')==='true')return;
  tick();
 },true);
})();
</script>{% endif %}
</body></html>"""

NAVS = {
    "admin": [("/admin/summary", "Overview"), ("/admin/processes", "Processes"), ("/admin/log", "Productivity log"), 
              ("/admin/leave-permission", "Leave & Permission Log"),
              ("/admin/employee-info", "Employee Info"), ("/admin/audit", "Audit Log"),
              ("/admin/email-controls", "Email Controls")],
    "employee": [("/employee", "Daily entry"), ("/employee/leave", "Leave & Permission"),
                 ("/employee/profile", "Personal details"), ("/employee/productivity", "Productivity Info")],
}

from functools import lru_cache
@lru_cache(maxsize=128)
def _compiled(src):
    return app.jinja_env.from_string(src)          # Update114: compile each page template once, not on every request

def render_fast(src, **context):
    """Same output as render_template_string(), but the compiled template is reused (big layouts were being re-compiled on every page view)."""
    app.update_template_context(context)
    return _compiled(src).render(context)

def page(body, title="Productivity Tracker", **ctx):
    ctx["title"] = title
    p = request.path
    items = list(NAVS.get(session.get("role"), []))
    if session.get("role") == "employee":
        try:      # Admin-controlled: the menu item exists only while Audit Log access is enabled for this employee
            if audit_active(audit_access(session.get("emp_id", ""))): items.append(("/employee/audit", "Audit Log"))
        except Exception:
            pass
        try:      # Admin-controlled: Mahizhchi appears only while it is published AND shared with this employee
            if mz_active(session.get("emp_id", "")): items.append(("/employee/mahizhchi", MZ_TITLE))
        except Exception as e:
            print("Mahizhchi menu check failed (are the Mahizhchi sheets created? restart the app once):", e)
    nav = [(h, l, p == h or (h != "/employee" and p.startswith(h + "/")), []) for h, l in items]
    if session.get("role") == "admin":      # Update66: Employee Info expands to Employees / Notifications / Mahizhchi
        view = request.args.get("view", "")
        kids = [("/admin/employee-info", "Employees", p.startswith("/admin/employee-info") and view != "notifications"),
                ("/admin/employee-info?view=notifications", "Notifications", p == "/admin/employee-info" and view == "notifications"),
                ("/admin/mahizhchi", "Mahizhchi", p.startswith("/admin/mahizhchi"))]
        nav = [(h, l, on or any(k[2] for k in kids), kids) if h == "/admin/employee-info" else (h, l, on, [])
               for h, l, on, _k in nav]
        # Update103: Productivity Log / Leave & Permission Log / Audit Log / Email Controls are grouped under one expandable "Log" menu.
        # Every URL is unchanged - only the sidebar grouping changed. Overview, Processes and Employee Info stay as main menu items.
        LOG_KIDS = [("/admin/log", "Productivity Log"), ("/admin/leave-permission", "Leave & Permission Log"),
                    ("/admin/audit", "Audit Log"), ("/admin/email-controls", "Email Controls")]
        def _on(h): return p == h or p.startswith(h + "/")
        log_kids = [(h, l, _on(h)) for h, l in LOG_KIDS]
        by_h = {n[0]: n for n in nav}
        nav = [by_h["/admin/summary"], by_h["/admin/processes"],
               ("/admin/log", "Log", any(k[2] for k in log_kids), log_kids),
               by_h["/admin/employee-info"]]
    side_avatar = ""
    if session.get("role") == "admin":
        side_avatar = ADMIN_AVATAR
    elif session.get("role") == "employee":
        # Update127: 3D animated avatar of the signed-in employee (gender from the Employees sheet, looked up once per request, cached)
        try:
            _g = gender_of(my_emp_row())
        except Exception:
            _g = ""
        side_avatar = render_fast(AVATAR3D, gender=_g, initials=initials_of(session.get("name", "")))
    return render_fast(BASE, body=render_fast(body, **ctx), title=title, nav=nav,
                                  side_avatar=side_avatar, bare=bool(ctx.get("bare")))


LOGIN = """<div class="win {{role}}"><div class="wbar"><i></i><i></i><i></i></div>
<div class="wbody"><div class="scene {{role}}" aria-hidden="true"><div class="sheen"></div>
<div class="gfw"><div class="gf"></div></div>
<div class="fl" style="left:5%;top:12%;--s:62px;--bt:8s"><div class="cube" style="--s:62px;--t:18s"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
<div class="fl" style="right:6%;top:9%;--s:46px;--bt:6.5s;--d:-2s"><div class="cube" style="--s:46px;--t:13s"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
<div class="fl hm" style="right:9%;bottom:14%;--s:74px;--bt:9s;--d:-4s"><div class="cube" style="--s:74px;--t:22s"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
<div class="fl" style="left:8%;bottom:10%;--bt:7.5s;--d:-1s"><div class="ring3d" style="--s:84px;--t:11s"></div></div>
<div class="fl hm" style="right:24%;top:5%;--bt:9s;--d:-3s"><div class="ring3d" style="--s:54px;--t:8s"></div></div>
<div class="fl" style="left:22%;top:6%;--bt:6s;--d:-2.5s"><div class="sph" style="--s:26px"></div></div>
<div class="fl hm" style="right:5%;top:46%;--bt:7s;--d:-1.5s"><div class="sph" style="--s:34px"></div></div>
<div class="fl hm" style="left:4%;top:48%;--bt:8s;--d:-5s"><div class="sph" style="--s:20px"></div></div>{% if role=='admin' %}<div class="dp adm"><div class="dp-lab"><b>&#9664;&#9664;&#9664;</b>&nbsp; LIVE DATA FEED &middot; INCOMING FROM SERVER</div><div class="dp-node l"><div class="dp-dash"><i></i><i></i><i></i><i></i></div><div class="dp-stand"></div><small>ADMIN DASHBOARD</small></div><div class="dp-node r"><div class="dp-rack"><i></i><i></i><i></i></div><small>SERVER</small></div><div class="dp-lane" style="--y:26%"><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i></div><div class="dp-lane" style="--y:50%"><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i></div><div class="dp-lane" style="--y:74%"><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i></div></div>{% else %}<div class="dp emp"><div class="dp-lab">UPLOADING ENCRYPTED DATA TO SERVER &nbsp;<b>&#9654;&#9654;&#9654;</b></div><div class="dp-node l"><div class="dp-scr"><i></i><i></i><i></i></div><div class="dp-stand"></div><small>EMPLOYEE</small></div><div class="dp-node r"><div class="dp-rack"><i></i><i></i><i></i></div><small>SERVER</small></div><div class="dp-lane" style="--y:26%"><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i></div><div class="dp-lane" style="--y:50%"><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i></div><div class="dp-lane" style="--y:74%"><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i><i class="dp-pk"></i></div></div>{% endif %}</div>
{% if role=='admin' %}<div class="adp"><div class="adp-body" aria-hidden="true"><p class="adp-t">Admin Panel</p><h3>Productivity<br>Dashboard</h3><p class="adp-s">Monitor attendance, tasks and team performance in one place.</p><div class="adp-3d"><div class="adp-st"><div class="adp-c c1"><small>Performance</small><div class="adp-bars"><i style="height:38%"></i><i style="height:62%"></i><i style="height:48%"></i><i style="height:80%"></i><i style="height:58%"></i><i style="height:92%"></i><i style="height:70%"></i></div></div><div class="adp-c c2"><small>Attendance</small><div class="adp-ring"></div></div><div class="adp-c c3"><small>Reports</small><div class="adp-ln"></div><div class="adp-ln s"></div></div></div></div></div></div>{% endif %}{% if role=='employee' %}<div class="rb" style="left:14%;top:56%;width:54px;height:54px;--d:-3s"></div><div class="rb hm" style="right:16%;top:14%;width:70px;height:40px;animation-delay:-6s"></div><div class="rb" style="right:8%;bottom:12%;width:44px;height:44px;animation-delay:-9s"></div>{% endif %}<div class="lcard">{% if role=='admin' %}<div class="lcard-top"><div class="lav">{{admin_avatar|safe}}</div><img class="lcard-logo" src="/logo.png" alt="Mobius Technologies and Services" width="190" height="99"></div>{% else %}<img class="lcard-logo" src="/logo.png" alt="Mobius Technologies and Services" width="190" height="99">{% endif %}<h2>Welcome back</h2><p>{{title}}</p>
<form method="post">
<div class="field"><input id="login_u" name="u" placeholder="{{ph}}" required autofocus autocomplete="off"></div>
<div class="field pw"><input id="login_p" name="p" type="password" placeholder="Password" required autocomplete="off">
<button type="button" class="pw-toggle" id="pw_toggle" aria-pressed="false" aria-label="Show password" title="Show password">
<svg class="eye" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>
<svg class="eye-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.9 17.9A10.9 10.9 0 0 1 12 19c-7 0-11-7-11-7a19.8 19.8 0 0 1 5.1-5.9M9.9 4.2A10.6 10.6 0 0 1 12 5c7 0 11 7 11 7a19.7 19.7 0 0 1-3.2 4.2M14.1 14.1a3 3 0 1 1-4.2-4.2"/><path d="M1 1l22 22"/></svg>
<span class="pw-t">Show</span></button></div>
<button>Log in</button></form>{% if role!='admin' %}<span class="fgt" title="Please contact your admin to reset your password">Forgot password?</span>{% endif %}</div></div>{% if role!='admin' %}<img class="orb" src="/photo/{{role}}" alt="">{% endif %}</div>
<script>
(function(){
  var u = document.getElementById('login_u'), p = document.getElementById('login_p');
  var w = document.querySelector('.win'), lg = document.querySelector('.lg');
  if (w && lg && window.matchMedia('(hover:hover) and (pointer:fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion:reduce)').matches) {
    var raf = 0, rx = 0, ry = 0;
    lg.addEventListener('mousemove', function(e){
      var r = lg.getBoundingClientRect();
      ry = ((e.clientX - r.left) / r.width - .5) * 10;
      rx = -((e.clientY - r.top) / r.height - .5) * 8;
      if (!raf) raf = requestAnimationFrame(function(){
        raf = 0; w.style.setProperty('--rx', rx.toFixed(2) + 'deg'); w.style.setProperty('--ry', ry.toFixed(2) + 'deg');
      });
    }, {passive: true});
    lg.addEventListener('mouseleave', function(){ w.style.setProperty('--rx', '0deg'); w.style.setProperty('--ry', '0deg'); });
  }
  var fm = document.querySelector('form'), sc = document.querySelector('.scene');
  if (fm) fm.addEventListener('submit', function(){
    if (sc) sc.classList.add('dp-paused');                       /* stop the decorative animation while the browser signs in */
    var b = fm.querySelector('button:not([type=button])');
    if (b) setTimeout(function(){ b.disabled = true }, 0);       /* one click = one sign-in */
  });
  window.addEventListener('pageshow', function(e){               /* back button: make the form usable again */
    if (!e.persisted || !fm) return;
    var b = fm.querySelector('button:not([type=button])'); if (b) b.disabled = false;
    if (sc) sc.classList.remove('dp-paused');
  });
  document.addEventListener('visibilitychange', function(){ if (sc) sc.classList.toggle('dp-paused', document.hidden) });
  var tg = document.getElementById('pw_toggle');
  if (tg && p) {
    tg.addEventListener('mousedown', function(e){ e.preventDefault(); });   // keep focus/caret in the password box
    tg.addEventListener('click', function(){
      var show = p.type === 'password';
      p.type = show ? 'text' : 'password';
      tg.setAttribute('aria-pressed', show ? 'true' : 'false');
      tg.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
      tg.title = show ? 'Hide password' : 'Show password';
      tg.querySelector('.pw-t').textContent = show ? 'Hide' : 'Show';
      p.focus();
    });
  }
})();
</script>
"""

TABLE = """<div class="card"><h2>{{title}}</h2>
<form method="post" class="grid">{% for h in heads %}{% if h not in locked %}<input name="f{{loop.index0}}" placeholder="{{h}}{% if h=='Target count / hour' %} (count in 1 hr, e.g. 1000){% endif %}"{% if h not in optional %} required{% endif %}>{% endif %}{% endfor %}
<button class="primary">Add</button></form>
{% if kind=='processes' %}<p class="mut">Set the <b>Target count / hour</b> &mdash; the count to complete in 1 hour (e.g. <b>1000 / 1</b> hr). The target for an entry is worked out automatically from the hours the employee logs: 8 hrs &rarr; 8 &times; the hourly count, 4 hrs &rarr; 4 &times;, 2 hrs &rarr; 2 &times;. If the employee's count is below that target, they get an alert.</p>{% endif %}
{% if missing %}<p class="mut">&#9888; {{missing}} employee(s) have no Designation yet. Use Edit to set it; it then fills in automatically on their daily entry page.</p>{% endif %}
{% if locked %}<p class="mut">Personal details are managed on the Personal details page. Office Email ID follows the login Email.</p>{% endif %}</div>
<table><tr>{% for h in heads %}<th>{{h}}</th>{% endfor %}{% if kind=='employees' %}<th>Status</th>{% endif %}<th></th></tr>
{% for r in data %}<tr>{% for h in heads %}<td>{{r[h]}}{% if h=='Target count / hour' and r[h] %} / 1{% endif %}</td>{% endfor %}
{% if kind=='employees' %}{% set lk = (r['Account locked']|string|lower) in ['yes','y','true','locked','1'] %}<td>{% if lk %}<span class="pill" style="background:#fde8e8;color:#b42318">Locked</span>{% else %}<span class="pill" style="background:#e6f6ec;color:#15803d">Active</span>{% endif %}</td>{% endif %}
<td class="act"><a href="/admin/{{kind}}/{{r['_row']}}">Edit</a>
{% if kind=='employees' %}<form method="post" action="/admin/employees/{{r['_row']}}/lock"><input type="hidden" name="eid" value="{{r['Employee ID']}}"><input type="hidden" name="do" value="{{'unlock' if lk else 'lock'}}"><button class="back sm" type="submit">{{'Unlock' if lk else 'Lock'}}</button></form>
<form method="post" action="/admin/employees/{{r['_row']}}/reset-password" onsubmit="var p=prompt('New password for {{r['Employee ID']}} (leave empty to generate one):','');if(p===null)return false;this.newpw.value=p;return true"><input type="hidden" name="eid" value="{{r['Employee ID']}}"><input type="hidden" name="newpw" value=""><button class="back sm" type="submit">Reset password</button></form>
<form method="post" action="/admin/employees/{{r['_row']}}/delete" onsubmit="return confirm('Permanently delete the account of {{r['Employee ID']}}? Their login is removed. Their past productivity entries stay in the log.')"><input type="hidden" name="eid" value="{{r['Employee ID']}}"><button class="danger">Delete</button></form>
{% else %}<form method="post" action="/admin/{{kind}}/{{r['_row']}}/delete" onsubmit="return confirm('Delete?')"><button class="danger">Delete</button></form>{% endif %}</td></tr>
{% else %}<tr><td colspan="9">No records yet.</td></tr>{% endfor %}</table>"""

EDIT = """<div class="card"><h2>Edit {{title}}</h2>{% if kind=='processes' %}<p class="mut">Set the <b>Target count / hour</b> &mdash; the count to complete in 1 hour (e.g. <b>1000 / 1</b> hr). The target for an entry is worked out automatically from the hours the employee logs: 8 hrs &rarr; 8 &times; the hourly count, 4 hrs &rarr; 4 &times;, 2 hrs &rarr; 2 &times;. If the employee's count is below that target, they get an alert.</p>{% endif %}<form method="post" class="grid">
{% for h in heads %}<label>{{h}}<input name="f{{loop.index0}}" value="{{vals[loop.index0]}}"{% if h not in optional %} required{% endif %}{% if h in locked %} readonly{% endif %}></label>{% endfor %}
<button class="primary sm">Save</button> <button type="button" class="back sm" onclick="if(history.length>1)history.back();else location.href='/admin/{{kind}}'">Back</button></form>
{% if locked %}<p class="mut">Personal details (grayed out) are entered by the employee on their own Personal details page.</p>{% endif %}</div>"""

# Update94: 3-second flower animation on the Employee page when the day just saved reached 100% (target + working hours)
BLOOM = """{% if bloom %}<style>
#bloom{position:fixed;inset:0;z-index:99999;pointer-events:none;overflow:hidden}
#bloom span{position:absolute;top:-12%;animation:bloomfall 3s ease-in forwards;opacity:0;will-change:transform}
@keyframes bloomfall{0%{transform:translateY(0) rotate(0);opacity:0}10%{opacity:1}85%{opacity:1}100%{transform:translateY(125vh) rotate(360deg);opacity:0}}
#bloom b{position:absolute;left:0;right:0;top:38%;text-align:center;font-size:2.2em;color:#be185d;text-shadow:0 2px 8px #fff;animation:bloomfade 3s ease forwards}
@keyframes bloomfade{0%{opacity:0;transform:scale(.6)}20%{opacity:1;transform:scale(1)}80%{opacity:1}100%{opacity:0}}
</style><div id="bloom" aria-hidden="true"><b>&#127800; 100% Target Achieved! &#127802;</b></div>
<script>(function(){var e=['\uD83C\uDF38','\uD83C\uDF3C','\uD83C\uDF3A','\uD83C\uDF37','\uD83C\uDF3B'],b=document.getElementById('bloom');if(!b)return;
for(var i=0;i<46;i++){var p=document.createElement('span');p.textContent=e[i%e.length];p.style.left=(Math.random()*96)+'%';p.style.fontSize=(22+Math.random()*26)+'px';p.style.animationDelay=(Math.random()*0.9)+'s';p.style.animationDuration=(1.9+Math.random()*1.0)+'s';b.appendChild(p)}
setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b)},3000)})();</script>{% endif %}"""

SAVED_ANIM = """{% if saved_anim %}<style>
#svwrap{position:fixed;inset:0;z-index:100000;pointer-events:none;display:flex;justify-content:center;align-items:flex-start;padding-top:12vh;perspective:900px;animation:svwrap 3s linear forwards}
@keyframes svwrap{0%,88%{opacity:1}100%{opacity:0}}
#svcard{position:relative;transform-style:preserve-3d;display:flex;align-items:center;gap:14px;padding:16px 26px 16px 18px;border-radius:16px;color:#fff;background:linear-gradient(135deg,#16a34a,#22c55e 55%,#4ade80);box-shadow:0 1px 0 #ffffff66 inset,0 8px 0 #166534,0 26px 40px -10px #14532d99;animation:svcard 3s cubic-bezier(.22,1,.36,1) forwards;will-change:transform}
@keyframes svcard{0%{transform:rotateX(-70deg) rotateY(-90deg) translateZ(-300px) scale(.4);opacity:0}18%{transform:rotateX(12deg) rotateY(10deg) translateZ(40px) scale(1.04);opacity:1}30%{transform:rotateX(0) rotateY(0) translateZ(0) scale(1)}55%{transform:rotateX(4deg) rotateY(-6deg) translateZ(10px) scale(1)}80%{transform:rotateX(0) rotateY(0) translateZ(0) scale(1);opacity:1}100%{transform:rotateX(60deg) rotateY(90deg) translateZ(-260px) scale(.5);opacity:0}}
#svcoin{width:48px;height:48px;border-radius:50%;background:#fff;color:#16a34a;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;box-shadow:0 4px 0 #bbf7d0,0 8px 14px #0003;transform-style:preserve-3d;animation:svspin 1.2s .25s ease-in-out 2 both}
@keyframes svspin{from{transform:rotateY(0)}to{transform:rotateY(360deg)}}
#svcard b{display:block;font-size:17px;letter-spacing:.2px;text-shadow:0 2px 0 #14532d66}
#svcard small{display:block;font-size:12.5px;opacity:.92;margin-top:2px}
#svcard::after{content:"";position:absolute;inset:0;border-radius:16px;background:linear-gradient(100deg,transparent 30%,#ffffff66 50%,transparent 70%);transform:translateX(-120%);animation:svshine 1.1s .5s ease forwards;pointer-events:none}
@keyframes svshine{to{transform:translateX(120%)}}
@media (prefers-reduced-motion:reduce){ #svcard,#svcoin,#svcard::after{animation-duration:3s} }
</style><div id="svwrap" role="status" aria-live="polite"><div id="svcard"><div id="svcoin">&#10003;</div><div><b>Saved successfully!</b><small>Your daily productivity entry is saved.</small></div></div></div>
<script>setTimeout(function(){var w=document.getElementById('svwrap');if(w&&w.parentNode)w.parentNode.removeChild(w)},3000);</script>{% endif %}"""

LIST = """<table><tr><th>Date</th>{% if session.role=='admin' %}<th>Employee</th><th>Designation</th>{% endif %}
<th>Productive hrs</th><th>Non-productive hrs</th><th>Total</th><th>Target count</th><th>Completed</th><th>Target status</th><th>Productivity</th><th></th></tr>
{% for s in subs %}<tr><td>{{s.date}}</td>{% if session.role=='admin' %}<td>{{s.emp_id}} &middot; {{s.emp_name}}</td><td>{{s.designation}}</td>{% endif %}
<td>{{s.prod|g}}</td><td>{{s.non|g}}</td><td>{{s.total|g}}</td>
<td>{{ (s.tgt_total|cnt) if s.tgt_state in ('met','miss') else '-' }}</td><td>{{ (s.cnt_total|cnt) if s.tgt_state in ('met','miss') else '-' }}</td>
<td>{% if s.tgt_state=='met' %}<span class="tg-badge met">&#9989; Achieved</span>{% elif s.tgt_state=='miss' %}<span class="tg-badge miss" title="Below target: {{s.tgt_miss|join(', ')}}">&#10060; Not Achieved</span>{% else %}-{% endif %}</td>
<td>{{ 'Weekend - not counted' if s.off else (s.pct ~ '%') }}</td>
<td class="act"><a href="/entry/{{s.id}}/view{{ ('?next=' ~ (nxt|urlencode)) if nxt else '' }}">View</a><a href="/entry/{{s.id}}{{ ('?next=' ~ (nxt|urlencode)) if nxt else '' }}">Edit</a>
<form method="post" action="/entry/{{s.id}}/delete{{ ('?next=' ~ (nxt|urlencode)) if nxt else '' }}" onsubmit="return confirm('Delete this entry?')"><button class="danger">Delete</button></form></td></tr>
{% else %}<tr><td colspan="{{ 10 if session.role=='admin' else 8 }}">{{ empty_msg or 'Nothing yet.' }}</td></tr>{% endfor %}</table>"""

FORM = """<div class="card" id="entryCard"><h2>{{heading}} <span id="tgtBadge"></span></h2>
<form method="post" action="{{action}}">
<div class="grid">
<label>Date<input type="date" name="date" value="{{sub.date}}" {% if maxdate %}max="{{maxdate}}"{% endif %}{% if mindate %} min="{{mindate}}"{% endif %} required></label>
<label>Designation<input value="{{sub.designation}}" placeholder="Not set - ask admin" readonly></label>
<label>Band<input value="{{sub.band}}" readonly></label>
<label>Employee ID<input value="{{sub.emp_id}}" readonly></label>
<label>Employee name<input value="{{sub.emp_name}}" readonly></label></div>
<h3>Process entries <span class="mut">(all fields required)</span></h3><div id="procs"></div>
<button type="button" onclick="addProc()">+ Add process</button>
<h3>Notes</h3><div id="notes"></div>
<button type="button" onclick="addNote()">+ Add note</button>
<div class="totals">Total day: <b>{{day|g}}</b> hrs &middot; Productive: <b id="tp">0</b> hrs &middot;
Non-productive: <b id="tn">0</b> hrs &middot; Balance: <b id="tb">{{day|g}}</b> hrs &middot;
Productivity: <b id="tpct">0</b>% &middot; <b id="tstat"></b> <span class="mut">({{target|g}} productive hrs = 100%, target set by Admin)</span></div>
<div id="tgtMsg" class="flash err" style="display:none" role="alert"></div>
<div id="formerr" class="flash err" style="display:none" role="alert"></div>
<button class="primary sm">Save</button> {% if heading == 'Daily productivity entry' %}<button type="button" class="back sm" onclick="event.preventDefault();window.scrollTo({top:0,behavior:'smooth'});var d=document.querySelector('#entryCard [name=date]');if(d)d.focus({preventScroll:true});return false">Back</button>{% else %}<button type="button" class="back sm" onclick="if(history.length>1)history.back();else location.href='{{ '/admin/summary' if session.role=='admin' else '/employee' }}'">Back</button>{% endif %}</form></div>
<script>
const WORK={{workday|g}}, PERM={{perm|tojson}}, MAXD={{maxdate|tojson}};
const P={{names|tojson}}, T={{tph|tojson}}, DAY={{day|g}}, TGT={{target|g}}, OTHER_H={{other_hours|g}};
const isOther=v=>['other','others'].includes(String(v==null?'':v).trim().toLowerCase()), isPoc=v=>String(v==null?'':v).trim().toLowerCase().replace(/ /g,'_')==='poc_sample', isGenai=v=>String(v==null?'':v).trim().toLowerCase().replace(/[ _-]/g,'')==='genai', isTrain=v=>String(v==null?'':v).trim().toLowerCase()==='training';
const effH=(nm,h)=>h;      // Update96: hours are exactly what the employee typed
function rowH(r){return effH((r.querySelector('[name=pn]')||{}).value,+((r.querySelector('[name=ph]')||{}).value)||0)}
function otherUI(r){const pv=(r.querySelector('[name=pn]')||{}).value,o=isOther(pv),pc_=isPoc(pv),ga_=isGenai(pv),tr=isTrain(pv)||o||pc_||ga_,d=r.querySelector('[name=pd]'),c=r.querySelector('[name=pc]');if(!d)return;
 let n=r.querySelector('.oth-note');
 if(c){if(tr){c.type='hidden';c.required=false;c.value='0'}else{if(c.type==='hidden'){c.type='number';c.value=''}c.required=true}}      // Training: Count is not shown / not required
 if(o||pc_||ga_||tr){d.placeholder=isTrain(pv)?'Training details *':'Description of the work done *';d.size=48;d.style.minWidth='320px';
  if(!n){n=document.createElement('div');n.className='oth-note mut';n.style.cssText='flex-basis:100%;font-size:.85em;color:#b45309';r.insertBefore(n,r.querySelector('button.danger'))}
  n.textContent=ga_?'"GenAI": enter the Hours and a Description only - no Count is needed.':pc_?'"POC_Sample": enter the Hours and a Description only - no Count is needed.':o?'"Other": enter the Hours and the work details in Description - no Count is needed. The hours you enter are counted as productive hours.':'"Training": enter the Hours and a Description only - no Count is needed. Productivity is calculated from the hours entered.'}
 else{d.placeholder='Description *';d.size=28;d.style.minWidth='';if(n)n.remove()}}
const E=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function row(h){const d=document.createElement('div');d.className='r';
 d.innerHTML=h+'<button type="button" class="danger" onclick="this.parentNode.remove();calc()">X</button>';return d}
function addProc(p){p=p||{};const _r=row(
 '<select name="pn" required onchange="otherUI(this.parentNode);calc()">'+P.map(n=>'<option '+(n==p.name?'selected':'')+'>'+E(n)+'</option>').join('')+'</select>'+
 '<input name="ph" type="number" step="0.25" min="0.25" required placeholder="Hour *" value="'+(p.hour||'')+'" oninput="calc()">'+
 '<input name="pc" type="number" min="0" required placeholder="Count *" value="'+(p.count||'')+'" oninput="calc()">'+
 '<input name="pd" required placeholder="Description *" size="28" value="'+E(p.desc)+'">');
 document.getElementById('procs').appendChild(_r);otherUI(_r);calc()}
function addNote(n){n=n||{};document.getElementById('notes').appendChild(row(
 '<input name="nd" placeholder="Description" size="30" value="'+E(n.desc)+'">'+
 '<input name="nh" type="number" step="0.25" min="0" placeholder="Hour" value="'+(n.hour||'')+'" oninput="calc()">'));calc()}
function reqHrs(){const d=document.querySelector('[name=date]').value;return Math.max(WORK-(PERM[d]||0),0)}
function calc(){const s=q=>[...document.querySelectorAll(q)].reduce((a,e)=>a+(+e.value||0),0);
 const p=[...document.querySelectorAll('#procs .r')].reduce((a,r)=>a+rowH(r),0),n=s('[name=nh]'),b=DAY-p-n;
 tp.textContent=p;tn.textContent=n;tb.textContent=b;tb.style.color=b<0?'red':'';
 tpct.textContent=Math.min(Math.round(p/TGT*100),100);
 const r=reqHrs(),left=Math.round((r-p-n)*100)/100;
 tstat.textContent=left>0?('Required '+r+' hrs - '+left+' hrs remaining'):('Required '+r+' hrs - complete');
 tstat.style.color=left>0?'#b45309':'#15803d';
 const prows=[...document.querySelectorAll('#procs .r')];                 // Target Count/Hour check (Admin-set, per process)
 const met=prows.length>0 && prows.every(row=>{
  const rate=T[(row.querySelector('[name=pn]')||{}).value]||0;
  const hr=rowH(row);
  const ct=+((row.querySelector('[name=pc]')||{}).value)||0;
  const need=rate*hr;
  return need<=0 || ct>=need;                                             // no target set for that process = counted as met
 });
 entryCard.classList.toggle('tgt-met',met);
 entryCard.classList.toggle('tgt-miss',!met);
 tgtBadge.textContent=met?'Target: Met':'Target: Not met';
 tgtBadge.className=met?'met':'miss';
 const low=[];prows.forEach(row=>{const nm=(row.querySelector('[name=pn]')||{}).value,rate=T[nm]||0,hr=rowH(row),ct=+((row.querySelector('[name=pc]')||{}).value)||0,need=rate*hr;
  if(need>0&&ct<need)low.push(nm+': '+ct+' of '+Math.round(need*100)/100)});
 tgtMsg.textContent=low.length?('⚠ Target not achieved (count per hour × hours worked) – '+low.join(' | ')):'';tgtMsg.style.display=low.length?'block':'none'}
document.querySelector('[name=date]').addEventListener('change',calc);
function showErr(m){formerr.textContent=m;formerr.style.display='block';formerr.scrollIntoView({behavior:'smooth',block:'center'})}
document.querySelector('form[action="{{action}}"]').addEventListener('submit',function(e){
 formerr.style.display='none';
 const d=document.querySelector('[name=date]').value;
 if(MAXD&&d>MAXD){e.preventDefault();return showErr('Future dates are not allowed. Choose today or an earlier date.')}
 if(!document.querySelector('[name=pn]')){e.preventDefault();return showErr('Add at least one process entry.')}
 const bad=[...document.querySelectorAll('#procs [name]')].some(x=>!String(x.value).trim());
 if(bad){e.preventDefault();return showErr('All Process Entry fields are mandatory - fill every field before saving.')}
 const t=[...document.querySelectorAll('#procs .r')].reduce((a,r2)=>a+rowH(r2),0)+[...document.querySelectorAll('[name=nh]')].reduce((a,x)=>a+(+x.value||0),0),r=reqHrs();
 if(t+1e-9<r){e.preventDefault();showErr('Entry incomplete: '+t+' of the required '+r+' working hours logged. Complete all '+r+' hours before saving.')}
 if(!e.defaultPrevented){const b=e.target.querySelector('button.primary');if(b){setTimeout(function(){b.disabled=true;b.textContent='Saving...'},0)}}      /* Update96: one click = one save (no double submit) */
});
window.addEventListener('pageshow',function(){const b=document.querySelector('form button.primary[disabled]');if(b){b.disabled=false;b.textContent='Save'}});
{{sub.procs|tojson}}.forEach(addProc);{{sub.notes|tojson}}.forEach(addNote);
</script>"""

VIEW = """<div class="card"><h2>{{s.date}} &middot; {{s.emp_name}} ({{s.emp_id}}{% if s.designation %}, {{s.designation}}{% endif %}, Band {{s.band}})</h2>
<table><tr><th>Process</th><th>Description</th><th>Hour</th><th>Count</th><th>Target count</th><th>Achievement</th></tr>
{% for p in s.procs %}<tr><td>{{p.name}}</td><td>{{p.desc}}</td><td>{{p.hour|g}}</td><td>{{ '-' if p.training else (p.count|g) }}</td><td>{{ '-' if p.training else (p.target|g) }}</td>
<td>{{ (p.pct ~ '%') if p.pct is not none else '-' }}</td></tr>{% endfor %}</table><br>
<table><tr><th>Notes</th><th>Hour</th></tr>{% for n in s.notes %}<tr><td>{{n.desc}}</td><td>{{n.hour|g}}</td></tr>{% endfor %}</table>
<div class="totals">Productive: <b>{{s.prod|g}}</b> hrs &middot; Non-productive: <b>{{s.non|g}}</b> hrs &middot; Total: <b>{{s.total|g}}</b> / {{day|g}} hrs &middot; {% if s.off %}<b>Weekend entry - not counted</b>{% else %}Productivity: <b>{{s.pct}}%</b> ({{s.avail|g}} hrs = 100%{% if s.ded %} &ndash; {{target|g}}-hr day less {{s.ded|g}} hr permission / half-day leave{% endif %}){% endif %}</div>
<a href="{{back}}">Back</a></div>"""

# ---------------------------------------------------------------- routes: common
_photo_cache = {}
@app.route("/photo/<role>")
def photo(role):
    import base64, hashlib
    from flask import Response
    if role not in PHOTOS: abort(404)
    if role not in _photo_cache:                                 # decode + hash once, not on every request
        _d = base64.b64decode(PHOTOS[role].split(",", 1)[1])
        _photo_cache[role] = (_d, hashlib.md5(_d).hexdigest())  # etag changes automatically if the photo changes
    data, etag = _photo_cache[role]
    if request.headers.get("If-None-Match") == etag:
        return Response(status=304)
    resp = Response(data, mimetype="image/jpeg")
    resp.headers["Cache-Control"] = "public, max-age=604800, immutable"   # cache for 7 days on slow connections
    resp.headers["ETag"] = etag
    return resp

@app.route("/employee_corner.png")
def employee_corner():
    import base64
    data = base64.b64decode(EMP_CORNER_B64)
    resp = Response(data, mimetype="image/png")
    resp.headers["Cache-Control"] = "public, max-age=604800"
    return resp

@app.route("/logo.png")
def company_logo():
    import base64
    data = base64.b64decode(LOGO_PNG_B64)
    resp = Response(data, mimetype="image/png")
    resp.headers["Cache-Control"] = "public, max-age=604800"
    return resp

@app.route("/")
def index():
    return page('<div class="card login"><h2>Productivity Tracker</h2>'
                '<p><a href="/employee/login">Employee login</a></p>'
                '<p><a href="/admin/login">Admin login</a></p></div>')

@app.route("/logout")
def logout():
    r = session.get("role")
    track_logout()
    session.clear()
    return redirect("/admin/login" if r == "admin" else "/employee/login")

# ---------------------------------------------------------------- admin
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("role") == "employee":               # employees never get the Admin login page
        return _wrong_area("admin")
    if request.method == "POST":
        if eq(request.form["u"], ADMIN_USER) and eq(request.form["p"], ADMIN_PASS):
            track_logout(auto=True, reason="New login")      # closes a previous session in this browser, if any
            session.clear(); session.update(role="admin", name="Admin")
            track_login("ADMIN", "Admin", "-")
            _bg(prefetch, "Employees", "Productivity log", "Processes", "Leave", "Permissions", "Settings", "Holidays")   # Update114: dashboard data loads while the welcome animation plays
            return redirect("/admin/welcome")
        flash("Wrong username or password.")
    return page(LOGIN, title="Admin login", ph="Admin username", role="admin",
                admin_avatar=render_fast(AVATAR3D, gender="male", initials="A"))

@app.route("/admin")
@need("admin")
def admin_home(): return redirect("/admin/summary")


def _acct_back():
    b = (request.form.get("back") or "").strip()
    return b if (b.startswith("/admin/employee-info") and "//" not in b and "\\" not in b and "\n" not in b and "\r" not in b) else "/admin/employees"

def _admin_emp(row, eid):
    """Re-read the row and make sure it still belongs to the employee the Admin clicked on."""
    heads = HEADERS["Employees"]; cur = ws_of("Employees").row_values(row); cur += [""] * (len(heads) - len(cur))
    return cur if _key(cur[heads.index("Employee ID")]) == _key(eid) else None

@app.route("/admin/employees/<int:row>/lock", methods=["POST"])
@need("admin")
def admin_emp_lock(row):
    eid = request.form.get("eid", ""); lock = request.form.get("do") == "lock"
    if _admin_emp(row, eid) is None:
        flash("That employee changed - please refresh and try again.", "error"); return redirect(_acct_back())
    set_employee_cell(row, eid, "Account locked", "Yes" if lock else "")
    try: log_change("Employees", "Locked" if lock else "Unlocked", f"Employee ID {eid}")
    except Exception as ex: print("log_change failed:", ex)
    flash(f"Account {eid} {'locked - this employee can no longer log in.' if lock else 'unlocked - this employee can log in again.'}")
    return redirect(_acct_back())

@app.route("/admin/employees/<int:row>/reset-password", methods=["POST"])
@need("admin")
def admin_emp_reset(row):
    eid = request.form.get("eid", ""); new = request.form.get("newpw", "").strip() or temp_password()
    if len(new) < 4:
        flash("The password must be at least 4 characters.", "error"); return redirect(_acct_back())
    if _admin_emp(row, eid) is None:
        flash("That employee changed - please refresh and try again.", "error"); return redirect(_acct_back())
    set_employee_cell(row, eid, "Password", new)
    try: log_change("Employees", "Password reset", f"Employee ID {eid}")
    except Exception as ex: print("log_change failed:", ex)
    flash(f"New password for {eid}: {new}   (share it with the employee).")
    return redirect(_acct_back())

@app.route("/admin/employees/<int:row>/delete", methods=["POST"])
@need("admin")
def admin_emp_delete(row):
    eid = request.form.get("eid", ""); cur = _admin_emp(row, eid)
    if cur is None:
        flash("That employee changed - please refresh and try again.", "error"); return redirect(_acct_back())
    ws_of("Employees").delete_rows(row); invalidate_cache("Employees")
    try: log_change("Employees", "Deleted", f"Employee ID {eid}")
    except Exception as ex: print("log_change failed:", ex)
    flash(f"Employee account {eid} deleted.")
    return redirect(_acct_back())

@app.route("/admin/<kind>", methods=["GET", "POST"])
@need("admin")
def admin_list(kind):
    sheet = KINDS.get(kind) or abort(404)
    heads = list_heads(sheet)
    if request.method == "POST":
        vals = [request.form.get(f"f{i}", "").strip() for i in range(len(heads))]
        if any(str(r[heads[0]]) == vals[0] for r in rows(sheet)):
            flash(f"{heads[0]} '{vals[0]}' already exists.")
        else:
            full = dict(zip(heads, vals))
            if sheet == "Processes":
                full["Target count / hour"], full["Target count / 8 hrs"], err = proc_targets_sync(
                    full.get("Target count / hour"), full.get("Target count / 8 hrs"))
                if err: flash(err, "error"); return redirect(request.path)
            if sheet == "Employees": full["Office Email ID"] = full.get("Email", "")
            ws_of(sheet).append_row([full.get(h, "") for h in HEADERS[sheet]],
                                               value_input_option="RAW"); invalidate_cache(sheet)
            flash("Added.")
        return redirect(request.path)
    data = rows(sheet)
    if sheet == "Processes":                      # show the hourly figure for processes saved with only the 8-hour column
        tg = process_targets()
        for r in data:
            t = tg.get(r["Process name"])
            if t and t["rate"] > 0:
                if not str(r.get("Target count / hour", "")).strip(): r["Target count / hour"] = _g4(t["rate"])
                if not str(r.get("Target count / 8 hrs", "")).strip(): r["Target count / 8 hrs"] = _g4(t["daily"])
    missing = sum(1 for r in data if not str(r.get("Designation", "x")).strip()) if sheet == "Employees" else 0
    return page(TABLE, title=sheet, heads=heads, data=data, kind=kind, missing=missing,
                optional=OPTIONAL_FIELDS, locked=LOCKED_FIELDS.get(sheet, set()))

@app.route("/admin/<kind>/<int:row>", methods=["GET", "POST"])
@need("admin")
def admin_edit(kind, row):
    sheet = KINDS.get(kind) or abort(404)
    heads = list_heads(sheet); ws = ws_of(sheet)
    if request.method == "POST":
        vals = [request.form.get(f"f{i}", "").strip() for i in range(len(heads))]
        full = ws.row_values(row); full += [""] * (len(HEADERS[sheet]) - len(full)); old = list(full)
        for h, v in zip(heads, vals): full[HEADERS[sheet].index(h)] = v
        if sheet == "Processes":
            ih, idl = HEADERS[sheet].index("Target count / hour"), HEADERS[sheet].index("Target count / 8 hrs")
            full[ih], full[idl], err = proc_targets_sync(full[ih], full[idl], old[ih], old[idl])
            if err: flash(err, "error"); return redirect(request.path)
        if sheet == "Employees":   # office email follows the login email
            full[HEADERS[sheet].index("Office Email ID")] = vals[heads.index("Email")]
        ws.update(range_name=f"A{row}", values=[full], value_input_option="RAW"); invalidate_cache(sheet)
        flash("Updated."); return redirect(f"/admin/{kind}")
    cur = ws.row_values(row); cur += [""] * (len(HEADERS[sheet]) - len(cur))
    vals = [cur[HEADERS[sheet].index(h)] for h in heads]
    if sheet == "Processes":                      # prefill the derived figure so the form never looks empty
        ihv = heads.index("Target count / hour"); dcur = cur[HEADERS[sheet].index("Target count / 8 hrs")]
        h_, d_, _e = proc_targets_sync(vals[ihv], dcur, vals[ihv], dcur)
        if not _e: vals[ihv] = h_
    return page(EDIT, title=sheet, heads=heads, vals=vals, kind=kind,
                optional=OPTIONAL_FIELDS, locked=LOCKED_FIELDS.get(sheet, set()))

@app.route("/admin/<kind>/<int:row>/delete", methods=["POST"])
@need("admin")
def admin_delete(kind, row):
    ws_of(KINDS.get(kind) or abort(404)).delete_rows(row); invalidate_cache(KINDS.get(kind))
    flash("Deleted."); return redirect(f"/admin/{kind}")

LOG_MANAGE = """<div class="card no-print"><h2>Manage employee entries</h2>
<p class="mut">Pick an employee to see their entries (then <b>View / Edit / Delete</b> in the list below), or add a new entry for any date.</p>
<form method="get" class="grid"><label>Employee<select name="emp" required><option value="">- select employee -</option>
{% for e in emp_list %}<option value="{{e['Employee ID']}}" {{'selected' if sel_emp and (sel_emp|upper) == (e['Employee ID']|string|trim|upper) else ''}}>{{e['Employee ID']}} &middot; {{e['Name']}}</option>{% endfor %}</select></label>
<label>Date for new entry<input type="date" name="adate" value="{{request.args.get('adate') or today_str}}"></label>
<div><button class="primary pbtn" type="submit" formaction="/admin/log">Show entries</button>
<button class="primary pbtn" type="submit" formaction="/admin/log/add" style="background:#22a06b">+ Add entry</button></div></form></div>"""

LOG_TOP = """<div class="card"><div class="loghead"><h2>Productivity log</h2>
<details class="exp no-print"><summary class="btnl pbtn">&#128438; Print / Export &#9662;</summary>
<div class="menu">
<a href="/admin/log/report?period=month&print=1&emp={{emp|urlencode}}" target="_blank">&#128438;<span>Print current month report<small>{{month_label}}</small></span></a>
<a href="/admin/log/report?period=week&print=1&emp={{emp|urlencode}}" target="_blank">&#128438;<span>Print weekly report<small>{{week_label}}</small></span></a>
<hr>
<a href="/admin/log/export?period=month&emp={{emp|urlencode}}">&#128196;<span>Download Excel &mdash; current month<small>.xlsx &middot; {{month_label}}</small></span></a>
<a href="/admin/log/export?period=week&emp={{emp|urlencode}}">&#128196;<span>Download Excel &mdash; weekly<small>.xlsx &middot; {{week_label}}</small></span></a>
</div></details></div>
{% if emp %}<p class="mut">Reports below are limited to employee filter: <b>{{emp}}</b></p>{% endif %}
<form class="grid"><label>Date<input type="date" name="date" value="{{request.args.get('date','')}}"></label>
<label>Employee ID / name<input name="emp" value="{{request.args.get('emp','')}}"></label>
<button class="primary pbtn">Filter</button> <a href="/admin/log">Clear</a></form>
<p class="totals no-print">Target check (Admin-set Target Count): <span class="tg-badge met">{{tg_met}} met</span> <span class="tg-badge miss">{{tg_miss}} not met</span>
<span class="mut">&middot; targets are set on the <a href="/admin/processes">Processes</a> page.</span></p></div>"""

def period_range(period, on=None):
    """(start, end, label) for the month or Monday-Sunday week containing `on` (default today)."""
    try: d = dt.date.fromisoformat(on) if on else today_local()
    except ValueError: d = today_local()
    if period == "week":
        st = d - dt.timedelta(days=d.weekday()); en = st + dt.timedelta(days=6)
        return st, en, f"Week {st.strftime('%d %b')} - {en.strftime('%d %b %Y')}"
    st = d.replace(day=1); en = (st.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return st, en, st.strftime("%B %Y")

def log_report_data(period, emp_q="", on=None):
    st, en, label = period_range(period, on)
    q = (emp_q or "").strip().lower()
    subs = [s for s in load_subs() if str(st) <= str(s["date"]) <= str(en)
            and (not q or q in (str(s["emp_id"]).lower(), str(s["emp_name"]).lower()) or q in str(s["emp_name"]).lower())]
    subs.sort(key=lambda s: (s["date"], str(s["emp_name"]).lower()))
    day = lambda d: dt.date.fromisoformat(str(d)).strftime("%a") if str(d)[:4].isdigit() else ""
    summary, detail = [], []
    for s in subs:
        pct = "Weekend - not counted" if s["off"] else s["pct"]
        summary.append([s["date"], day(s["date"]), s["emp_id"], s["emp_name"], s["designation"], s["band"],
                        s["prod"], s["non"], s["total"], pct])
        base = [s["date"], day(s["date"]), s["emp_id"], s["emp_name"], s["designation"], s["band"]]
        for p_ in s["procs"]:
            detail.append(base + ["Process", p_["name"], p_["desc"], p_["hour"], p_["count"], p_["target"],
                                  "" if p_["pct"] is None else p_["pct"]])
        for n_ in s["notes"]:
            detail.append(base + ["Note", n_["desc"], "", n_["hour"], "", "", ""])
    return dict(start=st, end=en, label=label, subs=subs, summary=summary, detail=detail, emp=emp_q)

SUMMARY_HEADS = ["Date", "Day", "Employee ID", "Employee name", "Designation", "Band",
                 "Productive hrs", "Non-productive hrs", "Total hrs", "Productivity %"]
DETAIL_HEADS = ["Date", "Day", "Employee ID", "Employee name", "Designation", "Band", "Type",
                "Process / Note", "Description", "Hours", "Count", "Target count", "Achievement %"]

LOG_REPORT = """<div class="rep-tools no-print"><button type="button" class="btnl pbtn" onclick="window.print()">&#128438; Print</button>
<a class="btnl pbtn" style="background:#22a06b;box-shadow:0 4px 0 #17734d" href="/admin/log/export?period={{period}}&emp={{emp|urlencode}}">&#128196; Download Excel</a>
<a href="/admin/log{% if emp %}?emp={{emp|urlencode}}{% endif %}">&larr; Back to log</a></div>
<h1 class="rep-title">Productivity Log &mdash; {{'Weekly' if period=='week' else 'Monthly'}} report</h1>
<p class="rep-meta">{{label}}{% if emp %} &middot; Employee filter: {{emp}}{% endif %} &middot; Generated {{now}}</p>
<div class="totals">Entries: <b>{{summary|length}}</b> &middot; Productive: <b>{{tp|g}}</b> hrs &middot; Non-productive: <b>{{tn|g}}</b> hrs &middot; Total: <b>{{(tp+tn)|g}}</b> hrs</div>
<h2>Daily summary</h2>
<table><tr>{% for h in sh %}<th>{{h}}</th>{% endfor %}</tr>
{% for r in summary %}<tr>{% for v in r %}<td>{% if loop.index in (7,8,9) %}{{v|g}}{% elif loop.last and v is number %}{{v}}%{% else %}{{v}}{% endif %}</td>{% endfor %}</tr>
{% else %}<tr><td colspan="10">No productivity entries for this period.</td></tr>{% endfor %}</table>
<h2>Entry details</h2>
<table><tr>{% for h in dh %}<th>{{h}}</th>{% endfor %}</tr>
{% for r in detail %}<tr>{% for v in r %}<td>{% if loop.index in (10,11,12) and v != '' %}{{v|g}}{% elif loop.last and v != '' %}{{v}}%{% else %}{{v}}{% endif %}</td>{% endfor %}</tr>
{% else %}<tr><td colspan="13">No details for this period.</td></tr>{% endfor %}</table>
{% if autoprint %}<script>window.addEventListener('load',function(){setTimeout(function(){window.print()},350)})</script>{% endif %}"""

@app.route("/admin/log")
@need("admin")
def admin_log():
    d, e = request.args.get("date", ""), request.args.get("emp", "").strip().lower()
    subs = [s for s in load_subs() if (not d or s["date"] == d) and
            (not e or e in (str(s["emp_id"]).lower(), str(s["emp_name"]).lower()))]
    emp_list = sorted(rows("Employees"), key=lambda x: str(x.get("Name", "")).lower())
    return page(LOG_MANAGE + LOG_TOP + LIST + LOG_MISSED, title="Productivity log", subs=subs, emp=request.args.get("emp", "").strip(), **log_missed_section(),
                emp_list=emp_list, sel_emp=request.args.get("emp", "").strip(), today_str=str(today_local()),
                nxt=request.full_path.rstrip("?"),
                tg_met=sum(1 for s in subs if s["tgt_state"] == "met"), tg_miss=sum(1 for s in subs if s["tgt_state"] == "miss"),
                month_label=period_range("month")[2], week_label=period_range("week")[2])

@app.route("/admin/log/add", methods=["GET", "POST"])
@need("admin")
def admin_log_add():
    """Update103: Admin adds a Daily Productivity Entry for any employee on any date (same form + same validation as the employee's)."""
    eid = (request.values.get("emp") or "").strip()
    e = next((e for e in rows("Employees") if _key(e.get("Employee ID", "")) == _key(eid)), None) if eid else None
    if not e:
        flash("Please select an employee first.", "error"); return redirect("/admin/log")
    emp_id, name, band = str(e["Employee ID"]).strip(), str(e.get("Name", "")), str(e.get("Band", ""))
    if is_view_only(emp_id):                                         # Update105
        flash(f"{name} has a View Only designation - productivity entries cannot be added.", "error"); return redirect("/admin/log")
    action = "/admin/log/add?emp=" + urllib.parse.quote(emp_id, safe="")
    if request.method == "POST":
        try:
            date, procs, notes, err = parse_form(emp_id)
            if err:
                flash(err, "error"); return redirect(action + "&date=" + urllib.parse.quote(date, safe=""))
            with _save_lock((emp_id, date)):                  # a double click / second tab cannot save the same day twice
                if duplicate_entry(emp_id, date, fresh=True):
                    flash(f"{name} already has an entry for {date}. Use Edit on that entry instead of adding the same date again.", "error")
                    return redirect("/admin/log?emp=" + urllib.parse.quote(emp_id, safe="") + "&date=" + urllib.parse.quote(date, safe=""))
                write_sub(uuid.uuid4().hex[:10], date, (band, emp_id, name), procs, notes)
        except Exception:
            import traceback; traceback.print_exc()
            flash("The entry could not be saved right now (the data service is busy). Nothing was saved - please press Save again.", "error")
            return redirect(action)
        flash(f"Entry for {date} added for {name}." + (f" Note: {date} is a weekly off, so it is not counted in calculations." if is_off(date) else ""))
        return redirect("/admin/log?emp=" + urllib.parse.quote(emp_id, safe=""))
    sub = dict(date=(request.args.get("date") or request.args.get("adate") or str(today_local())), band=band, designation=find_designation(emp_id, name, band),
               emp_id=emp_id, emp_name=name, procs=[{}], notes=[{}])
    body, ctx = form_page(sub, action, f"Add entry for {name}")
    return page(body, title="Add entry", **ctx)

@app.route("/admin/log/report")
@need("admin")
def admin_log_report():
    period = "week" if request.args.get("period") == "week" else "month"
    r = log_report_data(period, request.args.get("emp", ""), request.args.get("on"))
    tp = sum(x[6] for x in r["summary"] if x[9] != "Weekend - not counted")
    tn = sum(x[7] for x in r["summary"] if x[9] != "Weekend - not counted")
    return page(LOG_REPORT, title="Productivity report", period=period, label=r["label"], emp=r["emp"],
                summary=r["summary"], detail=r["detail"], sh=SUMMARY_HEADS, dh=DETAIL_HEADS, tp=tp, tn=tn,
                now=now_local().strftime("%Y-%m-%d %I:%M %p"), autoprint=request.args.get("print") == "1")

@app.route("/admin/log/export")
@need("admin")
def admin_log_export():
    period = "week" if request.args.get("period") == "week" else "month"
    r = log_report_data(period, request.args.get("emp", ""), request.args.get("on"))
    tag = ("week_" + str(r["start"])) if period == "week" else str(r["start"])[:7]
    fname = f"Productivity_Log_{tag}"
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:      # openpyxl not installed: still give a file Excel opens
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow([f"Productivity Log - {r['label']}"]); w.writerow(SUMMARY_HEADS); w.writerows(r["summary"])
        w.writerow([]); w.writerow(DETAIL_HEADS); w.writerows(r["detail"])
        return Response("\ufeff" + buf.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": f'attachment; filename="{fname}.csv"'})
    wb = Workbook()
    hfill = PatternFill("solid", fgColor="4F46E5"); thin = Side(style="thin", color="D9DCEB")
    def sheet(ws, title, heads, data, widths, numcols):
        ws.title = title
        ws.append([f"Productivity Log - {r['label']}" + (f"  |  Filter: {r['emp']}" if r["emp"] else "")])
        ws["A1"].font = Font(bold=True, size=13); ws.append([])
        ws.append(heads)
        for c in ws[3]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = hfill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for row in data:
            ws.append([("" if v is None else v) for v in row])
        for row in ws.iter_rows(min_row=4, max_row=ws.max_row):
            for c in row:
                c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
                if c.column in numcols: c.alignment = Alignment(horizontal="right")
        for i, wd in enumerate(widths, start=1): ws.column_dimensions[get_column_letter(i)].width = wd
        ws.freeze_panes = "A4"
        if data: ws.auto_filter.ref = f"A3:{get_column_letter(len(heads))}{ws.max_row}"
    sheet(wb.active, "Daily summary", SUMMARY_HEADS, r["summary"], [12, 6, 12, 22, 20, 8, 14, 18, 10, 22], {7, 8, 9, 10})
    sheet(wb.create_sheet(), "Entry details", DETAIL_HEADS, r["detail"], [12, 6, 12, 22, 20, 8, 10, 26, 30, 8, 8, 12, 14], {10, 11, 12, 13})
    out = io.BytesIO(); wb.save(out)
    return Response(out.getvalue(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": f'attachment; filename="{fname}.xlsx"'})


# ---------------------------------------------------------------- admin: Leave & Permission Log (all employees)
LP_LOG = """<div class="head"><div><h1>Leave &amp; Permission Log</h1>
<p class="mut">{{label}} &middot; every employee's leave and permission requests with dates, duration, reason and approval status. Both leave and permission requests need admin approval - use Approve / Reject in the Action column (a decision can be changed later). Holidays declared by admin are shown here too: employees cannot submit leave or productivity entries on a holiday, and holidays never reduce leave balance or count as missed entries.</p></div></div>
<div class="card no-print"><h2>&#127774; Mark a Holiday</h2>
<form method="post" action="/admin/leave-permission/holiday" class="grid">
<input type="hidden" name="next" value="{{here}}">
<label>From date<input type="date" name="d1" required></label>
<label>To date (optional)<input type="date" name="d2"></label>
<label>Holiday name<input name="name" placeholder="e.g. Diwali" required></label>
<button class="primary">Mark as Holiday</button></form></div>
<div class="kpis">
<div class="kpi"><span>Leave requests</span><b>{{n_leave}}</b></div>
<div class="kpi"><span>Leave days</span><b>{{leave_days}}</b></div>
<div class="kpi"><span>Permission requests</span><b>{{n_perm}}</b></div>
<div class="kpi"><span>Approved permission hrs</span><b>{{perm_hrs|g}}</b></div>
<div class="kpi"><span>Pending approval</span><b>{{n_pending}}</b></div>
<div class="kpi"><span>Holidays</span><b>{{n_hol}}</b></div></div>
<div class="card no-print"><form method="get" class="grid">
<label>Month<input type="month" name="month" value="{{month if month!='all' else ''}}"></label>
<label>Employee ID / name<input name="emp" value="{{emp}}" placeholder="Search"></label>
<label>Type<select name="type">{% for v,l in [('','All'),('leave','Leave'),('permission','Permission'),('holiday','Holiday')] %}<option value="{{v}}" {{'selected' if v==typ else ''}}>{{l}}</option>{% endfor %}</select></label>
<label>Status<select name="status">{% for v in ['','Pending','Approved','Rejected','Holiday'] %}<option value="{{v}}" {{'selected' if v==status else ''}}>{{v or 'All'}}</option>{% endfor %}</select></label>
<button class="primary pbtn">Filter</button><a href="/admin/leave-permission?month=all">All time</a><a href="/admin/leave-permission">This month</a>
<button type="button" class="btnl pbtn" onclick="window.print()">&#128438; Print</button></form></div>
<div style="overflow-x:auto"><table><tr><th>Type</th><th>Employee</th><th>Designation</th><th>Band</th><th>From</th><th>To</th><th>Duration</th>
<th>Reason</th><th>Applied at</th><th>Status</th><th>Reviewed</th><th class="no-print">Action</th></tr>
{% for r in rows %}{% if r.type=='Holiday' %}<tr style="background:rgba(245,158,11,.12)"><td><span class="pill act">&#127774; Holiday</span></td>
<td colspan="3"><b>{{r.name}}</b> &middot; all employees</td>
<td>{{r.start}}</td><td>{{r.end}}</td><td>1 day</td><td>Declared holiday - no leave / productivity entries; leave balance unaffected</td><td>-</td>
<td><span class="pill act">Holiday</span></td><td>-</td>
<td class="act no-print"><form method="post" action="/admin/leave-permission/holiday/delete" onsubmit="return confirm('Remove this holiday? Employees will be able to submit entries for this date again.')"><input type="hidden" name="date" value="{{r.start}}"><input type="hidden" name="next" value="{{here}}"><button class="danger">Remove</button></form></td></tr>
{% else %}<tr><td><span class="pill {{'act' if r.type=='Permission' else ''}}">{{r.type}}</span></td>
<td><a href="/admin/employee-info/{{r.eid|urlencode}}?tab=leave">{{r.eid}} &middot; {{r.name}}</a></td><td>{{r.desig}}</td><td>{{r.band}}</td>
<td>{{r.start}}</td><td>{{r.end}}</td><td>{{r.dur}}</td><td>{{r.reason}}</td><td>{{r.applied|t12}}</td>
<td><span class="pill {{r.status|ppill}}">{{r.status}}</span></td>
<td>{% if r.reviewed %}{{r.reviewed|t12}}{% if r.by %} &middot; {{r.by}}{% endif %}{% else %}-{% endif %}</td>
<td class="act no-print">{% set perm = r.type=='Permission' %}
{% if r.status!='Approved' %}<form method="post" action="{{ ('/admin/employee-info/' ~ (r.eid|urlencode) ~ '/permission/' ~ r.row ~ '/approve') if perm else '/admin/leave-permission/leave-review' }}">{% if not perm %}<input type="hidden" name="eid" value="{{r.eid}}"><input type="hidden" name="rows" value="{{r.lrows}}"><input type="hidden" name="status" value="Approved">{% endif %}<input type="hidden" name="next" value="{{here}}"><button class="primary">Approve</button></form>{% endif %}
{% if r.status!='Rejected' %}<form method="post" action="{{ ('/admin/employee-info/' ~ (r.eid|urlencode) ~ '/permission/' ~ r.row ~ '/reject') if perm else '/admin/leave-permission/leave-review' }}" onsubmit="return confirm('Reject this request?')">{% if not perm %}<input type="hidden" name="eid" value="{{r.eid}}"><input type="hidden" name="rows" value="{{r.lrows}}"><input type="hidden" name="status" value="Rejected">{% endif %}<input type="hidden" name="next" value="{{here}}"><button class="danger">Reject</button></form>{% endif %}</td></tr>{% endif %}
{% else %}<tr><td colspan="12">No leave, permission or holiday records found.</td></tr>{% endfor %}</table></div>"""

@app.route("/admin/leave-permission/leave-review", methods=["POST"])
@need("admin")
def admin_leave_review():
    """Approve / reject one leave request (all the day-rows that were applied together)."""
    status = request.form.get("status", "")
    eid = request.form.get("eid", "")
    want = {int(x) for x in request.form.get("rows", "").split(",") if x.strip().isdigit()}
    if status not in ("Approved", "Rejected") or not want: abort(400)
    mine = [r for r in rows("Leave") if r["_row"] in want and _key(r["Employee ID"]) == _key(eid)]
    if not mine:
        flash("Leave request not found - the employee may have cancelled it.")
    else:
        newly = status == "Approved" and any(leave_status(r) != "Approved" for r in mine)      # Update100: e-mail only on a real approval, never again
        now = now_local().strftime("%Y-%m-%d %H:%M:%S")
        _with_retry(ws_of("Leave").batch_update,
                    [{"range": f"G{r['_row']}:I{r['_row']}", "values": [[status, now, "Admin"]]} for r in mine],
                    value_input_option="RAW")
        invalidate_cache("Leave")
        flash(f"Leave request {status.lower()} ({len(mine)} day{'s' if len(mine) != 1 else ''}).")
        if newly:
            emp_row = next((x for x in rows("Employees") if _key(x["Employee ID"]) == _key(eid)), None)
            if emp_row:
                ds_ = sorted(str(r["Date"]) for r in mine)
                days_ = sum(0.5 if leave_is_half(r) else 1 for r in mine)
                dtxt = _pretty_date(ds_[0]) if len(ds_) == 1 else f"{_pretty_date(ds_[0])} to {_pretty_date(ds_[-1])}"
                dur = ("Half day (4 hrs)" if all(leave_is_half(r) for r in mine) and len(mine) == 1 else f"{days_:g} day{'s' if days_ != 1 else ''}")
                msg_, cat_ = notify_approved(emp_row, "Leave", dtxt, dur, len(mine))
                flash(msg_, "error") if cat_ == "error" else flash(msg_)
    nxt = request.form.get("next", "")
    return redirect(nxt if nxt.startswith("/admin/") else "/admin/leave-permission")

def _leave_runs(leaves):
    """One row per leave request: consecutive days added together (same employee, applied-at and reason) are merged."""
    groups = {}
    for l in leaves:
        groups.setdefault((_key(l["Employee ID"]), str(l.get("Applied at", "")), str(l.get("Reason", ""))), []).append(l)
    out = []
    for (_, applied, reason), items in groups.items():
        items.sort(key=lambda x: str(x["Date"])); run = []
        def flush():
            if run:
                out.append((run[0], run[-1], len(run), applied, reason, [x["_row"] for x in run]))
        for it in items:
            try: ok = run and dt.date.fromisoformat(str(it["Date"])) - dt.date.fromisoformat(str(run[-1]["Date"])) == dt.timedelta(days=1)
            except ValueError: ok = False
            if run and not ok: flush(); run = []
            run.append(it)
        flush()
    return out

@app.route("/admin/leave-permission")
@need("admin")
def admin_leave_permission():
    today = today_local()
    month = request.args.get("month") or today.strftime("%Y-%m")
    q = request.args.get("emp", "").strip().lower()
    typ, status = request.args.get("type", ""), request.args.get("status", "")
    if month == "all": m0, m1, label = "0000-00-00", "9999-99-99", "All time"
    else:
        st, _ = month_range(month); m0 = str(st)
        m1 = str((st.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)); label = st.strftime("%B %Y")
    emps = {_key(e["Employee ID"]): e for e in rows("Employees")}
    def who(eid, name, band):
        e = emps.get(_key(eid), {})
        return dict(eid=str(eid), name=name, band=band, desig=str(e.get("Designation", "")).strip())
    def match(r): return not q or q in str(r["eid"]).lower() or q in str(r["name"]).lower()
    out = []
    if typ in ("", "leave"):
        for first, last, n, applied, reason, lrows in _leave_runs(rows("Leave")):
            if str(last["Date"]) < m0 or str(first["Date"]) > m1: continue
            r = dict(who(first["Employee ID"], first["Employee name"], first["Band"]), type="Leave",
                     start=first["Date"], end=last["Date"], dur=("Half day (4 hrs)" if leave_is_half(first) else f"{n} day{'s' if n != 1 else ''}"), days=(0.5 if leave_is_half(first) else n), hrs=0,
                     reason=reason, applied=applied, status=leave_status(first), reviewed=first.get("Reviewed at", ""),
                     by=first.get("Reviewed by", ""), row=first["_row"], lrows=",".join(map(str, lrows)))
            if match(r): out.append(r)
    if typ in ("", "permission"):
        for x in rows("Permissions"):
            if not (m0 <= str(x["Date"]) <= m1): continue
            hrs = num(x.get("Hours"))
            r = dict(who(x["Employee ID"], x["Employee name"], x["Band"]), type="Permission", start=x["Date"], end=x["Date"],
                     dur=f"{hrs:g} hr{'s' if hrs != 1 else ''}", days=0, hrs=hrs, reason=x.get("Reason", ""),
                     applied=x.get("Applied at", ""), status=str(x.get("Status", "")).strip() or "Pending",
                     reviewed=x.get("Reviewed at", ""), by=x.get("Reviewed by", ""), row=x["_row"])
            if match(r): out.append(r)
    if typ in ("", "holiday"):
        for d, nm in holiday_map().items():
            if not (m0 <= d <= m1): continue
            r = dict(eid="", name=nm or "Holiday", band="", desig="", type="Holiday", start=d, end=d, dur="1 day", days=0, hrs=0,
                     reason=nm, applied="", status="Holiday", reviewed="", by="", row=0, lrows="")
            if not q or q in nm.lower(): out.append(r)
    if status: out = [r for r in out if r["status"] == status]
    out.sort(key=lambda r: (str(r["start"]), str(r["applied"])), reverse=True)
    perm = [r for r in out if r["type"] == "Permission"]
    return page(LP_LOG, title="Leave & Permission Log", rows=out, month=month, label=label, emp=request.args.get("emp", ""),
                typ=typ, status=status, here=request.full_path.rstrip("?"),
                n_leave=sum(r["type"] == "Leave" for r in out), leave_days=sum(r["days"] for r in out if r["status"] != "Rejected"),
                n_perm=len(perm), perm_hrs=sum(r["hrs"] for r in perm if r["status"] == "Approved"),
                n_pending=sum(r["status"] == "Pending" for r in out), n_hol=sum(r["type"] == "Holiday" for r in out))

@app.route("/admin/leave-permission/holiday", methods=["POST"])
@need("admin")
def admin_holiday_add():
    """Mark one date (or a range) as a holiday. Employees can no longer submit leave / productivity for it."""
    nxt = request.form.get("next", "")
    back = nxt if nxt.startswith("/admin/") else "/admin/leave-permission"
    d1 = (request.form.get("d1") or "").strip(); d2 = (request.form.get("d2") or "").strip() or d1
    name = (request.form.get("name") or "").strip() or "Holiday"
    try:
        a, b = dt.date.fromisoformat(d1), dt.date.fromisoformat(d2)
        if b < a or (b - a).days > 31: raise ValueError
    except ValueError:
        flash("Choose a valid holiday date (or date range, max 31 days)."); return redirect(back)
    have = holidays()
    new = [[str(a + dt.timedelta(days=i)), name] for i in range((b - a).days + 1) if str(a + dt.timedelta(days=i)) not in have]
    if new:
        ws_of("Holidays").append_rows(new, value_input_option="RAW"); invalidate_cache("Holidays")
    flash(f"{len(new)} holiday date(s) marked as '{name}'." if new else "Those dates are already holidays.")
    return redirect(back)

@app.route("/admin/leave-permission/holiday/delete", methods=["POST"])
@need("admin")
def admin_holiday_delete():
    nxt = request.form.get("next", "")
    date = (request.form.get("date") or "").strip()
    hits = sorted((r["_row"] for r in rows("Holidays") if str(r.get("Date")).strip() == date), reverse=True)
    for rw in hits: ws_of("Holidays").delete_rows(rw)
    if hits: invalidate_cache("Holidays")
    flash(f"Holiday on {date} removed." if hits else "Holiday not found.")
    return redirect(nxt if nxt.startswith("/admin/") else "/admin/leave-permission")

# ---------------------------------------------------------------- admin: notifications (background alerts)
@app.route("/admin/notify/poll")
@need("admin")
def admin_notify_poll():
    """Polled by the admin's browser every 15s: unread count + any alerts newer than `since`."""
    data = notif_rows()
    since = request.args.get("since", "0")
    since = int(since) if since.isdigit() else 0
    last = max((_nid(r) for r in data), default=0)
    items = [] if request.args.get("first") == "1" else \
            [dict(id=str(_nid(r)), text=note_text(r)) for r in sorted(data, key=_nid) if _nid(r) > since]
    return jsonify(unseen=sum(1 for r in data if str(r.get("Seen", "")).strip() != "Yes"),
                   last=str(max(last, since)), items=items)

# ---------------------------------------------------------------- admin: Employee Info (list -> employee details)
TABS = [("personal", "Personal Details"), ("missed", "Missed Entries"), ("leave", "Leave Log"),
        ("holidays", "Holidays"), ("mahizhchi", "Mahizhchi Log"), ("notifications", "Notifications")]

EMP_LIST = """<div class="head"><div><h1>Employee Info</h1><p class="mut">{% if view=='notifications' %}A log of what employees have added, updated or deleted, newest first (latest 200).{% elif view=='access' %}Enable or disable each employee's login. Disabled employees cannot log in; their data is not changed.{% else %}Click an employee's name to open their details. A name in red has unseen login/logout notifications.{% endif %}</p></div>
{% if view!='notifications' %}<form class="grid" method="get"><input name="q" placeholder="Search ID / name" value="{{q}}">
<button class="primary">Search</button><a href="/admin/employee-info">Reset</a></form>{% endif %}</div>
<div class="tabs no-print"><a href="/admin/employee-info" class="{{'on' if view=='employees' else ''}}">Employees</a>
<a href="/admin/employee-info?view=access" class="{{'on' if view=='access' else ''}}">Employee Login Access</a>
<a href="/admin/employee-info?view=notifications" class="{{'on' if view=='notifications' else ''}}">Notifications{% if new_count %} ({{new_count}} new){% endif %}</a></div>
{% if view=='access' %}
<div class="card no-print" id="addlogin"><h2 style="margin-top:0">Add employee login</h2>
<p class="mut">For a new joiner: enter the username (Employee ID) and an initial password, then save. The employee can sign in at <b>/employee/login</b> with the Employee ID or the Email, plus this password. If the Employee ID already exists without a password, only the password is set.</p>
<form method="post" action="/admin/employee-info/login-access/add" autocomplete="off" class="grid" onsubmit="var b=this.querySelector('button.primary');setTimeout(function(){b.disabled=true},0)">
<input name="eid" placeholder="Username / Employee ID *" required maxlength="40" value="{{ad.get('eid','')}}">
<input name="name" placeholder="Employee name *" required maxlength="80" value="{{ad.get('name','')}}">
<input name="email" type="email" placeholder="Office email (also works as username)" maxlength="120" value="{{ad.get('email','')}}">
<input name="band" placeholder="Band" maxlength="20" value="{{ad.get('band','')}}">
<input name="designation" placeholder="Designation" maxlength="80" value="{{ad.get('designation','')}}">
<select name="gender"><option value="">Gender (for 3D avatar)</option><option {{'selected' if ad.get('gender')=='Male'}}>Male</option><option {{'selected' if ad.get('gender')=='Female'}}>Female</option></select>
<span style="position:relative;display:inline-block"><input id="al_pw" name="pw" type="text" placeholder="Initial password * (min 4)" required minlength="4" maxlength="60" style="padding-right:84px"><button type="button" class="back sm" style="position:absolute;right:4px;top:50%;transform:translateY(-50%)" onclick="var c='ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789',o='';for(var i=0;i<8;i++)o+=c[Math.floor(Math.random()*c.length)];document.getElementById('al_pw').value=o">Generate</button></span>
<label style="display:flex;align-items:center;gap:6px"><input type="checkbox" name="enable" value="1" checked style="width:auto"> Enable login now</label>
<button class="primary" type="submit">Save login credentials</button></form></div>
<p class="mut">Login enabled: <b>{{n_on}}</b> &middot; Login disabled: <b>{{n_off}}</b></p>
<table><tr><th>Employee ID</th><th>Employee Name</th><th>Office Email ID</th><th>Login Access Status</th><th class="no-print">Action (Admin only)</th></tr>
{% for e in emps %}{% set off = e.login_off %}<tr><td>{{e['Employee ID']}}</td><td><b>{{e['Name']}}</b></td><td>{{e['Email'] or '-'}}</td>
<td>{% if off %}<span class="pill" style="background:#fde8e8;color:#b42318">Disabled</span>{% else %}<span class="pill" style="background:#e6f6ec;color:#15803d">Enabled</span>{% endif %}</td>
<td class="act no-print">
<form method="post" action="/admin/employee-info/login-access/{{e['_row']}}"><input type="hidden" name="eid" value="{{e['Employee ID']}}"><input type="hidden" name="back" value="{{request.full_path.rstrip('?')}}"><input type="hidden" name="do" value="enable"><button class="primary sm" type="submit" {{'' if off else 'disabled'}}>Enable Login</button></form>
<form method="post" action="/admin/employee-info/login-access/{{e['_row']}}" onsubmit="return confirm('Disable login for {{e['Employee ID']}} ({{e['Name']}})? This employee will not be able to log in until you enable it again. Their data is not changed.')"><input type="hidden" name="eid" value="{{e['Employee ID']}}"><input type="hidden" name="back" value="{{request.full_path.rstrip('?')}}"><input type="hidden" name="do" value="disable"><button class="danger sm" type="submit" {{'disabled' if off else ''}}>Disable Login</button></form>
<form method="post" action="/admin/employees/{{e['_row']}}/reset-password" onsubmit="var p=prompt('Set password for {{e['Employee ID']}} (leave empty to generate one):','');if(p===null)return false;this.newpw.value=p;return true"><input type="hidden" name="eid" value="{{e['Employee ID']}}"><input type="hidden" name="back" value="{{request.full_path.rstrip('?')}}"><input type="hidden" name="newpw" value=""><button class="back sm" type="submit">Set Password</button></form></td></tr>
{% else %}<tr><td colspan="5">No employees found.</td></tr>{% endfor %}</table>
{% elif view=='notifications' %}
<table><tr><th>Employee Name</th><th>Date &amp; Time</th><th>Section / Log</th><th>Action</th><th>Details</th><th>Summary</th></tr>
{% for r in log %}<tr{% if r.new %} style="font-weight:600"{% endif %}>
<td><a href="/admin/employee-info/{{r.id|urlencode}}">{{r.name}}</a></td><td>{{r.time|t12}}</td><td>{{r.section}}</td>
<td><span class="pill {{'out' if r.action=='Deleted' else 'act'}}">{{r.action}}</span></td><td>{{r.details or '-'}}</td><td>{{r.summary}}</td></tr>
{% else %}<tr><td colspan="6">No employee updates yet.</td></tr>{% endfor %}</table>
{% else %}
<table><tr><th>Employee ID</th><th>Name</th><th>Designation</th><th>Band</th><th>Status</th><th class="no-print">Account management (Admin only)</th></tr>
{% for e in emps %}{% set lk = (e['Account locked']|string|lower) in ['yes','y','true','locked','1'] %}<tr><td>{{e['Employee ID']}}</td>
<td><a href="/admin/employee-info/{{e['Employee ID']|urlencode}}"><b{% if e.flag %} class="emp-flag" title="Red means this employee has unseen login/logout notifications"{% endif %}>{{e['Name']}}</b></a></td>
<td>{{e['Designation']}}</td><td>{{e['Band']}}</td>
<td>{% if lk %}<span class="pill" style="background:#fde8e8;color:#b42318">Locked</span>{% else %}<span class="pill" style="background:#e6f6ec;color:#15803d">Active</span>{% endif %}</td>
<td class="act no-print">
<form method="post" action="/admin/employees/{{e['_row']}}/lock"><input type="hidden" name="eid" value="{{e['Employee ID']}}"><input type="hidden" name="back" value="{{request.full_path.rstrip('?')}}"><input type="hidden" name="do" value="{{'unlock' if lk else 'lock'}}"><button class="back sm" type="submit">{{'Unlock Account' if lk else 'Lock Account'}}</button></form>
<form method="post" action="/admin/employees/{{e['_row']}}/reset-password" onsubmit="var p=prompt('New password for {{e['Employee ID']}} (leave empty to generate one):','');if(p===null)return false;this.newpw.value=p;return true"><input type="hidden" name="eid" value="{{e['Employee ID']}}"><input type="hidden" name="back" value="{{request.full_path.rstrip('?')}}"><input type="hidden" name="newpw" value=""><button class="back sm" type="submit">Reset Password</button></form>
<form method="post" action="/admin/employees/{{e['_row']}}/delete" onsubmit="return confirm('Permanently delete the account of {{e['Employee ID']}} ({{e['Name']}})? Their login is removed. Past productivity entries stay in the log.')"><input type="hidden" name="eid" value="{{e['Employee ID']}}"><input type="hidden" name="back" value="{{request.full_path.rstrip('?')}}"><button class="danger sm" type="submit">Delete Account</button></form></td></tr>
{% else %}<tr><td colspan="6">No employees found.</td></tr>{% endfor %}</table>
{% endif %}"""

EMP_HEAD = """<div class="head"><div><h1>{{emp['Name']}}</h1>
<p class="mut">{{emp['Employee ID']}} &middot; {{emp['Designation'] or 'No designation'}} &middot; Band {{emp['Band']}}</p></div>
<a href="/admin/employee-info">&larr; All employees</a></div>
<div class="tabs no-print">{% for k,l in tabs %}<a href="/admin/employee-info/{{emp['Employee ID']|urlencode}}?tab={{k}}"
class="{{'on' if k==tab else ''}}">{{l}}</a>{% endfor %}</div>"""

T_PERSONAL = """<div class="card"><h2>Personal details</h2>
<table>{% for l,v in fields %}<tr><th style="width:220px">{{l}}</th><td>{{v or '-'}}</td></tr>{% endfor %}</table><br>
<a class="btnl no-print" href="/admin/personal/{{emp['_row']}}">Edit details</a></div>
<div class="card no-print"><h2>Job / Joining date</h2>
<p class="mut">Productivity entry is available only from this date. Earlier dates cannot be submitted and are never shown as missed or pending. Leave empty for no restriction.</p>
<form method="post" action="/admin/employee-info/{{emp['Employee ID']|urlencode}}/joining" class="grid"><input type="date" name="joining" value="{{emp.get('Joining date','')}}">
<button class="primary sm" type="submit">Save joining date</button></form></div>"""

T_MISSED = """<form class="grid no-print" method="get"><input type="hidden" name="tab" value="missed">
<input type="month" name="month" value="{{month if month!='all' else ''}}"><button class="primary">Show</button>
<a href="?tab=missed">This month</a><a href="?tab=missed&month=all">All time</a></form>
<div class="kpis"><div class="kpi"><span>Missed entries &middot; {{label}}</span><b>{{data|length}}</b></div></div>
<p class="mut">Working days (weekly off excluded) with no productivity entry and no leave. Today is not included.</p>
{% if data %}<form method="post" action="/admin/missed/send" class="no-print" onsubmit="return confirm('Send the Missed Entries e-mail to this employee?')"><input type="hidden" name="eid" value="{{emp['Employee ID']}}"><input type="hidden" name="month" value="{{month}}"><input type="hidden" name="next" value="/admin/employee-info/{{emp['Employee ID']|urlencode}}?tab=missed&month={{month}}"><button class="primary">&#9993; Send Missed Entries e-mail</button></form>{% endif %}
<table><tr><th>Date</th><th>Day</th></tr>
{% for r in data %}<tr><td>{{r.date}}</td><td>{{r.day}}</td></tr>
{% else %}<tr><td colspan="2">No missed entries.</td></tr>{% endfor %}</table>"""

T_LEAVE = """<p class="mut">This month's balance (working days / hours used against the monthly allowance; leave added here by admin does not count against the employee's limit).</p>
<div class="kpis"><div class="kpi"><span>Leave used / limit</span><b>{{leave_used|g}} / {{LEAVE_MONTHLY_LIMIT|g}} day(s)</b></div>
<div class="kpi"><span>Leave remaining</span><b>{{leave_remaining|g}} day(s)</b></div>
<div class="kpi"><span>Permission used / limit</span><b>{{perm_used|g}} / {{PERMISSION_MONTHLY_LIMIT|g}} hrs</b></div>
<div class="kpi"><span>Permission remaining</span><b>{{perm_remaining|g}} hrs</b></div></div>
<div class="card no-print"><h2>Add leave</h2><form method="post" action="/admin/employee-info/{{emp['Employee ID']|urlencode}}/leave" class="grid">
<label>From date<input type="date" name="d1" required></label><label>To date<input type="date" name="d2" required></label>
<label>Day type<select name="daytype"><option value="Full day">Full day</option><option value="Half day">Half day (4 hrs)</option></select></label>
<label>Reason<input name="reason" placeholder="Reason"></label><button class="primary">Add leave</button></form></div>
<table><tr><th>Date</th><th>Reason</th><th>Applied at</th><th>Status</th><th>Reviewed at</th><th class="no-print"></th></tr>
{% for r in data %}{% set st = r|lstatus %}<tr><td>{{r['Date']}}</td><td>{{r['Reason']}}{% if r|lhalf %} <span class="pill act">Half day</span>{% endif %}</td><td>{{r['Applied at']|t12}}</td>
<td><span class="pill {{st|ppill}}">{{st}}</span></td><td>{{(r['Reviewed at'] or '-')|t12}}</td>
<td class="act no-print">{% if st!='Approved' %}<form method="post" action="/admin/leave-permission/leave-review"><input type="hidden" name="eid" value="{{emp['Employee ID']}}"><input type="hidden" name="rows" value="{{r['_row']}}"><input type="hidden" name="status" value="Approved"><input type="hidden" name="next" value="/admin/employee-info/{{emp['Employee ID']|urlencode}}?tab=leave"><button class="primary">Approve</button></form>{% endif %}
{% if st!='Rejected' %}<form method="post" action="/admin/leave-permission/leave-review" onsubmit="return confirm('Reject this leave?')"><input type="hidden" name="eid" value="{{emp['Employee ID']}}"><input type="hidden" name="rows" value="{{r['_row']}}"><input type="hidden" name="status" value="Rejected"><input type="hidden" name="next" value="/admin/employee-info/{{emp['Employee ID']|urlencode}}?tab=leave"><button class="danger">Reject</button></form>{% endif %}<form method="post" action="/admin/employee-info/{{emp['Employee ID']|urlencode}}/leave/{{r['_row']}}/delete"
onsubmit="return confirm('Delete this leave?')"><button class="danger">Delete</button></form></td></tr>
{% else %}<tr><td colspan="6">No leave records.</td></tr>{% endfor %}</table>
<h2>Permission requests</h2>
<p class="mut">Employees choose the permission date themselves, up to {{PERMISSION_MONTHLY_LIMIT|g}} hrs total per month. Review pending requests below.</p>
<table><tr><th>Date</th><th>Hours</th><th>Reason</th><th>Applied at</th><th>Status</th><th>Reviewed at</th><th class="no-print"></th></tr>
{% for r in perms %}<tr><td>{{r['Date']}}</td><td>{{r['Hours']|g}}</td><td>{{r['Reason']}}</td><td>{{r['Applied at']|t12}}</td>
<td><span class="pill {{r['Status']|ppill}}">{{r['Status']}}</span></td><td>{{(r['Reviewed at'] or '-')|t12}}</td>
<td class="act no-print">{% if r['Status']=='Pending' %}
<form method="post" action="/admin/employee-info/{{emp['Employee ID']|urlencode}}/permission/{{r['_row']}}/approve"><button class="primary">Approve</button></form>
<form method="post" action="/admin/employee-info/{{emp['Employee ID']|urlencode}}/permission/{{r['_row']}}/reject"><button class="danger">Reject</button></form>
{% else %}-{% endif %}</td></tr>
{% else %}<tr><td colspan="7">No permission requests.</td></tr>{% endfor %}</table>"""

T_HOLIDAYS = """<p class="mut">Company holidays (they apply to every employee). <a href="/admin/holidays">Manage holidays</a></p>
<table><tr><th>Date</th><th>Day</th><th>Holiday</th></tr>
{% for r in data %}<tr><td>{{r['Date']}}</td><td>{{r.day}}</td><td>{{r['Name']}}</td></tr>
{% else %}<tr><td colspan="3">No holidays declared.</td></tr>{% endfor %}</table>"""

T_NOTIF = """<p class="mut">Everything this employee added, updated or deleted, plus login / logout alerts, newest first (latest 200).</p>
<table><tr><th>Date &amp; Time</th><th>Section / Log</th><th>Action</th><th>Details</th></tr>
{% for v in data %}<tr{% if v.new %} style="font-weight:600"{% endif %}><td>{{v.time|t12}}</td><td>{{v.section}}</td>
<td><span class="pill {{'in' if v.action=='Logged in' else ('out' if (v.action.startswith('Logged out') or v.action=='Deleted') else 'act')}}">{{v.action}}</span></td>
<td>{{v.details or '-'}}</td></tr>
{% else %}<tr><td colspan="4">No notifications yet.</td></tr>{% endfor %}</table>"""

@app.route("/admin/employee-info")
@need("admin")
def admin_employee_info():
    if request.args.get("view") == "notifications":
        log = update_log()
        return page(EMP_LIST, title="Employee Info", view="notifications", log=log,
                    new_count=sum(1 for r in log if r["new"]), emps=[], q="")
    q = request.args.get("q", "").strip().lower()
    emps = [e for e in rows("Employees") if not q or q in str(e["Employee ID"]).lower() or q in str(e["Name"]).lower()]
    emps.sort(key=lambda e: str(e["Name"]).lower())
    if request.args.get("view") == "access":            # Update117: Employee Login Access tab (Admin only)
        for e in emps: e["login_off"] = emp_locked(e)
        off = sum(1 for e in emps if e["login_off"])
        return page(EMP_LIST, title="Employee Info", view="access", emps=emps, q=request.args.get("q", ""),
                    n_on=len(emps) - off, n_off=off, new_count=sum(1 for r in update_log() if r["new"]),
                    ad=session.pop("_ad", {}))
    # Employees with unseen login/logout notifications get their name highlighted in red.
    unseen_ids = {str(r["Employee ID"]) for r in rows("Notifications") if str(r.get("Seen", "")).strip() != "Yes"}
    for e in emps: e["flag"] = str(e["Employee ID"]) in unseen_ids
    log = update_log()
    return page(EMP_LIST, title="Employee Info", view="employees", emps=emps, q=request.args.get("q", ""),
                new_count=sum(1 for r in log if r["new"]))

@app.route("/admin/employee-info/login-access/add", methods=["POST"])
@need("admin")
def admin_login_add():
    """Update121: Admin adds a new employee's login (username = Employee ID, initial password) and enables it.
    The Employee login already accepts Employee ID or Email + Password and honours the Account-locked flag, so nothing there changes."""
    f = request.form; heads = HEADERS["Employees"]
    eid, name = f.get("eid", "").strip(), f.get("name", "").strip()
    email, pw = f.get("email", "").strip(), f.get("pw", "").strip()
    keep = dict(eid=eid, name=name, email=email, band=f.get("band", "").strip(), designation=f.get("designation", "").strip(), gender=f.get("gender", ""))
    back = redirect("/admin/employee-info?view=access#addlogin")
    def fail(m):
        session["_ad"] = keep; flash(m, "error"); return back
    if not eid or not name: return fail("Employee ID (username) and name are required.")
    if re.search(r"\s", eid) or "@" in eid: return fail("The username (Employee ID) cannot contain spaces or '@'. Use the Email field for an email address.")
    if len(pw) < 4: return fail("The password must be at least 4 characters.")
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email): return fail("Please enter a valid email address.")
    invalidate_cache("Employees")
    emps = rows("Employees"); k = _key(eid); ek = email.lower()
    for e in emps:                                               # the username / email must be unique across all logins
        if email and (_key(e["Employee ID"]) == _key(email) or str(e.get("Email", "")).strip().lower() == ek) and _key(e["Employee ID"]) != k:
            return fail(f"The email {email} already belongs to {e['Employee ID']}.")
    existing = next((e for e in emps if _key(e["Employee ID"]) == k), None)
    enable = f.get("enable") == "1"
    if existing:
        if str(existing.get("Password", "")).strip():
            return fail(f"{eid} already has a login. Use 'Set Password' in the table below to change the password.")
        row = existing["_row"]
        set_employee_cell(row, eid, "Password", pw)
        set_employee_cell(row, eid, "Account locked", "" if enable else "Yes")
        flash(f"Password saved for {eid}. Login {'enabled' if enable else 'saved but disabled'}. Share the credentials with the employee: username {eid} / password {pw}")
        return redirect("/admin/employee-info?view=access")
    full = {h: "" for h in heads}
    full.update({"Employee ID": eid, "Name": name, "Band": keep["band"], "Email": email, "Office Email ID": email, "Password": pw,
                 "Designation": keep["designation"], "Gender": keep["gender"], "Account locked": "" if enable else "Yes",
                 "Joining date": str(now_local().date())})
    _with_retry(ws_of("Employees").append_row, [full[h] for h in heads], value_input_option="RAW")
    invalidate_cache("Employees")
    flash(f"Login created for {name}. Username: {eid} / Password: {pw} - {'login enabled' if enable else 'login is DISABLED until you enable it'}. Share these with the employee.")
    return redirect("/admin/employee-info?view=access")

@app.route("/admin/employee-info/login-access/<int:row>", methods=["POST"])
@need("admin")
def admin_login_access(row):
    """Update117: Enable / Disable an employee's login. Uses the existing "Account locked" flag, which the employee login already honours
    (blank = login enabled, Yes = disabled). No change to the login logic or to any other employee data."""
    if session.get("role") != "admin": abort(403)
    eid = request.form.get("eid", ""); disable = request.form.get("do") == "disable"
    if request.form.get("do") not in ("enable", "disable"): abort(400)
    if _admin_emp(row, eid) is None:
        flash("That employee changed - please refresh and try again.", "error"); return redirect(_acct_back())
    set_employee_cell(row, eid, "Account locked", "Yes" if disable else "")
    try: log_change("Employees", "Login disabled" if disable else "Login enabled", f"Employee ID {eid}")
    except Exception as ex: print("log_change failed:", ex)
    flash(f"Login {'disabled - ' + eid + ' can no longer log in.' if disable else 'enabled - ' + eid + ' can log in again.'}")
    return redirect(request.form.get("back") if (request.form.get("back") or "").startswith("/admin/employee-info") and "//" not in request.form.get("back") else "/admin/employee-info?view=access")

def emp_or_404(eid):
    e = next((e for e in rows("Employees") if _key(e["Employee ID"]) == _key(eid)), None)
    return e or abort(404)

@app.route("/admin/employee-info/<eid>/joining", methods=["POST"])
@need("admin")
def admin_set_joining(eid):
    emp = emp_or_404(eid); v = (request.form.get("joining") or "").strip()
    if v:
        try: dt.date.fromisoformat(v)
        except ValueError:
            flash("Please choose a valid joining date.", "error"); return redirect(f"/admin/employee-info/{urllib.parse.quote(str(emp['Employee ID']))}")
    if set_employee_cell(emp["_row"], emp["Employee ID"], "Joining date", v) is None:
        flash("That employee changed - please refresh and try again.", "error")
    else:
        flash(f"Joining date {'set to ' + v if v else 'cleared'} for {emp['Employee ID']}.")
    return redirect(f"/admin/employee-info/{urllib.parse.quote(str(emp['Employee ID']))}")

@app.route("/admin/employee-info/<eid>")
@need("admin")
def admin_employee_detail(eid):
    emp = emp_or_404(eid); eid = str(emp["Employee ID"])
    tab = request.args.get("tab", "personal")
    if tab not in dict(TABS): tab = "personal"
    today = today_local()
    month = request.args.get("month") or today.strftime("%Y-%m")
    ctx = dict(emp=emp, tab=tab, tabs=TABS)
    if tab == "personal":
        fields = [("Employee ID", emp["Employee ID"]), ("Name", emp["Name"]), ("Designation", emp.get("Designation", "")),
                  ("Band", emp["Band"])] + [(f, emp.get(f, "")) for f in EDITABLE_PERSONAL] + \
                 [("Joining date", emp.get("Joining date", "")), ("Office Email ID", emp.get("Email", "")), ("Last updated", t12(emp.get("Profile updated at", "")))]
        body = T_PERSONAL; ctx["fields"] = fields
    elif tab == "missed":
        subs = [s for s in load_subs() if _key(s["emp_id"]) == _key(eid)]
        leaves = [l for l in rows("Leave") if _key(l["Employee ID"]) == _key(eid)]
        if month == "all":
            ds = [s["date"] for s in subs] + [l["Date"] for l in leaves]
            start, label = (dt.date.fromisoformat(min(ds)) if ds else today), "All time"
            end = today - dt.timedelta(days=1)
        else:
            start, _ = month_range(month); label = start.strftime("%B %Y")
            end = min(month_range(month)[1], today - dt.timedelta(days=1))
        data = [dict(date=d, day=dt.date.fromisoformat(d).strftime("%a"))
                for d in missing_dates(eid, subs, leaves, start, end, fmt="%Y-%m-%d")]
        data.sort(key=lambda r: r["date"], reverse=True)
        body = T_MISSED; ctx.update(data=data, month=month, label=label)
    elif tab == "leave":
        data = sorted((r for r in rows("Leave") if _key(r["Employee ID"]) == _key(eid)),
                      key=lambda r: r["Date"], reverse=True)
        perms = sorted((r for r in rows("Permissions") if _key(r["Employee ID"]) == _key(eid)),
                       key=lambda r: r["Applied at"], reverse=True)
        cur_month = today.strftime("%Y-%m")
        lv_used = leave_days_used(eid, cur_month)
        perm_used = permission_hours_used(eid, cur_month)
        body = T_LEAVE; ctx.update(data=data, perms=perms,
            leave_used=lv_used, leave_remaining=max(LEAVE_MONTHLY_LIMIT - lv_used, 0),
            perm_used=perm_used, perm_remaining=round(PERMISSION_MONTHLY_LIMIT - perm_used, 2))
    elif tab == "holidays":
        data = sorted(rows("Holidays"), key=lambda r: str(r["Date"]), reverse=True)
        for r in data:
            try: r["day"] = dt.date.fromisoformat(str(r["Date"])).strftime("%a")
            except ValueError: r["day"] = ""
        body = T_HOLIDAYS; ctx["data"] = data
    elif tab == "mahizhchi":
        body = MZ_EMPINFO; ctx["detail"] = mz_detail(emp); ctx["back"] = None
    else:   # notifications - opening the tab marks this employee's alerts as read
        data = [notif_view(r) for r in sorted(rows("Notifications"), key=_nid, reverse=True)
                if _key(r["Employee ID"]) == _key(eid)][:200]
        fresh = [v for v in data if v["new"]]
        if fresh:
            ws_of("Notifications").batch_update(
                [{"range": f"F{v['row']}", "values": [["Yes"]]} for v in fresh], value_input_option="RAW")
            _notif_cache[1] = None
        body = T_NOTIF; ctx["data"] = data
    return page(EMP_HEAD + body, title=emp["Name"], **ctx)

@app.route("/admin/employee-info/<eid>/leave", methods=["POST"])
@need("admin")
def admin_employee_leave_add(eid):
    emp = emp_or_404(eid)
    try:
        leave_range_check(request.form['d1'], request.form['d2'])
        flash(f"{add_leave(emp, request.form['d1'], request.form['d2'], request.form['reason'].strip(), status="Approved", day_type=request.form.get('daytype', 'Full day'))} leave day(s) added (holiday dates are skipped).")
    except (ValueError, TypeError) as e:
        flash(str(e))
    return redirect(f"/admin/employee-info/{eid}?tab=leave")

@app.route("/admin/employee-info/<eid>/leave/<int:row>/delete", methods=["POST"])
@need("admin")
def admin_employee_leave_delete(eid, row):
    emp = emp_or_404(eid)
    r = next((r for r in rows("Leave") if r["_row"] == row), None)
    if not r or _key(r["Employee ID"]) != _key(emp["Employee ID"]): abort(404)
    ws_of("Leave").delete_rows(row)
    invalidate_cache("Leave")
    flash("Leave deleted."); return redirect(f"/admin/employee-info/{eid}?tab=leave")

def _review_permission(eid, row, status):
    emp = emp_or_404(eid)
    r = next((r for r in rows("Permissions") if r["_row"] == row), None)
    if not r or _key(r["Employee ID"]) != _key(emp["Employee ID"]): abort(404)
    prev = str(r.get("Status", "")).strip()
    now = now_local().strftime("%Y-%m-%d %H:%M:%S")
    ws_of("Permissions").update(range_name=f"I{row}:K{row}",
                                           values=[[status, now, "Admin"]], value_input_option="RAW")
    invalidate_cache("Permissions")
    flash(f"Permission request {status.lower()}.")
    if status == "Approved" and prev != "Approved":      # Update100: approval e-mail (never on Reject, never twice)
        hrs = num(r.get("Hours"))
        msg_, cat_ = notify_approved(emp, "Permission", _pretty_date(r.get("Date", "")), f"{hrs:g} hr{'s' if hrs != 1 else ''}", 1)
        flash(msg_, "error") if cat_ == "error" else flash(msg_)
    nxt = request.form.get("next", "")
    return redirect(nxt if nxt.startswith("/admin/") else f"/admin/employee-info/{eid}?tab=leave")

@app.route("/admin/employee-info/<eid>/permission/<int:row>/approve", methods=["POST"])
@need("admin")
def admin_permission_approve(eid, row):
    return _review_permission(eid, row, "Approved")

@app.route("/admin/employee-info/<eid>/permission/<int:row>/reject", methods=["POST"])
@need("admin")
def admin_permission_reject(eid, row):
    return _review_permission(eid, row, "Rejected")

# ---------------------------------------------------------------- employee
@app.route("/employee/login", methods=["GET", "POST"])
def employee_login():
    if session.get("role") == "admin":                  # the admin uses the Admin login only
        return _wrong_area("employee")
    if request.method != "POST": _prewarm_employees()
    if request.method == "POST":
        u = request.form["u"].strip().lower()
        for e in rows("Employees"):
            if u in (str(e["Employee ID"]).lower(), str(e["Email"]).lower()) and eq(request.form["p"], e["Password"]):
                if emp_locked(e):                                   # Update96: locked accounts cannot log in
                    flash("Your account is locked. Please contact the Admin to unlock it.", "error")
                    return page(LOGIN, title="Employee login", ph="Employee ID or Email", role="employee")
                track_logout(auto=True, reason="New login")      # closes a previous session in this browser, if any
                session.clear()
                session.update(role="employee", emp_id=str(e["Employee ID"]), name=e["Name"], band=e["Band"],
                               designation=str(e.get("Designation", "")))
                track_login(session["emp_id"], session["name"], session["band"])
                _bg(warm_employee_cache)                  # dashboard data loads while the welcome animation plays
                return redirect("/employee/welcome")
        flash("Wrong username or password.")
    return page(LOGIN, title="Employee login", ph="Employee ID or Email", role="employee")

def form_page(sub, action, heading):
    procs = rows("Processes")
    names = [r["Process name"] for r in procs]
    if not any(is_other(n) for n in names): names.append(OTHER_PROCESS)       # Update90: "Other" is always available
    if not any(is_genai(n) for n in names): names.insert(max(len(names) - 1, 0), GENAI_PROCESS)       # Update103: "GenAI" is always available, same as POC_Sample
    if not any(is_poc(n) for n in names): names.insert(max(len(names) - 1, 0), POC_SAMPLE_PROCESS)       # Update94: "POC_Sample" is always available (Hour, Count, Description required)
    if not any(is_training(n) for n in names): names.insert(max(len(names) - 1, 0), TRAINING_PROCESS)       # Update93: "Training" is always available (just before "Other")
    tph = process_rates()
    perm = {d: h for (_k, d), h in deduction_map(sub.get("emp_id")).items()}      # approved permission + half-day leave hours, by date
    maxdate = ""          # no upper limit on the entry date - employees may pick any date they need
    jd_ = join_date(sub.get("emp_id")) if session.get("role") == "employee" else None
    mindate = str(jd_) if jd_ else ""      # Update97: no entry before the joining date
    return FORM, dict(sub=sub, action=action, heading=heading, names=names, tph=tph, day=day_limit(), target=target_hours(),
                      workday=float(DAY_HOURS), perm=perm, maxdate=maxdate, mindate=mindate, other_hours=OTHER_HOURS)

def gender_of(emp):
    g = str(emp.get("Gender", "")).strip().lower()
    return "male" if g in ("male", "m", "man", "boy") or g.startswith("male") else ("female" if g in ("female", "f", "woman", "girl") or g.startswith("female") else "")

def initials_of(name):
    parts = str(name).replace(".", " ").split()
    return "".join(p[0] for p in parts[:2]).upper() or "?"


WL_SCENE = re.sub(r"\{% if role=='admin' %\}<div class=\"adp\".*?\{% endif %\}", "", LOGIN[LOGIN.index('<div class="scene '):LOGIN.index('<div class="lcard">')], flags=re.S)   # Update110: the Admin Panel / Productivity Dashboard text belongs to the login page only   # same 3D scene + data-packet flow as the login pages
WELCOME = """<style>
.wl{position:fixed;inset:0;z-index:9999;overflow:hidden;font-family:system-ui,-apple-system,Segoe UI,sans-serif}
.wl.admin{background:radial-gradient(900px 420px at 20% 0%,#3b5bdb55,transparent 60%),linear-gradient(120deg,#0b1230 0%,#182a6b 48%,#4f46e5 100%)}
.wl.employee{background:radial-gradient(900px 420px at 80% 0%,#ffb37066,transparent 60%),linear-gradient(120deg,#3b1f6e 0%,#a3407f 48%,#f29a63 100%)}
.wl .scene{border-radius:0}
.wl-card{position:absolute;left:50%;top:50%;width:min(380px,88vw);background:#fff;border-radius:14px;padding:26px 28px 22px;text-align:center;z-index:5;
 box-shadow:0 1px 0 #fff inset,0 30px 60px -16px #0009,0 0 0 1px #ffffff55,0 0 44px -6px #ffffff55;animation:wlPop .55s cubic-bezier(.22,1,.36,1) both;transform:translate(-50%,-50%)}
@keyframes wlPop{from{opacity:0;transform:translate(-50%,-46%) scale(.95)}to{opacity:1;transform:translate(-50%,-50%) scale(1)}}
.wl-card h1{font-family:Georgia,serif;font-size:27px;margin:0 0 4px;color:#5b4fb0;word-break:break-word}
.wl-card p{margin:0 0 14px;color:#6b7390;font-size:13px}
.wl-bar{height:6px;border-radius:4px;background:#e9e6fb;overflow:hidden}
.wl-bar i{display:block;height:100%;width:100%;border-radius:4px;background:linear-gradient(90deg,#6d70f5,#f58a8a);transform-origin:left;transform:scaleX(0);animation:wlFill 2.2s linear forwards}
@keyframes wlFill{to{transform:scaleX(1)}}
.wl-st{margin-top:10px;font:600 10px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.16em;color:#8a90ad}
.wl-ftr{position:fixed;left:0;right:0;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:10000;text-align:center;font-size:11.5px;font-weight:400;letter-spacing:.3px;color:#ffffffc7;text-shadow:0 1px 2px #0008;pointer-events:none}
</style>
<div class="wl {{session.role}}" id="wl">
""" + WL_SCENE.replace('{{role}}', "{{session.role}}").replace("role=='admin'", "session.role=='admin'") + """
 <div class="wl-card"><h1>Welcome, {{session.name}}</h1>
 <p>{{ 'Syncing live data from the server' if session.role=='admin' else 'Securely connecting to the server' }}&hellip;</p>
 <div class="wl-bar"><i></i></div><div class="wl-st">{{ 'RECEIVING DATA' if session.role=='admin' else 'SENDING DATA' }}</div><div class="wl-st" style="margin-top:6px;font-weight:500"><span id="wl_msg">&nbsp;</span></div></div>
<div class="site-foot" role="contentinfo">@2026_Mobius365 | LN_Map_AI</div>
</div>
<script>
(function(){
 /* Update114: Welcome Page = animation only. No AI voice, no music, no audio. The dashboard data loads in the background meanwhile. */
 var DEST={{ ('/admin/summary' if session.role=='admin' else '/employee') | tojson }};
 setTimeout(function(){ window.location.replace(DEST) },2200);
})();
</script>
<noscript><meta http-equiv="refresh" content="3;url={{ '/admin/summary' if session.role=='admin' else '/employee' }}"></noscript>"""

@app.route("/admin/welcome")
@need("admin")
def admin_welcome():
    return page(WELCOME, title="Welcome", wl_gender="male", bare=True)

# ---------------------------------------------------------------- employee GROUP CHAT (Update80 / Update82)
# ONE group = every employee who is online right now. Nobody is added by hand: coming online joins the group, going offline leaves it.
# The chat is a floating icon (bottom-right) on every employee page. Messages AND attachments live in memory only and are deleted GC_TTL seconds
# (12 hours) after sending. Update82: files, images/photos and emoji.
_gc, _gc_read, _gc_seq, _gc_lock = [], {}, [0], threading.Lock()
GC_MAX_LEN, GC_KEEP, GC_TTL = 500, 30000, 12 * 3600      # Update111: messages + shared files live 12 hours, then are permanently deleted
GC_MAX_FILE  = 5 * 1024 * 1024        # largest single attachment
GC_MAX_STORE = 150 * 1024 * 1024      # all attachments together; the oldest ones are dropped first when this is exceeded
# Never accept programs / scripts / web pages: they could be dangerous when opened. Everything else (documents, sheets, PDFs, zips, photos...) is fine.
GC_BLOCKED_EXT = {"exe", "bat", "cmd", "com", "scr", "msi", "msp", "dll", "js", "mjs", "vbs", "vbe", "wsf", "ps1", "psm1", "sh", "bash", "jar", "apk",
                  "app", "pif", "cpl", "reg", "lnk", "hta", "html", "htm", "xhtml", "svg", "php", "py", "pyc", "iso", "dmg"}

def _gc_purge():
    """Delete messages (and their attachments) older than GC_TTL = 12 hours (caller holds _gc_lock). Everything is memory-only, so nothing older survives."""
    cut = time.time() - GC_TTL
    _gc[:] = [m for m in _gc if m["ts"] > cut]

def _gc_sweeper():
    while True:                                   # Update111: background cleanup, no manual action; also runs on every chat poll / send
        time.sleep(60)
        try:
            with _gc_lock: _gc_purge()
        except Exception as ex:
            print("group chat cleanup error (will retry in 60 s):", ex)
threading.Thread(target=_gc_sweeper, daemon=True).start()

def _gc_img_mime(data):
    """Real image type from the file's first bytes (the browser-supplied type is never trusted). Only safe raster formats count as images."""
    if data[:8] == b"\x89PNG\r\n\x1a\n": return "image/png"
    if data[:3] == b"\xff\xd8\xff": return "image/jpeg"
    if data[:6] in (b"GIF87a", b"GIF89a"): return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP": return "image/webp"
    return ""

def _gc_clean_name(n):
    n = os.path.basename(str(n or "").replace("\\", "/"))
    n = "".join(c for c in n if c.isprintable() and c not in '<>:"|?*').strip(" .")
    return (n or "file")[:120]

def _gc_att_pick(m):
    a = m.get("att")
    if not a: return None
    return dict(fid=a["fid"], name=a["name"], kind=a["kind"], size=a["size"], gone=a["data"] is None)

@app.route("/employee/gc/state")
@need("employee")
def gc_state():
    """One poll: online members, unread count and the group's messages newer than ?after=. ?open=1 means the chat panel is on screen (all read)."""
    me = str(session.get("emp_id", ""))
    try: after = int(request.args.get("after", -1))
    except ValueError: after = -1
    members = online_list()
    ids = {r["id"] for r in members}
    with _gc_lock:
        _gc_purge()
        for k in [k for k in _gc_read if k not in ids]: del _gc_read[k]      # went offline -> left the group
        top = max([m["id"] for m in _gc] or [0])
        if me not in _gc_read or request.args.get("open") == "1": _gc_read[me] = top   # just joined: nothing unread; panel open: all read
        unread = sum(1 for m in _gc if m["frm"] != me and m["id"] > _gc_read[me])
        conv = [m for m in _gc if m["id"] > after][-200:]
        out = [dict(id=m["id"], name=m["name"], text=m["text"], t=m["t"], ts=m["ts"], mine=(m["frm"] == me), att=_gc_att_pick(m)) for m in conv]
    return jsonify(members=[dict(id=r["id"], name=r["name"], status=r["status"], me=(r["id"] == me)) for r in members],
                   unread=unread, now=time.time(), messages=out)

@app.route("/employee/gc/send", methods=["POST"])
@need("employee")
def gc_send():
    me = str(session.get("emp_id", ""))
    if request.content_length and request.content_length > GC_MAX_FILE + 256 * 1024:      # refuse before reading the upload
        return jsonify(ok=False, error="That file is too large - the limit is 5 MB."), 413
    text = (request.form.get("text") or "").strip()[:GC_MAX_LEN]
    up = request.files.get("file")
    att = None
    if up is not None and (up.filename or "").strip():
        data = up.read(GC_MAX_FILE + 1)
        if not data: return jsonify(ok=False, error="That file is empty."), 400
        if len(data) > GC_MAX_FILE: return jsonify(ok=False, error="That file is too large - the limit is 5 MB."), 413
        name = _gc_clean_name(up.filename)
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext in GC_BLOCKED_EXT:
            return jsonify(ok=False, error="'." + ext + "' files can't be sent in the chat (programs, scripts and web pages are blocked)."), 415
        mime = _gc_img_mime(data)
        att = dict(fid=uuid.uuid4().hex, name=name, kind="image" if mime else "file", mime=mime or "application/octet-stream", size=len(data), data=data)
    if not text and not att: return jsonify(ok=False, error="Type a message or attach a file first."), 400
    if me not in {r["id"] for r in online_list()}: return jsonify(ok=False, error="You are offline - message not sent."), 409
    with _gc_lock:
        _gc_purge()
        _gc_seq[0] += 1
        _gc.append(dict(id=_gc_seq[0], frm=me, name=str(session.get("name", "")), text=text, att=att,
                        t=now_local().strftime("%I:%M %p"), ts=time.time()))
        del _gc[:-GC_KEEP]
        _gc_read[me] = _gc_seq[0]
        total = sum(len(m["att"]["data"]) for m in _gc if m.get("att") and m["att"]["data"] is not None)
        for m in _gc:                                                       # over the storage cap: free the oldest attachments first
            if total <= GC_MAX_STORE: break
            a = m.get("att")
            if a and a["data"] is not None and m["id"] != _gc_seq[0]:
                total -= len(a["data"]); a["data"] = None
    return jsonify(ok=True)

@app.route("/employee/gc/file/<fid>")
@need("employee")
def gc_file(fid):
    """Serve one chat attachment. Photos display inline (verified raster images only); every other file is forced to download, never opened by the browser."""
    with _gc_lock:
        _gc_purge()
        a = next((m["att"] for m in _gc if m.get("att") and m["att"]["fid"] == fid), None)
        data = a["data"] if a else None
        meta = dict(a) if a else None
    if not meta or data is None: abort(404)
    inline = meta["kind"] == "image" and request.args.get("dl") != "1"
    resp = send_file(io.BytesIO(data), mimetype=meta["mime"] if meta["kind"] == "image" else "application/octet-stream",
                     as_attachment=not inline, download_name=meta["name"])
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Content-Security-Policy"] = "default-src 'none'; sandbox"
    return resp

@app.route("/employee/ping")
@need("employee")
def employee_ping():
    return ("", 204)          # heartbeat; the online bookkeeping happens in _idle_auto_logout

@app.route("/admin/online/poll")
@need("admin")
def admin_online_poll():
    return jsonify(items=online_list())

@app.route("/employee/welcome")
@need("employee")
def employee_welcome():
    try:
        g = gender_of(my_emp_row())
    except Exception:
        g = ""
    return page(WELCOME, title="Welcome", wl_gender=g or "male", bare=True)

@app.route("/employee")
@need("employee")
def employee_home():
    prefetch(*EMP_PAGE_SHEETS)          # cold cache: fetch all sheets together instead of one by one
    today = str(today_local())
    session["designation"] = find_designation(session["emp_id"], session["name"], session["band"])
    if desig_view_only(session["designation"]) or is_view_only(session["emp_id"]):      # Update105: View Only - no entry form, no Productivity %
        first_ = today_local().replace(day=1)
        today_perm_ = next((r for r in rows("Permissions") if str(r["Employee ID"]) == session["emp_id"] and r["Date"] == today), None)
        return page(EMP_TOP + VIEW_ONLY_CARD, title="Daily productivity", today=today, month_label=first_.strftime("%B %Y"),
                    lab1="Attendance", lab2="Productivity", a1=None, a2=None, extra=[], today_perm=today_perm_)
    sub = dict(date=today, band=session["band"], designation=session["designation"],
               emp_id=session["emp_id"], emp_name=session["name"],
               procs=[{}], notes=[{}])
    body, ctx = form_page(sub, "/employee/save", "Daily productivity entry")
    all_mine = [s for s in load_subs(session["emp_id"]) if s["emp_id"] == session["emp_id"]]
    mine = [s for s in all_mine if s["date"] == today]
    first = today_local().replace(day=1)
    lv = rows("Leave"); t0 = today_local()
    k = report([my_emp()], all_mine, lv, first, t0)[0]
    missed = missing_dates(session["emp_id"], all_mine, lv, first, t0 - dt.timedelta(days=1))
    emp_row = my_emp_row()
    missing_fields = missing_personal(emp_row)
    profile_incomplete = bool(missing_fields)
    extra = [("Present days", k["present"]), ("Leave days", k["leave"])]
    today_perm = next((r for r in rows("Permissions")
                       if str(r["Employee ID"]) == session["emp_id"] and r["Date"] == today), None)
    perm_used = permission_hours_used(session["emp_id"], today[:7])
    cut = str(t0 - dt.timedelta(days=6))
    tgt_miss = [m for s_ in all_mine if s_["date"] >= cut for m in sub_misses(s_)][:12]     # newest entries first
    return page(EMP_MARQUEE + EMP_TOP + EMP_ALERT + EMP_TARGET + body + '<h2>Submitted today</h2>' + LIST + BLOOM + SAVED_ANIM,
                title="Daily productivity", missed=missed, subs=mine, tgt_miss=tgt_miss, bloom=bool(session.pop("bloom", False)),
                saved_anim=bool(session.pop("saved_anim", False)),
                today=today, month_label=first.strftime("%B %Y"), lab1="Attendance", lab2="Productivity",
                a1=k["att"], a2=k["pct"], extra=extra, profile_incomplete=profile_incomplete, missing_fields=missing_fields,
                today_perm=today_perm, perm_limit=PERMISSION_MONTHLY_LIMIT, perm_used=perm_used,
                perm_remaining=round(PERMISSION_MONTHLY_LIMIT - perm_used, 2), **ctx)

def prod_months():
    """Update91: months an employee can open on Productivity Info - the current month and the previous month."""
    t = today_local(); cur = t.replace(day=1)
    prev = (cur - dt.timedelta(days=1)).replace(day=1)
    return [cur, prev]

@app.route("/employee/productivity")
@need("employee")
def employee_productivity():
    """Productivity Info: this employee's submissions for the chosen month (current month by default; the previous month is also
    available from the month picker, with View / Edit / Delete on every entry). Only the employee's OWN entries are ever listed."""
    prefetch("Productivity log", "Processes", "Employees", "Settings", "Permissions", "Holidays")
    today = today_local()
    months = prod_months()
    pick = (request.args.get("month") or "").strip()
    sel = next((m for m in months if str(m)[:7] == pick), months[0])
    month = str(sel)[:7]                                # e.g. 2026-09
    is_cur = sel == months[0]
    mlabel = sel.strftime("%B %Y")
    all_mine = [s for s in load_subs(session["emp_id"]) if s["emp_id"] == session["emp_id"]]
    month_subs = sorted((s for s in all_mine if str(s["date"]).startswith(month)),
                        key=lambda s: s["date"], reverse=True)
    counted = [s for s in month_subs if not s["off"]]    # weekly-off entries are not calculated
    m_count = len(counted)
    perms = sorted((r for r in rows("Permissions")
                    if str(r["Employee ID"]) == session["emp_id"] and str(r["Date"]).startswith(month)),
                   key=lambda r: r["Applied at"], reverse=True)
    m_perm = sum(num(r.get("Hours")) for r in perms if str(r.get("Status", "")).strip() == "Approved")
    m_prod = sum(s["prod"] for s in counted)             # hours really worked
    m_non = sum(s["non"] for s in counted)
    m_ded = sum(s["ded"] for s in counted)               # approved permission + half-day leave hours taken off the days worked
    m_avail = sum(s["avail"] for s in counted)           # working hours available (100%)
    m_pct = min(round(m_prod / m_avail * 100), 100) if m_avail > 0 else 0
    nxt = "/employee/productivity?month=" + month        # View / Edit / Delete come back to this month
    body = (
        '<div class="head"><h1>Productivity Info</h1></div>'
        '<form method="get" action="/employee/productivity" class="card no-print" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">'
        '<label style="margin:0"><b>Month</b> <select name="month" onchange="this.form.submit()">'
        '{% for m in months %}<option value="{{m.strftime(\'%Y-%m\')}}"{{\' selected\' if m==sel else \'\'}}>{{m.strftime(\'%B %Y\')}} &ndash; Productivity</option>{% endfor %}'
        '</select></label><noscript><button class="primary">Show</button></noscript>'
        '{% if not is_cur %}<span class="mut">Previous month &ndash; you can view, edit or delete your own entries.</span>{% endif %}</form>'
        '<h2>{{ \'This month\' if is_cur else \'Previous month\' }} ({{mlabel}})</h2>'
        '<div class="totals">Entries: <b>{{m_count}}</b> &middot; '
        'Productive: <b>{{m_prod|g}}</b> hrs &middot; '
        'Non-productive: <b>{{m_non|g}}</b> hrs &middot; '
        'Total: <b>{{(m_prod + m_non)|g}}</b> hrs<br>'
        'Working hours available: <b>{{m_avail|g}}</b> hrs (after <b>{{m_ded|g}}</b> hrs approved permission / half-day leave) &middot; '
        'Productivity: <b>{{m_pct}}%</b></div>'
        + LIST.replace("in subs", "in msubs")
        + '<h2>Permission requests ({{mlabel}})</h2>'
        + '<table><tr><th>Date</th><th>Hours</th><th>Reason</th><th>Applied at</th><th>Status</th></tr>'
        + '{% for r in perms %}<tr><td>{{r["Date"]}}</td><td>{{r["Hours"]|g}}</td><td>{{r["Reason"]}}</td><td>{{r["Applied at"]|t12}}</td>'
        + '<td><span class="pill {{r["Status"]|ppill}}">{{r["Status"]}}</span></td></tr>'
        + '{% else %}<tr><td colspan="5">No permission requests in {{mlabel}}.</td></tr>{% endfor %}</table>')
    return page(body, title="Productivity Info", msubs=month_subs, m_count=m_count, m_prod=m_prod, m_non=m_non,
                m_perm=m_perm, perms=perms, m_ded=m_ded, m_avail=m_avail, m_pct=m_pct,
                months=months, sel=sel, is_cur=is_cur, mlabel=mlabel, nxt=nxt,
                empty_msg="No productivity entries for " + mlabel + ".")

_save_locks = {}
_save_locks_guard = threading.Lock()
def _save_lock(key):
    with _save_locks_guard: return _save_locks.setdefault(key, threading.Lock())

@app.route("/employee/save", methods=["POST"])
@need("employee")
def employee_save():
    if is_view_only(session.get("emp_id", "")):                  # Update105
        flash(VIEW_ONLY_MSG, "error"); return redirect("/employee")
    try:
        date, procs, notes, err = parse_form(session["emp_id"])
        if err:
            flash(err, "error"); return redirect("/employee")
        with _save_lock((session["emp_id"], date)):          # Update96: a double click / second tab cannot save the same day twice
            if duplicate_entry(session["emp_id"], date, fresh=True):
                flash(f"You have already submitted an entry for {date}. Edit the existing entry instead of submitting the same date again.", "error")
                return redirect("/employee")
            write_sub(uuid.uuid4().hex[:10], date, (session["band"], session["emp_id"], session["name"]), procs, notes)
    except Exception as ex:
        import traceback; traceback.print_exc()
        flash("Your entry could not be saved right now (the data service is busy). Nothing was lost - please wait a few seconds and press Save again.", "error")
        return redirect("/employee")
    # ---- the data is saved from here on: nothing below may turn a successful save into an error page ----
    session["saved_anim"] = True       # Update95: 3-second 3D "Saved successfully" animation, shown on the same page after the data is saved
    flash("Saved." + (f" Note: {date} is a weekly off, so this entry is not counted in calculations." if is_off(date) else ""))
    try: log_change(SEC_PROD, "Added", entry_added_details(date, procs, notes))
    except Exception as ex: print("log_change failed:", ex)
    try:
        miss = [] if is_off(date) else miss_lines(date, [(n, h, c) for n, h, c, _d in procs])
        if miss: flash(target_alert_text(miss), "error")           # employee is told straight away that the target was missed
        # Update94: 100% = not a weekly off, every Admin target met, and all required working hours logged -> flower animation (3 s)
        if not is_off(date) and not miss and sum(p_[1] for p_ in procs) + sum(n_[1] for n_ in notes) + 1e-9 >= required_hours(session["emp_id"], date):
            session["bloom"] = True
    except Exception as ex:
        print("post-save checks failed:", ex)
    return redirect("/employee")

@app.route("/entry/<sid>", methods=["GET", "POST"])
@need()
def entry_edit(sid):
    s = get_sub(sid)
    if is_view_only(s["emp_id"]):                                  # Update105
        flash(VIEW_ONLY_MSG, "error"); return redirect(next_url() or home())
    if request.method == "POST":
        date, procs, notes, err = parse_form(s["emp_id"])
        if err:
            flash(err, "error"); return redirect(request.full_path.rstrip("?"))
        changed = entry_diff(s, date, procs, notes)          # compare with the saved entry before it is replaced
        with _save_lock((s["emp_id"], "edit")):               # Update103: one edit at a time per employee; duplicate check + replace are atomic
            if duplicate_entry(s["emp_id"], date, skip_sid=sid, fresh=True):
                flash(f"An entry for {date} already exists. Choose a different date or edit that entry.", "error"); return redirect(request.full_path.rstrip("?"))
            old = live_rows_of(sid)
            if not old:
                flash("This entry no longer exists (it was deleted). Nothing was changed.", "error"); return redirect(next_url() or home())
            delete_rows(old)
            write_sub(sid, date, (s["band"], s["emp_id"], s["emp_name"]), procs, notes)
        if changed: log_change(SEC_PROD, "Updated", changed)
        flash("Updated." + (f" Note: {date} is a weekly off, so this entry is not counted in calculations." if is_off(date) else ""))
        miss = [] if is_off(date) or session.get("role") != "employee" else miss_lines(date, [(n, h, c) for n, h, c, _d in procs])
        if miss: flash(target_alert_text(miss), "error")
        return redirect(next_url() or home())
    nx = next_url()
    body, ctx = form_page(s, request.path + (("?next=" + urllib.parse.quote(nx, safe="")) if nx else ""), "Edit entry")
    return page(body, title="Edit entry", **ctx)

@app.route("/entry/<sid>/view")
@need()
def entry_view(sid):
    return page(VIEW, title="Entry", s=get_sub(sid), day=day_limit(), target=target_hours(), back=next_url() or home())

@app.route("/entry/<sid>/delete", methods=["POST"])
@need()
def entry_delete(sid):
    s = get_sub(sid)
    with _save_lock((s["emp_id"], "edit")):
        old = live_rows_of(sid)                              # Update103: live row numbers - a double click / second admin cannot delete the wrong rows
        if old: delete_rows(old); invalidate_cache("Productivity log")
    log_change(SEC_PROD, "Deleted",
               f"Entry {s['date']} ({_fmt_num(s['prod'])} productive hr, {_fmt_num(s['non'])} non-productive hr)")
    flash("Deleted."); return redirect(next_url() or home())

# ---------------------------------------------------------------- leave + reports
app.jinja_env.filters["tone"] = lambda v: "" if v >= 90 else ("a" if v >= 75 else "r")

def workdays(start, end):          # Mon-Sat (Sunday = weekly off)
    n, d = 0, start
    while d <= end:
        n += not is_off(d)          # weekly offs AND holidays are not working days
        d += dt.timedelta(days=1)
    return n

def month_range(m):
    try:
        y, mo = map(int, m.split("-")); s = dt.date(y, mo, 1)
    except (ValueError, AttributeError):
        s = today_local().replace(day=1)
    e = (s.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return s, min(e, today_local())

def report(employees, subs, leaves, start, end):
    wd, a, b, out = workdays(start, end), str(start), str(end), []
    T = target_hours()
    perms = rows("Permissions")     # fetched once, filtered per employee below
    dmap = deduction_map()          # approved permission / half-day leave hours per employee and date
    leaves = live_leaves(leaves)    # rejected leave does not count
    for e in employees:
        eid = str(e["Employee ID"])
        jd_ = join_date(eid)                                            # Update97: working days count only from the joining date
        ea = str(jd_) if (jd_ and str(jd_) > a) else a
        wd_i = 0 if ea > b else (workdays(dt.date.fromisoformat(ea), end) if ea != a else wd)
        mine = [s for s in subs if str(s["emp_id"]) == eid and ea <= s["date"] <= b and not s["off"]]
        days = {s["date"] for s in mine}
        mylv = [l for l in leaves if str(l["Employee ID"]) == eid and ea <= l["Date"] <= b and not is_off(l["Date"])]
        lv = {l["Date"] for l in mylv if not leave_is_half(l)}          # full-day leave: the whole day is excused
        half = {l["Date"] for l in mylv if leave_is_half(l)}            # half-day leave: 4 hrs still have to be worked
        perm_hrs = sum(num(r.get("Hours")) for r in perms
                       if str(r["Employee ID"]) == eid and a <= str(r["Date"]) <= b
                       and str(r.get("Status", "")).strip() == "Approved")
        prod_hrs = sum(s["prod"] for s in mine)                       # hours really worked
        # 100% = the hours AVAILABLE on each day worked: target (8) less approved permission / half-day leave (2-hr permission = 6, half day = 4)
        base = sum(max(T - dmap.get((_key(eid), str(d)), 0.0), 0.0) for d in days)
        # ---- ATTENDANCE from each working day's real status:  Present = 1 day (100%) | Half day = 0.5 (50%) | Absent = 0 (0%)
        full = days - half                                              # worked days that are not half-day-leave days
        today_s = str(today_local())
        # today is still running: with no entry / leave yet it is "not marked" - it is NOT counted as Absent until the day is over
        pending_today = 1 if (ea <= today_s <= b and not is_off(today_s) and today_s not in (days | lv | half)) else 0
        wd_e = wd_i - pending_today                                       # working days that have a status so far
        credit = len(full) + 0.5 * len(half)                            # Present 1 + Half day 0.5 + Absent 0
        present_n = credit
        leave_n = len(lv) + 0.5 * len(half)
        absent_n = max(wd_e - len(full | lv | half), 0)
        _n = lambda v: int(v) if v == int(v) else v
        out.append(dict(id=eid, name=e["Name"], band=e["Band"], designation=e.get("Designation", ""), present=_n(present_n),
                        leave=_n(leave_n), absent=_n(absent_n), wd=wd_i, counted=wd_e,
                        att=min(round(credit / wd_e * 100), 100) if wd_e else 0,
                        pct=min(round(prod_hrs / base * 100), 100) if base else 0,
                        prod=prod_hrs, non=sum(s["non"] for s in mine), perm=perm_hrs))
    for r_, e_ in zip(out, employees):      # Update105: Senior Team Lead / Team Lead / Associate Manager -> View Only, no Productivity %
        if desig_view_only(e_.get("Designation", "")) or is_view_only(r_["id"]):
            r_.update(vo=True, pct=None, att=None, present="-", absent="-", prod=0, non=0)
        else:
            r_["vo"] = False
    return out

def leave_status(l):
    """Status of a Leave row. Rows saved before the approval feature have no status: treated as Approved."""
    return str(l.get("Status", "")).strip() or "Approved"

def live_leaves(leaves):
    """Leave rows that count in attendance / missed-entry calculations (Rejected leave does not)."""
    return [l for l in leaves if leave_status(l) != "Rejected"]
app.jinja_env.filters["lstatus"] = leave_status

def leave_days_used(eid, month):
    """Working (non weekly-off, non-holiday) leave days already applied for (Pending + Approved;
    Rejected doesn't count) by this employee in the given month ('YYYY-MM')."""
    eid = str(eid)
    return sum(0.5 if leave_is_half(r) else 1 for r in rows("Leave")
               if str(r["Employee ID"]) == eid and str(r["Date"]).startswith(month)
               and leave_status(r) != "Rejected" and not is_off(r["Date"]))

def add_leave(emp, d1, d2, reason, status="Pending", enforce_limit=None, day_type="Full day"):
    """Employees' leave starts as Pending (admin approves/rejects); leave added by admin is Approved.
    Self-service (Pending) requests are capped at LEAVE_MONTHLY_LIMIT working days per calendar month
    (Pending + Approved count against the limit); admin-added leave is not capped unless requested."""
    a, b = dt.date.fromisoformat(d1), dt.date.fromisoformat(d2)
    if b < a or (b - a).days > 31:
        raise ValueError("Choose a valid date range (max 31 days).")
    day_type = "Half day" if str(day_type).strip().lower().startswith("half") else "Full day"
    if day_type == "Half day" and a != b:
        raise ValueError("A half-day leave is for ONE date - choose the same From and To date.")
    if enforce_limit is None:
        enforce_limit = (status == "Pending")
    eid = str(emp["Employee ID"])
    have = {l["Date"] for l in live_leaves(rows("Leave")) if str(l["Employee ID"]) == eid}
    now = now_local().strftime("%Y-%m-%d %H:%M:%S")
    new = [[str(a + dt.timedelta(days=i)), eid, emp["Name"], emp["Band"], reason or "Leave", now, status,
           now if status != "Pending" else "", "Admin" if status != "Pending" else "", day_type]
           for i in range((b - a).days + 1)]
    new = [r for r in new if r[0] not in have and not is_holiday(r[0])]   # nothing is recorded against a holiday
    if enforce_limit and new:
        added_by_month = {}
        for r in new:
            if not is_off(r[0]):
                added_by_month[r[0][:7]] = added_by_month.get(r[0][:7], 0) + (0.5 if day_type == "Half day" else 1)
        for month, add_days in added_by_month.items():
            used = leave_days_used(eid, month)
            if used + add_days > LEAVE_MONTHLY_LIMIT:
                remaining = max(LEAVE_MONTHLY_LIMIT - used, 0)
                raise ValueError(f"Monthly leave limit is {LEAVE_MONTHLY_LIMIT:g} day(s). "
                                  f"You have {remaining:g} day(s) remaining for {month}.")
    if new: ws_of("Leave").append_rows(new, value_input_option="RAW"); invalidate_cache("Leave")
    return len(new)

def holidays_in_range(d1, d2):
    """Sorted holiday dates between two ISO dates (inclusive)."""
    try: a, b = dt.date.fromisoformat(d1), dt.date.fromisoformat(d2)
    except ValueError: return []
    return [str(a + dt.timedelta(days=i)) for i in range((b - a).days + 1) if is_holiday(a + dt.timedelta(days=i))]

def leave_range_check(d1, d2):
    """Raises if every day of the range is a holiday; returns the holiday dates that will be skipped."""
    hol = holidays_in_range(d1, d2)
    try: total = (dt.date.fromisoformat(d2) - dt.date.fromisoformat(d1)).days + 1
    except ValueError: return hol
    if hol and len(hol) >= total:
        raise ValueError(f"{', '.join(hol)} {'is a holiday' if total == 1 else 'are holidays'} - leave cannot be applied for a holiday.")
    return hol

def permission_hours_used(eid, month):
    """Hours already applied for (Pending + Approved; Rejected doesn't count) by this employee
    in the given month ('YYYY-MM')."""
    eid = str(eid)
    return sum(num(r.get("Hours")) for r in rows("Permissions")
               if str(r["Employee ID"]) == eid and str(r["Date"]).startswith(month)
               and str(r.get("Status", "")).strip() != "Rejected")

def add_permission(emp, reason, hours, date=None):
    """Permission is applied for a date picked in the same date picker as Apply Leave (default: today), once per date, and only
    up to PERMISSION_MONTHLY_LIMIT hrs total (Pending + Approved) per calendar month (the month of the chosen date)."""
    eid = str(emp["Employee ID"])
    date = str(date or today_local()).strip()
    try: date = str(dt.date.fromisoformat(date))                  # same date handling as leave: a real YYYY-MM-DD date
    except ValueError: raise ValueError("Choose a valid date.")
    if is_holiday(date):
        raise ValueError(f"{date} is a holiday - permission cannot be applied for a holiday.")
    if any(str(r["Employee ID"]) == eid and str(r["Date"]) == date for r in rows("Permissions")):
        raise ValueError("You have already applied for permission today." if date == str(today_local())
                         else f"You have already applied for permission on {date}.")
    try:
        hours = round(float(hours), 2)
    except (TypeError, ValueError):
        raise ValueError("Enter a valid number of permission hours.")
    if hours <= 0:
        raise ValueError("Permission hours must be greater than 0.")
    month = date[:7]
    used = permission_hours_used(eid, month)
    if used + hours > PERMISSION_MONTHLY_LIMIT:
        raise ValueError(f"Monthly permission limit is {PERMISSION_MONTHLY_LIMIT:g} hrs. "
                          f"You have {round(PERMISSION_MONTHLY_LIMIT - used, 2):g} hr(s) remaining for {month}.")
    now = now_local().strftime("%Y-%m-%d %H:%M:%S")
    pid = uuid.uuid4().hex[:10]
    ws_of("Permissions").append_row(
        [pid, date, eid, emp["Name"], emp["Band"], hours, reason or "Permission", now, "Pending", "", ""],
        value_input_option="RAW")
    invalidate_cache("Permissions")
    return pid

def permission_pill(status):
    return "in" if status == "Approved" else ("out" if status == "Rejected" else "act")
app.jinja_env.filters["ppill"] = permission_pill

def missing_dates(eid, subs, leaves, start, end, fmt="%d %b"):
    """Working days (weekly offs and holidays excluded) in start..end with no entry and no leave."""
    eid = str(eid)
    if is_view_only(eid): return []                    # Update105: no Missed Productivity Entry for View-Only designations
    jd = join_date(eid)
    if jd and start < jd: start = jd                  # Update97: dates before the joining date are never "missed" / "pending"
    leaves = live_leaves(leaves)
    done = {s["date"] for s in subs if str(s["emp_id"]) == eid} | \
           {l["Date"] for l in leaves if str(l["Employee ID"]) == eid and not leave_is_half(l)}      # a half-day leave still needs an entry (4 hrs)
    out, d = [], start
    while d <= end:
        if not is_off(d) and str(d) not in done:
            out.append(d.strftime(fmt))
        d += dt.timedelta(days=1)
    return out

EMP_MARQUEE = """{% if missed %}{% set msg %}&#9888; Productivity entry pending &mdash;
 You missed the entry for {{missed|length}} day(s) this month: {{missed|join(', ')}}. Pick that date in the form below and submit, or apply leave.{% endset %}
{% set dur = [44, ((msg|striptags|length) * 0.3)|int]|max %}
<div class="mq" role="status"><div class="mq-track" style="animation-duration:{{dur}}s">
<div class="mq-group"><span class="mq-item">{{msg}}</span></div>
<div class="mq-group" aria-hidden="true"><span class="mq-item">{{msg}}</span></div>
</div></div>{% endif %}"""

EMP_ALERT = """{% if profile_incomplete %}<div class="warn"><b>&#9888; Personal details incomplete</b>
<div>Please <a href="/employee/profile">complete your personal details</a>{% if missing_fields %} &mdash; missing: {{ missing_fields|join(', ') }}{% endif %}.</div></div>{% endif %}"""

EMP_TARGET = """{% if tgt_miss %}<div class="warn"><b>&#9888; Target not achieved (8-hour target)</b>
{% for m in tgt_miss %}<div>{{m.date}} &middot; {{m.name}}: <b>{{m.count|g}}</b> of <b>{{m.target|g}}</b> ({{m.pct}}%) for {{m.hour|g}} hr &mdash; 8-hour target: {{m.daily|g}}</div>{% endfor %}
<div class="mut">Last 7 days. Please complete the target within 8 hours.</div></div>{% endif %}"""

ADMIN_ALERT = """{% if miss or pend %}<div class="warn"><b>&#9888; Missed entries - {{mlabel}}</b>
{% for r in miss %}<div>{{r.id}} &middot; {{r.name}}: {{r.days|length}} day(s) - {{r.days|join(', ')}}</div>{% endfor %}
{% if pend %}<div>Not submitted today: {{pend|join(', ')}}</div>{% endif %}
<div><a href="/admin/missed-log">View full Missed Entries Log</a></div></div>{% endif %}"""

KPI = """<div class="kpis">
{% if a1 is not none %}<div class="kpi"><span>{{lab1}}</span><b>{{a1}}%</b><i class="bar {{a1|tone}}"><u style="width:{{[a1,100]|min}}%"></u></i></div>{% endif %}
{% if a2 is none %}<div class="kpi"><span>{{lab2}}</span><b>View Only</b></div>{% else %}<div class="kpi"><span>{{lab2}}</span><b>{{a2}}%</b><i class="bar {{a2|tone}}"><u style="width:{{[a2,100]|min}}%"></u></i></div>{% endif %}
{% for l,v in extra %}<div class="kpi"><span>{{l}}</span><b>{{v}}</b></div>{% endfor %}</div>"""

ADMIN_AVATAR = ('<div class="av-adm" role="img" aria-label="Admin profile picture"><svg viewBox="0 0 100 100" aria-hidden="true"><defs>'
 '<radialGradient id="aab" cx="30%" cy="22%" r="90%"><stop offset="0" stop-color="#9fb4ff"/><stop offset="1" stop-color="#2a2f8f"/></radialGradient>'
 '<linearGradient id="aas" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffdcbc"/><stop offset="1" stop-color="#dc9f74"/></linearGradient>'
 '<linearGradient id="aau" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#34407a"/><stop offset="1" stop-color="#151b3f"/></linearGradient></defs>'
 '<rect width="100" height="100" fill="url(#aab)"/>'
 '<path d="M10 100c1-22 18-31 40-31s39 9 40 31z" fill="url(#aau)"/>'
 '<path d="M39 69l11 15 11-15-5-4H44z" fill="#f3f5ff"/><path d="M47.5 74h5l2.2 15L50 94l-4.7-5z" fill="#4f46e5"/>'
 '<rect x="43" y="55" width="14" height="14" rx="6" fill="#d2956b"/>'
 '<ellipse cx="50" cy="40" rx="15" ry="17.5" fill="url(#aas)"/>'
 '<path d="M34.5 39c-2-15 8-22 16-22 9 0 17 6 15 22-3-7-8-10-15.500-10S37.500 32 34.500 39z" fill="#2a2233"/>'
 '<ellipse cx="41" cy="22" rx="15" ry="7" fill="#fff" opacity=".16"/></svg></div>')

AVATAR3D = """<div class="av3d" role="img" aria-label="{{ (gender|capitalize) if gender else 'Employee' }} profile picture"><div class="av-stage">
{% set c = ('#fce7f3','#f9a8d4','#c026d3') if gender=='female' else (('#dbeafe','#93c5fd','#4f46e5') if gender=='male' else ('#ccfbf1','#5eead4','#0d9488')) %}
<svg class="av-l" style="--z:0px" viewBox="0 0 200 200" aria-hidden="true"><defs><radialGradient id="avbg" cx="35%" cy="28%" r="85%"><stop offset="0" stop-color="{{c[0]}}"/><stop offset=".55" stop-color="{{c[1]}}"/><stop offset="1" stop-color="{{c[2]}}"/></radialGradient></defs><circle cx="100" cy="100" r="98" fill="url(#avbg)"/><ellipse cx="70" cy="48" rx="46" ry="20" fill="#fff" opacity=".3" transform="rotate(-24 70 48)"/></svg>
{% if gender %}
{% if gender=='female' %}<svg class="av-l" style="--z:10px" viewBox="0 0 200 200" aria-hidden="true"><defs><clipPath id="avc1"><circle cx="100" cy="100" r="98"/></clipPath><linearGradient id="avh1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6b3a4f"/><stop offset="1" stop-color="#3b1f2f"/></linearGradient></defs><g clip-path="url(#avc1)"><path d="M60 92 C54 46 84 30 102 30 C130 30 148 52 140 96 C146 128 150 156 140 176 L60 176 C50 156 54 126 60 92 Z" fill="url(#avh1)"/></g></svg>{% endif %}
<svg class="av-l" style="--z:20px" viewBox="0 0 200 200" aria-hidden="true"><defs><clipPath id="avc2"><circle cx="100" cy="100" r="98"/></clipPath><linearGradient id="avb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{{ '#ec4899' if gender=='female' else '#34418a' }}"/><stop offset="1" stop-color="{{ '#9d174d' if gender=='female' else '#1b2350' }}"/></linearGradient></defs><g clip-path="url(#avc2)"><path d="M14 204 C14 160 54 144 100 144 C146 144 186 160 186 204 Z" fill="url(#avb)"/><path d="M87 112 h26 v34 q-13 11 -26 0 z" fill="#dda774"/>
{% if gender=='male' %}<path d="M80 144 L100 180 L120 144 Z" fill="#fff"/><path d="M80 144 L100 180 L68 172 Z" fill="#1b2350"/><path d="M120 144 L100 180 L132 172 Z" fill="#1b2350"/><path d="M96 152 h8 l3 26 -7 8 -7 -8 z" fill="#6366f1"/>{% else %}<path d="M84 144 Q100 178 116 144 Z" fill="#f0bd93"/>{% endif %}</g></svg>
<svg class="av-l" style="--z:34px" viewBox="0 0 200 200" aria-hidden="true"><defs><linearGradient id="avf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe3c4"/><stop offset="1" stop-color="#f0b587"/></linearGradient></defs>
<ellipse cx="66" cy="94" rx="5" ry="8" fill="#e6b088"/><ellipse cx="134" cy="94" rx="5" ry="8" fill="#e6b088"/>
<ellipse cx="100" cy="90" rx="33" ry="38" fill="url(#avf)"/>
<ellipse cx="78" cy="106" rx="7" ry="4" fill="#f19a8a" opacity=".35"/><ellipse cx="122" cy="106" rx="7" ry="4" fill="#f19a8a" opacity=".35"/>
<ellipse cx="87" cy="93" rx="3.6" ry="4.4" fill="#2b2440"/><ellipse cx="113" cy="93" rx="3.6" ry="4.4" fill="#2b2440"/>
<circle cx="88.3" cy="91.4" r="1.3" fill="#fff"/><circle cx="114.3" cy="91.4" r="1.3" fill="#fff"/>
<path d="M80 83 q7 -5 14 -1 M106 82 q7 -4 14 1" stroke="#3a2b3f" stroke-width="2.6" fill="none" stroke-linecap="round"/>
<path d="M100 97 q-3 9 1 11" stroke="#c98d63" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M89 113 q11 9 22 0" stroke="#b4534b" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>
<svg class="av-l" style="--z:46px" viewBox="0 0 200 200" aria-hidden="true"><defs><linearGradient id="avh2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{{ '#7a4560' if gender=='female' else '#3d3260' }}"/><stop offset="1" stop-color="{{ '#3b1f2f' if gender=='female' else '#1f1a38' }}"/></linearGradient></defs>
{% if gender=='female' %}<path d="M65 94 C60 52 84 40 102 40 C128 40 142 58 135 94 C128 72 114 62 96 66 C82 70 70 78 65 94 Z" fill="url(#avh2)"/>{% else %}<path d="M65 90 C60 50 86 38 104 40 C130 42 142 60 135 90 C131 74 124 66 104 64 C86 64 71 72 65 90 Z" fill="url(#avh2)"/>{% endif %}</svg>
{% else %}
<svg class="av-l" style="--z:26px" viewBox="0 0 200 200" aria-hidden="true"><text x="100" y="124" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="78" font-weight="700" fill="#fff">{{initials}}</text></svg>
{% endif %}
</div></div>
<script>
(function(){var A=document.querySelectorAll('.av3d');if(!A.length||!window.requestAnimationFrame)return;
var a=A[0],w=document.body,raf=0,px=0,py=0;
w.addEventListener('pointermove',function(e){var r=a.getBoundingClientRect();
px=(e.clientX-(r.left+r.width/2))/260;py=(e.clientY-(r.top+r.height/2))/160;
if(raf)return;raf=requestAnimationFrame(function(){raf=0;A.forEach(function(x){x.classList.add('live');
x.style.setProperty('--ry',Math.max(-24,Math.min(24,px*24))+'deg');
x.style.setProperty('--rx',Math.max(-16,Math.min(16,-py*16))+'deg')})})});
w.addEventListener('pointerleave',function(){A.forEach(function(x){x.classList.remove('live');x.style.removeProperty('--ry');x.style.removeProperty('--rx')})});
})();
</script>"""

EMP_TOP = """<div class="head hero"><div class="welcome wflex"><div class="wtxt"><h1 class="wt"><span class="wt-hi">Hello,</span> <span class="wt-name">{{session.name}}</span></h1>
<p class="mut wsub"><span class="seg">{{today}}</span>{% if session.designation %}<span class="dot">&middot;</span><span class="seg">{{session.designation}}</span>{% endif %}<span class="dot">&middot;</span><span class="seg">Band {{session.band}}</span><span class="dot">&middot;</span><span class="seg">{{month_label}} summary</span>
{% if today_perm %}<span class="dot">&middot;</span>Permission today: <span class="pill {{today_perm['Status']|ppill}}">{{today_perm['Status']}}</span>{% endif %}</p></div></div></div>""" + KPI

VIEW_ONLY_CARD = """<div class="card"><h2 style="margin-top:0">Productivity &mdash; View Only</h2>
<p class="mut">Your designation ({{session.designation}}) has <b>View Only</b> access to Productivity. Daily productivity entry is not required,
no productivity % is calculated, and no missed-entry reminders are sent. Leave &amp; Permission works as usual.</p>
<a class="btnl" href="/employee/leave">Leave &amp; Permission</a> <a class="btnl" href="/employee/productivity">Productivity Info</a></div>"""

SUMMARY = """<div class="head ov-head"><div><h1>Overview</h1>
<p class="mut">{{label}} &middot; {{wd}} working days (weekly off excluded). Attendance = present days / working days. Productivity = productive hours logged &divide; the daily target of {{target|g}} hrs per present day (capped at 100%).</p></div>
<div class="ov-tools no-print">
<button type="button" class="btnl pbtn" onclick="window.print()" title="Print this overview"><span aria-hidden="true">&#128438;</span> Print</button>
<form class="grid" method="get" style="margin:0"><input type="month" name="month" value="{{month if month!='all' else ''}}">
<button class="primary pbtn">Show</button><a href="/admin/summary?month=all">All time</a></form></div></div>
""" + KPI + """
<div class="card" id="onl"><h2 style="margin:0 0 8px">Online Employees <span class="pill in" id="onl_n">{{online|length}}</span> <small class="mut">live &middot; updates automatically</small></h2>
<table id="onl_t"><tr><th>Employee</th><th>Status</th><th>Online since</th></tr>
{% for r in online %}<tr><td>{{r.id}} &middot; {{r.name}}</td><td><span class="pill {{'in' if r.status=='Online' else 'act'}}">&#9679; {{r.status}}</span></td><td>{{r.since}}</td></tr>
{% else %}<tr><td colspan="3">No employees are online right now.</td></tr>{% endfor %}</table></div>
<script>(function(){var t=document.getElementById('onl_t'),n=document.getElementById('onl_n');if(!t)return;
function cell(tr,txt,cls){var td=tr.insertCell();if(cls){var s=document.createElement('span');s.className='pill '+cls;s.textContent=txt;td.appendChild(s)}else td.textContent=txt}
function draw(list){while(t.rows.length>1)t.deleteRow(1);n.textContent=list.length;
 if(!list.length){var r=t.insertRow(),c=r.insertCell();c.colSpan=3;c.textContent='No employees are online right now.';return}
 list.forEach(function(e){var r=t.insertRow();cell(r,e.id+' · '+e.name);cell(r,'● '+e.status,e.status==='Online'?'in':'act');cell(r,e.since)})}
function poll(){fetch('/admin/online/poll',{credentials:'same-origin',cache:'no-store'}).then(function(r){return r.json()}).then(function(j){draw(j.items)}).catch(function(){})}
setInterval(poll,5000);document.addEventListener('visibilitychange',function(){if(!document.hidden)poll()})})();
</script>
<table><tr><th>Employee</th><th>Designation</th><th>Band</th><th>Present</th><th>Leave</th><th>Absent</th><th>Attendance</th>
<th>Productive hrs</th><th>Non-productive hrs</th><th>Productivity</th></tr>
{% for r in rep %}<tr><td>{{r.id}} &middot; {{r.name}}</td><td>{{r.designation}}</td><td>{{r.band}}</td><td>{{r.present}}</td><td>{{r.leave}}</td><td>{{r.absent}}</td>
{% if r.vo %}<td>-</td><td>-</td><td>-</td><td><span class="pill act">View Only</span></td></tr>{% else %}<td>{{r.att}}%<i class="bar {{r.att|tone}}"><u style="width:{{r.att}}%"></u></i></td>
<td>{{r.prod|g}}</td><td>{{r.non|g}}</td>
<td>{{r.pct}}%<i class="bar {{r.pct|tone}}"><u style="width:{{[r.pct,100]|min}}%"></u></i></td></tr>{% endif %}
{% else %}<tr><td colspan="9">No employees yet.</td></tr>{% endfor %}</table>"""

LEAVE_EMP = """<style>
.lp{font-size:12px}
.lp h1{font-size:18px}.lp h2{font-size:14px;margin:12px 0 6px}
.lp .mut,.lp p{font-size:11.5px;margin:2px 0 6px}
.lp label,.lp input,.lp button,.lp select{font-size:12px}
.lp input,.lp button{padding:5px 8px}
.lp .card{padding:12px 14px}
.lpsum{list-style:none;margin:6px 0 10px;padding:8px 12px;display:flex;flex-wrap:wrap;gap:4px 22px;background:#f7f8fc;border:1px solid var(--line);border-radius:8px;font-size:12px;color:var(--mut)}
.lpsum li{margin:0;line-height:1.4}.lpsum b{color:var(--ink);font-size:12px;font-weight:600}
</style><div class="lp"><div class="head"><h1>Leave &amp; Permission</h1><a href="/employee">Back to daily entry</a></div>

<div class="card"><h2>Apply leave</h2><p class="mut">Up to {{leave_limit|g}} working day(s) of leave per calendar month (weekly-offs and holidays don't count against the limit). A <b>half-day leave</b> counts as 0.5 day, is for one date only, and leaves you 4 working hours that day.</p>
<ul class="lpsum"><li>Monthly Limit: <b>{{leave_limit|g}} day(s)</b></li><li>Used This Month: <b>{{leave_used|g}} day(s)</b></li><li>Remaining: <b>{{leave_remaining|g}} day(s)</b></li></ul>
<form method="post" action="/employee/leave" class="grid">
<label>From date<input type="date" name="d1" value="{{today}}" required></label>
<label>To date<input type="date" name="d2" value="{{today}}" required></label>
<label>Day type<select name="daytype"><option value="Full day">Full day</option><option value="Half day">Half day (4 hrs)</option></select></label>
<label>Reason<input name="reason" size="30" placeholder="Reason"></label>
<button class="primary">Submit leave</button></form></div>
{% if hols %}<p class="mut">&#127774; <b>Upcoming holidays</b> (no leave, permission or productivity entry needed): {% for d,n in hols %}{{d}}{% if n %} - {{n}}{% endif %}{% if not loop.last %}; {% endif %}{% endfor %}</p>{% endif %}
<h2>My leave days</h2><table><tr><th>Date</th><th>Reason</th><th>Applied at</th><th>Status</th><th></th></tr>
{% for r in data %}{% set st = r|lstatus %}<tr><td>{{r['Date']}}</td><td>{{r['Reason']}}{% if r|lhalf %} <span class="pill act">Half day</span>{% endif %}</td><td>{{r['Applied at']|t12}}</td>
<td><span class="pill {{st|ppill}}">{{st}}</span></td>
<td>{% if st=='Pending' %}<form method="post" action="/employee/leave/{{r['_row']}}/delete" onsubmit="return confirm('Cancel this leave?')"><button class="danger">Cancel</button></form>{% else %}-{% endif %}</td></tr>
{% else %}<tr><td colspan="5">No leave yet.</td></tr>{% endfor %}</table>

<div class="card"><h2>Apply permission</h2><p class="mut">Pick the date for your permission (it opens on today, {{today}}) - use it if you need to arrive late, leave early, or step out during work hours. One request per date, up to {{perm_limit|g}} hrs total per calendar month.</p>
<ul class="lpsum"><li>Monthly Limit: <b>{{perm_limit|g}} hrs</b></li><li>Used This Month: <b>{{perm_used|g}} hrs</b></li><li>Remaining: <b>{{perm_remaining|g}} hrs</b></li></ul>
<form method="post" action="/employee/permission" class="grid">
<label>Date<input type="date" name="date" value="{{today}}" required></label>
<label>Hours<input type="number" name="hours" step="0.25" min="0.25" max="{{perm_limit}}" placeholder="e.g. 1" required></label>
<label>Reason<input name="reason" size="30" placeholder="Reason for permission" required></label>
<button class="primary">Submit request</button></form></div>
<h2>My permission requests</h2><table><tr><th>Date</th><th>Hours</th><th>Reason</th><th>Applied at</th><th>Status</th><th></th></tr>
{% for r in perm_data %}<tr><td>{{r['Date']}}</td><td>{{r['Hours']|g}}</td><td>{{r['Reason']}}</td><td>{{r['Applied at']|t12}}</td>
<td><span class="pill {{r['Status']|ppill}}">{{r['Status']}}</span></td>
<td>{% if r['Date'][:7]>=today[:7] %}<details><summary class="mut" style="cursor:pointer">Edit</summary>
<form method="post" action="/employee/permission/{{r['_row']}}/edit" class="grid" style="margin-top:6px"><input type="hidden" name="pid" value="{{r['Permission ID']}}">
<label>Hours<input type="number" name="hours" step="0.25" min="0.25" max="{{perm_limit}}" value="{{r['Hours']|g}}" required></label>
<label>Reason<input name="reason" size="24" value="{{r['Reason']}}" required></label>
<button class="primary sm">Save</button> <button type="button" class="back sm" onclick="if(history.length>1)history.back();else location.href='/employee'">Back</button></form>
{% if r['Status']!='Pending' %}<p class="mut">Saving a change sends this request back to Pending for admin approval.</p>{% endif %}</details>{% endif %}
{% if r['Status']=='Pending' %}<form method="post" action="/employee/permission/{{r['_row']}}/delete" onsubmit="return confirm('Cancel this request?')"><button class="danger">Cancel</button></form>{% elif r['Date'][:7]<today[:7] %}-{% endif %}</td></tr>
{% else %}<tr><td colspan="6">No permission requests yet.</td></tr>{% endfor %}</table></div>"""

LEAVE_ADMIN = """<div class="head"><h1>Leave log</h1></div>
<div class="card"><form method="post" class="grid">
<label>Employee<select name="emp">{% for e in emps %}<option value="{{e['Employee ID']}}">{{e['Employee ID']}} - {{e['Name']}}</option>{% endfor %}</select></label>
<label>From date<input type="date" name="d1" required></label><label>To date<input type="date" name="d2" required></label>
<label>Day type<select name="daytype"><option value="Full day">Full day</option><option value="Half day">Half day (4 hrs)</option></select></label>
<label>Reason<input name="reason" placeholder="Reason"></label><button class="primary">Add leave</button></form></div>
<table><tr><th>Date</th><th>Employee</th><th>Designation</th><th>Band</th><th>Reason</th><th>Applied at</th><th></th></tr>
{% for r in data %}<tr><td>{{r['Date']}}</td><td>{{r['Employee ID']}} &middot; {{r['Employee name']}}</td><td>{{r['Designation']}}</td><td>{{r['Band']}}</td>
<td>{{r['Reason']}}</td><td>{{r['Applied at']|t12}}</td><td class="act"><a href="/admin/leave/{{r['_row']}}">Edit</a>
<form method="post" action="/admin/leave/{{r['_row']}}/delete" onsubmit="return confirm('Delete?')"><button class="danger">Delete</button></form></td></tr>
{% else %}<tr><td colspan="7">No leave records.</td></tr>{% endfor %}</table>"""

PERSONAL_VIEW = """<div class="head"><div><h1>Personal details</h1>
<p class="mut">Admin can edit any employee's details; employees can also update their own from their Personal details page.</p></div>
<button type="button" class="btnl no-print" onclick="window.print()">&#128438; Print</button></div>
<table><tr><th>Emp ID</th><th>Name</th><th>Gender</th><th>Address Line_1</th><th>Address Line_2</th><th>City</th><th>PIN</th>
<th>Phone Number</th><th>Emergency no</th><th>Personal Email ID</th><th>Office Email ID <small>(login)</small></th><th>Last updated</th><th></th></tr>
{% for e in emps %}<tr><td>{{e['Employee ID']}}</td><td>{{e['Name']}}</td><td>{{e['Gender']}}</td><td>{{e['Address Line_1']}}</td><td>{{e['Address Line_2']}}</td>
<td>{{e['City']}}</td><td>{{e['PIN']}}</td><td>{{e['Phone Number']}}</td><td>{{e['Emergency no']}}</td>
<td>{{e['Personal Email ID']}}</td><td>{{e['Email']}}</td><td>{{(e['Profile updated at'] or '-')|t12}}</td><td class="act"><a href="/admin/personal/{{e['_row']}}">Edit</a></td></tr>
{% else %}<tr><td colspan="13">No employees yet.</td></tr>{% endfor %}</table>"""

@app.route("/admin/personal")
@need("admin")
def admin_personal():
    emps = sorted(rows("Employees"), key=lambda e: str(e["Name"]))
    return page(PERSONAL_VIEW, title="Personal details", emps=emps)

PERSONAL_EDIT = """<div class="card"><h2>Edit personal details</h2>
<form method="post" class="grid">
<label>Emp ID<input value="{{emp['Employee ID']}}" readonly></label>
<label>Name<input value="{{emp['Name']}}" readonly></label>
{% for f in fields %}{% if f=='Gender' %}<label>Gender<select name="Gender"><option value="">Select</option>{% for g in ['Male','Female'] %}<option {{'selected' if (emp.get('Gender') or '')|lower==g|lower else ''}}>{{g}}</option>{% endfor %}</select></label>{% else %}<label>{{f}}<input {% if f.endswith('Email ID') %}type="email" {% endif %}name="{{f}}" value="{{emp[f]}}"></label>{% endif %}{% endfor %}
<label>Office Email ID<input value="{{emp['Email']}}" readonly></label>
<button class="primary sm">Save</button> <button type="button" class="back sm" onclick="if(history.length>1)history.back();else location.href='/admin/personal'">Back</button></form>
<p class="mut">Office Email ID is linked to the employee's login email. To change it, edit the Email on the Employees page.</p></div>"""

@app.route("/admin/personal/<int:row>", methods=["GET", "POST"])
@need("admin")
def admin_personal_edit(row):
    heads = HEADERS["Employees"]
    emp = next((e for e in rows("Employees") if e["_row"] == row), None)
    if not emp: abort(404)
    if request.method == "POST":
        ok = save_employee_row(row, emp["Employee ID"], {f: request.form.get(f, "").strip() for f in EDITABLE_PERSONAL})
        flash("Updated." if ok else "Could not save - the employee list changed. Please reopen and try again.")
        return redirect("/admin/personal")
    return page(PERSONAL_EDIT, title="Personal details", emp=emp, fields=EDITABLE_PERSONAL)

@app.route("/admin/summary")
@need("admin")
def admin_summary():
    today = today_local()
    month = request.args.get("month") or today.strftime("%Y-%m")
    subs, leaves = load_subs(), rows("Leave")
    if month == "all":
        ds = [s["date"] for s in subs] + [l["Date"] for l in leaves]
        start, end, label = (dt.date.fromisoformat(min(ds)) if ds else today), today, "All time"
    else:
        start, end = month_range(month); label = start.strftime("%B %Y")
    emps = rows("Employees")
    rep = sorted(report(emps, subs, leaves, start, end), key=lambda r: str(r["name"]))
    std = [r for r in rep if not r.get("vo")]          # Update105: View-Only designations are excluded from the averages
    n = len(std) or 1
    a1, a2 = round(sum(r["att"] for r in std) / n), round(sum(r["pct"] for r in std) / n)
    extra = [("Employees", len(rep)), ("Total leave days", sum(r["leave"] for r in rep))]
    # Missed-entries list is intentionally NOT shown on the Overview page any more;
    # it lives only on the dedicated "Missed entries" page (/admin/missed).
    return page(SUMMARY, title="Overview", rep=rep, month=month, label=label, wd=workdays(start, end),
                lab1="Average attendance", lab2="Average productivity", a1=a1, a2=a2, extra=extra, target=target_hours(),
                online=online_list())

@app.route("/admin/settings/target", methods=["POST"])
@need("admin")
def admin_set_target():
    try:
        v = round(float(request.form.get("target", "").strip()), 2)
        if not 0.5 <= v <= 24: raise ValueError
    except ValueError:
        flash("Enter a daily target between 0.5 and 24 hours."); return redirect("/admin/summary")
    ws = ws_of("Settings")
    keys = ws.col_values(1)
    if TARGET_KEY in keys:
        ws.update(range_name=f"B{keys.index(TARGET_KEY) + 1}", values=[[v]], value_input_option="RAW")
    else:
        ws.append_row([TARGET_KEY, v], value_input_option="RAW")
    invalidate_cache("Settings")
    flash(f"Daily productivity target set to {v:g} hrs. Productivity % now uses this target.")
    return redirect("/admin/summary")

MISSED = """<div class="head"><div><h1>Missed entries</h1>
<p class="mut">{{label}} &middot; Working days (weekly off excluded) with no productivity entry and no leave. Today is not included.</p></div>
<form class="grid" method="get"><input type="month" name="month" value="{{month if month!='all' else ''}}">
<input name="emp" placeholder="Employee ID / name" value="{{emp}}">
<button class="primary">Show</button><a href="/admin/missed">Reset</a><a href="/admin/missed?month=all">All time</a></form></div>
<div class="kpis"><div class="kpi"><span>Missed entries</span><b>{{data|length}}</b></div>
<div class="kpi"><span>Employees affected</span><b>{{n_emp}}</b></div></div>
<p class="no-print"><a class="btnl" href="/admin/missed-log?month={{month}}">&#9993; Open the Missed Entries Log (view per employee &amp; send e-mail)</a></p>
<table><tr><th>Date</th><th>Day</th><th>Employee</th><th>Designation</th><th>Band</th></tr>
{% for r in data %}<tr><td>{{r.date}}</td><td>{{r.day}}</td><td>{{r.id}} &middot; {{r.name}}</td><td>{{r.designation}}</td><td>{{r.band}}</td></tr>
{% else %}<tr><td colspan="5">No missed entries.</td></tr>{% endfor %}</table>"""

PROFILE = """<div class="card"><h2>Personal details</h2>
<p class="mut">Employee ID, name and Office Email ID (your login email) are set by admin. You can update the rest yourself; admin can edit them too.</p>
<form method="post" class="grid">
<label>Emp ID<input value="{{emp['Employee ID']}}" readonly></label>
<label>Name<input value="{{emp['Name']}}" readonly></label>
<label>Address Line_1<input name="Address Line_1" value="{{emp['Address Line_1']}}"></label>
<label>Address Line_2<input name="Address Line_2" value="{{emp['Address Line_2']}}"></label>
<label>City<input name="City" value="{{emp['City']}}"></label>
<label>PIN<input name="PIN" value="{{emp['PIN']}}"></label>
<label>Phone Number<input name="Phone Number" value="{{emp['Phone Number']}}"></label>
<label>Emergency no<input name="Emergency no" value="{{emp['Emergency no']}}"></label>
<label>Personal Email ID<input type="email" name="Personal Email ID" value="{{emp['Personal Email ID']}}"></label>
<label>Office Email ID<input value="{{emp['Email']}}" readonly></label>
<button class="primary sm">Save</button> <button type="button" class="back sm" onclick="if(history.length>1)history.back();else location.href='/employee'">Back</button></form>
<p class="mut" style="margin-top:10px">Last updated: {{(emp['Profile updated at'] or '-')|t12}}</p></div>
<div class="card"><h2>Change password</h2>
<p class="mut">Enter your current password, then choose a new one (at least 6 characters). Use the new password next time you log in.</p>
<form method="post" action="/employee/password" class="grid" autocomplete="off">
<label>Current password<input type="password" name="current" required autocomplete="current-password"></label>
<label>New password<input type="password" name="new" minlength="6" required autocomplete="new-password"></label>
<label>Confirm new password<input type="password" name="confirm" minlength="6" required autocomplete="new-password"></label>
<button class="primary">Change password</button></form></div>"""

@app.route("/admin/missed")
@need("admin")
def admin_missed():
    today = today_local()
    month = request.args.get("month") or today.strftime("%Y-%m")
    q = request.args.get("emp", "").strip().lower()
    subs, leaves, emps = load_subs(), rows("Leave"), rows("Employees")
    if month == "all":
        ds = [s["date"] for s in subs] + [l["Date"] for l in leaves]
        start, label = (dt.date.fromisoformat(min(ds)) if ds else today), "All time"
    else:
        start, _ = month_range(month); label = start.strftime("%B %Y")
    end = today - dt.timedelta(days=1)
    if month != "all":
        end = min(month_range(month)[1], end)
    data = []
    for e in emps:
        if q and q not in (str(e["Employee ID"]).lower(), str(e["Name"]).lower()) \
                and q not in str(e["Name"]).lower():
            continue
        for d in missing_dates(e["Employee ID"], subs, leaves, start, end, fmt="%Y-%m-%d"):
            data.append(dict(date=d, day=dt.date.fromisoformat(d).strftime("%a"),
                             id=e["Employee ID"], name=e["Name"], band=e["Band"],
                             designation=e.get("Designation", "")))
    data.sort(key=lambda r: (r["date"], str(r["name"])), reverse=True)
    return page(MISSED, title="Missed entries", data=data, n_emp=len({r["id"] for r in data}),
                month=month, label=label, emp=request.args.get("emp", ""))


@app.route("/admin/leave", methods=["GET", "POST"])
@need("admin")
def admin_leave():
    emps = rows("Employees")
    if request.method == "POST":
        emp = next((e for e in emps if str(e["Employee ID"]) == request.form["emp"]), None)
        try:
            leave_range_check(request.form['d1'], request.form['d2'])
            flash(f"{add_leave(emp, request.form['d1'], request.form['d2'], request.form['reason'].strip(), status="Approved", day_type=request.form.get('daytype', 'Full day'))} leave day(s) added (holiday dates are skipped).")
        except (ValueError, TypeError) as e:
            flash(str(e))
        return redirect("/admin/leave")
    data = sorted(rows("Leave"), key=lambda r: r["Date"], reverse=True)
    dm = desig_map()
    for r in data: r["Designation"] = dm.get(_key(r["Employee ID"]), "")
    return page(LEAVE_ADMIN, title="Leave log", emps=emps, data=data)

def my_emp():
    return {"Employee ID": session["emp_id"], "Name": session["name"], "Band": session["band"]}

def my_emp_row():
    """Full Employees-sheet record (with _row) for the logged-in employee (looked up once per request)."""
    if has_request_context():
        hit = getattr(request, "_my_emp_row", None)
        if hit is not None and hit.get("Employee ID") == session.get("emp_id"): return hit
    r = my_emp_row_uncached()
    if has_request_context(): request._my_emp_row = r
    return r

def my_emp_row_uncached():
    r = next((e for e in rows("Employees") if str(e["Employee ID"]) == session["emp_id"]), None)
    if not r: abort(404)
    return r

def save_employee_row(row, emp_id, changes):
    """Write changes to one Employees row. Re-reads the row fresh from the sheet (so nothing another
    person just changed is overwritten), writes RAW (so IDs, passwords, phone numbers and PINs are
    stored exactly as typed - leading zeros kept), and stamps 'Profile updated at'.
    Returns False if that row no longer belongs to emp_id."""
    heads = HEADERS["Employees"]
    ws = ws_of("Employees")
    cur = ws.row_values(row); cur += [""] * (len(heads) - len(cur))
    if _key(cur[heads.index("Employee ID")]) != _key(emp_id):
        invalidate_cache("Employees"); return False
    for k, v in changes.items(): cur[heads.index(k)] = v
    cur[heads.index("Office Email ID")] = cur[heads.index("Email")]      # always mirrors the login email
    cur[heads.index("Profile updated at")] = now_local().strftime("%Y-%m-%d %H:%M:%S")
    _with_retry(ws.update, range_name=f"A{row}", values=[cur[:len(heads)]], value_input_option="RAW")
    invalidate_cache("Employees")
    return True

@app.route("/employee/profile", methods=["GET", "POST"])
@need("employee")
def employee_profile():
    emp = my_emp_row()
    if request.method == "POST":
        changes = {f: request.form.get(f, "").strip() for f in EMP_EDITABLE_PERSONAL}
        changed_fields = [f.replace("_", " ") for f in EMP_EDITABLE_PERSONAL
                           if changes[f] != str(emp.get(f, "") or "").strip()]
        change_lines = [field_change(f.replace("_", " "), emp.get(f, ""), changes[f]) for f in EMP_EDITABLE_PERSONAL
                        if changes[f] != str(emp.get(f, "") or "").strip()]
        ok = save_employee_row(emp["_row"], session["emp_id"], changes)
        if ok:
            if changed_fields:      # only log a notification when something was actually changed
                log_change(SEC_PERSONAL, "Updated", "; ".join(change_lines))
            flash("Profile updated. Admin can now see your latest details.")
        else:
            flash("Could not save - please reload the page and try again.")
        return redirect("/employee/profile")
    return page(PROFILE, title="Personal details", emp=emp)

@app.route("/employee/password", methods=["POST"])
@need("employee")
def employee_password():
    emp = my_emp_row()
    cur, new, conf = (request.form.get(k, "") for k in ("current", "new", "confirm"))
    if not eq(cur, emp["Password"]): flash("Current password is incorrect.")
    elif len(new) < 6: flash("New password must be at least 6 characters.")
    elif new != conf: flash("New password and confirmation do not match.")
    elif eq(new, cur): flash("New password must be different from the current one.")
    elif save_employee_row(emp["_row"], session["emp_id"], {"Password": new}):
        log_change("Account", "Updated", "Password")
        flash("Password changed. Use it the next time you log in.")
    else:
        flash("Could not change the password - please reload the page and try again.")
    return redirect("/employee/profile")

@app.route("/employee/leave", methods=["GET", "POST"])
@need("employee")
def employee_leave():
    if request.method == "POST":
        try:
            skipped = leave_range_check(request.form['d1'], request.form['d2'])
            n = add_leave(my_emp(), request.form['d1'], request.form['d2'], request.form['reason'].strip(), day_type=request.form.get('daytype', 'Full day'))
            if n:
                d1, d2, why = request.form['d1'], request.form['d2'], request.form['reason'].strip() or "Leave"
                log_change(SEC_LEAVE, "Added", f"{'Half-day leave' if request.form.get('daytype', '').lower().startswith('half') else 'Leave'} {d1 if d1 == d2 else d1 + ' to ' + d2} ({n} day(s)) \u2013 {_short(why, 80)}")
            flash(("Half-day leave submitted" if request.form.get('daytype', '').lower().startswith('half') and n else f"{n} leave day(s) submitted") + " - waiting for admin approval." +
                  (f" Holiday date(s) {', '.join(skipped)} were skipped (leave is not needed on a holiday)." if skipped else ""))
        except ValueError as e:
            flash(str(e))
        return redirect("/employee/leave")
    data = sorted((r for r in rows("Leave") if str(r["Employee ID"]) == session["emp_id"]),
                  key=lambda r: r["Date"], reverse=True)
    perm_data = sorted((r for r in rows("Permissions") if str(r["Employee ID"]) == session["emp_id"]),
                       key=lambda r: r["Applied at"], reverse=True)
    month = str(today_local())[:7]
    used = permission_hours_used(session["emp_id"], month)
    lv_used = leave_days_used(session["emp_id"], month)
    hols = sorted((d, n) for d, n in holiday_map().items() if d >= str(today_local()))[:10]
    return page(LEAVE_EMP, title="Leave & Permission", hols=hols, data=data, perm_data=perm_data, today=str(today_local()),
                perm_limit=PERMISSION_MONTHLY_LIMIT, perm_used=used,
                perm_remaining=round(PERMISSION_MONTHLY_LIMIT - used, 2),
                leave_limit=LEAVE_MONTHLY_LIMIT, leave_used=lv_used,
                leave_remaining=max(LEAVE_MONTHLY_LIMIT - lv_used, 0))

@app.route("/employee/leave/<int:row>/delete", methods=["POST"])
@need("employee")
def employee_leave_delete(row):
    r = next((r for r in rows("Leave") if r["_row"] == row), None)
    if not r or str(r["Employee ID"]) != session["emp_id"]: abort(403)
    if leave_status(r) != "Pending":
        flash("Only pending leave can be cancelled."); return redirect("/employee/leave")
    ws_of("Leave").delete_rows(row)
    invalidate_cache("Leave")
    log_change(SEC_LEAVE, "Deleted", f"Leave {r['Date']} \u2013 {_short(r.get('Reason', ''), 80)}")
    flash("Leave cancelled."); return redirect("/employee/leave")

@app.route("/employee/permission", methods=["POST"])
@need("employee")
def employee_permission():
    try:
        pdate = request.form.get("date", "").strip() or str(today_local())
        add_permission(my_emp(), request.form.get("reason", "").strip(), request.form.get("hours", ""), pdate)
        log_change(SEC_LEAVE, "Added", f"Permission request for {pdate} ({_fmt_num(round(float(request.form.get('hours', 0)), 2))} hr) "
                                        f"\u2013 {_short(request.form.get('reason', '').strip() or 'Permission', 80)}")
        flash("Permission request submitted for today." if pdate == str(today_local()) else f"Permission request submitted for {pdate}.")
    except ValueError as e:
        flash(str(e))
    return redirect("/employee/leave")

def update_permission(r, hours, reason):
    """Employee edits ONE of their own permission requests (hours + reason). Same rules as applying: > 0 hrs, monthly limit
    (this request's own hours are not counted twice). A change to an Approved / Rejected request returns it to Pending."""
    eid, row = str(r["Employee ID"]), r["_row"]
    if str(r.get("Date", ""))[:7] < str(today_local())[:7]:
        raise ValueError("Permission requests of earlier months cannot be edited.")
    try: hours = round(float(hours), 2)
    except (TypeError, ValueError): raise ValueError("Enter a valid number of permission hours.")
    if hours <= 0: raise ValueError("Permission hours must be greater than 0.")
    reason = " ".join(str(reason or "").split())
    if not reason: raise ValueError("Please enter a reason for the permission.")
    status = str(r.get("Status", "")).strip() or "Pending"
    mine_now = num(r.get("Hours")) if status != "Rejected" else 0.0
    used = permission_hours_used(eid, str(r["Date"])[:7]) - mine_now
    if used + hours > PERMISSION_MONTHLY_LIMIT + 1e-9:
        raise ValueError(f"Monthly permission limit is {PERMISSION_MONTHLY_LIMIT:g} hrs. "
                         f"You have {round(max(PERMISSION_MONTHLY_LIMIT - used, 0), 2):g} hr(s) available for this request.")
    if abs(hours - num(r.get("Hours"))) < 1e-9 and reason == str(r.get("Reason", "")).strip():
        return None                                              # nothing changed
    upd = [{"range": f"F{row}:G{row}", "values": [[hours, reason]]}]
    if status != "Pending": upd.append({"range": f"I{row}:K{row}", "values": [["Pending", "", ""]]})      # needs approval again
    _with_retry(ws_of("Permissions").batch_update, upd, value_input_option="RAW")
    invalidate_cache("Permissions")
    return dict(old_h=num(r.get("Hours")), new_h=hours, back=status != "Pending")

@app.route("/employee/permission/<int:row>/edit", methods=["POST"])
@need("employee")
def employee_permission_edit(row):
    eid = session["emp_id"]
    r = next((r for r in _fetch_rows("Permissions") if r["_row"] == row), None)          # fresh read: row numbers move when others delete
    if not r or _key(r["Employee ID"]) != _key(eid): abort(403)                         # only YOUR OWN records
    if request.form.get("pid", "") != str(r.get("Permission ID", "")):
        flash("That list was out of date - please try again."); return redirect("/employee/leave")
    try:
        res = update_permission(r, request.form.get("hours", ""), request.form.get("reason", ""))
    except ValueError as e:
        flash(str(e)); return redirect("/employee/leave")
    if res is None:
        flash("No changes to save."); return redirect("/employee/leave")
    log_change(SEC_LEAVE, "Updated", f"Permission request for {r['Date']}: {_fmt_num(res['old_h'])} hr \u2192 {_fmt_num(res['new_h'])} hr \u2013 "
                                      f"{_short(' '.join(request.form.get('reason', '').split()), 80)}" + (" (sent back for approval)" if res["back"] else ""))
    flash("Permission request updated." + (" It is Pending again and waits for admin approval." if res["back"] else ""))
    return redirect("/employee/leave")

@app.route("/employee/permission/<int:row>/delete", methods=["POST"])
@need("employee")
def employee_permission_delete(row):
    r = next((r for r in rows("Permissions") if r["_row"] == row), None)
    if not r or str(r["Employee ID"]) != session["emp_id"]: abort(403)
    if str(r.get("Status", "")).strip() != "Pending":
        flash("Only pending requests can be cancelled."); return redirect("/employee/leave")
    ws_of("Permissions").delete_rows(row)
    invalidate_cache("Permissions")
    log_change(SEC_LEAVE, "Deleted", f"Permission request for {r['Date']} "
                                      f"({_fmt_num(num(r.get('Hours')))} hr) \u2013 {_short(r.get('Reason', ''), 80)}")
    flash("Permission request cancelled."); return redirect("/employee/leave")

# ================================================================ Audit Log (Admin-controlled access)
# Admin -> Audit Log: pick an employee, see Productivity + Attendance, and control that employee's
# "Audit Log" access (on/off + which processes they may audit). Permissions live in the "Audit Access"
# sheet (one row per employee). An employee sees "Audit Log" in their menu ONLY while access is enabled.
AUDIT_ALL = "*"          # stored in the Processes column when every process is allowed

def _audit_parse(r):
    """Permission row -> dict. Access is ONLY ever the processes Admin ticked: the old catch-all value '*'
    (from earlier versions) grants nothing now - Admin must tick the processes again."""
    raw = str(r.get("Processes", "")).strip()
    legacy = raw == AUDIT_ALL
    if legacy: raw = ""
    return dict(enabled=str(r.get("Enabled", "")).strip().lower() == "yes", raw=raw, legacy=legacy,
                procs=[p.strip() for p in raw.split("|") if p.strip()],
                updated=str(r.get("Updated at", "")))

def audit_active(acc):
    """Audit Log is available to the employee only while it is switched on AND at least one process is ticked."""
    return bool(acc["enabled"] and acc["procs"])

def audit_access(eid, fresh=False):
    """This employee's Audit Log permission. fresh=True bypasses the cache (used to ENFORCE access, so a
    revoke takes effect on the very next click); the cached read is only used to draw menus and lists."""
    src = _fetch_rows("Audit Access") if fresh else rows("Audit Access")
    for r in src:
        if _key(r.get("Employee ID", "")) == _key(eid):
            return _audit_parse(r)
    return dict(enabled=False, raw="", legacy=False, procs=[], updated="")

def audit_access_map():
    return {_key(r["Employee ID"]): _audit_parse(r) for r in rows("Audit Access") if str(r.get("Employee ID", "")).strip()}

def audit_process_names():
    return [str(r["Process name"]).strip() for r in rows("Processes") if str(r.get("Process name", "")).strip()]

def audit_allowed(acc):
    """Process names Admin ticked for this employee (only those that still exist) - never 'everything'."""
    return [p for p in audit_process_names() if p in acc["procs"]]

def _audit_worked(subs):
    """{EMPLOYEE KEY: {process: [entries, last date]}} - the processes each employee actually logged work on."""
    out = {}
    for s in subs:                                   # subs are newest-first, so the first date seen is the last one
        d = out.setdefault(_key(s["emp_id"]), {})
        for pr in s["procs"]:
            w = d.setdefault(pr["name"], [0, s["date"]]); w[0] += 1
    return out

def audit_write(emp, enabled, raw):
    ws = ws_of("Audit Access")
    ids = ws.col_values(1)
    vals = [str(emp["Employee ID"]), emp["Name"], "Yes" if enabled else "No", raw,
            now_local().strftime("%Y-%m-%d %H:%M:%S"), "Admin"]
    at = next((i for i, v in enumerate(ids) if i > 0 and _key(v) == _key(emp["Employee ID"])), None)
    if at is None: ws.append_row(vals, value_input_option="RAW")
    else: ws.update(range_name=f"A{at + 1}:F{at + 1}", values=[vals], value_input_option="RAW")
    invalidate_cache("Audit Access")

def audit_need(f):
    """Employee-side guard: only employees Admin has enabled may open Audit Log pages."""
    @wraps(f)
    def w(*a, **k):
        acc = audit_access(session.get("emp_id", ""), fresh=True)
        if not audit_active(acc): abort(403)
        return f(acc, *a, **k)
    return w

def _aud_month():
    start, end = month_range(request.args.get("month", ""))
    return start.strftime("%Y-%m"), start, end

def _aud_proc_rows(subs, start, end):
    """Every process line an employee logged in the period (weekly-off days are not counted)."""
    out = []
    for s in subs:
        if s["off"] or not (str(start) <= str(s["date"]) <= str(end)): continue
        for p in s["procs"]:
            out.append(dict(date=s["date"], name=p["name"], hour=p["hour"], count=p["count"], target=p["target"],
                            pct=p["pct"], desc=p["desc"]))
    return sorted(out, key=lambda r: (r["date"], r["name"]), reverse=True)

def _aud_breakdown(lines, names):
    agg = {n: dict(name=n, hour=0.0, count=0.0, target=0.0) for n in names}
    for l in lines:
        if l["name"] in agg:
            a = agg[l["name"]]; a["hour"] += l["hour"]; a["count"] += l["count"]; a["target"] += l["target"] or 0
    for a in agg.values(): a["pct"] = round(a["count"] / a["target"] * 100) if a["target"] else None
    return list(agg.values())

TABS_CONST = """<div class="tabs no-print"><a href="/admin/audit" class="{{'on' if view=='process' else ''}}">By Process</a>
<a href="/admin/audit?view=employee" class="{{'on' if view=='employee' else ''}}">By Employee / Access</a></div>
"""
AUD_LIST = """<div class="head"><div><h1>Audit Log</h1>
<p class="mut">{% if admin %}Employee-wise productivity and attendance. For each employee you can see the processes they work on and tick exactly which processes they may audit.{% else %}Your productivity (for the processes Admin selected) and your attendance.{% endif %}</p></div></div>
<div class="tabs no-print"><a href="/admin/audit" class="{{'on' if view=='process' else ''}}">By Process</a>
<a href="/admin/audit?view=employee" class="{{'on' if view=='employee' else ''}}">By Employee / Access</a></div>
<form class="grid no-print" method="get"><input type="hidden" name="view" value="employee"><input name="q" value="{{q}}" placeholder="Search employee ID or name">
<input type="month" name="month" value="{{month}}"><button class="primary">Show</button><a href="{{base}}?view=employee">Reset</a></form>
<p class="mut">Period: <b>{{label}}</b></p>
<table><tr><th>Employee ID</th><th>Name</th><th>Designation</th><th>Attendance</th><th>Productivity</th>
{% if admin %}<th>Processes worked</th><th>Audit Log access</th><th>Processes allowed</th>{% endif %}<th></th></tr>
{% for r in rep %}<tr><td>{{r.id}}</td><td><a href="{{base}}/{{r.id|urlencode}}"><b>{{r.name}}</b></a></td><td>{{r.designation}}</td>
{% if r.vo %}<td>-</td><td><span class="pill act">View Only</span></td>{% else %}<td>{{r.att}}%</td><td>{{r.pct}}%</td>{% endif %}
{% if admin %}<td>{% if r.worked %}{{r.worked|join(', ')}}{% else %}<span class="mut">No entries yet</span>{% endif %}</td>
<td><span class="pill {{'in' if r.active else 'out'}}">{{'Enabled' if r.active else 'Disabled'}}</span></td>
<td>{% if r.acc.procs %}{{r.acc.procs|join(', ')}}{% if not r.active %} <span class="mut">(switched off)</span>{% endif %}{% else %}<span class="mut">None selected</span>{% endif %}</td>{% endif %}
<td class="act"><a href="{{base}}/{{r.id|urlencode}}">Open</a>
{% if admin %}<a href="{{base}}/{{r.id|urlencode}}?tab=access">Manage access</a>
<form method="post" action="{{base}}/{{r.id|urlencode}}/toggle"><button class="{{'danger' if r.active else 'primary'}}">{{'Disable' if r.active else 'Enable'}}</button></form>{% endif %}</td></tr>
{% else %}<tr><td colspan="9">No employees found.</td></tr>{% endfor %}</table>"""

AUD_HEAD = """<div class="head"><div><h1>{{'Audit Log' if not admin else emp.Name}}</h1>
<p class="mut">{{emp.id}} &middot; {{emp.desig or 'No designation'}} &middot; Band {{emp.band}}{% if not admin %} &middot; {{emp.Name}}{% endif %}</p></div>
{% if admin and process %}<a href="{{base}}?process={{process|urlencode}}&month={{month}}">&larr; {{process}} employees</a>{% elif admin %}<a href="{{base}}?view=employee">&larr; All employees</a>{% endif %}</div>
<div class="tabs no-print">{% for k,l in tabs %}<a href="{{base}}/{{emp.id|urlencode}}?tab={{k}}&month={{month}}{% if process %}&process={{process|urlencode}}{% endif %}" class="{{'on' if k==tab else ''}}">{{l}}</a>{% endfor %}</div>
{% if tab != 'access' %}<form class="grid no-print" method="get"><input type="hidden" name="tab" value="{{tab}}">{% if process %}<input type="hidden" name="process" value="{{process}}">{% endif %}
<input type="month" name="month" value="{{month}}"><button class="primary">Show</button></form>
<p class="mut">Period: <b>{{label}}</b></p>{% endif %}"""

AUD_PROD = """<div class="totals">Working days: <b>{{k.wd}}</b> &middot; Present: <b>{{k.present}}</b> &middot; Productive: <b>{{k.prod|g}}</b> hrs
&middot; Non-productive: <b>{{k.non|g}}</b> hrs &middot; Productivity: <b>{% if k.vo %}View Only{% else %}{{k.pct}}%{% endif %}</b></div>
<h2>Daily entries</h2>
<table><tr><th>Date</th><th>Productive hrs</th><th>Non-productive hrs</th><th>Total</th><th>Productivity</th></tr>
{% for s in subs %}<tr><td>{{s.date}}</td><td>{{s.prod|g}}</td><td>{{s.non|g}}</td><td>{{s.total|g}}</td>
<td>{{ 'Weekend - not counted' if s.off else (s.pct ~ '%') }}</td></tr>
{% else %}<tr><td colspan="5">No productivity entries for this period.</td></tr>{% endfor %}</table>"""

AUD_ATT = """<div class="totals">Working days: <b>{{k.wd}}</b> &middot; Present: <b>{{k.present}}</b> &middot; Leave: <b>{{k.leave}}</b>
&middot; Absent: <b>{{k.absent}}</b> &middot; Attendance: <b>{{k.att}}%</b></div>
<h2>Daily attendance</h2>
<table><tr><th>Date</th><th>Status</th><th>Login</th><th>Logout</th><th>Duration</th><th>Details</th></tr>
{% for d in days %}<tr><td>{{d.date}}</td><td><span class="pill {{'in' if d.status=='Present' else 'out'}}">{{d.status}}</span></td>
<td>{{d.login|t12 or '-'}}</td><td>{{d.logout|t12 or '-'}}</td><td>{{d.dur or '-'}}</td><td>{{d.note or '-'}}</td></tr>
{% else %}<tr><td colspan="6">No days in this period.</td></tr>{% endfor %}</table>
<h2>Login / logout history</h2>
<table><tr><th>Date</th><th>Login</th><th>Logout</th><th>Duration</th><th>Logout type</th></tr>
{% for r in sess %}<tr><td>{{r['Date']}}</td><td>{{r['Login time']|t12 or '-'}}</td><td>{{r['Logout time']|t12 or '-'}}</td>
<td>{{r['Duration'] or '-'}}</td><td>{{r['Logout type'] or 'Active'}}</td></tr>
{% else %}<tr><td colspan="5">No login records for this period.</td></tr>{% endfor %}</table>"""

AUD_PROC = """{% if not allowed %}<div class="card"><p>Admin has not granted you access to any process yet.</p></div>{% else %}
<p class="mut">{% if admin %}Productivity for process: {% else %}Productivity for the process(es) Admin selected for you: {% endif %}<b>{{allowed|join(', ')}}</b></p>
{% if admin and process %}<div class="rep-tools no-print"><button type="button" class="btnl pbtn" onclick="window.print()">&#128438; Print</button>
<a class="btnl pbtn" style="background:#22a06b;box-shadow:0 4px 0 #17734d" href="{{base}}/productivity/export?process={{process|urlencode}}&month={{month}}&emp={{emp.id|urlencode}}">&#128196; Download Excel</a></div>{% endif %}
<h2>Productivity by process</h2>
<table><tr><th>Process</th><th>Hours</th><th>Count</th><th>Target count</th><th>Achievement</th></tr>
{% for b in bd %}<tr><td>{{b.name}}</td><td>{{b.hour|g}}</td><td>{{b.count|g}}</td><td>{{b.target|g}}</td><td>{{ (b.pct ~ '%') if b.pct is not none else '-' }}</td></tr>{% endfor %}</table>
<h2>Your entries</h2>
<table><tr><th>Date</th><th>Process</th><th>Description</th><th>Hours</th><th>Count</th><th>Target count</th><th>Achievement</th></tr>
{% for l in lines %}<tr><td>{{l.date}}</td><td>{{l.name}}</td><td>{{l.desc}}</td><td>{{l.hour|g}}</td><td>{{l.count|g}}</td><td>{{l.target|g}}</td>
<td>{{ (l.pct ~ '%') if l.pct is not none else '-' }}</td></tr>
{% else %}<tr><td colspan="7">No entries for your permitted processes in this period.</td></tr>{% endfor %}</table>{% endif %}"""

AUD_ACCESS = """<div class="card"><h2>Audit Log access &mdash; by process</h2>
<p class="mut">Tick the process(es) <b>{{emp.Name}}</b> may audit. The employee's page then shows <b>Audit Log</b> with two separate sections:
<b>Productivity</b> (only the ticked processes) and <b>Attendance</b>. Un-tick a process and its data is no longer available to the employee;
tick none and the Audit Log disappears. No process is ever included automatically.</p>
{% if acc.legacy %}<p class="flash err">This employee was earlier set to &ldquo;All processes&rdquo;. That option no longer exists &mdash; tick the processes to grant.</p>{% endif %}
<form method="post" action="{{base}}/{{emp.id|urlencode}}/access">
<table><tr><th style="width:70px">Access</th><th>Process</th><th>Worked by this employee</th></tr>
{% for p in procs %}<tr><td><input type="checkbox" name="procs" value="{{p}}" {{'checked' if p in acc.procs}}></td><td>{{p}}</td>
<td>{% if p in worked %}Yes &middot; {{worked[p][0]}} entr{{'y' if worked[p][0]==1 else 'ies'}}, last {{worked[p][1]}}{% else %}<span class="mut">No entries yet</span>{% endif %}</td></tr>
{% else %}<tr><td colspan="3">No processes exist yet. Add them under Processes.</td></tr>{% endfor %}</table><br>
<button class="primary sm">Save permission</button> <button type="button" class="back sm" onclick="if(history.length>1)history.back();else location.href='{{base}}'">Back</button>
{% if acc.updated %}<p class="mut">Last saved: {{acc.updated|t12}}</p>{% endif %}</form></div>"""


def _aud_att_days(eid, subs, sess, start, end):
    """One row per calendar day in the period: Present / Leave / Holiday / Weekly off / Absent + first login, last logout."""
    present = {s["date"] for s in subs if not s["off"] and str(start) <= str(s["date"]) <= str(end)}
    _lv = [l for l in live_leaves(rows("Leave")) if _key(l["Employee ID"]) == _key(eid)]
    leave = {str(l["Date"]): leave_status(l) for l in _lv if not leave_is_half(l)}
    half_days = {str(l["Date"]) for l in _lv if leave_is_half(l)}
    by = {}
    for r in sess: by.setdefault(str(r["Date"]), []).append(r)
    out, d = [], start
    while d <= end:
        ds = str(d); ss = sorted(by.get(ds, []), key=lambda r: str(r["Login time"]))
        note = ""
        if ds in half_days and not is_off(d): st = "Half day"
        elif ds in present: st = "Present"
        elif ds in leave: st, note = "Leave", leave[ds] + " leave"
        elif ds in holiday_map(): st, note = "Holiday", holiday_name(ds)
        elif is_off(d): st = "Weekly off"
        elif d < today_local(): st = "Absent"
        else: st = "-"
        if ds in half_days: note = (note + " · " if note else "") + "Half-day leave (4 hrs)"
        if ss:
            note = (note + " · " if note else "") + f"{len(ss)} login{'s' if len(ss) > 1 else ''}"
        out.append(dict(date=ds, status=st, note=note,
                        login=ss[0]["Login time"] if ss else "",
                        logout=ss[-1]["Logout time"] if ss else "",
                        dur=", ".join(str(r["Duration"]) for r in ss if r.get("Duration"))))
        d += dt.timedelta(days=1)
    return out[::-1]

AUD_PROCESS = """<div class="head"><div><h1>Audit Log</h1>
<p class="mut">Select a process. The employees who worked on it are found automatically, with their productivity, productivity % and attendance.</p></div></div>
""" + TABS_CONST + """<form class="grid no-print" method="get"><select name="process" onchange="this.form.submit()">
<option value="">- Select process -</option>{% for p in procs %}<option value="{{p}}" {{'selected' if p==sel}}>{{p}}</option>{% endfor %}</select>
<input type="month" name="month" value="{{month}}">
{% if sel %}<input name="q" value="{{q}}" placeholder="Search employee ID or name">{% endif %}
<button class="primary">Show</button>
<button type="submit" class="primary" formaction="{{base}}/productivity" onclick="if(!this.form.process.value){alert('Please select a Process first.');return false}">Productivity</button><a href="{{base}}">Reset</a></form>
<p class="mut">Period: <b>{{label}}</b> &middot; Daily target: <b>{{T|g}} hrs</b></p>
{% if not sel %}
<h2>Available processes</h2>
<table><tr><th>Process</th><th>Employees who worked</th><th>Total hours</th><th>Entries</th><th></th></tr>
{% for r in overview %}<tr><td><b>{{r.name}}</b></td><td>{{r.emps}}</td><td>{{r.hour|g}}</td><td>{{r.entries}}</td>
<td class="act"><a href="{{base}}?process={{r.name|urlencode}}&month={{month}}">Open audit</a></td></tr>
{% else %}<tr><td colspan="5">No processes exist yet. Add them under Processes.</td></tr>{% endfor %}</table>
{% else %}
<div class="totals">Process: <b>{{sel}}</b> &middot; Employees: <b>{{rows|length}}</b> &middot; Total hours: <b>{{tot_hour|g}}</b>
&middot; Total count: <b>{{tot_count|g}}</b></div>
<table><tr><th>Employee ID</th><th>Employee</th><th>Process</th><th>Productivity (hrs)</th><th>Avg hrs / day</th><th>Productivity %</th>
<th>Count / Target</th><th>Achievement</th><th>Attendance</th><th>Audit access</th><th></th></tr>
{% for r in rows %}<tr><td>{{r.id}}</td><td><a href="{{base}}/{{r.id|urlencode}}?process={{sel|urlencode}}&month={{month}}"><b>{{r.name}}</b></a><br><span class="mut">{{r.desig}}</span></td>
<td>{{sel}}</td><td>{{r.hour|g}} hrs<br><span class="mut">{{r.days}} day{{'' if r.days==1 else 's'}}, {{r.entries}} entr{{'y' if r.entries==1 else 'ies'}}</span></td>
<td>{{r.avg|g}}</td><td><b>{{r.pct}}%</b></td>
<td>{{r.count|g}} / {{r.target|g}}</td><td>{{ (r.ach ~ '%') if r.ach is not none else '-' }}</td>
<td>{{r.status}}<br><span class="mut">Present {{r.present}} &middot; Leave {{r.leave}} &middot; Absent {{r.absent}} &middot; {{r.att}}%</span></td>
<td><span class="pill {{'in' if r.granted else 'out'}}">{{'Granted' if r.granted else 'Not granted'}}</span></td>
<td class="act"><a href="{{base}}/{{r.id|urlencode}}?process={{sel|urlencode}}&month={{month}}">Productivity</a>
<a href="{{base}}/{{r.id|urlencode}}?tab=attendance&process={{sel|urlencode}}&month={{month}}">Attendance</a></td></tr>
{% else %}<tr><td colspan="11">No employee worked on {{sel}} in this period{% if q %} matching your search{% endif %}.</td></tr>{% endfor %}</table>
<p class="mut">Productivity % = average hours per worked day on this process &divide; the daily target hours. Achievement = count &divide; target count for the hours logged.
Attendance is for the whole period (a day with an entry is Present). &ldquo;Audit access&rdquo; shows whether this employee may view their own audit data for this process.</p>{% endif %}"""

def _audit_process_view(base):
    prefetch("Employees", "Productivity log", "Processes", "Leave", "Permissions", "Settings", "Holidays", "Audit Access")
    month, start, end = _aud_month()
    a, b = str(start), str(end)
    procs = audit_process_names()
    sel = request.args.get("process", "").strip()
    if sel not in procs: sel = ""
    q = request.args.get("q", "").strip().lower()
    T = target_hours()
    subs = [x for x in load_subs() if not is_view_only(x["emp_id"])]          # Update105
    emap = {_key(e["Employee ID"]): e for e in rows("Employees")}
    agg = {}          # process -> {employee key: totals}
    for sub in subs:
        if sub["off"] or not (a <= str(sub["date"]) <= b): continue
        for pr in sub["procs"]:
            e = agg.setdefault(pr["name"], {}).setdefault(_key(sub["emp_id"]), dict(
                id=str(sub["emp_id"]), name=sub["emp_name"], hour=0.0, count=0.0, target=0.0, days=set(), entries=0))
            e["hour"] += pr["hour"]; e["count"] += pr["count"]; e["target"] += pr["target"] or 0
            e["days"].add(sub["date"]); e["entries"] += 1
    ctx = dict(base=base, view="process", procs=procs, sel=sel, q=request.args.get("q", ""), month=month,
               label=start.strftime("%B %Y"), T=T)
    if not sel:
        ctx["overview"] = [dict(name=p, emps=len(agg.get(p, {})), hour=sum(e["hour"] for e in agg.get(p, {}).values()),
                                entries=sum(e["entries"] for e in agg.get(p, {}).values())) for p in procs]
        return page(AUD_PROCESS, title="Audit Log", **ctx)
    workers = [e for e in agg.get(sel, {}).values() if not q or q in e["id"].lower() or q in str(e["name"]).lower()]
    people = [emap.get(_key(e["id"])) or dict(**{"Employee ID": e["id"], "Name": e["name"], "Band": ""}) for e in workers]
    att = {_key(r["id"]): r for r in report(people, subs, rows("Leave"), start, end)}
    amap = audit_access_map(); out = []
    today = str(today_local())
    for e in workers:
        k = att[_key(e["id"])]; acc = amap.get(_key(e["id"]))
        days = len(e["days"]); avg = e["hour"] / days if days else 0
        emp = emap.get(_key(e["id"]), {})
        status = "Present today" if today in e["days"] else ("Attendance recorded")
        out.append(dict(id=e["id"], name=e["name"], desig=emp.get("Designation", ""), hour=round(e["hour"], 2), days=days,
                        entries=e["entries"], avg=round(avg, 2), pct=min(round(avg / T * 100), 100) if T else 0,
                        count=round(e["count"], 2), target=round(e["target"], 1),
                        ach=round(e["count"] / e["target"] * 100) if e["target"] else None,
                        present=k["present"], leave=k["leave"], absent=k["absent"], att=k["att"], status=status,
                        granted=bool(acc and audit_active(acc) and sel in acc["procs"])))
    out.sort(key=lambda r: str(r["name"]).lower())
    ctx.update(rows=out, tot_hour=sum(r["hour"] for r in out), tot_count=sum(r["count"] for r in out))
    return page(AUD_PROCESS, title=f"Audit Log - {sel}", **ctx)

def _audit_list(base, admin):
    prefetch("Employees", "Productivity log", "Processes", "Leave", "Permissions", "Settings", "Holidays", "Audit Access")
    month, start, end = _aud_month()
    q = request.args.get("q", "").strip().lower()
    emps = [e for e in rows("Employees") if not q or q in str(e["Employee ID"]).lower() or q in str(e["Name"]).lower()]
    rep = sorted(report(emps, load_subs(), rows("Leave"), start, end), key=lambda r: str(r["name"]).lower())
    amap = audit_access_map(); worked = _audit_worked(load_subs())
    for r in rep:
        r["acc"] = amap.get(_key(r["id"]), dict(enabled=False, procs=[], raw="", legacy=False, updated=""))
        r["active"] = audit_active(r["acc"])
        r["worked"] = sorted(worked.get(_key(r["id"]), {}))
    return page(AUD_LIST, title="Audit Log", view="employee", rep=rep, base=base, admin=admin, q=request.args.get("q", ""),
                month=month, label=start.strftime("%B %Y"))

def _audit_detail(base, eid, admin, acc=None):
    prefetch("Productivity log", "Processes", "Leave", "Permissions", "Settings", "Holidays", "Attendance")
    emp = emp_or_404(eid); eid = str(emp["Employee ID"])
    if not admin and _key(eid) != _key(session.get("emp_id", "")): abort(403)   # employees: their OWN data only
    tabs = [("productivity", "Productivity"), ("attendance", "Attendance")]
    if admin: tabs.append(("access", "Process Audit Access"))
    tab = request.args.get("tab", "productivity")
    if tab not in dict(tabs): tab = "productivity"
    month, start, end = _aud_month()
    view = dict(id=eid, Name=emp["Name"], desig=emp.get("Designation", ""), band=emp["Band"])   # never expose the password column
    process = request.args.get("process", "").strip() if admin else ""
    if process not in audit_process_names(): process = ""
    ctx = dict(emp=view, base=base, tabs=tabs, tab=tab, month=month, label=start.strftime("%B %Y"), admin=admin, process=process)
    if tab == "access":
        subs = [s for s in load_subs(eid) if _key(s["emp_id"]) == _key(eid)]
        body = AUD_ACCESS
        ctx.update(acc=audit_access(eid, fresh=True), procs=audit_process_names(),
                   worked=_audit_worked(subs).get(_key(eid), {}))
    else:
        subs = [s for s in load_subs(eid) if _key(s["emp_id"]) == _key(eid)]
        k = report([emp], subs, rows("Leave"), start, end)[0]
        if tab == "attendance":                      # separate section: attendance only, no productivity figures
            body = AUD_ATT
            sess = [r for r in rows("Attendance") if _key(r["Employee ID"]) == _key(eid)
                    and str(start) <= str(r["Date"]) <= str(end)]
            sess.sort(key=lambda r: (str(r["Date"]), str(r["Login time"])), reverse=True)
            ctx.update(k=k, sess=sess, days=_aud_att_days(eid, subs, sess, start, end))
        elif admin and process:                      # Admin came from a process: only that process's lines
            lines = [l for l in _aud_proc_rows(subs, start, end) if l["name"] == process]
            body = AUD_PROC
            ctx.update(allowed=[process], lines=lines, bd=_aud_breakdown(lines, [process]))
        elif admin:                                  # Admin sees the employee's complete productivity
            body = AUD_PROD
            ctx.update(k=k, subs=[s for s in subs if str(start) <= str(s["date"]) <= str(end)])
        else:                                        # employee: ONLY the processes Admin ticked, nothing else
            allowed = audit_allowed(acc)
            lines = [l for l in _aud_proc_rows(subs, start, end) if l["name"] in allowed]
            body = AUD_PROC
            ctx.update(allowed=allowed, lines=lines, bd=_aud_breakdown(lines, allowed))
    return page(AUD_HEAD + body, title=f"Audit Log - {emp['Name']}", **ctx)

# ---- Update102: Process + Month Productivity report (page, Print, Excel)
def _aud_prod_report(process, start, end, emp_id=""):
    """All productivity lines for ONE process in ONE month (optionally one employee). Weekly-off days are not counted."""
    T = target_hours()
    emap = {_key(e["Employee ID"]): e for e in rows("Employees")}
    lines, per = [], {}
    for sub in load_subs():
        if is_view_only(sub["emp_id"]): continue                  # Update105
        if sub["off"] or not (str(start) <= str(sub["date"]) <= str(end)): continue
        if emp_id and _key(sub["emp_id"]) != _key(emp_id): continue
        for pr in sub["procs"]:
            if pr["name"] != process: continue
            lines.append(dict(date=str(sub["date"]), id=str(sub["emp_id"]), name=sub["emp_name"], desc=pr["desc"],
                              hour=pr["hour"], count=pr["count"], target=pr["target"] or 0))
            e = per.setdefault(_key(sub["emp_id"]), dict(id=str(sub["emp_id"]), name=sub["emp_name"], hour=0.0, count=0.0,
                                                          target=0.0, days=set(), entries=0))
            e["hour"] += pr["hour"]; e["count"] += pr["count"]; e["target"] += pr["target"] or 0
            e["days"].add(sub["date"]); e["entries"] += 1
    lines.sort(key=lambda r: (r["date"], str(r["name"]).lower()))
    for l in lines: l["ach"] = round(l["count"] / l["target"] * 100) if l["target"] else None
    summary = []
    for e in per.values():
        info = emap.get(_key(e["id"]), {}); d = len(e["days"]); avg = e["hour"] / d if d else 0
        summary.append(dict(id=e["id"], name=e["name"], desig=info.get("Designation", ""), band=info.get("Band", ""),
                            days=d, entries=e["entries"], hour=round(e["hour"], 2), avg=round(avg, 2),
                            pct=min(round(avg / T * 100), 100) if T else 0,
                            count=round(e["count"], 2), target=round(e["target"], 1),
                            ach=round(e["count"] / e["target"] * 100) if e["target"] else None))
    summary.sort(key=lambda r: str(r["name"]).lower())
    th, tc, tt = sum(r["hour"] for r in summary), sum(r["count"] for r in summary), sum(r["target"] for r in summary)
    tot = dict(emps=len(summary), entries=len(lines), hour=round(th, 2), count=round(tc, 2), target=round(tt, 1),
               ach=round(tc / tt * 100) if tt else None)
    emp_name = ""
    if emp_id: emp_name = str((emap.get(_key(emp_id)) or {}).get("Name", emp_id))
    return dict(lines=lines, summary=summary, tot=tot, emp_name=emp_name)

AUD_PROD_REPORT = """<style>.print-only{display:none}@media print{.print-only{display:block}.rep-meta{color:#000}}</style>
<div class="rep-tools no-print"><button type="button" class="btnl pbtn" onclick="window.print()">&#128438; Print</button>
<a class="btnl pbtn" style="background:#22a06b;box-shadow:0 4px 0 #17734d" href="{{base}}/productivity/export?process={{sel|urlencode}}&month={{month}}{% if emp_id %}&emp={{emp_id|urlencode}}{% endif %}">&#128196; Download Excel</a>
<a href="{{base}}?process={{sel|urlencode}}&month={{month}}">&larr; Back to Audit Log</a></div>
<form class="grid no-print" method="get" action="{{base}}/productivity"><select name="process">{% for p in procs %}<option value="{{p}}" {{'selected' if p==sel}}>{{p}}</option>{% endfor %}</select>
<input type="month" name="month" value="{{month}}"><button class="primary">Show</button></form>
<h1 class="rep-title">Productivity Audit Report</h1>
<p class="rep-meta">Process: <b>{{sel}}</b> &middot; Period: <b>{{label}}</b>{% if emp_name %} &middot; Employee: <b>{{emp_name}}</b> <a class="no-print" href="{{base}}/productivity?process={{sel|urlencode}}&month={{month}}">(show all employees)</a>{% endif %} &middot; Generated {{now}}</p>
<div class="totals">Employees: <b>{{tot.emps}}</b> &middot; Entries: <b>{{tot.entries}}</b> &middot; Total hours: <b>{{tot.hour|g}}</b> &middot; Total count: <b>{{tot.count|g}}</b>
&middot; Target count: <b>{{tot.target|g}}</b> &middot; Achievement: <b>{{ (tot.ach ~ '%') if tot.ach is not none else '-' }}</b></div>
<h2>Productivity by employee</h2>
<table><tr><th>Employee ID</th><th>Employee</th><th>Designation</th><th>Days worked</th><th>Hours</th><th>Avg hrs / day</th><th>Productivity %</th><th>Count</th><th>Target count</th><th>Achievement</th></tr>
{% for r in summary %}<tr><td>{{r.id}}</td><td>{{r.name}}</td><td>{{r.desig or '-'}}</td><td>{{r.days}}</td><td>{{r.hour|g}}</td><td>{{r.avg|g}}</td><td>{{r.pct}}%</td><td>{{r.count|g}}</td><td>{{r.target|g}}</td><td>{{ (r.ach ~ '%') if r.ach is not none else '-' }}</td></tr>
{% else %}<tr><td colspan="10">No entries for {{sel}} in {{label}}.</td></tr>{% endfor %}
{% if summary %}<tr style="font-weight:700"><td colspan="4">Total</td><td>{{tot.hour|g}}</td><td></td><td></td><td>{{tot.count|g}}</td><td>{{tot.target|g}}</td><td>{{ (tot.ach ~ '%') if tot.ach is not none else '-' }}</td></tr>{% endif %}</table>
<h2>Entries</h2>
<table><tr><th>Date</th><th>Employee ID</th><th>Employee</th><th>Process</th><th>Description</th><th>Hours</th><th>Count</th><th>Target count</th><th>Achievement</th></tr>
{% for l in lines %}<tr><td>{{l.date}}</td><td>{{l.id}}</td><td>{{l.name}}</td><td>{{sel}}</td><td>{{l.desc or '-'}}</td><td>{{l.hour|g}}</td><td>{{l.count|g}}</td><td>{{l.target|g}}</td><td>{{ (l.ach ~ '%') if l.ach is not none else '-' }}</td></tr>
{% else %}<tr><td colspan="9">No entries for {{sel}} in {{label}}.</td></tr>{% endfor %}</table>
<p class="mut">Productivity % = average hours per worked day on this process &divide; the daily target hours. Achievement = count &divide; target count. Weekly-off days are not counted.</p>
<p class="print-only mut">Audit report &mdash; {{sel}} &middot; {{label}} &middot; generated {{now}}</p>
{% if autoprint %}<script>window.addEventListener('load',function(){setTimeout(function(){window.print()},350)})</script>{% endif %}"""

def _aud_prod_args():
    """Validate Process + Month from the query string. Returns (process, month, start, end, emp_id) or None."""
    process = request.args.get("process", "").strip()
    if process not in audit_process_names(): return None
    month, start, end = _aud_month()
    return process, month, start, end, request.args.get("emp", "").strip()

@app.route("/admin/audit/productivity")
@need("admin")
def admin_audit_productivity():
    prefetch("Employees", "Productivity log", "Processes", "Settings", "Holidays")
    a = _aud_prod_args()
    if not a:
        flash("Please select a Process first.", "err")
        return redirect("/admin/audit")
    process, month, start, end, emp_id = a
    r = _aud_prod_report(process, start, end, emp_id)
    return page(AUD_PROD_REPORT, title=f"Productivity - {process}", base="/admin/audit", sel=process, month=month,
                label=start.strftime("%B %Y"), procs=audit_process_names(), emp_id=emp_id,
                now=now_local().strftime("%Y-%m-%d %I:%M %p"), autoprint=request.args.get("print") == "1", **r)

AUD_SUM_HEADS = ["Employee ID", "Employee name", "Designation", "Band", "Days worked", "Entries", "Hours",
                 "Avg hrs / day", "Productivity %", "Count", "Target count", "Achievement %"]
AUD_LINE_HEADS = ["Date", "Employee ID", "Employee name", "Process", "Description", "Hours", "Count",
                  "Target count", "Achievement %"]

@app.route("/admin/audit/productivity/export")
@need("admin")
def admin_audit_productivity_export():
    prefetch("Employees", "Productivity log", "Processes", "Settings", "Holidays")
    a = _aud_prod_args()
    if not a:
        flash("Please select a Process first.", "err")
        return redirect("/admin/audit")
    process, month, start, end, emp_id = a
    r = _aud_prod_report(process, start, end, emp_id)
    label = start.strftime("%B %Y")
    fname = "Audit_Productivity_" + re.sub(r"[^A-Za-z0-9]+", "_", process).strip("_") + "_" + month
    srows = [[x["id"], x["name"], x["desig"], x["band"], x["days"], x["entries"], x["hour"], x["avg"], x["pct"] / 100,
              x["count"], x["target"], (x["ach"] / 100 if x["ach"] is not None else "")] for x in r["summary"]]
    lrows = [[x["date"], x["id"], x["name"], process, x["desc"], x["hour"], x["count"], x["target"],
              (x["ach"] / 100 if x["ach"] is not None else "")] for x in r["lines"]]
    t = r["tot"]
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:      # openpyxl not installed: still give a file Excel opens
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow([f"Productivity Audit Report - {process} - {label}"]); w.writerow(AUD_SUM_HEADS)
        w.writerows([[("" if v is None else v) for v in row] for row in srows])
        w.writerow([]); w.writerow(AUD_LINE_HEADS); w.writerows(lrows)
        return Response("\ufeff" + buf.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": f'attachment; filename="{fname}.csv"'})
    wb = Workbook()
    hfill = PatternFill("solid", fgColor="4F46E5"); tfill = PatternFill("solid", fgColor="E8EAFB")
    thin = Side(style="thin", color="D9DCEB")
    meta = [("Process", process), ("Period", label)]
    if r["emp_name"]: meta.append(("Employee", r["emp_name"]))
    meta.append(("Generated", now_local().strftime("%Y-%m-%d %I:%M %p")))
    def sheet(ws, title, heads, data, widths, pct_cols, total_row):
        ws.title = title
        ws.append(["Productivity Audit Report"]); ws["A1"].font = Font(bold=True, size=14)
        for k, v in meta:
            ws.append([k, v]); ws.cell(ws.max_row, 1).font = Font(bold=True)
        ws.append([])
        hr = ws.max_row + 1
        ws.append(heads)
        for c in ws[hr]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = hfill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[hr].height = 30
        for row in data: ws.append(["" if v is None else v for v in row])
        last = ws.max_row
        if total_row:
            ws.append(total_row); last = ws.max_row
            for c in ws[last]: c.font = Font(bold=True); c.fill = tfill
        for row in ws.iter_rows(min_row=hr + 1, max_row=last):
            for c in row:
                c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
                if c.column in pct_cols: c.number_format = "0%"
                if isinstance(c.value, (int, float)): c.alignment = Alignment(horizontal="right")
        for i, wd in enumerate(widths, start=1): ws.column_dimensions[get_column_letter(i)].width = wd
        ws.freeze_panes = ws.cell(hr + 1, 1)
        if data: ws.auto_filter.ref = f"A{hr}:{get_column_letter(len(heads))}{hr + len(data)}"
        ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_title_rows = f"{hr}:{hr}"
    ach = (t["ach"] / 100) if t["ach"] is not None else ""
    sheet(wb.active, "Summary", AUD_SUM_HEADS, srows, [13, 24, 22, 8, 12, 9, 10, 13, 15, 10, 13, 15], {9, 12},
          ["Total", "", "", "", "", t["entries"], t["hour"], "", "", t["count"], t["target"], ach] if srows else None)
    sheet(wb.create_sheet(), "Entries", AUD_LINE_HEADS, lrows, [12, 13, 24, 22, 34, 9, 9, 13, 15], {9},
          ["Total", "", "", "", "", t["hour"], t["count"], t["target"], ach] if lrows else None)
    out = io.BytesIO(); wb.save(out)
    return Response(out.getvalue(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": f'attachment; filename="{fname}.xlsx"'})

# ---- Admin side
@app.route("/admin/audit")
@need("admin")
def admin_audit():
    if request.args.get("view") == "employee": return _audit_list("/admin/audit", True)
    return _audit_process_view("/admin/audit")

@app.route("/admin/audit/<eid>")
@need("admin")
def admin_audit_detail(eid): return _audit_detail("/admin/audit", eid, True)

@app.route("/admin/audit/<eid>/access", methods=["POST"])
@need("admin")
def admin_audit_save(eid):
    emp = emp_or_404(eid)
    valid = audit_process_names()
    picked = [p for p in request.form.getlist("procs") if p in valid]     # only real, ticked processes
    audit_write(emp, bool(picked), " | ".join(picked))
    flash(f"Audit Log access for {emp['Name']}: " + (", ".join(picked) if picked else "no process selected - Audit Log is off") + ".")
    return redirect(f"/admin/audit/{emp['Employee ID']}?tab=access")

@app.route("/admin/audit/<eid>/toggle", methods=["POST"])
@need("admin")
def admin_audit_toggle(eid):
    emp = emp_or_404(eid)
    cur = audit_access(str(emp["Employee ID"]), fresh=True)
    if audit_active(cur):
        audit_write(emp, False, cur["raw"])                # switched off; the ticked processes are remembered
        flash(f"Audit Log disabled for {emp['Name']}.")
    elif cur["procs"]:
        audit_write(emp, True, cur["raw"])
        flash(f"Audit Log enabled for {emp['Name']} ({', '.join(cur['procs'])}).")
    else:
        flash(f"Tick the process(es) {emp['Name']} may audit first.")
        return redirect(f"/admin/audit/{emp['Employee ID']}?tab=access")
    return redirect(request.referrer or "/admin/audit")

# ---- Employee side (only for employees Admin has given at least one process)
@app.route("/employee/audit")
@need("employee")
@audit_need
def employee_audit(acc): return _audit_detail("/employee/audit", session["emp_id"], False, acc)

@app.route("/employee/audit/<eid>")
@need("employee")
@audit_need
def employee_audit_detail(acc, eid): return _audit_detail("/employee/audit", eid, False, acc)   # 403 unless it is their own ID

# ================================================================ Mahizhchi (Question & Answer)  - Update62
# Admin keeps multiple-choice questions in the "Mahizhchi Log" Google Sheet (or pastes them on the Admin page):
#     Question | A | B | C | D | Correct Answer
# The correct option carries ONE tick mark (✓) - either in the option cell ("Pacific Ocean ✓"), in the
# Correct Answer column ("C"), or both (they must agree). Admin publishes the log and chooses which employees
# may see it ("Mahizhchi Access" sheet). Employees tick ONE option per question and submit (saved once, in the
# "Mahizhchi Answers" sheet, under their own ID only). They can never edit questions/options/the correct answer,
# and the correct answer is never included in anything sent to them. Reachable only while published AND shared.
import re as _re, hashlib as _hl
MZ_TITLE = "Mahizhchi"
MZ_SHEET, MZ_ACCESS_SHEET, MZ_ANS_SHEET, MZ_ATT_SHEET = "Mahizhchi Log", "Mahizhchi Access", "Mahizhchi Answers", "Mahizhchi Attempts"
MZ_TIME_LIMIT = int(os.getenv("MZ_TIME_SECONDS", "150"))   # quiz time limit per employee (seconds) - 2 minutes 30 seconds
MZ_SETS = int(os.getenv("MZ_SETS", "5"))                      # Update84: number of Sets in the quiz
MZ_PER_SET = int(os.getenv("MZ_PER_SET", "10"))              # questions in each Set (ALL must be answered to complete a Set)
MZ_WIN_CORRECT = min(MZ_PER_SET, int(os.getenv("MZ_WIN_CORRECT", str(MZ_PER_SET))))   # correct answers needed to WIN a Set (default: all 10)
MZ_CSHEET, MZ_CATT_SHEET = "Mahizhchi Connections", "Mahizhchi Connection Attempts"
MZ_CONN_TIME = int(os.getenv("MZ_CONN_SECONDS", "180"))       # Update85: Connection Game time limit (seconds)
MZ_CONN_MISTAKES = int(os.getenv("MZ_CONN_MISTAKES", "4"))    # wrong guesses allowed before the game is lost
_rs = os.getenv("MZ_RETRY_SETS", "all").replace(" ", "").lower()      # Update87: "all" (default) = EVERY Set can be retried until it is completed
MZ_RETRY_SETS = set(range(1, MZ_SETS + 1)) if _rs == "all" else {int(x) for x in _rs.split(",") if x.isdigit()}   # Update86: Sets that keep coming back until every question is answered correctly
MZ_ANNOUNCE_TO = os.getenv("MZ_ANNOUNCE_TO", "all")           # Update86: "all" = every logged-in employee sees set winners; "access" = only employees who can open Mahizhchi
MZ_GRACE = 8                                                # seconds of network delay tolerated when the page auto-submits at 0:00
def _mz_dur(sec):
    m, r = divmod(int(sec), 60)
    parts = ([f"{m} minute{'s' if m != 1 else ''}"] if m else []) + ([f"{r} second{'s' if r != 1 else ''}"] if r or not m else [])
    return " ".join(parts)
app.jinja_env.globals["mz_dur"] = _mz_dur
MZ_LETTERS = "ABCD"
MZ_TICKS = "✓✔☑✅"                      # any of these typed by Admin is treated as "the correct answer" and shown as ✓
MZ_PUB_KEY = "Mahizhchi Log published"   # row in the Settings sheet: Yes / No
MZ_MAX_PASTE = 60000                     # characters accepted in one paste
app.jinja_env.globals["MZ_TITLE"] = MZ_TITLE

def _mz_strip(v):
    """(text without any tick marks, whether a tick mark was present)."""
    s = str(v if v is not None else "")
    has = any(t in s for t in MZ_TICKS)
    for t in MZ_TICKS: s = s.replace(t, "")
    return " ".join(s.split()), has

def mz_parse(r):
    """One sheet row -> question dict, or None for a blank row. 'ok' is True only when there are >= 2 options and
    EXACTLY one correct answer that every marker (tick / Correct Answer column) agrees on. Rows that are not ok
    are shown to Admin with the reason and are NEVER shown to employees."""
    q = _re.sub(r"^\s*\d+\s*[.)]\s+", "", str(r.get("Question", "") or "").strip())
    if not q: return None
    opts, ticked, issues = [], [], []
    for L in MZ_LETTERS:
        txt, has = _mz_strip(r.get(L, ""))
        if txt:
            opts.append(dict(letter=L, text=txt))
            if has: ticked.append(L)
        elif has:
            issues.append(f"Option {L} has a ✓ but no answer text")
    letters = [o["letter"] for o in opts]
    if len(opts) < 2: issues.append("Needs at least 2 answer options")
    ca_raw, _ = _mz_strip(r.get("Correct Answer", ""))
    ca = None
    if ca_raw:
        t = ca_raw.strip(" .:()").upper()
        if t in letters: ca = t
        else:
            m = [o["letter"] for o in opts if o["text"].casefold() == ca_raw.casefold()]
            if len(m) == 1: ca = m[0]
            else: issues.append(f"Correct Answer “{ca_raw}” does not match any option")
    if len(ticked) > 1: issues.append("More than one option has a ✓ (only one correct answer is allowed)")
    tk = ticked[0] if len(ticked) == 1 else None
    if ca and tk and ca != tk: issues.append(f"Correct Answer column says {ca} but the ✓ is on {tk}")
    correct = ca or tk
    if not correct and not issues: issues.append("No correct answer marked (put a ✓ or fill the Correct Answer column)")
    qid = _hl.sha1(q.casefold().encode("utf-8")).hexdigest()[:10]      # stable id from the question text (survives row moves)
    return dict(row=r.get("_row"), qid=qid, q=q, opts=opts, correct=None if issues else correct, issues=issues, ok=not issues)

def mz_questions():
    out, seen = [], set()
    for r in rows(MZ_SHEET):
        p = mz_parse(r)
        if not p: continue
        if p["qid"] in seen:
            p["issues"].append("Duplicate question (the same text appears earlier)"); p["ok"] = False; p["correct"] = None
        seen.add(p["qid"]); out.append(p)
    return out

def mz_my_answers(eid, fresh=False):
    """{question id: letter} this employee has already submitted."""
    src = _fetch_rows(MZ_ANS_SHEET) if fresh else rows(MZ_ANS_SHEET)
    return {str(r.get("Question ID", "")).strip(): str(r.get("Answer", "")).strip().upper()
            for r in src if _key(r.get("Employee ID", "")) == _key(eid)}

def mz_split(qs):
    """Update84: ready questions in sheet order -> Sets. Questions 1-10 = Set 1, 11-20 = Set 2 ... Only FULL Sets are offered."""
    ok = [q for q in qs if q["ok"]]
    return [ok[i * MZ_PER_SET:(i + 1) * MZ_PER_SET] for i in range(MZ_SETS) if len(ok[i * MZ_PER_SET:(i + 1) * MZ_PER_SET]) == MZ_PER_SET]

def mz_order(eid, setno, setqs):
    """Update84: this employee's own random order for a Set. Seeded by employee ID + Set, so it differs between employees
    but stays the same for the same employee if the page is reloaded."""
    seed = int(_hl.sha1(f"mz|{_key(eid)}|{setno}".encode("utf-8")).hexdigest()[:12], 16)
    out = list(setqs); random.Random(seed).shuffle(out)
    return out

def mz_attempts_from(src, eid):
    """{set number: attempt} for one employee from Attempts-sheet rows (rows with no Set value are old Update62 rows = Set 1)."""
    out = {}
    for r in src:
        if _key(r.get("Employee ID", "")) != _key(eid): continue
        try: n = int(str(r.get("Set", "")).strip() or 1)
        except ValueError: n = 1
        if n in out: continue
        try: start = dt.datetime.strptime(str(r.get("Started at", "")).strip(), "%Y-%m-%d %H:%M:%S")
        except ValueError: start = dt.datetime(2000, 1, 1)          # unreadable start time -> treat the Set as long over
        try: extra = max(0, int(str(r.get("Extra seconds", "")).strip() or 0))      # Update84: time Admin has added to this Set
        except ValueError: extra = 0
        out[n] = dict(row=r["_row"], start=start, closed=bool(str(r.get("Closed at", "")).strip()), set=n, extra=extra)
    return out

def mz_attempts(eid):
    """This employee's Set attempts (always read fresh - the deadline must be exact)."""
    return mz_attempts_from(_fetch_rows(MZ_ATT_SHEET), eid)

def mz_seconds_left(att):
    lim = MZ_TIME_LIMIT + att.get("extra", 0)
    return max(0, min(lim, int(lim - (now_local() - att["start"]).total_seconds())))

def mz_extend(att, add_sec):
    """Update84: Admin adds time to ONE employee's Set - even after it expired or closed. The employee then gets exactly
    add_sec seconds from now (if the Set is still running the time is simply added to what is left). A closed Set is re-opened."""
    el = (now_local() - att["start"]).total_seconds()
    lim = MZ_TIME_LIMIT + att.get("extra", 0)
    extra = att.get("extra", 0) + add_sec if el <= lim else int(el - MZ_TIME_LIMIT) + add_sec
    r = att["row"]; upd = [{"range": f"I{r}", "values": [[extra]]}]
    if att["closed"] or el > lim:
        upd += [{"range": f"D{r}", "values": [[""]]}, {"range": f"F{r}:H{r}", "values": [["", "", ""]]}]
    _with_retry(ws_of(MZ_ATT_SHEET).batch_update, upd, value_input_option="RAW")
    invalidate_cache(MZ_ATT_SHEET)

def mz_close_attempt(att, answered, correct, won):
    r = att["row"]
    _with_retry(ws_of(MZ_ATT_SHEET).batch_update,
                [{"range": f"D{r}", "values": [[now_local().strftime("%Y-%m-%d %H:%M:%S")]]},
                 {"range": f"E{r}:H{r}", "values": [[att["set"], answered, correct, "Won" if won else ("Retry" if att["set"] in MZ_RETRY_SETS else "Not won")]]}],
                value_input_option="RAW")
    invalidate_cache(MZ_ATT_SHEET)

def mz_score(setqs, done, n=None):
    """(answered, correct, won) for one Set. A Set is WON only when every question is answered AND >= MZ_WIN_CORRECT are right."""
    a = sum(1 for q in setqs if q["qid"] in done)
    c = sum(1 for q in setqs if done.get(q["qid"]) == q["correct"])
    need = len(setqs) if n in MZ_RETRY_SETS else MZ_WIN_CORRECT      # retry Sets are only won with EVERY question correct
    return a, c, (a == len(setqs) and c >= need)

def mz_progress(eid, sets_q, atts, done, finalize=False):
    """Per-Set status: won / failed / active / open (can start now) / locked (earlier Set not won yet).
    finalize=True also closes (and records the result of) any Set whose time has run out - the Set closes by itself."""
    out, prev_won = [], True
    for n, sq in enumerate(sets_q, start=1):
        att = atts.get(n); a, c, won = mz_score(sq, done, n); left = 0
        if att:
            left = 0 if att["closed"] else mz_seconds_left(att)
            if left > 0: st = "active"
            else:
                if finalize and not att["closed"]: mz_close_attempt(att, a, c, won)
                st = "won" if won else ("failed" if n not in MZ_RETRY_SETS else ("open" if prev_won else "locked"))   # retry Set: just try again
        else: st = "open" if prev_won else "locked"
        out.append(dict(n=n, status=st, answered=a, correct=c, total=len(sq), left=left, att=att))
        prev_won = prev_won and st == "won"
    return out

def mz_status_text(prog):
    if prog and all(p["status"] == "won" for p in prog) and len(prog) >= MZ_SETS: return "Completed"
    won_n = sum(1 for p in prog if p["status"] == "won")
    f = next((p for p in prog if p["status"] == "failed"), None)
    if f: return f"Not won - stopped at Set {f['n']}"
    a = next((p for p in prog if p["status"] == "active"), None)
    if a: return f"In progress - Set {a['n']}"
    t = next((p for p in prog if p["status"] == "open" and p["att"]), None)
    if t: return f"Try again - Set {t['n']}"                        # Update87: an incomplete Set that can be attempted again
    return f"Next: Set {won_n + 1}" if won_n else "Not started"

def mz_detail(emp):
    """Everything Admin sees about ONE employee's Mahizhchi attempt (used by Results and by Employee Info -> Mahizhchi Log)."""
    eid = str(emp["Employee ID"]); sets_q = mz_split(mz_questions())
    mine = mz_my_answers(eid); prog = mz_progress(eid, sets_q, mz_attempts(eid), mine)
    sets = []
    for p, sq in zip(prog, sets_q):
        order = mz_order(eid, p["n"], sq)
        sets.append(dict(n=p["n"], status=p["status"], extra=p["att"]["extra"] if p["att"] else 0, can_add=bool(p["att"]) and p["status"] != "won", answered=p["answered"], correct=p["correct"], total=p["total"],
                         started=p["att"]["start"].strftime("%Y-%m-%d %H:%M:%S") if p["att"] else "",
                         lines=[dict(q=q, mine=mine.get(q["qid"])) for q in order]))
    return dict(eid=eid, name=emp["Name"], sets=sets, nsets=MZ_SETS, won_n=sum(1 for p in prog if p["status"] == "won"),
                status=mz_status_text(prog), need=MZ_WIN_CORRECT, per=MZ_PER_SET,
                shared=mz_access_map().get(_key(eid), False), pub=mz_published(), conn=mz_conn_detail(eid))

def mz_results(qs):
    """{employee key: dict(last, answered, prog)} scored against the CURRENT correct answers (Admin side only)."""
    sets_q = mz_split(qs); valid = {q["qid"] for sq in sets_q for q in sq}
    ans, last = {}, {}
    for r in rows(MZ_ANS_SHEET):
        qid = str(r.get("Question ID", "")).strip()
        if qid not in valid: continue
        k = _key(r.get("Employee ID", ""))
        ans.setdefault(k, {})[qid] = str(r.get("Answer", "")).strip().upper()
        last[k] = max(last.get(k, ""), str(r.get("Submitted at", "")))
    att_rows = rows(MZ_ATT_SHEET); crows = rows(MZ_CATT_SHEET); per = {}
    for k in set(ans) | {_key(r.get("Employee ID", "")) for r in att_rows}:
        if not k: continue
        prog = mz_progress(k, sets_q, mz_attempts_from(att_rows, k), ans.get(k, {}))
        ca = next((mz_conn_parse(r) for r in crows if _key(r.get("Employee ID", "")) == k), None)
        per[k] = dict(last=last.get(k, ""), answered=sum(p["answered"] for p in prog), prog=prog, conn=mz_conn_status(ca),
                      won_n=sum(1 for p in prog if p["status"] == "won"), status=mz_status_text(prog))
    return per

# ---- Update85: Connection Game - BONUS ROUND, playable only by employees who have won all Sets.
# Find 4 hidden groups of 4 words (16 words). Every guess is checked on the SERVER; the groups are never sent to the browser
# until they are solved (or the game is over). Each employee sees the 16 words in their own random order.
def mz_conn_puzzles():
    """{game id: puzzle} from the 'Mahizhchi Connections' sheet. A puzzle is ready only with exactly 4 groups of 4 distinct words."""
    out = {}
    for r in rows(MZ_CSHEET):
        gid = str(r.get("Game", "")).strip(); name = " ".join(str(r.get("Group name", "")).split())
        if not gid and not name: continue
        p = out.setdefault(gid, dict(id=gid, groups=[], issues=[], ok=False))
        p["groups"].append(dict(name=name, words=[" ".join(str(r.get(f"Word {i}", "")).split()) for i in range(1, 5)], row=r.get("_row")))
    for p in out.values():
        if len(p["groups"]) != 4: p["issues"].append(f"Needs exactly 4 groups (has {len(p['groups'])})")
        seen = set()
        for g in p["groups"]:
            if not g["name"]: p["issues"].append("A group has no name")
            if any(not w for w in g["words"]): p["issues"].append(f"Group “{g['name']}” needs 4 words")
            for w in g["words"]:
                if w and w.casefold() in seen: p["issues"].append(f"Word “{w}” appears twice (all 16 words must be different)")
                seen.add(w.casefold())
        p["ok"] = not p["issues"]
    return out

def mz_conn_parse_paste(text, next_id):
    """Paste layout: one group per line  'Group name: word1, word2, word3, word4'; 4 lines = one puzzle; blank line between puzzles."""
    blocks, cur = [], []
    for line in str(text).replace("\r", "").split("\n"):
        if line.strip(): cur.append(line.strip())
        elif cur: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    good, bad, gid = [], [], next_id
    for n, b in enumerate(blocks, start=1):
        rws, why, seen = [], None, set()
        for ln in b:
            m = _re.match(r"^(.+?)\s*[:\-\u2013]\s*(.+)$", ln)
            if not m: why = f"line “{_short(ln, 30)}” should look like  Group name: w1, w2, w3, w4"; break
            ws = [" ".join(w.split()) for w in _re.split(r"[,|]", m.group(2)) if w.strip()]
            if len(ws) != 4: why = f"group “{_short(m.group(1), 30)}” has {len(ws)} words (need 4)"; break
            for w in ws:
                if w.casefold() in seen: why = f"word “{w}” appears twice"; break
                seen.add(w.casefold())
            if why: break
            rws.append([str(gid), m.group(1).strip()] + ws)
        if not why and len(rws) != 4: why = f"has {len(rws)} groups (need exactly 4)"
        if why: bad.append(f"Puzzle {n}: {why}"); continue
        good += rws; gid += 1
    return good, bad

def mz_conn_parse(r):
    try: start = dt.datetime.strptime(str(r.get("Started at", "")).strip(), "%Y-%m-%d %H:%M:%S")
    except ValueError: start = dt.datetime(2000, 1, 1)
    try: extra = max(0, int(str(r.get("Extra seconds", "")).strip() or 0))
    except ValueError: extra = 0
    try: mist = int(str(r.get("Mistakes", "")).strip() or 0)
    except ValueError: mist = 0
    solved = [int(x) for x in str(r.get("Solved", "")).split(",") if x.strip().isdigit()]
    return dict(row=r["_row"], game=str(r.get("Game", "")).strip(), start=start, closed=bool(str(r.get("Closed at", "")).strip()),
                solved=solved, mistakes=mist, result=str(r.get("Result", "")).strip(), extra=extra)

def mz_conn_attempt(eid, fresh=True):
    src = _fetch_rows(MZ_CATT_SHEET) if fresh else rows(MZ_CATT_SHEET)
    r = next((r for r in src if _key(r.get("Employee ID", "")) == _key(eid)), None)
    return mz_conn_parse(r) if r else None

def mz_conn_left(att):
    lim = MZ_CONN_TIME + att["extra"]
    return max(0, min(lim, int(lim - (now_local() - att["start"]).total_seconds())))

def mz_conn_status(att):
    if not att: return "—"
    if att["result"]: return att["result"]
    return "Playing" if mz_conn_left(att) > 0 else "Lost"

def mz_conn_save(att, solved, mistakes, result):
    r = att["row"]; closed = now_local().strftime("%Y-%m-%d %H:%M:%S") if result else ""
    _with_retry(ws_of(MZ_CATT_SHEET).update, range_name=f"E{r}:H{r}",
                values=[[closed, ",".join(str(i) for i in solved), mistakes, result]], value_input_option="RAW")
    invalidate_cache(MZ_CATT_SHEET)
    att.update(solved=list(solved), mistakes=mistakes, result=result, closed=bool(result))

def mz_conn_norm(w): return " ".join(str(w).split()).casefold()

def mz_conn_judge(puz, solved, pick):
    """-> ('invalid'|'correct'|'one_away'|'wrong', group index or None) for a guess of 4 words."""
    pk = {mz_conn_norm(w) for w in pick}
    open_g = [i for i in range(len(puz["groups"])) if i not in solved]
    pool = {mz_conn_norm(w) for i in open_g for w in puz["groups"][i]["words"]}
    if len(pk) != 4 or not pk <= pool: return "invalid", None
    best = 0
    for i in open_g:
        gs = {mz_conn_norm(w) for w in puz["groups"][i]["words"]}
        if gs == pk: return "correct", i
        best = max(best, len(gs & pk))
    return ("one_away" if best == 3 else "wrong"), None

def mz_all_won(eid):
    sets_q = mz_split(mz_questions())
    if len(sets_q) < MZ_SETS: return False
    prog = mz_progress(eid, sets_q, mz_attempts(eid), mz_my_answers(eid, fresh=True))
    return len(prog) >= MZ_SETS and all(p["status"] == "won" for p in prog)

def mz_conn_pick(eid, puzzles):
    ready = sorted((p for p in puzzles.values() if p["ok"]), key=lambda p: p["id"])
    if not ready: return None
    return ready[int(_hl.sha1(f"cg|{_key(eid)}".encode("utf-8")).hexdigest()[:8], 16) % len(ready)]

TONES = ["t0", "t1", "t2", "t3"]

def mz_conn_ctx(eid):
    """What the employee page shows for the Connection Game (None = nothing to show)."""
    puzzles = mz_conn_puzzles(); att = mz_conn_attempt(eid)
    base = dict(limit=MZ_CONN_TIME, max_m=MZ_CONN_MISTAKES)
    if not att:
        return dict(base, state="intro") if mz_conn_pick(eid, puzzles) else None
    puz = puzzles.get(att["game"])
    if not puz or not puz["ok"]: return None
    if not att["result"] and mz_conn_left(att) == 0: mz_conn_save(att, att["solved"], att["mistakes"], "Lost")     # time over -> closes by itself
    solved = [dict(name=puz["groups"][i]["name"], words=puz["groups"][i]["words"], tone=TONES[i]) for i in att["solved"]]
    allw = [w for g in puz["groups"] for w in g["words"]]
    random.Random(int(_hl.sha1(f"cgw|{_key(eid)}|{puz['id']}".encode("utf-8")).hexdigest()[:12], 16)).shuffle(allw)
    done_w = {mz_conn_norm(w) for sg in solved for w in sg["words"]}
    words = [w for w in allw if mz_conn_norm(w) not in done_w]
    ctx = dict(base, state=("won" if att["result"] == "Won" else "lost" if att["result"] else "active"), solved=solved, words=words,
               mistakes=att["mistakes"], remaining=0 if att["result"] else mz_conn_left(att), reveal=[])
    if ctx["state"] == "lost":
        ctx["reveal"] = [dict(name=puz["groups"][i]["name"], words=puz["groups"][i]["words"], tone=TONES[i])
                         for i in range(4) if i not in att["solved"]]
    return ctx

def mz_conn_detail(eid):
    att = mz_conn_attempt(eid)
    if not att: return None
    return dict(status=mz_conn_status(att), solved=len(att["solved"]), mistakes=att["mistakes"], max_m=MZ_CONN_MISTAKES, extra=att["extra"],
                started=att["start"].strftime("%Y-%m-%d %H:%M:%S"), game=att["game"],
                can_add=att["result"] != "Won" and att["mistakes"] < MZ_CONN_MISTAKES)

def mz_conn_extend(att, add_sec):
    """Admin adds time (also after it expired): the employee gets add_sec seconds from now; a time-closed game is re-opened."""
    el = (now_local() - att["start"]).total_seconds(); lim = MZ_CONN_TIME + att["extra"]
    extra = att["extra"] + add_sec if el <= lim else int(el - MZ_CONN_TIME) + add_sec
    r = att["row"]
    upd = [{"range": f"I{r}", "values": [[extra]]}]
    if att["closed"] or el > lim: upd += [{"range": f"E{r}", "values": [[""]]}, {"range": f"H{r}", "values": [[""]]}]
    _with_retry(ws_of(MZ_CATT_SHEET).batch_update, upd, value_input_option="RAW")
    invalidate_cache(MZ_CATT_SHEET)

def mz_set_winners():
    """{set n: dict(id, name, at)} - the FIRST employee to WIN each Set (earliest 'Closed at' of a 'Won' attempt; sheet order breaks ties)."""
    best = {}
    for r in rows(MZ_ATT_SHEET):
        if str(r.get("Result", "")).strip() != "Won": continue
        at = str(r.get("Closed at", "")).strip()
        if not at: continue
        try: n = int(str(r.get("Set", "")).strip() or 1)
        except ValueError: continue
        key = (at, r["_row"])
        if n not in best or key < best[n][0]: best[n] = (key, r)
    return {n: dict(id=str(r.get("Employee ID", "")), name=str(r.get("Employee name", "")), at=k[0]) for n, (k, r) in best.items()}

def mz_overall_winner(nsets):
    """Update87: the FIRST employee to complete ALL Sets = overall winner. Completion time = when their LAST Set was won; ties -> sheet order."""
    if nsets < 1: return None
    per = {}
    for r in rows(MZ_ATT_SHEET):
        if str(r.get("Result", "")).strip() != "Won": continue
        at = str(r.get("Closed at", "")).strip()
        try: n = int(str(r.get("Set", "")).strip() or 1)
        except ValueError: continue
        if not at or not 1 <= n <= nsets: continue
        d = per.setdefault(_key(r.get("Employee ID", "")), dict(id=str(r.get("Employee ID", "")), name=str(r.get("Employee name", "")), row=r["_row"], sets={}))
        if n not in d["sets"] or at < d["sets"][n]: d["sets"][n] = at
    done = [(max(d["sets"].values()), d["row"], d) for d in per.values() if len(d["sets"]) == nsets]
    if not done: return None
    at, _row, d = min(done, key=lambda x: (x[0], x[1]))
    return dict(id=d["id"], name=d["name"], at=at, text="🏆 " + d["name"] + " is the overall winner - first to complete all Sets!")

def mz_board(nsets):
    w = mz_set_winners()
    return [dict(n=n, name=w[n]["name"] if n in w else None,
                 text=("🏆 " + w[n]["name"] + " has completed Set " + str(n) + " first!") if n in w else "") for n in range(1, nsets + 1)]

def mz_can_see_board(eid):
    """Winner board / notifications: only while Mahizhchi is published; every logged-in employee (MZ_ANNOUNCE_TO=all) or only those with access."""
    try: return bool(eid) and mz_published() and (MZ_ANNOUNCE_TO == "all" or mz_access_map().get(_key(eid), False))
    except Exception: return False

def mz_published(fresh=False):
    src = _fetch_rows("Settings") if fresh else rows("Settings")
    r = next((r for r in src if str(r.get("Key", "")).strip() == MZ_PUB_KEY), None)
    return bool(r) and str(r.get("Value", "")).strip().lower() == "yes"

def mz_set_published(on):
    ws = ws_of("Settings"); keys = ws.col_values(1); val = "Yes" if on else "No"
    if MZ_PUB_KEY in keys: ws.update(range_name=f"B{keys.index(MZ_PUB_KEY) + 1}", values=[[val]], value_input_option="RAW")
    else: ws.append_row([MZ_PUB_KEY, val], value_input_option="RAW")
    invalidate_cache("Settings")

def mz_access_map(fresh=False):
    src = _fetch_rows(MZ_ACCESS_SHEET) if fresh else rows(MZ_ACCESS_SHEET)
    return {_key(r["Employee ID"]): str(r.get("Enabled", "")).strip().lower() == "yes"
            for r in src if str(r.get("Employee ID", "")).strip()}

def mz_active(eid, fresh=False):
    """True only while the log is PUBLISHED and shared with this employee. fresh=True (used to ENFORCE access)
    bypasses the cache so a revoke/unpublish takes effect on the very next click; the cached form only draws the menu."""
    return bool(eid) and mz_published(fresh) and mz_access_map(fresh).get(_key(eid), False)

def mz_set_access(emps, enabled):
    """Share / un-share for many employees with one read + one write (not one call per employee)."""
    if not emps: return
    ws = ws_of(MZ_ACCESS_SHEET)
    vals = _with_retry(ws.get_all_values)
    idx = {_key(row[0]): i for i, row in enumerate(vals, start=1) if i > 1 and row and row[0].strip()}
    stamp = now_local().strftime("%Y-%m-%d %H:%M:%S")
    upd, new = [], []
    for e in emps:
        row = [str(e["Employee ID"]), e["Name"], "Yes" if enabled else "No", stamp, "Admin"]
        i = idx.get(_key(e["Employee ID"]))
        if i: upd.append({"range": f"A{i}:E{i}", "values": [row]})
        else: new.append(row)
    if upd: _with_retry(ws.batch_update, upd, value_input_option="RAW")
    if new: _with_retry(ws.append_rows, new, value_input_option="RAW")
    invalidate_cache(MZ_ACCESS_SHEET)

# ---- paste importer: understands the layout Admin types, e.g.
#   1. Which is the largest ocean on Earth?
#   A. Atlantic Ocean   B. Indian Ocean   C. Pacific Ocean ✓   D. Arctic Ocean       (one option per line)
_MZ_OPT = _re.compile(r"^\s*\(?([A-Za-z])\s*[.):]\s*(.*?)\s*$")
_MZ_NUM = _re.compile(r"^\s*(?:Q(?:uestion)?\s*)?\d+\s*[.):\-]\s*(.+?)\s*$", _re.I)
_MZ_LABEL = _re.compile(r"^\s*(questions?|options?|answers?)\s*:?\s*$", _re.I)

def mz_parse_paste(text):
    """Pasted text -> (rows ready for the sheet, list of problems). Only questions with 2-4 options and exactly
    one ✓ are accepted; anything else is reported and skipped, never guessed."""
    blocks, cur = [], None
    for line in str(text).replace("\r", "").split("\n"):
        if not line.strip() or _MZ_LABEL.match(line): continue
        mo = _MZ_OPT.match(line)
        if mo and cur is not None:
            cur["opts"].append((mo.group(1).upper(), mo.group(2))); continue
        mn = _MZ_NUM.match(line)
        if mn: cur = dict(q=mn.group(1), opts=[]); blocks.append(cur); continue
        if cur is not None and not cur["opts"]: cur["q"] += " " + line.strip(); continue      # question wrapped over 2 lines
        if cur is not None and cur["opts"]: a, b = cur["opts"][-1]; cur["opts"][-1] = (a, (b + " " + line.strip()).strip()); continue
        cur = dict(q=line.strip(), opts=[]); blocks.append(cur)                              # un-numbered question
    good, bad = [], []
    for n, b in enumerate(blocks, start=1):
        q, _ = _mz_strip(b["q"]); why = None
        letters = [a for a, _ in b["opts"]]
        texts = {a: _mz_strip(t) for a, t in b["opts"]}
        ticks = [a for a in letters if texts[a][1]]
        if not q: why = "empty question"
        elif not (2 <= len(letters) <= len(MZ_LETTERS)): why = f"has {len(letters)} options (need 2 to {len(MZ_LETTERS)})"
        elif letters != list(MZ_LETTERS[:len(letters)]): why = "options must be lettered A, B, C, D in order"
        elif any(not texts[a][0] for a in letters): why = "an option is empty"
        elif len(ticks) != 1: why = "no ✓ found" if not ticks else "more than one ✓ (only one correct answer is allowed)"
        if why: bad.append(f"Question {n} (“{_short(q, 40)}”): {why}"); continue
        row = [q] + [(texts[L][0] + (" ✓" if L in ticks else "")) if L in texts else "" for L in MZ_LETTERS] + [ticks[0]]
        good.append(row)
    return good, bad

# ---- templates
MZ_CSS = """<style>
.mz-q{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 12px}
.mz-q h3{margin:0 0 8px;font-size:15px;line-height:1.5}.mz-q .no{color:var(--mut);font-weight:700;margin-right:6px}
.mz-o{display:flex;gap:10px;align-items:baseline;padding:7px 10px;border-radius:8px;border:1px solid transparent;margin:3px 0}
.mz-o .l{min-width:22px;color:var(--mut);font-weight:700}
.mz-o.ok{background:#e3f6ec;border-color:#9bd7b5;color:#146c43;font-weight:600}
.mz-o .tick{font-weight:800;color:#146c43;white-space:nowrap}
.mz-q.bad{border-color:#fca5a5;background:#fff8f8}.mz-issue{color:#991b1b;font-size:13px;margin:8px 0 0}
.mz-row{font-size:12px;color:var(--mut);margin-top:6px}
.mz-o.pick{cursor:pointer;align-items:center}.mz-o.pick:hover{background:#eef0ff;border-color:#d6d9ff}
.mz-o.pick input{margin:0}.mz-o.mine{background:#eef0ff;border-color:#b9bdf5;font-weight:600}
.mz-timer{position:sticky;top:0;z-index:5;background:#eef0ff;border:1px solid #d6d9ff;border-radius:10px;padding:9px 14px;margin:0 0 12px;font-weight:700}
.mz-timer.low{background:#fef2f2;border-color:#fca5a5;color:#991b1b}
.mz-locked .mz-o{opacity:.55;pointer-events:none}
.mz-stats{display:flex;gap:18px;flex-wrap:wrap;margin:6px 0 4px}
/* Update83: employee Mahizhchi page on a background PNG - content sits on frosted white so it stays readable */
.mz-stage{position:relative;isolation:isolate;border-radius:18px;padding:22px;margin:0 0 16px;min-height:62vh;background:linear-gradient(135deg,#eef0ff,#fdf2f8 55%,#fff7e6)}
.mz-stage.has-bg{background:var(--mzbg) center/cover no-repeat,linear-gradient(135deg,#eef0ff,#fdf2f8)}
.mz-stage.has-bg::before{content:'';position:absolute;inset:0;z-index:-1;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,.6))}
.mz-stage .head{margin-bottom:14px}
.mz-stage .head h1{display:inline-block;margin:0;padding:6px 18px;border-radius:12px;background:rgba(255,255,255,.92);box-shadow:0 4px 14px -6px rgba(28,35,64,.35)}
.mz-stage .card,.mz-stage .mz-q{background:rgba(255,255,255,.97);border:1px solid rgba(255,255,255,.9);box-shadow:0 8px 24px -12px rgba(28,35,64,.4);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);color:var(--ink)}
.mz-stage .flash{background:rgba(255,255,255,.95);color:var(--ink);font-weight:600}
.mz-stage .mz-timer{background:rgba(238,240,255,.97);box-shadow:0 6px 18px -8px rgba(28,35,64,.45)}
.mz-stage .mz-timer.low{background:rgba(254,242,242,.98)}
.mz-stage button.primary{padding:10px 24px;font-size:15px;box-shadow:0 0 0 4px rgba(255,255,255,.85),0 8px 18px -6px rgba(79,70,229,.6)}
@media(max-width:800px){.mz-stage{padding:12px;border-radius:12px;min-height:50vh}.mz-stage .head h1{font-size:22px;padding:4px 12px}}
/* Update83: animated "Mahizhchi" access highlight */
.mz-run{display:inline-flex;font-weight:800;letter-spacing:.4px;white-space:nowrap}
.mz-run span{display:inline-block;background:linear-gradient(90deg,#4f46e5,#ec4899,#f59e0b,#10b981,#4f46e5);background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;
animation:mzIn .45s ease both,mzWave 1.8s ease-in-out infinite,mzShine 4s linear infinite;
animation-delay:calc(var(--i)*.08s),calc(var(--i)*.08s + .7s),calc(var(--i)*-.2s)}
.mz-run.lg{font-size:24px}
.mz-badge{position:relative;display:inline-flex;align-items:center;gap:8px;padding:2px 12px;border-radius:999px;border:1.5px solid transparent;
background:linear-gradient(#fff,#fff) padding-box,linear-gradient(120deg,#4f46e5,#ec4899,#f59e0b) border-box;animation:mzGlow 2.4s ease-in-out infinite}
.mz-badge .mz-lbl{font-size:11px;font-weight:700;color:#146c43;background:#e3f6ec;border-radius:10px;padding:1px 8px}
.mz-em{position:absolute;font-size:13px;line-height:1;pointer-events:none;opacity:0;animation:mzFloat 2.8s ease-in-out infinite}
.mz-em.e1{left:-8px;top:-9px}.mz-em.e2{right:14px;top:-13px;animation-delay:.7s}.mz-em.e3{left:42%;top:-14px;animation-delay:1.4s}.mz-em.e4{right:-9px;bottom:-9px;animation-delay:2.1s}
.mz-badge:not(.burst) .mz-em{display:none}
tr.mz-new td{animation:mzRow 2.6s ease-out 1}
.mz-cele{position:relative;overflow:hidden;display:flex;align-items:center;gap:12px;flex-wrap:wrap;border-radius:14px;padding:14px 18px;margin:0 0 14px;
background:linear-gradient(120deg,#eef0ff,#fdf2f8,#fff7e6);border:1px solid #d6d9ff;animation:mzDrop .6s cubic-bezier(.2,1.2,.4,1) both}
.mz-cele .big{font-size:26px;animation:mzBounce 1.2s ease-in-out infinite}
.mz-cele .txt{color:var(--ink);font-weight:600}
.mz-conf{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.mz-conf span{position:absolute;top:-24px;font-size:16px;opacity:0;animation:mzFall 3s linear 2}
@keyframes mzIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes mzWave{0%,55%,100%{transform:translateY(0) scale(1)}25%{transform:translateY(-5px) scale(1.18)}}
@keyframes mzShine{to{background-position:300% 0}}
@keyframes mzGlow{0%,100%{box-shadow:0 0 0 0 rgba(79,70,229,.0)}50%{box-shadow:0 0 12px 2px rgba(236,72,153,.28)}}
@keyframes mzFloat{0%{opacity:0;transform:translateY(6px) scale(.5) rotate(0)}25%{opacity:1}70%{opacity:1;transform:translateY(-8px) scale(1.1) rotate(14deg)}100%{opacity:0;transform:translateY(-17px) scale(.6) rotate(-10deg)}}
@keyframes mzRow{0%,30%{background:#e9e7ff}100%{background:transparent}}
@keyframes mzDrop{from{opacity:0;transform:translateY(-14px) scale(.96)}to{opacity:1;transform:none}}
@keyframes mzBounce{0%,100%{transform:translateY(0) rotate(-6deg)}50%{transform:translateY(-6px) rotate(8deg)}}
@keyframes mzFall{0%{opacity:0;transform:translateY(0) rotate(0)}10%{opacity:1}100%{opacity:0;transform:translateY(120px) rotate(280deg)}}
@media(prefers-reduced-motion:reduce){.mz-run span{animation:none!important;opacity:1}.mz-em,.mz-conf{display:none}.mz-badge,.mz-cele .big,tr.mz-new td{animation:none!important}}
</style>
{% macro mzrun() %}<span class="mz-run" aria-label="Mahizhchi">{% for ch in 'Mahizhchi' %}<span aria-hidden="true" style="--i:{{loop.index0}}">{{ch}}</span>{% endfor %}</span>{% endmacro %}
{% macro mzbadge(label, burst) %}<span class="mz-badge {{'burst' if burst}}"><span class="mz-em e1">✨</span><span class="mz-em e2">🎉</span><span class="mz-em e3">🌟</span><span class="mz-em e4">🎊</span>{{ mzrun() }}<span class="mz-lbl">{{label}}</span></span>{% endmacro %}
{% macro mzcard(q, n, admin) %}<div class="mz-q {{'bad' if q.issues}}"><h3><span class="no">{{n}}.</span>{{q.q}}</h3>
{% for o in q.opts %}<div class="mz-o {{'ok' if o.letter==q.correct}}"><span class="l">{{o.letter}}.</span><span>{{o.text}}{% if o.letter==q.correct %} <span class="tick" title="Correct answer">&#10003;</span>{% endif %}</span></div>{% endfor %}
{% for i in q.issues %}<p class="mz-issue">&#9888; {{i}}</p>{% endfor %}
{% if admin %}<div class="mz-row">Sheet row {{q.row}}{% if q.set %} &middot; <b>Set {{q.set}}</b>{% endif %}{% if not q.issues %} &middot; correct answer: <b>{{q.correct}}</b>{% else %} &middot; <b>hidden from employees until fixed</b>{% endif %}</div>{% endif %}</div>{% endmacro %}
"""

MZ_TABS = """<div class="tabs no-print"><a href="/admin/mahizhchi" class="{{'on' if tab=='questions' else ''}}">Questions</a>
<a href="/admin/mahizhchi?tab=access" class="{{'on' if tab=='access' else ''}}">Share / Access</a>
<a href="/admin/mahizhchi?tab=add" class="{{'on' if tab=='add' else ''}}">Paste questions</a>
<a href="/admin/mahizhchi?tab=results" class="{{'on' if tab=='results' else ''}}">Results</a></div>"""

MZ_HEAD = """<div class="head"><div><h1>{{MZ_TITLE}}</h1>
<p class="mut">Admin sets the questions and the ✓ correct answer. Employees tick their own answer; they never see the correct one.</p></div></div>""" + MZ_TABS

MZ_ADMIN_Q = MZ_CSS + MZ_HEAD + """
<div class="card"><h2>Status: <span class="pill {{'in' if pub else 'out'}}">{{'Published' if pub else 'Not published'}}</span></h2>
<div class="mz-stats"><span>Questions: <b>{{qs|length}}</b></span><span>Ready: <b>{{ok_n}}</b></span>
<span>Need fixing: <b>{{qs|length - ok_n}}</b></span><span>Shared with: <b>{{shared_n}}</b> of <b>{{emp_n}}</b> employees</span><span>Sets ready: <b>{{sets_n}}</b> of <b>{{nsets}}</b> ({{per}} questions each)</span><span>Time limit: <b>{{mz_dur(limit)}}</b> per Set</span><span>To win a Set: answer all {{per}}, at least <b>{{need}}</b> correct</span></div>
{% if sets_n < nsets %}<p class="mz-issue">&#9888; Only {{sets_n}} full Set(s) are ready. Questions are grouped in sheet order: rows 1-{{per}} = Set 1, next {{per}} = Set 2 and so on. Add {{nsets*per - ok_n}} more ready question(s) so all {{nsets}} Sets can be played.</p>{% endif %}
<p class="mut">{% if pub %}Employees it is shared with can answer the {{ok_n}} ready question(s); the ✓ correct answer is never shown to them. Un-publish to hide it from everyone at once.
{% else %}Nobody but you can see the log until you publish it <i>and</i> share it with employees (Share / Access tab).{% endif %}</p>
<form method="post" action="/admin/mahizhchi/publish" style="display:inline">
<input type="hidden" name="on" value="{{0 if pub else 1}}"><button class="{{'danger' if pub else 'primary'}}">{{'Un-publish' if pub else 'Publish'}}</button></form>
<a class="btnl" href="https://docs.google.com/spreadsheets/d/{{sheet_id}}" target="_blank" rel="noopener">Open Google Sheet &#8599;</a>
<p class="mut">In the sheet use the tab <b>{{sheet}}</b>: columns <b>Question, A, B, C, D, Correct Answer</b>. Mark the right option with one ✓ (e.g. <i>Pacific Ocean ✓</i>; only you see it) and/or put its letter in Correct Answer.</p></div>
{% for q in qs %}{{ mzcard(q, loop.index, true) }}{% else %}<div class="card"><p>No questions yet. Add rows in the Google Sheet or use <a href="/admin/mahizhchi?tab=add">Paste questions</a>.</p></div>{% endfor %}"""

MZ_ADMIN_ACCESS = MZ_CSS + MZ_HEAD + """
{% if granted %}<div class="mz-cele"><span class="mz-conf" aria-hidden="true">{% for em in ['🎉','✨','🎊','⭐','💫','🎈','🌟','🎉','✨','🎊'] %}<span style="left:{{ 4 + loop.index0*10 }}%;animation-delay:{{ loop.index0*0.25 }}s">{{em}}</span>{% endfor %}</span>
<span class="big">🎉</span>{{ mzrun() }}<span class="txt">access granted to {{granted}} employee{{'s' if granted != 1}}!</span></div>{% endif %}
<div class="card"><h2>Who can see the {{MZ_TITLE}}</h2>
<p class="mut">Status: <span class="pill {{'in' if pub else 'out'}}">{{'Published' if pub else 'Not published'}}</span>
{% if not pub %} &mdash; nothing is visible to employees while un-published.{% endif %} Sharing with someone publishes it automatically.
Employees who are not ticked here do not see the menu item and cannot open the page.</p>
<form class="grid no-print" method="get"><input type="hidden" name="tab" value="access"><input name="q" value="{{q}}" placeholder="Search employee ID or name"><button class="primary">Search</button><a href="/admin/mahizhchi?tab=access">Reset</a></form>
<form method="post" action="/admin/mahizhchi/access">
<table><tr><th style="width:44px"><input type="checkbox" onclick="document.querySelectorAll('.mzc').forEach(c=>c.checked=this.checked)" title="Select all shown"></th>
<th>Employee ID</th><th>Name</th><th>Designation</th><th>Employee sees the menu?</th></tr>
{% for e in emps %}{% set sh = amap.get(e['Employee ID']|string|trim|upper) %}{% set isnew = sh and (newall or (e['Employee ID']|string|trim|upper) in newset) %}<tr class="{{'mz-new' if isnew}}"><td><input class="mzc" type="checkbox" name="ids" value="{{e['Employee ID']}}"></td><td>{{e['Employee ID']}}</td><td>{{e['Name']}}</td><td>{{e.get('Designation','')}}</td>
<td>{% if sh and pub %}{{ mzbadge('Access enabled', isnew) }}{% else %}<span class="pill {{'act' if sh else 'out'}}">{{'Shared - NOT published' if sh else 'No access'}}</span>{% endif %}</td></tr>
{% else %}<tr><td colspan="5">No employees found.</td></tr>{% endfor %}</table><br>
<button class="primary" name="action" value="share_selected">Share with selected</button>
<button class="danger" name="action" value="revoke_selected">Remove from selected</button>
<button class="primary" name="action" value="share_all" onclick="return confirm('Share the {{MZ_TITLE}} with ALL employees?')">Share with all</button>
<button class="danger" name="action" value="revoke_all" onclick="return confirm('Remove access from ALL employees?')">Remove from all</button></form></div>"""

MZ_ADMIN_CONN = MZ_CSS + MZ_HEAD + """<div class="card"><h2>Connection Game &mdash; bonus round</h2>
<p class="mut">Only employees who have <b>won all {{nsets}} Sets</b> can play. They must find the <b>4 hidden groups of 4 words</b> within <b>{{mz_dur(limit)}}</b> with at most <b>{{max_m}}</b> mistakes.
Each employee sees the 16 words in their own order. If several ready puzzles exist, each employee is given one of them automatically. Sheet tab: <b>{{sheet}}</b> (columns Game, Group name, Word 1&ndash;4; 4 rows per Game).</p>
<form method="post" action="/admin/mahizhchi/connect/import"><textarea name="text" rows="9" maxlength="{{maxlen}}" required style="width:100%;font-family:inherit" placeholder="Planets: Mars, Venus, Saturn, Mercury&#10;Fruits: Apple, Mango, Grape, Lemon&#10;Colours: Red, Blue, Green, Yellow&#10;Metals: Iron, Copper, Gold, Silver&#10;&#10;(leave a blank line, then paste the next puzzle)"></textarea><br><br>
<button class="primary">Add puzzle(s) to sheet</button></form></div>
{% for p in puzzles %}<div class="card"><h2>Puzzle {{p.id}} <span class="pill {{'in' if p.ok else 'out'}}">{{'Ready' if p.ok else 'Needs fixing - hidden from employees'}}</span></h2>
{% for g in p.groups %}<div class="mz-o ok"><span class="l">{{loop.index}}.</span><span><b>{{g.name}}</b>: {{g.words|join(', ')}}</span></div>{% endfor %}
{% for i in p.issues %}<p class="mz-issue">&#9888; {{i}}</p>{% endfor %}</div>{% else %}<div class="card"><p>No Connection puzzles yet. Paste one above or add rows in the Google Sheet.</p></div>{% endfor %}"""

MZ_ADMIN_ADD = MZ_CSS + MZ_HEAD + """
<div class="card"><h2>Paste questions</h2>
<p class="mut">Paste questions in this layout &mdash; one ✓ on the correct option. They are added to the <b>{{sheet}}</b> sheet (existing rows are not changed).
A question is skipped, and reported, if it has no ✓, more than one ✓, or fewer than 2 options.</p>
<form method="post" action="/admin/mahizhchi/import">
<textarea name="text" rows="14" maxlength="{{maxlen}}" required style="width:100%;font-family:inherit" placeholder="1. Which is the largest ocean on Earth?&#10;A. Atlantic Ocean&#10;B. Indian Ocean&#10;C. Pacific Ocean ✓&#10;D. Arctic Ocean"></textarea><br><br>
<button class="primary">Add to sheet</button> <a href="/admin/mahizhchi">Cancel</a></form></div>"""

MZ_DETAIL = """{% if detail.shared and detail.pub %}<div class="mz-cele" style="animation:none;padding:10px 16px">{{ mzbadge('Access enabled', true) }}<span class="txt">{{detail.name}} can open the Mahizhchi Log.</span></div>{% endif %}
<div class="card"><h2>{{detail.name}} &mdash; {{detail.won_n}} / {{detail.nsets}} Sets won{% if detail.status=='Completed' %} &#9989; Completed{% endif %}</h2>
<p class="mut">Status: <b>{{detail.status}}</b> &middot; a Set is won by answering all {{detail.per}} questions with at least {{detail.need}} correct
{% if not detail.shared %} &middot; <span class="pill out">Not shared with this employee</span>{% elif not detail.pub %} &middot; <span class="pill act">Shared - not published</span>{% endif %}
{% if back %} &middot; <a href="{{back}}">&larr; All results</a>{% endif %}</p></div>
{% for st in detail.sets %}<div class="card"><h2>Set {{st.n}} &mdash; <span class="pill {{'in' if st.status=='won' else ('out' if st.status=='failed' else 'act')}}">{{ {'won':'Won','failed':'Not won','active':'In progress','open':'Not started','locked':'Locked'}[st.status] }}</span></h2>
<p class="mut">Answered {{st.answered}} of {{st.total}} &middot; correct {{st.correct}}{% if st.started %} &middot; started {{st.started|t12}}{% endif %} &middot; questions shown to this employee in their own order{% if st.extra %} &middot; extra time given: <b>{{mz_dur(st.extra)}}</b>{% endif %}</p>
{% if st.can_add %}<form method="post" action="/admin/mahizhchi/extend" class="no-print" style="margin-top:8px" onsubmit="return confirm('Give {{detail.name}} more time on Set {{st.n}}? A closed Set is re-opened and the employee can answer the questions still unanswered.')">
<input type="hidden" name="emp" value="{{detail.eid}}"><input type="hidden" name="set" value="{{st.n}}">
<b>Add time:</b> <input type="number" name="min" min="0" max="60" value="1" style="width:70px"> min <input type="number" name="sec" min="0" max="59" value="0" style="width:70px"> sec
<button class="primary">Add time</button> <span class="mut">(the employee gets this much time from now, even if the Set already expired)</span></form>{% endif %}</div>
{% for d in st.lines %}<div class="mz-q"><h3><span class="no">{{loop.index}}.</span>{{d.q.q}}</h3>
{% for o in d.q.opts %}<div class="mz-o {{'ok' if o.letter==d.q.correct else ('mine' if o.letter==d.mine else '')}}"><span class="l">{{o.letter}}.</span>
<span>{{o.text}}{% if o.letter==d.q.correct %} <span class="tick">&#10003;</span>{% endif %}{% if o.letter==d.mine %} <span class="pill {{'in' if d.mine==d.q.correct else 'out'}}">employee&rsquo;s answer</span>{% endif %}</span></div>{% endfor %}
{% if not d.mine %}<p class="mz-issue">Not answered</p>{% endif %}</div>{% endfor %}{% else %}<div class="card"><p>No full Set of questions in Mahizhchi yet.</p></div>{% endfor %}
{% if detail.conn %}<div class="card"><h2>&#128279; Connection Game &mdash; <span class="pill {{'in' if detail.conn.status=='Won' else ('out' if detail.conn.status=='Lost' else 'act')}}">{{detail.conn.status}}</span></h2>
<p class="mut">Puzzle {{detail.conn.game}} &middot; groups found {{detail.conn.solved}} of 4 &middot; mistakes {{detail.conn.mistakes}} of {{detail.conn.max_m}} &middot; started {{detail.conn.started|t12}}{% if detail.conn.extra %} &middot; extra time given: <b>{{mz_dur(detail.conn.extra)}}</b>{% endif %}</p>
{% if detail.conn.can_add %}<form method="post" action="/admin/mahizhchi/connect/extend" class="no-print" onsubmit="return confirm('Give {{detail.name}} more time on the Connection Game?')">
<input type="hidden" name="emp" value="{{detail.eid}}"><b>Add time:</b> <input type="number" name="min" min="0" max="60" value="1" style="width:70px"> min <input type="number" name="sec" min="0" max="59" value="0" style="width:70px"> sec <button class="primary">Add time</button></form>{% endif %}</div>{% endif %}"""
MZ_EMPINFO = MZ_CSS + MZ_DETAIL
MZ_ADMIN_RESULTS = MZ_CSS + MZ_HEAD + "{% if detail %}" + MZ_DETAIL + """{% else %}<div class="card"><h2>&#127942; Winners</h2>{% if overall %}<div class="mz-win" style="font-weight:700">&#127942; Overall Winner: <b>{{overall.name}}</b> &mdash; first to complete all Sets ({{overall.at|t12}})</div>{% endif %}{% for b in board %}{% if b.name %}<div class="mz-win">&#127942; Set {{b.n}} Winner: <b>{{b.name}}</b></div>{% else %}<div class="mz-win none">Set {{b.n}} &mdash; no winner yet</div>{% endif %}{% endfor %}</div>
<div class="card"><h2>Results</h2><p class="mut">{{nsets}} Sets of {{per}} questions. A Set is won by answering all {{per}} with at least {{need}} correct; the next Set opens only after the previous one is won. Completed = all {{nsets}} Sets won; the first employee to complete them all is the overall winner.</p>
<table><tr><th>Employee ID</th><th>Name</th><th>Sets won</th>{% for i in range(1, nsets+1) %}<th>Set {{i}}</th>{% endfor %}<th>Status</th><th>Connection Game</th><th>Last submitted</th><th></th></tr>
{% for r in res %}<tr><td>{{r.id}}</td><td>{{r.name}}</td><td><b>{{r.won_n}} / {{nsets}}</b></td>
{% for i in range(1, nsets+1) %}{% set p = r.prog[i-1] if r.prog|length >= i else none %}<td>{% if not p or p.status in ('locked','open') %}&mdash;{% elif p.status=='won' %}<span class="pill in">&#10003; {{p.correct}}/{{p.total}}</span>{% elif p.status=='failed' %}<span class="pill out">{{p.correct}}/{{p.total}} - not won</span>{% else %}<span class="pill act">playing</span>{% endif %}</td>{% endfor %}
<td>{% if r.status=='Completed' %}<span class="pill in">&#9989; Completed</span>{% else %}{{r.status}}{% endif %}</td><td>{% if r.conn=='Won' %}<span class="pill in">&#127942; Won</span>{% elif r.conn=='Lost' %}<span class="pill out">Lost</span>{% else %}{{r.conn}}{% endif %}</td><td>{{r.last|t12}}</td>
<td>{% if r.answered or r.prog|selectattr('att')|list %}<a href="/admin/mahizhchi?tab=results&emp={{r.id|urlencode}}">Details</a>{% endif %}</td></tr>
{% else %}<tr><td colspan="{{nsets+7}}">No employee has access or answers yet.</td></tr>{% endfor %}</table></div>{% endif %}"""

MZ_EMP = MZ_CSS + """<style>.mz-sets{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}.mz-sets span{padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.95);font-weight:700;font-size:13px;border:1px solid #d6d9ff}
.mz-sets .won{background:#e3f6ec;border-color:#9bd7b5;color:#146c43}.mz-sets .failed{background:#fef2f2;border-color:#fca5a5;color:#991b1b}.mz-sets .active,.mz-sets .open{background:#eef0ff;border-color:#4f46e5;color:#3730a3}.mz-sets .locked{opacity:.6}
.mz-win{padding:8px 12px;border-radius:10px;background:#fff7e6;border:1px solid #f5d58a;margin:0 0 6px;font-size:15px}.mz-win.none{background:#f1f2f6;border-color:#e1e4ee;color:var(--mut)}
.cg-band{border-radius:10px;padding:10px 14px;margin:0 0 8px;text-align:center;font-weight:700}.cg-band small{display:block;font-weight:500}
.t0{background:#fde68a}.t1{background:#bbf7d0}.t2{background:#bfdbfe}.t3{background:#ddd6fe}
.cg-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0}.cg-t{display:block;cursor:pointer}.cg-t input{position:absolute;opacity:0;pointer-events:none}
.cg-t span{display:flex;align-items:center;justify-content:center;text-align:center;min-height:56px;padding:6px;border-radius:10px;background:#f1f2f6;border:2px solid transparent;font-weight:700;font-size:14px;word-break:break-word}
.cg-t input:checked+span{background:#4f46e5;color:#fff}.cg-t input:disabled+span{opacity:.5;cursor:default}
.cg-dot{display:inline-block;width:11px;height:11px;border-radius:50%;background:#cbd0e0;margin-left:4px}.cg-dot.on{background:#4f46e5}
@media(max-width:600px){.cg-grid{grid-template-columns:repeat(2,1fr)}}</style>
<div class="mz-stage{{' has-bg' if bg_v}}"{% if bg_v %} style="--mzbg:url('/employee/mahizhchi/bg?v={{bg_v}}')"{% endif %}>
<div class="head"><div><h1>{{ mzrun() }}</h1></div></div>
{% if not prog %}<div class="card"><p>There are not enough questions in {{MZ_TITLE}} yet.</p></div>
{% else %}{% if board %}<div class="card" id="mzboardcard"><h2>&#127942; Winners</h2><div id="mzboard">{% if overall %}<div class="mz-win" style="font-weight:700">&#127942; Overall Winner: <b>{{overall.name}}</b> &mdash; first to complete all Sets</div>{% endif %}{% for b in board %}{% if b.name %}<div class="mz-win">&#127942; Set {{b.n}} Winner: <b>{{b.name}}</b></div>{% else %}<div class="mz-win none">Set {{b.n}} &mdash; no winner yet</div>{% endif %}{% endfor %}</div></div>{% endif %}
<div class="mz-sets">{% for p in prog %}<span class="{{p.status}}">Set {{p.n}}: {% if p.status=='open' and p.att %}Try again{% else %}{{ {'won':'Won \u2713','failed':'Not won','active':'In progress','open':'Ready','locked':'Locked'}[p.status] }}{% endif %}</span>{% endfor %}</div>
{% if state=='intro' %}<div class="card"><h2>Set {{cur}} of {{prog|length}}</h2>
<p>This Set has <b>{{per}}</b> questions and you have <b>{{mz_dur(limit)}}</b>. The timer starts when you press <b>Start</b> and cannot be paused or restarted. Your questions appear in your own order.
{% if retry %}{% if pn_started %}<b>{{todo_n}}</b> question(s) still need a correct answer &mdash; they keep coming back (with a fresh timer each round) until you answer them correctly.{% else %}Answer all <b>{{per}}</b> correctly to win this Set. Any question you miss keeps coming back (with a fresh timer each round) until you answer it correctly.{% endif %} When time is over your ticked answers are submitted automatically.
{% else %}Answer <b>all {{per}}</b> questions and get at least <b>{{need}}</b> right to win the Set and unlock the next one. When time is over the Set closes automatically and your ticked answers are submitted. Each Set can be attempted only once.{% endif %}</p>
<form method="post" action="/employee/mahizhchi/start"><button class="primary">{{ ('Try again - Set ' ~ cur) if (retry and pn_started) else ('Start Set ' ~ cur) }}</button></form></div>
{% elif state=='active' %}<div class="mz-timer" id="mzbar">&#9201; Mahizhchi Log &middot; Set {{cur}} &middot; <b id="mzt">{{"%d:%02d"|format(limit//60, limit%60)}}</b></div>
<form method="post" action="/employee/mahizhchi/submit" id="mzform">
{% for q in qs %}<div class="mz-q"><h3><span class="no">{{loop.index}}.</span>{{q.q}}</h3>
{% for o in q.opts %}<label class="mz-o pick"><input type="radio" name="a_{{q.qid}}" value="{{o.letter}}"><span class="l">{{o.letter}}.</span><span>{{o.text}}</span></label>{% endfor %}</div>{% endfor %}
<button class="primary" id="mzsub">Submit Set {{cur}}</button></form>
<script>(function(){
var f=document.getElementById('mzform'),t=document.getElementById('mzt'),bar=document.getElementById('mzbar');
var end=Date.now()+{{remaining}}*1000,over=false,iv;
function fmt(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}
function lock(){
  f.querySelectorAll('input[type=radio]:checked').forEach(function(r){var h=document.createElement('input');h.type='hidden';h.name=r.name;h.value=r.value;f.appendChild(h)});
  f.querySelectorAll('input,button').forEach(function(x){x.disabled=true});f.classList.add('mz-locked')}
function tick(){var s=Math.max(0,Math.ceil((end-Date.now())/1000));t.textContent=fmt(s);if(s<=30)bar.classList.add('low');
  if(s<=0&&!over){over=true;clearInterval(iv);bar.textContent='\u23F1 Time is up \u2013 this Set is closed, submitting\u2026';lock();f.submit()}}
f.addEventListener('submit',function(e){if(over)return;
  var names={},n=0,c=f.querySelectorAll('input[type=radio]:checked').length;
  f.querySelectorAll('input[type=radio]').forEach(function(r){if(!names[r.name]){names[r.name]=1;n++}});
  if(n>c&&!confirm((n-c)+' question(s) are not answered. You need to answer all of them to win this Set. Submit anyway? You cannot answer them later.')){e.preventDefault();return}
  over=true;clearInterval(iv)});
tick();iv=setInterval(tick,250);})();</script>
{% elif state=='winner' %}<div class="mz-cele"><span class="mz-conf" aria-hidden="true">{% for em in ['🎉','✨','🎊','⭐','💫','🎈','🌟','🎉','✨','🎊'] %}<span style="left:{{ 4 + loop.index0*10 }}%;animation-delay:{{ loop.index0*0.25 }}s">{{em}}</span>{% endfor %}</span>
<span class="big">🏆</span><span class="txt">&#9989; Completed! You have won all {{prog|length}} Sets.{% if overall and overall.id|upper == me|upper %} You are the <b>overall winner</b> &mdash; the first to complete every Set!{% elif overall %} The overall winner is <b>{{overall.name}}</b>.{% endif %}</span></div>
{% if conn %}<div class="card"><h2>&#128279; Bonus round: Connection Game</h2>
{% for g in conn.solved %}<div class="cg-band {{g.tone}}">{{g.name}}<small>{{g.words|join(', ')}}</small></div>{% endfor %}
{% if conn.state=='intro' %}<p>Find the <b>4 hidden groups of 4 words</b>. Pick 4 words you think belong together and press <b>Submit group</b>. You have <b>{{mz_dur(conn.limit)}}</b> and can make at most <b>{{conn.max_m}}</b> mistakes. You can play only once.</p>
<form method="post" action="/employee/mahizhchi/connect/start"><button class="primary">Start Connection Game</button></form>
{% elif conn.state=='active' %}<div class="mz-timer" id="cgbar">&#9201; Connection Game &middot; <b id="cgt">{{mz_dur(conn.limit)}}</b> &middot; Mistakes left: {% for i in range(conn.max_m) %}<span class="cg-dot{{' on' if i < conn.max_m - conn.mistakes}}"></span>{% endfor %}</div>
<form method="post" action="/employee/mahizhchi/connect/guess" id="cgform"><div class="cg-grid">{% for w in conn.words %}<label class="cg-t"><input type="checkbox" name="w" value="{{w}}"><span>{{w}}</span></label>{% endfor %}</div>
<button class="primary" id="cgsub" disabled>Submit group (<span id="cgn">0</span>/4)</button></form>
<script>(function(){var f=document.getElementById('cgform');if(!f)return;var b=document.getElementById('cgsub'),n=document.getElementById('cgn');
var boxes=[].slice.call(f.querySelectorAll('input[type=checkbox]'));
function upd(){var c=boxes.filter(function(x){return x.checked}).length;b.disabled=c!==4;n.textContent=c;boxes.forEach(function(x){if(!x.checked)x.disabled=c>=4})}
boxes.forEach(function(x){x.addEventListener('change',upd)});upd();
var t=document.getElementById('cgt'),end=Date.now()+{{conn.remaining}}*1000,iv;
function tick(){var s=Math.max(0,Math.ceil((end-Date.now())/1000));t.textContent=Math.floor(s/60)+':'+('0'+(s%60)).slice(-2);
 if(s<=0){clearInterval(iv);boxes.forEach(function(x){x.disabled=true});b.disabled=true;location.reload()}}
tick();iv=setInterval(tick,250);})();</script>
{% elif conn.state=='won' %}<p><b>&#127881; Brilliant! You found all 4 groups.</b></p>
{% else %}{% for g in conn.reveal %}<div class="cg-band {{g.tone}}">{{g.name}}<small>{{g.words|join(', ')}}</small></div>{% endfor %}<p>The Connection Game is over (time up or no mistakes left). The groups you missed are shown above. Thank you for playing!</p>{% endif %}</div>{% endif %}
{% else %}<div class="card"><h2>Set {{failed.n}} &mdash; not won</h2><p>You answered {{failed.answered}} of {{failed.total}} questions and got {{failed.correct}} correct. To win a Set you must answer all {{failed.total}} within the time and get at least {{need}} right, so the next Set stays locked. Thank you for taking part!</p></div>{% endif %}
{% endif %}
{% if state!='active' and reveal %}{% for rv in reveal %}<details class="card"><summary><b>Set {{rv.n}} &mdash; correct answers</b></summary>{% for it in rv['items'] %}<div class="mz-row" style="font-size:14px;color:var(--ink)"><b>{{loop.index}}.</b> {{it.q}} &mdash; <span class="tick">&#10003; {{it.a}}</span></div>{% endfor %}</details>{% endfor %}{% endif %}
</div>"""

def mz_bg_path():
    """Background PNG for the employee Mahizhchi page: $MZ_BG_FILE, else mahizhchi_bg.png next to this file (or in ./static)."""
    here = os.path.dirname(os.path.abspath(__file__))
    for pth in (os.getenv("MZ_BG_FILE", ""), os.path.join(here, "mahizhchi_bg.png"), os.path.join(here, "static", "mahizhchi_bg.png")):
        if pth and os.path.isfile(pth): return pth
    return ""

# ---- Admin side (full control)
@app.route("/admin/mahizhchi")
@need("admin")
def admin_mahizhchi():
    prefetch(MZ_SHEET, MZ_ACCESS_SHEET, MZ_ANS_SHEET, MZ_ATT_SHEET, MZ_CSHEET, MZ_CATT_SHEET, "Employees", "Settings")
    tab = request.args.get("tab", "questions")
    if tab == "add":
        return page(MZ_ADMIN_ADD, title=MZ_TITLE, tab="add", sheet=MZ_SHEET, maxlen=MZ_MAX_PASTE)
    if tab == "connect": return redirect("/admin/mahizhchi")      # Update88: the Connection Game admin tab was removed
    amap = mz_access_map()
    emps = rows("Employees")
    if tab == "results":
        qs = [q for q in mz_questions() if q["ok"]]; per = mz_results(qs)
        eid = request.args.get("emp", "").strip()
        if eid:
            detail = mz_detail(emp_or_404(eid))
            return page(MZ_ADMIN_RESULTS, title=MZ_TITLE, tab="results", detail=detail, back="/admin/mahizhchi?tab=results")
        res = []
        for e in emps:
            k = _key(e["Employee ID"]); d = per.get(k)
            if not d and not amap.get(k): continue
            d = d or dict(answered=0, last="", prog=[], won_n=0, status="Not started", conn="—")
            res.append(dict(id=e["Employee ID"], name=e["Name"], answered=d["answered"], last=d["last"], prog=d["prog"],
                            won_n=d["won_n"], status=d["status"], conn=d["conn"]))
        res.sort(key=lambda r: (-r["won_n"], str(r["name"]).lower()))        # winners first
        return page(MZ_ADMIN_RESULTS, title=MZ_TITLE, tab="results", detail=None, res=res, nsets=MZ_SETS, per=MZ_PER_SET, need=MZ_WIN_CORRECT, board=mz_board(len(mz_split(qs))), overall=mz_overall_winner(len(mz_split(qs))))
    if tab == "access":
        q = request.args.get("q", "").strip()
        shown = [e for e in emps if not q or q.lower() in str(e["Employee ID"]).lower() or q.lower() in str(e["Name"]).lower()]
        fresh = session.pop("mz_new", None) or {}          # Update83: set by the Share action, shown once (celebration)
        ids = fresh.get("ids")
        return page(MZ_ADMIN_ACCESS, title=MZ_TITLE, tab="access", emps=shown, amap=amap, q=q, pub=mz_published(),
                    granted=fresh.get("n", 0), newall=bool(fresh) and ids is None, newset=set(ids or []))
    qs = mz_questions()
    for n, sq in enumerate(mz_split(qs), start=1):          # Update84: label each ready question with its Set
        for q in sq: q["set"] = n
    ids = {_key(e["Employee ID"]) for e in emps}
    return page(MZ_ADMIN_Q, title=MZ_TITLE, tab="questions", qs=qs, ok_n=sum(1 for x in qs if x["ok"]),
                pub=mz_published(), shared_n=sum(1 for k, v in amap.items() if v and k in ids), emp_n=len(ids),
                sheet=MZ_SHEET, sheet_id=SHEET_ID, limit=MZ_TIME_LIMIT,
                sets_n=len(mz_split(qs)), nsets=MZ_SETS, per=MZ_PER_SET, need=MZ_WIN_CORRECT)

@app.route("/admin/mahizhchi/publish", methods=["POST"])
@need("admin")
def admin_mahizhchi_publish():
    on = request.form.get("on") == "1"
    if on and not any(q["ok"] for q in (mz_parse(r) for r in _fetch_rows(MZ_SHEET)) if q):
        flash("Add at least one complete question (with one ✓ correct answer) before publishing.", "error")
        return redirect("/admin/mahizhchi")
    mz_set_published(on)
    flash(f"{MZ_TITLE} published. Employees it is shared with can now view it." if on
          else f"{MZ_TITLE} un-published. No employee can see it now.")
    return redirect("/admin/mahizhchi")

@app.route("/admin/mahizhchi/access", methods=["POST"])
@need("admin")
def admin_mahizhchi_access():
    action = request.form.get("action", "")
    emps = rows("Employees")
    if action in ("share_all", "revoke_all"): chosen = emps
    elif action in ("share_selected", "revoke_selected"):
        want = {_key(i) for i in request.form.getlist("ids")}
        chosen = [e for e in emps if _key(e["Employee ID"]) in want]           # only real employees, never raw form values
        if not chosen:
            flash("Tick at least one employee first.", "error"); return redirect("/admin/mahizhchi?tab=access")
    else: abort(400)
    share = action.startswith("share")
    mz_set_access(chosen, share)
    if share:
        session["mz_new"] = dict(n=len(chosen), ids=[_key(e["Employee ID"]) for e in chosen] if len(chosen) <= 25 else None)
    note = ""
    if share and not mz_published(fresh=True):
        if any(q["ok"] for q in mz_questions()):
            mz_set_published(True); note = " It has also been published, so they can see it now."
        else:
            note = " Add at least one complete question (with one ✓) - until then employees cannot see anything."
    flash(f"{MZ_TITLE} {'shared with' if share else 'removed from'} {len(chosen)} employee(s)." + note)
    return redirect("/admin/mahizhchi?tab=access")

@app.route("/admin/mahizhchi/extend", methods=["POST"])
@need("admin")
def admin_mahizhchi_extend():
    """Update84: Admin adds time to one employee's Set (also after the time limit has expired)."""
    emp = emp_or_404(request.form.get("emp", "").strip()); eid = str(emp["Employee ID"])
    back = "/admin/mahizhchi?tab=results&emp=" + eid
    try: n = int(request.form.get("set", "0")); add = int(request.form.get("min", "0") or 0) * 60 + int(request.form.get("sec", "0") or 0)
    except ValueError: abort(400)
    if not 1 <= add <= 3600:
        flash("Enter between 1 second and 60 minutes to add.", "error"); return redirect(back)
    att = mz_attempts(eid).get(n)
    if not att:
        flash(f"{emp['Name']} has not started Set {n}, so there is no time to add.", "error"); return redirect(back)
    sets_q = mz_split(mz_questions())
    if n > len(sets_q): abort(404)
    if mz_score(sets_q[n - 1], mz_my_answers(eid, fresh=True), n)[2]:
        flash(f"Set {n} is already won by {emp['Name']}.", "error"); return redirect(back)
    mz_extend(att, add)
    flash(f"{_mz_dur(add)} added for {emp['Name']} on Set {n}. They can continue from their Mahizhchi page now.")
    return redirect(back)

@app.route("/admin/mahizhchi/connect/import", methods=["POST"])
@need("admin")
def admin_mahizhchi_connect_import():
    ids = []
    for r in _fetch_rows(MZ_CSHEET):
        try: ids.append(int(str(r.get("Game", "")).strip()))
        except ValueError: pass
    good, bad = mz_conn_parse_paste(request.form.get("text", "")[:MZ_MAX_PASTE], max(ids, default=0) + 1)
    if good:
        _with_retry(ws_of(MZ_CSHEET).append_rows, good, value_input_option="RAW"); invalidate_cache(MZ_CSHEET)
        flash(f"{len(good) // 4} Connection puzzle(s) added.")
    elif not bad: flash("Nothing to add - no puzzles were found in the pasted text.", "error")
    for b in bad[:10]: flash("Skipped: " + b, "error")
    return redirect("/admin/mahizhchi?tab=results")

@app.route("/admin/mahizhchi/connect/extend", methods=["POST"])
@need("admin")
def admin_mahizhchi_connect_extend():
    emp = emp_or_404(request.form.get("emp", "").strip()); eid = str(emp["Employee ID"])
    back = "/admin/mahizhchi?tab=results&emp=" + eid
    try: add = int(request.form.get("min", "0") or 0) * 60 + int(request.form.get("sec", "0") or 0)
    except ValueError: abort(400)
    if not 1 <= add <= 3600:
        flash("Enter between 1 second and 60 minutes to add.", "error"); return redirect(back)
    att = mz_conn_attempt(eid)
    if not att: flash(f"{emp['Name']} has not started the Connection Game.", "error"); return redirect(back)
    if att["result"] == "Won" or att["mistakes"] >= MZ_CONN_MISTAKES:
        flash("This Connection Game is already won, or ended because all mistakes were used - time cannot help.", "error"); return redirect(back)
    mz_conn_extend(att, add)
    flash(f"{_mz_dur(add)} added for {emp['Name']} on the Connection Game.")
    return redirect(back)

@app.route("/admin/mahizhchi/import", methods=["POST"])
@need("admin")
def admin_mahizhchi_import():
    text = request.form.get("text", "")[:MZ_MAX_PASTE]
    good, bad = mz_parse_paste(text)
    if good:
        _with_retry(ws_of(MZ_SHEET).append_rows, good, value_input_option="RAW")
        invalidate_cache(MZ_SHEET)
        flash(f"{len(good)} question(s) added to the {MZ_SHEET} sheet.")
    elif not bad:
        flash("Nothing to add - no questions were found in the pasted text.", "error")
    for b in bad[:10]: flash("Skipped: " + b, "error")
    if len(bad) > 10: flash(f"…and {len(bad) - 10} more skipped.", "error")
    return redirect("/admin/mahizhchi" if good else "/admin/mahizhchi?tab=add")

# ---- Employee side. The correct answer is deliberately NOT passed to the template (only qid / text / options / their own pick).
# The time limit is enforced HERE on the server (start time is stored in the "Mahizhchi Attempts" sheet), not just by the page's clock.
@app.route("/employee/mahizhchi", methods=["GET"])
@need("employee")
def employee_mahizhchi():
    eid = session.get("emp_id", "")
    if not mz_active(eid, fresh=True): abort(404)     # not published / not shared: page does not exist for them
    sets_q = mz_split(mz_questions()); done = mz_my_answers(eid, fresh=True)
    prog = mz_progress(eid, sets_q, mz_attempts(eid), done, finalize=True)      # a Set whose time ran out is closed here too
    act = next((p for p in prog if p["status"] == "active"), None)
    opn = next((p for p in prog if p["status"] == "open"), None)
    failed = next((p for p in prog if p["status"] == "failed"), None)
    qs, cur, remaining = [], 0, 0
    if act:
        state, cur, remaining = "active", act["n"], act["left"]
        qs = [dict(qid=q["qid"], q=q["q"], opts=q["opts"]) for q in mz_order(eid, cur, sets_q[cur - 1])      # this employee's own order
              if cur not in MZ_RETRY_SETS or done.get(q["qid"]) != q["correct"]]                              # retry Set: only what is not yet correct
    elif opn: state, cur = "intro", opn["n"]                 # questions are not sent to the browser until the employee presses Start
    elif prog and not failed and len(prog) >= MZ_SETS: state = "winner"
    else: state = "closed"
    bg = mz_bg_path()
    cs = sets_q[cur - 1] if cur else []
    todo_n = sum(1 for q in cs if done.get(q["qid"]) != q["correct"])
    reveal = []                     # Update86: after a Set is WON only the CORRECT answers are shown - never the employee's wrong picks
    for p in prog:
        if p["status"] == "won":
            reveal.append(dict(n=p["n"], items=[dict(q=q["q"], a=q["correct"] + ". " + next(o["text"] for o in q["opts"] if o["letter"] == q["correct"]))
                                                for q in mz_order(eid, p["n"], sets_q[p["n"] - 1])]))
    conn = mz_conn_ctx(eid) if state == "winner" else None            # Update85: bonus round only after all Sets are won
    return page(MZ_EMP, title=MZ_TITLE, conn=conn, prog=prog, retry=cur in MZ_RETRY_SETS, todo_n=todo_n, reveal=reveal,
                board=mz_board(len(sets_q)) if mz_can_see_board(eid) else [], overall=mz_overall_winner(len(sets_q)) if mz_can_see_board(eid) else None, me=eid, pn_started=bool(prog and cur and prog[cur - 1]["att"]), qs=qs, state=state, cur=cur, remaining=remaining, limit=MZ_TIME_LIMIT,
                per=MZ_PER_SET, need=MZ_WIN_CORRECT, failed=failed, bg_v=int(os.path.getmtime(bg)) if bg else 0)

@app.route("/employee/mahizhchi/winners")
@need("employee")
def employee_mahizhchi_winners():
    """Polled by every logged-in employee page (see BASE): who completed each Set first. Names only - never answers."""
    if not mz_can_see_board(session.get("emp_id", "")): return jsonify(show=False, sets=0, winners=[])
    b = mz_board(len(mz_split(mz_questions())))
    ov = mz_overall_winner(len(b))
    resp = jsonify(show=True, sets=len(b), board=[dict(n=x["n"], name=x["name"]) for x in b],
                   overall=dict(name=ov["name"], text=ov["text"]) if ov else None,
                   winners=[dict(set=x["n"], name=x["name"], text=x["text"]) for x in b if x["name"]])
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/employee/mahizhchi/bg")
@need("employee")
def employee_mahizhchi_bg():
    if not mz_active(session.get("emp_id", "")): abort(404)      # same rule as the page itself
    bg = mz_bg_path()
    if not bg: abort(404)
    resp = send_file(bg, mimetype="image/png"); resp.headers["Cache-Control"] = "private, max-age=3600"
    return resp

@app.route("/employee/mahizhchi/start", methods=["GET", "POST"])
@need("employee")
def employee_mahizhchi_start():
    if request.method != "POST": return redirect("/employee/mahizhchi")      # Update88: a stray GET (reload / back / re-login) is never a 405
    eid = session.get("emp_id", "")
    if not mz_active(eid, fresh=True): abort(404)
    sets_q = mz_split(mz_questions())
    if not sets_q:
        flash("There are not enough questions yet.", "error"); return redirect("/employee/mahizhchi")
    prog = mz_progress(eid, sets_q, mz_attempts(eid), mz_my_answers(eid, fresh=True), finalize=True)
    opn = next((p for p in prog if p["status"] == "open"), None)
    if not opn or any(p["status"] == "active" for p in prog):      # only the next unlocked Set can start; Start again never restarts a clock
        return redirect("/employee/mahizhchi")
    stamp = now_local().strftime("%Y-%m-%d %H:%M:%S")
    if opn["att"] and opn["n"] in MZ_RETRY_SETS:      # Update86: next round of a retry Set - same row, fresh timer
        r = opn["att"]["row"]
        _with_retry(ws_of(MZ_ATT_SHEET).update, range_name=f"C{r}:I{r}", values=[[stamp, "", opn["n"], "", "", "", 0]], value_input_option="RAW")
    else:
        _with_retry(ws_of(MZ_ATT_SHEET).append_row, [str(eid), session.get("name", ""), stamp, "", opn["n"], "", "", ""], value_input_option="RAW")
    invalidate_cache(MZ_ATT_SHEET)
    return redirect("/employee/mahizhchi")

@app.route("/employee/mahizhchi/submit", methods=["GET", "POST"])
@need("employee")
def employee_mahizhchi_submit():
    if request.method != "POST": return redirect("/employee/mahizhchi")      # Update88: a stray GET (reload / back / re-login) is never a 405
    eid = session.get("emp_id", "")
    if not mz_active(eid, fresh=True): abort(404)
    sets_q = mz_split(mz_questions()); atts = mz_attempts(eid); done = mz_my_answers(eid, fresh=True)
    act = next((n for n, a in sorted(atts.items()) if not a["closed"] and n <= len(sets_q)), None)
    if act is None:
        flash("This Set is already closed.", "error"); return redirect("/employee/mahizhchi")
    att, sq = atts[act], sets_q[act - 1]
    if (now_local() - att["start"]).total_seconds() > MZ_TIME_LIMIT + att.get("extra", 0) + MZ_GRACE:      # too late: nothing is accepted
        a, c, won = mz_score(sq, done, act); mz_close_attempt(att, a, c, won)
        flash(f"Time is over ({_mz_dur(MZ_TIME_LIMIT)}). Set {act} is closed.", "error"); return redirect("/employee/mahizhchi")
    picks = []
    for q in (q for q in sq if (done.get(q["qid"]) != q["correct"] if act in MZ_RETRY_SETS else q["qid"] not in done)):   # retry Sets re-take what is not yet correct;                    # ONLY this Set's questions are accepted
        a = request.form.get("a_" + q["qid"], "").strip().upper()
        if a in [o["letter"] for o in q["opts"]]:                        # must be one of THIS question's real options; blanks stay unanswered
            picks.append((q, a))
    if picks:
        stamp = now_local().strftime("%Y-%m-%d %H:%M:%S")
        _with_retry(ws_of(MZ_ANS_SHEET).append_rows,
                    [[str(eid), session.get("name", ""), q["qid"], q["q"], a, stamp] for q, a in picks], value_input_option="RAW")
        invalidate_cache(MZ_ANS_SHEET)
        done = dict(done); done.update({q["qid"]: a for q, a in picks})
    a, c, won = mz_score(sq, done, act)
    mz_close_attempt(att, a, c, won)                                     # Set is over: nothing more can be answered
    if won and act < len(sets_q) and act < MZ_SETS: flash(f"Set {act} won! You answered all {len(sq)} questions with {c} correct. Set {act + 1} is now open.")
    elif won:
        ov = mz_overall_winner(len(sets_q))
        flash("You are the OVERALL WINNER - first to complete every Set!" if ov and _key(ov["id"]) == _key(eid) else "Completed! You have won every Set.")
    elif act in MZ_RETRY_SETS: flash(f"{c} of {len(sq)} correct so far. The questions you have not answered correctly will keep coming back - press Try again.", "error")
    else: flash(f"Set {act} not won: {a} of {len(sq)} answered, {c} correct (need all answered and at least {MZ_WIN_CORRECT} correct).", "error")
    return redirect("/employee/mahizhchi")

@app.route("/employee/mahizhchi/connect/start", methods=["GET", "POST"])
@need("employee")
def employee_mahizhchi_connect_start():
    if request.method != "POST": return redirect("/employee/mahizhchi")      # Update88: a stray GET (reload / back / re-login) is never a 405
    eid = session.get("emp_id", "")
    if not mz_active(eid, fresh=True) or not mz_all_won(eid): abort(404)      # bonus round: all Sets must be won first
    if mz_conn_attempt(eid): return redirect("/employee/mahizhchi")           # one play only; Start again never restarts the clock
    puz = mz_conn_pick(eid, mz_conn_puzzles())
    if not puz:
        flash("The Connection Game is not ready yet.", "error"); return redirect("/employee/mahizhchi")
    _with_retry(ws_of(MZ_CATT_SHEET).append_row, [str(eid), session.get("name", ""), puz["id"],
                now_local().strftime("%Y-%m-%d %H:%M:%S"), "", "", 0, "", ""], value_input_option="RAW")
    invalidate_cache(MZ_CATT_SHEET)
    return redirect("/employee/mahizhchi")

@app.route("/employee/mahizhchi/connect/guess", methods=["GET", "POST"])
@need("employee")
def employee_mahizhchi_connect_guess():
    if request.method != "POST": return redirect("/employee/mahizhchi")      # Update88: a stray GET (reload / back / re-login) is never a 405
    eid = session.get("emp_id", "")
    if not mz_active(eid, fresh=True) or not mz_all_won(eid): abort(404)
    att = mz_conn_attempt(eid); puz = mz_conn_puzzles().get(att["game"]) if att else None
    if not att or not puz or not puz["ok"] or att["result"]:
        flash("The Connection Game is not open.", "error"); return redirect("/employee/mahizhchi")
    if (now_local() - att["start"]).total_seconds() > MZ_CONN_TIME + att["extra"] + MZ_GRACE:      # too late: nothing is accepted
        mz_conn_save(att, att["solved"], att["mistakes"], "Lost")
        flash("Time is over. The Connection Game is closed.", "error"); return redirect("/employee/mahizhchi")
    kind, gi = mz_conn_judge(puz, att["solved"], request.form.getlist("w"))
    solved, mist, result = list(att["solved"]), att["mistakes"], ""
    if kind == "invalid":
        flash("Pick exactly 4 of the words shown.", "error"); return redirect("/employee/mahizhchi")
    if kind == "correct":
        solved.append(gi); flash(f"Correct! That group is “{puz['groups'][gi]['name']}”.")
        if len(solved) == 4: result = "Won"; flash("You found all 4 groups - you win the Connection Game!")
    else:
        mist += 1
        flash(("One away! " if kind == "one_away" else "Not a group. ") + f"Mistakes left: {max(0, MZ_CONN_MISTAKES - mist)}.", "error")
        if mist >= MZ_CONN_MISTAKES: result = "Lost"; flash("No mistakes left - the Connection Game is over.", "error")
    mz_conn_save(att, solved, mist, result)
    return redirect("/employee/mahizhchi")


# ---------------------------------------------------------------- Update90: REMINDER MAIL (Daily Productivity Entry not submitted)
# Update115: the AUTOMATIC reminder e-mails (daily 1:35 PM scheduler and the scheduled missed-entries e-mail) are REMOVED.
# Reminder e-mails are sent ONLY manually, and ONLY by an Admin (Admin > Email Controls / Missed Entries Log).
# Environment variables:  SMTP_HOST (required unless BREVO_API_KEY), SMTP_PORT (587; 465 = SSL), SMTP_USER, SMTP_PASS, MAIL_FROM (default SMTP_USER),
#                         BREVO_API_KEY (optional, HTTPS), APP_URL (optional link placed in the mail).
import smtplib, ssl
from email.message import EmailMessage
from email.utils import formataddr
SMTP_HOST, SMTP_PORT = os.getenv("SMTP_HOST", "").strip(), int(os.getenv("SMTP_PORT", "587"))
SMTP_USER, SMTP_PASS = os.getenv("SMTP_USER", "").strip(), os.getenv("SMTP_PASS", "")
MAIL_FROM = os.getenv("MAIL_FROM", "").strip() or SMTP_USER
APP_URL = os.getenv("APP_URL", "").strip().rstrip("/")
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "").strip()      # Update94: send e-mail over HTTPS (port 443) via Brevo - works on hosts that block SMTP ports (e.g. Render free)
MAIL_READY = bool(BREVO_API_KEY or SMTP_HOST)      # Update98: the transport; the sender address comes from Admin > Email Controls (or MAIL_FROM)
print("E-mail mode:", "Brevo HTTPS API" if BREVO_API_KEY else ("SMTP " + SMTP_HOST if SMTP_HOST else "NOT CONFIGURED"))
_WORKER_ID = uuid.uuid4().hex[:8]

def productivity_access(eid, access_rows):
    """Everyone may submit the Daily Productivity Entry unless the 'Productivity Access' sheet has a row for them with Enabled = No."""
    if is_view_only(eid): return False                  # Update105: View-Only designations get no productivity reminder / missed-entry e-mails
    for r in access_rows:
        if _key(r.get("Employee ID", "")) == _key(eid):
            return str(r.get("Enabled", "")).strip().lower() not in ("no", "n", "false", "0", "disabled")
    return True

def employee_office_email(e):
    return str(e.get("Office Email ID") or e.get("Email") or "").strip()      # Office Email ID mirrors the login Email

def _brevo_send(messages):
    """Send via Brevo's HTTPS API (no SMTP port needed). Returns {email: 'Sent' | 'Failed: reason'}."""
    import json, urllib.request, urllib.error
    res = {}
    for m in messages:
        to = m["To"]
        try:
            html = m.get_body(preferencelist=("html",)); plain = m.get_body(preferencelist=("plain",))
            from email.utils import parseaddr
            _sn, _se = parseaddr(str(m["From"]))
            payload = {"sender": {"name": _sn or "Productivity Tracker", "email": _se or MAIL_FROM}, "to": [{"email": to}], "subject": str(m["Subject"]),
                       "htmlContent": html.get_content() if html else "<p>" + (plain.get_content() if plain else "") + "</p>"}
            if plain: payload["textContent"] = plain.get_content()
            req = urllib.request.Request("https://api.brevo.com/v3/smtp/email", data=json.dumps(payload).encode("utf-8"), method="POST",
                                         headers={"api-key": BREVO_API_KEY, "content-type": "application/json", "accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r: r.read()
            res[to] = "Sent"
        except urllib.error.HTTPError as ex:
            try: body = ex.read().decode("utf-8", "ignore")
            except Exception: body = ""
            res[to] = (f"Failed (Brevo) {ex.code}: {body}")[:230]
        except Exception as ex:
            res[to] = ("Failed (Brevo): " + str(ex))[:230]
    return res

def _smtp_send(messages):
    """Send all messages. Uses Brevo (HTTPS) when BREVO_API_KEY is set, otherwise ONE SMTP connection (IPv4 forced). Returns {email: 'Sent' | 'Failed: reason'}."""
    if BREVO_API_KEY: return _brevo_send(messages)
    import socket
    res = {}
    ctx = ssl.create_default_context()
    try: ip = socket.getaddrinfo(SMTP_HOST, SMTP_PORT, socket.AF_INET, socket.SOCK_STREAM)[0][4][0]      # force IPv4 (many hosts have no IPv6 route -> Errno 101)
    except Exception: ip = SMTP_HOST
    try:
        if SMTP_PORT == 465: srv = smtplib.SMTP_SSL(context=ctx, timeout=30)
        else: srv = smtplib.SMTP(timeout=30)
        srv._host = SMTP_HOST                                  # keep the real host name for TLS certificate checking
        srv.connect(ip, SMTP_PORT)
    except Exception as ex:
        return {m["To"]: (f"Failed (SMTP, no BREVO_API_KEY set on server): {ex}. Render free blocks SMTP - add BREVO_API_KEY in Environment and redeploy.")[:230] for m in messages}
    try:
        if SMTP_PORT != 465:
            srv.ehlo(); srv.starttls(context=ctx); srv.ehlo()
        if SMTP_USER: srv.login(SMTP_USER, SMTP_PASS)
        for m in messages:
            try: srv.send_message(m); res[m["To"]] = "Sent"
            except Exception as ex: res[m["To"]] = ("Failed: " + str(ex))[:200]
    except Exception as ex:
        for m in messages: res.setdefault(m["To"], ("Failed: " + str(ex))[:200])
    finally:
        try: srv.quit()
        except Exception: pass
    return res

# ---------------------------------------------------------------- Update92: MISSED ENTRIES E-MAIL (manual + automatic)
MISSED_LOG = "Missed Email Log"

def _setting(key, fresh=False):
    r = next((r for r in (_fetch_rows("Settings") if fresh else rows("Settings")) if str(r.get("Key", "")).strip() == key), None)
    return str(r.get("Value", "")).strip() if r else ""

def _set_setting(key, val):
    ws = ws_of("Settings"); keys = ws.col_values(1)
    if key in keys: ws.update(range_name=f"B{keys.index(key) + 1}", values=[[val]], value_input_option="RAW")
    else: ws.append_row([key, val], value_input_option="RAW")
    invalidate_cache("Settings")

def missed_mail_history(fresh=False):
    """-> ({EMP: last sent-at}, {EMP: set of dates already e-mailed successfully})."""
    last, done = {}, {}
    for r in (_fetch_rows(MISSED_LOG) if fresh else rows(MISSED_LOG)):
        if str(r.get("Employee ID", "")) == "__RUN__" or str(r.get("Status", "")) != "Sent" or str(r.get("Mode", "")) not in ("Manual", "Auto"): continue
        k = _key(r.get("Employee ID", ""))
        last[k] = max(last.get(k, ""), str(r.get("Sent at", "")))
        done.setdefault(k, set()).update(x.strip() for x in str(r.get("Missed dates", "")).split(",") if x.strip())
    return last, done

def missed_dates_for(eid, start, end):
    subs = [s_ for s_ in load_subs() if _key(s_["emp_id"]) == _key(eid)]
    leaves = [l for l in rows("Leave") if _key(l["Employee ID"]) == _key(eid)]
    return missing_dates(eid, subs, leaves, start, end, fmt="%Y-%m-%d")

# ---- Update98: sender settings + login link helpers
MAIL_SENDER_EMAIL_KEY, MAIL_SENDER_NAME_KEY = "Mail Sender Email", "Mail Sender Name"
EMAIL_RE = re.compile(r"^[^@\s,;<>\"]+@[^@\s,;<>\"]+\.[^@\s,;<>\"]+$")

def mail_sender(fresh=False):
    """-> (display name, e-mail). Admin's setting (Settings sheet) wins; falls back to the MAIL_FROM environment variable."""
    try:
        src = _fetch_rows("Settings") if fresh else rows("Settings")
        get = lambda k: next((str(r.get("Value", "")).strip() for r in src if str(r.get("Key", "")).strip() == k), "")
        em, nm = get(MAIL_SENDER_EMAIL_KEY), get(MAIL_SENDER_NAME_KEY)
    except Exception as ex:
        print("Could not read sender settings:", ex); em, nm = "", ""
    if not EMAIL_RE.match(em or ""): em = MAIL_FROM
    return ((nm or "Productivity Tracker (LN_Map)").replace("\r", " ").replace("\n", " ")[:60], em)

def app_url():
    u = APP_URL or os.getenv("RENDER_EXTERNAL_URL", "").strip().rstrip("/")      # Render sets RENDER_EXTERNAL_URL automatically
    if not u and has_request_context(): u = request.host_url.rstrip("/")
    return u

def employee_login_link():
    u = app_url()
    return (u + "/employee/login") if u else ""

def _html3d(nm, preheader, lead_html, middle_html, link, cta_text):
    """Update100: the ONE 3D-style e-mail design (table layout + inline CSS = works in Gmail/Outlook). Missed-entry AND approval mails use it."""
    import html as _h
    F = "font-family:'Segoe UI',Arial,Helvetica,sans-serif;"
    if link:
        lk = _h.escape(link)
        button = ('<table role="presentation" align="center" cellpadding="0" cellspacing="0" style="margin:6px auto 4px auto"><tr>'
                  '<td align="center" bgcolor="#d4af37" style="background:linear-gradient(180deg,#e8c95a,#c9a227);border-radius:14px;border-bottom:6px solid #8a6d1a;box-shadow:0 12px 22px rgba(201,162,39,.50)">'
                  f'<a href="{lk}" target="_blank" style="display:inline-block;padding:16px 40px;{F}font-size:17px;font-weight:bold;color:#1a1a1a;text-decoration:none;border-radius:14px">Login to Productivity Tracker &rarr;</a>'
                  '</td></tr></table>'
                  f'<p style="{F}margin:12px 0 0 0;font-size:12px;color:#64748b;text-align:center;word-break:break-all">Or copy this link: <a href="{lk}" style="color:#8a6d1a">{lk}</a></p>')
    else:
        button = f'<p style="{F}text-align:center;color:#b91c1c;font-size:14px">Please open the Productivity Tracker and log in.</p>'
    if not cta_text and not link:      # Update101: approval mails carry no login text / button / link
        cta_row = ""
    else:
        cta_row = f'<tr><td style="padding:8px 34px 8px 34px;{F}color:#1e293b"><p style="margin:0 0 18px 0;font-size:16px;line-height:1.55">{_h.escape(cta_text)}</p>{button}</td></tr>'
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>'
        '<body style="margin:0;padding:0;background:#efe9d8">'
        f'<div style="display:none;max-height:0;overflow:hidden;opacity:0">{_h.escape(preheader)}</div>'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#efe9d8" style="background:linear-gradient(160deg,#efe9d8,#faf7f0)"><tr><td align="center" style="padding:32px 12px">'
        '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#ffffff;border-radius:20px;border-bottom:7px solid #e6c76a;box-shadow:0 26px 50px rgba(15,23,42,.28)">'
        '<tr><td bgcolor="#2b2b2b" style="background:linear-gradient(135deg,#111111,#2b2b2b 60%,#424242);border-radius:20px 20px 0 0;padding:26px 30px"><table role="presentation" cellpadding="0" cellspacing="0"><tr>'
        f'<td style="padding-right:16px"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td align="center" width="58" height="58" bgcolor="#d4af37" style="width:58px;height:58px;background:linear-gradient(145deg,#f3dc8c,#d4af37);border-radius:16px;border-bottom:5px solid #8a6d1a;box-shadow:0 8px 14px rgba(0,0,0,.35);{F}font-size:22px;font-weight:bold;color:#1a1a1a">PT</td></tr></table></td>'
        f'<td style="{F}color:#ffffff"><div style="font-size:22px;font-weight:bold;letter-spacing:.3px">Productivity Tracker</div><div style="font-size:13px;color:#e6c76a;letter-spacing:2px;margin-top:3px">LN_MAP</div></td></tr></table></td></tr>'
        f'<tr><td style="padding:32px 34px 10px 34px;{F}color:#1e293b">'
        f'<p style="margin:0 0 14px 0;font-size:18px;font-weight:bold">Hello {nm},</p>'
        f'<p style="margin:0 0 18px 0;font-size:16px;line-height:1.55">{lead_html}</p></td></tr>'
        f'<tr><td align="center" style="padding:6px 24px 0 24px">{middle_html}</td></tr>'
        + cta_row +
        f'<tr><td style="padding:22px 34px 8px 34px;{F}color:#475569;font-size:13px;line-height:1.5"><p style="margin:0;border-top:1px solid #e2e8f0;padding-top:16px">This is an automated email. Please do not reply to this email.</p></td></tr>'
        f'<tr><td style="padding:6px 34px 30px 34px;{F}color:#1e293b;font-size:15px;line-height:1.5"><p style="margin:0">Thanks,<br><b>Productivity Tracker (LN_Map)</b></p></td></tr>'
        '</table></td></tr></table></body></html>')

def _orange_row(cells, F="font-family:'Segoe UI',Arial,Helvetica,sans-serif;"):
    """Update116: the e-mail data shown as ONE line (single table row) on an orange highlight. cells = [(label, value_html)]."""
    tds = "".join(
        f'<td align="center" valign="middle" style="padding:13px 8px;{F}{"border-left:1px solid #fb923c;" if i else ""}">'
        f'<div style="font-size:11px;letter-spacing:.8px;text-transform:uppercase;color:#7c2d12">{k}</div>'
        f'<div style="font-size:14px;font-weight:bold;color:#431407;margin-top:3px">{v}</div></td>' for i, (k, v) in enumerate(cells))
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#fdba74" '
            'style="max-width:532px;background:linear-gradient(180deg,#fed7aa,#fdba74);border-radius:14px;border-bottom:5px solid #ea580c;'
            f'box-shadow:0 10px 18px rgba(234,88,12,.35)"><tr>{tds}</tr></table>')

def _missed_html(nm, ds, pretty, link):
    import html as _h
    F = "font-family:'Segoe UI',Arial,Helvetica,sans-serif;"
    line = "  &bull;  ".join(_h.escape(d.strftime("%d %b %Y (%a)")) for d in ds[:4])
    tiles = _orange_row([("Missing Productivity Entry", line)], F)
    more = (f'<p style="{F}margin:0 0 6px 0;font-size:13px;color:#64748b;text-align:center">+ {len(ds) - 4} more date(s)</p>' if len(ds) > 4 else "")
    dl = _h.escape(", ".join(pretty))
    return _html3d(nm, f"Your Productivity Entry is missing for {', '.join(pretty)}.",
                   f'Your Productivity Entry is missing for <b style="color:#b91c1c">{dl}</b>.',
                   f'{tiles}{more.replace("margin:0 0 6px 0","margin:8px 0 6px 0")}', link,
                   "Please log in to the Productivity Tracker and complete the required entry:")

def approval_message(emp, kind, date_txt, duration_txt):
    """Update100: 'Leave' / 'Permission' APPROVED e-mail - same 3D template. Fields: employee name, request type, date, duration / hours, approval status."""
    import html as _h
    F = "font-family:'Segoe UI',Arial,Helvetica,sans-serif;"
    name = str(emp["name"])
    badge = ('<span style="display:inline-block;padding:4px 10px;border-radius:99px;background:#16a34a;border-bottom:3px solid #166534;'
             f'color:#ffffff;{F}font-size:13px;font-weight:bold;letter-spacing:.5px">&#10003; Approved</span>')
    fields = [("Employee Name", _h.escape(name)), ("Request Type", _h.escape(kind)), ("Date", _h.escape(date_txt)),
              ("Duration / Hours", _h.escape(duration_txt)), ("Status", badge)]
    card = _orange_row(fields, F)
    msg = EmailMessage()
    msg["Subject"] = f"{kind} request approved - {date_txt}"
    msg["From"] = formataddr(mail_sender()); msg["To"] = emp["email"]
    msg.set_content(f"Hello {name},\n\nYour {kind} request has been approved.\n\n"
                    f"Employee Name: {name}\nRequest Type: {kind}\nDate: {date_txt}\nDuration / Hours: {duration_txt}\nApproval Status: Approved\n\n"
                    "This is an automated email. Please do not reply to this email.\n\nThanks,\nProductivity Tracker (LN_Map)")
    msg.add_alternative(_html3d(_h.escape(name), f"Your {kind} request has been approved ({date_txt}).",
                                f'Your <b>{_h.escape(kind)}</b> request has been <b style="color:#15803d">approved</b>.', card, "", ""), subtype="html")
    return msg

def missed_message(emp, dates):
    """Update99: the single missed-entry e-mail (3D template) - used by Manual AND Automatic sending."""
    import html as _h
    ds = [dt.date.fromisoformat(d) for d in dates]
    pretty = [d.strftime("%d %b %Y") for d in ds]
    n = len(pretty); link = employee_login_link(); name = str(emp["name"])
    msg = EmailMessage()
    msg["Subject"] = "Productivity Entry missing for " + pretty[0] + (f" (+{n - 1} more)" if n > 1 else "")
    msg["From"] = formataddr(mail_sender()); msg["To"] = emp["email"]
    msg.set_content(f"Hello {name},\n\nYour Productivity Entry is missing for {', '.join(pretty)}.\n\n"
                    "Please log in to the Productivity Tracker and complete the required entry:\n"
                    f"{link or '(open the Productivity Tracker and log in)'}\n\n"
                    "This is an automated email. Please do not reply to this email.\n\nThanks,\nProductivity Tracker (LN_Map)")
    msg.add_alternative(_missed_html(_h.escape(name), ds, pretty, link), subtype="html")
    return msg

def send_logged(items, mode, by):
    """items = [(emp dict(eid,name,email), EmailMessage, dates_text, count)]. Each is logged as Pending, sent through Brevo (or SMTP), then updated to
    Sent / Failed-<reason> in the Missed Email Log (= the Email Controls status board). Returns {eid: status}."""
    ws = ws_of(MISSED_LOG)
    now = now_local().strftime("%Y-%m-%d %H:%M:%S"); today = now[:10]
    sender = mail_sender(fresh=True)[1]
    if not sender or not MAIL_READY:
        why = "Failed: no sender e-mail configured (Admin > Email Controls)" if not sender else "Failed: mail service not configured on the server (BREVO_API_KEY)"
        out = {e["eid"]: why for e, *_r in items}
        ws.append_rows([[today, e["eid"], e["name"], e["email"], dtxt, cnt, now, mode, why, by] for e, _m, dtxt, cnt in items], value_input_option="RAW")
        invalidate_cache(MISSED_LOG); return out
    resp = ws.append_rows([[today, e["eid"], e["name"], e["email"], dtxt, cnt, now, mode, "Pending", by] for e, _m, dtxt, cnt in items], value_input_option="RAW")
    invalidate_cache(MISSED_LOG)
    m_ = re.search(r"!A(\d+):", str((resp or {}).get("updates", {}).get("updatedRange", "")))
    try: first = int(m_.group(1)) if m_ else len(ws.col_values(1)) - len(items) + 1
    except Exception: first = None
    try: res = _smtp_send([m for _e, m, _d, _c in items])
    except Exception as ex:
        print("Mail send error:", ex); res = {e["email"]: ("Failed: " + str(ex))[:200] for e, *_r in items}
    out = {e["eid"]: res.get(e["email"], "Failed") for e, *_r in items}
    done = now_local().strftime("%Y-%m-%d %H:%M:%S")
    if first:
        try: ws.update(range_name=f"G{first}:I{first + len(items) - 1}", values=[[done, mode, out[e["eid"]]] for e, *_r in items], value_input_option="RAW")
        except Exception as ex: print("Could not update mail status:", ex)
    invalidate_cache(MISSED_LOG)
    return out

def _admin_only_mail():
    """Update115: reminder e-mails may be triggered ONLY from a signed-in Admin session (UI, API or a hand-made request)."""
    if session.get("role") != "admin": abort(403)

def send_missed_mails(items, mode, by):
    """items = [(emp, [dates])] -> one 3D missed-entry e-mail each (manual, Admin only). Returns {eid: status}."""
    _admin_only_mail()
    return send_logged([(e, missed_message(e, d), ", ".join(d), len(d)) for e, d in items], mode, by)

def _pretty_date(d):
    try: return dt.date.fromisoformat(str(d)).strftime("%d %b %Y (%a)")
    except ValueError: return str(d)

def notify_approved(emp_row, kind, date_txt, duration_txt, count):
    """Send the 'approved' e-mail for a Leave / Permission request. Never raises. Returns a flash-ready (text, category)."""
    mail = employee_office_email(emp_row); name = str(emp_row.get("Name", ""))
    if not EMAIL_RE.match(mail): return (f"No approval e-mail sent: {name} has no valid Office Email ID.", "error")
    e = dict(eid=str(emp_row["Employee ID"]), name=name, email=mail)
    try: st = send_logged([(e, approval_message(e, kind, date_txt, duration_txt), date_txt, count)], f"{kind} approval", session.get("name", "Admin"))[e["eid"]]
    except Exception as ex_: st = "Failed: " + str(ex_)[:150]; print("Approval mail error:", ex_)
    if st == "Sent": return (f"Approval e-mail sent to {name} ({mail}).", "ok")
    return (f"The request was approved, but the approval e-mail to {name} could not be sent: {st}", "error")

@app.route("/admin/missed/send", methods=["POST"])
@need("admin")
def admin_missed_send():
    _admin_only_mail()
    nxt = (request.form.get("next") or "").strip()
    back = nxt if (nxt.startswith("/admin/") and "//" not in nxt and "\\" not in nxt and "\n" not in nxt) else "/admin/missed-log"
    if not MAIL_READY:
        flash("E-mail is not set up on the server (BREVO_API_KEY or SMTP_HOST, and MAIL_FROM).", "error"); return redirect(back)
    eid = (request.form.get("eid") or "").strip()
    e = next((x for x in rows("Employees") if _key(x["Employee ID"]) == _key(eid)), None)
    if not e: flash("Employee not found.", "error"); return redirect(back)
    mail = employee_office_email(e)
    if "@" not in mail: flash(f"{e['Name']} has no valid Office Email ID.", "error"); return redirect(back)
    today = today_local(); month = request.form.get("month") or today.strftime("%Y-%m")
    end = today - dt.timedelta(days=1)
    if month == "all":
        ds = [s_["date"] for s_ in load_subs() if _key(s_["emp_id"]) == _key(eid)] + [l["Date"] for l in rows("Leave") if _key(l["Employee ID"]) == _key(eid)]
        start = dt.date.fromisoformat(min(ds)) if ds else today
    else:
        start = month_range(month)[0]; end = min(month_range(month)[1], end)
    dates = missed_dates_for(eid, start, end)
    if not dates: flash(f"{e['Name']} has no missed entries for this period - nothing to send.", "error"); return redirect(back)
    emp = dict(eid=str(e["Employee ID"]), name=str(e["Name"]), email=mail)
    try: st = send_missed_mails([(emp, dates)], "Manual", session.get("name", "admin"))[emp["eid"]]
    except Exception as ex_: st = "Failed: " + str(ex_)[:150]; print("Missed mail error:", ex_)
    if st == "Sent": flash(f"Missed Entries e-mail sent to {e['Name']} ({mail}) - {len(dates)} date(s).")
    else: flash(f"E-mail to {e['Name']} could not be sent: {st}", "error")
    return redirect(back)

# ---------------------------------------------------------------- Update93: MISSED ENTRIES LOG (separate Admin page)
MLOG = '''<div class="head"><div><h1>Missed Entries Log</h1>
<p class="mut">{{label}} &middot; Every employee with working days (weekly off / holidays excluded) that have no productivity entry and no leave. Today is not included.</p></div>
<form class="grid no-print" method="get"><input type="month" name="month" value="{{month if month!='all' else ''}}">
<input name="emp" placeholder="Employee ID / name" value="{{emp}}">
<button class="primary">Show</button><a href="/admin/missed-log">Reset</a><a href="/admin/missed-log?month=all">All time</a></form></div>
<div class="kpis"><div class="kpi"><span>Missed entries</span><b>{{total}}</b></div>
<div class="kpi"><span>Employees affected</span><b>{{summary|length}}</b></div></div>
<div class="card no-print"><h2>Missed entries e-mail</h2>
<p class="mut">Sends the employee's missed productivity entry dates to their registered Office Email ID. Dates shown follow the filter above ({{label}}).</p>
{% if not smtp_ok %}<div class="warn">E-mail is not set up on the server yet (BREVO_API_KEY or SMTP_HOST, and MAIL_FROM) - nothing can be sent until it is.</div>{% endif %}
<p class="mut">Reminder e-mails are sent by the Admin, or automatically when the Admin has switched on Automatic Email (Admin &rarr; Email Controls).</p>
<table><tr><th>Employee</th><th>E-mail</th><th>Missed dates</th><th>Not yet e-mailed</th><th>Last e-mailed</th><th></th></tr>
{% for x in summary %}<tr><td><a href="/admin/missed-log/{{x.id|urlencode}}?month={{month}}">{{x.id}} &middot; {{x.name}}</a></td><td>{{x.email or '-'}}</td><td>{{x.dates|length}}: {{x.dates|join(', ')}}</td><td>{{x.new}}</td><td>{{(x.last|t12) if x.last else 'Never'}}</td>
<td class="act"><a href="/admin/missed-log/{{x.id|urlencode}}?month={{month}}">View</a>
<form method="post" action="/admin/missed/send" onsubmit="return confirm('Send the Missed Entries e-mail to {{x.name}}?')"><input type="hidden" name="eid" value="{{x.id}}"><input type="hidden" name="month" value="{{month}}"><input type="hidden" name="next" value="/admin/missed-log?month={{month}}">
<button class="primary"{{' disabled title="No valid Office Email ID"' if not x.email else ''}}>Send e-mail</button></form></td></tr>
{% else %}<tr><td colspan="6">No employee has missed entries for this period.</td></tr>{% endfor %}</table></div>
<div class="card"><h2>E-mails sent</h2>
<table><tr><th>Sent at</th><th>Employee</th><th>E-mail</th><th>Dates</th><th>Mode</th><th>Status</th></tr>
{% for h in history %}<tr><td>{{h['Sent at']|t12}}</td><td>{{h['Employee ID']}} &middot; {{h['Employee name']}}</td><td>{{h['Email']}}</td><td>{{h['Missed dates']}}</td><td>{{h['Mode']}}</td><td>{{h['Status']}}</td></tr>
{% else %}<tr><td colspan="6">No e-mail has been sent yet.</td></tr>{% endfor %}</table></div>'''

MLOG_EMP = '''<div class="head"><div><h1>{{emp['Name']}} &middot; Missed entries</h1>
<p class="mut">{{emp['Employee ID']}} &middot; {{email or 'No Office Email ID'}} &middot; {{label}}</p></div>
<form class="grid no-print" method="get"><input type="month" name="month" value="{{month if month!='all' else ''}}">
<button class="primary">Show</button><a href="?">This month</a><a href="?month=all">All time</a></form></div>
<p class="no-print"><a href="/admin/missed-log?month={{month}}">&larr; Missed Entries Log</a></p>
<div class="kpis"><div class="kpi"><span>Missed entries</span><b>{{dates|length}}</b></div>
<div class="kpi"><span>Not yet e-mailed</span><b>{{new_count}}</b></div></div>
<div class="card no-print"><form method="post" action="/admin/missed/send" onsubmit="return confirm('Send the Missed Entries e-mail to this employee?')"><input type="hidden" name="eid" value="{{emp['Employee ID']}}"><input type="hidden" name="month" value="{{month}}"><input type="hidden" name="next" value="/admin/missed-log/{{emp['Employee ID']|urlencode}}?month={{month}}">
<button class="primary"{{' disabled' if not (email and dates) else ''}}>&#9993; Send Missed Entries e-mail</button>
{% if not smtp_ok %}<span class="mut"> E-mail is not set up on the server yet.</span>{% elif not email %}<span class="mut"> No valid Office Email ID.</span>{% elif not dates %}<span class="mut"> Nothing to send.</span>{% endif %}</form></div>
<table><tr><th>Date</th><th>Day</th><th>E-mailed</th></tr>
{% for d in dates %}<tr><td>{{d.date}}</td><td>{{d.day}}</td><td>{{'Yes' if d.sent else 'No'}}</td></tr>
{% else %}<tr><td colspan="3">No missed entries.</td></tr>{% endfor %}</table>
<div class="card"><h2>E-mail history</h2><table><tr><th>Sent at</th><th>Dates</th><th>Mode</th><th>Status</th></tr>
{% for h in history %}<tr><td>{{h['Sent at']|t12}}</td><td>{{h['Missed dates']}}</td><td>{{h['Mode']}}</td><td>{{h['Status']}}</td></tr>
{% else %}<tr><td colspan="4">No e-mail has been sent to this employee yet.</td></tr>{% endfor %}</table></div>'''

def missed_scope(month, subs, leaves):
    today = today_local(); end = today - dt.timedelta(days=1)
    if month == "all":
        ds = [x["date"] for x in subs] + [l["Date"] for l in leaves]
        return (dt.date.fromisoformat(min(ds)) if ds else today), end, "All time"
    st, en = month_range(month)
    return st, min(en, end), st.strftime("%B %Y")

def mail_history(eid=None, limit=40):
    out = [r for r in rows(MISSED_LOG) if str(r.get("Employee ID", "")) != "__RUN__" and str(r.get("Mode", "")) in ("Manual", "Auto") and (eid is None or _key(r.get("Employee ID", "")) == _key(eid))]
    return sorted(out, key=lambda r: str(r.get("Sent at", "")), reverse=True)[:limit]

@app.route("/admin/missed-log")
@need("admin")
def admin_missed_log():
    prefetch("Employees", "Productivity log", "Leave", "Holidays", "Settings", MISSED_LOG)
    month = request.args.get("month") or today_local().strftime("%Y-%m")
    q = request.args.get("emp", "").strip().lower()
    subs, leaves, emps = load_subs(), rows("Leave"), rows("Employees")
    start, end, label = missed_scope(month, subs, leaves)
    last, notified = missed_mail_history()
    summary, total = [], 0
    for e in emps:
        if q and q not in str(e["Employee ID"]).lower() and q not in str(e["Name"]).lower(): continue
        k = _key(e["Employee ID"])
        dates = missing_dates(e["Employee ID"], [x for x in subs if _key(x["emp_id"]) == k], [l for l in leaves if _key(l["Employee ID"]) == k], start, end, fmt="%Y-%m-%d")
        if not dates: continue
        total += len(dates)
        summary.append(dict(id=e["Employee ID"], name=e["Name"], email=employee_office_email(e), dates=sorted(dates), last=last.get(k, ""),
                            new=len([d for d in dates if d not in notified.get(k, set())])))
    summary.sort(key=lambda x: str(x["name"]))
    return page(MLOG, title="Missed Entries Log", month=month, label=label, emp=request.args.get("emp", ""), summary=summary, total=total,
                smtp_ok=MAIL_READY, history=mail_history())

@app.route("/admin/missed-log/<eid>")
@need("admin")
def admin_missed_log_emp(eid):
    prefetch("Employees", "Productivity log", "Leave", "Holidays", MISSED_LOG)
    e = next((x for x in rows("Employees") if _key(x["Employee ID"]) == _key(eid)), None)
    if not e: abort(404)
    month = request.args.get("month") or today_local().strftime("%Y-%m")
    k = _key(eid)
    subs = [x for x in load_subs() if _key(x["emp_id"]) == k]; leaves = [l for l in rows("Leave") if _key(l["Employee ID"]) == k]
    start, end, label = missed_scope(month, subs, leaves)
    _l, notified = missed_mail_history(); sent = notified.get(k, set())
    ds = sorted(missing_dates(eid, subs, leaves, start, end, fmt="%Y-%m-%d"), reverse=True)
    dates = [dict(date=d, day=dt.date.fromisoformat(d).strftime("%a"), sent=d in sent) for d in ds]
    return page(MLOG_EMP, title="Missed entries - " + str(e["Name"]), emp=e, email=employee_office_email(e), month=month, label=label, dates=dates,
                new_count=sum(1 for d in dates if not d["sent"]), smtp_ok=MAIL_READY, history=mail_history(eid))

# ---------------------------------------------------------------- Update98: ADMIN EMAIL CONTROLS
def mail_month_start(): return today_local().replace(day=1)      # Update100: manual sending covers the CURRENT month only (today is never "missed")

def mail_status(v):
    v = str(v or "").strip()
    return "Sent" if v == "Sent" else ("Pending" if v == "Pending" else "Failed")

# ---------------------------------------------------------------- Update122: AUTOMATIC missed-entry e-mail (Admin-only switch)
AUTO_MAIL_KEY = "Auto Missed Email"
AUTO_MAIL_TIME_KEY = "Auto Missed Email Time"                       # Update123: Admin-selected send time (Settings sheet, HH:MM)
AUTO_MAIL_TIME = os.getenv("AUTO_MAIL_TIME", "09:30").strip()      # HH:MM, app timezone - default until the Admin saves a time

def auto_mail_on(fresh=False):
    return _setting(AUTO_MAIL_KEY, fresh).lower() in ("yes", "on", "true", "1", "enabled")

def _parse_hhmm(s):
    m = re.fullmatch(r"\s*([01]?\d|2[0-3]):([0-5]\d)\s*", str(s or ""))
    return dt.time(int(m.group(1)), int(m.group(2))) if m else None

def _auto_time():
    """Admin-selected time (Settings sheet) -> AUTO_MAIL_TIME env default -> 09:30."""
    try: saved = _setting(AUTO_MAIL_TIME_KEY)
    except Exception: saved = ""
    return _parse_hhmm(saved) or _parse_hhmm(AUTO_MAIL_TIME) or dt.time(9, 30)

def _auto_claim_run(today):
    """One automatic run per day across all workers: the first '__RUN__' row of the day wins."""
    ws = ws_of(MISSED_LOG); t = str(today)
    def mine():
        runs = [r for r in _fetch_rows(MISSED_LOG) if str(r.get("Employee ID", "")) == "__RUN__" and str(r.get("Mode", "")) == "Auto" and str(r.get("Date sent", "")) == t]
        return runs
    if mine(): return False
    ws.append_row([t, "__RUN__", _WORKER_ID, "", "", 0, now_local().strftime("%Y-%m-%d %H:%M:%S"), "Auto", "Run", "System"], value_input_option="RAW")
    invalidate_cache(MISSED_LOG)
    runs = mine()
    return bool(runs) and str(runs[0].get("Employee name", "")) == _WORKER_ID

def run_auto_missed_mail():
    """Background job (no request / session). E-mails each employee their NEW missed dates of this month. Never raises. Returns the number of e-mails tried."""
    try:
        if not (MAIL_READY and auto_mail_on(fresh=True)): return 0
        today = today_local()
        if not _auto_claim_run(today): return 0
        end = today - dt.timedelta(days=1); start = mail_month_start()
        try: access = _fetch_rows("Productivity Access")
        except Exception: access = []
        subs, leaves = load_subs(), _fetch_rows("Leave")
        _l, notified = missed_mail_history(fresh=True)
        items = []
        for e in _fetch_rows("Employees"):
            eid = str(e.get("Employee ID", "")); k = _key(eid)
            mail = employee_office_email(e)
            if not eid or not EMAIL_RE.match(mail) or not productivity_access(eid, access): continue
            ds = missing_dates(eid, [x for x in subs if _key(x["emp_id"]) == k], [l for l in leaves if _key(l["Employee ID"]) == k], start, end, fmt="%Y-%m-%d")
            new = sorted(d for d in ds if d not in notified.get(k, set()))
            if not new: continue
            emp = dict(eid=eid, name=str(e.get("Name", "")), email=mail)
            items.append((emp, missed_message(emp, new), ", ".join(new), len(new)))
        for i in range(0, len(items), 25):
            send_logged(items[i:i + 25], "Auto", "System")      # logged in the Missed Email Log; failed ones are retried next day
        print(f"Automatic missed-entry e-mail: {len(items)} employee(s).")
        return len(items)
    except Exception as ex:
        print("Automatic missed-entry e-mail error:", ex); return 0

_auto_done_day = [None]
def _auto_mail_loop():
    time.sleep(60)
    while True:
        try:
            now = now_local()
            if _auto_done_day[0] != now.date() and now.time() >= _auto_time() and auto_mail_on():
                run_auto_missed_mail(); _auto_done_day[0] = now.date()
        except Exception as ex:
            print("auto mail loop error:", ex)
        time.sleep(60)

threading.Thread(target=_auto_mail_loop, daemon=True).start()

@app.route("/admin/email-controls/auto", methods=["POST"])
@need("admin")
def admin_email_controls_auto():
    _admin_only_mail()                                   # Admin session only - employees get 403
    on = request.form.get("auto") == "on"
    t = _parse_hhmm(request.form.get("auto_time", ""))
    if t is None:
        flash("Please choose a valid send time (HH:MM).", "error"); return redirect("/admin/email-controls")
    _set_setting(AUTO_MAIL_TIME_KEY, t.strftime("%H:%M"))
    _set_setting(AUTO_MAIL_KEY, "Yes" if on else "No")
    flash(f"Automatic Email ENABLED - employees with missed entries will be e-mailed every day at {t.strftime('%I:%M %p')}." if on else f"Automatic Email DISABLED (send time saved: {t.strftime('%I:%M %p')}).")
    return redirect("/admin/email-controls")

EMAIL_CONTROLS = """<div class="head"><div><h1>Email Controls</h1>
<p class="mut">Reminders for missed Productivity entries - manual or automatic (Admin only). Mails go to each employee's Office Email ID using one 3D-style template (missed date(s) + Login button). They are sent by this application running on Render. Only Admin can open this page.</p></div></div>
{% if not mail_ok %}<div class="warn"><b>&#9888; E-mail service is not set up on the server.</b> Add <code>BREVO_API_KEY</code> (recommended on Render - it sends over HTTPS) or <code>SMTP_HOST</code> in the Render Environment settings and redeploy. Nothing can be sent until then.</div>{% endif %}
{% if not login_link %}<div class="warn">No Employee Login link is available: set <code>APP_URL</code> (e.g. https://your-app.onrender.com) in the Render Environment settings.</div>{% endif %}
<div class="kpis"><div class="kpi"><span>Sent</span><b>{{counts.Sent}}</b></div><div class="kpi"><span>Failed</span><b>{{counts.Failed}}</b></div><div class="kpi"><span>Pending</span><b>{{counts.Pending}}</b></div></div>

<div class="card"><h2>Automatic Email</h2>
<form method="post" action="/admin/email-controls/auto" class="grid" style="align-items:end">
<label style="display:inline-flex;gap:8px;align-items:center"><input type="checkbox" name="auto" value="on" {{'checked' if auto_on else ''}}> Send missed-entry e-mails automatically</label>
<label>Send time<input type="time" name="auto_time" value="{{auto_time_val}}" required></label>
<button class="primary sm">Save</button></form>
<p class="mut">Status: <b style="color:{{'#15803d' if auto_on else '#991b1b'}}">{{'ENABLED' if auto_on else 'DISABLED'}}</b>. When enabled, every day at <b>{{auto_time}}</b> (the time set here by the Admin) each employee who has missed a Productivity Entry this month receives an e-mail with their name, the missed date(s) and the Productivity Tracker login link. A date is never e-mailed twice. Last automatic run: <b>{{auto_last or 'never'}}</b>. Only Admin can change this.</p></div>

<div class="card"><h2>1. Send a reminder manually</h2>
<form method="post" action="/admin/email-controls/send" id="ec-form" onsubmit="return ecCheck()">
<label>Employee<select name="eid" id="ec-emp"><option value="">- choose an employee -</option>
{% for e in emps %}<option value="{{e.id}}"{{' disabled' if not e.email else ''}}>{{e.id}} &middot; {{e.name}} &middot; {{e.email or 'no Office Email ID'}} ({{e.n}} missed)</option>{% endfor %}</select></label>
<p class="mut" style="margin:10px 0 4px">Missed date(s) to include (current month - {{month_label}}):</p>
<div id="ec-dates" style="max-height:220px;overflow:auto;border:1px solid #d0d5dd;border-radius:8px;padding:8px 12px">Choose an employee first.</div>
<p style="margin:10px 0"><label style="display:inline-flex;gap:6px;align-items:center"><input type="checkbox" id="ec-all"> Select all dates</label></p>
<button class="primary" id="ec-send" disabled>&#9993; Send reminder e-mail</button></form></div>

<div class="card"><h2>2. Sender e-mail / account</h2>
<form method="post" action="/admin/email-controls/sender" class="grid" style="align-items:end">
<label>Sender name<input name="sender_name" value="{{sender_name}}" maxlength="60" placeholder="Productivity Tracker"></label>
<label>Sender e-mail<input type="email" name="sender_email" value="{{sender_email}}" placeholder="noreply@yourcompany.com"></label>
<button class="primary sm">Save sender</button></form>
<p class="mut">Mail service in use: <b>{{transport}}</b>. The address you save here is used as the From address. With Brevo it must be a verified sender in your Brevo account, otherwise mails will show as Failed. The Brevo API key / SMTP password are kept in the Render Environment settings (never in the sheet) - change them there. Leave the e-mail empty to fall back to <code>MAIL_FROM</code>{% if env_from %} (now: {{env_from}}){% endif %}.</p>
<p class="mut">Current sender: <b>{{cur_sender}}</b></p></div>

<div class="card"><h2>3. E-mail status</h2>
<form method="get" class="grid no-print" style="align-items:end">
<label>Status<select name="status"><option value="">All</option>{% for x in ['Sent','Failed','Pending'] %}<option{{' selected' if status==x else ''}}>{{x}}</option>{% endfor %}</select></label>
<input name="q" placeholder="Employee ID / name" value="{{q}}"><button class="primary sm">Show</button><a href="/admin/email-controls">Reset</a></form>
<table><tr><th>Time</th><th>Employee</th><th>Office e-mail</th><th>Missed date(s)</th><th>Mode</th><th>Status</th><th>Sent by</th></tr>
{% for h in history %}<tr><td>{{h.at|t12}}</td><td>{{h.emp}}</td><td>{{h.email}}</td><td>{{h.dates}}</td><td>{{h.mode}}</td>
<td><span style="padding:2px 9px;border-radius:99px;font-weight:600;{{ {'Sent':'background:#dcfce7;color:#166534','Failed':'background:#fee2e2;color:#991b1b','Pending':'background:#fef3c7;color:#92400e'}[h.status] }}">{{h.status}}</span>
{% if h.status=='Failed' and h.detail %}<br><small class="mut">{{h.detail}}</small>{% endif %}</td><td>{{h.by}}</td></tr>
{% else %}<tr><td colspan="7">No e-mails recorded{{' for this filter' if status or q else ' yet'}}.</td></tr>{% endfor %}</table>
<p class="mut">Latest {{history|length}} of {{total}} shown. Pending = being sent right now (a row that stays Pending means the server stopped before it finished).</p></div>
<script>
(function(){
 var M={{ missed_map|tojson }};
 var sel=document.getElementById('ec-emp'),box=document.getElementById('ec-dates'),btn=document.getElementById('ec-send'),all=document.getElementById('ec-all');
 function boxes(){return box.querySelectorAll('input[type=checkbox]');}
 function upd(){var n=0;boxes().forEach(function(c){if(c.checked)n++;});btn.disabled=!n;}
 function render(){
  var list=M[sel.value]||[];box.innerHTML='';all.checked=false;
  if(!sel.value){box.textContent='Choose an employee first.';}
  else if(!list.length){box.textContent='No missed dates in {{month_label}}.';}
  list.forEach(function(x){
   var l=document.createElement('label');l.style.cssText='display:flex;gap:8px;align-items:center;margin:3px 0';
   var c=document.createElement('input');c.type='checkbox';c.name='dates';c.value=x.d;c.addEventListener('change',upd);
   var t=document.createElement('span');t.textContent=x.label+(x.sent?'  (already e-mailed)':'');
   l.appendChild(c);l.appendChild(t);box.appendChild(l);});
  upd();}
 sel.addEventListener('change',render);
 all.addEventListener('change',function(){boxes().forEach(function(c){c.checked=all.checked;});upd();});
 window.ecCheck=function(){var n=0;boxes().forEach(function(c){if(c.checked)n++;});
  if(!n){alert('Select at least one missed date.');return false;}
  return confirm('Send the reminder for '+n+' date(s) to the selected employee?');};
 render();
})();
</script>"""

@app.route("/admin/email-controls")
@need("admin")
def admin_email_controls():
    prefetch("Employees", "Productivity log", "Leave", "Holidays", "Settings", MISSED_LOG)
    today = today_local(); end = today - dt.timedelta(days=1); start = mail_month_start()
    subs, leaves = load_subs(), rows("Leave")
    _last, notified = missed_mail_history()
    emps, missed_map = [], {}
    for e in rows("Employees"):
        k = _key(e["Employee ID"]); eid = str(e["Employee ID"])
        ds = sorted(missing_dates(eid, [x for x in subs if _key(x["emp_id"]) == k], [l for l in leaves if _key(l["Employee ID"]) == k], start, end, fmt="%Y-%m-%d"), reverse=True)
        missed_map[eid] = [dict(d=d, label=dt.date.fromisoformat(d).strftime("%d %b %Y (%a)"), sent=d in notified.get(k, set())) for d in ds]
        emps.append(dict(id=eid, name=str(e.get("Name", "")), email=(employee_office_email(e) if "@" in employee_office_email(e) else ""), n=len(ds)))
    emps.sort(key=lambda x: x["name"].lower())
    allrows = [r for r in rows(MISSED_LOG) if str(r.get("Employee ID", "")) != "__RUN__"]
    allrows.sort(key=lambda r: str(r.get("Sent at", "")), reverse=True)
    counts = {"Sent": 0, "Failed": 0, "Pending": 0}
    for r in allrows: counts[mail_status(r.get("Status"))] += 1
    status = request.args.get("status", "").strip(); q = request.args.get("q", "").strip().lower()
    hist = []
    for r in allrows:
        st = mail_status(r.get("Status"))
        if status in counts and st != status: continue
        if q and q not in str(r.get("Employee ID", "")).lower() and q not in str(r.get("Employee name", "")).lower(): continue
        hist.append(dict(at=str(r.get("Sent at", "")), emp=f"{r.get('Employee ID', '')} · {r.get('Employee name', '')}", email=str(r.get("Email", "")),
                         dates=str(r.get("Missed dates", "")), mode=str(r.get("Mode", "")), status=st,
                         detail=str(r.get("Status", ""))[:200] if st == "Failed" else "", by=str(r.get("Sent by", ""))))
    nm, em = mail_sender()
    cur = f"{nm} <{em}>" if em else "not set"
    transport = "Brevo HTTPS API" if BREVO_API_KEY else (f"SMTP ({SMTP_HOST})" if SMTP_HOST else "NOT CONFIGURED")
    return page(EMAIL_CONTROLS, title="Email Controls", mail_ok=MAIL_READY, login_link=employee_login_link(), counts=counts, emps=emps, missed_map=missed_map, month_label=today.strftime("%B %Y"), sender_name=_setting(MAIL_SENDER_NAME_KEY),
                sender_email=_setting(MAIL_SENDER_EMAIL_KEY), env_from=MAIL_FROM, cur_sender=cur, transport=transport,
                history=hist[:100], total=len(hist), status=status, q=request.args.get("q", ""),
                auto_on=auto_mail_on(fresh=True), auto_time=_auto_time().strftime("%I:%M %p"), auto_time_val=_auto_time().strftime("%H:%M"),
                auto_last=max([str(r.get("Date sent", "")) for r in rows(MISSED_LOG) if str(r.get("Employee ID", "")) == "__RUN__" and str(r.get("Mode", "")) == "Auto"] or [""]))

@app.route("/admin/email-controls/sender", methods=["POST"])
@need("admin")
def admin_email_controls_sender():
    nm = re.sub(r"[\r\n]+", " ", (request.form.get("sender_name") or "")).strip()[:60]
    em = (request.form.get("sender_email") or "").strip()
    if em and not EMAIL_RE.match(em): flash("Enter a valid sender e-mail address.", "error"); return redirect("/admin/email-controls")
    _set_setting(MAIL_SENDER_NAME_KEY, nm); _set_setting(MAIL_SENDER_EMAIL_KEY, em)
    flash(f"Sender saved: {mail_sender(fresh=True)[1] or 'none - set an address or MAIL_FROM'}.")
    return redirect("/admin/email-controls")

@app.route("/admin/email-controls/send", methods=["POST"])
@need("admin")
def admin_email_controls_send():
    _admin_only_mail()
    back = "/admin/email-controls"
    if not MAIL_READY:
        flash("E-mail is not set up on the server (BREVO_API_KEY or SMTP_HOST).", "error"); return redirect(back)
    eid = (request.form.get("eid") or "").strip()
    e = next((x for x in rows("Employees") if _key(x["Employee ID"]) == _key(eid)), None)
    if not e: flash("Choose an employee.", "error"); return redirect(back)
    mail = employee_office_email(e)
    if not EMAIL_RE.match(mail): flash(f"{e['Name']} has no valid Office Email ID.", "error"); return redirect(back)
    asked = {d for d in request.form.getlist("dates") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)}
    today = today_local()
    missed = set(missed_dates_for(eid, mail_month_start(), today - dt.timedelta(days=1)))
    chosen = sorted(asked & missed)
    if not chosen: flash("Select at least one missed date (only this month's missed dates can be sent).", "error"); return redirect(back)
    emp = dict(eid=str(e["Employee ID"]), name=str(e["Name"]), email=mail)
    try: st = send_missed_mails([(emp, chosen)], "Manual", session.get("name", "admin"))[emp["eid"]]
    except Exception as ex_: st = "Failed: " + str(ex_)[:150]; print("Manual missed mail error:", ex_)
    if st == "Sent": flash(f"Reminder sent to {e['Name']} ({mail}) for {len(chosen)} date(s).")
    else: flash(f"E-mail to {e['Name']} could not be sent: {st}", "error")
    return redirect(back)


# ---------------------------------------------------------------- Update99: "Missed Entries" section below the Productivity log
LOG_MISSED = """<div class="card" id="missed-entries" style="margin-top:22px"><h2>Missed Entries</h2>
<p class="mut">Working days (weekly off / holidays excluded) with no productivity entry and no leave &middot; today is not included. Same data as Employee Info &rarr; Missed Entries, for all employees. The Employee filter above also applies here.</p>
<form class="grid no-print" method="get" action="/admin/log#missed-entries">
<input type="hidden" name="date" value="{{request.args.get('date','')}}"><input type="hidden" name="emp" value="{{request.args.get('emp','')}}">
<label>Month<input type="month" name="mmonth" value="{{mmonth if mmonth!='all' else ''}}"></label><button class="primary">Show</button>
<a href="/admin/log?date={{request.args.get('date','')|urlencode}}&emp={{request.args.get('emp','')|urlencode}}#missed-entries">This month</a>
<a href="/admin/log?date={{request.args.get('date','')|urlencode}}&emp={{request.args.get('emp','')|urlencode}}&mmonth=all#missed-entries">All time</a></form>
<div class="kpis"><div class="kpi"><span>Missed entries &middot; {{mlabel}}</span><b>{{mdata|length}}</b></div><div class="kpi"><span>Employees affected</span><b>{{m_emps}}</b></div></div>
<p class="no-print"><a class="btnl" href="/admin/email-controls">&#9993; Email Controls (send reminders / schedule)</a></p>
<table><tr><th>Date</th><th>Day</th><th>Employee</th><th>Designation</th><th>E-mailed</th></tr>
{% for r in mdata %}<tr><td>{{r.date}}</td><td>{{r.day}}</td><td><a href="/admin/employee-info/{{r.id|urlencode}}?tab=missed&month={{mmonth}}">{{r.id}} &middot; {{r.name}}</a></td><td>{{r.designation}}</td><td>{{'Yes' if r.sent else 'No'}}</td></tr>
{% else %}<tr><td colspan="5">No missed entries.</td></tr>{% endfor %}</table></div>"""

def log_missed_section():
    prefetch("Employees", "Productivity log", "Leave", "Holidays", MISSED_LOG)
    today = today_local()
    month = (request.args.get("mmonth") or "").strip()
    if month != "all" and not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month): month = today.strftime("%Y-%m")
    q = request.args.get("emp", "").strip().lower()
    subs, leaves = load_subs(), rows("Leave")
    start, end, label = missed_scope(month, subs, leaves)
    _l, notified = missed_mail_history()
    data = []
    for e in rows("Employees"):
        if q and q not in str(e["Employee ID"]).lower() and q not in str(e["Name"]).lower(): continue
        k = _key(e["Employee ID"])
        for d in missing_dates(e["Employee ID"], [x for x in subs if _key(x["emp_id"]) == k], [l for l in leaves if _key(l["Employee ID"]) == k], start, end, fmt="%Y-%m-%d"):
            data.append(dict(date=d, day=dt.date.fromisoformat(d).strftime("%a"), id=e["Employee ID"], name=e["Name"],
                             designation=e.get("Designation", ""), sent=d in notified.get(k, set())))
    data.sort(key=lambda r: (r["date"], str(r["name"])), reverse=True)
    return dict(mdata=data, m_emps=len({r["id"] for r in data}), mmonth=month, mlabel=label)


if __name__ == "__main__":
    # NOTE: Flask's built-in dev server (even with threaded=True) is still not
    # meant for real concurrent traffic, and debug=True is a security risk in
    # production (exposes a remote code-execution console on error pages).
    # For local testing with a few users this is fine; for the real deployment
    # run with a production WSGI server instead, e.g.:
    #   pip install gunicorn
    #   gunicorn -w 4 --threads 4 -b 0.0.0.0:5000 app:app
    # (4 worker processes x 4 threads comfortably covers 20 concurrent users;
    # gspread calls are I/O-bound so threads work well here.)
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug, threaded=True)
