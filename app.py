from DBconnection import dbManager
from flask import Flask, session, render_template, request, session, g, redirect, url_for
import os,stripe
import mysql.connector
import string
import logging
import random
from flask_mail import Mail, Message
from flask_sendgrid import SendGrid

app=Flask(__name__)

app.config.update(
 	DEBUG=True,
 	MAIL_SERVER='smtp.sendgrid.net',
    MAIL_USE_TLS = False,
    MAIL_PORT = 465,
 	MAIL_USE_SSL=True,
 	MAIL_USERNAME = 'apikey',
     MAIL_DEBUG = True,
 	MAIL_PASSWORD = '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'
	)
pub_key = 'pk_test_wLuj1f9wp0kvPH8emMGddGFL00Jojo7zG5'  #to identify the account through which the payment has to be charged
secret_key = 'sk_test_iuwg8PsZ9Egz4dwMbefnjuul00tC1UT6s4' #same as above
stripe.api_key = secret_key
mail = Mail(app)
class MeetDoc:
    @app.route('/MeetDoc', methods = ['POST','GET']) 
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

class Pharmacy:
    @app.route('/showFirstPage', methods = ['POST','GET']) 
    def Pharmacy(self):
        if request.method == "POST":
            pharmId  = request.form['pharmId']
            
        pharmtype = []
        dbcon=dbManager.databaseConnection()
        cur=dbcon.cursor()
        query = " "
        data = cur.fetchall()
        for row in data:
            if row[0] not in pharmtype:
                pharmtype.append(row[0])
        return render_template('firstPage.html',pharmtype = pharmtype)

class LabTest:
    @app.route('/showFirstPage', methods = ['POST','GET']) 
    def LabTest(self):
        test = []
        dbcon=dbManager.databaseConnection()
        cur=dbcon.cursor()
        query = " "
        data = cur.fetchall()
        for row in data:
            if row[0] not in test:
                test.append(row[0])
        return render_template('firstPage.html',test = test)

class Booking:
    @app.route("/bookdoc",methods = ['POST','GET'])
    def bookdoc():
        if g.user:
            if request.method == "POST":
                date = request.form['date'] 
                #date = request.args.get('date') 
                dbcon=dbManager.databaseConnection()
                cur=dbcon.cursor()
                query3=''
                cur.execute(query3,[date])
                data6 = cur.fetchall()
                for row in data6:
                    docname = row[0]
                return render_template("invoice.html",date = date)
        else:
            return render_template("firstPage.html")

class Payment():
    @app.route("/payment",methods =['POST','GET'])
    def payment():
        if request.method == "POST":
            totalAmount = request.args.get('total_Amount')
            emailOfReceiver = request.args.get('vistEmail')
        print("EMail of reciver",emailOfReceiver)
        print(totalAmount)
        return render_template("payment.html",pub_key = pub_key, totalAmount = totalAmount,emailOfReceiver = emailOfReceiver)

    
    @app.route("/processPayment", methods = ['POST'])
    def processPayment():
        if request.method == "POST":
            emailOfReceiver = request.args.get('emailOfReceiver')
        customer = stripe.Customer.create(email = request.form['stripeEmail'],source = request.form['stripeToken'])
        charge = stripe.Charge.create(
            customer = customer.id,
            amount = 500,
            currency = 'eur',
            description = 'Movie'
        )
        return redirect(url_for("send_mail",emailOfReceiver = emailOfReceiver))

@app.route('/send_mail',methods = ['POST','GET'])
def send_mail():
    userEmail = request.args.get('emailOfReceiver')
    print(userEmail)
    msg = Message('Booking Confirmed', sender = 'naik.raghavendra31.com', recipients = [str(userEmail)])
    msg.body = "Your doctor booking is confirmed."
    mail.send(msg)
    return render_template("success.html")