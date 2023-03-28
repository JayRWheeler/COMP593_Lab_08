"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.


Usage:
 python create_relationships.py
"""
import os
import sqlite3
from faker import Faker
import random


# Determine the path of the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social_network.db')


def main():
    create_relationships_table()
    populate_relationships_table()


def create_relationships_table():
    """Creates the relationships table in the DB"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY,
                    person1_id INTEGER NOT NULL,
                    person2_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    start_date DATE NOT NULL,
                    FOREIGN KEY (person1_id) REFERENCES people (id),
                    FOREIGN KEY (person2_id) REFERENCES people (id));''')
    con.commit()
    con.close()


def populate_relationships_table():
    """Adds 100 random relationships to the DB"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    fake = Faker()
    for i in range(100):
        person1_id = random.randint(1, 200)
        person2_id = random.randint(1, 200)
        while person1_id == person2_id:
            person2_id = random.randint(1, 200)
        relationship_type = fake.random_element(elements=('spouse', 'parent', 'child', 'sibling'))
        start_date = fake.date_between(start_date='-10y', end_date='today')
        cur.execute("INSERT INTO relationships (person1_id, person2_id, type, start_date) VALUES (?, ?, ?, ?)",
                    (person1_id, person2_id, relationship_type, start_date))
        con.commit()
    con.close()


if __name__ == '__main__':
   main()