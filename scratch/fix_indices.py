with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any bad text widget indices
content = content.replace('sql_text.delete(1, tk.END)', 'sql_text.delete("1.0", tk.END)')
content = content.replace('txt_research.delete(1, tk.END)', 'txt_research.delete("1.0", tk.END)')
content = content.replace('research_txt.get("1", tk.END)', 'research_txt.get("1.0", tk.END)')
content = content.replace('research_txt.get("1.0", tk.END)', 'research_txt.get("1.0", tk.END)')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed text widget indices in main.py")
