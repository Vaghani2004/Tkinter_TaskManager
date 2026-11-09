"""
Aim :- Develop programs to learn GUI programming using Tkinter.
Tkinter Mini-Project: Study Task Tracker (CRUD Application)
===========================================================
A standalone Python GUI application built with Tkinter and ttk demonstrating :-
- Responsive form layout using grid() and pack()
- Data binding with tk.StringVar()
- Scrollable tabular data display using ttk.Treeview and ttk.Scrollbar
- CRUD operations (Create, Read, Update status, Edit task, Delete rows)
- Dynamic Task Search and Filtering (by Title, Category, Priority, and Status)
- Task Deadlines, Interactive Calendar Date Picker, and periodic .after() Reminders
- Permanent local storage with Python's built-in sqlite3 module
- Input validation and confirmation alerts with tkinter.messagebox
- Saving and loading structured JSON files with tkinter.filedialog
- Multi-theme UI customization (Light, Dark, Ocean Blue, Forest Green, High Contrast)

Run with :- python tkinter_TaskManager.py
"""

import calendar
import json
import os
import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class TaskTrackerApp(tk.Tk):
    """Standalone Task & Study Tracker application built with Tkinter and ttk."""

    CATEGORIES = ["Widgets", "Layouts", "Events", "Canvas", "Dialogs"]
    PRIORITIES = ["Low", "Medium", "High"]
    STATUSES = ["Pending", "In Progress", "Completed"]

    THEMES = {
        "Light": {
            "bg": "#f8fafc",
            "surface": "#ffffff",
            "fg": "#0f172a",
            "header_fg": "#1e293b",
            "sub_fg": "#475569",
            "btn_bg": "#e2e8f0",
            "btn_fg": "#0f172a",
            "btn_active": "#cbd5e1",
            "entry_bg": "#ffffff",
            "entry_fg": "#0f172a",
            "tree_bg": "#ffffff",
            "tree_fg": "#0f172a",
            "tree_heading_bg": "#e2e8f0",
            "tree_heading_fg": "#1e293b",
            "tree_selected_bg": "#2563eb",
            "tree_selected_fg": "#ffffff",
            "border": "#cbd5e1",
            "overdue_bg": "#fee2e2",
            "overdue_fg": "#991b1b",
            "approaching_bg": "#fef3c7",
            "approaching_fg": "#92400e",
            "completed_bg": "#dcfce7",
            "completed_fg": "#166534",
        },
        "Dark": {
            "bg": "#0f172a",
            "surface": "#1e293b",
            "fg": "#f1f5f9",
            "header_fg": "#f8fafc",
            "sub_fg": "#94a3b8",
            "btn_bg": "#334155",
            "btn_fg": "#f8fafc",
            "btn_active": "#475569",
            "entry_bg": "#1e293b",
            "entry_fg": "#f8fafc",
            "tree_bg": "#1e293b",
            "tree_fg": "#f1f5f9",
            "tree_heading_bg": "#334155",
            "tree_heading_fg": "#f8fafc",
            "tree_selected_bg": "#3b82f6",
            "tree_selected_fg": "#ffffff",
            "border": "#475569",
            "overdue_bg": "#451a1a",
            "overdue_fg": "#fca5a5",
            "approaching_bg": "#422006",
            "approaching_fg": "#fde68a",
            "completed_bg": "#052e16",
            "completed_fg": "#86efac",
        },
        "Ocean Blue": {
            "bg": "#f0f9ff",
            "surface": "#ffffff",
            "fg": "#0c4a6e",
            "header_fg": "#0369a1",
            "sub_fg": "#0284c7",
            "btn_bg": "#bae6fd",
            "btn_fg": "#0c4a6e",
            "btn_active": "#7dd3fc",
            "entry_bg": "#ffffff",
            "entry_fg": "#0c4a6e",
            "tree_bg": "#ffffff",
            "tree_fg": "#0c4a6e",
            "tree_heading_bg": "#e0f2fe",
            "tree_heading_fg": "#075985",
            "tree_selected_bg": "#0284c7",
            "tree_selected_fg": "#ffffff",
            "border": "#7dd3fc",
            "overdue_bg": "#ffe4e6",
            "overdue_fg": "#9f1239",
            "approaching_bg": "#fef9c3",
            "approaching_fg": "#854d0e",
            "completed_bg": "#d1fae5",
            "completed_fg": "#065f46",
        },
        "Forest Green": {
            "bg": "#f0fdf4",
            "surface": "#ffffff",
            "fg": "#14532d",
            "header_fg": "#166534",
            "sub_fg": "#15803d",
            "btn_bg": "#bbf7d0",
            "btn_fg": "#14532d",
            "btn_active": "#86efac",
            "entry_bg": "#ffffff",
            "entry_fg": "#14532d",
            "tree_bg": "#ffffff",
            "tree_fg": "#14532d",
            "tree_heading_bg": "#dcfce7",
            "tree_heading_fg": "#166534",
            "tree_selected_bg": "#16a34a",
            "tree_selected_fg": "#ffffff",
            "border": "#86efac",
            "overdue_bg": "#fee2e2",
            "overdue_fg": "#991b1b",
            "approaching_bg": "#fef3c7",
            "approaching_fg": "#92400e",
            "completed_bg": "#dcfce7",
            "completed_fg": "#166534",
        },
        "High Contrast": {
            "bg": "#000000",
            "surface": "#121212",
            "fg": "#ffffff",
            "header_fg": "#ffff00",
            "sub_fg": "#00ffff",
            "btn_bg": "#262626",
            "btn_fg": "#ffff00",
            "btn_active": "#404040",
            "entry_bg": "#000000",
            "entry_fg": "#ffffff",
            "tree_bg": "#000000",
            "tree_fg": "#ffffff",
            "tree_heading_bg": "#262626",
            "tree_heading_fg": "#ffff00",
            "tree_selected_bg": "#ffff00",
            "tree_selected_fg": "#000000",
            "border": "#ffffff",
            "overdue_bg": "#660000",
            "overdue_fg": "#ffffff",
            "approaching_bg": "#664d00",
            "approaching_fg": "#ffff00",
            "completed_bg": "#004d00",
            "completed_fg": "#00ff00",
        },
    }

    def __init__(self, db_path=None):
        super().__init__()
        self.title("Tkinter Mini-Project — Study Task Tracker")
        self.geometry("980x620")
        self.minsize(840, 520)

        # Database path & reminder tracking state
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = db_path or os.path.join(base_dir, "study_tasks.db")
        self.conn = None
        self._notified_task_ids = set()
        self._reminder_after_id = None

        # Configure modern ttk styling
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#1e293b")
        self.style.configure("Subheader.TLabel", font=("Helvetica", 10), foreground="#475569")

        # Theme state variable
        self.theme_var = tk.StringVar(value="Light")

        # Shared status bar variable
        self.status_var = tk.StringVar(value="Ready — Add a new task or select an existing row below.")

        # Initialize SQLite database before building interface
        self._init_database()

        self._build_header()
        self._build_main_interface()
        self._build_statusbar()

        # Apply initial theme and load tasks from SQLite
        self._apply_theme(self.theme_var.get())
        self._load_tasks_from_db(seed_if_first_run=True)

        # Keyboard shortcuts
        self.bind("<Return>", lambda event: self._handle_return_key(event))
        self.bind("<Delete>", lambda event: self._delete_selected_task())
        self.bind("<Control-e>", lambda event: self._edit_selected_task())
        self.bind("<Control-f>", lambda event: self.search_entry.focus_set())
        self.bind("<Control-q>", lambda event: self._on_close())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Start periodic deadline reminder check using Tkinter's .after()
        self._reminder_after_id = self.after(1500, self._check_deadlines)

    # =========================================================================
    # UI Construction
    # =========================================================================
    def _build_header(self):
        """Builds the top title banner and theme selector."""
        header_frame = ttk.Frame(self, padding=(16, 12, 16, 6))
        header_frame.pack(fill=tk.X)

        title_box = ttk.Frame(header_frame)
        title_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(
            title_box,
            text="Study Task Tracker",
            style="Header.TLabel",
        ).pack(anchor=tk.W)
        ttk.Label(
            title_box,
            text="Create, search, filter, edit, and track study tasks with SQLite persistence & deadline alerts.",
            style="Subheader.TLabel",
        ).pack(anchor=tk.W, pady=(2, 0))

        # Theme switcher controls
        theme_box = ttk.Frame(header_frame)
        theme_box.pack(side=tk.RIGHT, anchor=tk.NE)
        ttk.Label(theme_box, text="Theme:").pack(side=tk.LEFT, padx=(0, 6))
        self.theme_combo = ttk.Combobox(
            theme_box,
            textvariable=self.theme_var,
            values=list(self.THEMES.keys()),
            state="readonly",
            width=14,
        )
        self.theme_combo.pack(side=tk.LEFT)
        self.theme_combo.bind("<<ComboboxSelected>>", lambda event: self._apply_theme(self.theme_var.get()))

    def _build_main_interface(self):
        """Builds the input form, search/filter bar, scrollable Treeview table, and action bar."""
        container = ttk.Frame(self, padding=(16, 8, 16, 12))
        container.pack(fill=tk.BOTH, expand=True)

        # 1. Input Form (grid layout)
        form_frame = ttk.LabelFrame(container, text="Add New Study Task", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(form_frame, text="Task Title:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        self.task_title_var = tk.StringVar()
        self.title_entry = ttk.Entry(form_frame, textvariable=self.task_title_var, width=26)
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 12))

        ttk.Label(form_frame, text="Category:").grid(row=0, column=2, sticky=tk.W, padx=(0, 6))
        self.task_cat_var = tk.StringVar(value="Widgets")
        ttk.Combobox(
            form_frame,
            textvariable=self.task_cat_var,
            values=self.CATEGORIES,
            state="readonly",
            width=12,
        ).grid(row=0, column=3, sticky=tk.W, padx=(0, 12))

        ttk.Label(form_frame, text="Priority:").grid(row=0, column=4, sticky=tk.W, padx=(0, 6))
        self.task_prio_var = tk.StringVar(value="High")
        ttk.Combobox(
            form_frame,
            textvariable=self.task_prio_var,
            values=self.PRIORITIES,
            state="readonly",
            width=9,
        ).grid(row=0, column=5, sticky=tk.W, padx=(0, 12))

        ttk.Label(form_frame, text="Deadline:").grid(row=0, column=6, sticky=tk.W, padx=(0, 6))
        default_deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        self.task_deadline_var = tk.StringVar(value=default_deadline)
        self.deadline_entry = ttk.Entry(form_frame, textvariable=self.task_deadline_var, width=12)
        self.deadline_entry.grid(row=0, column=7, sticky=tk.W, padx=(0, 4))

        ttk.Button(
            form_frame,
            text="Pick Date",
            command=lambda: self._open_date_picker(self.task_deadline_var, self),
            width=9,
        ).grid(row=0, column=8, sticky=tk.W, padx=(0, 10))

        ttk.Button(form_frame, text="Add Task", command=self._add_task).grid(row=0, column=9, padx=4)
        form_frame.grid_columnconfigure(1, weight=1)

        # 1b. Search and Filter Bar
        filter_frame = ttk.LabelFrame(container, text="Search & Filter Tasks", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="Search Title:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=24)
        self.search_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 12))

        ttk.Label(filter_frame, text="Category:").grid(row=0, column=2, sticky=tk.W, padx=(0, 6))
        self.filter_cat_var = tk.StringVar(value="All")
        filter_cat_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_cat_var,
            values=["All"] + self.CATEGORIES,
            state="readonly",
            width=12,
        )
        filter_cat_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 12))

        ttk.Label(filter_frame, text="Priority:").grid(row=0, column=4, sticky=tk.W, padx=(0, 6))
        self.filter_prio_var = tk.StringVar(value="All")
        filter_prio_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_prio_var,
            values=["All"] + self.PRIORITIES,
            state="readonly",
            width=10,
        )
        filter_prio_combo.grid(row=0, column=5, sticky=tk.W, padx=(0, 12))

        ttk.Label(filter_frame, text="Status:").grid(row=0, column=6, sticky=tk.W, padx=(0, 6))
        self.filter_status_var = tk.StringVar(value="All")
        filter_status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_status_var,
            values=["All"] + self.STATUSES,
            state="readonly",
            width=12,
        )
        filter_status_combo.grid(row=0, column=7, sticky=tk.W, padx=(0, 10))

        ttk.Button(filter_frame, text="Reset Filters", command=self._reset_filters).grid(row=0, column=8, padx=4)
        filter_frame.grid_columnconfigure(1, weight=1)

        # Dynamic traces so changing search text or filter dropdowns updates the Treeview immediately
        self.search_var.trace_add("write", lambda *args: self._refresh_treeview())
        filter_cat_combo.bind("<<ComboboxSelected>>", lambda event: self._refresh_treeview())
        filter_prio_combo.bind("<<ComboboxSelected>>", lambda event: self._refresh_treeview())
        filter_status_combo.bind("<<ComboboxSelected>>", lambda event: self._refresh_treeview())

        # 2. Treeview Table with Vertical Scrollbar
        table_frame = ttk.Frame(container)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("title", "category", "priority", "status", "deadline", "created")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        headings = {
            "title": ("Task Title", 270),
            "category": ("Category", 110),
            "priority": ("Priority", 90),
            "status": ("Status", 110),
            "deadline": ("Deadline", 115),
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
        ttk.Button(action_bar, text="Edit Task", command=self._edit_selected_task).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(action_bar, text="Delete Selected", command=self._delete_selected_task).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(action_bar, text="Clear All", command=self._clear_all_tasks).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(
            action_bar,
            text="Check Deadlines",
            command=lambda: self._check_deadlines(force_popup=True),
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(action_bar, text="Export JSON...", command=self._export_tasks_json).pack(side=tk.RIGHT)
        ttk.Button(action_bar, text="Import JSON...", command=self._import_tasks_json).pack(
            side=tk.RIGHT, padx=(0, 8)
        )

    def _build_statusbar(self):
        """Builds the bottom status bar."""
        status_frame = ttk.Frame(self, relief=tk.SUNKEN, padding=(12, 4))
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT)

    # =========================================================================
    # SQLite Database Management
    # =========================================================================
    def _init_database(self):
        """Creates the SQLite database file and required tables if they do not exist."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS app_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            # Ensure backward compatibility if an older tasks table lacked 'deadline'
            cursor.execute("PRAGMA table_info(tasks)")
            existing_cols = {row[1] for row in cursor.fetchall()}
            if "deadline" not in existing_cols:
                default_dl = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
                cursor.execute(f"ALTER TABLE tasks ADD COLUMN deadline TEXT NOT NULL DEFAULT '{default_dl}'")
            self.conn.commit()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Failed to initialize SQLite database:\n{exc}")

    def _load_tasks_from_db(self, seed_if_first_run=False):
        """Loads tasks from SQLite and populates starter tasks on first application launch."""
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            if seed_if_first_run:
                cursor.execute("SELECT value FROM app_meta WHERE key = 'seeded'")
                already_seeded = cursor.fetchone()
                cursor.execute("SELECT COUNT(*) FROM tasks")
                task_count = cursor.fetchone()[0]

                if not already_seeded and task_count == 0:
                    today = datetime.now()
                    starter_tasks = [
                        (
                            "Practice StringVar two-way binding",
                            "Events",
                            "High",
                            "Completed",
                            (today - timedelta(days=1)).strftime("%Y-%m-%d"),
                        ),
                        (
                            "Build responsive 3x3 grid layout",
                            "Layouts",
                            "High",
                            "In Progress",
                            (today + timedelta(days=1)).strftime("%Y-%m-%d"),
                        ),
                        (
                            "Create custom modal Toplevel form",
                            "Dialogs",
                            "Medium",
                            "Pending",
                            (today + timedelta(days=3)).strftime("%Y-%m-%d"),
                        ),
                        (
                            "Animate shapes on tk.Canvas with .after()",
                            "Canvas",
                            "Low",
                            "Pending",
                            (today + timedelta(days=5)).strftime("%Y-%m-%d"),
                        ),
                    ]
                    now_str = today.strftime("%Y-%m-%d %H:%M")
                    cursor.executemany(
                        """
                        INSERT INTO tasks (title, category, priority, status, deadline, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        [(t, c, p, s, d, now_str) for t, c, p, s, d in starter_tasks],
                    )
                    cursor.execute("INSERT OR REPLACE INTO app_meta (key, value) VALUES ('seeded', '1')")
                    self.conn.commit()

            self._refresh_treeview()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Failed to load tasks from database:\n{exc}")

    # =========================================================================
    # Search, Filtering & Treeview Rendering
    # =========================================================================
    def _refresh_treeview(self):
        """Reloads and filters Treeview rows from SQLite based on active search and filter controls."""
        if not hasattr(self, "tree") or not self.conn:
            return

        selected_Before = self.tree.selection()
        selected_iid = selected_Before[0] if selected_Before else None

        for item_id in self.tree.get_children():
            self.tree.delete(item_id)

        search_query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        cat_filter = self.filter_cat_var.get() if hasattr(self, "filter_cat_var") else "All"
        prio_filter = self.filter_prio_var.get() if hasattr(self, "filter_prio_var") else "All"
        status_filter = self.filter_status_var.get() if hasattr(self, "filter_status_var") else "All"

        try:
            cursor = self.conn.cursor()
            sql = "SELECT id, title, category, priority, status, deadline, created_at FROM tasks WHERE 1=1"
            params = []

            if search_query:
                sql += " AND LOWER(title) LIKE ?"
                params.append(f"%{search_query}%")
            if cat_filter and cat_filter != "All":
                sql += " AND category = ?"
                params.append(cat_filter)
            if prio_filter and prio_filter != "All":
                sql += " AND priority = ?"
                params.append(prio_filter)
            if status_filter and status_filter != "All":
                sql += " AND status = ?"
                params.append(status_filter)

            sql += " ORDER BY id ASC"
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            for task_id, title, cat, prio, status, deadline, created in rows:
                tag = self._get_row_tag(status, deadline)
                iid = str(task_id)
                self.tree.insert(
                    "",
                    tk.END,
                    iid=iid,
                    values=(title, cat, prio, status, deadline, created),
                    tags=(tag,) if tag else (),
                )

            if selected_iid and self.tree.exists(selected_iid):
                self.tree.selection_set(selected_iid)
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Failed to filter tasks:\n{exc}")

    def _reset_filters(self):
        """Resets search text and category, priority, and status filters to show all tasks."""
        self.search_var.set("")
        self.filter_cat_var.set("All")
        self.filter_prio_var.set("All")
        self.filter_status_var.set("All")
        self._refresh_treeview()
        self.status_var.set("Filters reset — Showing all tasks.")

    def _get_row_tag(self, status, deadline_str):
        """Returns the visual Treeview tag ('completed', 'overdue', 'approaching', or '') for a row."""
        if status == "Completed":
            return "completed"
        deadline_date = self._parse_deadline_date(deadline_str)
        if not deadline_date:
            return ""
        today = datetime.now().date()
        if deadline_date < today:
            return "overdue"
        if deadline_date <= today + timedelta(days=1):
            return "approaching"
        return ""

    # =========================================================================
    # Validation, Date Picker & Deadline Reminders (.after)
    # =========================================================================
    @staticmethod
    def _parse_deadline_date(deadline_str):
        """Parses a YYYY-MM-DD string into a datetime.date object, or returns None if invalid."""
        if not deadline_str or deadline_str == "N/A":
            return None
        try:
            return datetime.strptime(deadline_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None

    def _validate_task_inputs(self, title, category, priority, status, deadline_str, parent=None):
        """Validates all task fields and shows a warning messagebox if any field is invalid."""
        dialog_parent = parent or self
        if not title or not title.strip():
            messagebox.showwarning("Validation Error", "Please enter a task title before saving.", parent=dialog_parent)
            return False
        if category not in self.CATEGORIES:
            messagebox.showwarning("Validation Error", f"Invalid category: '{category}'.", parent=dialog_parent)
            return False
        if priority not in self.PRIORITIES:
            messagebox.showwarning("Validation Error", f"Invalid priority: '{priority}'.", parent=dialog_parent)
            return False
        if status not in self.STATUSES:
            messagebox.showwarning("Validation Error", f"Invalid status: '{status}'.", parent=dialog_parent)
            return False
        if not self._parse_deadline_date(deadline_str):
            messagebox.showwarning(
                "Validation Error",
                "Please enter a valid deadline date in YYYY-MM-DD format (e.g., 2026-11-15).",
                parent=dialog_parent,
            )
            return False
        return True

    def _open_date_picker(self, target_var, parent_window):
        """Opens a pure-Tkinter modal calendar popup to select a YYYY-MM-DD deadline date."""
        current_date = self._parse_deadline_date(target_var.get()) or datetime.now().date()
        picker = tk.Toplevel(parent_window)
        picker.title("Select Deadline Date")
        picker.geometry("290x280")
        picker.resizable(False, False)
        picker.transient(parent_window)
        picker.grab_set()

        theme = self.THEMES.get(self.theme_var.get(), self.THEMES["Light"])
        picker.configure(bg=theme["bg"])

        state = {"year": current_date.year, "month": current_date.month}

        nav_frame = ttk.Frame(picker, padding=(10, 8))
        nav_frame.pack(fill=tk.X)

        month_label_var = tk.StringVar()
        cal_grid_frame = ttk.Frame(picker, padding=(10, 4))
        cal_grid_frame.pack(fill=tk.BOTH, expand=True)

        def render_month():
            for widget in cal_grid_frame.winfo_children():
                widget.destroy()

            month_label_var.set(f"{calendar.month_name[state['month']]} {state['year']}")

            days_header = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
            for idx, day_name in enumerate(days_header):
                ttk.Label(cal_grid_frame, text=day_name, anchor=tk.CENTER, width=4).grid(
                    row=0, column=idx, padx=1, pady=2
                )

            month_weeks = calendar.monthcalendar(state["year"], state["month"])
            for r_idx, week in enumerate(month_weeks, start=1):
                for c_idx, day_num in enumerate(week):
                    if day_num == 0:
                        ttk.Label(cal_grid_frame, text="", width=4).grid(row=r_idx, column=c_idx, padx=1, pady=1)
                    else:
                        def pick_day(d=day_num):
                            chosen = f"{state['year']:04d}-{state['month']:02d}-{d:02d}"
                            target_var.set(chosen)
                            picker.destroy()

                        ttk.Button(cal_grid_frame, text=str(day_num), width=3, command=pick_day).grid(
                            row=r_idx, column=c_idx, padx=1, pady=1
                        )

        def prev_month():
            if state["month"] == 1:
                state["month"] = 12
                state["year"] -= 1
            else:
                state["month"] -= 1
            render_month()

        def next_month():
            if state["month"] == 12:
                state["month"] = 1
                state["year"] += 1
            else:
                state["month"] += 1
            render_month()

        ttk.Button(nav_frame, text="<", width=3, command=prev_month).pack(side=tk.LEFT)
        ttk.Label(nav_frame, textvariable=month_label_var, anchor=tk.CENTER).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        ttk.Button(nav_frame, text=">", width=3, command=next_month).pack(side=tk.RIGHT)

        footer = ttk.Frame(picker, padding=(10, 6))
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Button(
            footer,
            text="Today",
            command=lambda: (target_var.set(datetime.now().strftime("%Y-%m-%d")), picker.destroy()),
        ).pack(side=tk.LEFT)
        ttk.Button(footer, text="Cancel", command=picker.destroy).pack(side=tk.RIGHT)

        render_month()

    def _check_deadlines(self, force_popup=False):
        """Periodically checks task deadlines using Tkinter's .after() and alerts on overdue/approaching tasks."""
        if not self.conn:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, title, status, deadline FROM tasks WHERE status != 'Completed'")
            rows = cursor.fetchall()

            today = datetime.now().date()
            overdue_tasks = []
            approaching_tasks = []
            newly_flagged_ids = []

            for task_id, title, status, deadline_str in rows:
                dl_date = self._parse_deadline_date(deadline_str)
                if not dl_date:
                    continue
                if dl_date < today:
                    overdue_tasks.append((task_id, title, deadline_str))
                    if task_id not in self._notified_task_ids:
                        newly_flagged_ids.append(task_id)
                elif dl_date <= today + timedelta(days=1):
                    approaching_tasks.append((task_id, title, deadline_str))
                    if task_id not in self._notified_task_ids:
                        newly_flagged_ids.append(task_id)

            # Refresh row tag highlighting
            self._refresh_treeview()

            if overdue_tasks or approaching_tasks:
                summary_parts = []
                if overdue_tasks:
                    summary_parts.append(f"{len(overdue_tasks)} overdue")
                if approaching_tasks:
                    summary_parts.append(f"{len(approaching_tasks)} due soon")
                self.status_var.set(f"Deadline Alert: {', '.join(summary_parts)}.")

                if force_popup or newly_flagged_ids:
                    lines = []
                    if overdue_tasks:
                        lines.append("OVERDUE TASKS:")
                        for _, t_title, d_str in overdue_tasks[:5]:
                            lines.append(f"  • {t_title} (Due: {d_str})")
                    if approaching_tasks:
                        if lines:
                            lines.append("")
                        lines.append("APPROACHING DEADLINES (Due Today/Tomorrow):")
                        for _, t_title, d_str in approaching_tasks[:5]:
                            lines.append(f"  • {t_title} (Due: {d_str})")

                    self._notified_task_ids.update(newly_flagged_ids)
                    messagebox.showwarning("Task Deadline Reminder", "\n".join(lines))
            elif force_popup:
                messagebox.showinfo("Deadlines Checked", "All active tasks are on schedule! No overdue or due-soon tasks.")
        except sqlite3.Error:
            pass
        finally:
            if self._reminder_after_id is not None:
                try:
                    self.after_cancel(self._reminder_after_id)
                except ValueError:
                    pass
            # Schedule next periodic check in 60 seconds
            self._reminder_after_id = self.after(60000, self._check_deadlines)

    # =========================================================================
    # CRUD, Editing & File Operations
    # =========================================================================
    def _handle_return_key(self, event):
        """Triggers _add_task when pressing Enter unless focus is in the search box."""
        if self.focus_get() == getattr(self, "search_entry", None):
            self._refresh_treeview()
        else:
            self._add_task()

    def _add_task(self):
        title = self.task_title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation Error", "Please enter a task title before adding.")
            self.title_entry.focus_set()
            return

        cat = self.task_cat_var.get()
        prio = self.task_prio_var.get()
        deadline = self.task_deadline_var.get().strip()

        if not self._validate_task_inputs(title, cat, prio, "Pending", deadline):
            self.deadline_entry.focus_set()
            return

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (title, category, priority, status, deadline, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, cat, prio, "Pending", deadline, now_str),
            )
            self.conn.commit()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Failed to save task:\n{exc}")
            return

        self._refresh_treeview()
        self.task_title_var.set("")
        self.title_entry.focus_set()
        self.status_var.set(f"Added task: '{title}' (Deadline: {deadline})")

    def _toggle_task_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a Row", "Please select a task in the table first.")
            return
        item_id = selected[0]
        vals = list(self.tree.item(item_id, "values"))
        new_status = "Completed" if vals[3] != "Completed" else "Pending"
        vals[3] = new_status

        try:
            if item_id.isdigit():
                cursor = self.conn.cursor()
                cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, int(item_id)))
                self.conn.commit()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Failed to update task status:\n{exc}")
            return

        tag = self._get_row_tag(new_status, vals[4])
        self.tree.item(item_id, values=vals, tags=(tag,) if tag else ())
        self._refresh_treeview()
        self.status_var.set(f"Marked '{vals[0]}' as {new_status}.")

    def _edit_selected_task(self):
        """Opens a modal dialog to edit the selected task's title, category, priority, status, and deadline."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a Row", "Please select a task to edit.")
            return

        item_id = selected[0]
        vals = list(self.tree.item(item_id, "values"))
        curr_title, curr_cat, curr_prio, curr_status, curr_deadline, curr_created = vals

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Study Task")
        edit_win.geometry("430x290")
        edit_win.resizable(False, False)
        edit_win.transient(self)
        edit_win.grab_set()

        theme = self.THEMES.get(self.theme_var.get(), self.THEMES["Light"])
        edit_win.configure(bg=theme["bg"])

        body = ttk.Frame(edit_win, padding=16)
        body.pack(fill=tk.BOTH, expand=True)

        edit_title_var = tk.StringVar(value=curr_title)
        edit_cat_var = tk.StringVar(value=curr_cat if curr_cat in self.CATEGORIES else self.CATEGORIES[0])
        edit_prio_var = tk.StringVar(value=curr_prio if curr_prio in self.PRIORITIES else self.PRIORITIES[1])
        edit_status_var = tk.StringVar(value=curr_status if curr_status in self.STATUSES else self.STATUSES[0])
        edit_deadline_var = tk.StringVar(value=curr_deadline)

        ttk.Label(body, text="Task Title:").grid(row=0, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))
        title_box = ttk.Entry(body, textvariable=edit_title_var, width=32)
        title_box.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=(0, 8))
        title_box.focus_set()

        ttk.Label(body, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))
        ttk.Combobox(body, textvariable=edit_cat_var, values=self.CATEGORIES, state="readonly", width=20).grid(
            row=1, column=1, columnspan=2, sticky=tk.W, pady=(0, 8)
        )

        ttk.Label(body, text="Priority:").grid(row=2, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))
        ttk.Combobox(body, textvariable=edit_prio_var, values=self.PRIORITIES, state="readonly", width=20).grid(
            row=2, column=1, columnspan=2, sticky=tk.W, pady=(0, 8)
        )

        ttk.Label(body, text="Status:").grid(row=3, column=0, sticky=tk.W, pady=(0, 8), padx=(0, 10))
        ttk.Combobox(body, textvariable=edit_status_var, values=self.STATUSES, state="readonly", width=20).grid(
            row=3, column=1, columnspan=2, sticky=tk.W, pady=(0, 8)
        )

        ttk.Label(body, text="Deadline (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, pady=(0, 12), padx=(0, 10))
        ttk.Entry(body, textvariable=edit_deadline_var, width=16).grid(row=4, column=1, sticky=tk.W, pady=(0, 12))
        ttk.Button(
            body,
            text="Pick Date",
            command=lambda: self._open_date_picker(edit_deadline_var, edit_win),
        ).grid(row=4, column=2, sticky=tk.W, padx=(6, 0), pady=(0, 12))

        body.grid_columnconfigure(1, weight=1)

        def save_edits():
            new_title = edit_title_var.get().strip()
            new_cat = edit_cat_var.get()
            new_prio = edit_prio_var.get()
            new_status = edit_status_var.get()
            new_deadline = edit_deadline_var.get().strip()

            if not self._validate_task_inputs(new_title, new_cat, new_prio, new_status, new_deadline, parent=edit_win):
                return

            try:
                if item_id.isdigit():
                    cursor = self.conn.cursor()
                    cursor.execute(
                        """
                        UPDATE tasks
                        SET title = ?, category = ?, priority = ?, status = ?, deadline = ?
                        WHERE id = ?
                        """,
                        (new_title, new_cat, new_prio, new_status, new_deadline, int(item_id)),
                    )
                    self.conn.commit()
                    self._notified_task_ids.discard(int(item_id))
            except sqlite3.Error as exc:
                messagebox.showerror("Database Error", f"Failed to update task:\n{exc}", parent=edit_win)
                return

            tag = self._get_row_tag(new_status, new_deadline)
            self.tree.item(
                item_id,
                values=(new_title, new_cat, new_prio, new_status, new_deadline, curr_created),
                tags=(tag,) if tag else (),
            )
            self._refresh_treeview()
            self.status_var.set(f"Updated task: '{new_title}'")
            edit_win.destroy()

        btn_bar = ttk.Frame(body)
        btn_bar.grid(row=5, column=0, columnspan=3, sticky=tk.E, pady=(6, 0))
        ttk.Button(btn_bar, text="Save Changes", command=save_edits).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_bar, text="Cancel", command=edit_win.destroy).pack(side=tk.LEFT)

        edit_win.bind("<Return>", lambda event: save_edits())
        edit_win.bind("<Escape>", lambda event: edit_win.destroy())

    def _delete_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a Row", "Please select a task to delete.")
            return
        item_id = selected[0]
        title = self.tree.item(item_id, "values")[0]

        try:
            if item_id.isdigit():
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM tasks WHERE id = ?", (int(item_id),))
                self.conn.commit()
                self._notified_task_ids.discard(int(item_id))
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Failed to delete task:\n{exc}")
            return

        self.tree.delete(item_id)
        self.status_var.set(f"Deleted task: '{title}'")

    def _clear_all_tasks(self):
        children = self.tree.get_children()
        if not children:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            if cursor.fetchone()[0] == 0:
                return
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to remove all tasks?"):
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM tasks")
                self.conn.commit()
                self._notified_task_ids.clear()
            except sqlite3.Error as exc:
                messagebox.showerror("Database Error", f"Failed to clear tasks:\n{exc}")
                return

            for item_id in self.tree.get_children():
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
            vals = self.tree.item(item_id, "values")
            if len(vals) == 6:
                title, cat, prio, status, deadline, created = vals
            else:
                title, cat, prio, status, created = vals
                deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            records.append(
                {
                    "title": title,
                    "category": cat,
                    "priority": prio,
                    "status": status,
                    "deadline": deadline,
                    "created_at": created,
                }
            )
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2)
            self.status_var.set(f"Exported {len(records)} tasks to {filepath}")
        except OSError as exc:
            messagebox.showerror("Export Error", f"Failed to write JSON file:\n{exc}")

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

            default_deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor = self.conn.cursor()

            count = 0
            for item in records:
                if not isinstance(item, dict):
                    continue
                title = str(item.get("title", "Untitled Task")).strip() or "Untitled Task"
                cat = item.get("category", "Widgets")
                if cat not in self.CATEGORIES:
                    cat = "Widgets"
                prio = item.get("priority", "Medium")
                if prio not in self.PRIORITIES:
                    prio = "Medium"
                status = item.get("status", "Pending")
                if status not in self.STATUSES:
                    status = "Pending"
                raw_deadline = str(item.get("deadline", default_deadline)).strip()
                deadline = raw_deadline if self._parse_deadline_date(raw_deadline) else default_deadline
                created = str(item.get("created_at", now_str))

                cursor.execute(
                    """
                    INSERT INTO tasks (title, category, priority, status, deadline, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (title, cat, prio, status, deadline, created),
                )
                count += 1

            self.conn.commit()
            self._refresh_treeview()
            self.status_var.set(f"Imported {count} tasks from {filepath}")
        except Exception as exc:
            messagebox.showerror("Import Error", f"Failed to load JSON file:\n{exc}")

    # =========================================================================
    # Theme & Appearance Customization
    # =========================================================================
    def _apply_theme(self, theme_name):
        """Applies the selected color palette across all ttk widgets and Treeview tags."""
        palette = self.THEMES.get(theme_name, self.THEMES["Light"])
        self.configure(bg=palette["bg"])

        self.style.configure(".", background=palette["bg"], foreground=palette["fg"], font=("Helvetica", 10))
        self.style.configure("TFrame", background=palette["bg"])
        self.style.configure("TLabelframe", background=palette["bg"], bordercolor=palette["border"])
        self.style.configure(
            "TLabelframe.Label",
            background=palette["bg"],
            foreground=palette["header_fg"],
            font=("Helvetica", 10, "bold"),
        )
        self.style.configure("TLabel", background=palette["bg"], foreground=palette["fg"])
        self.style.configure(
            "Header.TLabel",
            background=palette["bg"],
            foreground=palette["header_fg"],
            font=("Helvetica", 14, "bold"),
        )
        self.style.configure(
            "Subheader.TLabel",
            background=palette["bg"],
            foreground=palette["sub_fg"],
            font=("Helvetica", 10),
        )

        self.style.configure(
            "TButton",
            background=palette["btn_bg"],
            foreground=palette["btn_fg"],
            bordercolor=palette["border"],
            padding=(8, 4),
        )
        self.style.map(
            "TButton",
            background=[("active", palette["btn_active"]), ("pressed", palette["btn_active"])],
            foreground=[("active", palette["btn_fg"])],
        )

        self.style.configure(
            "TEntry",
            fieldbackground=palette["entry_bg"],
            foreground=palette["entry_fg"],
            insertcolor=palette["entry_fg"],
            bordercolor=palette["border"],
        )

        self.style.configure(
            "TCombobox",
            fieldbackground=palette["entry_bg"],
            background=palette["btn_bg"],
            foreground=palette["entry_fg"],
            arrowcolor=palette["fg"],
            bordercolor=palette["border"],
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", palette["entry_bg"])],
            foreground=[("readonly", palette["entry_fg"])],
            selectbackground=[("readonly", palette["entry_bg"])],
            selectforeground=[("readonly", palette["entry_fg"])],
        )

        self.style.configure(
            "Treeview",
            background=palette["tree_bg"],
            fieldbackground=palette["tree_bg"],
            foreground=palette["tree_fg"],
            rowheight=26,
            bordercolor=palette["border"],
        )
        self.style.configure(
            "Treeview.Heading",
            background=palette["tree_heading_bg"],
            foreground=palette["tree_heading_fg"],
            font=("Helvetica", 10, "bold"),
            relief=tk.FLAT,
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", palette["btn_active"])],
        )
        self.style.map(
            "Treeview",
            background=[("selected", palette["tree_selected_bg"])],
            foreground=[("selected", palette["tree_selected_fg"])],
        )

        self.style.configure(
            "Vertical.TScrollbar",
            background=palette["btn_bg"],
            troughcolor=palette["bg"],
            arrowcolor=palette["fg"],
        )

        # Configure Combobox dropdown listbox colors for readability
        self.option_add("*TCombobox*Listbox.background", palette["entry_bg"])
        self.option_add("*TCombobox*Listbox.foreground", palette["entry_fg"])
        self.option_add("*TCombobox*Listbox.selectBackground", palette["tree_selected_bg"])
        self.option_add("*TCombobox*Listbox.selectForeground", palette["tree_selected_fg"])

        if hasattr(self, "tree"):
            self.tree.tag_configure(
                "overdue",
                background=palette["overdue_bg"],
                foreground=palette["overdue_fg"],
            )
            self.tree.tag_configure(
                "approaching",
                background=palette["approaching_bg"],
                foreground=palette["approaching_fg"],
            )
            self.tree.tag_configure(
                "completed",
                background=palette["completed_bg"],
                foreground=palette["completed_fg"],
            )
        self.status_var.set(f"Applied '{theme_name}' theme.")

    def _on_close(self):
        """Cancels scheduled .after() callbacks and closes the SQLite connection cleanly."""
        if self._reminder_after_id is not None:
            try:
                self.after_cancel(self._reminder_after_id)
            except ValueError:
                pass
            self._reminder_after_id = None
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
            self.conn = None
        self.destroy()


if __name__ == "__main__":
    app = TaskTrackerApp()
    app.mainloop()