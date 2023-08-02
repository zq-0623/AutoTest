from openpyxl.styles import PatternFill
from openpyxl.styles import colors,Font
import openpyxl as vb

#读取 需要对比的excel表
workbook_a = vb.load_workbook(r'表1.xlsx')
workbook_b = vb.load_workbook(r'表2.xlsx')
#读取需要对比的sheet名
sheet_a = workbook_a['Sheet1']
sheet_b = workbook_b['Sheet1']
#遍历所有的行与列
maxrow = sheet_a.max_row
maxcolumn = sheet_b.max_column

#循环对比表格的所有单元格数据
for i in range(1,maxrow):
    for j in range(1,maxcolumn):
        cell_a = sheet_a.cell(i,j)
        cell_b = sheet_b.cell(i,j)
        #如果有差异数据，就标识出来(蓝色加粗字体，黄色填充)，
        if cell_a.value != cell_b.value:
            cell_a.fill = PatternFill("solid",fgColor='FFFF00')
            cell_a.font = Font(color=colors.BLUE,bold=True)
            cell_b.fill = PatternFill("solid",fgColor='FFFF00')
            cell_b.font = Font(color=colors.BLUE,bold=True)
#差异结果存入新的excel表中
workbook_a.save('表1_差异结果.xlsx')
workbook_b.save('表2_差异结果.xlsx')

print("执行对比完成")
