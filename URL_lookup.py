#!/usr/bin/python

from flask import Flask,request,g,Response,jsonify
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
     pass  
  else:
     data=dict(Invalid_URL_Format="Please see Readme for valid Url formati and don't forget to add http://")
     resp = jsonify(data)
     return resp
     
  #Strip http(s) and www from url
  reg = re.compile(r"https?://(www\.)?")
  new_URL=reg.sub('', URL).strip().strip('/')

 
  #print new_URL
  return new_URL     
     
  
if __name__ == "__main__":
  app.run(debug=True)


   


