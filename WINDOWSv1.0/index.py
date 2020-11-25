import mod
import os
import time

# MAIN PROGRAM #


try:
	mod.title()
	authentication = mod.pwd()
	if authentication is True:
		mod.title()
		choice = mod.mainmenu()
		while choice is not None:

			if choice == 1:    # Purchase
				mod.pmod()
				mod.title()
				choice = mod.mainmenu()
			elif choice == 2:  # Sales
				mod.smod()
				mod.title()
				choice = mod.mainmenu()
			elif choice == 3:
				mod.title()
				ch3 = mod.menu3()
				while ch3 is not None:
					if ch3 == 1:
						mod.PnLmod()
						mod.title()
						ch3 = mod.menu3()
					elif ch3 == 2:
						mod.productreport()
						mod.title()
						ch3 = mod.menu3()
					elif ch3 == 3:
						mod.title()
						choice = mod.mainmenu()
						break
					else:
						print("\033[5;31;40mAn error occured!\033[0;37m")
						time.sleep(1)
						mod.title()
						choice = mod.mainmenu()# Calc
			elif choice == 4:  # Inventory
				mod.title()
				mod.inventory()
				mod.title()
				choice = mod.mainmenu()
			else:
				print("\033[5;31;40mAn error occured!\033[0;37m")
				time.sleep(1)
				mod.title()
				choice = mod.mainmenu()
	else:
		print("Authentication Failed!")
		print("Program will now  exit..")
		time.sleep(1)
except Exception as ex:
	os.system('cls')
	print(ex)
	print("\033[0;31mAn Exception Occured!\nProgram will exit now..\033[1m")
	time.sleep(1)


# authentication = mod.pwd()
# if authentication is True:
#     ch1 = mod.menu1()
#     if ch1 == 1:
#         mod.pmod()
#     elif ch1 == 2:
#         mod.smod()
#     elif ch1 == 3:
#         mod.title()
#         choice = mod.mainmenu()
#     else:
#         print("\033[5;31;40mAn error occured!\033[0;37m")
#         time.sleep(1)
#         mod.title()
#         choice = mod.mainmenu()
# elif authentication is False:
#     print("authentication Failed!")
#     time.sleep(1)
#     mod.title()
#     choice = mod.mainmenu()
