# -*- coding:utf-8 -*-
# 文件 ：6.py
# IED ：PyCharm
# 时间 ：2019/12/13 0013 15:59
# 版本 ：V1.0


import json
import os
import re
import xlwt

'''
第七步读取数据文件，生成excel
'''
if __name__ == "__main__":
    rootPath = "newJson/"
    workbook = xlwt.Workbook(encoding='ascii')  # 创建一个文件
    worksheet = workbook.add_sheet('汽车之家')  # 创建一个表
    files = os.listdir(rootPath)
    startRow = 0
    isFlag = True  # 默认记录表头
    for file in files:
        list = []
        carItem = {}
        print("fileName==" + file.title())
        text = ""
        for fi in open(rootPath + file, 'r', encoding="utf-8"):
            text = text + fi
        # else:
        # print("文件内容=="+text)
        # 解析基本参数配置参数，颜色三种参数，其他参数
        config = "var config = (.*?);"
        option = "var option = (.*?);"
        bag = "var bag = (.*?);"
        color = "var color = (.*?);"
        innerColor = "var innerColor = (.*?);"

        configRe = re.findall(config, text)
        optionRe = re.findall(option, text)
        bagRe = re.findall(bag, text)
        colorRe = re.findall(color, text)
        innerColorRe = re.findall(innerColor, text)
        for a in configRe:
            config = a
        print("++++++++++++++++++++++\n")
        for b in optionRe:
            option = b
            print("---------------------\n")
        for c in bagRe:
            bag = c
        for d in colorRe:
            color = d
        for e in innerColorRe:
            innerColor = e
        # print(config)
        # print(option)
        # print(bag)

        # print(bag)
        try:
            config = json.loads(config)
            option = json.loads(option)
            bag = json.loads(bag)
            color = json.loads(color)
            innerColor = json.loads(innerColor)
            path = "autoHome.xls"

            configItem = config['result']['paramtypeitems'][0]['paramitems']
            optionItem = option['result']['configtypeitems'][0]['configitems']
        except Exception as e:
            f = open("错误记录.txt", "a", encoding="utf-8")
            f.write(file.title() + "\n")
            continue

        # 解析基本参数
        for car in configItem:
            carItem[car['name']] = []
            for ca in car['valueitems']:
                carItem[car['name']].append(ca['value'])
        # print(carItem)
        # 解析配置参数
        for car in optionItem:
            carItem[car['name']] = []
            for ca in car['valueitems']:
                carItem[car['name']].append(ca['value'])

        if isFlag:
            co1s = 0

            for co in carItem:
                co1s = co1s + 1
                worksheet.write(startRow, co1s, co)
            else:
                startRow = startRow + 1
                isFlag = False

        # 计算起止行号
        endRowNum = startRow + len(carItem['车型名称'])  # 车辆款式记录数
        for row in range(startRow, endRowNum):
            print(row)
            colNum = 0
            for col in carItem:
                colNum = colNum + 1
                print(str(carItem[col][row - startRow]), end='|')
                worksheet.write(row, colNum, str(carItem[col][row - startRow]))

        else:
            startRow = endRowNum
    workbook.save('Mybook.xls')
