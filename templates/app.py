from DBconnection import dbManager
from flask import Flask, session, render_template, request, session, g, redirect, url_for
import os,stripe
import mysql.connector
import string
import logging
import random

app=Flask(_name_)

class MeetDoc:
    @app.route('/showFirstPage', methods = ['POST','GET']) 
    def MeetDoc(self):
        doctortype = []
        dbcon=dbManager.databaseConnection()
        cur=dbcon.cursor()
        query = " "
        data = cur.fetchall()
        for row in data:
            if row[0] not in doctortype:
                doctortype.append(row[0])
        return render_template('firstPage.html',doctortype = doctortype)