#run this file to create and populate a db with some dummy values
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from app import db
from app.models import User, Task

USERS = [ {'username':'JamesBond', 'pw':'python', 'email':'James007@mi6.gov'}, 
		  {'username':'PhilIvey', 'pw':'javascript', 'email':'polarizing@ft.com'},
		  {'username':'KeiserSoze', 'pw':'ruby', 'email':'kevinspacey@gmail.com'},
		  {'username':'Bowser', 'pw':'haskell', 'email':'bowser@nes.com'} ]

TASKS = [ { 'title':'go to store','body':'pick up some koolaid'},
		  { 'title':'omaha', 'body':' repot dbl suit aces' },                         
		  { 'title':'REST up', 'body':'be stateless'},
		  { 'title':'birthday party', 'body':'buy some gifts'} ]

def reset_db():
	db.drop_all()
	db.create_all()

def set_users():
	for user in USERS:
		try: 	
			db.session.add(User(username=user["username"],email=user['email']))
		except:
			print "error creating users"
			break
	db.session.commit()

	for user in USERS:
		try:
			x = User.query.filter_by(username=user["username"]).first()
			x.hash_password(user["pw"])
		except:
			print "error setting passwords"
			break
	db.session.commit()

def set_tasks():
	for i in range(1,5):
		for task in TASKS:
			try:
				newTask = Task(title=task["title"],
							   body=task["body"],
							   user_id=i)
				db.session.add(newTask)
				db.session.commit()
			except:
				print "error populating tasks"

if __name__=='__main__':
	reset_db()
	set_users()
	set_tasks()

