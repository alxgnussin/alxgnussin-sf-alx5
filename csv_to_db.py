import os
import csv
import psycopg2

meals = "meals_4.csv"
cat = "categories.csv"
conn_str = os.environ.get("DATABASE_URL")


def csv_reader(file):
    my_list = []
    with open(file, "r") as f_obj:
        reader = csv.reader(f_obj)
        for row in reader:
            my_list.append(",".join(row).split(';'))
    return my_list


def insert_to_categories():
    my_list = csv_reader(cat)
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "p5_categories" ("title") VALUES '
    for x in my_list:
        query = prefix + '(%s)'
        curs.execute(query, [x[1]])
        conn.commit()
    conn.close()


def insert_to_meals():
    my_list = csv_reader(meals)
    conn = psycopg2.connect(conn_str)
    curs = conn.cursor()
    prefix = 'INSERT INTO "p5_meals" ("title", "price", "description", "picture", "category_id") VALUES '
    for x in my_list:
        query = prefix + '(%s, %s, %s, %s, %s)'
        curs.execute(query, [x[1], x[2], x[3], x[4], x[5]])
        conn.commit()
    conn.close()


insert_to_categories()
insert_to_meals()
