# 📚 Study Task Tracker – Tkinter Mini Project

A standalone desktop GUI application developed using Python's standard **Tkinter** and **ttk (Themed Tkinter)** libraries. This project demonstrates practical concepts of Python GUI development, including responsive layout management, two-way data binding, interactive tabular data display, keyboard shortcuts, CRUD operations, and JSON file handling.

## 🎯 Aim & Learning Objectives

**Aim :** To develop a desktop GUI application using Python Tkinter that demonstrates the implementation of various GUI programming concepts and task management operations.

The main learning objectives of this project are :-

- **Responsive Layout Management:** Implement responsive GUI layouts by combining `grid()` and `pack()` geometry managers with column weight configuration using `grid_columnconfigure()` inside `ttk.Frame` and `ttk.LabelFrame` containers.

- **Two-Way Data Binding:** Use `tk.StringVar()` to establish data binding between form input fields and application variables, allowing dynamic updates to the user interface, including status bar messages.

- **Scrollable Tabular Display:** Display multiple task records in a structured table using `ttk.Treeview` and integrate a vertical `ttk.Scrollbar` for smooth navigation through task records.

- **CRUD Operations:** Implement complete Create, Read, Update, and Delete (CRUD) functionality to add new tasks, display existing tasks, update task completion status, and delete individual or all task records.

- **Input Validation and Modal Alerts:** Validate user inputs to prevent empty task submissions and use `tkinter.messagebox` to display warning, information, and confirmation messages.

- **Structured JSON File Handling:** Implement JSON file import and export functionality using Python's `json` module and native file selection dialogs provided by `tkinter.filedialog`.

## ✨ Features

- **Add Tasks:** Create new study tasks with a title, category, and priority.
- **View Tasks:** Display all tasks in a structured table using `ttk.Treeview`.
- **Update Status:** Mark tasks as Completed or Pending.
- **Delete Tasks:** Delete selected tasks from the task list.
- **Clear All Tasks:** Remove all tasks with a confirmation message.
- **Import JSON:** Load previously saved tasks from a JSON file.
- **Export JSON:** Save task records into a JSON file.
- **Input Validation:** Prevent adding tasks without a title.
- **Scrollable Table:** Navigate through tasks using a scrollbar.
- **Keyboard Shortcuts:** Perform common operations using keyboard shortcuts.
- **Status Bar:** Display messages about application activities.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **GUI Framework:** Tkinter
- **UI Components:** ttk (Themed Tkinter)
- **Data Storage:** JSON
- **Python Modules:** json, tkinter, datetime

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Enter | Add a new task |
| Delete | Delete the selected task |
| Ctrl + Q | Exit the application |
| Double Click | Toggle task completion status |


## Installation and Setup

### Option 1 : Run the Windows Executable (No Python Required)

1. Open the repository's **Releases** section (`v1.0.0`) on GitHub.
2. Download **`tkinter_learning_suite.exe`** from the **Assets** list.
3. Double-click `tkinter_learning_suite.exe` to launch the Study Task Tracker on Windows.

### Option 2 : Run from Python Source

1. Clone this repository and navigate into the project folder:

   ```bash
   git clone https://github.com/Vaghnai123/Tinker_TaskManager.git
   
   cd Tinker_TaskManager
   ```
3. Run the application (no third-party `pip` packages are required to run the script):
   
   ```bash
   python tkinter_TaskManager.py
   ```

## Building a Standalone Executable

To package `tkinter_TaskManager.py` into a single-file executable :-

```bash
pip install pyinstaller

pyinstaller --onefile --windowed tkinter_TaskManager.py
```

## 🔮 Future Improvements

- Add task search and filtering functionality.
- Add task deadlines and reminders.
- Store tasks in an SQLite database.
- Add task editing functionality.
- Improve the interface with additional themes and customization.







