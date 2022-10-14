from models import (Base, session, engine, Product)

import sqlalchemy

import datetime

import csv


def add_csv(filename):
	"""adds products in csv file into database"""
	with open(filename) as csvfile:
		inventory = csv.reader(csvfile)
		next(csvfile)
		for item in inventory:
			db_product = session.query(Product).filter(Product.product_name == item[0]).one_or_none()
			csv_product_name = item[0]
			product_price = clean_price(item[1])
			product_quantity = clean_quantity(item[2])
			product_date_updated = clean_date(item[3])
			update_inventory = Product(product_name=csv_product_name, product_quantity=product_quantity, product_price=product_price, date_updated=product_date_updated)
			if db_product == None:	
				session.add(update_inventory)
			else:
				db_product_date_updated = datetime.datetime.strptime(str(db_product.date_updated), '%Y-%m-%d')
				if db_product_date_updated < update_inventory.date_updated:
					session.add(update_inventory)
					session.delete(db_product)
				if db_product_date_updated > update_inventory.date_updated:
					pass
		session.commit()
			

def clean_price(price_string):##
	"""cleans string for easy use"""
	return int(float(price_string.split('$')[1]) * 100)


def clean_quantity(quantity_string):
	"""cleans quantity for easy use"""
	return int(quantity_string)


def clean_date(date_string):
	"""turns date string into a datetime"""
	split_date = date_string.split('/')
	month = int(split_date[0])
	day = int(split_date[1])
	year = int(split_date[2])
	date = datetime.datetime(year=year, month=month, day=day)
	return date 


def menu():
	"""where user interacts with the program"""
	print("Options:")
	print("(v) view product details\n(a) add new product to the database\n(b) make a backup of the database contents")
	running = True
	while running:
		user_input = input("What do you want to do?--> ").lower()
		if user_input == "v":
			view_product()
		if user_input == "a":
			add_new_product()
		if user_input == "b":
			backup()
		else:
			print("Please enter (v, a, b):\n(v) view product details\n(a) add new product to the database\n(b) make a backup of the database contents")
			continue


def view_product():
	"""allows the user to view aspects of a product""" 
	while True:
		print("Enter (menu) to go back to main menu!")
		user_input = input("Enter product ID number to view product information--> ").lower()
		if user_input == "menu":
			break
		if user_input.isalpha() == True:
			print("Please enter a number ")
			continue
		try:
			for item in session.query(Product):
				user_item =session.query(Product).filter(Product.product_id==user_input).one()
			print(f"\nProduct id: {user_item.product_id}\nProduct name: {user_item.product_name}\nProduct price: {user_item.product_price/100}\nProduct quantity: {user_item.product_quantity}\nDate updated: {user_item.date_updated}\n")
		except sqlalchemy.exc.NoResultFound:
			print("There are no products with that id number")


def add_new_product():
	"""allows user to add new products to the database"""
	while True:
		new_name = input("Enter the new products name: ")
		break
	while True:
		try:
			new_price = input("Enter the new products price: ")
			new_price = clean_price('$' + str(new_price))
		except ValueError:
			print("Please enter a number!")
			continue
		else:
			break
	while True:
		try:
			new_quantity = input("Enter the new products quantity: ")
			new_quantity = clean_quantity(new_quantity)
		except ValueError:
			print("Please enter a number")
			continue
		else:
			break
	while True:
		try:
			new_date_updated = input("Enter the date updated (month/day/four digit year): ")
			new_date_updated = clean_date(new_date_updated)
		except (ValueError, IndexError):
			print("Please enter a date in the format (12/22/1998): ")
			continue
		else:
			break
	add_product = input(f"Add Name: {new_name} Price: {new_price/100} Quantity: {new_quantity} Date: {new_date_updated} to the database (y/n)? ").lower()
	if add_product == 'y':
		new_product = Product(product_name=new_name, product_price=new_price, product_quantity=new_quantity, date_updated=new_date_updated)
		one_or_none = session.query(Product).filter(Product.product_name==new_name).one_or_none()
		if one_or_none == None:
			session.add(new_product)
			session.commit()
		if one_or_none != None:
			one_or_none_datetime = datetime.datetime.strptime(str(one_or_none.date_updated), '%Y-%m-%d')
			if new_date_updated > one_or_none_datetime:
				one_or_none.product_name = new_name
				one_or_none.product_price = new_price
				one_or_none.product_quantity = new_quantity
				one_or_none.date_updated = new_date_updated
				session.commit()
				print("product added!")
			else:
				while True:
					add = input("A product updated on {} is on file, replace it?(y/n) ".format(one_or_none.date_updated)).lower()
					if add == 'y':
						one_or_none.product_name = new_name
						one_or_none.product_price = new_price
						one_or_none.product_quantity = new_quantity
						one_or_none.date_updated = new_date_updated
						session.commit()
						print("product added!")
						break
					if add =='n':
						break
					else:
						print("please enter y or n")
						continue
	another_product = input("Do you want to add another product? (y/n) ").lower()
	if another_product == 'y':
		add_new_product()			


def backup():
	"""creates a backup file using information from the database"""
	with open('backup.csv', 'w') as csvfile:
		fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_updated']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for item in session.query(Product):
			writer.writerow({'product_name': item.product_name, 'product_price': '$'+(str(item.product_price/100)), 'product_quantity': item.product_quantity, 'date_updated': item.date_updated})
		print("File has been backed up!!!")


if __name__ == "__main__":
	Base.metadata.create_all(engine)
	add_csv('inventory.csv')
	menu()
