import re
from datetime import datetime

sql_subscribers = []

def subscribe_to_sql(callback):
    sql_subscribers.append(callback)

def notify_sql(sql, params, success, rows_or_returned, error_msg="", is_cascade=False):
    display_sql = sql
    if params:
        formatted_params = []
        for p in params:
            if p is None:
                formatted_params.append("NULL")
            elif isinstance(p, (int, float)):
                formatted_params.append(str(p))
            else:
                safe_str = str(p).replace("'", "''")
                formatted_params.append(f"'{safe_str}'")
        try:
            display_sql = sql % tuple(formatted_params)
        except:
            display_sql = f"{sql} | Params: {params}"
            
    # Format the query nicely
    display_sql = display_sql.strip()
    if not display_sql.endswith(';'):
        display_sql += ';'
        
    for sub in sql_subscribers:
        try:
            sub({
                "time": datetime.now().strftime("%H:%M:%S"),
                "sql": display_sql,
                "success": success,
                "rows": rows_or_returned,
                "error": error_msg,
                "is_cascade": is_cascade
            })
        except:
            pass
