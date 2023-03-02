from flask import Flask, render_template, request, url_for, redirect, session,flash
from datetime import datetime, timedelta
from psycopg2 import *


class AccountManager:
    def __init__(self):
        self.conn = connect("postgresql://postgres:Jonny3699@localhost:5432/Fullstack")
        self.cur = self.conn.cursor()

    def create_account(self, fname, lname, email, password):
        
        self.cur.execute("""
            SELECT * FROM userdata WHERE email = %s;
            """,
            (email,))
        record = self.cur.fetchone()
        if record :
            return flash("Email already exists.")
        else:
            
            self.cur.execute("""
                INSERT INTO userdata (firstname, lastname, email, password)
                VALUES (%s, %s, %s, %s);
                """,
                (fname, lname, email, password))
            self.conn.commit()

    def check_email(self, email):
        self.cur.execute("""
            SELECT * FROM userdata WHERE LOWER(email) = LOWER(%s);
            """,
            (email,))
        record = self.cur.fetchone()
        if record:
            return True
        else:
            return False
        
    def check_credentials(self, email, password):
        self.cur.execute("""
            SELECT * FROM userdata WHERE LOWER(email) = LOWER(%s) AND password = %s;
            """,
            (email, password))
        record = self.cur.fetchone()
        if record:
            return True
        else:
            
            return False
        
    def get_firstname(self, email):
        self.cur.execute("""
            SELECT firstname FROM userdata WHERE LOWER(email) = LOWER(%s);
        """, (email,))
        firstname = self.cur.fetchone()[0]
        self.conn.commit() 
        return firstname
        
    def get_money(self, email):
        self.cur.execute("""
            SELECT money FROM userdata WHERE LOWER(email) = LOWER(%s);
            """,
            (email,))
        record = self.cur.fetchone()
        if record:
            return record[0]
        else:
            return None
        
        
    def create_watchlist(self, email, stock, time ):
        
        self.cur.execute("""
                INSERT INTO watchlist (email, stock, date)
                VALUES (%s, %s, %s);
                """,
                (email, stock, time ))
        self.conn.commit()
    
    def delete_watchlist_item(self, email, stock):
        self.cur.execute("""
                DELETE FROM watchlist
                WHERE email = %s AND stock = %s;
                """,
                (email, stock))
        self.conn.commit()

    def watchlist(self, email):
        self.cur.execute("""
            SELECT stock FROM watchlist WHERE LOWER(email) = LOWER(%s);
            """,
            (email,))
        records = self.cur.fetchall()
        if records:
            return [record[0] for record in records]
        else:
            return []
        
    def close(self):
        self.cur.close()
        self.conn.close()
