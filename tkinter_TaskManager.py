"""
Aim :- Develop programs to learn GUI programming using Tkinter.
Tkinter Mini-Project: Study Task Tracker (CRUD Application)
===========================================================
A standalone Python GUI application built with Tkinter and ttk demonstrating :-
- Responsive form layout using grid() and pack()
- Data binding with tk.StringVar()
- Scrollable tabular data display using ttk.Treeview and ttk.Scrollbar
- CRUD operations (Create, Read, Update status, Delete rows)
- Input validation and confirmation alerts with tkinter.messagebox
- Saving and loading structured JSON files with tkinter.filedialog

Run with :- python tkinter_learning_suite.py
"""

import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class TaskTrackerApp(tk.Tk):
    """Standalone Task & Study Tracker application built with Tkinter and ttk."""

    def __init__(self):
        super().__init__()
        self.title("Tkinter Mini-Project — Study Task Tracker")
        self.geometry("820x520")
        self.minsize(720, 440)

        # Configure modern ttk styling
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#1e293b")
        self.style.configure("Subheader.TLabel", font=("Helvetica", 10), foreground="#475569")

        # Shared status bar variable
        self.status_var = tk.StringVar(value="Ready — Add a new task or select an existing row below.")
        self._build_header()
        self._build_main_interface()
        self._build_statusbar()

        # Keyboard shortcuts
        self.bind("<Return>", lambda event: self._add_task())
        self.bind("<Delete>", lambda event: self._delete_selected_task())
        self.bind("<Control-q>", lambda event: self.quit())

    def _build_header(self):
        """Builds the top title banner."""
        header_frame = ttk.Frame(self, padding=(16, 12, 16, 6))
        header_frame.pack(fill=tk.X)

        ttk.Label(
            header_frame,
            text="Study Task Tracker",
            style="Header.TLabel",
        ).pack(anchor=tk.W)
        ttk.Label(
            header_frame,
            text="Create, update, filter, and export study tasks using ttk.Treeview, Combobox, and File Dialogs.",
            style="Subheader.TLabel",
        ).pack(anchor=tk.W, pady=(2, 0))

    def _build_main_interface(self):
        """Builds the input form, scrollable Treeview table, and action bar."""
        container = ttk.Frame(self, padding=(16, 8, 16, 12))
        container.pack(fill=tk.BOTH, expand=True)

        # 1. Input Form (grid layout)
        form_frame = ttk.LabelFrame(container, text="Add New Study Task", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Task Title:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        self.task_title_var = tk.StringVar()
        self.title_entry = ttk.Entry(form_frame, textvariable=self.task_title_var, width=30)
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 12))

        ttk.Label(form_frame, text="Category:").grid(row=0, column=2, sticky=tk.W, padx=(0, 6))
        self.task_cat_var = tk.StringVar(value="Widgets")
        ttk.Combobox(
            form_frame,
            textvariable=self.task_cat_var,
            values=["Widgets", "Layouts", "Events", "Canvas", "Dialogs"],
            state="readonly",
            width=14,
        ).grid(row=0, column=3, sticky=tk.W, padx=(0, 12))

        ttk.Label(form_frame, text="Priority:").grid(row=0, column=4, sticky=tk.W, padx=(0, 6))
        self.task_prio_var = tk.StringVar(value="High")
        ttk.Combobox(
            form_frame,
            textvariable=self.task_prio_var,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=10,
        ).grid(row=0, column=5, sticky=tk.W, padx=(0, 12))

        ttk.Button(form_frame, text="Add Task", command=self._add_task).grid(row=0, column=6, padx=4)
        form_frame.grid_columnconfigure(1, weight=1)

        # 2. Treeview Table with Vertical Scrollbar
        table_frame = ttk.Frame(container)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("title", "category", "priority", "status", "created")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        headings = {
            "title": ("Task Title", 280),
            "category": ("Category", 120),
            "priority": ("Priority", 100),
            "status": ("Status", 110),
            "created": ("Created At", 140),
        }
        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Double-click row to toggle status
        self.tree.bind("<Double-1>", lambda event: self._toggle_task_status())

        # 3. Bottom Action Buttons
        action_bar = ttk.Frame(container, padding=(0, 10, 0, 0))
        action_bar.pack(fill=tk.X)

        ttk.Button(action_bar, text="Toggle Completed", command=self._toggle_task_status).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(action_bar, text="Delete Selected", command=self._delete_selected_task).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(action_bar, text="Clear All", command=self._clear_all_tasks).pack(
            side=tk.LEFT, padx=(0, 8)
        )

        ttk.Button(action_bar, text="Export JSON...", command=self._export_tasks_json).pack(side=tk.RIGHT)
        ttk.Button(action_bar, text="Import JSON...", command=self._import_tasks_json).pack(
            side=tk.RIGHT, padx=(0, 8)
        )

        # Pre-populate starter tasks
        starter_tasks = [
            ("Practice StringVar two-way binding", "Events", "High", "Completed"),
            ("Build responsive 3x3 grid layout", "Layouts", "High", "In Progress"),
            ("Create custom modal Toplevel form", "Dialogs", "Medium", "Pending"),
            ("Animate shapes on tk.Canvas with .after()", "Canvas", "Low", "Pending"),
        ]
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        for title, cat, prio, status in starter_tasks:
            self.tree.insert("", tk.END, values=(title, cat, prio, status, now_str))

    def _build_statusbar(self):
        """Builds the bottom status bar."""
        status_frame = ttk.Frame(self, relief=tk.SUNKEN, padding=(12, 4))
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)

    # =========================================================================
    # CRUD & File Operations
    # =========================================================================
    def _add_task(self):
        title = self.task_title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation Error", "Please enter a task title before adding.")
            self.title_entry.focus_set()
            return

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tree.insert(
            "",
            tk.END,
            values=(title, self.task_cat_var.get(), self.task_prio_var.get(), "Pending", now_str),
        )
        self.task_title_var.set("")
        self.title_entry.focus_set()
        self.status_var.set(f"Added task: '{title}'")

    def _toggle_task_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a Row", "Please select a task in the table first.")
            return
        item_id = selected[0]
        vals = list(self.tree.item(item_id, "values"))
        vals[3] = "Completed" if vals[3] != "Completed" else "Pending"
        self.tree.item(item_id, values=vals)
        self.status_var.set(f"Marked '{vals[0]}' as {vals[3]}.")

    def _delete_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a Row", "Please select a task to delete.")
            return
        item_id = selected[0]
        title = self.tree.item(item_id, "values")[0]
        self.tree.delete(item_id)
        self.status_var.set(f"Deleted task: '{title}'")

    def _clear_all_tasks(self):
        children = self.tree.get_children()
        if not children:
            return
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to remove all tasks?"):
            for item_id in children:
                self.tree.delete(item_id)
            self.status_var.set("Cleared all tasks.")

    def _export_tasks_json(self):
        filepath = filedialog.asksaveasfilename(
            title="Export Tasks to JSON",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return

        records = []
        for item_id in self.tree.get_children():
            title, cat, prio, status, created = self.tree.item(item_id, "values")
            records.append(
                {
                    "title": title,
                    "category": cat,
                    "priority": prio,
                    "status": status,
                    "created_at": created,
                }
            )
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        self.status_var.set(f"Exported {len(records)} tasks to {filepath}")

    def _import_tasks_json(self):
        filepath = filedialog.askopenfilename(
            title="Import Tasks from JSON",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                records = json.load(f)
            if not isinstance(records, list):
                raise ValueError("JSON root must be a list of task objects.")

            count = 0
            for item in records:
                title = item.get("title", "Untitled Task")
                cat = item.get("category", "Widgets")
                prio = item.get("priority", "Medium")
                status = item.get("status", "Pending")
                created = item.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M"))
                self.tree.insert("", tk.END, values=(title, cat, prio, status, created))
                count += 1
            self.status_var.set(f"Imported {count} tasks from {filepath}")
        except Exception as exc:
            messagebox.showerror("Import Error", f"Failed to load JSON file:\n{exc}")


if __name__ == "__main__":
    app = TaskTrackerApp()
    app.mainloop()