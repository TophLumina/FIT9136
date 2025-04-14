print("CHECK FILENAMES")

# file set
file_arch = {"filea", "fileb", "filec", "filed", "filee"}

while 1:
    file_name = input("Input a filename (or quit to exit): ")
    if file_name == "quit":
        break

    # check if the target file is in the file set
    tmp = "*is not*"
    if file_name in file_arch:
        tmp = "is"

    print(file_name, "-", tmp, "a valid filename.")

print("GOODBYE")
