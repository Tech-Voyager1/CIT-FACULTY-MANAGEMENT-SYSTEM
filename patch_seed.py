import re

def update_seed():
    with open('database/seed.sql', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out = []
    in_faculty = False
    for line in lines:
        if line.startswith('INSERT INTO faculty ('):
            line = line.replace('joining_date)', 'joining_date, experience_years)')
            out.append(line)
            in_faculty = True
        elif in_faculty and line.strip().startswith('('):
            # determine experience based on designation
            exp = 'NULL'
            if 'Assistant Professor' in line:
                exp = '11'
            if 'Associate Professor' in line:
                exp = '15'
            if 'Professor' in line and 'Head' not in line and 'Principal' not in line and 'Assistant' not in line and 'Associate' not in line:
                exp = '18'
            if 'Professor & Head' in line or 'Principal & Professor' in line:
                exp = '20'
                
            # replace phone with NULL if empty ('')
            line = line.replace("''", 'NULL')
            line = line.replace("'None'", 'NULL')
            line = line.replace("'Not Publicly Listed'", 'NULL')
                
            # replace the last parenthesis
            line = line.replace('),', f', {exp}),').replace(');', f', {exp});')
            out.append(line)
        else:
            if ';' in line:
                in_faculty = False
            out.append(line)
            
    with open('database/seed.sql', 'w', encoding='utf-8') as f:
        f.writelines(out)

if __name__ == '__main__':
    update_seed()
