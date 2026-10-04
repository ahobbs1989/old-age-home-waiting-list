# Old Age Home — Waiting List System

This is a simple website for managing a retirement home's waiting list.
People can apply to join the list, check their place in line, and renew
their application. Staff get a password-protected admin area to search
records, mark payments, and run reports.

**You do not need any technical knowledge to use this.** You won't write
code or type commands yourself. Instead, you'll install two free-to-download
programs and then *ask an AI assistant called Claude, in plain English*, to
do everything for you: set the website up, change how it works, and put it
on the internet.

---

## What you'll do

| Part | What it is | Time |
|---|---|---|
| [Part 1](#part-1--get-a-claude-subscription) | Get a Claude subscription | 5 min |
| [Part 2](#part-2--install-vs-code) | Install VS Code (the program you'll work in) | 5 min |
| [Part 3](#part-3--download-this-project) | Download this project | 5 min |
| [Part 4](#part-4--open-the-project-in-vs-code) | Open the project in VS Code | 2 min |
| [Part 5](#part-5--install-claude-code-inside-vs-code) | Install Claude Code inside VS Code | 5 min |
| [Part 6](#part-6--talk-to-claude) | Talk to Claude: it does the rest | as long as you like |

Do the parts **in order**. Don't skip ahead.

> **If something on your screen looks slightly different from this guide**,
> don't worry. Websites and programs change their layout from time to time.
> Look for a button with a similar name nearby. And once you reach Part 6,
> you can simply ask Claude: *"My screen doesn't look like the guide. What
> do I do?"*

---

## Part 1 — Get a Claude subscription

Claude Code (the AI assistant you'll use) needs a **paid** Claude account.
The free plan does **not** include it.

1. Go to **[claude.ai](https://claude.ai)** in your web browser.
2. Click **Sign up** and create an account. You can use your email address
   or a Google account.
3. Once you're signed in, open the plans page (click your name or initials
   in the corner, then **Upgrade** or **Settings → Billing**).
4. Choose **Pro** (the cheapest paid plan, which is plenty for this) or
   **Max**, and enter your payment details.
5. Remember the email address you used. You'll need it in Part 5.

> If your organisation already gives you a Claude **Team** or **Enterprise**
> account, use that instead. You don't need to buy anything.

---

## Part 2 — Install VS Code

**VS Code** (short for "Visual Studio Code") is a free program from
Microsoft. Think of it as the "office" where you and Claude will work on
the website together.

1. Go to **[code.visualstudio.com](https://code.visualstudio.com)**.
2. Click the big blue **Download** button. The website automatically
   picks the right version for your computer.
3. Open the file you just downloaded (it's usually in your **Downloads**
   folder).

**On Windows:**

4. Accept the agreement and click **Next** on each screen.
5. When you see a screen of checkboxes, **tick all of them**, especially
   **"Add to PATH"**.
6. Click **Install**, then **Finish**.

**On Mac:**

4. The download is a `.zip` file. Double-click it and it will turn into
   an app called **Visual Studio Code**.
5. Drag **Visual Studio Code** into your **Applications** folder.
6. Open it from Applications (or Launchpad). If the Mac asks *"Are you
   sure you want to open it?"*, click **Open**.

When VS Code opens, you'll see a welcome screen. You can close any
"Welcome" or "Get Started" tabs. You don't need them.

---

## Part 3 — Download this project

1. Go to this page: **https://github.com/ahobbs1989/old-age-home-waiting-list**
2. Click the green **`<> Code`** button near the top right of the list of
   files.
3. Click **Download ZIP** at the bottom of the little menu that appears.
4. Find the downloaded file in your **Downloads** folder. It will be called
   something like `old-age-home-waiting-list-main.zip`.
5. **Unzip it:**
   - **Windows:** right-click the file, choose **Extract All...**, then
     click **Extract**.
   - **Mac:** double-click the file.
6. You now have a normal folder with the same name (without `.zip`).
   **Move this folder to your Desktop** (or your Documents folder) so it's
   easy to find. **Don't** leave it inside the zip file or your Downloads
   folder.

From now on, this guide calls that folder **the project folder**.

> **Windows tip:** sometimes unzipping creates a folder *inside* a folder
> with the same name. If you open the folder and see only one other folder
> inside it, use that **inner** one as the project folder. You know you have
> the right one when you can see files called `main.py` and `README.md`.

---

## Part 4 — Open the project in VS Code

1. Open **VS Code**.
2. At the top of the screen, click **File**, then **Open Folder...**
   (On a Mac it may just say **Open...**.)
3. Find **the project folder** (on your Desktop), click it **once** so it's
   highlighted, then click **Select Folder** (Windows) or **Open** (Mac).
4. A box will pop up asking **"Do you trust the authors of the files in
   this folder?"** Click **Yes, I trust the authors**.
5. On the left side of VS Code you should now see a list of files,
   including `main.py`, `README.md` and a folder called `app`.

You'll never need to edit these files yourself. Claude will do that.

> **Every time you come back to work on the website**, open VS Code. It
> usually reopens the project folder automatically. If it doesn't, repeat
> steps 2–4 above.

---

## Part 5 — Install Claude Code inside VS Code

Claude Code is an add-on (VS Code calls these "extensions") that puts
Claude right inside VS Code, where it can see the project and work on it.

### Step 5.1: Install the extension

1. Look at the narrow strip of icons down the **far left edge** of VS Code.
2. Click the icon that looks like **four little squares** (one slightly
   apart from the others). This is **Extensions**.
   - Can't find it? Press **Ctrl+Shift+X** (Windows) or **Cmd+Shift+X**
     (Mac).
3. A search box appears at the top. Type **Claude Code**.
4. Click the result called **Claude Code** published by **Anthropic**.
   (Make sure it says Anthropic. Ignore look-alikes from other publishers.)
5. Click the blue **Install** button.
6. If VS Code asks whether you trust the publisher, click **Trust
   Publisher & Install** (or similar).

### Step 5.2: Open Claude and sign in

1. Look for the **Claude icon** (a small orange star/spark shape). It
   appears in one of these places:
   - in the strip of icons on the **far left edge**, or
   - in the **top right corner** of VS Code, when a file is open.
   - Still can't find it? Press **Ctrl+Shift+P** (Windows) or
     **Cmd+Shift+P** (Mac), type **Claude Code: Open**, and press **Enter**.
2. Click it. A Claude chat panel opens.
3. Click **Sign in** (or follow the on-screen prompt) and choose to log in
   with your **Claude.ai account** (the one from Part 1).
4. Your web browser opens. Log in if asked, then click **Authorize** /
   **Allow**.
5. Switch back to VS Code. The Claude panel should now show a box where
   you can type a message. **You're ready.**

> **Windows only:** if Claude tells you it needs **Git** installed, go to
> **[git-scm.com/downloads](https://git-scm.com/downloads)**, download the
> Windows version, and install it, clicking **Next** on every screen
> without changing anything. Then close VS Code completely, reopen it, and
> try again.

---

## Part 6 — Talk to Claude

This is where everything happens. You type what you want in normal
English, and Claude does it.

Claude already knows about this project. There's a file in the project
folder called `CLAUDE.md` that explains to Claude how the website is
built and the rules it should follow. You don't need to explain any of
that.

### How it works

1. Click in the message box at the bottom of the Claude panel.
2. Type (or copy and paste) what you'd like. See the ready-made messages
   below.
3. Press **Enter**.
4. Claude will reply, explain what it's going to do, and then start working.

### When Claude asks for permission

Before Claude changes a file or runs something on your computer, it will
often **stop and ask you**. You'll see a box with buttons like **Yes**,
**Yes, and don't ask again**, and **No**.

- Read the one-line description of what it wants to do.
- If it matches what you asked for, click **Yes**.
- If you're not sure, click **No** and type: *"What were you trying to do
  just then, and why? Please explain in plain English."*
- Choosing **"Yes, and don't ask again"** for a type of action is fine
  once you're comfortable. It saves you a lot of clicking.

### Golden rules

- **Ask for one thing at a time.** Wait until Claude has finished before
  asking for the next thing.
- **Tell Claude you're not technical.** It will explain things more simply
  and walk you through any steps it can't do for you (like signing up for
  a website).
- **If you don't understand something, ask.** *"I don't understand, can you
  explain that more simply?"* always works.
- **If something goes wrong, tell Claude exactly what you see.** Copy any
  error message and paste it in, or describe it: *"The page says 'Not
  Found'."*
- **Claude can undo things.** *"Please undo the last change you made"* is a
  perfectly good request.
- **Never paste real passwords or bank details into the chat** unless
  you understand why Claude needs them. Claude will usually tell you where
  to type them yourself instead.

---

## Ready-made messages to send Claude

Copy any of these into the Claude message box. Change the wording in
*italics* to suit you.

### ▶ The very first thing to send

```
Hi Claude. I'm not technical at all and I've never done anything like
this before. Please set up this project on my computer and start the
website so I can see it in my web browser. Install anything that's
needed, explain each step in plain English, and tell me exactly what to
click if I need to do anything myself.
```

Claude will install what's needed (including a program called Python),
start the website, and give you a link like `http://localhost:8080` to
open in your browser.

> The website only runs **on your computer** at this stage, and only while
> VS Code is open. That's normal. It's for trying things out. Putting it on
> the internet is covered further down.

### ▶ Show me around

```
Please give me a simple tour of what this website does. What pages are
there, what can applicants do, and what can staff do in the admin area?
How do I log in to the admin area?
```

### ▶ Start the website again (next time you open VS Code)

```
Please start the website again so I can see it in my browser.
```

### ▶ Change how the website looks or works

Describe the change the way you'd describe it to a person. For example:

```
On the "Join the waiting list" page, please add a field asking for the
applicant's *preferred move-in date*. Make it optional. Then restart the
website so I can see the change.
```

```
Please change the *banking details shown for EFT payments* to:
*Bank name, account number, branch code, reference format*.
```

```
Please change the wording at the top of the home page to say
*"Welcome to Sunnyvale Retirement Village"*.
```

```
Please change the colours of the website to *dark green and white*.
```

After any change, it's a good idea to send:

```
Please check that everything still works properly after that change,
and tell me in plain English if anything is broken.
```

### ▶ Put the website on the internet (so others can use it)

```
I want to put this website on the internet so applicants and staff can
use it from anywhere. Please recommend the simplest, cheapest hosting
option for someone non-technical, then walk me through it step by step.
Make sure the waiting-list data is stored safely so it isn't lost when
the server restarts, and make sure the admin password is changed from
the default to something secure. Tell me exactly which websites to sign
up for and what to click, and do as much of the work for me as you can.
```

Claude will guide you through creating any accounts you need (for example
a free **GitHub** account to store the code online, and a hosting service
such as **Railway**). Some steps, like signing up and entering payment
details, you'll have to do yourself in your browser. Claude will tell
you exactly what to click.

> **Important:** the admin area's default password is `admin123`. Anyone
> could guess that. Never share your website's link before the password
> has been changed. The message above asks Claude to do this for you.

### ▶ Update the live website after making changes

Once the website is on the internet, changes you make with Claude only
happen on your computer until you publish them:

```
I've made some changes and I'm happy with them. Please publish them
to the live website, and tell me when it's done and how to check.
```

### ▶ Change the admin password

```
Please help me change the admin password on the live website. Don't ask
me to type the new password into this chat. Tell me where to enter it
myself.
```

### ▶ Back up the waiting-list data

```
Please explain how I can make a backup copy of all the waiting-list
data from the live website, and help me do it now.
```

### ▶ When something's wrong

```
Something isn't working. Here's what I see: *describe what you see, or
paste the error message here*. Please find out what's wrong and fix it,
and explain what happened in plain English.
```

```
The website was working yesterday and now it isn't. Please investigate
and fix it.
```

### ▶ Save your work to GitHub

```
Please save all my changes to GitHub with a short description of what
changed. If I haven't set up GitHub yet, walk me through it.
```

---

## Common questions

**Do I need to understand the code?**
No. Ask Claude to explain anything you're curious about, but you never
need to read or edit code yourself.

**Will I break something?**
It's very hard to do lasting damage. Claude can undo changes, and while
you're trying things out on your own computer, nothing you do affects the
live website. If you're worried, ask Claude *"Before you change anything,
please save a copy so we can go back to it if needed."*

**Where do I see the website while I'm working on it?**
Ask Claude to start it. It will give you a link (usually
`http://localhost:8080`) to open in your normal web browser. This link only
works on your own computer.

**How do staff log in to the admin area?**
Add `/admin` to the end of the website's address (for example
`http://localhost:8080/admin`) and enter the admin password. Ask Claude
if you're not sure what the password currently is.

**Does this website take card payments?**
No. Applicants are shown your bank details and pay by EFT. Staff then
mark the application as "paid" in the admin area. If you want real online
payments one day, ask Claude what that would involve.

**Does it send renewal reminder emails automatically?**
No. The admin area has a **Renewal follow-up** report listing applicants
who are overdue, so staff can contact them. Ask Claude if you'd like to
explore automating this.

**How accurate are the waiting-time estimates?**
They're rough. They're based on a "units available per year" figure that
staff set in the admin area under **Wait-time settings**. Keep that figure
up to date for better estimates.

**Claude stopped halfway / I closed VS Code by accident.**
Just reopen VS Code, open the Claude panel, and say *"Please carry on with
what we were doing"* or describe what you were trying to do.

**Claude says I've hit a usage limit.**
Claude subscriptions have a usage allowance that resets every few hours.
Wait a while and try again, or consider upgrading your plan.

**The Claude icon has disappeared.**
Press **Ctrl+Shift+P** (Windows) or **Cmd+Shift+P** (Mac), type
**Claude Code: Open**, and press **Enter**. If that doesn't work, repeat
[Part 5](#part-5--install-claude-code-inside-vs-code).

---

## For developers

If you're a developer, see [CLAUDE.md](CLAUDE.md) for the project's
architecture, conventions, commands and scope notes.
