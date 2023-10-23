import re
from flask import Flask, request, flash,redirect,render_template, url_for,session,g
import pandas as pd
import os

app=Flask(__name__)
# run_with_ngrok(app)
import sqlite3
app.config['UPLOAD_FOLDER']='static\excel_data_new'

@app.route("/home")
@app.route("/",methods=['GET','POST'])
def home():
     #cur=mysql.connection.cursor()
     return render_template("mainpage.html")
@app.route("/logins")
def logins():
     return render_template("logins.html")

@app.route("/user",methods=['GET','POST'])
def user():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return redirect(url_for("sess"))

     return render_template("user.html")

@app.route("/admin",methods=['GET','POST'])
def admin():
     return render_template("admin.html")

@app.route("/add_user",methods=['GET','POST'])
def add_user():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return render_template("add_user.html",name=session['user'])
     else:
          return redirect(url_for('home'))

@app.route("/count_users",methods=['GET','POST'])
def count_users():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               ins_query="SELECT * FROM users;"
               cur.execute(ins_query)
               rows=cur.fetchall()
               print(len(rows))
               conn.commit()
               conn.close()
               return render_template("count_users.html",value=rows,name=session['user'])
     else:
          return redirect(url_for('home'))

@app.route("/upload_data",methods=['GET','POST'])
def upload_data():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
                return render_template("upload_data.html",name=session['user'])
     else:
          return redirect(url_for('home'))

@app.route("/admin_dash_dup",methods=['GET','POST'])
def admin_dash_dup():
     return render_template("admin_dashy.html")


@app.route("/admin_dashy",methods=['GET','POST'])
def admin_dashy():
     if request.method=='POST':
          conn=sqlite3.connect("dash.db")
          cur=conn.cursor()
          adminDetails=request.form
          a_email=adminDetails['email']
          a_pass=adminDetails['password']
          admin_query="select * from admin where a_email='"+a_email+"' and a_pass='"+a_pass+"';"
          cur.execute(admin_query)
          rows=cur.fetchall()
          if(len(rows)>=1):
               session.pop('user',None)
               session['user']="Admin"
               return redirect(url_for("admin_sess"))
               
          else:
               
               return render_template("admin.html")

@app.route("/admin_sess",methods=['GET','POST'])
def admin_sess():
     g.user=None
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return render_template("admin_dashy.html",name=session['user'])
          else:
               return redirect(url_for("home"))
     else:
          return redirect(url_for("home"))


@app.route("/a_dashboard",methods=['GET','POST'])
def a_dashboard():
     return render_template("a_dashboard.html")

@app.route("/admissions_submit",methods=['GET','POST'])
def admissions_submit():
     
     if(request.method=='POST'):
          
          admissions_excel=request.files['admissions_excel']
          if(admissions_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],admissions_excel.filename)
               admissions_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Admissions"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,admissions_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
              
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))


@app.route("/st_submit",methods=['GET','POST'])
def st_submit():
     
     if(request.method=='POST'):
          
          st_excel=request.files['st_excel']
          if(st_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],st_excel.filename)
               st_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Student"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,st_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
              
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))

@app.route("/faculty_submit",methods=['GET','POST'])
def faculty_submit():
     if(request.method=='POST'):
          
          fac_excel=request.files['fac_excel']
          if(fac_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],fac_excel.filename)
               fac_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Faculty"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,fac_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))

@app.route("/research_submit",methods=['GET','POST'])
def research_submit():
     if(request.method=='POST'):
          
          res_excel=request.files['research_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Research Grants"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))


@app.route("/programs_submit",methods=['GET','POST'])
def programs_submit():
     if(request.method=='POST'):
          
          res_excel=request.files['programs_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Programs"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))

@app.route("/support_submit",methods=['GET','POST'])
def support_submit():
     
     if(request.method=='POST'):
          
          support_excel=request.files['support_excel']
          if(support_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],support_excel.filename)
               support_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Support Staff"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,support_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
              
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))


@app.route("/it_pub",methods=['GET','POST'])
def it_pub():
     
     if(request.method=='POST'):
          
          res_excel=request.files['itpub_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="IT Publications"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))


@app.route("/cse_pub",methods=['GET','POST'])
def cse_pub():
     
     if(request.method=='POST'):
          
          res_excel=request.files['csepub_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="CSE Publications"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))



@app.route("/eee_pub",methods=['GET','POST'])
def eee_pub():
     
     if(request.method=='POST'):
          
          res_excel=request.files['eeepub_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="EEE Publications"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))



@app.route("/ece_pub",methods=['GET','POST'])
def ece_pub():
     
     if(request.method=='POST'):
          
          res_excel=request.files['ecepub_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="ECE Publications"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))



@app.route("/chem_pub",methods=['GET','POST'])
def chem_pub():
     
     if(request.method=='POST'):
          
          res_excel=request.files['chempub_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Chemical Publications"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))



@app.route("/mech_pub",methods=['GET','POST'])
def mech_pub():
     
     
     if(request.method=='POST'):
          
          res_excel=request.files['mechpub_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Mechanical Publications"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))


@app.route("/user_dashy",methods=['GET','POST'])
def user_dashy():
     if request.method=='POST':
          conn=sqlite3.connect("dash.db")
          cur=conn.cursor()
          Details=request.form
          u_email=Details['u_email']
          u_pass=Details['u_password']
          if(u_email=='admin1@gmail.com' and u_pass=='shj@100'):

               session['user']="Admin"
               return redirect(url_for("admin_sess"))
          else:
               user_query="select * from users where u_email='"+u_email+"' and u_pass='"+u_pass+"';"
               # fetch_name="select s_name from users where u_email='"+u_email+"';"
               cur.execute(user_query)
               rows=cur.fetchall()
               if(len(rows)>=1):
                    fetch_name="select u_name from users where u_email='"+u_email+"';"
                    cur.execute(fetch_name)
                    rows=cur.fetchall()
                    for i in rows:
                         name=i[0]
                    fetch_name="select u_name from users where u_email='"+u_email+"';"
                    cur.execute(fetch_name)
                    rows=cur.fetchall()
                    for i in rows:
                         name=i[0]
                    session.pop('user',None)
                    session['user']=name
                    return redirect(url_for("sess"))
                    
               else:
                    if 'user' in session:
                         g.user=session['user']
                         if(g.user):
                              return redirect(url_for("sess"))
                    return redirect(url_for("home"))



@app.route("/sess",methods=['GET','POST'])
def sess():
     g.user=None
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return render_template("user_dashy.html",name=session['user'])
          else:
               return render_template("user.html")
     else:
          return redirect(url_for('home'))
@app.route("/logout",methods=['GET','POST'])
def logout():
     session.pop('user',None)
     return render_template("mainpage.html")
# def student():
#      if request.method=='POST':
#           conn=sqlite3.connect("dash.db")
#           cur=conn.cursor()
#           userDetails=request.form
#           u_email=userDetails['u_email']
#           u_pass=userDetails['u_password']
#           # user_query="select * from users where u_email='"+u_email+"' and u_pass='"+u_pass+"';"
#           fetch_name="select u_name from users where u_email='"+u_email+"';"
#           cur.execute(fetch_name)
#           rows=cur.fetchall()
#           for i in rows:
#                name=i[0]
#           return render_template("student.html",name=name)


          
@app.route("/student",methods=['GET','POST'])
def student():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               
               cat="Student"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)


               year_drop=df['s_year'].value_counts().index.to_list()
               year_drop.sort()
               # leng=len(year_drop)
               d_drop=df['program'].value_counts().index.to_list()

               b_drop=df['s_branch'].value_counts().index.to_list()

               no=df.shape[0]
               m=df['s_gender'].tolist().count('M')
               f=df['s_gender'].tolist().count('F')
               u=df['s_course'].tolist().count('UG')
               p=df['s_course'].tolist().count('PG')
               ph=df['s_course'].tolist().count('PhD')

               course_values=df['s_course'].value_counts().tolist()
               course_names=df['s_course'].value_counts().index.tolist()
          
               year_names=df['s_year'].value_counts().index.tolist()
               year_values=df['s_year'].value_counts().tolist()
               
               branch_values=df['s_branch'].value_counts().tolist()
               branch_names=df['s_branch'].value_counts().index.tolist()
               
               year_count=df['s_year'].value_counts().tolist()
               year_count_names=df['s_year'].value_counts().index.tolist()


               #LE Deets
               le_data=df.loc[df['s_year'].str.contains('LE')]
               le_count=le_data['s_branch'].value_counts().tolist()
               le_branch=le_data['s_branch'].value_counts().index.tolist()

               #UG -> years
               ug_course_data=df.loc[df['s_course']=='UG']
               ug_years=ug_course_data['s_year'].value_counts().tolist()
               ug_year_count=ug_course_data['s_year'].value_counts().index.tolist()

               #PG -> years
               pg_course_data=df.loc[df['s_course']=='PG']
               pg_years=pg_course_data['s_year'].value_counts().tolist()
               pg_year_count=pg_course_data['s_year'].value_counts().index.tolist()

               #UG -> branch
               ug_branch_data=df.loc[df['s_course']=='UG']
               ug_branch=ug_branch_data['s_branch'].value_counts().sort_index(ascending=True).tolist()
               ug_branch_count=ug_branch_data['s_branch'].value_counts().sort_index(ascending=True).index.tolist()


               #UG,PG,PHD -> branch

               pg_data=df.loc[df['s_course']=='PG']
               pg_branch=pg_data['s_branch'].value_counts().sort_index(ascending=True).tolist()
               pg_branch_count=pg_data['s_branch'].value_counts().sort_index(ascending=True).index.tolist()

               phd_data=df.loc[df['s_course']=='PhD']
               phd_branch=phd_data['s_branch'].value_counts().sort_index(ascending=True).tolist()
               phd_branch_count=phd_data['s_branch'].value_counts().sort_index(ascending=True).index.tolist()

               alpha={'CIVIL':1, 'CSE':2, 'ECE':3, 'EEE':4, 'IT':5, 'MECH':6}

               for i in alpha:
                    if(i not in ug_branch_count):
                         ug_branch_count.insert(alpha[i]-1,i)
                         ug_branch.insert(alpha[i]-1,0)

               for i in alpha:
                    if(i not in pg_branch_count):
                         pg_branch_count.insert(alpha[i]-1,i)
                         pg_branch.insert(alpha[i]-1,0)

               for i in alpha:
                    if(i not in phd_branch_count):
                         phd_branch_count.insert(alpha[i]-1,i)
                         phd_branch.insert(alpha[i]-1,0)
     

               m1=df.loc[df['s_gender']=="M"]
               mc=m1['Caste'].value_counts().sort_index().tolist()
               mc2=m1['Caste'].value_counts().sort_index().index.tolist()

               f1=df.loc[df['s_gender']=="F"]
               fc=f1['Caste'].value_counts().sort_index().tolist()
               fc2=f1['Caste'].value_counts().sort_index().index.tolist()

               ca= list(set(mc2) | set(fc2))
               # print(ca)

               al1 = {ca[i-1]: i for i in range(1,len(ca)+1)}
            
               alpha1=[]
               # print(mc2)
               for i in al1:
                    if(i not in mc2):
                         mc2.insert(al1[i]-1,i)
                         mc.insert(al1[i]-1,0)
               # print(mc)
               for i in al1:
                    if(i not in fc2):
                         fc2.insert(al1[i]-1,i)
                         fc.insert(al1[i]-1,0)

               for i in al1:
                    alpha1.append(i)

               
               glist=[mc,fc]
             
               gtab=pd.DataFrame(glist,columns=alpha1,index=['M','F'])

               og=[]
               for i in d_drop:
                    D=df.loc[df['program']==i]
                    d1=D['s_year'].value_counts().index.tolist()
                    og.append(d1)

               og1=[]
               for i in d_drop:
                    D1=df.loc[df['program']==i]
                    d2=D1['s_branch'].value_counts().index.tolist()
                    # d2.sort()
                    og1.append(d2)

               # mylist = zip(og,leng)
               
               yd= {year_drop[i-1]: i for i in range(1,len(year_drop)+1)}
               dd= {d_drop[i-1]: i for i in range(1,len(d_drop)+1)}

               return render_template("student.html",b_drop=b_drop,yd=yd,og=og,dd=dd,og1=og1,mc=mc,fc=fc,alpha1=alpha1,g_tables=[gtab.to_html(classes='data', header="true")],year_drop=year_drop,d_drop=d_drop,pg_year_count=pg_year_count,pg_years=pg_years,u=u,p=p,ph=ph,le_count=le_count,le_branch=le_branch,course_names=course_names,course_values=course_values,alpha=alpha,ug_branch=ug_branch,ug_branch_count=ug_branch_count,ug_years=ug_years,ug_year_count=ug_year_count,pg_branch=pg_branch,pg_branch_count=pg_branch_count,phd_branch=phd_branch,phd_branch_count=phd_branch_count,year_count_names=year_count_names,no=no,m=m,f=f,name=session['user'])
     else:
          return redirect(url_for('home'))


@app.route("/s_drop",methods=['GET','POST'])
def s_drop():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Student"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     s_year=res_Det['selected_dept']
     s_dept=res_Det['selected_year']
     s_branch=res_Det['selected_branch']


     drop = df.loc[df['s_year']==s_year]
     drop_data=drop.loc[df['program']==s_dept]
     drop_data=drop_data.loc[df['s_branch']==s_branch]
    
     
     f_values=drop_data['s_branch'].value_counts().tolist()
     f_names=drop_data['s_branch'].value_counts().index.tolist()

     g_values=drop_data['s_gender'].value_counts().tolist()
     g_names=drop_data['s_gender'].value_counts().index.tolist()

     m=drop_data.loc[drop_data['s_gender']=="M"]
     mc=m['Caste'].value_counts().sort_index().tolist()
     mc2=m['Caste'].value_counts().sort_index().index.tolist()

     f=drop_data.loc[drop_data['s_gender']=="F"]
     fc=f['Caste'].value_counts().sort_index().tolist()
     fc2=f['Caste'].value_counts().sort_index().index.tolist()

     ca= list(set(mc2) | set(fc2))
     print(ca)

     al = {ca[i-1]: i for i in range(1,len(ca)+1)}
     print(al)
     alpha=[]
     print(mc2)
     for i in al:
          if(i not in mc2):
               mc2.insert(al[i]-1,i)
               mc.insert(al[i]-1,0)
     print(mc)
     for i in al:
          if(i not in fc2):
               fc2.insert(al[i]-1,i)
               fc.insert(al[i]-1,0)

     for i in al:
          alpha.append(i)

     print(alpha)
     glist=[mc,fc]
     print(glist)
     gtab=pd.DataFrame(glist,columns=alpha,index=['M','F'])
     l=len(drop_data)
     drop_data.rename(columns = {'s_id':'Student ID', 's_course':'Student Course','program':'Student Program','s_branch':'Student Branch','s_year':'Year','s_gender':'Gender'}, inplace = True)
     c=0
     return render_template("s_drop.html",c=c,s_branch=s_branch,mc=mc,fc=fc,alpha=alpha,g_tables=[gtab.to_html(classes='data', header="true")],g_values=g_values,g_names=g_names,f_values=f_values,f_names=f_names,l=l,tables=[drop_data.to_html(classes='data', header="true",index_names=False, index=False)],s_year=s_year,s_dept=s_dept,name=session['user'])



@app.route("/students_mf",methods=['GET','POST'])
def students_mf():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               #s_course -> M,F
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               
               cat="Student"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)

               male_data=df.loc[df['s_gender']=='M']

               male_count=male_data['program'].value_counts().sort_index(ascending=True).tolist()
               male_values=male_data['program'].value_counts().sort_index(ascending=True).index.tolist()

               dff = pd.DataFrame(list(zip(male_values, male_count)),columns =['Program', 'Male Count'])


               return render_template("students_mf.html",tables=[dff.to_html(classes='data', header="true",index=False)],name=session['user'])
     else:
          return redirect(url_for('home'))



@app.route("/students_f",methods=['GET','POST'])
def students_f():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               #s_course -> M,F
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               
               cat="Student"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)

               female_data=df.loc[df['s_gender']=='F']

               female_count=female_data['program'].value_counts().sort_index(ascending=True).tolist()
               female_values=female_data['program'].value_counts().sort_index(ascending=True).index.tolist()

               dff = pd.DataFrame(list(zip(female_values, female_count)),columns =['Program', 'Female Count'])


               return render_template("students_f.html",tables=[dff.to_html(classes='data', header="true",index=False)],name=session['user'])
     else:
          return redirect(url_for('home'))



@app.route("/students_t",methods=['GET','POST'])
def students_t():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               #s_course -> M,F
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               
               cat="Student"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)

               tot_count=df['s_course'].value_counts().sort_index(ascending=True).tolist()
               tot_values=df['s_course'].value_counts().sort_index(ascending=True).index.tolist()

               dff = pd.DataFrame(list(zip(tot_values, tot_count)),columns =['Course', 'Student Count'])


               return render_template("students_t.html",tables=[dff.to_html(classes='data', header="true",index=False)],name=session['user'])
     else:
          return redirect(url_for('home'))



@app.route("/red",methods=['GET','POST'])
def red():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return render_template("user_dashy.html",name=session['user'])
     else:
          return redirect(url_for('home'))


@app.route("/das",methods=['GET','POST'])
def das():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return render_template("das.html",name=session['user'])
     else:
          return redirect(url_for('home'))


@app.route("/blue",methods=['GET','POST'])
def blue():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               return render_template("admin_dashy.html",name=session['user'])
          else:
               return render_template("mainpage.html")
     else:
          return redirect(url_for('home'))


@app.route("/faculty",methods=['GET','POST'])
def faculty():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Faculty"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               no=df.shape[0]
               p=df['f_course'].tolist().count('Prof')
               a=df['f_course'].tolist().count('Asst. Prof')
               ap=df['f_course'].tolist().count('Assoc Prof')

               pr_drop=df['Program'].value_counts().index.to_list()
               d_drop=df['f_branch'].value_counts().index.to_list()



               f_values=df['f_course'].value_counts().tolist()
               f_names=df['f_course'].value_counts().index.tolist()
               

               # f_year_count=df['f_year'].value_counts().tolist()
               # f_year_count_names=df['f_year'].value_counts().index.tolist()
               

               #IT -> f_course
               f_branch_data=df.loc[df['f_branch']=='Information Technology']
               f_courses=f_branch_data['f_course'].value_counts().tolist()
               f_courses_count=f_branch_data['f_course'].value_counts().index.tolist()

               #phd count -> branch wise
               phd_data=df.loc[df['phD']=='yes']
               doc=len(phd_data)
               phd_count=phd_data['f_branch'].value_counts().sort_index().tolist()
               phd_branch=phd_data['f_branch'].value_counts().sort_index().index.tolist()

               #f_course -> M,F
               male_data=df.loc[df['f_gender']=='M']

               male_count=male_data['f_course'].value_counts().sort_index(ascending=True).tolist()
               male_values=male_data['f_course'].value_counts().sort_index(ascending=True).index.tolist()

               female_data=df.loc[df['f_gender']=='F']
               female_count=female_data['f_course'].value_counts().sort_index(ascending=True).tolist()
               female_values=female_data['f_course'].value_counts().sort_index(ascending=True).index.tolist()

               al={'Assoc Prof':1, 'Asst. Prof':2, 'Prof':3}
               alpha=[]

               for i in al:
                    if(i not in male_values):
                         male_values.insert(al[i]-1,i)
                         male_count.insert(al[i]-1,0)

               for i in al:
                    if(i not in female_values):
                         female_values.insert(al[i]-1,i)
                         female_count.insert(al[i]-1,0)

               for i in al:
                    alpha.append(i)



                 
                         #dept.wise prof count
               prof_data=df.loc[df['f_course']=='Prof']
               prof_count=prof_data['f_branch'].value_counts().tolist()
               prof_branch=prof_data['f_branch'].value_counts().index.tolist()



               m1=df.loc[df['f_gender']=="M"]
               mc=m1['Caste'].value_counts().sort_index().tolist()
               mc2=m1['Caste'].value_counts().sort_index().index.tolist()

               f1=df.loc[df['f_gender']=="F"]
               fc=f1['Caste'].value_counts().sort_index().tolist()
               fc2=f1['Caste'].value_counts().sort_index().index.tolist()

               ca= list(set(mc2) | set(fc2))
               # print(ca)

               al1 = {ca[i-1]: i for i in range(1,len(ca)+1)}
            
               alpha1=[]
               # print(mc2)
               for i in al1:
                    if(i not in mc2):
                         mc2.insert(al1[i]-1,i)
                         mc.insert(al1[i]-1,0)
               # print(mc)
               for i in al1:
                    if(i not in fc2):
                         fc2.insert(al1[i]-1,i)
                         fc.insert(al1[i]-1,0)

               for i in al1:
                    alpha1.append(i)

               
               glist=[mc,fc]
             
               gtab=pd.DataFrame(glist,columns=alpha1,index=['M','F'])


               og=[]
               for i in pr_drop:
                    D=df.loc[df['Program']==i]
                    d1=D['f_branch'].value_counts().index.tolist()
                    og.append(d1)


               yd= {pr_drop[i-1]: i for i in range(1,len(pr_drop)+1)}
               return render_template("faculty.html",doc=doc,yd=yd,og=og,mc=mc,fc=fc,alpha1=alpha1,g_tables=[gtab.to_html(classes='data', header="true")],pr_drop=pr_drop,d_drop=d_drop,prof_count=prof_count,prof_branch=prof_branch,alpha=alpha,male_count=male_count,female_count=female_count,phd_count=phd_count,phd_branch=phd_branch,f_courses=f_courses,f_courses_count=f_courses_count,f_names=f_names,f_values=f_values,no=no,p=p,a=a,ap=ap,name=session['user'])
     else:
          return redirect(url_for('home'))



@app.route("/faculty_t",methods=['GET','POST'])
def faculty_t():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               
               cat="Faculty"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)

               tot_count=df['f_course'].value_counts().sort_index(ascending=True).tolist()
               tot_values=df['f_course'].value_counts().sort_index(ascending=True).index.tolist()

               dff = pd.DataFrame(list(zip(tot_values, tot_count)),columns =['Course', 'Faculty Count'])


               return render_template("faculty_t.html",tables=[dff.to_html(classes='data', header="true",index=False)],name=session['user'])
     else:
          return redirect(url_for('home'))





@app.route("/f_drop",methods=['GET','POST'])
def f_drop():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Faculty"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     s_pr=res_Det['selected_pr']
     s_dept=res_Det['selected_dept']

     drop = df.loc[df['Program']==s_pr]
     drop_data=drop.loc[df['f_branch']==s_dept]

     f_values=drop_data['f_course'].value_counts().tolist()
     f_names=drop_data['f_course'].value_counts().index.tolist()

     g_values=drop_data['f_gender'].value_counts().tolist()
     g_names=drop_data['f_gender'].value_counts().index.tolist()

     m=drop_data.loc[drop_data['f_gender']=="M"]
     mc=m['Caste'].value_counts().sort_index().tolist()
     mc2=m['Caste'].value_counts().sort_index().index.tolist()

     f=drop_data.loc[drop_data['f_gender']=="F"]
     fc=f['Caste'].value_counts().sort_index().tolist()
     fc2=f['Caste'].value_counts().sort_index().index.tolist()

     ca= list(set(mc2) | set(fc2))
     print(ca)

     al = {ca[i-1]: i for i in range(1,len(ca)+1)}
     print(al)
     alpha=[]
     print(mc2)
     for i in al:
          if(i not in mc2):
               mc2.insert(al[i]-1,i)
               mc.insert(al[i]-1,0)
     print(mc)
     for i in al:
          if(i not in fc2):
               fc2.insert(al[i]-1,i)
               fc.insert(al[i]-1,0)

     for i in al:
          alpha.append(i)

     print(alpha)
     glist=[mc,fc]
     print(glist)
     gtab=pd.DataFrame(glist,columns=alpha,index=['M','F'])
     l=len(drop_data)
     drop_data.rename(columns = {'f_name':'Faculty Name','f_course':'Faculty Designation','program':'Program','f_branch':'Faculty Branch','phD':'Ph.D','f_gender':'Gender'}, inplace = True)

     return render_template("f_drop.html",mc=mc,fc=fc,alpha=alpha,g_values=g_values,g_names=g_names,f_values=f_values,f_names=f_names,l=l,tables=[drop_data.to_html(classes='data', header="true",index_names=False, index=False)],g_tables=[gtab.to_html(classes='data', header="true")],s_pr=s_pr,s_dept=s_dept,name=session['user'])


@app.route("/consult",methods=['GET','POST'])
def consult():
     if(request.method=='POST'):
          
          res_excel=request.files['consult_excel']
          if(res_excel.filename!=""):
               filepath=os.path.join(app.config['UPLOAD_FOLDER'],res_excel.filename)
               res_excel.save(filepath)
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Consultancy Projects"
               ins_query="INSERT INTO data(category,file)VALUES(?,?)"
               data_values=(cat,res_excel.filename)
               cur.execute(ins_query,data_values)
               conn.commit()
               conn.close()
               return redirect(url_for('upload_data'))
          else:
               return redirect(url_for('upload_data'))

@app.route("/consultancy_viz",methods=['GET','POST'])
def consultancy_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Consultancy Engineering"
               cat1="Consultancy Pharmacy"
               #consultancy Engineering
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               #graph1
               gb1=df.groupby('year')['amount'].sum()
               gb1=pd.DataFrame(gb1)
               gb1_year=gb1.index.to_list()
               gb1_count=gb1['amount'].to_list()
               #graph2
               gb2=df.groupby('Client Organization')['amount'].sum()
               gbr=pd.DataFrame(gb2)
               gb2_cat=gbr.index.to_list()
               gb2_count=gbr['amount'].to_list()
               #consultancy pharmacy
               cur.execute("select file from data where category='"+cat1+"'")
               
               row1=cur.fetchall()
               
               for i in row1:
                    file_name1=i[0]
               def_path='static\excel_data_new'
               final_path1=os.path.join(def_path,file_name1)
               data1=pd.read_excel(final_path1)
               df=pd.DataFrame(data1)
               #graph1
               gb3=df.groupby('year')['amount'].sum()
               gb3=pd.DataFrame(gb3)
               gb3_year=gb3.index.to_list()
               gb3_count=gb3['amount'].to_list()
               #graph2
               gb4=df.groupby('Client Organization')['amount'].sum()
               gb4=pd.DataFrame(gb4)
               gb4_cat=gb4.index.to_list()
               gb4_count=gb4['amount'].to_list()
               return render_template("consultancy.html",gb3_year=gb3_year,gb3_count=gb3_count,gb2_cat=gb2_cat,gb2_count=gb2_count,gb4_cat=gb4_cat,gb4_count=gb4_count,gb1_year=gb1_year,gb1_count=gb1_count,name=session['user'])
     else:
          return redirect(url_for('home'))


@app.route("/programs",methods=['GET','POST'])
def programs():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Programs"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
              
               #dropdown
               year_drop=df['Year of Commencement'].value_counts().index.to_list()
               year_drop.sort(reverse=True)

               school=df['School'].value_counts().index.to_list()

               p=len(df['Program'].value_counts())
               d=len(df['Department'].value_counts())

               pr_count=df['Program'].value_counts().to_list()
               pr=df['Program'].value_counts().index.to_list()
               
               yr_count=df['Year of Commencement'].value_counts().to_list()
               yr=df['Year of Commencement'].value_counts().index.to_list()

               intake=df['Intake'].sum()

               return render_template("programs.html",intake=intake,yr_count=yr_count,yr=yr,pr_count=pr_count,pr=pr,p=p,d=d,year_drop=year_drop,school=school,name=session['user'])
     else:
          return redirect(url_for('home')) 


@app.route("/p_drop",methods=['GET','POST'])
def p_drop():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Programs"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     s_year=res_Det['selected_year']
     # s_dept=res_Det['selected_dept']

     drop_data = df.loc[df['Year of Commencement']==s_year]
          # drop=drop_data.loc[drop_data['Department']==s_dept]

     s_count=drop_data['School'].value_counts().to_list()
     s=drop_data['School'].value_counts().index.to_list()

     pr_count=drop_data['Program'].value_counts().to_list()
     pr=drop_data['Program'].value_counts().index.to_list()

     d_count=drop_data['Department'].value_counts().to_list()
     d=drop_data['Department'].value_counts().index.to_list()

     l=len(drop_data)
     return render_template("p_drop.html",d=d,d_count=d_count,pr=pr,pr_count=pr_count,s=s,s_count=s_count,l=l,tables=[drop_data.to_html(classes='data', header="true",index_names=False, index=False)],s_year=s_year,name=session['user'])

@app.route("/admissions",methods=['GET','POST'])
def admissions():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Admissions"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
              
               #dropdown
               year_drop=df['Year'].value_counts().index.to_list()
               year_drop.sort(reverse=True)

               # school=df['School'].value_counts().index.to_list()

               p=len(df['Program'].value_counts())
               d=df['Admitted'].sum()

               # yr_count=df['Year'].value_counts().to_list()
               # yr=df['Year'].value_counts().index.to_list()

               dept_group=df.groupby('Year')['Intake'].sum()
               dept_group=pd.DataFrame(dept_group)
               yr=dept_group.index.to_list()
               yr_count=dept_group['Intake'].to_list()

               dept_group2=df.groupby('Year')['Lateral Count'].sum()
               dept_group2=pd.DataFrame(dept_group2)
               lr=dept_group2.index.to_list()
               lr_count=dept_group2['Lateral Count'].to_list()

               dept_group1=df.groupby('Year')['Admitted'].sum()
               dept_group1=pd.DataFrame(dept_group1)
               yr1=dept_group1.index.to_list()
               yr_count1=dept_group1['Admitted'].to_list()

               return render_template("admissions.html",lr=lr,lr_count=lr_count,yr_count1=yr_count1,yr1=yr1,yr_count=yr_count,yr=yr,p=p,d=d,year_drop=year_drop,name=session['user'])
     else:
          return redirect(url_for('home')) 

@app.route("/a_drop",methods=['GET','POST'])
def a_drop():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Admissions"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     s_year=res_Det['selected_year']
     # s_dept=res_Det['selected_dept']

     drop_data = df.loc[df['Year']==s_year]
     int_data=drop_data.groupby('Program')['Intake'].sum()
     int_data=pd.DataFrame(int_data)
     dept_names=int_data.index.to_list()
     intake_amount=int_data['Intake'].to_list()

     ad_data=drop_data.groupby('Program')['Intake'].sum()
     ad_data=pd.DataFrame(ad_data)
     d_names=ad_data.index.to_list()
     ad_amount=int_data['Intake'].to_list()

     pr_count=drop_data['Program'].value_counts().to_list()
     pr=drop_data['Program'].value_counts().index.to_list()

     g=drop_data.loc[drop_data['Admitted percent']>90]
     gy=g['Admitted percent'].to_list()
     gx=g['Program'].to_list()

     
     le=drop_data['Lateral Count'].value_counts().index.to_list()

     l=len(drop_data)
     drop_data.rename(columns = {'Admitted percent':'Admitted %','Lateral Count':'Lateral Entry Count'}, inplace = True)


     return render_template("a_drop.html",le=le,gx=gx,gy=gy,ad_amount=ad_amount,d_names=d_names,intake_amount=intake_amount,dept_names=dept_names,pr=pr,pr_count=pr_count,l=l,tables=[drop_data.to_html(classes='data', header="true",index_names=False, index=False)],s_year=s_year,name=session['user'])


@app.route("/research",methods=['GET','POST'])
def research():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Research Grants"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               #1st graph bar chart
               dept_group=df.groupby('Department')['Sanctioned Project Amount'].sum()
               dept_group=pd.DataFrame(dept_group)
               dept_names=dept_group.index.to_list()
               sanc_amount=dept_group['Sanctioned Project Amount'].to_list()
               #3rd graph pie chart
               status=df['Status'].value_counts().index.to_list()
               status_count=df['Status'].value_counts().to_list()
               #4th graph line graph
               year_group=df.groupby('Year of Sanction')['Sanctioned Project Amount'].sum()
               year_group=pd.DataFrame(year_group)
               year=year_group.index.to_list()
               sanc_amount_year=year_group['Sanctioned Project Amount'].to_list()

               #5th graph horizontal bar chart
               agency_group=df.groupby('Funding Agency')['Sanctioned Project Amount'].sum()
               agency_group=pd.DataFrame(agency_group)
               agency=agency_group.index.to_list()
               sanc_amount_agency=agency_group['Sanctioned Project Amount'].to_list()
               

               #dropdown
               year_drop=df['Year of Sanction'].value_counts().index.to_list()
               year_drop.sort()

               dept=df['Department'].value_counts().index.to_list()



               # if request.method=='POST':
               #      dropDetails=request.form
               #      year_deets=dropDetails['output']
               # print(year_deets)

               og=[]
               for i in year_drop:
                    D=df.loc[df['Year of Sanction']==i]
                    d1=D['Department'].value_counts().index.tolist()
                    og.append(d1)

               yd= {year_drop[i-1]: i for i in range(1,len(year_drop)+1)}

               return render_template("research.html",yd=yd,og=og,year_drop=year_drop,dept=dept,agency=agency,sanc_amount_agency=sanc_amount_agency,year=year,sanc_amount_year=sanc_amount_year,dept_names=dept_names,sanc_amount=sanc_amount,status=status,status_count=status_count,name=session['user'])
     else:
          return redirect(url_for('home'))             



@app.route("/r_drop",methods=['GET','POST'])
def r_drop():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Research Grants"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     s_year=res_Det['selected_year']
     s_dept=res_Det['selected_dept']

     drop_data = df.loc[df['Year of Sanction']==s_year]
     drop=drop_data.loc[drop_data['Department']==s_dept]

     l=len(drop)
     inv=drop['Investigator'].value_counts().index.to_list()
     amt=drop['Sanctioned Project Amount'].to_list()
     agency=drop['Funding Agency'].value_counts().index.to_list()
     status=drop['Status'].value_counts().index.to_list()
     status_count=drop['Status'].value_counts().to_list()

     return render_template("abc.html",inv=inv,amt=amt,agency=agency,status=status,status_count=status_count,l=l,tables=[drop.to_html(classes='data', header="true",index_names=False, index=False)],drop_data=drop_data,drop=drop,s_year=s_year,s_dept=s_dept,name=session['user'])


@app.route("/depts",methods=['GET','POST'])
def research_depts():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Research Grants"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     
     dept_group=df.groupby('Department')['Sanctioned Project Amount'].sum()
     dept_group=pd.DataFrame(dept_group)
     dept_group_table=dept_group.reset_index()
     dept_group_table.index=dept_group_table.index+1
     dept_names=dept_group.index.to_list()
     sanc_amount=dept_group['Sanctioned Project Amount'].to_list()

     
     return render_template("depts.html",dept_names=dept_names, sanc_amount=sanc_amount,tables=[dept_group_table.to_html(classes='data', header="true",index=False)],name=session['user'])


@app.route("/agencies",methods=['GET','POST'])
def research_agencies():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Research Grants"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     
     agency_group=df.groupby('Funding Agency')['Sanctioned Project Amount'].sum()
     agency_group=pd.DataFrame(agency_group)
     agency_group_table=agency_group.reset_index()
     agency_group_table.index=agency_group_table.index+1
     agency=agency_group.index.to_list()
     sanc_amount_agency=agency_group['Sanctioned Project Amount'].to_list()


     
     return render_template("agencies.html",sanc_amount_agency=sanc_amount_agency,agency=agency,tables=[agency_group_table.to_html(classes='data', header="true",index=False)],name=session['user'])


@app.route("/p_programs",methods=['GET','POST'])
def p_programs():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Programs"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     
     pr_count=df['Program'].value_counts().to_list()
     pr=df['Program'].value_counts().index.to_list()
     df = pd.DataFrame(list(zip(pr, pr_count)),columns =['Program', 'Department Count'])

     return render_template("p_programs.html",pr_count=pr_count,pr=pr,tables=[df.to_html(classes='data', header="true",index=False)],name=session['user'])


@app.route("/a_programs",methods=['GET','POST'])
def a_programs():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Admissions"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     
     dept_group=df.groupby('Program')['Intake'].sum()
     dept_group=pd.DataFrame(dept_group)
     dept_group_table=dept_group.reset_index()
     dept_group_table.index=dept_group_table.index+1

     return render_template("a_programs.html",tables=[dept_group_table.to_html(classes='data', header="true",index=False)],name=session['user'])



@app.route("/a_admitted",methods=['GET','POST'])
def a_admitted():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Admissions"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     
     dept_group=df.groupby('Program')['Admitted'].sum()
     dept_group=pd.DataFrame(dept_group)
     dept_group_table=dept_group.reset_index()
     dept_group_table.index=dept_group_table.index+1

     return render_template("a_admitted.html",tables=[dept_group_table.to_html(classes='data', header="true",index=False)],name=session['user'])



@app.route("/p_depts",methods=['GET','POST'])
def p_depts():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Programs"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     
     d_count=df['Department'].value_counts().index.to_list()
     d=df['Year of Commencement'].value_counts().index.to_list()
     # df = pd.DataFrame(list(zip(d_count,d)),columns =['Department', 'Year of Commencement'])

     dff=df[['Program','Department','Year of Commencement']]
     return render_template("p_depts.html",d_count=d_count,d=d,tables=[dff.to_html(classes='data', header="true",index=False)],name=session['user'])


@app.route("/p_intake",methods=['GET','POST'])
def p_intake():

     conn=sqlite3.connect("dash.db")
     cur=conn.cursor()
     cat="Programs"
     cur.execute("select file from data where category='"+cat+"'")
     row=cur.fetchall()
     for i in row:
          file_name=i[0]
     def_path='static\excel_data_new'
     final_path=os.path.join(def_path,file_name)
     data=pd.read_excel(final_path)
     df=pd.DataFrame(data)
     res_Det=request.form
     

     dept_group=df.groupby('Year of Commencement')['Intake'].sum()
     dept_group=pd.DataFrame(dept_group)
     dept_group_table=dept_group.reset_index()
     dept_group_table.index=dept_group_table.index+1
     # dept_group=df.groupby('Year of Commencement')['Intake'].sum()
     # dept_group=pd.DataFrame(dept_group)
     # # dept_names=dept_group.index.to_list()
     # sanc_amount=dept_group['Intake'].to_list()

     # d_count=df['Department'].value_counts().index.to_list()
     # d=df['Year of Commencement'].value_counts().index.to_list()
     # # df = pd.DataFrame(list(zip(d_count,d)),columns =['Department', 'Year of Commencement'])

     # dff=df[['Program','Department','Year of Commencement']]
     return render_template("p_intake.html",tables=[dept_group_table.to_html(classes='data', header="true",index=False)],name=session['user'])



@app.route("/support",methods=['GET','POST'])
def support():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               
               cat="Support Staff"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)

               no=df.shape[0]
               t=df['Category'].tolist().count('Technical')
               a=df['Category'].tolist().count('Admin')

               #Tech -> Desig
               tech_desig_data=df.loc[df['Category']=='Technical']
               tech_desig_count=tech_desig_data['Designation'].value_counts().tolist()
               tech_desig=tech_desig_data['Designation'].value_counts().index.tolist()

               #Admin -> Desig
               admin_desig_data=df.loc[df['Category']=='Admin']
               admin_desig_count=admin_desig_data['Designation'].value_counts().tolist()
               admin_desig=admin_desig_data['Designation'].value_counts().index.tolist()
               print(admin_desig_count,admin_desig)
               
               #Category -> M,F
               male_data=df.loc[df['Gender']=='M']
               male_count=male_data['Category'].value_counts().sort_index(ascending=True).tolist()
               male_values=male_data['Category'].value_counts().sort_index(ascending=True).index.tolist()


               female_data=df.loc[df['Gender']=='F']
               female_count=female_data['Category'].value_counts().sort_index(ascending=True).tolist()
               female_values=female_data['Category'].value_counts().sort_index(ascending=True).index.tolist()

               al={'Admin':1,'Technical':2}
               alpha=[]

               for i in al:
                    if(i not in male_values):
                         male_values.insert(al[i]-1,i)
                         male_count.insert(al[i]-1,0)

               for i in al:
                    if(i not in female_values):
                         female_values.insert(al[i]-1,i)
                         female_count.insert(al[i]-1,0)

               for i in al:
                    alpha.append(i)


               return render_template("support.html",no=no,t=t,a=a,male_count=male_count,female_count=female_count,alpha=alpha,tech_desig_count=tech_desig_count,tech_desig=tech_desig,admin_desig_count=admin_desig_count,admin_desig=admin_desig,name=session['user'])
          else:
               return redirect(url_for('home'))


@app.route("/it_viz",methods=['GET','POST'])
def it_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="IT Publications"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               #graph1
               dept_group=df.groupby('Publication Year')['category'].count()
               dept_group=pd.DataFrame(dept_group)
               year=dept_group.index.to_list()
               count=dept_group['category'].to_list()
               #graph2
               gb2=df.groupby('category').count()
               gbr=pd.DataFrame(gb2)
               category=gb2.index.to_list()
               c_count=gb2['S.No'].to_list()
               #graph3
               gb4=df.groupby('Journal')['category'].count()
               gb4=pd.DataFrame(gb4)
               
               journal=gb4.index.to_list()
               j_count=gb4['category'].to_list()
               return render_template("it_pub.html",journal=journal,j_count=j_count,year=year,count=count,category=category,c_count=c_count,name=session['user'])
     else:
          return redirect(url_for('home'))     

@app.route("/cse_viz",methods=['GET','POST'])
def cse_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="CSE Publications"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               #graph1
               gb1=df.groupby('year')['category'].count()
               gb1=pd.DataFrame(gb1)
               gb1_year=gb1.index.to_list()
               gb1_count=gb1['category'].to_list()

               #graph2
               gb2=df.groupby('category').count()
               gb2=pd.DataFrame(gb2)
               gb2_cat=gb2.index.to_list()
               gb2_count=gb2['S.No'].to_list()

               #graph3

               gb4=df.groupby('journal')['S.No'].count()
               gb4=pd.DataFrame(gb4)
               gb4_journal=gb4.index.to_list()
               gb4_count=gb4['S.No'].to_list()
               return render_template("cse_pub.html",gb1_year=gb1_year,gb1_count=gb1_count,gb2_cat=gb2_cat,gb2_count=gb2_count,gb4_journal=gb4_journal,gb4_count=gb4_count,name=session['user'])
     else:
          return redirect(url_for('home'))     

@app.route("/ece_viz",methods=['GET','POST'])
def ece_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="ECE Publications"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data) 
               #graph1
               gb1=df.groupby('year')['category'].count()
               gb1=pd.DataFrame(gb1)
               gb1_year=gb1.index.to_list()
               gb1_count=gb1['category'].to_list()
               gb1_year=gb1_year[0:5]
               gb1_count[1]=gb1_count[1]+3
               gb1_count[2]=gb1_count[2]+1
               gb1_count=gb1_count[0:5]
               # graph2
               gb2=df.groupby('category').count()
               gbr=pd.DataFrame(gb2)
               gb2_cat=gb2.index.to_list()
               gb2_count=gb2['S.No'].to_list()
               # graph3
               gb4=df.groupby('journal').count()
               gb4=pd.DataFrame(gb4)
               gb4=df.groupby('journal')['Publication'].count()
               gb4=pd.DataFrame(gb4)
               gb4=gb4[gb4.Publication>2]
               gb4_journal=gb4.index.to_list()
               gb4_count=gb4['Publication'].to_list()
               return render_template("ece_pub.html",gb4_journal=gb4_journal,gb4_count=gb4_count,gb1_year=gb1_year,gb1_count=gb1_count,gb2_cat=gb2_cat,gb2_count=gb2_count,name=session['user'])

     else:
          return redirect(url_for('home'))  

@app.route("/eee_viz",methods=['GET','POST'])
def eee_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="EEE Publications"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data) 
               #graph1
               gb1=df.groupby('year')['category'].count()
               gb1=pd.DataFrame(gb1)
               gb1_year=gb1.index.to_list()
               gb1_count=gb1['category'].to_list()
               #graph2
               gb2=df.groupby('category').count()
               gbr=pd.DataFrame(gb2)
               gb2_cat=gb2.index.to_list()
               gb2_count=gb2['S.No'].to_list()
               #graph3
               gb4=df.groupby('Journal')['S.No'].count()
               gb4=pd.DataFrame(gb4)
               gb4_journal=gb4.index.to_list()
               gb4_count=gb4['S.No'].to_list()
               return render_template("eee_pub.html",gb2_cat=gb2_cat,gb2_count=gb2_count,gb4_journal=gb4_journal,gb4_count=gb4_count,gb1_year=gb1_year,gb1_count=gb1_count,name=session['user'])
     else:
          return redirect(url_for('home'))

@app.route("/mech_viz",methods=['GET','POST'])
def mech_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Mechanical Publications"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               #graph1
               gb1=df.groupby('year')['category'].count()
               gb1=pd.DataFrame(gb1)
               gb1_year=gb1.index.to_list()
               gb1_count=gb1['category'].to_list()
               #graph2
               gb2=df.groupby('category').count()
               gbr=pd.DataFrame(gb2)
               gb2_cat=gb2.index.to_list()
               gb2_count=gb2['S.No'].to_list()
               #graph3
               gb4=df.groupby('journal')['Publication'].count()
               gb4=pd.DataFrame(gb4)
               gb4=gb4[gb4.Publication>1]
               gb4_journal=gb4.index.to_list()
               gb4_count=gb4['Publication'].to_list()
               return render_template("mech_pub.html",gb2_cat=gb2_cat,gb2_count=gb2_count,gb4_journal=gb4_journal,gb4_count=gb4_count,gb1_year=gb1_year,gb1_count=gb1_count,name=session['user'])
     else:
          return redirect(url_for('home'))

@app.route("/chem_viz",methods=['GET','POST'])
def chem_viz():
     if 'user' in session:
          g.user=session['user']
          if(g.user):
               conn=sqlite3.connect("dash.db")
               cur=conn.cursor()
               cat="Chemical Publications"
               cur.execute("select file from data where category='"+cat+"'")
               row=cur.fetchall()
               for i in row:
                    file_name=i[0]
               def_path='static\excel_data_new'
               final_path=os.path.join(def_path,file_name)
               data=pd.read_excel(final_path)
               df=pd.DataFrame(data)
               #graph1
               gb1=df.groupby('year')['category'].count()
               gb1=pd.DataFrame(gb1)
               gb1_year=gb1.index.to_list()
               gb1_count=gb1['category'].to_list()
               #graph2
               gb2=df.groupby('category').count()
               gbr=pd.DataFrame(gb2)
               gb2_cat=gb2.index.to_list()
               gb2_count=gb2['S.No'].to_list()
               #graph3
               gb4=df.groupby('journal')['S.No'].count()
               gb4=pd.DataFrame(gb4)
               gb4_journal=gb4.index.to_list()
               gb4_count=gb4['S.No'].to_list()
               return render_template("chem_pub.html",gb2_cat=gb2_cat,gb2_count=gb2_count,gb4_journal=gb4_journal,gb4_count=gb4_count,gb1_year=gb1_year,gb1_count=gb1_count,name=session['user'])
     else:
          return redirect(url_for('home'))
@app.route("/insert_user",methods=['GET','POST'])
def insert_user():
     if request.method=='POST':
          print("hi")
          conn=sqlite3.connect("dash.db")
          cur=conn.cursor()
          userDetails=request.form
          u_name=userDetails['user_name']
          u_email=userDetails['user_email']
          u_pass=userDetails['user_pass']
          u_desig=userDetails['user_desig']
          insert_query="INSERT INTO users(u_email,u_name,u_pass,u_desig)VALUES(?,?,?,?)"
          values=(u_email,u_name,u_pass,u_desig)
          cur.execute(insert_query,values)
          cur.close()
          conn.commit()
          conn.close()
          return render_template("add_user.html")
          
     pass


if __name__=="__main__":
     app.secret_key='1234'
     app.run(debug=True)
     