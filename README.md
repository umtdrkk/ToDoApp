# Focus — Personal Productivity App

Your tasks are stored in **tasks.db** (SQLite), a real database file sitting right in this folder. It persists forever and you can back it up anytime.

---

## Setup (one time only)

Open **Terminal** and run:

```bash
pip3 install flask
```

That's it. Flask is the only thing you need to install.

---

## Running the app

In Terminal, navigate to this folder and run:

```bash
cd ~/path/to/this/folder
python3 app.py
```

Then open your browser and go to:

**http://localhost:5000**

To stop the app, press `Ctrl+C` in Terminal.

---

## Features

- ✅ Add, edit, delete tasks
- 🗓 Calendar view (tasks with due dates show up on the calendar)
- 📊 Overview stats (total, completed, due today, overdue)
- 🏷 Categories and priorities
- 🔍 Search tasks
- 📌 Filter by: All / Today / Upcoming / Done
- ⌨️ Keyboard shortcuts: `Cmd+N` = new task, `Esc` = close modal

## Your data

- All tasks are saved in `tasks.db` in this folder
- To back up your data: copy `tasks.db` somewhere safe
- Data is never lost unless you delete the file
