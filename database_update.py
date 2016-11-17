#!/usr/bin/python
'''Script for populating malware URLs' in MYSQL database 
   This script need to br run first to create a database
'''
import sys,logging
import mysql.connector
from mysql_connection import database_name
from mysql_connection import TB_name
from mysql_connection import config

def create_db(cursor):                        #Database creation
  try:
    query = '''CREATE DATABASE IF NOT EXISTS {0}'''.format(database_name)
    cursor.execute(query)
    print {"Database  name malicious": "is created"}

  except mysql.connector.errors.Error as err:
    data = {"Issue in creating database": "Error:{}".format(err)}
    sys.exit(data)
    
def create_TB(cursor,connection):             #Creating a table
  try:
    cursor.execute('''DROP TABLE IF EXISTS URLlookup''')
    query = '''CREATE TABLE {}(malicious VARCHAR(100) NOT NULL)'''.format(TB_name)
    cursor.execute(query)
    connection.commit()
    data = {"Table name URLlookup": "is successfully created"}
    print data

  except mysql.connector.errors.Error as err:
    data = {"There is an issue in creating table":"Error:{}".format(err)}
    sys.exit(data)

def insert_data(url,cursor,conn):             #Insert URL from txt file into database
  try:
    cursor.execute('''INSERT INTO URLlookup (malicious) VALUES ("{0}")'''.format(url))
    conn.commit()
  
  except mysql.connector.errors.Error as err:
    data = {"There is an issue in inserting data into table":"Error:{}".format(err)}
    sys.exit(data)

def connection():                              #Creating connection  with mysql and perfroming CRUD operations
  try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    create_db(cursor)
    cnx.database = database_name
   
    create_TB(cursor,cnx)
  
    logging.warning('Adding URL entries from malicious.Text file into database')
    with open("malicious_url.txt") as malware:
      for read in malware:
        read = read.strip('\n')
        insert_data(read,cursor,cnx)
     
    cursor.execute('''select * from URLlookup''')
    fetch = cursor.fetchall() 
    if not fetch:
      print {"status": 409, "Error": "Database is empty"}
    else:
       print "Fetching URL entries from database"
       for iterator in fetch:
            data = dict(URL= iterator[0])
            print data 
            
  except mysql.connector.errors.Error as err:
    data = {"There is an issue in connection to DB":"Error:{}".format(err)}
    sys.exit(data)
  
  finally:
    cursor.close()
    cnx.close()

if __name__ == "__main__":
 connection()  
  
  
  
