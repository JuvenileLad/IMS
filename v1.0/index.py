import mod
import os
import time

try:
	mod.title()
	authentication = mod.pwd()
	if authentication is True:
		mod.title()
		choice = mod.mainmenu()
		while choice is not None:

			if choice == 1:    # PURCHASE
				mod.pmod()
				mod.title()
				choice = mod.mainmenu()
			elif choice == 2:  # SALES
				mod.smod()
				mod.title()
				choice = mod.mainmenu()
			elif choice == 3:  # CALC MODULE
				mod.title()
				ch3 = mod.menu3()

				while ch3 is not None:
					if ch3 == 1: # REVENUE CALCULATOR
						mod.PnLmod()
						mod.title()
						ch3 = mod.menu3()
					elif ch3 == 2: # PRODUCT REPORTS
						mod.productreport()
						mod.title()
						ch3 = mod.menu3()
					elif ch3 == 3: # BACK TO MAIN MENU
						mod.title()
						choice = mod.mainmenu()
						break
					else:
						print("\033[5;31;40mAn error occured!\033[0;37m")
						time.sleep(1)
						mod.title()
						choice = mod.mainmenu()# CALC

			elif choice == 4:  # INVENTORY
				mod.title()
				mod.inventory()
				mod.title()
				choice = mod.mainmenu()
			else:
				print("\033[5;31;40mAn error occured!\033[0;37m")
				time.sleep(1)
				mod.title()
				choice = mod.mainmenu()
	else: # AUTHENTICATION ERROR
		print("Authentication Error!")
		print("Program will now  exit..")
		time.sleep(1)

except Exception as ex:
	# os_type = os.getOSKernal()
	# if  os_type == '':
	
	# else :
	os.system('clear')
	print(ex)
	print("\033[0;31mAn Exception Occured!\nProgram will exit now..\033[1m")
	time.sleep(1)


