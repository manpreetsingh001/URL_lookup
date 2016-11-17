#!/usr/bin/python

from flask import Flask,request,Response,jsonify,render_template
import mysql.connector
import sys,os,urlparse,json,re
from mysql_connection import database_name
from mysql_connection import TB_name
from mysql_connection import config  

app = Flask(__name__)

@app.errorhandler(404)                                        #Error handling  for wrong URL input
def not_found(error=None):
    message = dict(status= 404,message= 'Not Found: ' + request.url,)
    resp = jsonify(message)
    resp.status_code = 404
    return resp 

@app.route('/urlinfo/1/<path:URL>', methods=['GET'])
def search(URL):

  '''Take the  input URL,check it is valid URL or not 
    search the database for a possible malicious address'''

  '''Check URL is of valid format
    for ex:www.google.com
          http://www.google.com #Valid
          http://google.com     #Invalid
          www.google            #Invalid 
          http://www.google.com/images   #Valid
          http://www.youtube.com/watch?v=6RB89BOxaYY  #Valid
  '''
    
  regex = re.compile(
      r'^https?://'  # http:// or https://
      r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
      r'localhost|'  # localhost...
      r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
      r'(?::\d+)?'  # optional port
      r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
  if URL is not None and  regex.search(URL):
    #Strip http(s) and www from url
    reg = re.compile(r"https?://(www\.)?")
    new_URL = reg.sub('', URL).strip().strip('/') 
  else:
    data = dict(Invalid_URL_Format="Please Enter a valid URL format like http://www.google.com")
    resp = jsonify(data)
    return resp

  #Strip http(s) and www from url
  #reg = re.compile(r"https?://(www\.)?")
  #new_URL=reg.sub('', URL).strip().strip('/')
 
  #search database for malicious URL
  try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cnx.database = database_name
    cursor.execute('''SELECT COUNT(1) FROM URLlookup where malicious = '{0}' '''.format(new_URL))
    Malware = cursor.fetchone()[0]
  except mysql.connector.errors.Error as err:
    data = dict(Error="{}".format(err) )
    resp = jsonify(data)
    return resp

  #cursor.execute('''SELECT COUNT(1) FROM URLlookup where malicious = '{0}'".format(new_URL)''')
  #Malware = cursor.fetchone()[0]
  if not Malware:
    data = dict(Current_status = "Safe Browsing",Recent_activity = "No  malicious content seen Redirecting you on .... {}".format(new_URL))
    resp= jsonify(data)
    return resp 
  else:
    data = dict(Current_status = "Dangerous Site",Recent_activity = "Malicious content seen on {}".format(new_URL))
    resp= jsonify(data)
    return resp
  
if __name__ == "__main__":
  app.run(debug=True)


   


