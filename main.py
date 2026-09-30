import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dotenv import load_dotenv, set_key

import db
import db_logger


# Ensure environment variables are loaded
load_dotenv()

class CITFacultyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CIT Faculty Management System - DBMS Mini-Project (Two-Table GUI)")
        self.geometry("1180x740")
        self.minsize(980, 640)

        # Active Table State: "faculty" or "faculty_academic"
        self.active_table = "faculty"
        
        # Live SQL Toggle State
        self.live_sql_enabled = False
        self.sql_history = []


        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Build Main UI Layout
        self.create_header()
        self.create_dashboard_summary()
        self.create_table_selector_bar()
        self.create_search_bar()
        self.create_directory_tree()
        self.create_action_buttons()
        self.create_sql_panel()
        self.create_statusbar()

        # Subscribe to SQL Logs
        db_logger.subscribe_to_sql(self.on_sql_activity)

        # Check DB Connection & Initialize Data

        self.after(200, self.check_and_init_db)

    def configure_styles(self):
        """Sets up custom TTK widget styling."""
        self.BG_DARK = "#003366"     # CIT Navy Blue
        self.BG_ACCENT = "#D4AF37"   # Academic Gold
        self.BG_LIGHT = "#F4F6F9"    # Off-white background
        self.CARD_BG = "#FFFFFF"

        self.configure(bg=self.BG_LIGHT)

        # Treeview styling
        self.style.configure("Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1F2937"
        )
        self.style.configure("Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#003366",
            foreground="#FFFFFF",
            padding=5
        )
        self.style.map("Treeview",
            background=[("selected", "#0284C7")],
            foreground=[("selected", "#FFFFFF")]
        )

        # Button Styles
        self.style.configure("Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#003366",
            foreground="#FFFFFF",
            padding=(10, 6)
        )
        self.style.map("Primary.TButton",
            background=[("active", "#002244")]
        )

        self.style.configure("Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#0D9488",
            foreground="#FFFFFF",
            padding=(10, 6)
        )
        self.style.map("Accent.TButton",
            background=[("active", "#0F766E")]
        )

        self.style.configure("Danger.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#DC2626",
            foreground="#FFFFFF",
            padding=(10, 6)
        )
        self.style.map("Danger.TButton",
            background=[("active", "#B91C1C")]
        )

        self.style.configure("Secondary.TButton",
            font=("Segoe UI", 10),
            background="#4B5563",
            foreground="#FFFFFF",
            padding=(8, 5)
        )
        self.style.map("Secondary.TButton",
            background=[("active", "#374151")]
        )

    def create_header(self):
        """Top Header Banner with CIT Academic Branding."""
        header_frame = tk.Frame(self, bg="#003366", height=75)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="COIMBATORE INSTITUTE OF TECHNOLOGY",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#003366"
        )
        title_label.pack(anchor=tk.W, padx=20, pady=(8, 0))

        subtitle_label = tk.Label(
            header_frame,
            text="FACULTY MANAGEMENT SYSTEM — TWO-TABLE RELATIONAL DATABASE GUI",
            font=("Segoe UI", 10, "bold"),
            fg="#D4AF37",
            bg="#003366"
        )
        subtitle_label.pack(anchor=tk.W, padx=20, pady=(0, 8))

    def create_dashboard_summary(self):
        """Top Metrics Cards Frame displaying counts from MySQL."""
        self.dashboard_frame = tk.Frame(self, bg="#F4F6F9", pady=8, padx=15)
        self.dashboard_frame.pack(fill=tk.X, side=tk.TOP)

        self.card_widgets = {}
        departments = [
            ("Total", "TOTAL FACULTY", "#1E3A8A"),
            ("CSE", "CSE", "#0284C7"),
            ("ECE", "ECE", "#0D9488"),
            ("EEE", "EEE", "#D97706"),
            ("MECH", "MECHANICAL", "#7C3AED"),
            ("CIVIL", "CIVIL", "#4B5563")
        ]

        for i, (key, label, color) in enumerate(departments):
            card = tk.Frame(self.dashboard_frame, bg="#FFFFFF", highlightbackground="#E5E7EB", highlightthickness=1, bd=0)
            card.grid(row=0, column=i, padx=5, sticky="ew")
            self.dashboard_frame.columnconfigure(i, weight=1)

            strip = tk.Frame(card, bg=color, height=4)
            strip.pack(fill=tk.X, side=tk.TOP)

            val_lbl = tk.Label(card, text="--", font=("Segoe UI", 16, "bold"), fg=color, bg="#FFFFFF")
            val_lbl.pack(pady=(4, 0))

            title_lbl = tk.Label(card, text=label, font=("Segoe UI", 8, "bold"), fg="#6B7280", bg="#FFFFFF")
            title_lbl.pack(pady=(0, 4))

            self.card_widgets[key] = val_lbl

    def create_table_selector_bar(self):
        """Prominent Two-Table Switcher Control Bar."""
        selector_frame = tk.Frame(self, bg="#E2E8F0", height=45, padx=15, pady=6)
        selector_frame.pack(fill=tk.X, side=tk.TOP, padx=15, pady=(2, 4))

        tk.Label(
            selector_frame,
            text="SELECT MYSQL DATABASE TABLE:",
            font=("Segoe UI", 10, "bold"),
            fg="#003366",
            bg="#E2E8F0"
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.table_selector_cb = ttk.Combobox(
            selector_frame,
            values=["Faculty", "Faculty Academic"],
            state="readonly",
            width=20,
            font=("Segoe UI", 10, "bold")
        )
        self.table_selector_cb.set("Faculty")
        self.table_selector_cb.pack(side=tk.LEFT, padx=(0, 20))
        self.table_selector_cb.bind("<<ComboboxSelected>>", self.on_table_switched)

        self.table_status_lbl = tk.Label(
            selector_frame,
            text="CURRENT TABLE VIEW: FACULTY (Table: faculty)",
            font=("Segoe UI", 10, "bold"),
            fg="#003366",
            bg="#E2E8F0"
        )
        self.table_status_lbl.pack(side=tk.LEFT)

    def create_search_bar(self):
        """Dynamic Search and Filter Controls Bar."""
        self.search_frame = tk.LabelFrame(
            self,
            text=" Search & Filter Controls ",
            font=("Segoe UI", 10, "bold"),
            fg="#003366",
            bg="#F4F6F9",
            padx=12,
            pady=6
        )
        self.search_frame.pack(fill=tk.X, padx=15, pady=(0, 6))

        # Search By Dropdown
        tk.Label(self.search_frame, text="Search Field:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.search_field_cb = ttk.Combobox(
            self.search_frame,
            values=["All Fields", "Faculty Name", "Department", "Designation", "Faculty ID"],
            state="readonly",
            width=18
        )
        self.search_field_cb.set("All Fields")
        self.search_field_cb.grid(row=0, column=1, padx=(0, 15), sticky=tk.W)

        # Keyword Entry
        tk.Label(self.search_frame, text="Keyword:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.search_entry = ttk.Entry(self.search_frame, width=22)
        self.search_entry.grid(row=0, column=3, padx=(0, 15), sticky=tk.W)
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        # Department Filter Combobox
        self.dept_label = tk.Label(self.search_frame, text="Department:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9")
        self.dept_label.grid(row=0, column=4, padx=(0, 5), sticky=tk.W)

        self.dept_filter_cb = ttk.Combobox(
            self.search_frame,
            values=[
                "All",
                "Computer Science and Engineering",
                "Electronics and Communication Engineering",
                "Electrical and Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering"
            ],
            state="readonly",
            width=26
        )
        self.dept_filter_cb.set("All")
        self.dept_filter_cb.grid(row=0, column=5, padx=(0, 15), sticky=tk.W)
        self.dept_filter_cb.bind("<<ComboboxSelected>>", lambda e: self.on_search())

        # Search and Reset Buttons
        btn_search = ttk.Button(self.search_frame, text="🔍 SEARCH", style="Primary.TButton", command=self.on_search)
        btn_search.grid(row=0, column=6, padx=(0, 5))

        btn_reset = ttk.Button(self.search_frame, text="🔄 RESET", style="Secondary.TButton", command=self.on_reset_search)
        btn_reset.grid(row=0, column=7)

    def create_directory_tree(self):
        """Directory Table using TTK Treeview with dynamic column re-configuration."""
        tree_container = tk.Frame(self, bg="#F4F6F9")
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 6))

        self.tree = ttk.Treeview(tree_container, show="headings", selectmode="browse")

        # Scrollbars
        vsb = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)

        # Double click to view full profile
        self.tree.bind("<Double-1>", lambda e: self.on_view_profile())

    def create_action_buttons(self):
        """Action Toolbar with Table-Specific CRUD and Relational JOIN Buttons."""
        action_frame = tk.Frame(self, bg="#F4F6F9")
        action_frame.pack(fill=tk.X, padx=15, pady=(0, 8))

        self.btn_add = ttk.Button(action_frame, text="➕ Add Faculty", style="Primary.TButton", command=self.on_add_record)
        self.btn_add.pack(side=tk.LEFT, padx=(0, 10))

        btn_view = ttk.Button(action_frame, text="👁️ View Full Profile (JOIN)", style="Accent.TButton", command=self.on_view_profile)
        btn_view.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_edit = ttk.Button(action_frame, text="✏️ Edit Record", style="Primary.TButton", command=self.on_edit_record)
        self.btn_edit.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_del = ttk.Button(action_frame, text="🗑️ Delete Record", style="Danger.TButton", command=self.on_delete_record)
        self.btn_del.pack(side=tk.LEFT, padx=(0, 10))

        btn_config = ttk.Button(action_frame, text="⚙️ DB Config", style="Secondary.TButton", command=self.on_open_db_config)
        btn_config.pack(side=tk.RIGHT)

        self.btn_live_sql = ttk.Button(action_frame, text="[ LIVE SQL: OFF ]", style="Secondary.TButton", command=self.toggle_live_sql)
        self.btn_live_sql.pack(side=tk.RIGHT, padx=(0, 10))

        self.btn_adv_query = ttk.Button(action_frame, text="🔍 ADVANCED QUERY", style="Accent.TButton", command=self.open_advanced_query)
        self.btn_adv_query.pack(side=tk.RIGHT, padx=(0, 10))
        # removing pack call below to prevent duplicate

        btn_refresh = ttk.Button(action_frame, text="🔄 Refresh List", style="Secondary.TButton", command=self.refresh_data)
        btn_refresh.pack(side=tk.RIGHT, padx=(0, 10))


    def create_statusbar(self):
        """Bottom Status bar showing DB state and active table status."""
        self.status_var = tk.StringVar(value="Initializing System...")
        status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg="#4B5563",
            bg="#E5E7EB",
            anchor=tk.W,
            padx=10,
            pady=3
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar_widget = status_bar

    def create_sql_panel(self):
        """Creates the Live SQL Activity Panel (initially hidden)."""
        self.sql_panel_frame = tk.Frame(self, bg="#1E1E1E")
        
        header = tk.Frame(self.sql_panel_frame, bg="#333333")
        header.pack(fill=tk.X)
        tk.Label(header, text="LIVE SQL ACTIVITY", font=("Consolas", 10, "bold"), fg="#4ADE80", bg="#333333").pack(side=tk.LEFT, padx=10, pady=5)
        
        btn_clear = ttk.Button(header, text="CLEAR LOG", style="Secondary.TButton", command=self.clear_sql_log)
        btn_clear.pack(side=tk.RIGHT, padx=10, pady=2)
        
        self.sql_text = scrolledtext.ScrolledText(self.sql_panel_frame, height=10, bg="#1E1E1E", fg="#D4D4D4", font=("Consolas", 10))
        self.sql_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.sql_text.config(state="disabled")

    def open_advanced_query(self):
        AdvancedQueryDialog(self)

    def toggle_live_sql(self):
        """Toggles the visibility of the Live SQL Activity Panel."""
        self.live_sql_enabled = not self.live_sql_enabled
        if self.live_sql_enabled:
            self.btn_live_sql.config(text="[ LIVE SQL: ON ]", style="Accent.TButton")
            self.sql_panel_frame.pack(fill=tk.X, side=tk.BOTTOM, before=self.status_bar_widget)
        else:
            self.btn_live_sql.config(text="[ LIVE SQL: OFF ]", style="Secondary.TButton")
            self.sql_panel_frame.pack_forget()

    def clear_sql_log(self):
        self.sql_history.clear()
        self.sql_text.config(state="normal")
        self.sql_text.delete(1.0, tk.END)
        self.sql_text.config(state="disabled")

    def on_sql_activity(self, log_entry):
        """Callback for db_logger. Appends SQL activity to the UI."""
        self.sql_history.append(log_entry)
        if len(self.sql_history) > 20:
            self.sql_history.pop(0)

        # Build display text
        lines = []
        lines.append("-" * 60)
        lines.append(f"[{log_entry['time']}]")
        lines.append("")
        lines.append(log_entry['sql'])
        lines.append("")
        if log_entry['success']:
            lines.append("\u2713 Query executed successfully")
            if log_entry.get('rows', 0) is not None:
                lines.append(f"Rows affected/returned: {log_entry['rows']}")
            if log_entry.get('is_cascade'):
                lines.append("Related faculty_academic record handled by foreign-key CASCADE.")
        else:
            lines.append("\u2717 Query failed")
            lines.append(f"Reason: {log_entry['error']}")
        lines.append("-" * 60)
        lines.append("")

        text_block = "\n".join(lines)

        # Schedule the widget update on the next Tkinter event loop tick.
        # This safely decouples from dialog destroy() calls that may be in-flight.
        def _update_widget():
            try:
                self.sql_text.config(state="normal")
                self.sql_text.insert(tk.END, text_block)
                self.sql_text.see(tk.END)
                self.sql_text.config(state="disabled")
            except tk.TclError:
                pass  # widget destroyed — ignore

        self.after(0, _update_widget)

    # -------------------------------------------------------------
    # TABLE SWITCHING & RECONFIGURATION LOGIC

    # -------------------------------------------------------------
    def on_table_switched(self, event=None):
        """Handles switching between 'faculty' and 'faculty_academic' tables."""
        selected_table_display = self.table_selector_cb.get()

        if selected_table_display == "Faculty Academic":
            self.active_table = "faculty_academic"
            self.table_status_lbl.config(
                text="CURRENT TABLE VIEW: FACULTY ACADEMIC (Table: faculty_academic)",
                fg="#0D9488"
            )
            self.btn_add.config(text="➕ Add Academic Record")
            self.btn_edit.config(text="✏️ Edit Academic Record")
            self.btn_del.config(text="🗑️ Delete Academic Record")

            # Update search field choices for Faculty Academic
            self.search_field_cb.config(values=[
                "All Fields", "Academic ID", "Faculty ID", "UG Qualification", "PG Qualification", "Ph.D. Qualification", "Research Interest"
            ])
            self.search_field_cb.set("All Fields")

            # Hide Department Filter for Academic table
            self.dept_label.grid_remove()
            self.dept_filter_cb.grid_remove()
        else:
            self.active_table = "faculty"
            self.table_status_lbl.config(
                text="CURRENT TABLE VIEW: FACULTY (Table: faculty)",
                fg="#003366"
            )
            self.btn_add.config(text="➕ Add Faculty Record")
            self.btn_edit.config(text="✏️ Edit Faculty Record")
            self.btn_del.config(text="🗑️ Delete Faculty Record")

            # Update search field choices for Faculty
            self.search_field_cb.config(values=[
                "All Fields", "Faculty Name", "Department", "Designation", "Faculty ID"
            ])
            self.search_field_cb.set("All Fields")

            # Show Department Filter for Faculty table
            self.dept_label.grid(row=0, column=4, padx=(0, 5), sticky=tk.W)
            self.dept_filter_cb.grid(row=0, column=5, padx=(0, 15), sticky=tk.W)

        self.setup_treeview_columns()
        self.on_search()

    def setup_treeview_columns(self):
        """Dynamically reconfigures Treeview columns & headers for active table."""
        # Clear items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.active_table == "faculty":
            cols = ("faculty_id", "faculty_name", "department", "designation", "email", "phone", "experience_years")
            self.tree.config(columns=cols)

            self.tree.heading("faculty_id", text="Faculty ID", anchor=tk.CENTER)
            self.tree.heading("faculty_name", text="Faculty Name", anchor=tk.W)
            self.tree.heading("department", text="Department", anchor=tk.W)
            self.tree.heading("designation", text="Designation", anchor=tk.W)
            self.tree.heading("email", text="Email Address", anchor=tk.W)
            self.tree.heading("phone", text="Phone", anchor=tk.CENTER)
            self.tree.heading("experience_years", text="Experience", anchor=tk.CENTER)

            self.tree.column("faculty_id", width=90, minwidth=80, anchor=tk.CENTER)
            self.tree.column("faculty_name", width=180, minwidth=140, anchor=tk.W)
            self.tree.column("department", width=220, minwidth=160, anchor=tk.W)
            self.tree.column("designation", width=170, minwidth=130, anchor=tk.W)
            self.tree.column("email", width=190, minwidth=150, anchor=tk.W)
            self.tree.column("phone", width=130, minwidth=100, anchor=tk.CENTER)
            self.tree.column("experience_years", width=80, minwidth=60, anchor=tk.CENTER)
        else:
            cols = ("academic_id", "faculty_id", "ug_qualification", "pg_qualification", "phd_qualification", "research_interest", "publication_count")
            self.tree.config(columns=cols)

            self.tree.heading("academic_id", text="Academic ID", anchor=tk.CENTER)
            self.tree.heading("faculty_id", text="Faculty ID", anchor=tk.CENTER)
            self.tree.heading("ug_qualification", text="UG Qualification", anchor=tk.W)
            self.tree.heading("pg_qualification", text="PG Qualification", anchor=tk.W)
            self.tree.heading("phd_qualification", text="Ph.D. Qualification", anchor=tk.W)
            self.tree.heading("research_interest", text="Research Interest", anchor=tk.W)
            self.tree.heading("publication_count", text="Pub. Count", anchor=tk.CENTER)

            self.tree.column("academic_id", width=95, minwidth=80, anchor=tk.CENTER)
            self.tree.column("faculty_id", width=95, minwidth=80, anchor=tk.CENTER)
            self.tree.column("ug_qualification", width=130, minwidth=100, anchor=tk.W)
            self.tree.column("pg_qualification", width=170, minwidth=120, anchor=tk.W)
            self.tree.column("phd_qualification", width=180, minwidth=130, anchor=tk.W)
            self.tree.column("research_interest", width=290, minwidth=200, anchor=tk.W)
            self.tree.column("publication_count", width=90, minwidth=70, anchor=tk.CENTER)

    # -------------------------------------------------------------
    # DB CONTROL & DATA REFRESH LOGIC
    # -------------------------------------------------------------
    def check_and_init_db(self):
        """Checks DB connectivity and initializes schema/seed if needed."""
        self.status_var.set("Connecting to MySQL Database...")
        success, msg = db.setup_database_schema()
        if success:
            self.status_var.set("Connected to MySQL Database: cit_faculty_db @ localhost:3306")
            self.setup_treeview_columns()
            self.refresh_data()
        else:
            self.status_var.set(f"DB Error: {msg}")
            resp = messagebox.askyesno(
                "MySQL Connection Failed",
                f"Could not connect to local MySQL server:\n\n{msg}\n\nWould you like to configure your MySQL Password in .env?"
            )
            if resp:
                self.on_open_db_config()

    def refresh_data(self):
        """Refreshes Dashboard metrics cards and Directory Treeview data."""
        # 1. Update Metrics Cards
        counts = db.get_dashboard_counts()
        for k, lbl in self.card_widgets.items():
            lbl.config(text=str(counts.get(k, 0)))

        # 2. Update Directory Tree
        self.on_search()

    def on_search(self):
        """Executes search against MySQL for active table and populates Treeview."""
        search_field = self.search_field_cb.get()
        search_text = self.search_entry.get().strip()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self.active_table == "faculty":
            dept_filter = self.dept_filter_cb.get()
            records = db.get_faculty_list(
                search_field=search_field,
                search_text=search_text,
                department_filter=dept_filter
            )
            for r in records:
                self.tree.insert("", tk.END, values=(
                    r["faculty_id"],
                    r["faculty_name"],
                    r["department"],
                    r["designation"],
                    r["email"] or "",
                    r["phone"] or "",
                    str(r.get("experience_years", "")) if r.get("experience_years") is not None else ""
                ))
            self.status_var.set(f"Loaded {len(records)} records from MySQL 'faculty' table.")
        else:
            records = db.get_academic_list(
                search_field=search_field,
                search_text=search_text
            )
            for r in records:
                self.tree.insert("", tk.END, values=(
                    r["academic_id"],
                    r["faculty_id"],
                    r["ug_qualification"] or "",
                    r["pg_qualification"] or "",
                    r["phd_qualification"] or "",
                    r["research_interest"] or "",
                    str(r["publication_count"]) if r["publication_count"] is not None else ""
                ))
            self.status_var.set(f"Loaded {len(records)} records from MySQL 'faculty_academic' table.")

    def on_reset_search(self):
        """Resets search filters and reloads all records."""
        self.search_field_cb.set("All Fields")
        self.search_entry.delete(0, tk.END)
        self.dept_filter_cb.set("All")
        self.on_search()

    # -------------------------------------------------------------
    # CRUD DIALOG & ACTION HANDLERS
    # -------------------------------------------------------------
    def get_selected_row_values(self):
        """Returns values tuple of selected row in Treeview."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a row from the table first.")
            return None
        return self.tree.item(selected[0], "values")

    def on_view_profile(self):
        """Opens Full Profile Window demonstrating Relational JOIN."""
        row_vals = self.get_selected_row_values()
        if not row_vals:
            return

        if self.active_table == "faculty":
            faculty_id = row_vals[0]
        else:
            faculty_id = row_vals[1]  # Second column in academic table is faculty_id

        profile = db.get_full_faculty_profile(faculty_id)
        if not profile:
            messagebox.showerror("Error", f"Could not retrieve combined profile for Faculty ID: {faculty_id}")
            return

        FacultyProfileDialog(self, profile)

    def on_add_record(self):
        """Opens Add Form Dialog for the active table."""
        if self.active_table == "faculty":
            AddFacultyDialog(self, mode="ADD", callback=self.refresh_data)
        else:
            AddAcademicDialog(self, mode="ADD", callback=self.refresh_data)

    def on_edit_record(self):
        """Opens Edit Form Dialog for the selected record in active table."""
        row_vals = self.get_selected_row_values()
        if not row_vals:
            return

        if self.active_table == "faculty":
            fac_id = row_vals[0]
            record = db.get_single_faculty_record(fac_id)
            if not record:
                messagebox.showerror("Error", f"Could not fetch record for Faculty ID: {fac_id}")
                return
            AddFacultyDialog(self, mode="EDIT", record=record, callback=self.refresh_data)
        else:
            aca_id = row_vals[0]
            record = db.get_single_academic_record(aca_id)
            if not record:
                messagebox.showerror("Error", f"Could not fetch record for Academic ID: {aca_id}")
                return
            AddAcademicDialog(self, mode="EDIT", record=record, callback=self.refresh_data)

    def on_delete_record(self):
        """Deletes selected record from active table with confirmation."""
        row_vals = self.get_selected_row_values()
        if not row_vals:
            return

        if self.active_table == "faculty":
            fac_id = row_vals[0]
            fac_name = row_vals[1]
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the faculty record from 'faculty' table?\n\n"
                f"Faculty ID: {fac_id}\n"
                f"Name: {fac_name}\n\n"
                f"Note: This will also automatically delete associated academic records via foreign key CASCADE."
            )
            if confirm:
                success, msg = db.delete_single_faculty(fac_id)
                if success:
                    messagebox.showinfo("Success", msg)
                    self.refresh_data()
                else:
                    messagebox.showerror("Deletion Failed", msg)
        else:
            aca_id = row_vals[0]
            fac_id = row_vals[1]
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the academic record from 'faculty_academic' table?\n\n"
                f"Academic ID: {aca_id}\n"
                f"Faculty ID: {fac_id}"
            )
            if confirm:
                success, msg = db.delete_single_academic(aca_id)
                if success:
                    messagebox.showinfo("Success", msg)
                    self.refresh_data()
                else:
                    messagebox.showerror("Deletion Failed", msg)

    def on_open_db_config(self):
        """Opens DB Credentials Dialog."""
        DBConfigDialog(self, callback=self.check_and_init_db)


# =================================================================
# FORM DIALOG 1: FACULTY TABLE FORM (Add / Edit)
# =================================================================
class AddFacultyDialog(tk.Toplevel):
    def __init__(self, parent, mode="ADD", record=None, callback=None):
        super().__init__(parent)
        self.mode = mode
        self.record = record or {}
        self.callback = callback

        title_txt = "Add New Faculty Record" if mode == "ADD" else f"Edit Faculty Record: {record.get('faculty_id', '')}"
        self.title(title_txt)
        self.geometry("480x500")
        self.resizable(False, False)
        self.configure(bg="#F4F6F9")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        if mode == "EDIT":
            self.populate_fields()

    def create_widgets(self):
        header = tk.Frame(self, bg="#003366", height=40, padx=12, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        title_str = "ADD FACULTY RECORD (Table: faculty)" if self.mode == "ADD" else f"EDIT FACULTY: {self.record.get('faculty_id', '')}"
        tk.Label(header, text=title_str, font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#003366").pack(anchor=tk.W)

        form = tk.Frame(self, bg="#F4F6F9", padx=20, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Department *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.dept_cb = ttk.Combobox(
            form,
            values=[
                "Computer Science and Engineering",
                "Electronics and Communication Engineering",
                "Electrical and Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering"
            ],
            state="readonly" if self.mode == "ADD" else "disabled",
            width=32
        )
        self.dept_cb.set("Computer Science and Engineering")
        self.dept_cb.grid(row=0, column=1, pady=3, sticky=tk.W)
        self.dept_cb.bind("<<ComboboxSelected>>", self.on_dept_changed)

        tk.Label(form, text="Faculty ID *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.id_entry = ttk.Entry(form, width=34)
        self.id_entry.grid(row=1, column=1, pady=3, sticky=tk.W)
        if self.mode == "EDIT":
            self.id_entry.config(state="disabled")

        tk.Label(form, text="Faculty Name *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.name_entry = ttk.Entry(form, width=34)
        self.name_entry.grid(row=2, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Designation *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.desig_cb = ttk.Combobox(
            form,
            values=["Professor", "Professor & Head", "Associate Professor", "Assistant Professor (Sr. Gr.)", "Assistant Professor (Sl. Gr.)", "Assistant Professor"],
            width=32
        )
        self.desig_cb.set("Assistant Professor")
        self.desig_cb.grid(row=3, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Email Address", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.email_entry = ttk.Entry(form, width=34)
        self.email_entry.grid(row=4, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Phone Number", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=5, column=0, sticky=tk.W, pady=3)
        self.phone_entry = ttk.Entry(form, width=34)
        self.phone_entry.grid(row=5, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Experience (Years)", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=6, column=0, sticky=tk.W, pady=3)
        self.exp_entry = ttk.Entry(form, width=34)
        self.exp_entry.grid(row=6, column=1, pady=3, sticky=tk.W)

        btn_bar = tk.Frame(self, bg="#F4F6F9", pady=10, padx=20)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_save = ttk.Button(btn_bar, text="SAVE RECORD", style="Primary.TButton", command=self.on_save)
        btn_save.pack(side=tk.RIGHT)

        btn_cancel = ttk.Button(btn_bar, text="CANCEL", style="Secondary.TButton", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=10)

        if self.mode == "ADD":
            self.on_dept_changed()

    def on_dept_changed(self, event=None):
        if self.mode == "ADD":
            dept = self.dept_cb.get()
            fac_id = db.generate_next_faculty_id(dept)
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, fac_id)

    def populate_fields(self):
        r = self.record
        self.dept_cb.set(r.get("department", ""))
        # id_entry is disabled in EDIT mode — temporarily enable to populate, then disable
        self.id_entry.config(state="normal")
        self.id_entry.insert(0, r.get("faculty_id", ""))
        self.id_entry.config(state="disabled")
        self.name_entry.insert(0, r.get("faculty_name", ""))
        self.desig_cb.set(r.get("designation", ""))
        self.email_entry.insert(0, r.get("email", "") or "")
        self.phone_entry.insert(0, r.get("phone", "") or "")
        self.exp_entry.insert(0, str(r.get("experience_years", "")) if r.get("experience_years") is not None else "")

    def on_save(self):
        # In EDIT mode id_entry is disabled; read from the original record
        if self.mode == "EDIT":
            fac_id = self.record.get("faculty_id", "").strip()
        else:
            fac_id = self.id_entry.get().strip()
        fac_name = self.name_entry.get().strip()
        dept = self.dept_cb.get().strip()
        desig = self.desig_cb.get().strip()

        if not fac_id or not fac_name or not dept or not desig:
            messagebox.showwarning("Validation Warning", "Please fill in all mandatory fields (*):\n- Faculty ID\n- Faculty Name\n- Department\n- Designation")
            return

        exp_val = self.exp_entry.get().strip()
        if exp_val and not exp_val.isdigit():
            messagebox.showwarning("Validation Warning", "Experience must be a valid non-negative integer.")
            return
        fac_data = {
            "faculty_id": fac_id,
            "faculty_name": fac_name,
            "department": dept,
            "designation": desig,
            "email": self.email_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "experience_years": exp_val if exp_val else None
        }

        if self.mode == "ADD":
            success, msg = db.add_single_faculty(fac_data)
        else:
            success, msg = db.update_single_faculty(fac_data)

        if success:
            messagebox.showinfo("Success", msg)
            if self.callback:
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Database Error", msg)


# =================================================================
# FORM DIALOG 2: FACULTY ACADEMIC TABLE FORM (Add / Edit)
# =================================================================
class AddAcademicDialog(tk.Toplevel):
    def __init__(self, parent, mode="ADD", record=None, callback=None):
        super().__init__(parent)
        self.mode = mode
        self.record = record or {}
        self.callback = callback

        title_txt = "Add Faculty Academic Record" if mode == "ADD" else f"Edit Academic Record: {record.get('academic_id', '')}"
        self.title(title_txt)
        self.geometry("520x560")
        self.resizable(False, False)
        self.configure(bg="#F4F6F9")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        if mode == "EDIT":
            self.populate_fields()

    def create_widgets(self):
        header = tk.Frame(self, bg="#0D9488", height=40, padx=12, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        title_str = "ADD ACADEMIC RECORD (Table: faculty_academic)" if self.mode == "ADD" else f"EDIT ACADEMIC RECORD: {self.record.get('academic_id', '')}"
        tk.Label(header, text=title_str, font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#0D9488").pack(anchor=tk.W)

        form = tk.Frame(self, bg="#F4F6F9", padx=20, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Academic ID *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.aca_id_entry = ttk.Entry(form, width=34)
        self.aca_id_entry.grid(row=0, column=1, pady=3, sticky=tk.W)
        if self.mode == "EDIT":
            self.aca_id_entry.config(state="disabled")
        else:
            next_aca = db.generate_next_academic_id()
            self.aca_id_entry.insert(0, next_aca)

        tk.Label(form, text="Faculty ID (Foreign Key) *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=1, column=0, sticky=tk.W, pady=3)
        
        # Populate combobox with existing faculty IDs
        existing_fac_ids = db.get_all_faculty_ids()
        self.fac_id_cb = ttk.Combobox(form, values=existing_fac_ids, width=32)
        if existing_fac_ids:
            self.fac_id_cb.set(existing_fac_ids[0])
        self.fac_id_cb.grid(row=1, column=1, pady=3, sticky=tk.W)
        if self.mode == "EDIT":
            self.fac_id_cb.config(state="disabled")

        tk.Label(form, text="UG Qualification", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.ug_entry = ttk.Entry(form, width=34)
        self.ug_entry.grid(row=2, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="PG Qualification", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.pg_entry = ttk.Entry(form, width=34)
        self.pg_entry.grid(row=3, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Ph.D. Qualification", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=4, column=0, sticky=tk.W, pady=3)
        self.phd_entry = ttk.Entry(form, width=34)
        self.phd_entry.grid(row=4, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Publication Count", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=5, column=0, sticky=tk.W, pady=3)
        self.pub_entry = ttk.Entry(form, width=34)
        self.pub_entry.grid(row=5, column=1, pady=3, sticky=tk.W)

        tk.Label(form, text="Research Interest", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=6, column=0, sticky=tk.W, pady=3)
        self.research_txt = scrolledtext.ScrolledText(form, width=32, height=4, font=("Segoe UI", 9))
        self.research_txt.grid(row=6, column=1, pady=3, sticky=tk.W)

        btn_bar = tk.Frame(self, bg="#F4F6F9", pady=10, padx=20)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_save = ttk.Button(btn_bar, text="SAVE RECORD", style="Accent.TButton", command=self.on_save)
        btn_save.pack(side=tk.RIGHT)

        btn_cancel = ttk.Button(btn_bar, text="CANCEL", style="Secondary.TButton", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=10)

    def populate_fields(self):
        r = self.record
        self.aca_id_entry.insert(0, r.get("academic_id", ""))
        self.fac_id_cb.set(r.get("faculty_id", ""))
        self.ug_entry.insert(0, r.get("ug_qualification", "") or "")
        self.pg_entry.insert(0, r.get("pg_qualification", "") or "")
        self.phd_entry.insert(0, r.get("phd_qualification", "") or "")
        self.pub_entry.insert(0, str(r.get("publication_count", "")) if r.get("publication_count") is not None else "")
        self.research_txt.insert(tk.END, r.get("research_interest", "") or "")

    def on_save(self):
        aca_id = self.aca_id_entry.get().strip()
        fac_id = self.fac_id_cb.get().strip()

        if not aca_id or not fac_id:
            messagebox.showwarning("Validation Warning", "Please fill in mandatory fields (*):\n- Academic ID\n- Faculty ID")
            return

        pub_cnt_str = self.pub_entry.get().strip()
        if pub_cnt_str and not pub_cnt_str.isdigit():
            messagebox.showwarning("Validation Warning", "Publication Count must be a valid integer number.")
            return

        aca_data = {
            "academic_id": aca_id,
            "faculty_id": fac_id,
            "ug_qualification": self.ug_entry.get().strip(),
            "pg_qualification": self.pg_entry.get().strip(),
            "phd_qualification": self.phd_entry.get().strip(),
            "publication_count": pub_cnt_str,
            "research_interest": self.research_txt.get("1.0", tk.END).strip()
        }

        if self.mode == "ADD":
            success, msg = db.add_single_academic(aca_data)
        else:
            success, msg = db.update_single_academic(aca_data)

        if success:
            messagebox.showinfo("Success", msg)
            if self.callback:
                self.callback()
            self.destroy()
        else:
            messagebox.showerror("Database Error", msg)


# =================================================================
# DIALOG 3: FULL FACULTY PROFILE DIALOG (JOIN DEMONSTRATION)
# =================================================================
class FacultyProfileDialog(tk.Toplevel):
    def __init__(self, parent, profile):
        super().__init__(parent)
        self.profile = profile
        self.parent = parent

        self.title(f"Full Faculty Profile - {profile.get('faculty_name', '')} ({profile.get('faculty_id', '')})")
        self.geometry("680x600")
        self.resizable(False, False)
        self.configure(bg="#F4F6F9")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        """Displays full combined profile fetched using relational JOIN."""
        p = self.profile

        # Header Banner
        header = tk.Frame(self, bg="#003366", height=60, padx=15, pady=10)
        header.pack(fill=tk.X, side=tk.TOP)

        name_lbl = tk.Label(header, text=p.get("faculty_name", "N/A"), font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#003366")
        name_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(header, text=f"{p.get('designation', '')} | {p.get('department', '')} | Faculty ID: {p.get('faculty_id', '')}", font=("Segoe UI", 9, "bold"), fg="#D4AF37", bg="#003366")
        sub_lbl.pack(anchor=tk.W)

        body = tk.Frame(self, bg="#F4F6F9", padx=15, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # 1. Faculty Information Frame
        fac_group = tk.LabelFrame(body, text=" PERSONAL & CONTACT INFORMATION (Table: faculty) ", font=("Segoe UI", 10, "bold"), fg="#003366", bg="#F4F6F9", padx=12, pady=8)
        fac_group.pack(fill=tk.X, pady=(0, 10))

        fac_info = [
            ("Faculty ID:", p.get("faculty_id")),
            ("Full Name:", p.get("faculty_name")),
            ("Department:", p.get("department")),
            ("Designation:", p.get("designation")),
            ("Email Address:", p.get("email") or "N/A"),
            ("Phone Number:", p.get("phone") or "N/A"),
            ("Experience (Years):", str(p.get("experience_years")) if p.get("experience_years") is not None else "N/A")
        ]

        for i, (label, val) in enumerate(fac_info):
            r, c = divmod(i, 2)
            lbl = tk.Label(fac_group, text=label, font=("Segoe UI", 9, "bold"), fg="#4B5563", bg="#F4F6F9")
            lbl.grid(row=r*2, column=c*2, sticky=tk.W, padx=5, pady=(2, 0))

            val_lbl = tk.Label(fac_group, text=val, font=("Segoe UI", 9), fg="#1F2937", bg="#F4F6F9")
            val_lbl.grid(row=r*2+1, column=c*2, sticky=tk.W, padx=5, pady=(0, 6))

        fac_group.columnconfigure(0, weight=1)
        fac_group.columnconfigure(2, weight=1)

        # 2. Academic Information Frame
        aca_group = tk.LabelFrame(body, text=" ACADEMIC QUALIFICATIONS & RESEARCH (Table: faculty_academic) ", font=("Segoe UI", 10, "bold"), fg="#003366", bg="#F4F6F9", padx=12, pady=8)
        aca_group.pack(fill=tk.BOTH, expand=True)

        aca_info = [
            ("Academic ID:", p.get("academic_id") or "N/A"),
            ("UG Degree:", p.get("ug_qualification") or "N/A"),
            ("PG Degree:", p.get("pg_qualification") or "N/A"),
            ("Ph.D. Qualification:", p.get("phd_qualification") or "N/A"),
            ("Publication Count:", str(p.get("publication_count")) if p.get("publication_count") is not None else "N/A")
        ]

        for i, (label, val) in enumerate(aca_info):
            r, c = divmod(i, 2)
            lbl = tk.Label(aca_group, text=label, font=("Segoe UI", 9, "bold"), fg="#4B5563", bg="#F4F6F9")
            lbl.grid(row=r*2, column=c*2, sticky=tk.W, padx=5, pady=(2, 0))

            val_lbl = tk.Label(aca_group, text=val, font=("Segoe UI", 9), fg="#1F2937", bg="#F4F6F9")
            val_lbl.grid(row=r*2+1, column=c*2, sticky=tk.W, padx=5, pady=(0, 6))

        aca_group.columnconfigure(0, weight=1)
        aca_group.columnconfigure(2, weight=1)

        # Research Interests
        tk.Label(aca_group, text="Research Interests:", font=("Segoe UI", 9, "bold"), fg="#4B5563", bg="#F4F6F9").grid(row=6, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(4, 0))
        res_txt = scrolledtext.ScrolledText(aca_group, height=3, font=("Segoe UI", 9), bg="#FFFFFF", fg="#1F2937")
        res_txt.insert(tk.END, p.get("research_interest") or "N/A")
        res_txt.config(state="disabled")
        res_txt.grid(row=7, column=0, columnspan=4, sticky="ew", padx=5, pady=(2, 6))

        # Bottom Action Bar
        btn_bar = tk.Frame(self, bg="#F4F6F9", pady=10, padx=15)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_close = ttk.Button(btn_bar, text="CLOSE", style="Secondary.TButton", command=self.destroy)
        btn_close.pack(side=tk.RIGHT)


# =================================================================
# DIALOG 4: DB CREDENTIALS CONFIGURATION DIALOG
# =================================================================
class DBConfigDialog(tk.Toplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback

        self.title("MySQL Database Connection Configuration")
        self.geometry("450x380")
        self.resizable(False, False)
        self.configure(bg="#F4F6F9")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#003366", height=40, padx=12, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        tk.Label(header, text="MYSQL DATABASE CONFIGURATION", font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#003366").pack(anchor=tk.W)

        form = tk.Frame(self, bg="#F4F6F9", padx=20, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Database Host:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.host_entry = ttk.Entry(form, width=28)
        self.host_entry.insert(0, os.getenv("DB_HOST", "localhost"))
        self.host_entry.grid(row=0, column=1, pady=4)

        tk.Label(form, text="Database Port:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.port_entry = ttk.Entry(form, width=28)
        self.port_entry.insert(0, os.getenv("DB_PORT", "3306"))
        self.port_entry.grid(row=1, column=1, pady=4)

        tk.Label(form, text="MySQL Username:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.user_entry = ttk.Entry(form, width=28)
        self.user_entry.insert(0, os.getenv("DB_USER", "root"))
        self.user_entry.grid(row=2, column=1, pady=4)

        tk.Label(form, text="MySQL Password:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.pass_entry = ttk.Entry(form, width=28, show="*")
        self.pass_entry.insert(0, os.getenv("DB_PASSWORD", ""))
        self.pass_entry.grid(row=3, column=1, pady=4)

        tk.Label(form, text="Database Name:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=4, column=0, sticky=tk.W, pady=4)
        self.name_entry = ttk.Entry(form, width=28)
        self.name_entry.insert(0, os.getenv("DB_NAME", "cit_faculty_db"))
        self.name_entry.grid(row=4, column=1, pady=4)

        btn_bar = tk.Frame(self, bg="#F4F6F9", pady=10, padx=20)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_save = ttk.Button(btn_bar, text="SAVE & CONNECT", style="Primary.TButton", command=self.on_save)
        btn_save.pack(side=tk.RIGHT)

        btn_cancel = ttk.Button(btn_bar, text="CANCEL", style="Secondary.TButton", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=10)

    def on_save(self):
        """Saves environment parameters to .env file and triggers DB reconnect."""
        env_file = ".env"

        set_key(env_file, "DB_HOST", self.host_entry.get().strip())
        set_key(env_file, "DB_PORT", self.port_entry.get().strip())
        set_key(env_file, "DB_USER", self.user_entry.get().strip())
        set_key(env_file, "DB_PASSWORD", self.pass_entry.get().strip())
        set_key(env_file, "DB_NAME", self.name_entry.get().strip())

        load_dotenv(override=True)

        messagebox.showinfo("Config Saved", "Database configuration updated in .env file successfully.")
        if self.callback:
            self.callback()
        self.destroy()


# =================================================================
# MAIN ENTRY POINT
# =================================================================
class AdvancedQueryDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Advanced DBMS Query Builder")
        self.geometry("780x600")
        self.configure(bg="#F4F6F9")
        self.transient(parent)
        self.grab_set()
        
        self.conditions = []
        self.fac_fields = ['faculty_id', 'faculty_name', 'department', 'designation', 'email', 'phone', 'experience_years']
        self.aca_fields = ['academic_id', 'ug_qualification', 'pg_qualification', 'phd_qualification', 'research_interest', 'publication_count']

        # Known values for categorical fields (used to populate value dropdowns)
        self.VALUE_OPTIONS = {
            'department': [
                'Computer Science and Engineering',
                'Electronics and Communication Engineering',
                'Electrical and Electronics Engineering',
                'Mechanical Engineering',
                'Civil Engineering',
            ],
            'designation': [
                'Principal & Professor',
                'Professor & Head',
                'Professor',
                'Associate Professor',
                'Assistant Professor (Sr. Gr.)',
                'Assistant Professor (Sl. Gr.)',
                'Assistant Professor',
            ],
            'ug_qualification':  self._fetch_distinct('faculty_academic', 'ug_qualification'),
            'pg_qualification':  self._fetch_distinct('faculty_academic', 'pg_qualification'),
            'phd_qualification': self._fetch_distinct('faculty_academic', 'phd_qualification'),
            'research_interest': self._fetch_distinct('faculty_academic', 'research_interest'),
        }

        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#003366", height=50, padx=15, pady=10)
        header.pack(fill=tk.X, side=tk.TOP)
        tk.Label(header, text="ADVANCED SQL QUERY BUILDER", font=("Segoe UI", 12, "bold"), fg="#FFFFFF", bg="#003366").pack(anchor=tk.W)
        
        # Query Type Frame
        top_frame = tk.Frame(self, bg="#F4F6F9", padx=15, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="Query Type:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").pack(side=tk.LEFT)
        self.qtype_cb = ttk.Combobox(top_frame, values=["Records", "Count"], state="readonly", width=15)
        self.qtype_cb.set("Records")
        self.qtype_cb.pack(side=tk.LEFT, padx=10)
        
        tk.Label(top_frame, text="Table Scope:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").pack(side=tk.LEFT, padx=(20, 0))
        self.table_scope_cb = ttk.Combobox(top_frame, values=["Faculty", "Faculty Academic"], state="readonly", width=20)
        self.table_scope_cb.set("Faculty")
        self.table_scope_cb.pack(side=tk.LEFT, padx=10)
        self.table_scope_cb.bind("<<ComboboxSelected>>", self.on_scope_change)
        
        # Conditions Frame
        self.cond_frame = tk.LabelFrame(self, text=" Filtering Conditions ", font=("Segoe UI", 10, "bold"), bg="#F4F6F9", fg="#003366", padx=10, pady=10)
        self.cond_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.cond_list_frame = tk.Frame(self.cond_frame, bg="#F4F6F9")
        self.cond_list_frame.pack(fill=tk.BOTH, expand=True)
        
        btn_add_cond = ttk.Button(self.cond_frame, text="+ ADD CONDITION", command=self.add_condition_row)
        btn_add_cond.pack(anchor=tk.W, pady=10)
        
        # Sorting Frame
        sort_frame = tk.LabelFrame(self, text=" Sorting (ORDER BY) ", font=("Segoe UI", 10, "bold"), bg="#F4F6F9", fg="#003366", padx=10, pady=10)
        sort_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(sort_frame, text="Sort By:", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=0, column=0, padx=5, pady=5)
        self.sort_field_cb = ttk.Combobox(sort_frame, state="readonly", width=25)
        self.sort_field_cb.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(sort_frame, text="Order:", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=0, column=2, padx=15, pady=5)
        self.sort_order_cb = ttk.Combobox(sort_frame, values=["ASC", "DESC"], state="readonly", width=10)
        self.sort_order_cb.set("ASC")
        self.sort_order_cb.grid(row=0, column=3, padx=5, pady=5)
        
        self.on_scope_change()
        
        # Bottom Buttons
        btn_bar = tk.Frame(self, bg="#F4F6F9", pady=10, padx=15)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_run = ttk.Button(btn_bar, text="▶ RUN QUERY", style="Accent.TButton", command=self.run_query)
        btn_run.pack(side=tk.RIGHT)
        
        btn_clear = ttk.Button(btn_bar, text="CLEAR CONDITIONS", style="Secondary.TButton", command=self.clear_conditions)
        btn_clear.pack(side=tk.RIGHT, padx=10)
        
        self.add_condition_row()
        
    def _fetch_distinct(self, table, column):
        """Fetches distinct non-null values from a column for dropdown population."""
        try:
            import db as _db
            conn = _db.get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT DISTINCT `{column}` FROM `{table}` WHERE `{column}` IS NOT NULL ORDER BY `{column}`;")
            vals = [r[0] for r in cur.fetchall() if r[0]]
            cur.close()
            conn.close()
            return vals
        except Exception:
            return []

    def on_scope_change(self, event=None):
        scope = self.table_scope_cb.get()
        if scope == "Faculty":
            fields = self.fac_fields
        else:
            fields = self.fac_fields + self.aca_fields
        self.sort_field_cb.config(values=[""] + fields)
        self.sort_field_cb.set("")

        for row in self.conditions:
            row['field_cb'].config(values=fields)
            if row['field_cb'].get() not in fields:
                row['field_cb'].set(fields[0])
            self._refresh_val_widget(row)

    def _refresh_val_widget(self, row):
        """Updates the value Combobox options based on the currently selected field."""
        field = row['field_cb'].get()
        op = row['op_cb'].get()
        val_cb = row['val_entry']  # it's actually a Combobox now

        if op in ('IS NULL', 'IS NOT NULL'):
            val_cb.config(state='disabled', values=[])
            return

        options = self.VALUE_OPTIONS.get(field, [])
        val_cb.config(values=options)
        if options:
            val_cb.config(state='normal')   # editable combobox
        else:
            val_cb.config(state='normal')   # plain editable entry behaviour

    def add_condition_row(self):
        row_frame = tk.Frame(self.cond_list_frame, bg="#F4F6F9")
        row_frame.pack(fill=tk.X, pady=2)

        scope = self.table_scope_cb.get()
        fields = self.fac_fields if scope == "Faculty" else self.fac_fields + self.aca_fields

        logic_cb = ttk.Combobox(row_frame, values=["AND", "OR"], state="readonly", width=5)
        if not self.conditions:
            logic_cb.set("")
            logic_cb.config(state="disabled")
        else:
            logic_cb.set("AND")
        logic_cb.pack(side=tk.LEFT, padx=2)

        field_cb = ttk.Combobox(row_frame, values=fields, state="readonly", width=20)
        field_cb.set(fields[0])
        field_cb.pack(side=tk.LEFT, padx=2)

        op_cb = ttk.Combobox(row_frame, values=["=", "!=", ">", "<", ">=", "<=", "LIKE", "IS NULL", "IS NOT NULL"], state="readonly", width=12)
        op_cb.set("=")
        op_cb.pack(side=tk.LEFT, padx=2)

        # Value widget: editable Combobox so categorical fields show a dropdown
        # but user can still type custom values
        initial_opts = self.VALUE_OPTIONS.get(fields[0], [])
        val_cb = ttk.Combobox(row_frame, values=initial_opts, width=25)
        val_cb.pack(side=tk.LEFT, padx=2)

        btn_del = ttk.Button(row_frame, text="X", width=3, command=lambda f=row_frame: self.remove_condition_row(f))
        btn_del.pack(side=tk.LEFT, padx=5)

        row_dict = {
            'frame': row_frame,
            'logic_cb': logic_cb,
            'field_cb': field_cb,
            'op_cb': op_cb,
            'val_entry': val_cb,   # key kept as val_entry for compatibility with run_query
        }
        self.conditions.append(row_dict)

        # When field changes → refresh value dropdown options
        def on_field_change(event, row=row_dict):
            self._refresh_val_widget(row)
            row['val_entry'].set('')   # clear stale value
        field_cb.bind("<<ComboboxSelected>>", on_field_change)

        # When operator changes → handle IS NULL / IS NOT NULL disabling
        def on_op_change(event, row=row_dict):
            self._refresh_val_widget(row)
        op_cb.bind("<<ComboboxSelected>>", on_op_change)

        
    def remove_condition_row(self, frame):
        for cond in self.conditions:
            if cond['frame'] == frame:
                frame.destroy()
                self.conditions.remove(cond)
                break
        if self.conditions:
            self.conditions[0]['logic_cb'].set("")
            self.conditions[0]['logic_cb'].config(state="disabled")
            
    def clear_conditions(self):
        for cond in self.conditions:
            cond['frame'].destroy()
        self.conditions.clear()
        self.sort_field_cb.set("")
        self.add_condition_row()
        
    def run_query(self):
        cond_data = []
        for i, row in enumerate(self.conditions):
            op = row['op_cb'].get()
            val = row['val_entry'].get().strip()
            if op not in ['IS NULL', 'IS NOT NULL'] and not val:
                continue
            cond_data.append({
                'logic': row['logic_cb'].get() if i > 0 else "",
                'field': row['field_cb'].get(),
                'op': op,
                'val': val
            })
            
        qtype = self.qtype_cb.get()
        scope = self.table_scope_cb.get()  # "Faculty" or "Faculty Academic"
        sort_by = self.sort_field_cb.get()
        sort_order = self.sort_order_cb.get()

        if not sort_by:
            sort_by = None

        success, result = db.execute_advanced_query(qtype, cond_data, sort_by, sort_order, scope=scope)

        if not success:
            messagebox.showerror("Query Failed", f"Execution failed:\n{result}")
            return

        if qtype == "Count":
            messagebox.showinfo("Query Result", f"Total matching records: {result}")
            return  # Keep dialog open so user can adjust and re-run

        # ── RECORDS mode: push results into main Treeview ──────────────
        self.parent.tree.delete(*self.parent.tree.get_children())

        is_academic = (scope == "Faculty Academic") or (result and 'academic_id' in result[0])

        if is_academic:
            # Sync active table & dropdown
            self.parent.active_table = "faculty_academic"
            if hasattr(self.parent, 'table_selector_cb'):
                self.parent.table_selector_cb.set("Faculty Academic")
            self.parent.setup_treeview_columns()
            for r in result:
                self.parent.tree.insert("", tk.END, values=(
                    r.get("academic_id", ""),
                    r.get("faculty_id", ""),
                    r.get("ug_qualification", "") or "",
                    r.get("pg_qualification", "") or "",
                    r.get("phd_qualification", "") or "",
                    r.get("research_interest", "") or "",
                    str(r.get("publication_count", "")) if r.get("publication_count") is not None else ""
                ))
        else:
            # Sync active table & dropdown
            self.parent.active_table = "faculty"
            if hasattr(self.parent, 'table_selector_cb'):
                self.parent.table_selector_cb.set("Faculty")
            self.parent.setup_treeview_columns()
            for r in result:
                self.parent.tree.insert("", tk.END, values=(
                    r.get("faculty_id", ""),
                    r.get("faculty_name", ""),
                    r.get("department", ""),
                    r.get("designation", ""),
                    r.get("email", "") or "",
                    r.get("phone", "") or "",
                    str(r.get("experience_years", "")) if r.get("experience_years") is not None else ""
                ))

        self.parent.status_var.set(
            f"Advanced Query [{scope}] — {len(result)} record(s) returned."
        )
        self.destroy()


if __name__ == "__main__":
    app = CITFacultyApp()
    app.mainloop()

# =================================================================
# DIALOG 5: ADVANCED QUERY BUILDER
# =================================================================
