#!/usr/bin/python

from flask import Flask,render_template,jsonify
import mysql.connector
from URl_lookup import search

'''
 Simple Api test to show that web service is 
 responding to get requests and blocking access to malicious URL 
'''


