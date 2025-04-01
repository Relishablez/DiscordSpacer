import tkinter as tk
from tkinter import PhotoImage

# --- Unicode Options ---
UNICODE_SPACES = {
    "Z W S (​)": "​",
    "L R M(‎)": "‎",
    "R L M (‏)": "‏",
    "B B  (⠀)": "⠀",
    "H F  (ㅤ)": "ㅤ"
}

# --- GUI Setup ---
root = tk.Tk()
root.title("Stealthifier")
root.geometry("900x700")
root.configure(bg="#1e1e1e")
root.resizable(True, True)

# --- Set Custom Icon (Optional .ico file required) ---
try:
    icon = PhotoImage(file="icon.png")  # Replace with your icon path
    root.iconphoto(False, icon)
except Exception:
    pass

# --- Widgets ---
tk.Label(root, text="Enter your message:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10)).pack(pady=10)

entry_frame = tk.Frame(root, bg="#1e1e1e")
entry_frame.pack(fill="both", padx=10, expand=True)
entry_scrollbar = tk.Scrollbar(entry_frame)
entry_scrollbar.pack(side="right", fill="y")
entry_text = tk.Text(
    entry_frame,
    height=4,
    wrap="word",
    yscrollcommand=entry_scrollbar.set,
    bg="#333333",
    fg="white",
    insertbackground="white",
    font=("Arial", 11),
    relief="flat",
    bd=2
)
entry_text.pack(expand=True, fill="both")
entry_scrollbar.config(command=entry_text.yview)

output_widgets = {}
copy_buttons = {}

container = tk.Frame(root, bg="#1e1e1e")
container.pack(pady=20, fill="both", expand=True)

def copy_to_clipboard(text, btn):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    btn.config(text="Copied", state="disabled")
    root.after(1500, lambda: btn.config(text="Copy", state="normal"))

def stealthify_all(event=None):
    input_text = entry_text.get("1.0", tk.END).strip()
    if not input_text:
        return
    for label, char in UNICODE_SPACES.items():
        converted = char.join(input_text.split(' '))
        widget = output_widgets[label]
        widget.delete("1.0", tk.END)
        widget.insert("1.0", converted)
        if copy_buttons.get(label):
            copy_buttons[label].config(text="Copy", state="normal")

def copy_all():
    lines = []
    for label in UNICODE_SPACES:
        text = output_widgets[label].get("1.0", tk.END).strip()
        if text:
            lines.append(text)
    full_text = "\n".join(lines)
    root.clipboard_clear()
    root.clipboard_append(full_text)
    root.update()
    copy_all_btn.config(text="Copied All", state="disabled")
    root.after(1500, lambda: copy_all_btn.config(text="Copy All", state="normal"))

def clear_all():
    entry_text.delete("1.0", tk.END)
    for widget in output_widgets.values():
        widget.delete("1.0", tk.END)
    for btn in copy_buttons.values():
        btn.config(text="Copy", state="normal")
    copy_all_btn.config(text="Copy All", state="normal")

stealthify_btn = tk.Button(root, text="Stealthify All", command=stealthify_all, bg="#3b82f6", fg="white", relief="flat")
stealthify_btn.pack()

copy_all_btn = tk.Button(root, text="Copy All", command=copy_all, bg="#f59e0b", fg="white", relief="flat")
copy_all_btn.pack(pady=(0, 5))

clear_all_btn = tk.Button(root, text="Clear All", command=clear_all, bg="#ef4444", fg="white", relief="flat")
clear_all_btn.pack(pady=(0, 10))

for label, char in UNICODE_SPACES.items():
    frame = tk.Frame(container, bg="#1e1e1e")
    frame.pack(pady=5, fill='both', expand=True)
    tk.Label(frame, text=label, bg="#1e1e1e", fg="#bbbbbb", width=30, anchor='w').pack(side="left", padx=(5, 0))
    text_widget = tk.Text(
        frame,
        height=2,
        wrap="word",
        bg="#2d2d2d",
        fg="white",
        font=("Arial", 10),
        relief="solid",
        bd=1,
        padx=5,
        pady=3
    )
    text_widget.pack(side="left", padx=5, fill='both', expand=True)
    btn = tk.Button(frame, text="Copy", bg="#10b981", fg="white", relief="flat")
    btn.pack(side="left", padx=(5, 10))
    btn.config(command=lambda t=text_widget, b=btn: copy_to_clipboard(t.get("1.0", tk.END).strip(), b))
    output_widgets[label] = text_widget
    copy_buttons[label] = btn

# Bind Enter key to run stealthify_all
root.bind('<Return>', stealthify_all)

root.mainloop()
