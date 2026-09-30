-- ============================================================
-- CIT FACULTY MANAGEMENT SYSTEM - SEED DATA IMPORT
-- Generated from verified data/faculty.csv & data/faculty_academic.csv
-- ============================================================

USE cit_faculty_db;

-- Disable FK checks temporarily during bulk insert
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE faculty_academic;
TRUNCATE TABLE faculty;

SET FOREIGN_KEY_CHECKS = 1;

-- Insert records into faculty
INSERT INTO faculty (faculty_id, faculty_name, department, designation, email, phone, joining_date) VALUES
('CSE001', 'Dr. K. Amshakala', 'Computer Science and Engineering', 'Professor', 'amshakala@cit.edu.in', NULL, NULL),
('CSE002', 'Dr. A. Saran Kumar', 'Computer Science and Engineering', 'Associate Professor', 'sarankumar.a@cit.edu.in', NULL, NULL),
('CSE003', 'Dr. M. Mohanapriya', 'Computer Science and Engineering', 'Associate Professor', 'mohanapriya.m@cit.edu.in', NULL, NULL),
('CSE004', 'Dr. S. P. Abirami', 'Computer Science and Engineering', 'Associate Professor', 'abirami.sp@cit.edu.in', NULL, NULL),
('CSE005', 'Dr. A. Priyadharshini', 'Computer Science and Engineering', 'Associate Professor', 'priyadharshini.a@cit.edu.in', NULL, NULL),
('CSE006', 'Dr. G. Karthikeyan', 'Computer Science and Engineering', 'Assistant Professor (Sr. Gr.)', 'karthikeyan.g@cit.edu.in', NULL, NULL),
('ECE001', 'Dr. A. Rajeswari', 'Electronics and Communication Engineering', 'Principal & Professor', 'principal@cit.edu.in', '0422-2574071', NULL),
('ECE002', 'Dr. M. Poongothai', 'Electronics and Communication Engineering', 'Professor & Head', 'hodece@cit.edu.in', '0422-2574072', NULL),
('ECE003', 'Dr. G. Puvaneswari', 'Electronics and Communication Engineering', 'Associate Professor', 'puvaneswari@cit.edu.in', NULL, NULL),
('ECE004', 'Dr. P. Muthu Subramanian', 'Electronics and Communication Engineering', 'Associate Professor', 'dpo@cit.edu.in', NULL, NULL),
('ECE005', 'Dr. T. Balakumaran', 'Electronics and Communication Engineering', 'Assistant Professor (Sr. Gr.)', 'balakumaran.t@cit.edu.in', NULL, NULL),
('ECE006', 'Dr. M. Ramya', 'Electronics and Communication Engineering', 'Assistant Professor (Sl. Gr.)', 'ramya.m@cit.edu.in', NULL, NULL),
('EEE001', 'Dr. E. Chandira Sekaran', 'Electrical and Electronics Engineering', 'Professor & Head', 'hodeee@cit.edu.in', '0422-2574073', NULL),
('EEE002', 'Dr. S. Elango', 'Electrical and Electronics Engineering', 'Associate Professor', 'elango.s@cit.edu.in', NULL, NULL),
('EEE003', 'Dr. A. Kavithamani', 'Electrical and Electronics Engineering', 'Associate Professor', 'kavithamani.a@cit.edu.in', NULL, NULL),
('EEE004', 'Dr. M. L. Merlin Sajini', 'Electrical and Electronics Engineering', 'Associate Professor', 'merlinsajini@cit.edu.in', NULL, NULL),
('EEE005', 'Dr. B. Vasanthan', 'Electrical and Electronics Engineering', 'Assistant Professor (Sl. Gr.)', 'vasanthan.b@cit.edu.in', NULL, NULL),
('EEE006', 'Dr. Y. Hamsavarthini', 'Electrical and Electronics Engineering', 'Assistant Professor (Sr. Gr.)', 'hamsavarthini.y@cit.edu.in', NULL, NULL),
('MECH001', 'Dr. Rajesh Ranganathan', 'Mechanical Engineering', 'Professor & Head', 'hodmech@cit.edu.in', '0422-2574074', NULL),
('MECH002', 'Dr. N. Rajam Ramaswamy', 'Mechanical Engineering', 'Associate Professor', 'rajamramaswamy@cit.edu.in', NULL, NULL),
('MECH003', 'Dr. G. Suresh Kannan', 'Mechanical Engineering', 'Associate Professor', 'sureshkannan@cit.edu.in', NULL, NULL),
('MECH004', 'Dr. G. Sivakumar', 'Mechanical Engineering', 'Associate Professor', 'vmsivakumar@cit.edu.in', NULL, NULL),
('MECH005', 'Mr. P. Ramakrishnan', 'Mechanical Engineering', 'Assistant Professor', 'ramakrishnan.p@cit.edu.in', NULL, NULL),
('MECH006', 'Dr. M. Velliangiri', 'Mechanical Engineering', 'Assistant Professor', 'velliangiri.m@cit.edu.in', NULL, NULL),
('CIVIL001', 'Dr. R. Sathyanarayan Sridhar', 'Civil Engineering', 'Professor & Head', 'sathyanarayan@cit.edu.in', '0422-2574075', NULL),
('CIVIL002', 'Dr. P. Vinayagam', 'Civil Engineering', 'Professor', 'vinayagam.p@cit.edu.in', NULL, NULL),
('CIVIL003', 'Dr. S. Shanmuga Priya', 'Civil Engineering', 'Professor', 'shanmugapriya@cit.edu.in', NULL, NULL),
('CIVIL004', 'Dr. M. P. Muthuraj', 'Civil Engineering', 'Associate Professor', 'muthuraj@cit.edu.in', NULL, NULL),
('CIVIL005', 'Ms. M. Hannah Angelin', 'Civil Engineering', 'Assistant Professor (Sr. Gr.)', 'hannahangelin.m@cit.edu.in', NULL, NULL),
('CIVIL006', 'Dr. M. Kaarthik', 'Civil Engineering', 'Assistant Professor (Sr. Gr.)', 'kaarthik@cit.edu.in', '9585579885', NULL);

-- Insert records into faculty_academic
INSERT INTO faculty_academic (academic_id, faculty_id, ug_qualification, pg_qualification, phd_qualification, research_interest, publication_count) VALUES
('ACA001', 'CSE001', 'B.E. (CSE)', 'M.E. (CSE)', 'Ph.D. (CSE)', 'Data Integration, Semantics Extraction, Data Mining, Image Processing', 28),
('ACA002', 'CSE002', 'B.E. (IT)', 'M.E. (CSE), MBA (HR)', 'Ph.D. (Information and Communication Engineering)', 'Data Analytics, Machine Learning, HR Analytics', 50),
('ACA003', 'CSE003', 'B.E. (CSE)', 'M.E. (CSE)', 'Ph.D. (CSE)', 'Network Security, Machine Learning, IoT, Data Science', 22),
('ACA004', 'CSE004', 'B.E. (CSE)', 'M.E. (CSE)', 'Ph.D. (CSE)', 'Machine Learning, Deep Learning, Cloud Computing, Big Data Analytics', 19),
('ACA005', 'CSE005', 'B.E. (CSE)', 'M.E. (CSE)', 'Ph.D. (Information and Communication Engineering)', 'Wireless Networks, Cognitive Radio Networks, Machine Learning', 17),
('ACA006', 'CSE006', 'B.E. (CSE)', 'M.E. (CSE)', 'Ph.D. (CSE)', 'IoT, Blockchain Applications, Smart Contracts', 14),
('ACA007', 'ECE001', 'B.E. (ECE)', 'M.E. (Communication Systems)', 'Ph.D. (ECE)', 'Signal Processing, Wireless Networks, Embedded Systems', 65),
('ACA008', 'ECE002', 'B.E. (ECE)', 'M.E. (Communication Systems)', 'Ph.D. (ECE)', 'VLSI Design, Wireless Sensor Networks, IoT Systems', 42),
('ACA009', 'ECE003', 'B.E. (ECE)', 'M.E. (Applied Electronics)', 'Ph.D. (ECE)', 'Intruder Identification Systems, Image Processing, Security', 25),
('ACA010', 'ECE004', 'B.E. (ECE)', 'M.E. (Communication Systems)', 'Ph.D. (ECE)', 'RF Communications, Microwave Antennas, Wireless Networks', 20),
('ACA011', 'ECE005', 'B.E. (ECE)', 'M.E. (Applied Electronics)', 'Ph.D. (ECE)', 'Medical Image Processing, Machine Learning in Healthcare', 16),
('ACA012', 'ECE006', 'B.E. (ECE)', 'M.E. (VLSI Design)', 'Ph.D. (ECE)', 'Low Power VLSI, Nano-electronics, Micro-sensors', 12),
('ACA013', 'EEE001', 'B.E. (EEE)', 'M.E. (Power Systems)', 'Ph.D. (EEE)', 'Power System Optimization, Smart Grids, Renewable Energy Integration', 48),
('ACA014', 'EEE002', 'B.E. (EEE)', 'M.E. (Power Electronics and Drives)', 'Ph.D. (EEE)', 'Power Converters, Motor Control, Electric Vehicles', 28),
('ACA015', 'EEE003', 'B.E. (EEE)', 'M.E. (Electrical Machines)', 'Ph.D. (EEE)', 'Special Machines, Wind Energy Conversion, Solar PV Systems', 21),
('ACA016', 'EEE004', 'B.E. (EEE)', 'M.E. (Power Electronics)', 'Ph.D. (EEE)', 'Dielectric Materials, Insulation Diagnostics, High Voltage DC', 18),
('ACA017', 'EEE005', 'B.E. (EEE)', 'M.E. (Power Systems)', 'Ph.D. (EEE)', 'Electricity Markets, Power Quality, Microgrids', 15),
('ACA018', 'EEE006', 'B.E. (EEE)', 'M.E. (Embedded Systems)', 'Ph.D. (EEE)', 'Smart Grid Security, Energy Harvesting, IoT Sensors', 11),
('ACA019', 'MECH001', 'B.E. (Mechanical)', 'M.E. (Manufacturing Engineering)', 'Ph.D. (Loughborough University, UK)', 'Rapid Prototyping, RFID Integration, Prosthesis Design, Lean Systems', 55),
('ACA020', 'MECH002', 'B.E. (Mechanical)', 'M.E. (Industrial Engineering)', 'Ph.D. (Mechanical Engineering)', 'Manufacturing System Simulation, Production Planning, Ergonomics', 30),
('ACA021', 'MECH003', 'B.E. (Mechanical)', 'M.E. (Thermal Engineering)', 'Ph.D. (Mechanical Engineering)', 'Metal Matrix Composites, Materials Characterization, Machining', 24),
('ACA022', 'MECH004', 'B.E. (Mechanical)', 'M.E. (Advanced Manufacturing Tech)', 'Ph.D. (Anna University)', 'Surface Engineering, Friction Stir Welding, Machining Optimization', 26),
('ACA023', 'MECH005', 'B.E. (Mechanical)', 'M.Tech. (Mechanical)', NULL, 'Computational Fluid Dynamics, Heat Exchanger Optimization', 8),
('ACA024', 'MECH006', 'B.E. (Mechanical)', 'M.E. (CAD/CAM)', 'Ph.D. (Mechanical Engineering)', 'Biomechanics, Finite Element Modeling, Composite Design', 12),
('ACA025', 'CIVIL001', 'B.E. (Civil)', 'M.E. (Foundation Engineering)', 'Ph.D. (Civil Engineering)', 'Ground Improvement Techniques, Deep Foundations, Soil-Structure Interaction', 38),
('ACA026', 'CIVIL002', 'B.E. (Civil)', 'M.E. (Structural Engineering)', 'Ph.D. (Civil Engineering)', 'High Performance Concrete, Seismic Resilience, Retrofitting', 32),
('ACA027', 'CIVIL003', 'B.E. (Civil)', 'M.E. (Environmental Engineering)', 'Ph.D. (Civil Engineering)', 'Industrial Wastewater Treatment, Membrane Technology, Environmental Impact', 27),
('ACA028', 'CIVIL004', 'B.E. (Civil)', 'M.E. (Structural Engineering)', 'Ph.D. (Civil Engineering)', 'Composite Plates, Cold-formed Steel, Pavement Materials', 20),
('ACA029', 'CIVIL005', 'B.E. (Civil)', 'M.E. (Structural Engineering)', NULL, 'Sustainable Concrete, Waste Utilization in Concrete', 9),
('ACA030', 'CIVIL006', 'B.E. (Civil)', 'M.E. (Structural Engineering)', 'Ph.D. (Civil Engineering)', 'Non-Destructive Testing (NDT), Recycled Aggregates, Cold-Formed Steel', 24);
