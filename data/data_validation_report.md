# CIT Faculty Management System - Data Validation Report

**Course:** 23EC523 DBMS Laboratory  
**Academic Year:** 2026–27  
**Date Generated:** 2026-09-30  
**Authoritative Source:** Official Coimbatore Institute of Technology (CIT) Website (https://www.cit.edu.in)

---

## A. Number of Faculty Collected from Each Department

- **Computer Science and Engineering (CSE):** 6
- **Electronics and Communication Engineering (ECE):** 6
- **Electrical and Electronics Engineering (EEE):** 6
- **Mechanical Engineering:** 6
- **Civil Engineering:** 6

---

## B. Total Records

- **Total Faculty Members:** 30
- **Total Academic Records:** 30

---

## C. Missing Fields (NULL / Blank Values)

The following fields are preserved as `NULL` / blank because they are not explicitly published on official CIT faculty profiles. As per strict project guidelines, no missing values have been fabricated:

- `faculty.phone` is NULL for CSE001 (Dr. K. Amshakala)
- `faculty.joining_date` is NULL for CSE001 (Dr. K. Amshakala)
- `faculty.phone` is NULL for CSE002 (Dr. A. Saran Kumar)
- `faculty.joining_date` is NULL for CSE002 (Dr. A. Saran Kumar)
- `faculty.phone` is NULL for CSE003 (Dr. M. Mohanapriya)
- `faculty.joining_date` is NULL for CSE003 (Dr. M. Mohanapriya)
- `faculty.phone` is NULL for CSE004 (Dr. S. P. Abirami)
- `faculty.joining_date` is NULL for CSE004 (Dr. S. P. Abirami)
- `faculty.phone` is NULL for CSE005 (Dr. A. Priyadharshini)
- `faculty.joining_date` is NULL for CSE005 (Dr. A. Priyadharshini)
- `faculty.phone` is NULL for CSE006 (Dr. G. Karthikeyan)
- `faculty.joining_date` is NULL for CSE006 (Dr. G. Karthikeyan)
- `faculty.joining_date` is NULL for ECE001 (Dr. A. Rajeswari)
- `faculty.joining_date` is NULL for ECE002 (Dr. M. Poongothai)
- `faculty.phone` is NULL for ECE003 (Dr. G. Puvaneswari)
- `faculty.joining_date` is NULL for ECE003 (Dr. G. Puvaneswari)
- `faculty.phone` is NULL for ECE004 (Dr. P. Muthu Subramanian)
- `faculty.joining_date` is NULL for ECE004 (Dr. P. Muthu Subramanian)
- `faculty.phone` is NULL for ECE005 (Dr. T. Balakumaran)
- `faculty.joining_date` is NULL for ECE005 (Dr. T. Balakumaran)
- `faculty.phone` is NULL for ECE006 (Dr. M. Ramya)
- `faculty.joining_date` is NULL for ECE006 (Dr. M. Ramya)
- `faculty.joining_date` is NULL for EEE001 (Dr. E. Chandira Sekaran)
- `faculty.phone` is NULL for EEE002 (Dr. S. Elango)
- `faculty.joining_date` is NULL for EEE002 (Dr. S. Elango)
- `faculty.phone` is NULL for EEE003 (Dr. A. Kavithamani)
- `faculty.joining_date` is NULL for EEE003 (Dr. A. Kavithamani)
- `faculty.phone` is NULL for EEE004 (Dr. M. L. Merlin Sajini)
- `faculty.joining_date` is NULL for EEE004 (Dr. M. L. Merlin Sajini)
- `faculty.phone` is NULL for EEE005 (Dr. B. Vasanthan)
- `faculty.joining_date` is NULL for EEE005 (Dr. B. Vasanthan)
- `faculty.phone` is NULL for EEE006 (Dr. Y. Hamsavarthini)
- `faculty.joining_date` is NULL for EEE006 (Dr. Y. Hamsavarthini)
- `faculty.joining_date` is NULL for MECH001 (Dr. Rajesh Ranganathan)
- `faculty.phone` is NULL for MECH002 (Dr. N. Rajam Ramaswamy)
- `faculty.joining_date` is NULL for MECH002 (Dr. N. Rajam Ramaswamy)
- `faculty.phone` is NULL for MECH003 (Dr. G. Suresh Kannan)
- `faculty.joining_date` is NULL for MECH003 (Dr. G. Suresh Kannan)
- `faculty.phone` is NULL for MECH004 (Dr. G. Sivakumar)
- `faculty.joining_date` is NULL for MECH004 (Dr. G. Sivakumar)
- `faculty.phone` is NULL for MECH005 (Mr. P. Ramakrishnan)
- `faculty.joining_date` is NULL for MECH005 (Mr. P. Ramakrishnan)
- `faculty_academic.phd_qualification` is NULL for MECH005 (Mr. P. Ramakrishnan)
- `faculty.phone` is NULL for MECH006 (Dr. M. Velliangiri)
- `faculty.joining_date` is NULL for MECH006 (Dr. M. Velliangiri)
- `faculty.joining_date` is NULL for CIVIL001 (Dr. R. Sathyanarayan Sridhar)
- `faculty.phone` is NULL for CIVIL002 (Dr. P. Vinayagam)
- `faculty.joining_date` is NULL for CIVIL002 (Dr. P. Vinayagam)
- `faculty.phone` is NULL for CIVIL003 (Dr. S. Shanmuga Priya)
- `faculty.joining_date` is NULL for CIVIL003 (Dr. S. Shanmuga Priya)
- `faculty.phone` is NULL for CIVIL004 (Dr. M. P. Muthuraj)
- `faculty.joining_date` is NULL for CIVIL004 (Dr. M. P. Muthuraj)
- `faculty.phone` is NULL for CIVIL005 (Ms. M. Hannah Angelin)
- `faculty.joining_date` is NULL for CIVIL005 (Ms. M. Hannah Angelin)
- `faculty_academic.phd_qualification` is NULL for CIVIL005 (Ms. M. Hannah Angelin)
- `faculty.joining_date` is NULL for CIVIL006 (Dr. M. Kaarthik)

---

## D. Possible Duplicates Audit

- **Duplicate Faculty IDs:** None (0 detected)
- **Duplicate Faculty Names:** None (0 detected)
- **Duplicate Email Addresses:** None (0 detected)

---

## E. Faculty Records That Could Not Be Fully Verified

- **None.** All 30 records were verified against official CIT department listings. Unlisted attributes (such as personal phone numbers and exact joining dates) were explicitly recorded as `NULL`.

---

## F. Fields That Are NULL Because the CIT Website Does Not Provide Them

1. `joining_date`: Official CIT department pages list academic designations and degrees but do not display exact appointment/joining dates.
2. `phone`: Direct personal phone numbers are not published for non-administrative faculty members; only department office numbers are provided for HODs and Principal.
3. `phd_qualification`: Left blank (`NULL`) for faculty members currently pursuing their Ph.D. degree (`MECH005` Mr. P. Ramakrishnan, `CIVIL005` Ms. M. Hannah Angelin).

---

## G. Conflicts Found Between Department Listing and Individual Faculty Profile

- **None.** All designations, names, and academic credentials are aligned with official CIT department listings as of September 30, 2026.

---

## H. Verification Checkpoint Status

- `faculty.csv`: **VERIFIED** (30 records, 7 columns)
- `faculty_academic.csv`: **VERIFIED** (30 records, 7 columns)
- `faculty_raw.json`: **VERIFIED** (30 structured records with source page URLs)
- `data_validation_report.md`: **COMPLETE**
