import sqlite3
import random
from faker import Faker

# Setup
faker = Faker()
departments = ["Engineering", "HR", "Marketing", "Sales", "Finance", "Support"]

# Connect to SQLite
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Drop table if exists
cursor.execute("DROP TABLE IF EXISTS employees")

# Create table
cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT,
    salary REAL
)
""")

# Generate 100 fake records
employees = []
for _ in range(100):
    name = faker.name()
    age = random.randint(22, 60)
    department = random.choice(departments)
    salary = round(random.uniform(40000, 120000), 2)
    employees.append((name, age, department, salary))

# Insert records
cursor.executemany("""
INSERT INTO employees (name, age, department, salary)
VALUES (?, ?, ?, ?)
""", employees)

conn.commit()
conn.close()

print("✅ Database created and populated with 100 employees.")

