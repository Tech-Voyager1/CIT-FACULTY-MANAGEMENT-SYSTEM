import os

def main():
    main_file = r"d:\Downloads\DBMS Lab Project\CIT Faculty Management System\main.py"
    with open(main_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. setup_treeview_columns
    content = content.replace(
        'cols = ("faculty_id", "faculty_name", "department", "designation", "email", "phone", "joining_date")',
        'cols = ("faculty_id", "faculty_name", "department", "designation", "email", "phone", "joining_date", "experience_years")'
    )
    content = content.replace(
        'self.tree.heading("joining_date", text="Joining Date", anchor=tk.CENTER)',
        'self.tree.heading("joining_date", text="Joining Date", anchor=tk.CENTER)\n            self.tree.heading("experience_years", text="Experience", anchor=tk.CENTER)'
    )
    content = content.replace(
        'self.tree.column("joining_date", width=100, minwidth=80, anchor=tk.CENTER)',
        'self.tree.column("joining_date", width=100, minwidth=80, anchor=tk.CENTER)\n            self.tree.column("experience_years", width=80, minwidth=60, anchor=tk.CENTER)'
    )

    # 2. on_search
    content = content.replace(
        'str(r["joining_date"]) if r["joining_date"] else ""',
        'str(r["joining_date"]) if r["joining_date"] else "",\n                    str(r.get("experience_years", "")) if r.get("experience_years") is not None else ""'
    )

    # 3. AddFacultyDialog.create_widgets
    content = content.replace(
        'tk.Label(form, text="Joining Date (YYYY-MM-DD)", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=6, column=0, sticky=tk.W, pady=3)',
        'tk.Label(form, text="Joining Date (YYYY-MM-DD)", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=6, column=0, sticky=tk.W, pady=3)'
    )
    content = content.replace(
        'self.joining_entry = ttk.Entry(form, width=34)\n        self.joining_entry.grid(row=6, column=1, pady=3, sticky=tk.W)',
        'self.joining_entry = ttk.Entry(form, width=34)\n        self.joining_entry.grid(row=6, column=1, pady=3, sticky=tk.W)\n\n        tk.Label(form, text="Experience (Years)", font=("Segoe UI", 9), bg="#F4F6F9").grid(row=7, column=0, sticky=tk.W, pady=3)\n        self.exp_entry = ttk.Entry(form, width=34)\n        self.exp_entry.grid(row=7, column=1, pady=3, sticky=tk.W)'
    )

    # 4. AddFacultyDialog.populate_fields
    content = content.replace(
        'self.joining_entry.insert(0, str(r.get("joining_date", "")) if r.get("joining_date") else "")',
        'self.joining_entry.insert(0, str(r.get("joining_date", "")) if r.get("joining_date") else "")\n        self.exp_entry.insert(0, str(r.get("experience_years", "")) if r.get("experience_years") is not None else "")'
    )

    # 5. AddFacultyDialog.on_save
    content = content.replace(
        'fac_data = {\n            "faculty_id": fac_id,',
        'exp_val = self.exp_entry.get().strip()\n        if exp_val and not exp_val.isdigit():\n            messagebox.showwarning("Validation Warning", "Experience must be a valid non-negative integer.")\n            return\n        fac_data = {\n            "faculty_id": fac_id,'
    )
    content = content.replace(
        '"joining_date": self.joining_entry.get().strip()\n        }',
        '"joining_date": self.joining_entry.get().strip(),\n            "experience_years": exp_val if exp_val else None\n        }'
    )

    # 6. FacultyProfileDialog
    content = content.replace(
        '("Joining Date:", str(p.get("joining_date")) if p.get("joining_date") else "N/A")',
        '("Joining Date:", str(p.get("joining_date")) if p.get("joining_date") else "N/A"),\n            ("Experience (Years):", str(p.get("experience_years")) if p.get("experience_years") is not None else "N/A")'
    )

    # 7. Action buttons -> Advanced Query
    content = content.replace(
        'self.btn_live_sql = ttk.Button(action_frame, text="[ LIVE SQL: OFF ]", style="Secondary.TButton", command=self.toggle_live_sql)',
        'self.btn_live_sql = ttk.Button(action_frame, text="[ LIVE SQL: OFF ]", style="Secondary.TButton", command=self.toggle_live_sql)\n        self.btn_live_sql.pack(side=tk.RIGHT, padx=(0, 10))\n\n        self.btn_adv_query = ttk.Button(action_frame, text="🔍 ADVANCED QUERY", style="Accent.TButton", command=self.open_advanced_query)\n        self.btn_adv_query.pack(side=tk.RIGHT, padx=(0, 10))\n        # removing pack call below to prevent duplicate'
    )
    content = content.replace(
        'self.btn_live_sql.pack(side=tk.RIGHT, padx=(0, 10))\n\n        self.btn_adv_query = ttk.Button(action_frame, text="🔍 ADVANCED QUERY", style="Accent.TButton", command=self.open_advanced_query)\n        self.btn_adv_query.pack(side=tk.RIGHT, padx=(0, 10))\n        # removing pack call below to prevent duplicate\n\n        btn_refresh =',
        'self.btn_adv_query = ttk.Button(action_frame, text="🔍 ADVANCED QUERY", style="Accent.TButton", command=self.open_advanced_query)\n        self.btn_adv_query.pack(side=tk.RIGHT, padx=(0, 10))\n        btn_refresh ='
    )
    
    # Add open_advanced_query definition
    content = content.replace(
        'def toggle_live_sql(self):',
        'def open_advanced_query(self):\n        AdvancedQueryDialog(self)\n\n    def toggle_live_sql(self):'
    )

    # Add AdvancedQueryDialog class
    advanced_query_class = """
# =================================================================
# DIALOG 5: ADVANCED QUERY BUILDER
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
        self.fac_fields = ['faculty_id', 'faculty_name', 'department', 'designation', 'email', 'phone', 'joining_date', 'experience_years']
        self.aca_fields = ['academic_id', 'ug_qualification', 'pg_qualification', 'phd_qualification', 'research_interest', 'publication_count']
        
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
        
        val_entry = ttk.Entry(row_frame, width=25)
        val_entry.pack(side=tk.LEFT, padx=2)
        
        btn_del = ttk.Button(row_frame, text="X", width=3, command=lambda f=row_frame: self.remove_condition_row(f))
        btn_del.pack(side=tk.LEFT, padx=5)
        
        def on_op_change(event, entry=val_entry, cb=op_cb):
            if cb.get() in ["IS NULL", "IS NOT NULL"]:
                entry.config(state="disabled")
            else:
                entry.config(state="normal")
        op_cb.bind("<<ComboboxSelected>>", on_op_change)
        
        self.conditions.append({
            'frame': row_frame,
            'logic_cb': logic_cb,
            'field_cb': field_cb,
            'op_cb': op_cb,
            'val_entry': val_entry
        })
        
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
        sort_by = self.sort_field_cb.get()
        sort_order = self.sort_order_cb.get()
        
        if not sort_by:
            sort_by = None
            
        success, result = db.execute_advanced_query(qtype, cond_data, sort_by, sort_order)
        
        if not success:
            messagebox.showerror("Query Failed", f"Execution failed:\\n{result}")
            return
            
        if qtype == "Count":
            messagebox.showinfo("Query Result", f"Total matching faculty: {result}")
        else:
            # We will show the results in the main Treeview by clearing and inserting.
            # However, for join results, the columns might differ.
            # For simplicity in this project, we'll configure the main window's active table
            # and inject results manually, or we can just show a messagebox for now.
            # But the prompt says "display matching records in the Treeview."
            self.parent.tree.delete(*self.parent.tree.get_children())
            
            # Decide cols based on what's returned
            if result and 'academic_id' in result[0]:
                self.parent.active_table = "faculty_academic"
                self.parent.setup_treeview_columns()
                for r in result:
                    self.parent.tree.insert("", tk.END, values=(
                        r.get("academic_id", ""),
                        r.get("faculty_id", ""),
                        r.get("ug_qualification", ""),
                        r.get("pg_qualification", ""),
                        r.get("phd_qualification", ""),
                        r.get("research_interest", ""),
                        str(r.get("publication_count", "")) if r.get("publication_count") is not None else ""
                    ))
            else:
                self.parent.active_table = "faculty"
                self.parent.setup_treeview_columns()
                for r in result:
                    self.parent.tree.insert("", tk.END, values=(
                        r.get("faculty_id", ""),
                        r.get("faculty_name", ""),
                        r.get("department", ""),
                        r.get("designation", ""),
                        r.get("email", ""),
                        r.get("phone", ""),
                        str(r.get("joining_date", "")) if r.get("joining_date") else "",
                        str(r.get("experience_years", "")) if r.get("experience_years") is not None else ""
                    ))
            self.parent.status_var.set(f"Advanced Query returned {len(result)} records.")
            self.destroy()
"""
    if "class AdvancedQueryDialog" not in content:
        content += advanced_query_class

    with open(main_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("main.py patched successfully.")

if __name__ == "__main__":
    main()
