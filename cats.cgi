#! /usr/bin/python3
import cgi
import cgitb
import passwords
import MySQLdb
import json
import os

cgitb.enable()

conn = MySQLdb.connect(host = passwords.SQL_host, user = passwords.SQL_user, passwd = passwords.SQL_passwd, db = "gwen")


c= conn.cursor()
path_info = ""
if "PATH_INFO" in os.environ:
    path_info = os.environ["PATH_INFO"]
if "PATH_INFO" not in os.environ:
    path_info = ""
if path_info == "":
    print("Status: 302 Redirect")
    print("Location: cats.cgi/")
    print()
if path_info == "/":
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print("""<html><body><p><a href = cats.cgi/allcats> all cats</a></p><p><a href=cats.cgi/catsform>add a new cat</a></p></body></html>""")
if "allcats" in path_info:
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()
    c = conn.cursor()

    c.execute("SELECT * FROM cats;")

    results = c.fetchall()
    c.close()
    results_json = json.dumps(results, indent =2)
    print(results_json)
    

if "catsform" in path_info:
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print("""<html><body>
    <form action = "cats.cgi/output" method = "get">
    Enter in a cat name
    <input type = text name = catname>
    Enter in a cat age
    <input type = text name = age>
    Enter in a cats favorite toy
    <input type = text name = toy>
    <input type = submit>
    </form>
    """)
    
if "output" in path_info:
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    
    form = cgi.FieldStorage()
    if "catname" in form:
        cat_name = form["catname"].value
        cat_age = form["age"].value
        cat_toy = form["toy"].value
    c= conn.cursor()
    c.execute("INSERT INTO cats (name, age, toy) VALUES(%s, %s, %s);", (cat_name,cat_age,cat_toy))

    c.close()
    conn.commit()

    c= conn.cursor()
    c.execute("SELECT * FROM cats WHERE id = (SELECT MAX(id) FROM cats);")
    results = c.fetchall()
    c.close()

    results_json = json.dumps(results, indent =2)
    print(results_json)



