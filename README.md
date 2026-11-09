# 📚 Study Task Tracker – Tkinter Mini Project

A standalone desktop GUI application developed using Python's standard **Tkinter** and **ttk (Themed Tkinter)** libraries. This project demonstrates practical concepts of Python GUI development, including responsive layout management, two-way data binding, interactive tabular data display, keyboard shortcuts, CRUD operations, task search and filtering, deadline reminders, SQLite database integration, and JSON file handling.

## 🎯 Aim & Learning Objectives

**Aim :** To develop a desktop GUI application using Python Tkinter that demonstrates various GUI programming concepts and provides an efficient task management system with database integration.

The main learning objectives of this project are :-

- **Responsive Layout Management:** Implement responsive GUI layouts using `grid()` and `pack()` geometry managers with column weight configuration inside Tkinter containers.

- **Two-Way Data Binding:** Use `tk.StringVar()` to establish data binding between form input fields and application variables, allowing dynamic updates to the user interface.

- **Scrollable Tabular Display:** Display multiple task records in a structured table using `ttk.Treeview` and integrate scrollbars for smooth navigation.

- **CRUD Operations:** Implement Create, Read, Update, and Delete operations to add, display, edit, update, and delete task records.

- **Task Search and Filtering:** Implement task searching and filtering functionality based on task title, category, priority, and status.

- **Deadline and Reminder Management:** Allow users to assign deadlines to tasks and receive reminders about approaching or overdue deadlines.

- **SQLite Database Integration:** Use Python's built-in `sqlite3` module to store task records permanently and retrieve them when the application starts.

- **Input Validation and Modal Alerts:** Validate user inputs and use `tkinter.messagebox` to display warning, information, and confirmation messages.

- **JSON File Handling:** Implement JSON import and export functionality using Python's `json` module and native file selection dialogs.

- **Theme Customization:** Provide multiple interface themes, including Light and Dark modes, to improve the application's appearance and usability.

## ✨ Features

### 📋 Task Management
- **Add Tasks:** Create new study tasks with a title, category, priority, and deadline.
- **View Tasks:** Display all tasks in a structured table using `ttk.Treeview`.
- **Edit Tasks:** Modify existing task details, including title, category, priority, status, and deadline.
- **Update Status:** Change task status between Pending, In Progress, and Completed.
- **Delete Tasks:** Delete selected tasks from the task list.
- **Clear All Tasks:** Remove all tasks with a confirmation message.

### 🔍 Search and Filtering
- **Task Search:** Search for tasks using their titles.
- **Category Filter:** Filter tasks according to their categories.
- **Priority Filter:** Filter tasks based on Low, Medium, and High priority.
- **Status Filter:** Display All, Pending, In Progress, or Completed tasks.
- **Dynamic Filtering:** Automatically update the task table when search or filter options change.

### ⏰ Deadline and Reminders
- **Set Deadlines:** Assign deadlines to individual tasks.
- **Deadline Display:** View task deadlines in the task table.
- **Deadline Reminders:** Receive reminders when task deadlines are approaching.
- **Overdue Notifications:** Identify tasks whose deadlines have passed.
- **Automatic Checking:** Use Tkinter's `after()` method to periodically check task deadlines.

### 💾 Data Storage and File Management
- **SQLite Database:** Store task records permanently using Python's built-in `sqlite3` module.
- **Automatic Database Creation:** Create the database and required table automatically if they do not exist.
- **Data Persistence:** Load previously saved tasks automatically when the application starts.
- **JSON Import:** Import previously saved task records from JSON files.
- **JSON Export:** Export task records into JSON files.
- **Backward Compatibility:** Support existing JSON task records while handling the additional task fields.

### 🎨 Interface Customization
- **Light Theme:** Use a clean and bright interface.
- **Dark Theme:** Switch to a dark interface for comfortable viewing.
- **Additional Themes:** Provide additional interface styling options.
- **Theme Switching:** Change the application appearance through the theme selection option.

### ⚙️ Additional Features
- **Input Validation:** Prevent adding tasks without a valid task title.
- **Confirmation Dialogs:** Display confirmation messages before deleting tasks or clearing all records.
- **Scrollable Table:** Navigate through task records using scrollbars.
- **Keyboard Shortcuts:** Perform common operations using keyboard shortcuts.
- **Status Bar:** Display messages about application activities.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Tkinter | Desktop GUI development |
| ttk | Themed GUI components |
| SQLite3 | Permanent task data storage |
| JSON | Task import and export |
| datetime | Date and time management |
| tkinter.filedialog | File selection dialogs |
| tkinter.messagebox | Alerts and confirmation dialogs |

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Enter | Add a new task |
| Delete | Delete the selected task |
| Ctrl + Q | Exit the application |
| Double Click | Toggle task completion status |

## 📂 Project Structure

```text
Study-Task-Tracker/
│
├── tkinter_TaskManager.py
├── README.md
├── tasks.db
│
└── exports/
    └── tasks.json
```

*Note: The SQLite database and export folder are created or used by the application as required.*

## 🚀 Installation and Setup

### Option 1: Run the Windows Executable (No Python Required)

1. Open the repository's **Releases** section (`v1.0.0`) on GitHub.
2. Download `tkinter_learning_suite.exe` from the Assets list.
3. Double-click the executable to launch the Study Task Tracker on Windows.

### Option 2: Run from Python Source

1. Clone this repository and navigate into the project folder:

   ```bash
   git clone https://github.com/Vaghnai123/Tinker_TaskManager.git

   cd Tinker_TaskManager
   ```

2. Run the application:

   ```bash
   python tkinter_TaskManager.py
   ```

**Note:** No third-party Python packages are required if the application uses only the standard Python libraries. Make sure Python and Tkinter are installed on your system.

## 📦 Building a Standalone Executable

To package the Python application into a single-file Windows executable, install PyInstaller:

```bash
pip install pyinstaller
```

Run the following command:

```bash
pyinstaller --onefile --windowed tkinter_TaskManager.py
```

The generated executable will be available inside the `dist` directory.

## 👨‍💻 Author

**Vaghani123**

GitHub Repository: https://github.com/Vaghani2004/Tinker_TaskManager

---

⭐ If you find this project useful, consider giving it a star on GitHub!
