import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file, jsonify
import webbrowser
import random
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/hc_home')
def hc_home():
	return render_template("hc_home.html")

@app.route('/ChatConfirmation')
def ChatConfirmation():
	return render_template("ChatConfirmation.html")

@app.route('/HomePage')
def HomePage():
	return render_template("HomePage.html")

@app.route('/SplashScreen')
def SplashScreen():
	return render_template("SplashScreen.html")

@app.route('/ah_home')
def ah_home():
	return render_template("ah_home.html")

@app.route('/lh')
def lh():
	return render_template("lh.html")

@app.route('/sas')
def sas():
	return render_template("sas.html")

@app.route('/animal_info_form')
def animal_info_form():
	return render_template("animal_info_form.html")

@app.route('/animal_info_form',methods=['POST', 'GET'])
def animal_info_form_reg():
	if request.method=='POST':
		animal_type=request.form.get('animal_type')
		animal_age=request.form.get('animal_age')
		gender=request.form.get('gender')
		semen_potency=request.form.get('semen_potency')
		is_diseased=request.form.get('is_diseased')
		husbandry=request.form.get('husbandry')	
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO animal_info VALUES(?,?,?,?,?,?);", (animal_type, animal_age, gender, semen_potency, is_diseased, husbandry))
		conn.commit()
		conn.close()
		return render_template('animal_info_form.html')

@app.route('/disease_chart_form')
def disease_chart_form():
	return render_template("disease_chart_form.html")

@app.route('/disease_chart_form',methods=['POST', 'GET'])
def disease_chart_form_reg():
	if request.method=='POST':
		animal_type=request.form.get('animal_type')
		animal_age=request.form.get('animal_age')
		gender=request.form.get('gender')
		disease=request.form.get('disease')
		no_of_deaths=request.form.get('no_of_deaths')
		location=request.form.get('location')	
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO animal_disease_chart VALUES(?,?,?,?,?,?);", (animal_type, animal_age, gender, disease, no_of_deaths, location))
		conn.commit()
		conn.close()
		return redirect('/disease_chart_view')

@app.route('/husbandry_form')
def husbandry_form():
	return render_template("husbandry_form.html")

@app.route('/husbandry_form',methods=['POST', 'GET'])
def husbandry_form_reg():
	if request.method=='POST':
		contact_detail=request.form.get('contact_detail')
		location=request.form.get('location')	
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO husbandry VALUES(?,?);", (contact_detail, location))
		conn.commit()
		conn.close()
		return redirect('/husbandry_view')

@app.route('/disease_chart_view')
def disease_chart_view():
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	results = cur.execute("select * from animal_disease_chart;").fetchall()
	return render_template("disease_chart_view.html", results=results)

@app.route('/husbandry_view')
def husbandry_view():
	conn = sqlite3.connect("data.db")
	cur = conn.cursor()
	results = cur.execute("select * from husbandry;").fetchall()
	return render_template("husbandry_view.html", results=results)

@app.route('/animal_info_view')
def animal_info_view():
	return render_template("animal_info_view.html")

@app.route('/animal_info_view',methods=['POST', 'GET'])
def animal_info_view_reg():
	if request.method=='POST':
		animal_type=request.form.get('animal_type')
		gender=request.form.get('gender')
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		results = cur.execute("select * from animal_info where type == ? and gender == ?;", (animal_type,gender,)).fetchall()
		print(results)
		return render_template("animal_info_view.html", results=results)

@app.route('/warehouse_detail_form')
def warehouse_detail_form():
	return render_template("warehouse_detail_form.html")

@app.route('/warehouse_detail_form',methods=['POST', 'GET'])
def warehouse_detail_form_reg():
	if request.method=='POST':
		warehouse_name=request.form.get('warehouse_name')
		owner_contact=request.form.get('owner_contact')
		crop_avail=request.form.get('crop_avail')
		crop_qty=request.form.get('crop_qty')
		crop_price=request.form.get('crop_price')
		total_capacity=request.form.get('total_capacity')
		location=request.form.get('location')	
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO warehouse_detail VALUES(?,?,?,?,?,?,?);", (warehouse_name, owner_contact, crop_avail, crop_qty, crop_price, total_capacity, location))
		conn.commit()
		conn.close()
		return render_template('warehouse_detail_form.html')

@app.route('/crop_diseases_form')
def crop_diseases_form():
	return render_template("crop_diseases_form.html")

@app.route('/crop_diseases_form',methods=['POST', 'GET'])
def crop_diseases_form_reg():
	if request.method=='POST':
		location=request.form.get('location')
		type_of_crop=request.form.get('type_of_crop')
		disease_of_crop=request.form.get('disease_of_crop')
		size_of_field=request.form.get('size_of_field')
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		cur.execute("INSERT INTO crop_diseases VALUES(?,?,?,?);", (location, type_of_crop, disease_of_crop, size_of_field))
		conn.commit()
		conn.close()
		return render_template('crop_diseases_form.html')

toggle = 0
ware_name = "abc"
@app.route('/warehouse_update_form')
def warehouse_update_form():
	return render_template("warehouse_update_form.html")

@app.route('/warehouse_update_form',methods=['POST', 'GET'])
def warehouse_update_form_reg():
	if request.method=='POST' and toggle==0:
		global toggle
		global ware_name
		toggle = 1
		count = 0
		warehouse_name=request.form.get('warehouse_name')
		ware_name = warehouse_name
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		results = cur.execute("select * from warehouse_detail where name == ? ;", (warehouse_name,)).fetchone()
		print(results)
		if results == 'NoneType':
			count = 1
		return render_template("warehouse_update_form.html", results=results, count=count)
	else:
		return warehouse_update_form_change()

@app.route('/warehouse_update_form',methods=['POST', 'GET'])
def warehouse_update_form_change():
	if request.method=='POST' and toggle==1:
		global toggle
		global ware_name
		toggle = 0
		crop_avail=request.form.get('crop_avail')
		crop_qty=request.form.get('crop_qty')
		crop_price=request.form.get('crop_price')
		conn = sqlite3.connect("data.db")
		cur = conn.cursor()
		results = cur.execute("update warehouse_detail set avail = ?, qty = ?, price = ? where name == ? ;", (crop_avail, crop_qty, crop_price, ware_name,))
		conn.commit()
		conn.close()
		print(results)
		return render_template("warehouse_update_form.html", results=results)
	else:
		return warehouse_update_form_update()

if __name__ == '__main__':
	app.run(debug=True)
