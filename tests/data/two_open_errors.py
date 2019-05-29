def get_filename1_text():
    with open("filename1.txt", "r") as file1:
        return file1.read()


with open("filename2.txt", "r") as file2:
    file2.read()
