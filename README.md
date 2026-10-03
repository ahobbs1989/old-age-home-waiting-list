# Old Age Home — Waiting List System

This is a simple website for managing a retirement home's waiting
list: people can apply to join, check their place in line, and renew
their application. Staff have an admin area to search records and run
reports.

This guide assumes **no technical background**. It walks through three
things, in order:

1. [Download the code](#1-download-the-code) onto your computer
2. [Run it on your own computer](#2-run-it-on-your-own-computer), just to see it working
3. [Put it on the internet](#3-put-it-on-the-internet) so other people can use it from anywhere

Each part takes about 10–15 minutes. Do them in order — part 3 depends
on part 1.

> If anything on screen doesn't match what's described here exactly,
> it's usually because a website has changed its layout slightly.
> Look for a button or link with a similar name nearby.

---

## 1. Download the code

1. Open this page in your browser: **https://github.com/ahobbs1989/old-age-home-waiting-list**
2. Click the green **`<> Code`** button near the top of the page.
3. Click **Download ZIP**.
4. Find the downloaded file (usually in your **Downloads** folder) — it
   will be named something like `old_age_home-main.zip`.
5. Right-click it and choose **Extract All...** (Windows) or just
   double-click it (Mac) to unzip it.
6. You now have a folder containing the code — move it somewhere easy
   to find, like your Desktop, and remember where it is. The rest of
   this guide calls this **the project folder**.

---

## 2. Run it on your own computer

### Step 2.1 — Install Python

The code is written in a language called Python, so your computer
needs Python installed to run it.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
   and click the big **Download Python** button.
2. Open the downloaded installer.
3. **Windows only:** on the very first screen of the installer, tick
   the checkbox at the bottom that says **"Add python.exe to PATH"**
   (or "Add Python to PATH"). This step is easy to miss and causes
   problems later if skipped.
4. Click **Install Now** and let it finish.
5. Mac users: the installer runs itself with default options — just
   keep clicking **Continue** / **Install**.

### Step 2.2 — Open a terminal in the project folder

A "terminal" is a plain window where you type commands instead of
clicking buttons.

**On Windows:**
1. Open the project folder in File Explorer.
2. Click once in the empty address bar at the top of the window
   (where the folder path is shown).
3. Type `cmd` and press **Enter**. A black window (Command Prompt)
   opens, already pointed at your project folder.

**On Mac:**
1. Open the project folder in Finder.
2. Right-click (or two-finger click) inside the folder on empty space.
3. Choose **New Terminal at Folder**. (If you don't see this option,
   open the **Terminal** app from Launchpad, type `cd ` with a space
   after it, then drag the project folder into the window and press
   **Enter**.)

### Step 2.3 — Install the app's requirements

Copy and paste these commands into the terminal window, one line at a
time, pressing **Enter** after each one.

**Windows (Command Prompt):**
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac (Terminal):**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This downloads everything the app needs. It can take a minute or two,
and will print a lot of text — that's normal.

### Step 2.4 — Run the app

In the same terminal window, type:

**Windows:**
```
python main.py
```

**Mac:**
```
python3 main.py
```

You should see a message like `NiceGUI ready to go on http://localhost:8080`.

Open your web browser and go to: **http://localhost:8080**

The website is now running — but only on your own computer, and only
while that terminal window stays open. Closing the terminal stops it.
This is normal and expected at this stage; part 3 makes it available
permanently, to everyone, from anywhere.

To stop it, click into the terminal window and press **Ctrl+C**.

---

## 3. Put it on the internet

To let other people use the site from their own computers or phones,
it needs to run on a server rather than your own computer. We'll use a
free service called **Railway** that runs the app for you, around the
clock.

### Step 3.1 — Put your code on GitHub

Railway deploys code from GitHub, so if you haven't already, you need
a copy of this code in your own GitHub account:

1. Go to **[github.com](https://github.com)** and sign in (or create a
   free account if you don't have one).
2. Go back to **https://github.com/ahobbs1989/old-age-home-waiting-list**
   and click the **Fork** button near the top-right. This creates your
   own copy of the project under your GitHub account.

### Step 3.2 — Create a Railway account

1. Go to **[railway.app](https://railway.app)**.
2. Click **Login** (or **Start a New Project**) and choose
   **Continue with GitHub**. This connects Railway to your GitHub
   account so it can read your forked repository.

### Step 3.3 — Deploy the app

1. In Railway, click **New Project**.
2. Choose **Deploy from GitHub repo**.
3. Pick your fork of this project from the list (authorize Railway to
   access it if asked).
4. Railway will start building the app automatically — you'll see a
   progress screen with logs. This takes a few minutes the first time.
5. Click on the deployed service (the box that appears), then open the
   **Settings** tab.
6. Scroll to **Deploy** and find **Custom Start Command**. Set it to:
   ```
   python main.py
   ```
7. Still in Settings, find **Networking**, and click **Generate
   Domain**. Railway will give you a public web address like
   `your-app-name.up.railway.app` — this is the link you'll share with
   people.

### Step 3.4 — Keep the waiting-list data safe between restarts

By default, anything the app saves can be lost when Railway restarts
it. To keep applicant data safe permanently:

1. In your Railway project, click **+ New** and choose **Volume**.
2. Set the **Mount Path** to `/data`.
3. Attach this volume to your app's service.
4. Go to your service's **Variables** tab and add a new variable:
   - Name: `DB_PATH`
   - Value: `/data/app.db`
5. Redeploy the service (Railway usually does this automatically after
   a settings change — if not, there's a **Redeploy** button on the
   deployments screen).

### Step 3.5 — Set a real admin password

Anyone who finds your site's link can try to log into the admin area,
so change the password from its default before sharing the link
widely:

1. In Railway, go to your service's **Variables** tab.
2. Add a variable:
   - Name: `ADMIN_PASSWORD`
   - Value: *(choose a password only staff should know)*
3. Add a second variable, which keeps people logged in securely:
   - Name: `STORAGE_SECRET`
   - Value: *(any long random text, e.g. mash the keyboard for 30 characters)*
4. Redeploy if it doesn't happen automatically.

### Step 3.6 — Share it

Visit the address from Step 3.3 in your own browser first, to make
sure everything works. Then share that link with whoever needs to use
the site — applicants can go straight to `/join` or `/status` on that
address, and staff can use `/admin` with the password you set.

---

## Troubleshooting

**"python is not recognized" (Windows)**
Python wasn't added to PATH during install. Re-run the Python
installer, choose **Modify**, and make sure "Add python.exe to PATH"
is ticked. Then close and reopen the terminal.

**"command not found: python" (Mac)**
Use `python3` instead of `python` — Macs often only have `python3`
installed.

**The terminal says "address already in use"**
Something is already running on that port. Close any other terminal
windows that might still be running `main.py`, then try again.

**I forgot the admin password**
Whoever has access to the Railway project can see and change it any
time under the service's **Variables** tab (see Step 3.5).

**Changes I make on Railway don't seem to appear**
Make sure you redeployed after changing a variable or setting — look
for a **Redeploy** button on the Railway deployments screen.

---

## For developers

If you're going to make changes to the code rather than just run it,
see [CLAUDE.md](CLAUDE.md) for the project's architecture, conventions,
and POC scope notes.
