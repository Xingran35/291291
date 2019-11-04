# -*- coding: utf-8 -*-
import sqlite3
import sys, getopt
import time
from urllib.request import pathname2url
import re
import datetime
from datetime import date
from random import randint
from itertools import chain 
from dateutil.relativedelta import relativedelta

def main(argv):
    # Main structure of the script
    # The script takes a database then require the right username and password 
    # to access the database, user can access and modify the database after 
    # entering the right username and password
    # user can quit at anytime
    if len(argv) == 1:
        exit_script(2)
    option =argv[1]
    file_path = argv[2]
    if option == '-i':
        pass
    else:
        exit_script(2)
    conn = read_file(file_path)
    print("\n Welcome to This Script! This Script is Aiming to Get Full Mark in Cmput291 Mini-Project.\n")
    time.sleep(0.5)
    cursor = conn.cursor()
    user = check_log_in(cursor)
    all_commands = {'RAB': 'Register a birth.',
                    'RAM': 'Register a marriage.',
                    'RAR': 'Renew a vehicle registration.',
                    'PAB': 'Process a bill of sale.',
                    'PAP': 'Process a payment.',
                    'GAD': 'Get a driver abstract.',
                    'IAT': 'Issue a ticket.',
                    'FAC': 'Find a car owner.',
                    'Exit': 'Quit the program.'
                    }
    print("\nBelow is the Command Table: \n")
    print_commands(all_commands)
    while True:
        current_command = input("\nEnter Your Command in the New Line: \n")
        if current_command.upper() == 'EXIT':
            exit_script(0)
        else:
            handle_command(current_command.upper(), all_commands, cursor, user)
            conn.commit()
        

def read_file(file_path):
    # this function checks if the file can be read
    # if the file is read successfully, the function return the database
    # otherwise it quit the script
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(file_path))
        conn = sqlite3.connect(dburi, uri=True)
    except:
        exit_script(1)
    return conn

def print_row(command, description):
    # print each row of the command
    print(" %-15s %-15s" % (command, description))
    
def print_commands(all_commands):
    # This function prints out all possible command
    command = list(all_commands.keys())
    print("\n")
    print_row('Command', 'Description')
    for c in command:
        print_row(c, all_commands.get(c))         
        print("\n")


def print_invalid(name):
    # print the input is invaliad
    print('\n******Invalid ' + name +' *******\n')


def check_log_in(cursor):
    # This function checks if the user enter the right user name and password that already stored in the database
    # return the name of the user
    print('\nEnter Your Username and Password to Access or Modify the Database. \n')
    while True:
        username = input("\nEnter your Username, Note This is Case-Sensitive: ")
        password = input("Enter Your Password, Note This is Case-Sensitive: ")
        result = cursor.execute("select * from users where uid = ? and pwd = ?;",(username,password))
        result = result.fetchall()
        if len(result) == 1:
            print("\nWelcome! " + result[0][3]+' ' + result[0][4] + ".")
            print("\n")
            time.sleep(0.5)
            break
        else:
            print('\n****** Wrong Username or Password! Remember, Case Matters!! *******\n')
    return result[0]
    

def handle_command(current_command, all_commands, cursor, user):
    # This function handles the input command
    # and print the result to the terminal
    user_fname = user[3]
    user_lname = user[4]
    user_type = user[2] # 'a' for agents, 'o' for officers
    user_city = user[5]
    if current_command == 'RAB':
        succ = do_RAB(cursor, user_city, user_type)
        print_succ(succ)
        
    elif current_command == 'RAM':
        succ = do_RAM(cursor, user_city, user_type)
        print_succ(succ)
        
    elif current_command == 'RAR':
        succ = do_RAR(cursor, user_city, user_type)
        print_succ(succ)
        
    elif current_command == 'PAB':
        succ = do_PAB(cursor, user_city, user_type)
        print_succ(succ)
        
    elif current_command == 'PAP':
        succ = do_PAP(cursor, user_city, user_type)
        print_succ(succ)
        
    elif current_command == 'GAD':
        succ = do_GAD(cursor, user_city, user_type)
        print_succ(succ)
                
    elif current_command == 'IAT':
        succ = do_IAT(cursor, user_city, user_type) # succed or not
        print_succ(succ)
                 
    elif current_command == 'FAC':
        succ = do_FAC(cursor, user_city, user_type)
        print_succ(succ)
        
    else:
        print('\n******Wrong Command!!!****** \n')
        print_commands(all_commands)


def print_succ(succ):
    # Print the command excuted result
    if succ:
        print('****** Command Executed Successfully! ******')
    else:
        print('****** Command did not Executed Successfully ******')    

        
def do_RAB(cursor, user_city, user_type):
    # This function perform the operation for Register a birth
    if not check_user_agent(user_type):
        return False
    fname = get_input_string('First Name of the New Birth', 12, isname = True)
    lname = get_input_string('Last Name of the New Birth', 12, isname = True)
    gender = get_input_string('Gender of the New Birth', 1, isgender = True)
    bdate = get_input_string('Birth Date of the New Birth', 0, isdate = True)
    bplace = get_input_string('Birth Place of the New Birth', 20, isaddress = True)
    fnamef = get_input_string('First Name of Father of the New Birth', 12, isname = True)
    lnamef = get_input_string('Last Name of Father of the New Birth', 12, isname = True)
    fnamem = get_input_string('First Name of Mother of the New Birth', 12, isname = True)
    lnamem = get_input_string('Last Name of Mother of the New Birth', 12, isname = True)
    today = date.today()
    regdate =  today.strftime('%Y-%m-%d') # regdate in format 1960-1-1
    regplace = user_city
    regno = get_unique_id(cursor, 'births', 'regno')
    father = reg_new_person(cursor, fnamef, lnamef) # get info about father
    mother = reg_new_person(cursor, fnamem, lnamem) # get info about mother
    person_data = (fname, lname, bdate, bplace, mother[4], mother[5])
    succ = reg_new_person(cursor, fname, lname, data = person_data)
    if succ:
        print('\n****** Successfully Added the Newborn '+fname+' ' +lname+' to the *Persons Talbe ! ******\n')
        print('****** His Person Information is %s %s %s %s %s %s ******' % change_none_to_Null(person_data))
    else:
        print('\n****** Warning! The Newborn '+fname+' ' +lname+' Already Exist in the *Persons Table ! ******')
        return False
    birth_data = (regno, fname, lname, regdate, bplace, gender, fnamef, lnamef, fnamem, lnamem)
    exist_birth = check_exist(cursor, 'births','fname', 'lname', fname, lname)
    if not exist_birth:
        cursor.execute("insert into births values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ;",birth_data)
        print('\n****** Successfully Added the Newborn '+fname+' ' +lname+' to the *Birth Talbe ! ******\n')
        print('****** His Birth Information is %s %s %s %s %s %s %s %s %s %s ******\n' % change_none_to_Null(birth_data))
        return True
    else:
        print('\n****** Warning! The Newborn '+fname+' ' +lname+' Already Exist in the *Birth Table ! ******')
        return False
    

def do_RAM(cursor, user_city, user_type):
    # This function perform the operation for Register a Marriage
    if not check_user_agent(user_type):
        return False
    fnamep1 = get_input_string('First Name of Partner1', 12, isname = True)
    lnamep1 = get_input_string('Last Name of Partner1', 12, isname = True)
    fnamep2 = get_input_string('First Name of Partner2',12, isname = True)
    lnamep2 = get_input_string('Last Name of Partner2', 12, isname = True)
    today = date.today()
    regdate =  today.strftime('%Y-%m-%d') # regdate in format 1960-1-1
    regplace = user_city
    regno = get_unique_id(cursor, 'marriages', 'regno')
    partner1 = reg_new_person(cursor, fnamep1, lnamep1) # register the person if not exists 
    partner2 = reg_new_person(cursor, fnamep2, lnamep2) # register the second person if not exists
    data = (regno, regdate, regplace, fnamep1, lnamep1, fnamep2, lnamep2)
    try:
        cursor.execute("insert into marriages values (?, ?, ?, ?, ?, ?, ?) ;",data)
        print('\n****** Successfully Added the '+fnamep1+' ' +lnamep1+', '+ fnamep2+' ' +lnamep2+' to the *Marriage Talbe ! ******\n')
        print('****** Their Marriage Information is %s %s %s %s %s %s %s ******\n' % change_none_to_Null(data))
        return True
    except:
        return False
    
    
def do_RAR(cursor, user_city, user_type):
    # This function perform the operation for Renewm a Registration
    if not check_user_agent(user_type):
        return False
    today = date.today()
    regno =input("Enter Your Registration Number: \n")
    try:
        regno = int(regno)
    except:
        print('\n****** Warning! Only Integer Numbers are Allowed Here ! ******')
        return False
    today_plus_year = today + relativedelta(years=1)
    format_today =  today.strftime('%Y-%m-%d') # regdate in format 1960-1-1
    result = cursor.execute("select * from registrations where regno = ? ;",(regno,))
    result = result.fetchall()
    if len(result) == 0:
        print('\n****** Warning! No Matching Record Found ! ******')
        return False
    else:
        result = result[0]
        expiry = result[2]
        if expiry<=format_today:
            new_exp = today_plus_year.strftime('%Y-%m-%d')
        else:
            datetime_object = datetime.datetime.strptime(expiry, '%Y-%m-%d').date()
            new_date = datetime_object + relativedelta(years=1)
            new_exp = datetime.datetime.strftime(new_date, '%Y-%m-%d')
        cursor.execute("UPDATE registrations SET expiry=? WHERE regno= ? ;",(new_exp, regno))
        print('\n****** Update Successfully, the Old Expire Time was: %s, the New Expire Time is Now %s  ******\n' % (expiry, new_exp))
        return True


def do_PAB(cursor, user_city, user_type):
    # Process a payment
    if not check_user_agent(user_type):
        return False
    today = date.today()
    today_plus_year = today + relativedelta(years=1)
    format_today =  today.strftime('%Y-%m-%d') # regdate in format 1960-1-1
    format_today_plus_year = today_plus_year.strftime('%Y-%m-%d')

    current_fname = get_input_string('First Name of Current Owner', 12, isname = True)
    current_lname = get_input_string('Last Name of Current Owner', 12, isname = True)
    new_fname = get_input_string('First Name of New Owner', 12, isname = True)
    new_lname = get_input_string('Last Name of New Owner', 12, isname = True)
    vin = get_input_string('VIN', 5, isaddress = True)
    plate = get_input_string('plate', 7, isaddress = True)

    new_exist = check_exist(cursor, 'persons','fname', 'lname', new_fname, new_lname)
    if not new_exist: # If the new owner doesn't exist
        print('\n****** Warning! The New Owner doesn not Exist ! ******')
        return False
    check_result = check_onwer(cursor,current_fname, current_lname, vin)
    if  check_result== False:
        print('\n****** Warning! The Current Owner is not the Latest Owner of the Veichile ! ******')
        return False
    elif check_result == None:
        print('\n****** Warning! The Veichile Currently does not Have a Owner! ******')
        return False
    regno = get_unique_id(cursor, 'registrations', 'regno')
    cursor.execute("UPDATE registrations SET expiry=? WHERE regno= ? ;",(format_today, check_result))
    data = (regno, format_today, format_today_plus_year, plate, vin, new_fname, new_lname)
    cursor.execute("insert into registrations values (?, ?, ?, ?, ?, ?, ?) ;",data)
    print('\n****** Processed Payment Successfully, the New Registation is %s %s %s %s %s %s %s ******\n' % change_none_to_Null(data))
    return True


def do_PAP(cursor, user_city, user_type):
    # This function process a payment
    if not check_user_agent(user_type):
        return False
    today = date.today()
    format_today =  today.strftime('%Y-%m-%d') # regdate in format 1960-1-1
    tno =input("Enter the Ticket Number: \n")
    try:
        tno = int(tno)
    except:
        print('\n****** Warning! Only Integer Numbers are Allowed Here ! ******')
        return False
    
    amount =input("Enter the Amount of Your Payment: \n")
    try:
        amount = int(amount)
    except:
        print('\n****** Warning! Only Integer Numbers are Allowed Here ! ******')
        return False
    
    check_result =  get_sum_ticket_amout(cursor, amount, tno)
    if check_result == None:
        print('\n****** Warning! The Ticket does not Exist ! ******')
        return False
    elif check_result == False:
        print('\n****** Warning! The Amount Exceed the Total Remaining Fine ! ******')
        return False
    else:
        data = (tno, format_today, amount)
        try:
            cursor.execute("insert into payments values (?, ?, ?) ;",data)
            return True
        except:
            print('\n****** Warning! Same Ticket cannot be Paid Twice a Day ! ******')
            return False
        
        
def do_GAD(cursor, user_city, user_type):
    # This function gets a driver's information
    if not check_user_agent(user_type):
        return False
    fname = get_input_string('First Name of the Driver', 12, isname = True)
    lname = get_input_string('Last Name of the Driver', 12, isname = True)
    
    exist_result = check_exist(cursor, 'registrations', 'fname', 'lname', fname, lname)
    if not exist_result:
        print('\n****** Warning! The Driver does not Exist in the Registation Table ! ******') 
        return False
    tickets_2_years = get_driver_tickets(cursor, fname, lname, is_2_years = True)
    tickets_life_time = get_driver_tickets(cursor, fname, lname)

    demerit_2_years = get_driver_demerit(cursor, fname, lname, is_2_years = True)
    demerit_life_time = get_driver_demerit(cursor, fname, lname)
    
    demerit_2_years_num = demerit_2_years[0]
    demerit_life_time_num = demerit_life_time[0]
    demerit_points_2_years = demerit_2_years[1]
    demerit_points_life_time = demerit_life_time[1]
    
    ticket_2_years_num = tickets_2_years[0]
    ticket_life_time_num = tickets_life_time[0]
    ticket_list_2_years = tickets_2_years[1]
    ticket_list_life_time = tickets_life_time[1]
    
    
    print('\n****** The Total Number of Tickets within 2 Years are %d, the Total Number of Tickets in Life Time are %d ******' % (ticket_2_years_num, ticket_life_time_num))
    print('\n****** The Total Number of Demerit Notice within 2 Years are %d, the Total Number of Demerit Notice in Life Time are %d ******' % (demerit_2_years_num, demerit_life_time_num))
    print('\n****** The Total Number of Demerit Points within 2 Years are %d, the Total Number of Demerit Points in Life Time are %d\n ******' % (demerit_points_2_years, demerit_points_life_time))
    
    if ticket_life_time_num >5:
        tickets = ticket_list_life_time[0:4]
    else:
        tickets = ticket_list_life_time

    order = input("Do You Want to View the Tickets? (Y/N)")
    if order.upper() == 'Y':
        print("Ticket number  Violation date  Violation Description  Fine  Registration Number  Make  Model")
        for value in tickets:
            print(value)
        if ticket_life_time_num >5:
            order = input("\n Do You Want to View More Tickets? (Y/N)")
            if order.upper() == 'Y':
                for value in ticket_list_life_time[4:-1]:
                    print(value)
    elif order.upper() == 'N':
        pass
    else:
        print_invalid('Order')
    
    return True
    

def do_IAT(cursor, user_city, user_type):
    # Issue a ticket.
    #check_user_officer(user_type)
    if not check_user_officer(user_type):
        return False
    
    regno =input("Enter The Registration Number: \n")
    try:
        regno = int(regno)
    except:
        print('\n****** Warning! Only Integer Numbers are Allowed Here ! ******')
        return False

    result = cursor.execute('''SELECT r.fname, r.lname, v.make, v.model, v.year, v.color 
                               FROM registrations r, vehicles v 
                               WHERE r.vin = v.vin and r.regno = ?  COLLATE NOCASE;''',(regno,))
    result = result.fetchall()
    if len(result) == 0:
        print('\n****** Warning! No Matching Record Found ! ******')
        return False
    else:
        print(result[0])
    

    violation_date = get_input_string('violation date', 0, isdate = True, isrequired = False)
    if violation_date == None:
        today = date.today()
        violation_date =  today.strftime('%Y-%m-%d')
    violation_text = get_input_string('violation text', 12, isaddress = True)
    amount =input("Enter the Amount of Your Payment: ")
    try:
        amount = int(amount)
    except:
        print('\n****** Warning! Only Integer Numbers are Allowed Here ! ******')
        return False
    
    tno = get_unique_id(cursor, 'tickets', 'tno')
    ticket_data = (tno, regno, amount, violation_text, violation_date)

    cursor.execute("insert into tickets values (?, ?, ?, ?, ?) ;",ticket_data)
    print('\n****** Successfully issue a ticket to ticket Table ! ******\n')

    return True



            



def do_FAC(cursor,user_city,user_type):
    # Find a car owner
    if not check_user_officer(user_type):
        return False
    
    #one or more of make, model, year, color, and plate. 
    make = get_input_string('Make of the car', 12, isaddress = True, isrequired = False)
    model= get_input_string('Model of the car', 7, isaddress = True, isrequired = False)
    color= get_input_string('Color of the car', 12, isaddress = True,isrequired = False)
    plate = get_input_string('plate', 7, isaddress = True,isrequired = False)
    
    result = cursor.execute('''SELECT distinct r.vin
                               FROM registrations r, vehicles v 
                               WHERE r.vin = v.vin 
                               GROUP BY r.vin
                               HAVING (v.make = ? COLLATE NOCASE and v.model = ? COLLATE NOCASE and v.color = ? COLLATE NOCASE and r.plate = ? COLLATE NOCASE) or ('1' == '1');''',(make,model,color,plate,))
                               
    result = result.fetchall()
    #print(result)
    length = len(result)
    new_list = []
    #print(result)
    if length > 4:
        for i in range(length):
            vin_need = result[i][0]
            single_result = cursor.execute('''SELECT v.make, v.model, v.year, v.color, r.plate, v.vin
                               FROM registrations r, vehicles v 
                               WHERE r.vin = v.vin and r.vin = ? ;''',(vin_need,))
            single_result = single_result.fetchall()
            for k in range(len(single_result)):
                print(single_result[k])
                new_list.append((single_result[k]))
    
        # select one result and print the selected car information
        index  = int(input("***Choose one of the vehicle above by row number (>4 case) :"))
        for j in range(5):
            print(new_list[index-1][j])

        printed_reg_info = check_recent_registration(cursor,new_list[index-1][5]) 
        print("The latest registration date is :")
        print(printed_reg_info[0][1])
        print("The expiry date is :")
        print(printed_reg_info[0][2])
        print("The name of its owner is :")
        print(printed_reg_info[0][5], printed_reg_info[0][6])
        
    elif length==0:
        print("no such car")
        return False
    else:
        print("less than 4")
        for i in range(length):
            vin_need = result[i][0]
            single_result = cursor.execute('''SELECT v.make, v.model, v.year, v.color, r.plate, v.vin
                               FROM registrations r, vehicles v 
                               WHERE r.vin = v.vin and r.vin = ? ;''',(vin_need,))
            single_result = single_result.fetchall()
            for k in range(len(single_result)):
                print(single_result[k])
                new_list.append((single_result[k]))
        

        #print all the car informaiton
        for i in range(len(new_list)):
            print("********************This is the result",i+1)
            print(new_list[i])
            printed_reg_info = check_recent_registration(cursor,new_list[i][5]) 
            print("The latest registration date is :")
            print(printed_reg_info[0][1])
            print("The expiry date is :")
            print(printed_reg_info[0][2])
            print("The name of its owner is :")
            print(printed_reg_info[0][5], printed_reg_info[0][6])
            print("\n")


        



#for each match, the make, model, year, color, and the plate of the matching car will be shown as well as the latest registration date, the expiry date, and the name of the person listed in the latest registration record.
    


        

           

    
    


    return True


    
    

def get_driver_tickets(cursor, fname, lname, is_2_years = False):
    # this function returns the tickets that the driver got
    if is_2_years:
        tickets = cursor.execute('''select t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
                                 from tickets t, registrations r, vehicles v
                                where t.regno = r.regno and r.vin = v.vin
                                and r.fname = ? COLLATE NOCASE and r.lname = ? COLLATE NOCASE
                                and t.vdate >= date('now', '-2 years') 
                                order by vdate desc
                                ;''', (fname, lname))
        tickets = tickets.fetchall()
        tickets_num = len(tickets)
        return (tickets_num ,tickets)
    else:
        tickets = cursor.execute('''select t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
                                 from tickets t, registrations r, vehicles v
                                where t.regno = r.regno and r.vin = v.vin
                                and r.fname = ? COLLATE NOCASE and r.lname = ? COLLATE NOCASE
                                order by vdate desc
                                ;''', (fname, lname))
        tickets = tickets.fetchall()
        tickets_num = len(tickets)
        return (tickets_num ,tickets)
        

def get_driver_demerit(cursor, fname, lname, is_2_years = False):
    # this function returns the dermirt notice that the driver get
    if is_2_years:
        demerits= cursor.execute('''select *
                             from demeritNotices
                            where fname = ? COLLATE NOCASE and lname = ? COLLATE NOCASE 
                            and ddate >= date('now', '-2 years') 
                            ;''', (fname, lname))
        demerits = demerits.fetchall()
        demerit_num = len(demerits)
        demerits_sum = 0
        for i in demerits:
            demerits_sum+=i[3]
        return (demerit_num, demerits_sum)
    else:
        demerits= cursor.execute('''select *
                             from demeritNotices
                            where fname = ? COLLATE NOCASE and lname = ? COLLATE NOCASE
                            ;''', (fname, lname))
        demerits = demerits.fetchall()
        demerit_num = len(demerits)
        demerits_sum = 0
        for i in demerits:
            demerits_sum+=i[3]
        return (demerit_num, demerits_sum)


def get_sum_ticket_amout(cursor, amount, tno):
    # This function checks whether the total payment amount exceed tha maximum
    # after making this payment
    ticket = cursor.execute("select * from tickets where tno = ? ;", (tno,))
    ticket = ticket.fetchall()
    if len(ticket) == 0:
        return None
    ticket = ticket[0]
    fine = ticket[2]
    total = 0
    payment = cursor.execute("select * from payments where tno = ?;", (tno,))
    payment = payment.fetchall()
    for i in range(0,len(payment)):
        current = payment[i]
        total += current[2]
    return total+amount<=fine


def change_none_to_Null(data):
    # This function changes the None in tuple to Null
    conv = lambda i : i or 'Null' 
    res = [conv(i) for i in data] 
    return tuple(res)


def check_user_agent(user_type):
    # Return true if user is agent
    if user_type == 'a':
        return True
    else:
        print('****** Warning! Only Agent can Choose this Command! ******')
        return False


def check_user_officer(user_type):
    # return True if user is offiecer
    if user_type == 'o':
        return True
    else:
        print('****** Warning! Only Officer can Choose this Command! ******')
        return False



def get_unique_id(cursor, table_name, id_column_name, max_length=6):
    # Return a unique id for certain field in the table
    while True:
        result = cursor.execute("select "+id_column_name+ " from " +table_name+" ;")
        result = result.fetchall()
        result = list(chain.from_iterable(result)) #convert to 1d
        new_id = randint(1, (10**max_length)-1)
        if new_id not in result:
            return new_id
        #else enter a new while loop


def check_exist(cursor, table_name, field_name1, field_name2, val1, val2):
    # This function checks if the certain field with certain condition exists in 
    # the table, return False if not exist
    result = cursor.execute("select * from " +table_name+" where "+field_name1+" = ? COLLATE NOCASE and "+field_name2+" = ? COLLATE NOCASE;",(val1, val2))
    result = result.fetchall()
    if len(result) == 0:
        return False
    else:
        return result[0]
    
    
def check_onwer(cursor,current_fname, current_lname, vin):
    # This function checks If the name of the current owner (that is provided) 
    #  match the name of the most recent owner of the car in the system
    result = cursor.execute("select * from registrations where vin = ? COLLATE NOCASE order by regdate desc;",(vin, ))
    result = result.fetchall()
    if len(result) == 0:
        return None
    result = result[0]
    if result[5].upper() == current_fname.upper() and result[6].upper() == current_lname.upper():
        return result[0]
    else:
        return False

def check_recent_registration(cursor,vin):
    result = cursor.execute("select * from registrations where vin = ? COLLATE NOCASE order by regdate desc;",(vin, ))
    result = result.fetchall()
    if len(result) == 0:
        return None
    else:
        return result

    
    
    
def reg_new_person(cursor, fname, lname, data = False):
    # This function register a new person into persons if the person doesn't exist,
    # agent need to input the birthdate, birthpalce, address and phone
    # otherwise it returns the infor about the person
    # it also returns the person's information as a tuple
    exist = check_exist(cursor, 'persons','fname', 'lname', fname, lname)
    if exist and not data:
        # if the person exist in the table
        # and we only want to query about his existence instead of trying to force a new insertion
        return exist
    else:
        if not data: #if data about the person is not provided
            #fname = get_input_string('First Name', 12, isname = True)
            #lname = get_input_string('Last Name', 12, isname = True)
            print("\n ******* Detected "+fname+" " +lname+" is not in the System Yet, Fill in the Following Information plz ********** \n")
            print("\n ******* Following Field can be Left with Empty If You Don't Want to Provide ********** \n")
            time.sleep(0.5)
            bdate = get_input_string('Birth Date', 0, isdate = True, isrequired = False)
            bplace = get_input_string('Birth Place', 20, isaddress = True, isrequired = False)
            address = get_input_string('Address', 30, isaddress = True, isrequired = False)
            phone = get_input_string('Phone Number', 12, isphone = True, isrequired = False)
            cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?)",(fname, lname, bdate, bplace, address, phone))
            return (fname, lname, bdate, bplace, address, phone)
        else:
            # In this case data is given, so we explictly require a new person
            # if the person already exist, return False
            if not exist:
                cursor.execute("insert into persons values (?, ?, ?, ?, ?, ?)",data)
                return True
            else:
                return False

    

def exit_script(num):
    # Exit the script 
    if num == 0:
        print('\n******Exit Successfully!****** \n')
        sys.exit(0)
    elif num == 1:
        print('\n******Broken File, or Invalid File Path!!!****** \n')
        sys.exit(1)
    elif num == 2:
        print('\n******Wrong Option, Should Be mini1.py -i <inputfile>!!!*******\n')
        sys.exit(1)
    else:
        sys.exit(0)
        

def replace_empty_null(input_string):
    # This function replace the input string to be None if it's empty
    # if the input string is empty, otherwise return the oringin string
    if len(input_string) == 0:
        return None
    else:
        return input_string.upper()


def check_char_num(input_string, max_length, isaddress, isname, isphone, isrequired, isgender):
    #This function checks whether the input string has only 26 characters
    # it also checks whether the lentgth of the string exceed the max length       
    result = True
    if not isrequired:
        if len(input_string) == 0: #If the user entered a empty string
            return True
        
    if isaddress:
        if len(input_string) > max_length:
            result = False
            print('\n******Too long!!*******\n')
        
        elif len(input_string) == 0:
            result = False
            print('\n******You cannot Enter a Empty String!!*******\n')
        return result
#        if re.findall('[^A-Za-z0-9]',input_string) != []:
#            if set(re.findall('[^A-Za-z0-9]',input_string)) == {','}:
#                pass
#            else:
#                result = False
#                print('\n******Special Char Except \',\' is *Not Allowed!*******\n')
    elif isname:
        if re.findall('[^A-Za-z0-9]',input_string) != []:
            if set(re.findall('[^A-Za-z]',input_string)) == {'-'}:
                pass
            else:
                result = False
                print('\n******Special Char Except \'-\' is *Not Allowed!*******\n')
    elif isphone:
        if re.findall('[^0-9]',input_string) != []:
            if set(re.findall('[^0-9]',input_string)) == {'-'}:
                pass
            else:
                result = False
                print('\n******Special Char Except \'-\' is *Not Allowed!*******\n')
    elif isgender:
        if input_string in ('f','m','F','M'):
            pass
        else:
            result = False
            print('\n******Only *m and *f is Allowed for This Field!*******\n')
                         
    else:
        if len(re.findall('[^A-Za-z]',input_string)) != 0:
            result = False
            print('\n******Special Char is *Not Allowed!*******\n')

    if len(input_string) > max_length:
        result = False
        print('\n******Too long!!*******\n')
    
    elif len(input_string) == 0:
        result = False
        print('\n******You cannot Enter a Empty String!!*******\n')
    
    return result


def check_valid_date(input_string, isrequired):
    # This function checks if the input string is a valid date
    if not isrequired:
        if len(input_string) == 0: #If the user entered a empty string
            return True
    try:
        datetime.datetime.strptime(input_string, '%Y-%m-%d')
        return True
    except ValueError:
        print("\n******Date should be in Format 1960-01-01!!*******\n")
        return False



def get_input_string(name, max_length, isdate= False, isaddress = False, isname = False, isphone = False, isrequired = True, isgender = False):
    # This function get the input string, return the input only if it meets the condition
    # input is the name of the input, max char in the input
    if isdate:
        while True:
            result = input("Enter your " +name+" : ")
            if check_valid_date(result, isrequired):
                return replace_empty_null(result) # change the return value to null if we get empty input
            else:
                print_invalid(name)
    else:
        while True:
            result = input("Enter your " +name+" : ")
            if check_char_num(result, max_length, isaddress, isname, isphone, isrequired, isgender):
                return replace_empty_null(result) # change the return value to null if we get empty input
            else:
                print_invalid(name)
                
                
                
if __name__ == "__main__":
    main(sys.argv)
    
