import time 		
import traceback  # ERROR REPORTS
import getpass 	  # HIDE PASSWORD
import os		  
import mysql.connector as mcn
from prettytable import PrettyTable
pet = PrettyTable()  

mydb = mcn.connect(
	host = "localhost",
	user = "root",
	passwd = "password",
	database = "ims")

def title():
	os.system( 'clear' )  # CLEAN THE TERMINAL SCREEN 
	print("\033[1;35m\t**********************************")
	print("\t*****   SUNSHINE RETAILERS   *****")
	print("\t**** 182 - K Barra-8, Kanpur  ****")
	print("\t***  GSTIN - 22AAGFC9527Q1ZW   ***")
	print("\t**  Inventory Management System **")
	print("\t**********************************\033[1;37m")

def mainmenu():   # MAIN MENU
	print("\nPlease select an option -")
	print('''1. Purchase Entry
2. Sale Entry
3. Calculations and Statistics
4. View Inventory  ''')
	return int( input( "\n\033[1;35m>> \033[37m" ))

def pwd():  # AUTHENTICATION 
	pswdinp = getpass.getpass( prompt="\nAdmin Password : " ) # HIDES THE INPUT
	if pswdinp == '1023':
		return True	
	else:
		print("\r\033[31mInvalid Password!")
		time.sleep(1)
		return False
		  # PROGRAM TERMINATED

def menu3(): # CALCULATION AND STATS MENU
	print()
	print("Calculation and Statistics Module - ")
	print("1. Revenue ")
	print("2. Product Wise Reports")
	print("3. Back")
	return int(input("\n\033[1;35m>> \033[1;37m"))


def inventory():
	try:
		csr = mydb.cursor()
		print()
		print("Inventory")

		final = [[],[]]
		pr_qt = {}
		sl_qt = [[],[]]
		csr.execute("SELECT Name, Quantity FROM sale")
		sl_get = csr.fetchall()
		for sg in sl_get:
			
			sl_qt[0].append( str(sg[0]) )
			sl_qt[1].append( int(sg[1]) )

		csr.execute("SELECT Name, Quantity FROM purchase")
		pur_get = csr.fetchall()
		for pg in pur_get:
			final[0].append( str(pg[0]) )
			k = str(pg[0])
			v = int(pg[1])
			pr_qt[k] = v

		for i in pr_qt.keys():
			if i in sl_qt[0]:
				val = sl_qt[0].index(i)
				pr_qt[i] = pr_qt[i] - sl_qt[1][val]

		for i in pr_qt.keys():
			final[1].append(pr_qt[i])

		pet = PrettyTable()
		pet.field_names = (["Name", "Available Quantity"])
		pet.align['Name'] = 'l'
		pet.align['Available Quantity'] = 'r'
		for i in range( len(final[0]) ):
			rows  = [ final[0][i], final[1][i] ]
			pet.add_row(rows)

		print(pet)
			
		print()
		input("\033[5;33mpress any key to continue\033[0;37m")
	except Exception as e:
		print(e)
		print("TIP: open sales module")
		print("\033[5;31;40mAn error occured!\033[1;37m")
		input("\033[5;33mpress any key to continue\033[0;37m")

def productreport():
	try:
		csr = mydb.cursor()
		print()
		print("Product wise Reports")
	
		prod_enq = input("enter name -- ")
		pe_cap = prod_enq.upper()
		product_summary =[]

		csr.execute(f"SELECT Cost_Price, Quantity, Date FROM purchase WHERE Name ='{pe_cap}' ")
		pe_frompurchase_get = csr.fetchall()
		for pe in pe_frompurchase_get:
			product_summary.append( float(pe[0]) )
			product_summary.append( int(pe[1]) )
			product_summary.append( str(pe[2]) )

		csr.execute(f"SELECT Sale_Price, Quantity FROM sale WHERE Name = '{pe_cap}' ")
		pe_fromsale_get = csr.fetchall()
		for pe2 in pe_fromsale_get:
			product_summary.append( float(pe2[0]) )
			product_summary.append( int(pe2[1]) )

		pet = PrettyTable(border=False, header=False, padding_width=2)
		pet.vertical_char = '\033[1m:\033[1m'
		pet.junction_char = '\033[1m*\033[1m'
		pet.horizontal_char = '\033[1m~\033[1m'
		pet.field_names = ["Item", "Data"]
		pet.align["Item"] = 'r'
		pet.align["Data"] = 'l'
		print()

		if len( product_summary ) == 5:
			pet.add_row(["PRODUCT NAME :", prod_enq])
			pet.add_row(["LAST PURCHASE DATE :", product_summary[2]])
			pet.add_row(["COST PRICE :", product_summary[0]])
			pet.add_row(["QUANTITY PURCHASED :", product_summary[1]])
			pet.add_row(["SALE PRICE :", product_summary[3]])
			pet.add_row(["QUANTITY SOLD :", product_summary[4]])
			print(pet)
		elif len( product_summary ) == 3:
			pet.add_row(["PRODUCT NAME :", prod_enq])
			pet.add_row(["LAST PURCHASE DATE :", product_summary[2]])
			pet.add_row(["COST PRICE :", product_summary[0]])
			pet.add_row(["QUANTITY PURCHASED :", product_summary[1]])
			pet.add_row(["SALES :", "None"])
			print(pet)
		else:
			print("The Product could not be found in the Database.")

		print()
		input("\033[5;33mpress any key to continue\033[0;37m")
	except Exception as e:
		print(e)
		print("\033[5;31;40mAn error occured!\033[0;37m")
		input("\033[5;33mpress any key to continue\033[0;37m")

def pmod():	
	try: 	                # HANDLE EXCEPTIONS IF ANY
		csr = mydb.cursor() # CURSOR INITIALISED; HAS TO BE INIITALISED INSIDE FUNCTION
		try:                # CREATE PURCHASE TABLE IF NOT PRESENT
			csr.execute(
            "CREATE TABLE purchase(Name varchar(50) primary key,Quantity int(9) not null,Cost_Price decimal(9, 2) not null,Date date)")

			print("\033[33mPurchase Database Created Successfully\033[37m")
		except BaseException: # IF TABLE ALREADY EXISTS CONTINUE
			print("\033[33mPurchase Database Initialised\033[37m")

		print("\n\n")
		
		pname = input("Enter Name - ")
		pnameC = pname.upper()
		pquantity = int( input("Enter Quantity - ") )
		pprice = float( input("Enter Cost Price (per piece) - ") )

		    # CHECK IF THE PRODUCT ALREADY EXISTS IN THE TABLE OR NOT
		check_comm = (f" SELECT Name FROM purchase WHERE Name = '{pnameC}' ")
		csr.execute(check_comm)
		check_result = csr.fetchone()# KEEPING THE FETCHED RESULTS IN A VARIABLE

		if check_result is None:
			pcomm = ("INSERT INTO purchase VALUES(%s, %s, %s, curdate())")
			pvals = (pnameC, pquantity, pprice)
			csr.execute(pcomm, pvals)
			mydb.commit()
		else:   # SOME VALUE WAS RETURNED
			    # i.e. THE PRODUCT EXISTS ON THE TABLE
			update_comm = (f" SELECT Quantity FROM purchase WHERE Name = '{pnameC}' ")
			csr.execute(update_comm)
			qt = csr.fetchone()
			qt = int(''.join( map( str, qt ) )) # CONVERT TUPLE TO INT
			
			new_qt = (qt + pquantity)
			    # UPDATE THE EXISTING QUANTITY AND COST PRICE
			pcom = (f" UPDATE purchase SET Quantity = '{new_qt}', Cost_Price = '{pprice}' WHERE Name = '{pnameC}' ")
			csr.execute(pcom)
			mydb.commit()
		input("\033[5;33mpress any key to continue\033[0;37m")
		
	except Exception as ex:
		print(ex)
		print(traceback.format_exc())
		print("Purchase Entry Failed!")
		input("\033[5;33mpress any key to continue\033[0;37m")
		    # PROGRAM RETURNS TO MAIN MENU


def smod():
	try:
		csr = mydb.cursor()
		try:	# CREATE SALES TABLE
			csr.execute(" CREATE TABLE sale( Name varchar(50) primary key,Quantity int(9), Sale_Price decimal(9, 2))")
			print("\033[33mSales Database Created Successfully\033[37m")
		except BaseException:	# IF TABLE ALREADY EXISTS
			print("\033[33mSales Database Initialised.\033[37m")
		print("\n\n")
		
		sname = input("Enter Name - ")
		snameC = sname.upper()
		squantity = int( input("Enter Quantity - ") )
		sprice = float( input("Enter Selling Price (per piece)- ") )

		try: # CHECK1 - IF NAME OF PRODUCT EXISTS IN PURCHASE TABLE OR NOT
			check_comm = (f" SELECT Name FROM purchase WHERE Name = '{snameC}' ")
			csr.execute(check_comm)
			check_result = csr.fetchone()

			if check_result is None:  # MySQL RETURNS NONE WHEN NO VALUE FETCHED
				print("\033[1;31;40mThere is no entry for the following item in purchase database:\033[1;37m ",sname)
			else:
				
				fetch_StockQt = (f" SELECT Quantity FROM purchase WHERE Name = '{snameC}' ")
				csr.execute(fetch_StockQt)
				stockQt = csr.fetchone()
				stockQt = int(''.join( map( str, stockQt ) ))

				    # CHECK2 - IF PRODUCT ALREADY EXISTS IN SALE TABLE OR NOT
				check2_comm = (f" SELECT Name FROM sale WHERE Name = '{snameC}' ")
				csr.execute(check2_comm)
				check2_result = csr.fetchone()

				if (check2_result is not None): 
					    # FETCH THE QUANTITY SOLD LAST TIME
					fetch_lastQt = (f" SELECT Quantity FROM sale WHERE Name = '{snameC}' ")
					csr.execute(fetch_lastQt)
					sqt = csr.fetchone()
					sqt = int(''.join( map( str, sqt ) ))




					    # CHECK IF SALE QUANTITY IS NOT BIGGER THAN AVAILABLE QUANTITY IN STOCK
					if ( (sqt + squantity) > stockQt ):
						print("\033[1;31;40mInsufficient Stock for the following item:\033[1;37m", sname)
					else:
						snew_qt = (sqt + squantity)

						scomm = (f" UPDATE sale SET Quantity = '{snew_qt}',Sale_Price = '{sprice}' WHERE Name ='{snameC}' ")
						csr.execute(scomm)
						mydb.commit()
				else:  # IF PRODUCT DOES NOT EXISTS IN THE SALE TABLE CHECK IF SALE QUANTITY IS NOT BIGGER THAN AVAILABLE QUANTITY IN STOCK
					if (squantity > stockQt):
						print("\033[1;31;40mInsufficient Stock for the following item:\033[1;37m", sname)
					else:
						scomm = (f" INSERT INTO sale VALUES( '{snameC}', '{squantity}', '{sprice}' )")
						csr.execute(scomm)
						mydb.commit()
		
		except Exception as ex:
			print(ex)
			print(traceback.format_exc())
			print("TIP: Start Purchase module before Sale Module")

		input("\033[5;33mpress any key to continue\033[0;37m")
		    # RETURN TO MAIN MENU
	
	except Exception as ex:
		print(ex)
		print("Sale Entry Failed!")
		input("\033[5;33mpress any key to continue\033[0;37m")

def PnLmod(): # REVENUE CALCULATOR
	try:
		csr = mydb.cursor()
		print()
		print("Revenue Calculation")

		csr.execute("SELECT Name FROM sale")
		product_name = csr.fetchall()
		product_nameL = []
		for n in product_name:
			  # ADD ALL PRODUCT NAMES TO A LIST
			product_nameL.append( str(n[0]) )

		selling_prices = []
		for x in product_nameL:
			csr.execute(f"SELECT Sale_Price FROM sale WHERE Name = '{x}' ")
			sp_fetch = csr.fetchall()
			for p in sp_fetch:
			    	# ADD ALL SALE PRICES TO A LIST
				selling_prices.append( float(p[0]) )

		cost_prices = []
		for x in product_nameL:
			csr.execute(f"SELECT Cost_Price FROM purchase WHERE Name = '{x}' ")
			cp_fetch = csr.fetchall()
			for c in cp_fetch:
				  # ADD ALL COST PRICES TO A LIST
				cost_prices.append( float(c[0]) )

		qt = []
		for x in product_nameL: 
			csr.execute(f"SELECT Quantity FROM sale WHERE Name ='{x}' ")
			qt_fetch = csr.fetchall()
			for q in qt_fetch:
				  # ADD ALL QUANTITIES TO A LIST
				qt.append( int(q[0]) )

		print()
		final_revenue = 0
		fr_list = []

		for i  in range( len(product_nameL) ):
			profit_perpiece = (selling_prices[i] - cost_prices[i])
			PL = profit_perpiece*qt[i]
			final_revenue += PL
			fr_list.append(PL)

		  # PRETTY PRINTING
		pet = PrettyTable(padding_width=2)
		pet.field_names = (["Product Name", "Cost Price", "Selling Price", "Quantity Sold", "Profit/Loss"])

		for i in range( len(product_nameL) ):
			row = [product_nameL[i], cost_prices[i], selling_prices[i], qt[i], fr_list[i]]
			pet.add_row(row)

		  # LEFT ALIGN
		pet.align["Product Name"] = 'l' 
		pet.align["Cost Price"] = 'l'
		pet.align["Selling Price"] = 'l'
		pet.align["Quantity Sold"] = 'l'
		pet.align["Profit/Loss"] = 'l'
		print(pet)

		print('\n\033[1;32mTotal Revenue = \033[1;37m', final_revenue)
		print()
		input("\033[5;33mpress any key to continue\033[0;37m")
	except Exception as e:
		print(e)
		print("\033[5;31;40mAn error occured!\033[0;37m")
		input("\033[5;33mpress any key to continue\033[0;37m")
