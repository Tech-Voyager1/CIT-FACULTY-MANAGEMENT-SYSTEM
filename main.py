import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dotenv import load_dotenv, set_key

import db
import db_logger


def get_app_dir():
    """Returns the base directory of the running app or executable."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


load_dotenv(os.path.join(get_app_dir(), ".env"))


class CITFacultyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CIT Faculty Management System — Desktop DBMS Dashboard")
        self.geometry("1280x800")
        self.minsize(1080, 680)

        # Single-instance References for Optional Toplevel Windows
        self.live_sql_window = None
        self.adv_query_window = None

        # In-memory buffer for Live SQL history
        self.sql_history = []

        # Configure styling system
        self.configure_styles()

        # Layout Main Architecture: Left Sidebar + Right Main Area
        self.create_main_structure()

        # Subscribe to SQL Logs via db_logger
        db_logger.subscribe_to_sql(self.on_sql_activity)

        # Initialize DB Connection & Load Views
        self.after(200, self.check_and_init_db)

    def configure_styles(self):
        """Sets up modern TTK widget design tokens and theme styling."""
        self.COLOR_SIDEBAR = "#0F172A"       # Dark Navy (Slate 900)
        self.COLOR_SIDEBAR_HOVER = "#1E293B" # Slate 800
        self.COLOR_SIDEBAR_ACTIVE = "#0284C7" # Sky Blue Accent
        self.COLOR_ACCENT_GOLD = "#D4AF37"   # CIT Gold
        self.COLOR_TEAL = "#0D9488"          # Teal
        self.COLOR_BG = "#F8FAFC"            # Light Gray / Off-white background
        self.COLOR_CARD_BG = "#FFFFFF"       # Clean White Cards
        self.COLOR_CARD_BORDER = "#E2E8F0"   # Light Slate Border
        self.COLOR_TEXT_MAIN = "#0F172A"     # Dark Charcoal Text
        self.COLOR_TEXT_MUTED = "#64748B"    # Slate Text
        self.COLOR_SUCCESS = "#16A34A"       # Emerald Green
        self.COLOR_DANGER = "#DC2626"        # Crimson Red

        self.configure(bg=self.COLOR_BG)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview Styling
        self.style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=30,
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground=self.COLOR_TEXT_MAIN,
            bordercolor=self.COLOR_CARD_BORDER,
            borderwidth=1
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background=self.COLOR_SIDEBAR,
            foreground="#FFFFFF",
            padding=(8, 6),
            relief="flat"
        )
        self.style.map(
            "Treeview",
            background=[("selected", self.COLOR_SIDEBAR_ACTIVE)],
            foreground=[("selected", "#FFFFFF")]
        )

        # Button Styles
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 9, "bold"),
            background=self.COLOR_SIDEBAR,
            foreground="#FFFFFF",
            padding=(10, 6)
        )
        self.style.map("Primary.TButton", background=[("active", "#1E293B")])

        self.style.configure(
            "Accent.TButton",
            font=("Segoe UI", 9, "bold"),
            background=self.COLOR_TEAL,
            foreground="#FFFFFF",
            padding=(10, 6)
        )
        self.style.map("Accent.TButton", background=[("active", "#0F766E")])

        self.style.configure(
            "Danger.TButton",
            font=("Segoe UI", 9, "bold"),
            background=self.COLOR_DANGER,
            foreground="#FFFFFF",
            padding=(10, 6)
        )
        self.style.map("Danger.TButton", background=[("active", "#B91C1C")])

        self.style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 9),
            background="#475569",
            foreground="#FFFFFF",
            padding=(9, 5)
        )
        self.style.map("Secondary.TButton", background=[("active", "#334155")])

        self.style.configure(
            "Nav.TButton",
            font=("Segoe UI", 9, "bold"),
            background=self.COLOR_SIDEBAR,
            foreground="#E2E8F0",
            anchor="w",
            padding=(15, 10)
        )
        self.style.map(
            "Nav.TButton",
            background=[("active", self.COLOR_SIDEBAR_HOVER)],
            foreground=[("active", "#FFFFFF")]
        )

        self.style.configure("TCombobox", padding=4, font=("Segoe UI", 9))
        self.style.configure("TLabelframe", background=self.COLOR_BG, bordercolor=self.COLOR_CARD_BORDER)
        self.style.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"), foreground=self.COLOR_SIDEBAR, background=self.COLOR_BG)

    def create_main_structure(self):
        """Creates the Left Sidebar and Right Content Container layout."""
        # 1. PERSISTENT LEFT SIDEBAR
        self.sidebar_frame = tk.Frame(self, bg=self.COLOR_SIDEBAR, width=240)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        # Sidebar Header Branding
        brand_frame = tk.Frame(self.sidebar_frame, bg=self.COLOR_SIDEBAR, padx=16, pady=20)
        brand_frame.pack(fill=tk.X)

        logo_lbl = tk.Label(
            brand_frame,
            text="CIT",
            font=("Segoe UI", 22, "bold"),
            fg=self.COLOR_ACCENT_GOLD,
            bg=self.COLOR_SIDEBAR
        )
        logo_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(
            brand_frame,
            text="Faculty Management System",
            font=("Segoe UI", 9, "bold"),
            fg="#94A3B8",
            bg=self.COLOR_SIDEBAR
        )
        sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        inst_lbl = tk.Label(
            brand_frame,
            text="Coimbatore Institute of Technology",
            font=("Segoe UI", 8),
            fg="#64748B",
            bg=self.COLOR_SIDEBAR
        )
        inst_lbl.pack(anchor=tk.W, pady=(2, 10))

        sep = tk.Frame(self.sidebar_frame, bg="#1E293B", height=1)
        sep.pack(fill=tk.X, padx=16, pady=(0, 15))

        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊 Dashboard", self.show_dashboard_view),
            ("faculty", "👨‍🏫 Faculty", self.show_faculty_view),
            ("academic", "🎓 Academic Details", self.show_academic_view),
            ("adv_query", "🔍 Advanced Query", self.open_advanced_query),
            ("live_sql", "💻 SQL Activity", self.toggle_live_sql),
            ("settings", "⚙️ Settings", self.on_open_db_config),
        ]

        for key, text, cmd in nav_items:
            btn = tk.Button(
                self.sidebar_frame,
                text=text,
                font=("Segoe UI", 10, "bold"),
                fg="#CBD5E1",
                bg=self.COLOR_SIDEBAR,
                activeforeground="#FFFFFF",
                activebackground=self.COLOR_SIDEBAR_HOVER,
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2",
                command=cmd
            )
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons[key] = btn

        # Sidebar Footer
        footer_frame = tk.Frame(self.sidebar_frame, bg=self.COLOR_SIDEBAR, padx=16, pady=15)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(
            footer_frame,
            text="DBMS Project v2",
            font=("Segoe UI", 8),
            fg="#64748B",
            bg=self.COLOR_SIDEBAR
        ).pack(anchor=tk.W)

        # 2. MAIN CONTENT AREA (RIGHT SIDE)
        self.main_area = tk.Frame(self, bg=self.COLOR_BG)
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Top Header Bar
        self.header_frame = tk.Frame(self.main_area, bg=self.COLOR_CARD_BG, height=65, padx=20, pady=10, highlightbackground=self.COLOR_CARD_BORDER, highlightthickness=1)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)

        header_text_frame = tk.Frame(self.header_frame, bg=self.COLOR_CARD_BG)
        header_text_frame.pack(side=tk.LEFT)

        self.page_title_lbl = tk.Label(
            header_text_frame,
            text="Dashboard Overview",
            font=("Segoe UI", 14, "bold"),
            fg=self.COLOR_TEXT_MAIN,
            bg=self.COLOR_CARD_BG
        )
        self.page_title_lbl.pack(anchor=tk.W)

        self.page_desc_lbl = tk.Label(
            header_text_frame,
            text="Real-time faculty metrics and institutional database status",
            font=("Segoe UI", 9),
            fg=self.COLOR_TEXT_MUTED,
            bg=self.COLOR_CARD_BG
        )
        self.page_desc_lbl.pack(anchor=tk.W)

        # MySQL Status Badge
        self.db_status_lbl = tk.Label(
            self.header_frame,
            text="● MySQL: ONLINE",
            font=("Segoe UI", 10, "bold"),
            fg="#16A34A",
            bg="#F0FDF4",
            padx=12,
            pady=4,
            relief="flat"
        )
        self.db_status_lbl.pack(side=tk.RIGHT)

        # Content Views Frame Container
        self.content_container = tk.Frame(self.main_area, bg=self.COLOR_BG, padx=15, pady=12)
        self.content_container.pack(fill=tk.BOTH, expand=True)

        # Instantiate View Frames
        self.views = {
            "dashboard": DashboardView(self.content_container, self),
            "faculty": FacultyView(self.content_container, self),
            "academic": AcademicView(self.content_container, self),
        }

        # Show default view
        self.current_view_name = None
        self.show_dashboard_view()

    def set_active_nav_button(self, active_key):
        """Highlights the active sidebar navigation button."""
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.config(bg=self.COLOR_SIDEBAR_ACTIVE, fg="#FFFFFF")
            else:
                btn.config(bg=self.COLOR_SIDEBAR, fg="#CBD5E1")

    def show_dashboard_view(self):
        self.set_active_nav_button("dashboard")
        self.page_title_lbl.config(text="Dashboard Overview")
        self.page_desc_lbl.config(text="Real-time metrics and institutional faculty statistics")
        self.switch_view("dashboard")
        self.views["dashboard"].refresh()

    def show_faculty_view(self):
        self.set_active_nav_button("faculty")
        self.page_title_lbl.config(text="Faculty Management")
        self.page_desc_lbl.config(text="View, add, edit, search and inspect faculty records & profile details")
        self.switch_view("faculty")
        self.views["faculty"].refresh()

    def show_academic_view(self):
        self.set_active_nav_button("academic")
        self.page_title_lbl.config(text="Academic Details")
        self.page_desc_lbl.config(text="Manage faculty academic qualifications, Ph.D. status and research publications")
        self.switch_view("academic")
        self.views["academic"].refresh()

    def switch_view(self, view_name):
        """Hides current view frame and displays the target view frame."""
        for vname, frame in self.views.items():
            if vname == view_name:
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack_forget()
        self.current_view_name = view_name

    def toggle_live_sql(self):
        """Opens or brings the optional Live SQL Activity window to front."""
        if self.live_sql_window and self.live_sql_window.winfo_exists():
            self.live_sql_window.deiconify()
            self.live_sql_window.lift()
            self.live_sql_window.focus_force()
        else:
            self.live_sql_window = LiveSQLWindow(self)

    def open_advanced_query(self):
        """Opens or brings the optional Advanced Query Builder window to front."""
        if self.adv_query_window and self.adv_query_window.winfo_exists():
            self.adv_query_window.deiconify()
            self.adv_query_window.lift()
            self.adv_query_window.focus_force()
        else:
            self.adv_query_window = AdvancedQueryWindow(self)

    def on_sql_activity(self, log_entry):
        """Callback for db_logger. Appends SQL activity to history and updates Live SQL window."""
        self.sql_history.append(log_entry)
        if len(self.sql_history) > 50:
            self.sql_history.pop(0)

        def _update_ui():
            if self.live_sql_window and self.live_sql_window.winfo_exists():
                try:
                    self.live_sql_window.append_entry(log_entry)
                except Exception:
                    pass

        self.after(0, _update_ui)

    def check_and_init_db(self):
        """Checks DB connectivity and initializes schema/seed if needed."""
        success, msg = db.setup_database_schema()
        if success:
            self.db_status_lbl.config(text="● MySQL: ONLINE", fg="#16A34A", bg="#F0FDF4")
            if self.current_view_name:
                self.views[self.current_view_name].refresh()
        else:
            self.db_status_lbl.config(text="● MySQL: OFFLINE", fg="#DC2626", bg="#FEF2F2")
            friendly_msg = (
                "MySQL server could not be reached.\n"
                "Please make sure MySQL Server is running.\n\n"
                f"Error Details: {msg}\n\n"
                "Would you like to open Database Configuration to check/update your settings in .env?"
            )
            resp = messagebox.askyesno("MySQL Connection Failed", friendly_msg)
            if resp:
                self.on_open_db_config()

    def on_open_db_config(self):
        """Opens DB Credentials Dialog."""
        DBConfigDialog(self, callback=self.check_and_init_db)


# =================================================================
# VIEW 1: DASHBOARD OVERVIEW PAGE
# =================================================================
class DashboardView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.COLOR_BG)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # 1. SUMMARY METRICS CARDS ROW
        self.cards_frame = tk.Frame(self, bg=self.app.COLOR_BG)
        self.cards_frame.pack(fill=tk.X, side=tk.TOP, pady=(0, 15))

        self.card_widgets = {}
        departments = [
            ("Total", "TOTAL FACULTY", "#0F172A"),
            ("CSE", "CSE", "#0284C7"),
            ("ECE", "ECE", "#0D9488"),
            ("EEE", "EEE", "#D97706"),
            ("MECH", "MECHANICAL", "#7C3AED"),
            ("CIVIL", "CIVIL", "#4B5563")
        ]

        for i, (key, label, color) in enumerate(departments):
            card = tk.Frame(
                self.cards_frame,
                bg=self.app.COLOR_CARD_BG,
                highlightbackground=self.app.COLOR_CARD_BORDER,
                highlightthickness=1,
                bd=0
            )
            card.grid(row=0, column=i, padx=5, sticky="ew")
            self.cards_frame.columnconfigure(i, weight=1)

            strip = tk.Frame(card, bg=color, height=4)
            strip.pack(fill=tk.X, side=tk.TOP)

            val_lbl = tk.Label(card, text="--", font=("Segoe UI", 18, "bold"), fg=color, bg=self.app.COLOR_CARD_BG)
            val_lbl.pack(pady=(8, 0))

            title_lbl = tk.Label(card, text=label, font=("Segoe UI", 8, "bold"), fg=self.app.COLOR_TEXT_MUTED, bg=self.app.COLOR_CARD_BG)
            title_lbl.pack(pady=(0, 8))

            self.card_widgets[key] = val_lbl

        # 2. OVERVIEW CONTAINER
        overview_card = tk.LabelFrame(
            self,
            text=" Departmental Faculty Distribution & Status ",
            font=("Segoe UI", 10, "bold"),
            fg=self.app.COLOR_SIDEBAR,
            bg=self.app.COLOR_BG,
            padx=15,
            pady=12
        )
        overview_card.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            overview_card,
            columns=("dept", "total_fac", "phd_fac", "avg_exp"),
            show="headings",
            height=8
        )
        self.tree.heading("dept", text="Department Name", anchor=tk.W)
        self.tree.heading("total_fac", text="Total Faculty Count", anchor=tk.CENTER)
        self.tree.heading("phd_fac", text="Ph.D. Qualified Faculty", anchor=tk.CENTER)
        self.tree.heading("avg_exp", text="Average Experience (Years)", anchor=tk.CENTER)

        self.tree.column("dept", width=300, anchor=tk.W)
        self.tree.column("total_fac", width=160, anchor=tk.CENTER)
        self.tree.column("phd_fac", width=180, anchor=tk.CENTER)
        self.tree.column("avg_exp", width=180, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def refresh(self):
        """Refreshes summary cards and department distribution table from MySQL."""
        counts = db.get_dashboard_counts()
        for k, lbl in self.card_widgets.items():
            lbl.config(text=str(counts.get(k, 0)))

        for item in self.tree.get_children():
            self.tree.delete(item)

        dept_list = [
            "Computer Science and Engineering",
            "Electronics and Communication Engineering",
            "Electrical and Electronics Engineering",
            "Mechanical Engineering",
            "Civil Engineering"
        ]

        for dept in dept_list:
            # Query MySQL for statistics
            records = db.get_faculty_list(department_filter=dept)
            total = len(records)
            exp_vals = [r["experience_years"] for r in records if r.get("experience_years") is not None]
            avg_exp = round(sum(exp_vals) / len(exp_vals), 1) if exp_vals else "N/A"

            # Check Ph.D. counts via JOIN query
            phd_cnt = 0
            for r in records:
                p = db.get_full_faculty_profile(r["faculty_id"])
                if p and p.get("phd_qualification"):
                    phd_cnt += 1

            self.tree.insert("", tk.END, values=(dept, total, phd_cnt, avg_exp))


# =================================================================
# VIEW 2: FACULTY MANAGEMENT PAGE (TREEVIEW + RIGHT PROFILE PANEL)
# =================================================================
class FacultyView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.COLOR_BG)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # 1. TOP SEARCH & FILTER BAR
        search_card = tk.LabelFrame(
            self,
            text=" Search & Filter Faculty ",
            font=("Segoe UI", 10, "bold"),
            fg=self.app.COLOR_SIDEBAR,
            bg=self.app.COLOR_BG,
            padx=12,
            pady=8
        )
        search_card.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))

        tk.Label(search_card, text="Search Field:", font=("Segoe UI", 9, "bold"), bg=self.app.COLOR_BG).grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.search_field_cb = ttk.Combobox(
            search_card,
            values=["All Fields", "Faculty Name", "Department", "Designation", "Faculty ID"],
            state="readonly",
            width=16
        )
        self.search_field_cb.set("All Fields")
        self.search_field_cb.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)

        tk.Label(search_card, text="Keyword:", font=("Segoe UI", 9, "bold"), bg=self.app.COLOR_BG).grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.search_entry = ttk.Entry(search_card, width=20)
        self.search_entry.grid(row=0, column=3, padx=(0, 10), sticky=tk.W)
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        tk.Label(search_card, text="Department:", font=("Segoe UI", 9, "bold"), bg=self.app.COLOR_BG).grid(row=0, column=4, padx=(0, 5), sticky=tk.W)
        self.dept_filter_cb = ttk.Combobox(
            search_card,
            values=[
                "All",
                "Computer Science and Engineering",
                "Electronics and Communication Engineering",
                "Electrical and Electronics Engineering",
                "Mechanical Engineering",
                "Civil Engineering"
            ],
            state="readonly",
            width=24
        )
        self.dept_filter_cb.set("All")
        self.dept_filter_cb.grid(row=0, column=5, padx=(0, 10), sticky=tk.W)
        self.dept_filter_cb.bind("<<ComboboxSelected>>", lambda e: self.on_search())

        btn_search = ttk.Button(search_card, text="🔍 Search", style="Primary.TButton", command=self.on_search)
        btn_search.grid(row=0, column=6, padx=(0, 5))

        btn_reset = ttk.Button(search_card, text="🔄 Reset", style="Secondary.TButton", command=self.on_reset_search)
        btn_reset.grid(row=0, column=7)

        # 2. MAIN SPLIT CONTAINER: LEFT DIRECTORY (65%) | RIGHT PROFILE CARD (35%)
        split_container = tk.Frame(self, bg=self.app.COLOR_BG)
        split_container.pack(fill=tk.BOTH, expand=True)

        # LEFT SIDE: DIRECTORY TREEVIEW
        left_frame = tk.Frame(split_container, bg=self.app.COLOR_BG)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tree_card = tk.LabelFrame(
            left_frame,
            text=" Faculty Directory ",
            font=("Segoe UI", 10, "bold"),
            fg=self.app.COLOR_SIDEBAR,
            bg=self.app.COLOR_BG,
            padx=8,
            pady=8
        )
        tree_card.pack(fill=tk.BOTH, expand=True)

        cols = ("faculty_id", "faculty_name", "department", "designation", "experience_years")
        self.tree = ttk.Treeview(tree_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("faculty_id", text="Faculty ID", anchor=tk.CENTER)
        self.tree.heading("faculty_name", text="Faculty Name", anchor=tk.W)
        self.tree.heading("department", text="Department", anchor=tk.W)
        self.tree.heading("designation", text="Designation", anchor=tk.W)
        self.tree.heading("experience_years", text="Exp (Yrs)", anchor=tk.CENTER)

        self.tree.column("faculty_id", width=85, minwidth=70, anchor=tk.CENTER)
        self.tree.column("faculty_name", width=160, minwidth=120, anchor=tk.W)
        self.tree.column("department", width=180, minwidth=140, anchor=tk.W)
        self.tree.column("designation", width=150, minwidth=110, anchor=tk.W)
        self.tree.column("experience_years", width=70, minwidth=55, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(tree_card, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_card, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_card.rowconfigure(0, weight=1)
        tree_card.columnconfigure(0, weight=1)

        # Bind row selection to update right profile panel
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)
        self.tree.bind("<Double-1>", lambda e: self.on_view_full_dialog())

        # Action Toolbar below Treeview
        action_bar = tk.Frame(left_frame, bg=self.app.COLOR_BG, pady=8)
        action_bar.pack(fill=tk.X)

        btn_add = ttk.Button(action_bar, text="➕ Add Faculty", style="Primary.TButton", command=self.on_add_faculty)
        btn_add.pack(side=tk.LEFT, padx=(0, 6))

        btn_edit = ttk.Button(action_bar, text="✏️ Edit", style="Primary.TButton", command=self.on_edit_faculty)
        btn_edit.pack(side=tk.LEFT, padx=(0, 6))

        btn_del = ttk.Button(action_bar, text="🗑️ Delete", style="Danger.TButton", command=self.on_delete_faculty)
        btn_del.pack(side=tk.LEFT, padx=(0, 6))

        btn_view_modal = ttk.Button(action_bar, text="👁️ View Profile (JOIN)", style="Accent.TButton", command=self.on_view_full_dialog)
        btn_view_modal.pack(side=tk.RIGHT)

        # RIGHT SIDE: FACULTY PROFILE PANEL (REFERENCE UI MATCH)
        self.right_frame = tk.LabelFrame(
            split_container,
            text=" Faculty Profile ",
            font=("Segoe UI", 10, "bold"),
            fg=self.app.COLOR_SIDEBAR,
            bg=self.app.COLOR_BG,
            width=360,
            padx=12,
            pady=12
        )
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)

        self.create_profile_panel()

    def create_profile_panel(self):
        """Creates the right-side profile inspection card."""
        self.prof_name_lbl = tk.Label(self.right_frame, text="Select a Faculty Member", font=("Segoe UI", 13, "bold"), fg=self.app.COLOR_SIDEBAR, bg=self.app.COLOR_BG)
        self.prof_name_lbl.pack(anchor=tk.W, pady=(0, 2))

        self.prof_desig_lbl = tk.Label(self.right_frame, text="Click any row in the directory table to inspect full profile details.", font=("Segoe UI", 9, "italic"), fg=self.app.COLOR_TEXT_MUTED, bg=self.app.COLOR_BG, wraplength=330, justify="left")
        self.prof_desig_lbl.pack(anchor=tk.W, pady=(0, 10))

        # Personal Details Section
        sec1 = tk.LabelFrame(self.right_frame, text=" Personal & Contact ", font=("Segoe UI", 9, "bold"), fg=self.app.COLOR_SIDEBAR, bg=self.app.COLOR_BG, padx=8, pady=6)
        sec1.pack(fill=tk.X, pady=(0, 8))

        self.lbl_fac_id = tk.Label(sec1, text="Faculty ID: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_fac_id.pack(anchor=tk.W, pady=1)

        self.lbl_dept = tk.Label(sec1, text="Department: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN, wraplength=320, justify="left")
        self.lbl_dept.pack(anchor=tk.W, pady=1)

        self.lbl_email = tk.Label(sec1, text="Email: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_email.pack(anchor=tk.W, pady=1)

        self.lbl_phone = tk.Label(sec1, text="Phone: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_phone.pack(anchor=tk.W, pady=1)

        self.lbl_exp = tk.Label(sec1, text="Experience: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_exp.pack(anchor=tk.W, pady=1)

        # Academic Details Section (relational JOIN data)
        sec2 = tk.LabelFrame(self.right_frame, text=" Academic & Research (JOIN) ", font=("Segoe UI", 9, "bold"), fg=self.app.COLOR_SIDEBAR, bg=self.app.COLOR_BG, padx=8, pady=6)
        sec2.pack(fill=tk.BOTH, expand=True)

        self.lbl_acad_id = tk.Label(sec2, text="Academic ID: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_acad_id.pack(anchor=tk.W, pady=1)

        self.lbl_ug = tk.Label(sec2, text="UG Degree: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_ug.pack(anchor=tk.W, pady=1)

        self.lbl_pg = tk.Label(sec2, text="PG Degree: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_pg.pack(anchor=tk.W, pady=1)

        self.lbl_phd = tk.Label(sec2, text="Ph.D. Status: --", font=("Segoe UI", 9, "bold"), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEAL)
        self.lbl_phd.pack(anchor=tk.W, pady=1)

        self.lbl_pubs = tk.Label(sec2, text="Publications: --", font=("Segoe UI", 9), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MAIN)
        self.lbl_pubs.pack(anchor=tk.W, pady=1)

        tk.Label(sec2, text="Research Interests:", font=("Segoe UI", 8, "bold"), bg=self.app.COLOR_BG, fg=self.app.COLOR_TEXT_MUTED).pack(anchor=tk.W, pady=(4, 0))
        self.txt_research = scrolledtext.ScrolledText(sec2, height=3, font=("Segoe UI", 8), bg="#FFFFFF", fg=self.app.COLOR_TEXT_MAIN)
        self.txt_research.pack(fill=tk.BOTH, expand=True, pady=2)
        self.txt_research.config(state="disabled")

    def refresh(self):
        self.on_search()

    def on_search(self):
        search_field = self.search_field_cb.get()
        search_text = self.search_entry.get().strip()
        dept_filter = self.dept_filter_cb.get()

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
                str(r.get("experience_years", "")) if r.get("experience_years") is not None else ""
            ))

    def on_reset_search(self):
        self.search_field_cb.set("All Fields")
        self.search_entry.delete(0, tk.END)
        self.dept_filter_cb.set("All")
        self.on_search()

    def on_row_selected(self, event=None):
        """Updates the right-side Faculty Profile panel with full JOIN profile."""
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        faculty_id = values[0]
        profile = db.get_full_faculty_profile(faculty_id)
        if not profile:
            return

        self.prof_name_lbl.config(text=profile.get("faculty_name", "N/A"))
        self.prof_desig_lbl.config(text=f"{profile.get('designation', '')} • {profile.get('department', '')}")

        self.lbl_fac_id.config(text=f"Faculty ID: {profile.get('faculty_id', 'N/A')}")
        self.lbl_dept.config(text=f"Department: {profile.get('department', 'N/A')}")
        self.lbl_email.config(text=f"Email: {profile.get('email') or 'N/A'}")
        self.lbl_phone.config(text=f"Phone: {profile.get('phone') or 'N/A'}")
        self.lbl_exp.config(text=f"Experience: {profile.get('experience_years') or '0'} Years")

        self.lbl_acad_id.config(text=f"Academic ID: {profile.get('academic_id') or 'None'}")
        self.lbl_ug.config(text=f"UG Degree: {profile.get('ug_qualification') or 'N/A'}")
        self.lbl_pg.config(text=f"PG Degree: {profile.get('pg_qualification') or 'N/A'}")
        self.lbl_phd.config(text=f"Ph.D. Status: {profile.get('phd_qualification') or 'Not Listed'}")
        self.lbl_pubs.config(text=f"Publications: {profile.get('publication_count') if profile.get('publication_count') is not None else 0}")

        self.txt_research.config(state="normal")
        self.txt_research.delete("1.0", tk.END)
        self.txt_research.insert(tk.END, profile.get("research_interest") or "No research interest specified.")
        self.txt_research.config(state="disabled")

    def get_selected_fac_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a faculty member from the directory table.")
            return None
        vals = self.tree.item(selected[0], "values")
        return vals[0] if vals else None

    def on_add_faculty(self):
        AddFacultyDialog(self.app, mode="ADD", callback=self.refresh)

    def on_edit_faculty(self):
        fac_id = self.get_selected_fac_id()
        if not fac_id:
            return
        record = db.get_single_faculty_record(fac_id)
        if record:
            AddFacultyDialog(self.app, mode="EDIT", record=record, callback=self.refresh)

    def on_delete_faculty(self):
        fac_id = self.get_selected_fac_id()
        if not fac_id:
            return
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete Faculty ID: {fac_id}?\n\n"
            f"Note: Foreign Key CASCADE will automatically remove associated academic records."
        )
        if confirm:
            success, msg = db.delete_single_faculty(fac_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh()
            else:
                messagebox.showerror("Error", msg)

    def on_view_full_dialog(self):
        fac_id = self.get_selected_fac_id()
        if not fac_id:
            return
        profile = db.get_full_faculty_profile(fac_id)
        if profile:
            FacultyProfileDialog(self.app, profile)


# =================================================================
# VIEW 3: ACADEMIC DETAILS PAGE (FACULTY_ACADEMIC TABLE)
# =================================================================
class AcademicView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.COLOR_BG)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Top Search Card
        search_card = tk.LabelFrame(
            self,
            text=" Search & Filter Academic Records (Table: faculty_academic) ",
            font=("Segoe UI", 10, "bold"),
            fg=self.app.COLOR_SIDEBAR,
            bg=self.app.COLOR_BG,
            padx=12,
            pady=8
        )
        search_card.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))

        tk.Label(search_card, text="Search Field:", font=("Segoe UI", 9, "bold"), bg=self.app.COLOR_BG).grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.search_field_cb = ttk.Combobox(
            search_card,
            values=["All Fields", "Academic ID", "Faculty ID", "UG Qualification", "PG Qualification", "Ph.D. Qualification", "Research Interest"],
            state="readonly",
            width=22
        )
        self.search_field_cb.set("All Fields")
        self.search_field_cb.grid(row=0, column=1, padx=(0, 15), sticky=tk.W)

        tk.Label(search_card, text="Keyword:", font=("Segoe UI", 9, "bold"), bg=self.app.COLOR_BG).grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.search_entry = ttk.Entry(search_card, width=25)
        self.search_entry.grid(row=0, column=3, padx=(0, 15), sticky=tk.W)
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        btn_search = ttk.Button(search_card, text="🔍 Search", style="Primary.TButton", command=self.on_search)
        btn_search.grid(row=0, column=4, padx=(0, 5))

        btn_reset = ttk.Button(search_card, text="🔄 Reset", style="Secondary.TButton", command=self.on_reset_search)
        btn_reset.grid(row=0, column=5)

        # Table Container
        tree_card = tk.LabelFrame(
            self,
            text=" Academic Records Directory ",
            font=("Segoe UI", 10, "bold"),
            fg=self.app.COLOR_SIDEBAR,
            bg=self.app.COLOR_BG,
            padx=8,
            pady=8
        )
        tree_card.pack(fill=tk.BOTH, expand=True)

        cols = ("academic_id", "faculty_id", "ug_qualification", "pg_qualification", "phd_qualification", "publication_count", "research_interest")
        self.tree = ttk.Treeview(tree_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("academic_id", text="Academic ID", anchor=tk.CENTER)
        self.tree.heading("faculty_id", text="Faculty ID", anchor=tk.CENTER)
        self.tree.heading("ug_qualification", text="UG Qualification", anchor=tk.W)
        self.tree.heading("pg_qualification", text="PG Qualification", anchor=tk.W)
        self.tree.heading("phd_qualification", text="Ph.D. Qualification", anchor=tk.W)
        self.tree.heading("publication_count", text="Pub. Count", anchor=tk.CENTER)
        self.tree.heading("research_interest", text="Research Interest", anchor=tk.W)

        self.tree.column("academic_id", width=95, minwidth=80, anchor=tk.CENTER)
        self.tree.column("faculty_id", width=95, minwidth=80, anchor=tk.CENTER)
        self.tree.column("ug_qualification", width=140, minwidth=110, anchor=tk.W)
        self.tree.column("pg_qualification", width=170, minwidth=120, anchor=tk.W)
        self.tree.column("phd_qualification", width=180, minwidth=130, anchor=tk.W)
        self.tree.column("publication_count", width=90, minwidth=70, anchor=tk.CENTER)
        self.tree.column("research_interest", width=260, minwidth=180, anchor=tk.W)

        vsb = ttk.Scrollbar(tree_card, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_card, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_card.rowconfigure(0, weight=1)
        tree_card.columnconfigure(0, weight=1)

        # Action Toolbar
        action_bar = tk.Frame(self, bg=self.app.COLOR_BG, pady=8)
        action_bar.pack(fill=tk.X)

        btn_add = ttk.Button(action_bar, text="➕ Add Academic Record", style="Accent.TButton", command=self.on_add_academic)
        btn_add.pack(side=tk.LEFT, padx=(0, 8))

        btn_edit = ttk.Button(action_bar, text="✏️ Edit Record", style="Primary.TButton", command=self.on_edit_academic)
        btn_edit.pack(side=tk.LEFT, padx=(0, 8))

        btn_del = ttk.Button(action_bar, text="🗑️ Delete Record", style="Danger.TButton", command=self.on_delete_academic)
        btn_del.pack(side=tk.LEFT, padx=(0, 8))

        btn_refresh = ttk.Button(action_bar, text="🔄 Refresh", style="Secondary.TButton", command=self.refresh)
        btn_refresh.pack(side=tk.RIGHT)

    def refresh(self):
        self.on_search()

    def on_search(self):
        search_field = self.search_field_cb.get()
        search_text = self.search_entry.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

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
                str(r["publication_count"]) if r["publication_count"] is not None else "",
                r["research_interest"] or ""
            ))

    def on_reset_search(self):
        self.search_field_cb.set("All Fields")
        self.search_entry.delete(0, tk.END)
        self.on_search()

    def get_selected_acad_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select an academic record from the table.")
            return None
        vals = self.tree.item(selected[0], "values")
        return vals[0] if vals else None

    def on_add_academic(self):
        AddAcademicDialog(self.app, mode="ADD", callback=self.refresh)

    def on_edit_academic(self):
        aca_id = self.get_selected_acad_id()
        if not aca_id:
            return
        record = db.get_single_academic_record(aca_id)
        if record:
            AddAcademicDialog(self.app, mode="EDIT", record=record, callback=self.refresh)

    def on_delete_academic(self):
        aca_id = self.get_selected_acad_id()
        if not aca_id:
            return
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete Academic ID: {aca_id}?"
        )
        if confirm:
            success, msg = db.delete_single_academic(aca_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh()
            else:
                messagebox.showerror("Error", msg)


# =================================================================
# OPTIONAL TOPLEVEL WINDOW 1: LIVE SQL ACTIVITY MONITOR
# =================================================================
class LiveSQLWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Live SQL Activity — Database Query Monitor")
        self.geometry("800x540")
        self.minsize(580, 360)
        self.resizable(True, True)
        self.configure(bg="#0F172A")

        self.create_widgets()
        self.load_history()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        header = tk.Frame(self, bg="#1E293B", height=45, padx=15, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header,
            text="LIVE SQL ACTIVITY",
            font=("Consolas", 11, "bold"),
            fg="#38BDF8",
            bg="#1E293B"
        )
        title_lbl.pack(side=tk.LEFT)

        status_lbl = tk.Label(
            header,
            text="● LIVE",
            font=("Segoe UI", 9, "bold"),
            fg="#4ADE80",
            bg="#1E293B"
        )
        status_lbl.pack(side=tk.LEFT, padx=(10, 0))

        btn_close = ttk.Button(header, text="CLOSE", style="Secondary.TButton", command=self.on_close)
        btn_close.pack(side=tk.RIGHT, padx=(5, 0))

        btn_clear = ttk.Button(header, text="CLEAR LOG", style="Secondary.TButton", command=self.clear_log)
        btn_clear.pack(side=tk.RIGHT)

        self.sql_text = scrolledtext.ScrolledText(
            self,
            bg="#0F172A",
            fg="#E2E8F0",
            insertbackground="#FFFFFF",
            font=("Consolas", 10),
            padx=12,
            pady=10
        )
        self.sql_text.pack(fill=tk.BOTH, expand=True)

        self.sql_text.tag_config("time", foreground="#94A3B8", font=("Consolas", 9, "italic"))
        self.sql_text.tag_config("sql", foreground="#FACC15", font=("Consolas", 10, "bold"))
        self.sql_text.tag_config("success", foreground="#4ADE80", font=("Consolas", 9, "bold"))
        self.sql_text.tag_config("error", foreground="#F87171", font=("Consolas", 9, "bold"))
        self.sql_text.tag_config("info", foreground="#38BDF8", font=("Consolas", 9))
        self.sql_text.tag_config("divider", foreground="#334155")

        self.sql_text.config(state="disabled")

    def load_history(self):
        for entry in self.parent.sql_history:
            self.append_entry(entry)

    def append_entry(self, log_entry):
        self.sql_text.config(state="normal")

        self.sql_text.insert(tk.END, "--------------------------------------------------------------------------------\n", "divider")
        self.sql_text.insert(tk.END, f"[{log_entry['time']}]\n", "time")
        self.sql_text.insert(tk.END, f"{log_entry['sql']}\n\n", "sql")

        if log_entry['success']:
            self.sql_text.insert(tk.END, "✓ Query executed successfully\n", "success")
            if log_entry.get('rows') is not None:
                self.sql_text.insert(tk.END, f"Rows affected / returned: {log_entry['rows']}\n", "info")
            if log_entry.get('is_cascade'):
                self.sql_text.insert(tk.END, "CASCADE: Associated records updated/deleted via Foreign Key constraint.\n", "info")
        else:
            self.sql_text.insert(tk.END, "✗ Query execution failed\n", "error")
            self.sql_text.insert(tk.END, f"Error details: {log_entry['error']}\n", "error")

        self.sql_text.insert(tk.END, "\n")
        self.sql_text.see(tk.END)
        self.sql_text.config(state="disabled")

    def clear_log(self):
        self.parent.sql_history.clear()
        self.sql_text.config(state="normal")
        self.sql_text.delete("1.0", tk.END)
        self.sql_text.config(state="disabled")

    def on_close(self):
        self.parent.live_sql_window = None
        self.destroy()


# =================================================================
# OPTIONAL TOPLEVEL WINDOW 2: ADVANCED QUERY BUILDER
# =================================================================
class AdvancedQueryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Advanced Query Builder — DBMS Visual Builder")
        self.geometry("860x660")
        self.minsize(720, 480)
        self.resizable(True, True)
        self.configure(bg="#F8FAFC")

        self.conditions = []
        self.fac_fields = ['faculty_id', 'faculty_name', 'department', 'designation', 'email', 'phone', 'experience_years']
        self.aca_fields = ['academic_id', 'ug_qualification', 'pg_qualification', 'phd_qualification', 'research_interest', 'publication_count']

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
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        header = tk.Frame(self, bg="#0F172A", height=50, padx=15, pady=10)
        header.pack(fill=tk.X, side=tk.TOP)

        tk.Label(
            header,
            text="ADVANCED SQL QUERY BUILDER",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg="#0F172A"
        ).pack(side=tk.LEFT)

        tk.Label(
            header,
            text="Visual Condition Builder & Multi-Table Filtering",
            font=("Segoe UI", 9),
            fg="#D4AF37",
            bg="#0F172A"
        ).pack(side=tk.LEFT, padx=(15, 0))

        top_frame = tk.Frame(self, bg="#F8FAFC", padx=15, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Query Type:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").pack(side=tk.LEFT)
        self.qtype_cb = ttk.Combobox(top_frame, values=["Records", "Count"], state="readonly", width=12)
        self.qtype_cb.set("Records")
        self.qtype_cb.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(top_frame, text="Table Scope:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").pack(side=tk.LEFT)
        self.table_scope_cb = ttk.Combobox(top_frame, values=["Faculty", "Faculty Academic"], state="readonly", width=18)
        self.table_scope_cb.set("Faculty")
        self.table_scope_cb.pack(side=tk.LEFT, padx=(5, 15))
        self.table_scope_cb.bind("<<ComboboxSelected>>", self.on_scope_change)

        self.cond_group = tk.LabelFrame(
            self,
            text=" Filtering Conditions ",
            font=("Segoe UI", 10, "bold"),
            bg="#F8FAFC",
            fg="#0F172A",
            padx=10,
            pady=10
        )
        self.cond_group.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.canvas = tk.Canvas(self.cond_group, bg="#F8FAFC", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.cond_group, orient="vertical", command=self.canvas.yview)
        self.cond_list_frame = tk.Frame(self.canvas, bg="#F8FAFC")

        self.cond_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.cond_list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        btn_add_cond = ttk.Button(self.cond_group, text="➕ ADD CONDITION", style="Primary.TButton", command=self.add_condition_row)
        btn_add_cond.pack(anchor=tk.W, pady=(8, 0))

        sort_frame = tk.LabelFrame(
            self,
            text=" Sorting (ORDER BY) ",
            font=("Segoe UI", 10, "bold"),
            bg="#F8FAFC",
            fg="#0F172A",
            padx=10,
            pady=8
        )
        sort_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(sort_frame, text="Sort By:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=0, column=0, padx=5, pady=5)
        self.sort_field_cb = ttk.Combobox(sort_frame, state="readonly", width=25)
        self.sort_field_cb.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(sort_frame, text="Order:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=0, column=2, padx=(15, 5), pady=5)
        self.sort_order_cb = ttk.Combobox(sort_frame, values=["ASC", "DESC"], state="readonly", width=10)
        self.sort_order_cb.set("ASC")
        self.sort_order_cb.grid(row=0, column=3, padx=5, pady=5)

        btn_bar = tk.Frame(self, bg="#F8FAFC", pady=10, padx=15)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_run = ttk.Button(btn_bar, text="▶ RUN QUERY", style="Accent.TButton", command=self.run_query)
        btn_run.pack(side=tk.RIGHT)

        btn_clear = ttk.Button(btn_bar, text="🧹 CLEAR CONDITIONS", style="Secondary.TButton", command=self.clear_conditions)
        btn_clear.pack(side=tk.RIGHT, padx=10)

        btn_close = ttk.Button(btn_bar, text="✖ CLOSE", style="Secondary.TButton", command=self.on_close)
        btn_close.pack(side=tk.RIGHT)

        self.on_scope_change()
        self.add_condition_row()

    def _on_mousewheel(self, event):
        if self.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _fetch_distinct(self, table, column):
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
        field = row['field_cb'].get()
        op = row['op_cb'].get()
        val_cb = row['val_entry']

        if op in ('IS NULL', 'IS NOT NULL'):
            val_cb.config(state='disabled', values=[])
            return

        options = self.VALUE_OPTIONS.get(field, [])
        val_cb.config(values=options)
        val_cb.config(state='normal')

    def add_condition_row(self):
        row_frame = tk.Frame(self.cond_list_frame, bg="#F8FAFC")
        row_frame.pack(fill=tk.X, pady=3, expand=True)

        scope = self.table_scope_cb.get()
        fields = self.fac_fields if scope == "Faculty" else self.fac_fields + self.aca_fields

        logic_cb = ttk.Combobox(row_frame, values=["AND", "OR"], state="readonly", width=6)
        if not self.conditions:
            logic_cb.set("")
            logic_cb.config(state="disabled")
        else:
            logic_cb.set("AND")
        logic_cb.pack(side=tk.LEFT, padx=3)

        field_cb = ttk.Combobox(row_frame, values=fields, state="readonly", width=20)
        field_cb.set(fields[0])
        field_cb.pack(side=tk.LEFT, padx=3)

        op_cb = ttk.Combobox(row_frame, values=["=", "!=", ">", "<", ">=", "<=", "LIKE", "IS NULL", "IS NOT NULL"], state="readonly", width=12)
        op_cb.set("=")
        op_cb.pack(side=tk.LEFT, padx=3)

        initial_opts = self.VALUE_OPTIONS.get(fields[0], [])
        val_cb = ttk.Combobox(row_frame, values=initial_opts, width=28)
        val_cb.pack(side=tk.LEFT, padx=3)

        btn_del = ttk.Button(row_frame, text="✖", style="Danger.TButton", width=3, command=lambda f=row_frame: self.remove_condition_row(f))
        btn_del.pack(side=tk.LEFT, padx=5)

        row_dict = {
            'frame': row_frame,
            'logic_cb': logic_cb,
            'field_cb': field_cb,
            'op_cb': op_cb,
            'val_entry': val_cb,
        }
        self.conditions.append(row_dict)

        def on_field_change(event, row=row_dict):
            self._refresh_val_widget(row)
            row['val_entry'].set('')
        field_cb.bind("<<ComboboxSelected>>", on_field_change)

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
        scope = self.table_scope_cb.get()
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
            return

        # Push results to active view
        if scope == "Faculty Academic" or (result and 'academic_id' in result[0]):
            self.parent.show_academic_view()
            view = self.parent.views["academic"]
            view.tree.delete(*view.tree.get_children())
            for r in result:
                view.tree.insert("", tk.END, values=(
                    r.get("academic_id", ""),
                    r.get("faculty_id", ""),
                    r.get("ug_qualification", "") or "",
                    r.get("pg_qualification", "") or "",
                    r.get("phd_qualification", "") or "",
                    str(r.get("publication_count", "")) if r.get("publication_count") is not None else "",
                    r.get("research_interest", "") or ""
                ))
        else:
            self.parent.show_faculty_view()
            view = self.parent.views["faculty"]
            view.tree.delete(*view.tree.get_children())
            for r in result:
                view.tree.insert("", tk.END, values=(
                    r.get("faculty_id", ""),
                    r.get("faculty_name", ""),
                    r.get("department", ""),
                    r.get("designation", ""),
                    str(r.get("experience_years", "")) if r.get("experience_years") is not None else ""
                ))

    def on_close(self):
        try:
            self.canvas.unbind_all("<MouseWheel>")
        except Exception:
            pass
        self.parent.adv_query_window = None
        self.destroy()


# =================================================================
# FORM DIALOG 1: FACULTY FORM (Add / Edit)
# =================================================================
class AddFacultyDialog(tk.Toplevel):
    def __init__(self, parent, mode="ADD", record=None, callback=None):
        super().__init__(parent)
        self.mode = mode
        self.record = record or {}
        self.callback = callback

        title_txt = "Add New Faculty Record" if mode == "ADD" else f"Edit Faculty Record: {record.get('faculty_id', '')}"
        self.title(title_txt)
        self.geometry("490x510")
        self.resizable(False, False)
        self.configure(bg="#F8FAFC")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        if mode == "EDIT":
            self.populate_fields()

    def create_widgets(self):
        header = tk.Frame(self, bg="#0F172A", height=45, padx=15, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        title_str = "ADD FACULTY RECORD (Table: faculty)" if self.mode == "ADD" else f"EDIT FACULTY: {self.record.get('faculty_id', '')}"
        tk.Label(header, text=title_str, font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#0F172A").pack(anchor=tk.W)

        form = tk.Frame(self, bg="#F8FAFC", padx=20, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Department *", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=0, column=0, sticky=tk.W, pady=4)
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
        self.dept_cb.grid(row=0, column=1, pady=4, sticky=tk.W)
        self.dept_cb.bind("<<ComboboxSelected>>", self.on_dept_changed)

        tk.Label(form, text="Faculty ID *", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.id_entry = ttk.Entry(form, width=34)
        self.id_entry.grid(row=1, column=1, pady=4, sticky=tk.W)
        if self.mode == "EDIT":
            self.id_entry.config(state="disabled")

        tk.Label(form, text="Faculty Name *", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.name_entry = ttk.Entry(form, width=34)
        self.name_entry.grid(row=2, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Designation *", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.desig_cb = ttk.Combobox(
            form,
            values=["Professor", "Professor & Head", "Associate Professor", "Assistant Professor (Sr. Gr.)", "Assistant Professor (Sl. Gr.)", "Assistant Professor"],
            width=32
        )
        self.desig_cb.set("Assistant Professor")
        self.desig_cb.grid(row=3, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Email Address", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=4, column=0, sticky=tk.W, pady=4)
        self.email_entry = ttk.Entry(form, width=34)
        self.email_entry.grid(row=4, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Phone Number", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=5, column=0, sticky=tk.W, pady=4)
        self.phone_entry = ttk.Entry(form, width=34)
        self.phone_entry.grid(row=5, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Experience (Years)", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=6, column=0, sticky=tk.W, pady=4)
        self.exp_entry = ttk.Entry(form, width=34)
        self.exp_entry.grid(row=6, column=1, pady=4, sticky=tk.W)

        btn_bar = tk.Frame(self, bg="#F8FAFC", pady=12, padx=20)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_save = ttk.Button(btn_bar, text="💾 SAVE RECORD", style="Primary.TButton", command=self.on_save)
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
        self.id_entry.config(state="normal")
        self.id_entry.insert(0, r.get("faculty_id", ""))
        self.id_entry.config(state="disabled")
        self.name_entry.insert(0, r.get("faculty_name", ""))
        self.desig_cb.set(r.get("designation", ""))
        self.email_entry.insert(0, r.get("email", "") or "")
        self.phone_entry.insert(0, r.get("phone", "") or "")
        self.exp_entry.insert(0, str(r.get("experience_years", "")) if r.get("experience_years") is not None else "")

    def on_save(self):
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
# FORM DIALOG 2: FACULTY ACADEMIC FORM (Add / Edit)
# =================================================================
class AddAcademicDialog(tk.Toplevel):
    def __init__(self, parent, mode="ADD", record=None, callback=None):
        super().__init__(parent)
        self.mode = mode
        self.record = record or {}
        self.callback = callback

        title_txt = "Add Faculty Academic Record" if mode == "ADD" else f"Edit Academic Record: {record.get('academic_id', '')}"
        self.title(title_txt)
        self.geometry("530x570")
        self.resizable(False, False)
        self.configure(bg="#F8FAFC")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        if mode == "EDIT":
            self.populate_fields()

    def create_widgets(self):
        header = tk.Frame(self, bg="#0D9488", height=45, padx=15, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        title_str = "ADD ACADEMIC RECORD (Table: faculty_academic)" if self.mode == "ADD" else f"EDIT ACADEMIC RECORD: {self.record.get('academic_id', '')}"
        tk.Label(header, text=title_str, font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#0D9488").pack(anchor=tk.W)

        form = tk.Frame(self, bg="#F8FAFC", padx=20, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Academic ID *", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.aca_id_entry = ttk.Entry(form, width=34)
        self.aca_id_entry.grid(row=0, column=1, pady=4, sticky=tk.W)
        if self.mode == "EDIT":
            self.aca_id_entry.config(state="disabled")
        else:
            next_aca = db.generate_next_academic_id()
            self.aca_id_entry.insert(0, next_aca)

        tk.Label(form, text="Faculty ID (Foreign Key) *", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=1, column=0, sticky=tk.W, pady=4)
        
        existing_fac_ids = db.get_all_faculty_ids()
        self.fac_id_cb = ttk.Combobox(form, values=existing_fac_ids, width=32)
        if existing_fac_ids:
            self.fac_id_cb.set(existing_fac_ids[0])
        self.fac_id_cb.grid(row=1, column=1, pady=4, sticky=tk.W)
        if self.mode == "EDIT":
            self.fac_id_cb.config(state="disabled")

        tk.Label(form, text="UG Qualification", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.ug_entry = ttk.Entry(form, width=34)
        self.ug_entry.grid(row=2, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="PG Qualification", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.pg_entry = ttk.Entry(form, width=34)
        self.pg_entry.grid(row=3, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Ph.D. Qualification", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=4, column=0, sticky=tk.W, pady=4)
        self.phd_entry = ttk.Entry(form, width=34)
        self.phd_entry.grid(row=4, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Publication Count", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=5, column=0, sticky=tk.W, pady=4)
        self.pub_entry = ttk.Entry(form, width=34)
        self.pub_entry.grid(row=5, column=1, pady=4, sticky=tk.W)

        tk.Label(form, text="Research Interest", font=("Segoe UI", 9), bg="#F8FAFC", fg="#0F172A").grid(row=6, column=0, sticky=tk.NW, pady=4)
        self.research_txt = scrolledtext.ScrolledText(form, width=32, height=4, font=("Segoe UI", 9))
        self.research_txt.grid(row=6, column=1, pady=4, sticky=tk.W)

        btn_bar = tk.Frame(self, bg="#F8FAFC", pady=12, padx=20)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_save = ttk.Button(btn_bar, text="💾 SAVE RECORD", style="Accent.TButton", command=self.on_save)
        btn_save.pack(side=tk.RIGHT)

        btn_cancel = ttk.Button(btn_bar, text="CANCEL", style="Secondary.TButton", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=10)

    def populate_fields(self):
        r = self.record
        self.aca_id_entry.config(state="normal")
        self.aca_id_entry.delete(0, tk.END)
        self.aca_id_entry.insert(0, r.get("academic_id", ""))
        self.aca_id_entry.config(state="disabled")

        self.fac_id_cb.config(state="normal")
        self.fac_id_cb.set(r.get("faculty_id", ""))
        self.fac_id_cb.config(state="disabled")

        self.ug_entry.insert(0, r.get("ug_qualification", "") or "")
        self.pg_entry.insert(0, r.get("pg_qualification", "") or "")
        self.phd_entry.insert(0, r.get("phd_qualification", "") or "")
        self.pub_entry.insert(0, str(r.get("publication_count", "")) if r.get("publication_count") is not None else "")
        self.research_txt.insert(tk.END, r.get("research_interest", "") or "")

    def on_save(self):
        if self.mode == "EDIT":
            aca_id = self.record.get("academic_id", "").strip()
            fac_id = self.record.get("faculty_id", "").strip()
        else:
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
# DIALOG 3: FULL FACULTY PROFILE DIALOG (RELATIONAL JOIN)
# =================================================================
class FacultyProfileDialog(tk.Toplevel):
    def __init__(self, parent, profile):
        super().__init__(parent)
        self.profile = profile
        self.parent = parent

        self.title(f"Full Faculty Profile — {profile.get('faculty_name', '')} ({profile.get('faculty_id', '')})")
        self.geometry("700x620")
        self.resizable(False, False)
        self.configure(bg="#F8FAFC")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        p = self.profile

        header = tk.Frame(self, bg="#0F172A", height=65, padx=20, pady=12)
        header.pack(fill=tk.X, side=tk.TOP)

        name_lbl = tk.Label(header, text=p.get("faculty_name", "N/A"), font=("Segoe UI", 15, "bold"), fg="#FFFFFF", bg="#0F172A")
        name_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(header, text=f"{p.get('designation', '')} | {p.get('department', '')} | Faculty ID: {p.get('faculty_id', '')}", font=("Segoe UI", 9, "bold"), fg="#D4AF37", bg="#0F172A")
        sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        body = tk.Frame(self, bg="#F8FAFC", padx=18, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        fac_group = tk.LabelFrame(body, text=" PERSONAL & CONTACT INFORMATION (Table: faculty) ", font=("Segoe UI", 10, "bold"), fg="#0F172A", bg="#F8FAFC", padx=12, pady=8)
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
            lbl = tk.Label(fac_group, text=label, font=("Segoe UI", 9, "bold"), fg="#64748B", bg="#F8FAFC")
            lbl.grid(row=r*2, column=c*2, sticky=tk.W, padx=5, pady=(2, 0))

            val_lbl = tk.Label(fac_group, text=val, font=("Segoe UI", 10), fg="#0F172A", bg="#F8FAFC")
            val_lbl.grid(row=r*2+1, column=c*2, sticky=tk.W, padx=5, pady=(0, 6))

        fac_group.columnconfigure(0, weight=1)
        fac_group.columnconfigure(2, weight=1)

        aca_group = tk.LabelFrame(body, text=" ACADEMIC QUALIFICATIONS & RESEARCH (Table: faculty_academic) ", font=("Segoe UI", 10, "bold"), fg="#0F172A", bg="#F8FAFC", padx=12, pady=8)
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
            lbl = tk.Label(aca_group, text=label, font=("Segoe UI", 9, "bold"), fg="#64748B", bg="#F8FAFC")
            lbl.grid(row=r*2, column=c*2, sticky=tk.W, padx=5, pady=(2, 0))

            val_lbl = tk.Label(aca_group, text=val, font=("Segoe UI", 10), fg="#0F172A", bg="#F8FAFC")
            val_lbl.grid(row=r*2+1, column=c*2, sticky=tk.W, padx=5, pady=(0, 6))

        aca_group.columnconfigure(0, weight=1)
        aca_group.columnconfigure(2, weight=1)

        tk.Label(aca_group, text="Research Interests:", font=("Segoe UI", 9, "bold"), fg="#64748B", bg="#F8FAFC").grid(row=6, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(4, 0))
        res_txt = scrolledtext.ScrolledText(aca_group, height=3, font=("Segoe UI", 9), bg="#FFFFFF", fg="#0F172A")
        res_txt.insert(tk.END, p.get("research_interest") or "N/A")
        res_txt.config(state="disabled")
        res_txt.grid(row=7, column=0, columnspan=4, sticky="ew", padx=5, pady=(2, 6))

        btn_bar = tk.Frame(self, bg="#F8FAFC", pady=10, padx=15)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_close = ttk.Button(btn_bar, text="CLOSE", style="Secondary.TButton", command=self.destroy)
        btn_close.pack(side=tk.RIGHT)


# =================================================================
# DIALOG 4: DB CONFIGURATION DIALOG
# =================================================================
class DBConfigDialog(tk.Toplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback

        self.title("MySQL Database Connection Configuration")
        self.geometry("460x390")
        self.resizable(False, False)
        self.configure(bg="#F8FAFC")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#0F172A", height=45, padx=15, pady=8)
        header.pack(fill=tk.X, side=tk.TOP)

        tk.Label(header, text="MYSQL DATABASE CONFIGURATION", font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#0F172A").pack(anchor=tk.W)

        form = tk.Frame(self, bg="#F8FAFC", padx=20, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="Database Host:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.host_entry = ttk.Entry(form, width=28)
        self.host_entry.insert(0, os.getenv("DB_HOST", "localhost"))
        self.host_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Database Port:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.port_entry = ttk.Entry(form, width=28)
        self.port_entry.insert(0, os.getenv("DB_PORT", "3306"))
        self.port_entry.grid(row=1, column=1, pady=5)

        tk.Label(form, text="MySQL Username:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_entry = ttk.Entry(form, width=28)
        self.user_entry.insert(0, os.getenv("DB_USER", "root"))
        self.user_entry.grid(row=2, column=1, pady=5)

        tk.Label(form, text="MySQL Password:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.pass_entry = ttk.Entry(form, width=28, show="*")
        self.pass_entry.insert(0, os.getenv("DB_PASSWORD", ""))
        self.pass_entry.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Database Name:", font=("Segoe UI", 9, "bold"), bg="#F8FAFC", fg="#0F172A").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form, width=28)
        self.name_entry.insert(0, os.getenv("DB_NAME", "cit_faculty_db"))
        self.name_entry.grid(row=4, column=1, pady=5)

        btn_bar = tk.Frame(self, bg="#F8FAFC", pady=12, padx=20)
        btn_bar.pack(fill=tk.X, side=tk.BOTTOM)

        btn_save = ttk.Button(btn_bar, text="🔌 SAVE & CONNECT", style="Primary.TButton", command=self.on_save)
        btn_save.pack(side=tk.RIGHT)

        btn_cancel = ttk.Button(btn_bar, text="CANCEL", style="Secondary.TButton", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=10)

    def on_save(self):
        env_file = os.path.join(get_app_dir(), ".env")

        set_key(env_file, "DB_HOST", self.host_entry.get().strip())
        set_key(env_file, "DB_PORT", self.port_entry.get().strip())
        set_key(env_file, "DB_USER", self.user_entry.get().strip())
        set_key(env_file, "DB_PASSWORD", self.pass_entry.get().strip())
        set_key(env_file, "DB_NAME", self.name_entry.get().strip())

        load_dotenv(env_file, override=True)

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
