"""
setup_database_gui.py
GUI-based one-shot database installer for CIT Faculty Management System.
Run this ONCE on any machine that has MySQL installed.
"""
import os, sys, threading, tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

SCHEMA_SQL = """
CREATE DATABASE IF NOT EXISTS `cit_faculty_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `cit_faculty_db`;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `faculty_academic`;
DROP TABLE IF EXISTS `faculty`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `faculty` (
    `faculty_id` VARCHAR(20) NOT NULL,
    `faculty_name` VARCHAR(100) NOT NULL,
    `department` VARCHAR(100) NOT NULL,
    `designation` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) DEFAULT NULL,
    `phone` VARCHAR(20) DEFAULT NULL,
    `experience_years` INT DEFAULT NULL,
    PRIMARY KEY (`faculty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `faculty_academic` (
    `academic_id` VARCHAR(20) NOT NULL,
    `faculty_id` VARCHAR(20) NOT NULL,
    `ug_qualification` VARCHAR(100) DEFAULT NULL,
    `pg_qualification` VARCHAR(150) DEFAULT NULL,
    `phd_qualification` VARCHAR(150) DEFAULT NULL,
    `research_interest` TEXT DEFAULT NULL,
    `publication_count` INT DEFAULT NULL,
    PRIMARY KEY (`academic_id`),
    CONSTRAINT `fk_fac_aca` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

FACULTY_ROWS = [
    ("CSE001","Dr. K. Amshakala","Computer Science and Engineering","Professor","amshakala@cit.edu.in","9000000001",18),
    ("CSE002","Dr. A. Saran Kumar","Computer Science and Engineering","Associate Professor","sarankumar.a@cit.edu.in","9000000002",15),
    ("CSE003","Dr. M. Mohanapriya","Computer Science and Engineering","Associate Professor","mohanapriya.m@cit.edu.in","9000000003",15),
    ("CSE004","Dr. S. P. Abirami","Computer Science and Engineering","Associate Professor","abirami.sp@cit.edu.in","9000000004",15),
    ("CSE005","Dr. A. Priyadharshini","Computer Science and Engineering","Associate Professor","priyadharshini.a@cit.edu.in","9000000005",15),
    ("CSE006","Dr. G. Karthikeyan","Computer Science and Engineering","Assistant Professor (Sr. Gr.)","karthikeyan.g@cit.edu.in","9000000006",11),
    ("ECE001","Dr. A. Rajeswari","Electronics and Communication Engineering","Principal & Professor","principal@cit.edu.in","0422-2574071",20),
    ("ECE002","Dr. M. Poongothai","Electronics and Communication Engineering","Professor & Head","hodece@cit.edu.in","0422-2574072",20),
    ("ECE003","Dr. G. Puvaneswari","Electronics and Communication Engineering","Associate Professor","puvaneswari@cit.edu.in","9000000009",15),
    ("ECE004","Dr. P. Muthu Subramanian","Electronics and Communication Engineering","Associate Professor","dpo@cit.edu.in","9000000010",15),
    ("ECE005","Dr. T. Balakumaran","Electronics and Communication Engineering","Assistant Professor (Sr. Gr.)","balakumaran.t@cit.edu.in","9000000011",11),
    ("ECE006","Dr. M. Ramya","Electronics and Communication Engineering","Assistant Professor (Sl. Gr.)","ramya.m@cit.edu.in","9000000012",11),
    ("ECE007","Ms. Harini","Electronics and Communication Engineering","Assistant Professor","harini@cit.edu.in","9000000031",5),
    ("EEE001","Dr. E. Chandira Sekaran","Electrical and Electronics Engineering","Professor & Head","hodeee@cit.edu.in","0422-2574073",20),
    ("EEE002","Dr. S. Elango","Electrical and Electronics Engineering","Associate Professor","elango.s@cit.edu.in","9000000014",15),
    ("EEE003","Dr. A. Kavithamani","Electrical and Electronics Engineering","Associate Professor","kavithamani.a@cit.edu.in","9000000015",15),
    ("EEE004","Dr. M. L. Merlin Sajini","Electrical and Electronics Engineering","Associate Professor","merlinsajini@cit.edu.in","9000000016",15),
    ("EEE005","Dr. B. Vasanthan","Electrical and Electronics Engineering","Assistant Professor (Sl. Gr.)","vasanthan.b@cit.edu.in","9000000017",11),
    ("EEE006","Dr. Y. Hamsavarthini","Electrical and Electronics Engineering","Assistant Professor (Sr. Gr.)","hamsavarthini.y@cit.edu.in","9000000018",11),
    ("MECH001","Dr. Rajesh Ranganathan","Mechanical Engineering","Professor & Head","hodmech@cit.edu.in","0422-2574074",20),
    ("MECH002","Dr. N. Rajam Ramaswamy","Mechanical Engineering","Associate Professor","rajamramaswamy@cit.edu.in","9000000020",15),
    ("MECH003","Dr. G. Suresh Kannan","Mechanical Engineering","Associate Professor","sureshkannan@cit.edu.in","9000000021",15),
    ("MECH004","Dr. G. Sivakumar","Mechanical Engineering","Associate Professor","vmsivakumar@cit.edu.in","9000000022",15),
    ("MECH005","Mr. P. Ramakrishnan","Mechanical Engineering","Assistant Professor","ramakrishnan.p@cit.edu.in","9000000023",11),
    ("MECH006","Dr. M. Velliangiri","Mechanical Engineering","Assistant Professor","velliangiri.m@cit.edu.in","9000000024",11),
    ("CIVIL001","Dr. R. Sathyanarayan Sridhar","Civil Engineering","Professor & Head","sathyanarayan@cit.edu.in","0422-2574075",20),
    ("CIVIL002","Dr. P. Vinayagam","Civil Engineering","Professor","vinayagam.p@cit.edu.in","9000000026",18),
    ("CIVIL003","Dr. S. Shanmuga Priya","Civil Engineering","Professor","shanmugapriya@cit.edu.in","9000000027",18),
    ("CIVIL004","Dr. M. P. Muthuraj","Civil Engineering","Associate Professor","muthuraj@cit.edu.in","9000000028",15),
    ("CIVIL005","Ms. M. Hannah Angelin","Civil Engineering","Assistant Professor (Sr. Gr.)","hannahangelin.m@cit.edu.in","9000000029",11),
    ("CIVIL006","Dr. M. Kaarthik","Civil Engineering","Assistant Professor (Sr. Gr.)","kaarthik@cit.edu.in","9585579885",11),
]

ACADEMIC_ROWS = [
    ("ACA001","CSE001","B.E. (CSE)","M.E. (CSE)","Ph.D. (CSE)","Data Integration, Semantics Extraction, Data Mining, Image Processing",28),
    ("ACA002","CSE002","B.E. (IT)","M.E. (CSE), MBA (HR)","Ph.D. (Information and Communication Engineering)","Data Analytics, Machine Learning, HR Analytics",50),
    ("ACA003","CSE003","B.E. (CSE)","M.E. (CSE)","Ph.D. (CSE)","Network Security, Machine Learning, IoT, Data Science",22),
    ("ACA004","CSE004","B.E. (CSE)","M.E. (CSE)","Ph.D. (CSE)","Machine Learning, Deep Learning, Cloud Computing, Big Data Analytics",19),
    ("ACA005","CSE005","B.E. (CSE)","M.E. (CSE)","Ph.D. (Information and Communication Engineering)","Wireless Networks, Cognitive Radio Networks, Machine Learning",17),
    ("ACA006","CSE006","B.E. (CSE)","M.E. (CSE)","Ph.D. (CSE)","IoT, Blockchain Applications, Smart Contracts",14),
    ("ACA007","ECE001","B.E. (ECE)","M.E. (Communication Systems)","Ph.D. (ECE)","Signal Processing, Wireless Networks, Embedded Systems",65),
    ("ACA008","ECE002","B.E. (ECE)","M.E. (Communication Systems)","Ph.D. (ECE)","VLSI Design, Wireless Sensor Networks, IoT Systems",42),
    ("ACA009","ECE003","B.E. (ECE)","M.E. (Applied Electronics)","Ph.D. (ECE)","Intruder Identification Systems, Image Processing, Security",25),
    ("ACA010","ECE004","B.E. (ECE)","M.E. (Communication Systems)","Ph.D. (ECE)","RF Communications, Microwave Antennas, Wireless Networks",20),
    ("ACA011","ECE005","B.E. (ECE)","M.E. (Applied Electronics)","Ph.D. (ECE)","Medical Image Processing, Machine Learning in Healthcare",16),
    ("ACA012","ECE006","B.E. (ECE)","M.E. (VLSI Design)","Ph.D. (ECE)","Low Power VLSI, Nano-electronics, Micro-sensors",12),
    ("ACA013","ECE007","B.E. (ECE)","M.E. (Communication Systems)",None,"Signal Processing, Embedded Systems, IoT",5),
    ("ACA014","EEE001","B.E. (EEE)","M.E. (Power Systems)","Ph.D. (EEE)","Power System Optimization, Smart Grids, Renewable Energy Integration",48),
    ("ACA015","EEE002","B.E. (EEE)","M.E. (Power Electronics and Drives)","Ph.D. (EEE)","Power Converters, Motor Control, Electric Vehicles",28),
    ("ACA016","EEE003","B.E. (EEE)","M.E. (Electrical Machines)","Ph.D. (EEE)","Special Machines, Wind Energy Conversion, Solar PV Systems",21),
    ("ACA017","EEE004","B.E. (EEE)","M.E. (Power Electronics)","Ph.D. (EEE)","Dielectric Materials, Insulation Diagnostics, High Voltage DC",18),
    ("ACA018","EEE005","B.E. (EEE)","M.E. (Power Systems)","Ph.D. (EEE)","Electricity Markets, Power Quality, Microgrids",15),
    ("ACA019","EEE006","B.E. (EEE)","M.E. (Embedded Systems)","Ph.D. (EEE)","Smart Grid Security, Energy Harvesting, IoT Sensors",11),
    ("ACA020","MECH001","B.E. (Mechanical)","M.E. (Manufacturing Engineering)","Ph.D. (Loughborough University, UK)","Rapid Prototyping, RFID Integration, Prosthesis Design, Lean Systems",55),
    ("ACA021","MECH002","B.E. (Mechanical)","M.E. (Industrial Engineering)","Ph.D. (Mechanical Engineering)","Manufacturing System Simulation, Production Planning, Ergonomics",30),
    ("ACA022","MECH003","B.E. (Mechanical)","M.E. (Thermal Engineering)","Ph.D. (Mechanical Engineering)","Metal Matrix Composites, Materials Characterization, Machining",24),
    ("ACA023","MECH004","B.E. (Mechanical)","M.E. (Advanced Manufacturing Tech)","Ph.D. (Anna University)","Surface Engineering, Friction Stir Welding, Machining Optimization",26),
    ("ACA024","MECH005","B.E. (Mechanical)","M.Tech. (Mechanical)",None,"Computational Fluid Dynamics, Heat Exchanger Optimization",8),
    ("ACA025","MECH006","B.E. (Mechanical)","M.E. (CAD/CAM)","Ph.D. (Mechanical Engineering)","Biomechanics, Finite Element Modeling, Composite Design",12),
    ("ACA026","CIVIL001","B.E. (Civil)","M.E. (Foundation Engineering)","Ph.D. (Civil Engineering)","Ground Improvement Techniques, Deep Foundations, Soil-Structure Interaction",38),
    ("ACA027","CIVIL002","B.E. (Civil)","M.E. (Structural Engineering)","Ph.D. (Civil Engineering)","High Performance Concrete, Seismic Resilience, Retrofitting",32),
    ("ACA028","CIVIL003","B.E. (Civil)","M.E. (Environmental Engineering)","Ph.D. (Civil Engineering)","Industrial Wastewater Treatment, Membrane Technology, Environmental Impact",27),
    ("ACA029","CIVIL004","B.E. (Civil)","M.E. (Structural Engineering)","Ph.D. (Civil Engineering)","Composite Plates, Cold-formed Steel, Pavement Materials",20),
    ("ACA030","CIVIL005","B.E. (Civil)","M.E. (Structural Engineering)",None,"Sustainable Concrete, Waste Utilization in Concrete",9),
    ("ACA031","CIVIL006","B.E. (Civil)","M.E. (Structural Engineering)","Ph.D. (Civil Engineering)","Non-Destructive Testing (NDT), Recycled Aggregates, Cold-Formed Steel",24),
]

C = {
    "bg":"#0F172A","card":"#1E293B","accent":"#6366F1","accent2":"#818CF8",
    "success":"#22C55E","error":"#EF4444","warn":"#F59E0B",
    "text":"#F1F5F9","subtext":"#94A3B8","border":"#334155","entry_bg":"#0F172A",
}
FT = ("Segoe UI",18,"bold"); FL=("Segoe UI",10); FB=("Segoe UI",10,"bold")
FM=("Consolas",9); FBTN=("Segoe UI",11,"bold"); FS=("Segoe UI",8)

class SetupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CIT Faculty Management — Database Setup")
        self.configure(bg=C["bg"])
        self.resizable(False,False)
        w,h=620,700
        self.geometry(f"{w}x{h}")
        self.update_idletasks()
        x=(self.winfo_screenwidth()-w)//2; y=(self.winfo_screenheight()-h)//2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self._build()

    def _build(self):
        tk.Frame(self,bg=C["accent"],height=6).pack(fill="x")
        tf=tk.Frame(self,bg=C["bg"],pady=18); tf.pack(fill="x",padx=30)
        tk.Label(tf,text="🎓  CIT Faculty Management System",font=FT,bg=C["bg"],fg=C["text"]).pack(anchor="w")
        tk.Label(tf,text="Database Setup Installer  •  Run once before launching the app",font=FS,bg=C["bg"],fg=C["subtext"]).pack(anchor="w")

        card=tk.Frame(self,bg=C["card"],highlightthickness=1,highlightbackground=C["border"])
        card.pack(fill="x",padx=30,pady=(0,10))
        tk.Label(card,text="MySQL Connection Settings",font=FB,bg=C["card"],fg=C["accent2"]).pack(anchor="w",padx=20,pady=(14,4))
        ttk.Separator(card).pack(fill="x",padx=20,pady=(0,10))

        ff=tk.Frame(card,bg=C["card"]); ff.pack(fill="x",padx=20,pady=(0,14))
        self.vs={}
        style=ttk.Style(self); style.theme_use("clam")
        style.configure("S.TEntry",fieldbackground=C["entry_bg"],foreground=C["text"],bordercolor=C["border"],insertcolor=C["text"],relief="flat")
        style.map("S.TEntry",fieldbackground=[("focus","#1E3A5F")],bordercolor=[("focus",C["accent"])])

        for lbl,key,dflt,sec in [("Host","DB_HOST","localhost",False),("Port","DB_PORT","3306",False),("Username","DB_USER","root",False),("Password","DB_PASSWORD","",True)]:
            r=tk.Frame(ff,bg=C["card"]); r.pack(fill="x",pady=4)
            tk.Label(r,text=lbl,font=FL,bg=C["card"],fg=C["subtext"],width=12,anchor="w").pack(side="left")
            v=tk.StringVar(value=dflt); self.vs[key]=v
            ttk.Entry(r,textvariable=v,show="*" if sec else "",style="S.TEntry",font=FM).pack(side="left",fill="x",expand=True,ipady=6)

        info=tk.Frame(self,bg="#0C2340",highlightthickness=1,highlightbackground="#1E3A5F")
        info.pack(fill="x",padx=30,pady=(0,10))
        tk.Label(info,text="ℹ  What this installer does:",font=FB,bg="#0C2340",fg=C["accent2"]).pack(anchor="w",padx=16,pady=(12,4))
        for s in ["1.  Connect to your MySQL server","2.  Create database  cit_faculty_db","3.  Create tables: faculty  and  faculty_academic","4.  Insert 31 faculty + 31 academic records (all departments)","5.  Write .env file with your credentials  →  launch main app"]:
            tk.Label(info,text=s,font=FS,bg="#0C2340",fg=C["text"]).pack(anchor="w",padx=24)
        tk.Label(info,text="",bg="#0C2340").pack()

        lf=tk.Frame(self,bg=C["bg"]); lf.pack(fill="both",expand=True,padx=30,pady=(0,8))
        tk.Label(lf,text="Setup Log",font=FB,bg=C["bg"],fg=C["subtext"]).pack(anchor="w")
        self.log=tk.Text(lf,height=8,font=FM,bg=C["card"],fg=C["text"],relief="flat",state="disabled",highlightthickness=1,highlightbackground=C["border"],insertbackground=C["text"])
        self.log.pack(fill="both",expand=True)

        style.configure("TProgressbar",troughcolor=C["card"],background=C["accent"])
        self.prog=ttk.Progressbar(lf,mode="indeterminate"); self.prog.pack(fill="x",pady=(4,0))

        bf=tk.Frame(self,bg=C["bg"]); bf.pack(fill="x",padx=30,pady=(0,16))
        self.rbtn=tk.Button(bf,text="▶  Run Setup",font=FBTN,bg=C["accent"],fg="white",activebackground=C["accent2"],activeforeground="white",relief="flat",bd=0,padx=20,pady=10,cursor="hand2",command=self._start)
        self.rbtn.pack(side="left")
        tk.Button(bf,text="✕  Exit",font=FBTN,bg=C["border"],fg=C["text"],activebackground="#475569",activeforeground="white",relief="flat",bd=0,padx=20,pady=10,cursor="hand2",command=self.destroy).pack(side="right")

        self.sv=tk.StringVar(value="Ready — fill in your MySQL credentials and click Run Setup.")
        tk.Label(self,textvariable=self.sv,font=FS,bg=C["bg"],fg=C["subtext"]).pack(pady=(0,6))

    def _log(self,msg,tag="n"):
        self.log.configure(state="normal")
        self.log.insert("end",msg+"\n",tag)
        for t,col in [("n",C["text"]),("s",C["success"]),("e",C["error"]),("w",C["warn"]),("a",C["accent2"])]:
            self.log.tag_config(t,foreground=col)
        self.log.see("end"); self.log.configure(state="disabled"); self.update_idletasks()

    def _start(self):
        self.rbtn.configure(state="disabled"); self.prog.start(12)
        self._log("="*55,"a"); self._log("  CIT Faculty Management — Database Setup","a"); self._log("="*55,"a")
        threading.Thread(target=self._run,daemon=True).start()

    def _run(self):
        host=self.vs["DB_HOST"].get().strip(); user=self.vs["DB_USER"].get().strip(); pwd=self.vs["DB_PASSWORD"].get()
        try: port=int(self.vs["DB_PORT"].get().strip())
        except: self.after(0,self._fail,"Invalid port — must be a number (default 3306)."); return

        self._log(f"\n[1/5]  Connecting to MySQL at {host}:{port} as '{user}' …")
        try:
            conn=mysql.connector.connect(host=host,port=port,user=user,password=pwd,connection_timeout=10)
        except mysql.connector.Error as e:
            self.after(0,self._fail,f"Cannot connect to MySQL:\n{e.msg}\n\nCheck:\n• MySQL server is running\n• Host/Port/Username/Password are correct"); return
        self._log("       Connected ✓","s")
        cur=conn.cursor()

        self._log("\n[2/5]  Creating database …")
        try:
            for stmt in SCHEMA_SQL.split(";"):
                s=stmt.strip()
                if s: cur.execute(s)
            conn.commit()
        except mysql.connector.Error as e:
            self.after(0,self._fail,f"Schema failed: {e.msg}"); cur.close(); conn.close(); return
        self._log("       Tables created ✓","s")

        self._log("\n[3/5]  Clearing old data …")
        try:
            cur.execute("USE `cit_faculty_db`")
            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            cur.execute("TRUNCATE TABLE `faculty_academic`")
            cur.execute("TRUNCATE TABLE `faculty`")
            cur.execute("SET FOREIGN_KEY_CHECKS=1")
            conn.commit()
        except mysql.connector.Error as e:
            self._log(f"       [warn] {e.msg}","w")

        self._log("\n[4/5]  Inserting 31 faculty records …")
        try:
            cur.executemany(
                "INSERT INTO `faculty` (faculty_id,faculty_name,department,designation,email,phone,experience_years) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                FACULTY_ROWS
            )
            conn.commit()
        except mysql.connector.Error as e:
            self.after(0,self._fail,f"faculty insert failed: {e.msg}"); cur.close(); conn.close(); return
        self._log("       faculty rows inserted ✓","s")

        self._log("       Inserting 31 academic records …")
        try:
            cur.executemany(
                "INSERT INTO `faculty_academic` (academic_id,faculty_id,ug_qualification,pg_qualification,phd_qualification,research_interest,publication_count) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                ACADEMIC_ROWS
            )
            conn.commit()
        except mysql.connector.Error as e:
            self.after(0,self._fail,f"faculty_academic insert failed: {e.msg}"); cur.close(); conn.close(); return
        self._log("       academic rows inserted ✓","s")

        self._log("\n[5/5]  Verifying …")
        cur.execute("SELECT COUNT(*) FROM `faculty`"); fac=cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM `faculty_academic`"); aca=cur.fetchone()[0]
        cur.close(); conn.close()
        self._log(f"       faculty          : {fac} rows","s")
        self._log(f"       faculty_academic  : {aca} rows","s")

        self._log("\n[+]   Writing .env …")
        try:
            base=os.path.dirname(sys.executable if getattr(sys,"frozen",False) else os.path.abspath(__file__))
            env_path=os.path.join(base,".env")
            with open(env_path,"w") as f:
                f.write(f"DB_HOST='{host}'\nDB_PORT='{port}'\nDB_USER='{user}'\nDB_PASSWORD='{pwd}'\nDB_NAME='cit_faculty_db'\n")
            self._log(f"       .env saved → {env_path}","s")
        except Exception as ex:
            self._log(f"       [warn] Could not write .env: {ex}","w")

        self.after(0,self._success,fac,aca)

    def _success(self,fac,aca):
        self.prog.stop()
        self._log("\n"+"="*55,"s"); self._log("  ✅  SETUP COMPLETE!","s")
        self._log(f"  faculty: {fac}  |  faculty_academic: {aca}","s")
        self._log("  You can now launch  CIT_Faculty_Management.exe","s"); self._log("="*55,"s")
        self.rbtn.configure(state="normal",text="✓  Done — Launch App?",bg=C["success"],command=self._launch)
        self.sv.set("✅  Setup complete! Click 'Launch App' or close this window.")

    def _fail(self,msg):
        self.prog.stop(); self._log("\n[ERROR] "+msg,"e")
        self.rbtn.configure(state="normal"); self.sv.set("❌  Setup failed. See error above.")
        messagebox.showerror("Setup Failed",msg,parent=self)

    def _launch(self):
        base=os.path.dirname(sys.executable if getattr(sys,"frozen",False) else os.path.abspath(__file__))
        exe=os.path.join(base,"CIT_Faculty_Management.exe")
        if os.path.exists(exe):
            import subprocess; subprocess.Popen([exe]); self.destroy()
        else:
            messagebox.showinfo("Not found",f"CIT_Faculty_Management.exe not found in:\n{base}\n\nPlease run it manually.",parent=self)

if __name__=="__main__":
    SetupApp().mainloop()
