'''
Author: Mrx
Date: 2023-03-19 19:33:33
LastEditors: Mrx
LastEditTime: 2023-03-19 19:36:39
FilePath: \cs271_final_project\log.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
my_list = ["item 1", "item 2", "item 3"]

# Writing the list to a file
with open("my_file.txt", "w") as file:
    for item in my_list:
        file.write(item + "\n")

# Reading the list from the file
with open("my_file.txt", "r") as file:
    my_list = [line.strip() for line in file.readlines()]

print(my_list)
