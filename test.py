from itertools import count
import sqlite3
from numpy import insert
import pandas as pd
from flask import Flask, request, flash,redirect,render_template, url_for,session,g

import os
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

s_year="II year"
s_dept="B.Tech"
drop = df.loc[df['s_year']==s_year]
drop_data=drop.loc[df['program']==s_dept]
# drop_data=drop_data.loc[df['s_branch']==s_branch]

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

print(drop_data,l)