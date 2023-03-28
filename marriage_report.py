import os
import sqlite3
import csv
from create_relationships import db_path


def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)


def get_married_couples():
    """Queries the Social Network database for all married couples.


    Returns:
        list: (name1, name2, start_date) of married couples
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('''SELECT p1.name, p2.name, r.start_date
                   FROM relationships AS r
                   JOIN people AS p1 ON r.person1_id = p1.id
                   JOIN people AS p2 ON r.person2_id = p2.id
                   WHERE r.type='spouse' ''')
    married_couples = cur.fetchall()
    con.close()
    return married_couples


def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's
    names and their wedding anniversary date  


    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Person 1', 'Person 2', 'Anniversary'])
        writer.writerows(married_couples)


if __name__ == '__main__':
    main()
