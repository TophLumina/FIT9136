print("CHECK FILENAMES")

# department set
departments = {"dep1", "dep2", "dep3"}

# file-department set
file_arch = {
    ("filea", "dep1"),
    ("fileb", "dep1"),
    ("filec", "dep2"),
    ("filed", "dep2"),
    ("filea", "dep3"),
    ("filec", "dep3"),
}

# file-password map
passwords = {"fileb": "pass1", "filed": "pass2"}

# access flag
access = False

while 1:
    file_department = input("Input a department (or quit to exit): ")
    if file_department == "quit":
        break

    # check if the department is in the department set
    if file_department in departments:
        while 1:
            file_name = input("Input a filename: ")
            if len(file_name) > 0:
                break

        # check if the file-department is in the file-department set
        tmp = "*is not*"
        if (file_name, file_department) in file_arch:
            tmp = "is"
            # set access flag to TRUE if the file is not in the file-password map
            if file_name not in passwords:
                access = True
            # 3 chances to provide a valid password if the file is in the file-password map
            else:
                for chance in range(0, 3):
                    print(3 - chance, "password attempts remain.")
                    password = input("Input password: ")
                    # check if the password match the item in file-password map
                    if passwords[file_name] == password:
                        access = True
                        break

        # check if the user grant access or the file and department doesn't match
        if access or (not access and tmp == "*is not*"):
            print(file_name, "-", tmp, "a valid filename for -", file_department)
            # reset access flag to FALSE
            access = False

print("GOODBYE")
