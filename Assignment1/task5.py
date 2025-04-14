print("CHECK FILENAMES")

# department set
departments = {"dep1", "dep2", "dep3"}

# file-department set
file_arch = {
    ("filea", "dep1"),
    ("fileb", "dep1"),
    ("filec", "dep2"),
    ("filea", "dep3"),
    ("filec", "dep3"),
}

while 1:
    file_department = input("Input a department (or quit to exit): ")
    if file_department == "quit":
        break

    # check if the target department is in the department set
    if file_department in departments:
        while 1:
            file_name = input("Input a filename: ")
            if len(file_name) > 0:
                break

        # check if the target file-department is in the file-department set
        tmp = "*is not*"
        if (file_name, file_department) in file_arch:
            tmp = "is"
        print(file_name, "-", tmp, "a valid filename for -", file_department)

print("GOODBYE")
