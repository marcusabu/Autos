import sqlite3
import pandas as pd

conn = sqlite3.connect('../db.sqlite3')
df = pd.read_sql_query("SELECT * FROM scraper_auto", conn)
conn.close()