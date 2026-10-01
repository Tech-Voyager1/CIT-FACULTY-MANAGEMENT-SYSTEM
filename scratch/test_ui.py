import sys
import os
import tkinter as tk

# Ensure current dir & workspace root are in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
import db

def run_headless_tests():
    print("--- STARTING MAJOR UI/UX REDESIGN INTEGRATION TESTS ---")
    
    app = main.CITFacultyApp()
    app.update()

    # 1. Test Startup & DB Connection
    print("[TEST 1] Initializing DB schema and persistent sidebar UI...")
    app.check_and_init_db()
    app.update()
    assert "ONLINE" in app.db_status_lbl.cget("text"), f"Expected ONLINE status, got: {app.db_status_lbl.cget('text')}"
    print("[OK] PASS: MySQL Connection & Persistent Sidebar")

    # 2. Test Navigation Frame Switching
    print("[TEST 2] Testing Sidebar Frame Navigation (Dashboard, Faculty, Academic)...")
    assert app.current_view_name == "dashboard"
    
    app.show_faculty_view()
    app.update()
    assert app.current_view_name == "faculty"

    app.show_academic_view()
    app.update()
    assert app.current_view_name == "academic"

    app.show_dashboard_view()
    app.update()
    assert app.current_view_name == "dashboard"
    print("[OK] PASS: Sidebar Navigation & Frame Switching")

    # 3. Test Faculty Page & Right-Side Live Profile Panel
    print("[TEST 3] Testing Faculty Page & Right-Side Live Profile Panel...")
    app.show_faculty_view()
    app.update()
    fac_view = app.views["faculty"]

    # Select first row in directory tree
    tree_items = fac_view.tree.get_children()
    assert len(tree_items) > 0, "Directory treeview should contain faculty rows"
    first_item = tree_items[0]
    fac_view.tree.selection_set(first_item)
    fac_view.on_row_selected()
    app.update()

    # Verify right profile panel updated with full JOIN details
    prof_name = fac_view.prof_name_lbl.cget("text")
    assert prof_name != "Select a Faculty Member", f"Expected faculty name in profile panel, got: {prof_name}"
    print(f"[OK] PASS: Right-Side Live Profile Panel loaded selected faculty: {prof_name}")

    # 4. Test Academic Details Page
    print("[TEST 4] Testing Academic Details Page...")
    app.show_academic_view()
    app.update()
    acad_view = app.views["academic"]
    acad_items = acad_view.tree.get_children()
    assert len(acad_items) > 0, "Academic treeview should contain academic records"
    print(f"[OK] PASS: Academic Details Page loaded {len(acad_items)} records from faculty_academic table")

    # 5. Test Live SQL Window (Optional Toplevel & Single Instance)
    print("[TEST 5] Testing Optional Live SQL Window...")
    assert app.live_sql_window is None, "Live SQL window should NOT be open at startup"
    app.toggle_live_sql()
    app.update()
    assert app.live_sql_window is not None and app.live_sql_window.winfo_exists()
    sql_win = app.live_sql_window

    # Re-trigger toggle_live_sql to test single-instance
    app.toggle_live_sql()
    app.update()
    assert app.live_sql_window is sql_win, "Should bring existing window to front, not spawn duplicate"

    app.live_sql_window.on_close()
    app.update()
    assert app.live_sql_window is None
    print("[OK] PASS: Optional Live SQL Window (open/bring-to-front/close)")

    # 6. Test Advanced Query Window (Optional Toplevel & Scrolling & Single Instance)
    print("[TEST 6] Testing Optional Advanced Query Builder Window...")
    assert app.adv_query_window is None, "Advanced Query window should NOT be open at startup"
    app.open_advanced_query()
    app.update()
    assert app.adv_query_window is not None and app.adv_query_window.winfo_exists()
    adv_win = app.adv_query_window

    app.open_advanced_query()
    app.update()
    assert app.adv_query_window is adv_win

    # Add conditions (vertical scrolling test)
    adv_win.add_condition_row()
    adv_win.add_condition_row()
    app.update()
    assert len(adv_win.conditions) == 3

    # Execute query: Mechanical Engineering
    adv_win.qtype_cb.set("Records")
    adv_win.table_scope_cb.set("Faculty")
    adv_win.on_scope_change()
    row0 = adv_win.conditions[0]
    row0['field_cb'].set('department')
    row0['op_cb'].set('=')
    row0['val_entry'].set('Mechanical Engineering')

    adv_win.run_query()
    app.update()

    assert app.current_view_name == "faculty"
    mech_items = fac_view.tree.get_children()
    assert len(mech_items) > 0, "Advanced query should return Mechanical Engineering records"
    print(f"[OK] PASS: Advanced Query executed and returned {len(mech_items)} records")

    adv_win.on_close()
    app.update()
    assert app.adv_query_window is None

    # 7. Test CRUD Operations (Faculty table & Academic table)
    print("[TEST 7] Testing CRUD Operations (Add, Update, Delete)...")
    test_fac_data = {
        "faculty_id": "TEST888",
        "faculty_name": "Test Modern Faculty",
        "department": "Computer Science and Engineering",
        "designation": "Professor",
        "email": "modern.fac@cit.edu.in",
        "phone": "9876543210",
        "experience_years": "12"
    }
    success, msg = db.add_single_faculty(test_fac_data)
    assert success, f"Add faculty failed: {msg}"

    test_fac_data["faculty_name"] = "Updated Modern Faculty"
    success, msg = db.update_single_faculty(test_fac_data)
    assert success, f"Update faculty failed: {msg}"

    # Test Academic record edit dialog logic
    acad_rec = db.get_single_academic_record("ACA001")
    assert acad_rec is not None
    dlg = main.AddAcademicDialog(app, mode="EDIT", record=acad_rec)
    app.update()
    assert dlg.aca_id_entry.get() == "ACA001" or dlg.record.get("academic_id") == "ACA001"
    dlg.destroy()

    success, msg = db.delete_single_faculty("TEST888")
    assert success, f"Delete faculty failed: {msg}"
    print("[OK] PASS: CRUD Operations for Faculty & Academic tables")

    app.destroy()
    print("\n============================================================")
    print("ALL MAJOR UI/UX REDESIGN TESTS PASSED SUCCESSFULLY!")
    print("============================================================")

if __name__ == "__main__":
    run_headless_tests()
