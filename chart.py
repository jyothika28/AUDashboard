from flask import Flask, request, flash,redirect,render_template, url_for
#from flask_mysqldb import MySQL
import pandas as pd
import csv
import os
app=Flask(__name__)
import sqlite3

@app.route("/")
def student():
     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Student"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     values=df['s_course'].value_counts().tolist()
     names=df['s_course'].value_counts().index.tolist()
     
     return render_template("charts.html",names=names,values=values)
     #,s_course_counts=s_course_counts,s_course_names=s_course_names

if __name__=="__main__":
     app.secret_key='1234'
     app.run(debug=True)