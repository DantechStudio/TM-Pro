import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from models.data_model import TaskModel

class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.db = TaskModel()
        self.dark_mode = True
        self.custom_categories = self.db.get_custom_categories()

        self.default_categories = ["Work", "Personal", "Shopping", "Education", "Health", "General"]

        self.parent.attributes('-fullscreen', True)

        self.setup_ui()
        self.load_tasks()

    def get_categories(self):
        return self.default_categories + self.custom_categories

    def setup_ui(self):
        if self.dark_mode:
            bg = '#1e1e1e'
            fg = '#ffffff'
            entry_bg = '#2d2d2d'
            btn_bg = '#0d6efd'
            listbox_bg = '#2d2d2d'
        else:
            bg = '#f0f0f0'
            fg = '#000000'
            entry_bg = '#ffffff'
            btn_bg = '#007bff'
            listbox_bg = '#ffffff'

        self.parent.configure(bg=bg)

        for widget in self.parent.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.parent, bg=bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        top_frame = tk.Frame(main_frame, bg=bg)
        top_frame.pack(fill=tk.X, pady=(0, 20))

        title_frame = tk.Frame(top_frame, bg=bg)
        title_frame.pack(side=tk.LEFT)

        title = tk.Label(
            title_frame,
            text="TM-Pro",
            font=('Arial', 30, 'bold'),
            bg=bg,
            fg=fg
        )
        title.pack(anchor='w')

        credit = tk.Label(
            title_frame,
            text="Developed By DantechStudio",
            font=('Arial', 10),
            bg=bg,
            fg=fg
        )
        credit.pack(anchor='w')

        exit_btn = tk.Button(top_frame, text="✖ Exit", command=self.exit_app, bg='#dc3545', fg='white', padx=15, pady=5)
        exit_btn.pack(side=tk.RIGHT, padx=5)

        fullscreen_btn = tk.Button(top_frame, text="🗖 Fullscreen Mode", command=self.toggle_fullscreen, bg='#6c757d', fg='white', padx=15, pady=5)
        fullscreen_btn.pack(side=tk.RIGHT, padx=5)

        if self.dark_mode:
            dark_text = "Light Mode"
        else:
            dark_text = "Dark Mode"
        dark_btn = tk.Button(top_frame, text=dark_text, command=self.toggle_dark_mode, bg='#ffc107', fg='black', padx=15, pady=5)
        dark_btn.pack(side=tk.RIGHT, padx=5)

        form_frame = tk.LabelFrame(main_frame, text="Add New Task", bg=bg, fg=fg, font=('Arial', 11, 'bold'))
        form_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(form_frame, text="Title:", bg=bg, fg=fg).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.title_entry = tk.Entry(form_frame, width=40, bg=entry_bg, fg=fg)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Description:", bg=bg, fg=fg).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.desc_text = tk.Text(form_frame, height=3, width=40, bg=entry_bg, fg=fg)
        self.desc_text.grid(row=1, column=1, padx=10, pady=5)

        cat_frame = tk.Frame(form_frame, bg=bg)
        cat_frame.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Category:", bg=bg, fg=fg).grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.category_var = tk.StringVar()
        categories = self.get_categories()
        self.category_menu = ttk.Combobox(cat_frame, textvariable=self.category_var, values=categories, width=30)
        self.category_menu.pack(side=tk.LEFT)
        if categories:
            self.category_var.set("Work")

        add_cat_btn = tk.Button(cat_frame, text="New Category", command=self.add_new_category, bg='#28a745', fg='white', padx=10)
        add_cat_btn.pack(side=tk.LEFT, padx=5)

        tk.Label(form_frame, text="Priority:", bg=bg, fg=fg).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.priority_var = tk.StringVar()
        priority_frame = tk.Frame(form_frame, bg=bg)
        priority_frame.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.priority_var.set("Medium")
        priorities = [("🔴 High", "High"), ("🟡 Medium", "Medium"), ("🟢 Low", "Low")]

        for text, value in priorities:
            tk.Radiobutton(priority_frame, text=text, variable=self.priority_var, value=value, bg=bg, fg=fg, selectcolor=bg).pack(side=tk.LEFT, padx=5)

        tk.Label(form_frame, text="Due Date:", bg=bg, fg=fg).grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.date_entry = tk.Entry(form_frame, width=40, bg=entry_bg, fg=fg)
        self.date_entry.grid(row=4, column=1, padx=10, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        add_btn = tk.Button(form_frame, text="Add Task", command=self.add_task, bg=btn_bg, fg='white', padx=20, pady=5)
        add_btn.grid(row=5, column=0, columnspan=2, pady=15)

        filter_frame = tk.LabelFrame(main_frame, text="Filter", bg=bg, fg=fg)
        filter_frame.pack(fill=tk.X, pady=(0, 15))

        filter_inner = tk.Frame(filter_frame, bg=bg)
        filter_inner.pack(pady=10)

        btn_left = tk.Frame(filter_inner, bg=bg)
        btn_left.pack(side=tk.LEFT)

        complete_btn = tk.Button(btn_left, text="✅ Complete", command=self.complete_task, bg='#28a745', fg='white', padx=15, pady=5)
        complete_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(btn_left, text="🗑 Delete", command=self.delete_task, bg='#dc3545', fg='white', padx=15, pady=5)
        delete_btn.pack(side=tk.LEFT, padx=5)

        delete_all_btn = tk.Button(btn_left, text="🗑 Delete All", command=self.delete_all_tasks, bg='#dc3545', fg='white', padx=15, pady=5)
        delete_all_btn.pack(side=tk.LEFT, padx=5)

        tk.Frame(filter_inner, width=50, bg=bg).pack(side=tk.LEFT)

        btn_right = tk.Frame(filter_inner, bg=bg)
        btn_right.pack(side=tk.LEFT)

        tk.Label(btn_right, text="Category:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=5)

        filter_cats = ["All"] + self.get_categories()
        self.filter_category = ttk.Combobox(btn_right, values=filter_cats, width=15)
        self.filter_category.set("All")
        self.filter_category.pack(side=tk.LEFT, padx=5)

        tk.Label(btn_right, text="Priority:", bg=bg, fg=fg).pack(side=tk.LEFT, padx=5)

        filter_prios = ["All", "High", "Medium", "Low"]
        self.filter_priority = ttk.Combobox(btn_right, values=filter_prios, width=12)
        self.filter_priority.set("All")
        self.filter_priority.pack(side=tk.LEFT, padx=5)

        filter_btn = tk.Button(btn_right, text="Apply", command=self.load_tasks, bg='#17a2b8', fg='white')
        filter_btn.pack(side=tk.LEFT, padx=10)

        list_frame = tk.Frame(main_frame, bg=bg)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Arial', 10), height=15, bg=listbox_bg, fg=fg, selectbackground='#0d6efd')
        self.tasks_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)

    def exit_app(self):
        self.parent.quit()
        self.parent.destroy()

    def toggle_fullscreen(self):
        self.parent.attributes('-fullscreen', not self.parent.attributes('-fullscreen'))

    def add_new_category(self):
        new_category = simpledialog.askstring("New Category", "New category name:")
        if new_category:
            new_category = new_category.strip()
            if new_category not in self.get_categories():
                self.custom_categories.append(new_category)
                self.db.save_custom_categories(self.custom_categories)
                self.setup_ui()
                self.load_tasks()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.setup_ui()
        self.load_tasks()

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        due_date = self.date_entry.get()

        if not title:
            messagebox.showwarning("Error", "Enter title!")
            return

        self.db.add_task(title, description, category, priority, due_date)
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.load_tasks()

    def complete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task!")
            return
        task_info = self.tasks_listbox.get(selected[0])
        task_id = int(task_info.split("|")[0])
        self.db.complete_task(task_id)
        self.load_tasks()

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task!")
            return
        if messagebox.askyesno("Confirm", "Are you sure?"):
            task_info = self.tasks_listbox.get(selected[0])
            task_id = int(task_info.split("|")[0])
            self.db.delete_task(task_id)
            self.load_tasks()

    def delete_all_tasks(self):
        if messagebox.askyesno("Confirm", "Delete all tasks?"):
            self.db.delete_all_tasks()
            self.load_tasks()

    def load_tasks(self):
        self.tasks_listbox.delete(0, tk.END)

        category = self.filter_category.get()
        priority = self.filter_priority.get()

        if category == "All":
            category = None
        if priority == "All":
            priority = None

        tasks = self.db.get_all_tasks(category, priority)

        priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

        for task in tasks:
            priority_icon = priority_icons.get(task[4], "⚪")
            status_icon = "✅" if task[6] == "completed" else "⏳"

            cat_display = task[3]
            pri_display = task[4]

            display = f"{task[0]} | {priority_icon} {task[1]} | {cat_display} | {pri_display} | {task[5]} | {status_icon}"
            self.tasks_listbox.insert(tk.END, display)
