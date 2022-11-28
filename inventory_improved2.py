

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country 
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity 

    def get_cost(self):
        return self.cost 

    def get_quantity(self):
        return self.quantity

    def change_quantity(self, new_quantity):
        self.quantity = new_quantity

    def get_code(self):
        return self.code

    def get_name(self):
        return self.product

    def __str__(self):
        print(f'''
Country = {self.country}
Code = {self.code}
Product = {self.product}
Cost = {self.cost}
Quantity = {self.quantity}''')

    def original_details(self):                   #this method can be used to repopulate the database 
        line = '\n' + str(self.country)+','+str(self.code)+','+str(self.product)+','+str(self.cost)+','+str(self.quantity)
        return line

#=============Shoe list===========

shoe_list = []

#==========Functions outside the class==============
def read_shoes_data():
    shoe_list = [] #reset shoe list 
    filename = 'inventory.txt'
    f = open(filename, 'r') 

    contents = ""                  #store file contents here

    for line in f :
        contents+=line
    
    line_list = contents.split("\n")   #line_list is a list where each element is a line
    del(line_list[0])                  #but we must delete the first row

    list_of_lists = []

    for line in range(0, len(line_list)):
        list_of_lists.append(line_list[line].split(","))


    #we now have something like 
    #[['country1', 'code1', 'product1', 'cost1', 'quantity1'], ['country2', 'code2', 'product2', 'cost2', 'quantity2']]

    #now to create our shoe objects. We want to check that the data was in the right format, with no header included: so the int() function...
    #...will throw an error if it encounters a header, as it cannot convert letters (of the title) to integers (for the product code)
    try:
        for line in range(0, len(list_of_lists)) : 
            #so list_of_lists[line] will be like ['country1', 'code1', 'product1', 'cost1', 'quantity1']
            object_to_be_added = Shoe(list_of_lists[line][0], list_of_lists[line][1], list_of_lists[line][2], list_of_lists[line][3], list_of_lists[line][4])
            shoe_list.append(object_to_be_added)
    except ValueError :
        raise Exception("Invalid data format. Please check that the header/title is only the first line of the file.")

    #list of shoes is our list of Shoe class objects

    f.close()
    return shoe_list

def capture_shoes():
    
    #so I interpreted this task as taking user input and appending it to inventory.txt
    #so we do just that, with these input statements 
    country = input("Please enter the country that the shoe is from: ")
    code = input("Please enter the shoe code: ")
    product = input("Please enter the product name: ")
    cost = input("Please enter the cost: ")
    quantity = int(input("Please enter the quantity: "))

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    print(f'''
    Task complete: new shoe added! 
    Country = {country}
    Code = {code}
    Product = {product}
    Cost = {cost}
    Quantity = {quantity}
    ''')

    f = open('inventory.txt', 'a')
    f.write(f'''\n{country},{code},{product},{cost},{quantity}''')
    f.close()

def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    shoe_list = read_shoes_data()
    for shoe in range(0, len(shoe_list)) :
        shoe_list[shoe].__str__()

def re_stock():
    
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    quantities_list = []   #create and populate a list of just each shoe object's quantity, and append to list...
    
    shoe_list = read_shoes_data()

    for i in range(0, len(shoe_list)):
        quantities_list.append(int(shoe_list[i].get_quantity()))  #...using our get quantity method
 
    lowest_quantity = min(quantities_list)
    lowest_quantity_index = int(quantities_list.index(lowest_quantity))  #now find the index of the lowest one

    print("The shoe with the lowest quantity is: ")
    shoe_list[lowest_quantity_index].__str__()

    choice = input('''
    Would you like to restock it? Y/N
    ''').lower()

    if choice == 'y' :
        new_quantity = int(input("After restocking, please enter the quantity of this shoe you would like to record for the database: "))

        shoe_list[lowest_quantity_index].change_quantity(new_quantity)
        print(f"Task complete! The new quantity value is: {shoe_list[lowest_quantity_index].get_quantity()}")

        #now to repopulate the inventory file with the new values for quantities.

        f = open('inventory.txt', 'w') #this will overwrite the file

        new_contents = "Country,Code,Product,Cost,Quantity"           #this will create our new contents string and add our first line, which is always the same.

        for shoe in range(0, len(shoe_list)):
            new_contents += shoe_list[shoe].original_details()         #this will add all the shoe objects' details back, in the same format as before, but with our updated stock value of course

        f.write(new_contents)

        print(f'''
        Task complete, please check inventory.txt for the updated details.
        ''')

        f.close()

    elif choice == 'n' :
        print("Thanks!")
    else :
        print("Please choose only Y or N.")


def search_shoe():
    shoe_list = read_shoes_data()
    code_list = []

    for i in range(0, len(shoe_list)): 
        code_list.append(shoe_list[i].get_code())   #now we have a list of codes
    
    search_input = input("Please enter the code you would like to search for: ")
    
    if search_input in code_list :
        for index in range(0, len(code_list)) :   
            if code_list[index] == search_input : 
                searched_shoe = shoe_list[index]                    #this finds the index of the code they are searching for
    else : 
        raise Exception("The code you searched for does not exist. Please try again.")

    print(f'''The shoe you searched for was: ''')
    searched_shoe.__str__()
    print('''Task Complete!
    ''')
    
def value_per_item():
    #okay my plan for this one is to essentially produce a dictionary.
    #the keys will be shoe names, the values will be the shoe values 

    shoe_list = read_shoes_data()

    list_of_shoe_values = [] #we first make our two lists which we will zip together 
    list_of_shoe_names = []

    for shoe in range(0,len(shoe_list)): 
        list_of_shoe_values.append(int(shoe_list[shoe].get_quantity()) * int(shoe_list[shoe].get_cost()))
        list_of_shoe_names.append(shoe_list[shoe].get_name())

    #print(len(list_of_shoe_names))    # I printed these to check the two lists were the same length - because otherwise...
    #print(len(list_of_shoe_values))   #...when we make our dictionary it may miss off some values otherwise
    values_dict = {}

    for i in range(len(list_of_shoe_names)):
        key = list_of_shoe_names[i]
        value = list_of_shoe_values[i]

        print(f'''{key} : {str(value)} dollars''')
        values_dict[key] = value

    #now our dictionary is made, and printed in a viewable way. 

    #but there a lots of values here so we should allow the user to search for a specific product.
    choice = input('''
    Would you like to get the price of an individual product, by name? Y/N: ''').strip(" ").lower()

    if choice == 'y' :
        choice2 = input("Please enter the exact name of the shoe you would like to view the price for: ").strip(" ")
        try: 
            print(f'''
            
            The price of {choice2} is: {values_dict[choice2]}
            
            ''')
        except KeyError:
            print("Sorry, that shoe was not found. Please try again.")
    elif choice == 'n': 
        print("Task complete. Thanks.")
    else :
        print("Please only enter Y/N")

def highest_qty():
    
    list_of_quantities = []
    shoe_list = read_shoes_data()

    for i in range(0, len(shoe_list)):
        list_of_quantities.append(int(shoe_list[i].get_quantity()))
    
    index_of_maximum = list_of_quantities.index(max(list_of_quantities))
    
    
    print(f'''
    The shoe with the greatest quantity is {shoe_list[index_of_maximum].get_name()}:''')

    shoe_list[index_of_maximum].__str__()

    print('''
    FOR SALE!
    ''')

highest_qty()
#==========Main Menu=============


while True:
    menu_choice = input('''
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                                                                                             #
    #   Welcome to the inventory application! Please choose from the following options:           #
    #                                                                                             #
    #  1 - capture shoes (add a new product description to the database)                          #
    #  2 - view all products in the database                                                      #
    #  3 - re-stock the lowest-stocked shoe on the database                                       #
    #  4 - search for details of a given shoe on record                                           #
    #  5 - browse the value of the products in stock                                              #
    #  6 - view the shoe with the highest quantity on record currently                            #
    #  e - exit                                                                                   #
    #                                                                                             #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    Please enter here:   ''').strip(" ").lower()

    if menu_choice == '1' :
        capture_shoes()
    elif menu_choice == '2' :
        view_all()
    elif menu_choice == '3' :
        re_stock()
    elif menu_choice == '4' :
        search_shoe()
    elif menu_choice == '5' :
        value_per_item()
    elif menu_choice == '6' :
        highest_qty()
    elif menu_choice == 'e' :
        print("Goodbye!")
        break
    else: 
        print("Please only enter from the options given, thank you.")
