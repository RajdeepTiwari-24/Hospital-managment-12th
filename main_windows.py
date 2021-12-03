import csv


current_user = "null"
current_uid = 0
ad_pass = "420"

ls = ["General Physician", "Cardiologist", "ENT",
      "Neurologist", "Psychiatrist", "Orthologist", "Obstetrician", "Surgeon"]
lt = record = []
sort_by = 0


def Login():
    user_logged = False
    ch = input("Login Id. (if an existing user) / New User (Press Enter) -> ")
    if ch == "admin" or ch == "Admin":
        passwrd = input("Enter Admin Password-> ")
        if passwrd == ad_pass:
            global current_user
            current_user = "admin"
        return
    elif ch == "" or ch == "new user" or ch == "new":
        SignUp()
        return
    try:
        with open("patient-details.csv", "r") as pf:
            cV = csv.reader(pf, delimiter=',')
            for i in cV:
                if int(i[0]) == int(ch):
                    user_logged = True
                    while True:
                        print("Enter password for Patient Id.",
                              ch, "-> ", end="")
                        passwrd = input()
                        if i[2] == passwrd:
                            print()
                            print("Logged in Successfully!")
                            print()
                            print("Welcome", i[1])
                            global current_uid
                            current_user = i[1]
                            current_uid = i[0]
                            break
                        else:
                            print("Incorrect Password! Try Again.")
            if user_logged != True:
                print("User not found! Please SignUp ->")
                SignUp()
    except FileNotFoundError:
        print("File not found.")


def SignUp():
    temp = []
    try:
        with open("patient-details.csv", "r+", newline="") as pf:
            cr = csv.reader(pf, delimiter=',')
            cW = csv.writer(pf, delimiter=',')
            for i in cr:
                temp.append(i)
            temp.sort()
            uid = int(temp[len(temp) - 1][0]) + 1
            name = input("Enter your name-> ")
            try:
                phno = int(input("Enter your Phone Number-> "))
            except:
                print("Not a valid Phone Number! Try Again.")
                phno = int(input("Enter your Phone Number-> "))
            password = input("Enter Password for your account-> ")
            age = int(input("Enter your Age-> "))
            sex = input("Enter your Gender-> ")
            pat_det = [uid, name, password, sex, age, phno]
            cW.writerow(pat_det)
            print()
            print("User Added Successfully! Your User Id is",
                  uid, ".(Please note it for future use)")
            print("Welcome", name)
            global current_uid
            global current_user
            current_user = name
            current_uid = uid
    except FileNotFoundError:
        print("File not found.")


def Patient_Reg(c_user):
    print()
    print('''Please select a department:
1. General Physician
2. Cardiologist
3. ENT
4. Neurologist
5. Psychiatrist
6. Orthologist
7. Obstetrician
8. Surgeon''')
    uopt = int(input("Enter an Option-> "))
    try:
        with open("doctor.csv", "r") as doc:
            cr = csv.reader(doc, delimiter=',')
            for i in cr:
                if i[2] == ls[uopt-1]:
                    print(i[2], "Doctor available is", i[1])
                    reg_opt = input(
                        "Want to book an appointment with the above Doctor? [Yes/No] ")
                    if reg_opt == "Yes" or reg_opt == "Y" or reg_opt == "y":
                        with open("patient-details.csv", "r") as app:
                            cp = csv.reader(app, delimiter=',')
                            for j in cp:
                                if j[1] == c_user:
                                    lt = j
                    with open("reg_diary.csv", "r+", newline="") as rec:
                        cw = csv.writer(rec, delimiter=',')
                        cread = csv.reader(rec, delimiter=',')
                        for k in cread:
                            reg_id = "PRN" + str(int(k[0]) + 1)
                        reg_date = input(
                            "Enter the date you want for appointment [dd/mm/yyyy]-> ")
                        bed_num = int(reg_id[3:]) % 6
                        bed_fl = (int(reg_id[3:]) // 6) + 1
                        new_reg = [reg_id[3:]] + [lt[1]] + lt[3:5] + \
                            [ls[uopt-1]] + [i[1]] + \
                            [reg_date] + [bed_fl] + [bed_num]
                        cw.writerow(new_reg)
                        print("Your appointment on",
                              reg_date, "has been approved.")
                        print("Your Registration ID is", reg_id)
    except FileNotFoundError:
        print("File not found.")


def Cancel_Appoint(c_user):
    print()
    del_rec = []
    try:
        with open("reg_diary.csv", "r") as of:
            cr = csv.reader(of, delimiter=',')
            for i in cr:
                record.append(i)
        with open("reg_diary.csv", "w", newline="") as doc:
            cw = csv.writer(doc)
            for i in range(0,len(record)-1):
                if record[i][1] == c_user:
                    del_rec = record.pop(i)
            cw.writerows(record)
            if del_rec == []:
                print("You have 0 appointments.")
            else:
                print("All appointments cancelled.")
    except FileNotFoundError:
        print("File not found.")


def Editpatient_details(c_user, c_uid):
    print()
    temp = ch_user = []
    if c_user == "admin":
        c_uid = int(input("Enter User ID of the Patient-> "))
    try:
        with open("patient-details.csv", "r") as pf:
            cv = csv.reader(pf)
            for i in cv:
                temp.append(i)
                if i[0] == c_uid:
                    ch_user = i
                    temp.remove(i)
                    if c_user != "admin":
                        print("Name:", i[1], "Password:",
                              i[2], "Gender:", i[3], "Age:", i[4], "Phone no:", i[5])
                    ch_user[1] = input("Name of Patient: ")
                    ch_user[3] = input("Gender: ")
                    ch_user[4] = int(input("Age: "))
                    ch_user[5] = int(input("Phone Number of Patient: "))
                    if c_user != "admin":
                        ch_user[2] = input("Enter Password: ")
                    temp.append(ch_user)
        with open("patient-details.csv", "w", newline="") as chf:
            cw = csv.writer(chf)
            cw.writerows(temp)
    except FileNotFoundError:
        print("File not Found!")


def Bed_Allot():
    print()
    pat_bed = True
    pat_id = input("Enter Patient ID-> ")
    try:
        with open("reg_diary.csv", "r") as doc:
            cr = csv.reader(doc, delimiter=',')
            for i in cr:
                if i[0] == pat_id[3:]:
                    pat_bed = False
                    print("You have been alloted a floor on-")
                    print("Floor Number:", i[7], "| Bed Number:", i[8])
            if pat_bed:
                print("You have no bed alloted.")
    except FileNotFoundError:
        print("File not found.")


def Bill_Rep():
    pat_id = input("Enter Patient ID-> ")
    try:
        with open("reg_diary.csv", "r") as doc:
            cr = csv.reader(doc, delimiter=',')
            for i in cr:
                if i[0] == pat_id[3:]:
                    with open("doctor.csv", "r") as fee:
                        cread = csv.reader(fee, delimiter=',')
                        for j in cread:
                            if i[5] == j[1]:
                                doc_fee = int(j[3])
                    bed_charges = 8000
                    pat_meal = 1000
                    Nursing_fee = 500
                    total = doc_fee + bed_charges + pat_meal + Nursing_fee
                    Tax = 0.08*(total)
                    tot_tax = total + Tax
                    print()
                    print("Patient Name:", i[1])
                    print("Gender:", i[2], "; Age:", i[3])
                    print("Doctor Consulted:", i[5], "| Department:", i[4])
                    print("Date of Consultation:", i[6])
                    print("Bed Alloted on Floor Number->",
                          i[7], "| Room Number->", i[8])
                    print()
                    print("/"*38)
                    print()
                    print("%24s" % ("Doctor Fees:"), doc_fee, "INR")
                    print("%24s" % ("Bed Charges:"), bed_charges, "INR")
                    print("%24s" % ("Patient Meal Charges:"), pat_meal, "INR")
                    print("%24s" % ("Nursing Fees:"), Nursing_fee, "INR")
                    print("-"*38)
                    print("%24s" % ("Total Bill without Tax:"), total, "INR")
                    print("%24s" % ("Total Bill with Tax:"), tot_tax, "INR")
    except FileNotFoundError:
        print("File not found.")


def sort_key(ls):
    return ls[sort_by]


def Sort_Pat(c_user):
    temp = []
    try:
        with open("reg_diary.csv", "r") as doc:
            cr = csv.reader(doc, delimiter=',')
            for i in cr:
                temp.append(i)
        print('''1:Arrange by reg_id
2:Arrange by Name
3:Arrange by Age
4:Arrange by Patient's Doctor
5:Arrange by Date

Enter your choice -> ''', end="")
        ch = input()
        global sort_by
        if ch == "1" or ch == "2":
            sort_by = int(ch) - 1
            temp.sort(key=sort_key)
            for j in temp:
                print(j)
        elif ch == "3":
            sort_by = 3
            temp.sort(key=sort_key)
            for j in temp:
                print(j)
        elif ch == "4":
            sort_by = 5
            temp.sort(key=sort_key)
            for j in temp:
                print(j)
        elif ch == "5":
            sort_by = 6
            temp.sort(key=sort_key)
            for j in temp:
                print(j)
        else:
            print("This function is not available for", ch)
    except FileNotFoundError:
        print("File not found!")


def Doc_Display():
    print()
    try:
        with open("doctor.csv", "r") as doc:
            cr = csv.reader(doc, delimiter=',')
            for i in cr:
                print("Doctor ID: %3s | Name: %20s | Department: %18s | Fee: %4s" %
                      (i[0], i[1], i[2], i[3]))
    except FileNotFoundError:
        print("File not found.")


def Del_Pat():
    temp = []
    uid = input("Enter User Id of the patient-> ")
    try:
        with open("patient-details.csv", "r") as doc1:
            cr = csv.reader(doc1, delimiter=',')
            for i in cr:
                temp.append(i)
    except FileNotFoundError:
        print("File not found!")
    for j in temp:
        if j[0] == uid:
            print("Patient Name:", j[1], "| Mobile Number:", j[2])
            temp.remove(j)
            print("User Deleted!")
    try:
        with open("patient-details.csv", "w", newline="") as doc2:
            cw = csv.writer(doc2)
            cw.writerows(temp)
    except FileNotFoundError:
        print("File not found!")


def Edit_Doc():
    A = []
    Y = input("Enter Doctor id:   ")
    try:
        with open("doctor.csv", "r") as dl:
            cv = csv.reader(dl, delimiter=',')
            for i in cv:
                A.append(i)
        for j in A:
            if j[0] == Y:
                print("Name:", j[1], "; Branch:", j[2], "; Fee:", j[3])
                j[1] = input("Name of Doctor: ")
                j[2] = input("Branch of Doctor: ")
                j[3] = int(input("Fee of Doctor: "))
                print()
                print("Doctor Details Updated.")
                break
        else:
            print("Wrong Doctor ID")
        with open("doctor.csv", "w", newline="") as doc:
            cw = csv.writer(doc)
            cw.writerows(A)
    except FileNotFoundError:
        print("File Not Found")


def View_Appoint():
    print()
    try:
        with open("reg_diary.csv", "r") as doc:
            cr = csv.reader(doc, delimiter=',')
            for i in cr:
                print(i)
    except FileNotFoundError:
        print("File not found!")


def View_patient_details():
    print()
    try:
        with open("patient-details.csv", "r") as pf:
            cv = csv.reader(pf)
            for i in cv:
                print(i)
    except FileNotFoundError:
        print("File Not Found")


def View_Report():
    print()
    try:
        with open("Report.csv", "r") as qu:
            cr = csv.reader(qu, delimiter=',')
            for i in cr:
                print("Query:", i[0])
                print("Asked By:", i[1])
                print()
    except FileNotFoundError:
        print("File Not Found")


def Report():
    print()
    try:
        with open("Report.csv", "a", newline="") as qu:
            cw = csv.writer(qu)
            AB = []
            while True:
                Ques = input("Please Report your Query: ")
                email = input("Enter your email id: ")
                AB.append(Ques)
                AB.append(email)
                cw.writerow(AB)
                AB = []
                ch = input("More query Yes or No: ")
                if ch == "No" or ch == "no" or ch == "n":
                    break
        print()
        print("Your Query will soon be answered by our staff. Thank you!")

    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    print("##### Welcome To KAILASH Hospital #####")
    print("Please Login or SignUp - ")
    Login()
    if current_user != "null":
        while True:
            print()
            print('''Patient Options:
1. Patient Registration
2. Display Doctor Details
3. Edit Patient Details
4. Cancel Appointment
5. Bed Allotment
6. Billing
7. Report
8. Quit (type q or Q or 8)''')
            if current_user == "admin":
                print()
                print('''Admin Options :
A1. View all Appointments
A2. Sort Patients
A3. Delete Patient
A4. View Report
A5. View Patient Details
A6. Edit Doctor Details''')
            print()
            opt = input("Enter an option-> ")
            if opt == "1":
                Patient_Reg(current_user)
            elif opt == "2":
                Doc_Display()
            elif opt == "3":
                Editpatient_details(current_user, current_uid)
            elif opt == "4":
                Cancel_Appoint(current_user)
            elif opt == "5":
                Bed_Allot()
            elif opt == "6":
                Bill_Rep()
            elif opt == "7":
                Report()
            elif opt == "A1" or opt == "a1":
                View_Appoint()
            elif opt == "A2" or opt == "a2":
                Sort_Pat(current_user)
            elif opt == "A3" or opt == "a3":
                Del_Pat()
            elif opt == "A4" or opt == "a4":
                View_Report()
            elif opt == "A5" or opt == "a5":
                View_patient_details()
            elif opt == "A6" or opt == "a6":
                Edit_Doc()
            elif opt == "q" or opt == "Q" or opt == "8":
                print("Thank You!")
                break
            else:
                print("Not an option! Enter Again.")
    else:
        print("Something went wrong! Try again Later.")
