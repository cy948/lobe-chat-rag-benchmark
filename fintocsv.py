import jsonlines
import openpyxl

# 输入 JSONL 文件名
input_file = 'data/fin.jsonl'
# 输出 XLSX 文件名
output_file = 'fin.xlsx'

# 创建一个新的工作簿
wb = openpyxl.Workbook()
# 获取当前活跃的工作表
ws = wb.active

# 打开 JSON Lines 文件进行读取
with jsonlines.open(input_file) as reader:
    # 逐行读取 JSON Lines 文件
    for index, obj in enumerate(reader):
        # 如果这是第一行，写入表头
        if index == 0:
            headers = list(obj.keys())
            ws.append(headers)
        
        # 写入每一行数据
        row = [obj.get(header) for header in headers]
        ws.append(row)

# 保存工作簿
wb.save(output_file)

print("转换完成！")