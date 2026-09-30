import os

def fix_main():
    with open('main.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    main_start = -1
    for i, line in enumerate(lines):
        if line.startswith('if __name__ == "__main__":'):
            main_start = i
            break
            
    if main_start != -1:
        # Check if AdvancedQueryDialog is defined after this
        has_dialog = False
        for i in range(main_start, len(lines)):
            if 'class AdvancedQueryDialog' in lines[i]:
                has_dialog = True
                break
                
        if has_dialog:
            # We need to extract the __main__ block
            # It should just be the if statement and the few lines after it.
            # But wait, we can just grab everything from __main__ that is indented, and move it to the end.
            
            new_lines = []
            main_block = []
            in_main = False
            
            for line in lines:
                if line.startswith('if __name__ == "__main__":'):
                    in_main = True
                    main_block.append(line)
                    continue
                    
                if in_main:
                    if line.startswith('class '):
                        in_main = False
                        new_lines.append(line)
                    else:
                        main_block.append(line)
                else:
                    new_lines.append(line)
                    
            # clean up trailing newlines
            while main_block and not main_block[-1].strip():
                main_block.pop()
                
            new_lines.extend(['\n\n'] + main_block + ['\n'])
            
            with open('main.py', 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print('Fixed main.py block order')
            return
    print('No fix needed')

if __name__ == "__main__":
    fix_main()
