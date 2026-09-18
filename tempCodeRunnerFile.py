import os, json, datetime, random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from calendar_sync import add_revision_event
from PIL import Image, ImageTk

# --- CONFIG ---
MAIN_STORAGE = "revision_material.json"
RECYCLED_FOLDER = "recycled_material.json"
INTERVALS = [1,3,7,14,30,60,90]

quotes = [
    "Success is the sum of small efforts, repeated day in and day out.",
    "Discipline is the bridge between goals and accomplishment.",
    "Small progress each day adds up to big results.",
    "Do not fear boredom or anxiety; they are quiet teachers of patience."
]

# --- Helpers ---
def load_data(file):
    return json.load(open(file)) if os.path.exists(file) else {}

def save_data(file, data):
    json.dump(data, open(file,"w"), indent=4)

def calculate_today_progress():
    today = datetime.date.today()
    data = load_data(MAIN_STORAGE)
    total, done = 0, 0
    for _, info in data.items():
        schedule = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in info["schedule"]]
        total += len(schedule)
        done += sum(1 for d in schedule if d <= today)
    return int((done/total)*100) if total else 0

# --- Actions ---
def add_material():
    topic = topic_entry.get()
    date = date_entry.get()
    if not topic or not date:
        messagebox.showwarning("Missing info","Enter topic and date")
        return
    file_path = filedialog.askopenfilename(title="Select revision file")
    if not file_path:
        return
    start = datetime.datetime.strptime(date,"%Y-%m-%d").date()
    schedule = [(start+datetime.timedelta(days=i)).isoformat() for i in INTERVALS]
    data = load_data(MAIN_STORAGE)
    data[topic] = {"start":start.isoformat(),"schedule":schedule,"file":file_path}
    save_data(MAIN_STORAGE,data)
    add_revision_event(topic,date,INTERVALS)
    messagebox.showinfo("Added",f"Added {topic}\nLinked file: {file_path}")
    refresh_progress()

def show_today_material():
    today = datetime.date.today().isoformat()
    data = load_data(MAIN_STORAGE)
    todays = [t for t,i in data.items() if today in i["schedule"]]
    messagebox.showinfo("Today's Material","\n".join(todays) if todays else "No material today")

def show_all_materials_status():
    today = datetime.date.today()
    data = load_data(MAIN_STORAGE)
    if not data:
        messagebox.showinfo("Status","No materials found")
        return
    text=""
    for topic,info in data.items():
        schedule=[datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in info["schedule"]]
        done=sum(1 for d in schedule if d<=today)
        total=len(schedule)
        next_rev=next((d for d in schedule if d>today),"✅ All done")
        text+=f"{topic}\n  Start:{info['start']}\n  Done:{done}/{total}\n  Next:{next_rev}\n\n"
    messagebox.showinfo("All Status",text)

def remove_material():
    topic=topic_entry.get()
    data=load_data(MAIN_STORAGE)
    if topic in data:
        del data[topic]
        save_data(MAIN_STORAGE,data)
        messagebox.showinfo("Removed",f"Removed {topic}")
        refresh_progress()
    else:
        messagebox.showwarning("Not Found",f"{topic} not found")

def recycle_expired():
    today=datetime.date.today()
    data=load_data(MAIN_STORAGE)
    recycled=load_data(RECYCLED_FOLDER)
    expired=[t for t,i in data.items() if (today-datetime.datetime.strptime(i["start"],"%Y-%m-%d").date()).days>90]
    for t in expired:
        recycled[t]={"recycled_on":today.isoformat()}
        del data[t]
    save_data(MAIN_STORAGE,data); save_data(RECYCLED_FOLDER,recycled)
    if expired: messagebox.showinfo("Recycled",f"♻️ {', '.join(expired)}")

def purge_recycled():
    today=datetime.date.today()
    recycled=load_data(RECYCLED_FOLDER)
    to_delete=[t for t,i in recycled.items() if (today-datetime.datetime.strptime(i["recycled_on"],"%Y-%m-%d").date()).days>90]
    for t in to_delete: del recycled[t]
    save_data(RECYCLED_FOLDER,recycled)
    if to_delete: messagebox.showinfo("Deleted",f"🗑️ {', '.join(to_delete)}")

def refresh_progress():
    progress["value"]=calculate_today_progress()

# --- GUI ---
root=tk.Tk()
root.title("Revision Manager")
root.geometry("900x600")

# Background image (PNG version)
bg_image = Image.open("study_bg.png")   # ensure your image is saved as PNG
bg = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg)
bg_label.place(relwidth=1, relheight=1)

# Motivational quote (kept at top, styled black/white)
quote_label = tk.Label(root, text=random.choice(quotes),
                       font=("Helvetica", 14, "italic"),
                       bg="black", fg="white", relief="flat")
quote_label.place(relx=0.5, y=40, anchor="center")

# Input fields (smaller, shifted bottom-left on shirt area)
tk.Label(root, text="Material Name:", bg="black", fg="white").place(x=50, y=400)
topic_entry = tk.Entry(root, width=18, bg="black", fg="white", relief="flat")
topic_entry.place(x=180, y=400)

tk.Label(root, text="Start Date (YYYY-MM-DD):", bg="black", fg="white").place(x=50, y=430)
date_entry = tk.Entry(root, width=18, bg="black", fg="white", relief="flat")
date_entry.place(x=180, y=430)

# Buttons (compact, black background, white text, bottom-left corner)
btn_style = {"width":16, "bg":"black", "fg":"white", "relief":"flat", "highlightthickness":0}

tk.Button(root, text="➕ Add Material", command=add_material, **btn_style).place(x=50, y=460)
tk.Button(root, text="📅 Show Today's Material", command=show_today_material, **btn_style).place(x=220, y=460)
tk.Button(root, text="📊 Show All Status", command=show_all_materials_status, **btn_style).place(x=50, y=490)
tk.Button(root, text="❌ Remove Material", command=remove_material, **btn_style).place(x=220, y=490)
tk.Button(root, text="♻️ Recycle Expired", command=recycle_expired, **btn_style).place(x=50, y=520)
tk.Button(root, text="🗑️ Purge Recycled", command=purge_recycled, **btn_style).place(x=220, y=520)

# Progress bar (aligned with buttons at bottom-left)
progress = ttk.Progressbar(root, length=250, mode="determinate")
progress.place(x=100, y=550)
refresh_progress()

root.mainloop()