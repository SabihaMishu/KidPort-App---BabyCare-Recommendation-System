from sqlalchemy import create_engine, text

SQLALCHEMY_DATABASE_URL = "sqlite:///./kidport.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

columns_to_add = [
    ("child_name", "TEXT"),
    ("pattern", "TEXT"),
    ("recommendation", "TEXT")
]

with engine.connect() as conn:
    for col_name, col_type in columns_to_add:
        try:
            conn.execute(text(f"ALTER TABLE child_logs ADD COLUMN {col_name} {col_type}"))
            print(f"Added column {col_name}")
        except Exception as e:
            print(f"Column {col_name} might already exist or error: {e}")
    conn.commit()
