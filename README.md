# Study Task Tracker — Tkinter CRUD Application

A standalone desktop GUI application built with Python's standard [tkinter](https://docs.python.org/3/library/tkinter.html) and [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html) libraries. Designed as a practical mini-project to demonstrate modern desktop GUI layout management, two-way variable binding, interactive tabular views, keyboard shortcuts, and JSON file persistence.

## Aim & Learning Objectives

Develop a desktop GUI application in Python using [Tkinter](https://docs.python.org/3/library/tk.html) that demonstrates:

* **Responsive Layout Management:** Combining `grid()` and `pack()` geometry managers with column weight configuration (`grid_columnconfigure`) inside [ttk.Frame and ttk.LabelFrame](https://docs.python.org/3/library/tkinter.ttk.html) containers.
* **Two-Way Data Binding:** Synchronizing form inputs and dynamic status bar messages using `tk.StringVar()` variable classes from [tkinter](https://docs.python.org/3/library/tkinter.html).
* **Scrollable Tabular Display:** Rendering multi-column task records with `ttk.Treeview` paired with a vertical `ttk.Scrollbar` from [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html).
* **Full CRUD Workflow:** Supporting task creation (**Create**), tabular inspection (**Read**), completion status toggling (**Update**), and single or bulk row removal (**Delete**).
* **Validation & Modal Alerts:** Guarding against empty submissions and accidental data loss using `tkinter.messagebox` prompts from [Tkinter Dialogs](https://docs.python.org/3/library/dialog.html).
* **Structured JSON Persistence:** Exporting and importing task lists using native OS file pickers via `tkinter.filedialog` from [Tkinter Dialogs](https://docs.python.org/3/library/dialog.html).

🛠️ Technologies Used

Programming Language: Python

GUI Framework: Tkinter

UI Components: ttk (Themed Tkinter)

Data Storage: JSON

Date and Time: datetime

Python Modules: json, tkinter, datetime

## Key Features & Controls

| Feature / Control | Implementation Component | Description |
| :--- | :--- | :--- |
| **Add Study Task** | `ttk.Entry`, `ttk.Combobox`, `ttk.Button` | Captures task title, topic category (`Widgets`, `Layouts`, `Events`, `Canvas`, `Dialogs`), and priority (`Low`, `Medium`, `High`) using [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html) widgets |
| **Interactive Task Table** | `ttk.Treeview` & `ttk.Scrollbar` | Displays `Task Title`, `Category`, `Priority`, `Status`, and `Created At` timestamps with vertical scrolling via [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html) |
| **Toggle Completion** | `<Double-1>` event & `Toggle Completed` button | Switches the selected task row between `Pending` and `Completed` states using [tkinter](https://docs.python.org/3/library/tkinter.html) event bindings |
| **Delete & Clear Tasks** | `<Delete>` key, `Delete Selected`, `Clear All` | Removes a single highlighted row or clears the entire table after a confirmation dialog via [Tkinter Dialogs](https://docs.python.org/3/library/dialog.html) |
| **JSON Import / Export** | `filedialog.asksaveasfilename` & `askopenfilename` | Saves current tasks to a formatted `.json` file or loads external `.json` task lists using [Tkinter Dialogs](https://docs.python.org/3/library/dialog.html) |

## Keyboard Shortcuts

| Shortcut Key | Action |
| :--- | :--- |
| `Enter` (`<Return>`) | Add the current task from the input form |
| `Double-Click` (`<Double-1>`) | Toggle the selected task status between `Pending` and `Completed` |
| `Delete` (`<Delete>`) | Delete the currently selected task row |
| `Ctrl + Q` (`<Control-q>`) | Exit the application |

## Getting Started

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
3. Run the application with Python 3 (no third-party `pip` packages are required to run the script):
   
   ```bash
   python tkinter_TaskManager.py
   ```

## Building a Standalone Executable

To package `tkinter_TaskManager.py` into a single-file executable using [PyInstaller](https://pyinstaller.org/en/stable/usage.html):

```bash
pip install pyinstaller

pyinstaller --onefile --windowed tkinter_TaskManager.py
```


