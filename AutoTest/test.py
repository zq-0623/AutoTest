# -*- coding: utf-8 -*-

file_path = "./df-sz.log"
file = open(file_path,"r",encoding="utf-8")
content = file.read()
count_num = content.count("checkPriceLineUp_Start")
print(count_num)
