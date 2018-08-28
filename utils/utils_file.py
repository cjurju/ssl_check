import os
import difflib

class FileUtils():

    """
    The open_file() function is used to open files.
    It takes 2 parameters:
        - file : name of file to open
        - mode : "r" for reading, "w" for writing, "a" to append
    """
    def open_file(self, file, mode):
        try:
            file_in = open(file, mode)
        except FileNotFoundError:
            print(f"File '{file}' does not exist.")
        except IOError as e:
            errno, strerror = e.args
            print("I/O error({0}): {1}".format(errno,strerror))

        return file_in


    def remove_file(self, file):
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f"File '{file}' does not exist")


    def rename_file(self, source, destination):
        try:
            os.rename(source, destination)
        except FileNotFoundError:
            print("Exception at file renaming")


    def format_file(self, file):
        file.write(str().ljust(100, '#') + '\n')
        file.write(str().ljust(15, ' ') + 'HOSTNAME' + str().ljust(37, ' ') +
                   'CERTIFICATE_EXPIRY_DATE' + str().ljust(15, ' ') + '\n')
        file.write(str().ljust(100, '#') + '\n\n')


    def compare_content(self, text_1, text_2):
        d = difflib.Differ()
        diff = d.compare(text_1, text_2)
        print(''.join(diff))