import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dotenv import load_dotenv, set_key

import db

# Ensure environment variables are loaded
load_dotenv()

class CITFacultyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CIT Faculty Management System - DBMS Mini-Project")
        self.geometry("1180x740")
        self.minsize(980, 640)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Build Main UI Layout
        self.create_header()
        self.create_dashboard_summary()
        self.create_search_bar()
        self.create_directory_tree()
        self.create_action_buttons()
        self.create_statusbar()

        # Check DB Connection & Initialize Data
        self.after(200, self.check_and_init_db)

    def configure_styles(self):
        """Sets up custom TTK widget styling."""
        # Colors
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
            text="FACULTY MANAGEMENT SYSTEM — 23EC523 DBMS LABORATORY MINI-PROJECT",
            font=("Segoe UI", 10, "bold"),
            fg="#D4AF37",
            bg="#003366"
        )
        subtitle_label.pack(anchor=tk.W, padx=20, pady=(0, 8))

    def create_dashboard_summary(self):
        """Top Metrics Cards Frame displaying real counts from MySQL."""
        self.dashboard_frame = tk.Frame(self, bg="#F4F6F9", pady=10, padx=15)
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

            # Top Strip Color
            strip = tk.Frame(card, bg=color, height=4)
            strip.pack(fill=tk.X, side=tk.TOP)

            val_lbl = tk.Label(card, text="--", font=("Segoe UI", 18, "bold"), fg=color, bg="#FFFFFF")
            val_lbl.pack(pady=(6, 0))

            title_lbl = tk.Label(card, text=label, font=("Segoe UI", 8, "bold"), fg="#6B7280", bg="#FFFFFF")
            title_lbl.pack(pady=(0, 6))

            self.card_widgets[key] = val_lbl

    def create_search_bar(self):
        """Search and Filter Controls Bar."""
        search_frame = tk.LabelFrame(
            self,
            text=" Search & Filter Faculty Directory ",
            font=("Segoe UI", 10, "bold"),
            fg="#003366",
            bg="#F4F6F9",
            padx=12,
            pady=8
        )
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 8))

        # Search By Dropdown
        tk.Label(search_frame, text="Search Field:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.search_field_cb = ttk.Combobox(
            search_frame,
            values=["All Fields", "Faculty Name", "Department", "Designation", "Faculty ID"],
            state="readonly",
            width=14
        )
        self.search_field_cb.set("All Fields")
        self.search_field_cb.grid(row=0, column=1, padx=(0, 15), sticky=tk.W)

        # Search Query Entry
        tk.Label(search_frame, text="Keyword:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.search_entry = ttk.Entry(search_frame, width=24)
        self.search_entry.grid(row=0, column=3, padx=(0, 15), sticky=tk.W)
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        # Department Filter Combobox
        tk.Label(search_frame, text="Department:", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=4, padx=(0, 5), sticky=tk.W)
        self.dept_filter_cb = ttk.Combobox(
            search_frame,
            values=[
                "All",
                "Computer Science and Engineering",
                "Electronics and Communication Engineering",
                "Electrical and Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering"
            ],
            state="readonly",
            width=28
        )
        self.dept_filter_cb.set("All")
        self.dept_filter_cb.grid(row=0, column=5, padx=(0, 15), sticky=tk.W)
        self.dept_filter_cb.bind("<<ComboboxSelected>>", lambda e: self.on_search())

        # Search and Reset Buttons
        btn_search = ttk.Button(search_frame, text="🔍 SEARCH", style="Primary.TButton", command=self.on_search)
        btn_search.grid(row=0, column=6, padx=(0, 5))

        btn_reset = ttk.Button(search_frame, text="🔄 RESET", style="Secondary.TButton", command=self.on_reset_search)
        btn_reset.grid(row=0, column=7)

    def create_directory_tree(self):
        """Faculty Directory Table using TTK Treeview."""
        tree_container = tk.Frame(self, bg="#F4F6F9")
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 8))

        columns = ("faculty_id", "faculty_name", "department", "designation", "email", "phone", "joining_date")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings", selectmode="browse")

        # Headings
        self.tree.heading("faculty_id", text="Faculty ID", anchor=tk.CENTER)
        self.tree.heading("faculty_name", text="Faculty Name", anchor=tk.W)
        self.tree.heading("department", text="Department", anchor=tk.W)
        self.tree.heading("designation", text="Designation", anchor=tk.W)
        self.tree.heading("email", text="Email Address", anchor=tk.W)
        self.tree.heading("phone", text="Phone", anchor=tk.CENTER)
        self.tree.heading("joining_date", text="Joining Date", anchor=tk.CENTER)

        # Column widths
        self.tree.column("faculty_id", width=90, minwidth=80, anchor=tk.CENTER)
        self.tree.column("faculty_name", width=180, minwidth=140, anchor=tk.W)
        self.tree.column("department", width=220, minwidth=160, anchor=tk.W)
        self.tree.column("designation", width=170, minwidth=130, anchor=tk.W)
        self.tree.column("email", width=190, minwidth=150, anchor=tk.W)
        self.tree.column("phone", width=110, minwidth=90, anchor=tk.CENTER)
        self.tree.column("joining_date", width=100, minwidth=80, anchor=tk.CENTER)

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
        """Action Toolbar with CRUD operation buttons."""
        action_frame = tk.Frame(self, bg="#F4F6F9")
        action_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        btn_add = ttk.Button(action_frame, text="➕ Add Faculty", style="Primary.TButton", command=self.on_add_faculty)
        btn_add.pack(side=tk.LEFT, padx=(0, 10))

        btn_view = ttk.Button(action_frame, text="👁️ View Full Profile (JOIN)", style="Accent.TButton", command=self.on_view_profile)
        btn_view.pack(side=tk.LEFT, padx=(0, 10))

        btn_edit = ttk.Button(action_frame, text="✏️ Edit Faculty", style="Primary.TButton", command=self.on_edit_faculty)
        btn_edit.pack(side=tk.LEFT, padx=(0, 10))

        btn_del = ttk.Button(action_frame, text="🗑️ Delete Faculty", style="Danger.TButton", command=self.on_delete_faculty)
        btn_del.pack(side=tk.LEFT, padx=(0, 10))

        btn_config = ttk.Button(action_frame, text="⚙️ DB Config", style="Secondary.TButton", command=self.on_open_db_config)
        btn_config.pack(side=tk.RIGHT)

        btn_refresh = ttk.Button(action_frame, text="🔄 Refresh List", style="Secondary.TButton", command=self.refresh_data)
        btn_refresh.pack(side=tk.RIGHT, padx=(0, 10))

    def create_statusbar(self):
        """Bottom Status bar showing DB state and status messages."""
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

    # -------------------------------------------------------------
    # DB CONTROL & DATA REFRESH LOGIC
    # -------------------------------------------------------------
    def check_and_init_db(self):
        """Checks DB connectivity and initializes schema/seed if needed."""
        self.status_var.set("Connecting to MySQL Database...")
        success, msg = db.setup_database_schema()
        if success:
            self.status_var.set("Connected to MySQL Database: cit_faculty_db @ localhost:3306")
            self.refresh_data()
        else:
            self.status_var.set(f"DB Error: {msg}")
            # Prompt user if connection failed
            resp = messagebox.askyesno(
                "MySQL Connection Failed",
                f"Could not connect to local MySQL server:\n\n{msg}\n\nWould you like to configure your MySQL Password in .env?"
            )
            if resp:
                self.on_open_db_config()

    def refresh_data(self):
        """Refreshes Metrics Cards and Directory Treeview data."""
        # 1. Update Metrics Cards
        counts = db.get_dashboard_counts()
        for k, lbl in self.card_widgets.items():
            lbl.config(text=str(counts.get(k, 0)))

        # 2. Update Directory Tree
        self.on_search()

    def on_search(self):
        """Executes search against MySQL and populates Treeview."""
        search_field = self.search_field_cb.get()
        search_text = self.search_entry.get().strip()
        dept_filter = self.dept_filter_cb.get()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

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
                str(r["joining_date"]) if r["joining_date"] else ""
            ))

        self.status_var.set(f"Loaded {len(records)} faculty records from MySQL database.")

    def on_reset_search(self):
        """Resets search filters and reloads all records."""
        self.search_field_cb.set("All Fields")
        self.search_entry.delete(0, tk.END)
        self.dept_filter_cb.set("All")
        self.on_search()

    # -------------------------------------------------------------
    # CRUD DIALOG HANDLERS
    # -------------------------------------------------------------
    def get_selected_faculty_id(self):
        """Returns the selected faculty_id from Treeview."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a faculty member from the directory table first.")
            return None
        item_values = self.tree.item(selected[0], "values")
        return item_values[0]

    def on_view_profile(self):
        """Opens Full Profile Window demonstrating Relational JOIN."""
        faculty_id = self.get_selected_faculty_id()
        if not faculty_id:
            return

        profile = db.get_full_faculty_profile(faculty_id)
        if not profile:
            messagebox.showerror("Error", f"Could not retrieve profile for Faculty ID: {faculty_id}")
            return

        FacultyProfileDialog(self, profile)

    def on_add_faculty(self):
        """Opens Add Faculty Dialog."""
        AddEditFacultyDialog(self, mode="ADD", callback=self.refresh_data)

    def on_edit_faculty(self):
        """Opens Edit Faculty Dialog for selected record."""
        faculty_id = self.get_selected_faculty_id()
        if not faculty_id:
            return

        profile = db.get_full_faculty_profile(faculty_id)
        if not profile:
            messagebox.showerror("Error", f"Could not retrieve record for Faculty ID: {faculty_id}")
            return

        AddEditFacultyDialog(self, mode="EDIT", profile=profile, callback=self.refresh_data)

    def on_delete_faculty(self):
        """Deletes selected faculty record with confirmation."""
        faculty_id = self.get_selected_faculty_id()
        if not faculty_id:
            return

        selected = self.tree.selection()
        fac_name = self.tree.item(selected[0], "values")[1]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the faculty record for:\n\n"
            f"ID: {faculty_id}\n"
            f"Name: {fac_name}\n\n"
            f"Note: This will also remove the corresponding academic details via foreign key CASCADE."
        )

        if confirm:
            success, msg = db.delete_faculty_record(faculty_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_data()
            else:
                messagebox.showerror("Deletion Failed", msg)

    def on_open_db_config(self):
        """Opens DB Connection Credentials Configuration Dialog."""
        DBConfigDialog(self, callback=self.check_and_init_db)


# =================================================================
# DIALOG 1 & 2: ADD / EDIT FACULTY FORM DIALOG
# =================================================================
class AddEditFacultyDialog(tk.Toplevel):
    def __init__(self, parent, mode="ADD", profile=None, callback=None):
        super().__init__(parent)
        self.mode = mode
        self.profile = profile or {}
        self.callback = callback

        title_text = "Add New Faculty Member" if mode == "ADD" else f"Edit Faculty Record: {profile.get('faculty_id', '')}"
        self.title(title_text)
        self.geometry("760x620")
        self.resizable(False, False)
        self.configure(bg="#F4F6F9")
        self.transient(parent)
        self.grab_set()

        self.create_form_widgets()
        if mode == "EDIT":
            self.populate_existing_values()

    def create_form_widgets(self):
        """Constructs the form layout for Faculty and Academic fields."""
        # Header Banner
        header = tk.Frame(self, bg="#003366", height=45)
        header.pack(fill=tk.X, side=tk.TOP)
        title_lbl = tk.Label(
            header,
            text="FACULTY MEMBER FORM" if self.mode == "ADD" else f"EDIT FACULTY: {self.profile.get('faculty_id', '')}",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg="#003366"
        )
        title_lbl.pack(side=tk.LEFT, padx=15, pady=8)

        # Main Scrollable Frame Container
        container = tk.Frame(self, bg="#F4F6F9", padx=15, pady=10)
        container.pack(fill=tk.BOTH, expand=True)

        # Left Column: Faculty Master Details
        fac_frame = tk.LabelFrame(container, text=" Faculty Information (Table: faculty) ", font=("Segoe UI", 10, "bold"), fg="#003366", bg="#F4F6F9", padx=10, pady=8)
        fac_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Right Column: Academic Details
        aca_frame = tk.LabelFrame(container, text=" Academic Information (Table: faculty_academic) ", font=("Segoe UI", 10, "bold"), fg="#003366", bg="#F4F6F9", padx=10, pady=8)
        aca_frame.grid(row=0, column=1, sticky="nsew")

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # --- FACULTY FIELDS ---
        tk.Label(fac_frame, text="Department *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.dept_cb = ttk.Combobox(
            fac_frame,
            values=[
                "Computer Science and Engineering",
                "Electronics and Communication Engineering",
                "Electrical and Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering"
            ],
            state="readonly" if self.mode == "ADD" else "disabled",
            width=30
        )
        self.dept_cb.set("Computer Science and Engineering")
        self.dept_cb.grid(row=1, column=0, sticky=tk.EW, pady=(0, 8))
        self.dept_cb.bind("<<ComboboxSelected>>", self.on_department_changed)

        tk.Label(fac_frame, text="Faculty ID *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.fac_id_entry = ttk.Entry(fac_frame, width=30)
        self.fac_id_entry.grid(row=3, column=0, sticky=tk.EW, pady=(0, 8))
        if self.mode == "EDIT":
            self.fac_id_entry.config(state="disabled")

        tk.Label(fac_frame, text="Faculty Name *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.fac_name_entry = ttk.Entry(fac_frame, width=30)
        self.fac_name_entry.grid(row=5, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(fac_frame, text="Designation *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.desig_entry = ttk.Combobox(
            fac_frame,
            values=["Professor", "Professor & Head", "Associate Professor", "Assistant Professor (Sr. Gr.)", "Assistant Professor (Sl. Gr.)", "Assistant Professor"],
            width=30
        )
        self.desig_entry.set("Assistant Professor")
        self.desig_entry.grid(row=7, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(fac_frame, text="Email Address", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(fac_frame, width=30)
        self.email_entry.grid(row=9, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(fac_frame, text="Phone Number", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(fac_frame, width=30)
        self.phone_entry.grid(row=11, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(fac_frame, text="Joining Date (YYYY-MM-DD)", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=12, column=0, sticky=tk.W, pady=2)
        self.joining_entry = ttk.Entry(fac_frame, width=30)
        self.joining_entry.grid(row=13, column=0, sticky=tk.EW, pady=(0, 8))

        # --- ACADEMIC FIELDS ---
        tk.Label(aca_frame, text="Academic ID *", font=("Segoe UI", 9, "bold"), bg="#F4F6F9").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.aca_id_entry = ttk.Entry(aca_frame, width=30)
        self.aca_id_entry.grid(row=1, column=0, sticky=tk.EW, pady=(0, 8))
        if self.mode == "EDIT":
            self.aca_id_entry.config(state="disabled")

        tk.Label(aca_frame, text="UG Qualification", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.ug_entry = ttk.Entry(aca_frame, width=30)
        self.ug_entry.grid(row=3, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(aca_frame, text="PG Qualification", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.pg_entry = ttk.Entry(aca_frame, width=30)
        self.pg_entry.grid(row=5, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(aca_frame, text="Ph.D. Qualification", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.phd_entry = ttk.Entry(aca_frame, width=30)
        self.phd_entry.grid(row=7, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(aca_frame, text="Publication Count", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.pub_entry = ttk.Entry(aca_frame, width=30)
        self.pub_entry.grid(row=9, column=0, sticky=tk.EW, pady=(0, 8))

        tk.Label(aca_frame, text="Research Interests", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.research_txt = scrolledtext.ScrolledText(aca_frame, width=30, height=4, font=("Segoe UI", 9))
        self.research_txt.grid(row=11, column=0, sticky=tk.EW, pady=(0, 8))

        # Bottom Button Bar
        btn_bar = tk.Frame(self, bg="#F4F6F9", pady=10)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        save_txt = "SAVE FACULTY RECORD" if self.mode == "ADD" else "UPDATE FACULTY RECORD"
        btn_save = ttk.Button(btn_bar, text=save_txt, style="Primary.TButton", command=self.on_save)
        btn_save.pack(side=tk.RIGHT, padx=15)

        btn_cancel = ttk.Button(btn_bar, text="CANCEL", style="Secondary.TButton", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT)

        if self.mode == "ADD":
            self.on_department_changed()

    def on_department_changed(self, event=None):
        """Auto-generates Faculty ID and Academic ID on department change."""
        if self.mode == "ADD":
            dept = self.dept_cb.get()
            fac_id, aca_id = db.generate_next_ids(dept)

            self.fac_id_entry.delete(0, tk.END)
            self.fac_id_entry.insert(0, fac_id)

            self.aca_id_entry.delete(0, tk.END)
            self.aca_id_entry.insert(0, aca_id)

    def populate_existing_values(self):
        """Populates fields with existing data when editing."""
        p = self.profile
        self.dept_cb.set(p.get("department", ""))
        self.fac_id_entry.insert(0, p.get("faculty_id", ""))
        self.fac_name_entry.insert(0, p.get("faculty_name", ""))
        self.desig_entry.set(p.get("designation", ""))
        self.email_entry.insert(0, p.get("email", "") or "")
        self.phone_entry.insert(0, p.get("phone", "") or "")
        self.joining_entry.insert(0, str(p.get("joining_date", "")) if p.get("joining_date") else "")

        self.aca_id_entry.insert(0, p.get("academic_id", ""))
        self.ug_entry.insert(0, p.get("ug_qualification", "") or "")
        self.pg_entry.insert(0, p.get("pg_qualification", "") or "")
        self.phd_entry.insert(0, p.get("phd_qualification", "") or "")
        self.pub_entry.insert(0, str(p.get("publication_count", "")) if p.get("publication_count") is not None else "")
        self.research_txt.insert(tk.END, p.get("research_interest", "") or "")

    def on_save(self):
        """Validates inputs and commits transaction to MySQL."""
        fac_id = self.fac_id_entry.get().strip()
        fac_name = self.fac_name_entry.get().strip()
        dept = self.dept_cb.get().strip()
        desig = self.desig_entry.get().strip()
        aca_id = self.aca_id_entry.get().strip()

        # Mandatory validations
        if not fac_id or not fac_name or not dept or not desig or not aca_id:
            messagebox.showwarning("Validation Warning", "Please fill in all mandatory fields (*):\n- Faculty ID\n- Faculty Name\n- Department\n- Designation\n- Academic ID")
            return

        pub_cnt_str = self.pub_entry.get().strip()
        if pub_cnt_str and not pub_cnt_str.isdigit():
            messagebox.showwarning("Validation Warning", "Publication Count must be a valid integer number.")
            return

        fac_data = {
            "faculty_id": fac_id,
            "faculty_name": fac_name,
            "department": dept,
            "designation": desig,
            "email": self.email_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "joining_date": self.joining_entry.get().strip()
        }

        aca_data = {
            "academic_id": aca_id,
            "ug_qualification": self.ug_entry.get().strip(),
            "pg_qualification": self.pg_entry.get().strip(),
            "phd_qualification": self.phd_entry.get().strip(),
            "publication_count": pub_cnt_str,
            "research_interest": self.research_txt.get("1.0", tk.END).strip()
        }

        if self.mode == "ADD":
            success, msg = db.add_faculty_record(fac_data, aca_data)
        else:
            success, msg = db.update_faculty_record(fac_data, aca_data)

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

        name_lbl = tk.Label(header, text=p.get("faculty_name", ""), font=("Segoe UI", 14, "bold"), fg="#FFFFFF", bg="#003366")
        name_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(header, text=f"{p.get('designation', '')} | {p.get('department', '')} | ID: {p.get('faculty_id', '')}", font=("Segoe UI", 9, "bold"), fg="#D4AF37", bg="#003366")
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
            ("Joining Date:", str(p.get("joining_date")) if p.get("joining_date") else "N/A")
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
            ("Academic ID:", p.get("academic_id")),
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

        btn_edit = ttk.Button(btn_bar, text="✏️ Edit This Profile", style="Primary.TButton", command=self.on_edit)
        btn_edit.pack(side=tk.LEFT)

        btn_close = ttk.Button(btn_bar, text="CLOSE", style="Secondary.TButton", command=self.destroy)
        btn_close.pack(side=tk.RIGHT)

    def on_edit(self):
        """Switches from view profile to edit profile."""
        self.destroy()
        AddEditFacultyDialog(self.parent, mode="EDIT", profile=self.profile, callback=self.parent.refresh_data)


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
if __name__ == "__main__":
    app = CITFacultyApp()
    app.mainloop()
