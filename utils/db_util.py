#run this file to create and populate a db with some dummy values
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from api import db
from api.models.users import User
from api.models.tasks import Task
from api.models.groups import Group, Company


def reset_db():
	db.drop_all()
	db.create_all()

def create_companys():
	company1 = Company(name="Chocolate.Factory",
					   website="www.site.com")
	company2 = Company(name="Larchmont Nurseries",
					   website="www.larchmontnurseries.com")
	db.session.add(company1)
	db.session.add(company2)
	db.session.commit()
	print "# Companies created.."

def create_groups():
	group1 = Group(name="Loompas", company_id=1,
				  createdOn=datetime.now(),
				  description="Mix the chocolate")
	group2 = Group(name="Oompas", company_id=1,
				  createdOn=datetime.now(),
				  description="Gum research")
	group3 = Group(name="Gardeners", company_id=2,
				  createdOn=datetime.now(),
				  description="Landscaping duties")
	group4 = Group(name="Floor Staff", company_id=2,
				  createdOn=datetime.now(),
				  description="Assist customers")
	db.session.add(group1)
	db.session.add(group2)
	db.session.add(group3)
	db.session.add(group4)
	db.session.commit()
	print "# Groups created.."

def create_tasks():
	try:
		task1 = Task(title="Mash cocoa beans",
					 body="Make Chocolate!",
					 group_id=1, createdOn=datetime.now())
		task2 = Task(title="Side-effects mitigation",
					 body="Fix swelling reaction some people have",
					 group_id=2, createdOn=datetime.now())	
		task3 = Task(title="Test flavors",
					 body="Create new flavors",
					 group_id=2, createdOn=datetime.now())	
		task4 = Task(title="Trim hedges on coligni ave",
					 body="Reponsible for houses 321, 326, 327",
					 group_id=3, createdOn=datetime.now())
		task5 = Task(title="Fertilizer shipment",
					 body="Delivery at 9:00am tuesday.",
					 group_id=4, createdOn=datetime.now())
		db.session.add(task1)
		db.session.add(task2)
		db.session.add(task3)
		db.session.add(task4)
		db.session.add(task5)
		db.session.commit()		
		print "# Tasks created..."	
	except Exception as err:
		print "-- Task creation failed.."
		print err	 					 	

def create_users():
	user1 = User(username="Wonka", email="wonka@wonka.com",
				rank="Admin", company_id=1)
	user2 = User(username="Bob", email="Bob@wonka.com",
				rank="employee", company_id=1)
	user3 = User(username="Ed", email="Ed@wonka.com",
				rank="manager", company_id=1)
	user4 = User(username="Andy", email="Andy@lnurseries.com",
				rank="employee", company_id=2)
	user5 = User(username="Joanna", email="Joanna@lnurseries.com",
				rank="Admin", company_id=2)
	user6 = User(username="Doug", email="Doug@lnurseries.com",
				rank="employee", company_id=2)
	db.session.add(user1)
	db.session.add(user2)
	db.session.add(user3)
	db.session.add(user4)
	db.session.add(user5)
	db.session.add(user6)
	db.session.commit()
	print "# Users created..."

def assign_users_to_groups():
	try:


		#company1
		a = User.query.filter_by(id=1).first()
		b = User.query.filter_by(id=2).first()
		c = User.query.filter_by(id=3).first()
		#company2
		d = User.query.filter_by(id=4).first()
		e = User.query.filter_by(id=5).first()
		f = User.query.filter_by(id=6).first()
		#company1:
		g = Group.query.filter_by(id=1).first()
		h = Group.query.filter_by(id=2).first()
		#company2:
		i = Group.query.filter_by(id=3).first()
		j = Group.query.filter_by(id=4).first()

		g.members.extend([a,b,c])
		h.members.extend([b,c])
		i.members.extend([d,e,f])
		j.members.extend([d,e])

		db.session.add(g)
		db.session.add(h)
		db.session.add(i)
		db.session.add(j)
		db.session.commit()
		print "## Group assignment successful"
	except Exception as err:
		print "-- Group assignment failed.."
		print err

def assign_tasks():
	try:
		#company1
		a = User.query.filter_by(id=1).first()
		b = User.query.filter_by(id=2).first()
		c = User.query.filter_by(id=3).first()
		#company2
		d = User.query.filter_by(id=4).first()
		e = User.query.filter_by(id=5).first()
		f = User.query.filter_by(id=6).first()

		task1 = Task.query.filter_by(id=1).first()
		a.tasks.append(task1)
		b.tasks.append(task1)
		c.tasks.append(task1)
		task2 = Task.query.filter_by(id=2).first()
		task3 = Task.query.filter_by(id=3).first()
		b.tasks.extend([task2, task3])
		c.tasks.extend([task2, task3])

		task4 = Task.query.filter_by(id=4).first()
		task5 = Task.query.filter_by(id=5).first()
		d.tasks.extend([task4, task5])
		e.tasks.extend([task4, task5])
		f.tasks.append(task4)

		db.session.add(a)
		db.session.add(b)
		db.session.add(c)
		db.session.add(d)
		db.session.add(e)
		db.session.add(f)
		db.session.commit()
		print "## Task assignment successful"
	except Exception as err:
		print "-- Task assignment failed.."
		print err


if __name__=='__main__':
	reset_db()
	create_companys()
	create_groups()
	create_users()
	create_tasks()
	assign_users_to_groups()
	assign_tasks()



	

