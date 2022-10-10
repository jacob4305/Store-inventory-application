from models import (Base, session, engine, Product)
import sqlalchemy
import datetime
import csv

#figure out how to keep it from adding repeating items to the database!!!!!!!
def add_csv(filename):
	with open(filename) as csvfile:
		inventory = csv.reader(csvfile)
		next(csvfile)
		for item in inventory:
			#print(item)
			product_name = item[0]
			product_price = clean_price(item[1])
			product_quantity = clean_quantity(item[2])
			product_date_updated = clean_date(item[3])
			#print(product_name, product_price, product_quantity, product_date_updated)

			#update_inventory = Product(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=product_date_updated)
			#session.add(update_inventory)
			#session.commit()

def clean_price(price_string):
	return float(price_string.split('$')[1]) * 100


def clean_quantity(quantity_string):
	return int(quantity_string)


def clean_date(date_string):
	split_date = date_string.split('/')
	month = int(split_date[0])
	day = int(split_date[1])
	year = int(split_date[2])
	date = datetime.date(year, month, day)
	return date 


def menu():
	print("Options:")
	print("(v) view product details\n(a) add new product to the database\n(b) make a backup of the database contents")
	running = True
	while running:
		user_input = input("What do you want to do?--> ").lower()
		if user_input == "v":
			view_product()
		if user_input == "a":
			pass
		if user_input == "b":
			pass
		else:
			print("Please enter (v, a, b):\n(v) view product details\n(a) add new product to the database\n(b) make a backup of the database contents")
			continue

def view_product():
	while True:
		print("Enter (menu) to go back to main menu!")
		user_input = input("Enter product ID to view product information--> ").lower()
		if user_input == "menu":
			break
		try:
			for item in session.query(Product):
				user_item =session.query(Product).filter(Product.product_id==user_input).one()
			print(f"\nProduct id: {user_item.product_id}\nProduct name: {user_item.product_name}\nProduct quantity: {user_item.product_quantity}\nDate updated: {user_item.date_updated}\n")
		except sqlalchemy.exc.NoResultFound:
			print("Product id not found")

def add_new_product():
	while True:
		start = input("Add new product to database? (y/n): ")
		if start == "n":
			break
		if start == "y":
			new_name = input("Enter the new products name: ")
			new_price = input("Enter the new products price: ")
			new_price = clean_price(new_price)
			new_quantity = input("Enter the new products quantity: ")
			new_quantity = clean_quantity(new_quantity)
			new_date_updated = input("Enter the date updated: ")
			new_date_updated = clean_date(new_date_updated)
			new_product = Product(product_name=new_name, product_price=new_price, product_quantity=new_quantity, date_updated=new_date_updated)
			print(new_product)
		else:
			print("Please enter (y) to add new product to database or (n) exit to main menu")




if __name__ == "__main__":
	Base.metadata.create_all(engine)
	add_csv('inventory.csv')
	menu()
	#clean_csv_price('$7.41')
	#clean_csv_date('3/10/2018')
	#for i in session.query(Product):
		#session.delete(i)
		#session.commit()