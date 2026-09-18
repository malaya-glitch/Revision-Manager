# Revision Manager

A desktop study planner built with Python and Tkinter. It creates a spaced-repetition schedule for each study topic and can add the revision sessions to Google Calendar.

## Features

- Adds a topic, a start date, and a linked study file.
- Schedules revisions after 1, 3, 7, 14, 30, 60, and 90 days.
- Shows today's due materials and each topic's revision progress.
- Creates 30-minute Google Calendar events for scheduled revisions.
- Recycles topics after 90 days and permanently purges recycled topics after another 90 days.

## Requirements

- Python 3.9 or newer
- Tkinter (normally included with Python on Windows)
- Pillow
- Google Calendar API client libraries

Install the external packages:

```bash
pip install Pillow google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Google Calendar setup

1. In [Google Cloud Console](https://console.cloud.google.com/), create or select a project and enable the **Google Calendar API**.
2. Create an OAuth 2.0 **Desktop app** client and download its JSON credentials.
3. Save the downloaded file as `credentials.json` in the project root.
4. Run the app and complete the browser sign-in and consent flow. A local `token.json` will be created automatically.

`credentials.json` and `token.json` are intentionally ignored by Git and must never be committed.

## Run

From the project folder, run:

```bash
python main.py
```

Enter a material name and start date in `YYYY-MM-DD` format, then select the related study file and choose **Add Material**.

## Project files

- `main.py` — Tkinter application and revision workflow.
- `calendar_sync.py` — Google Calendar authentication and event creation.
- `revision_material.json` — saved active revision schedules.
- `recycled_material.json` — records of recycled materials.
- `study_bg.png` — application background image.

## Notes

The app stores the selected study file's local path. If the file is moved or opened on a different computer, that stored path will no longer point to it.
