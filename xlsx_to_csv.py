import os
import openpyxl
import csv
import sys

# ------------------------------------------------------------------------- #
# 日期：2023年11月6日
# 功能：xlsx格式转换为csv格式
# 使用说明：直接运行该脚本，把对应目录的绝对路径贴进去即可。（注意路径不要添加引号）
# ------------------------------------------------------------------------- #

def main():
    xlsx_dir = input('请输入 Xlsx 文件目录：')
    csv_dir = input('请输入 Csv 文件输出目录：')

    if not os.path.exists(xlsx_dir):
        print(f'{xlsx_dir} 不存在!')
        sys.exit(1)

    os.makedirs(csv_dir, exist_ok=True)

    for filename in os.listdir(xlsx_dir):
        print(f'开始转换 {filename}')
        if filename.endswith('.xlsx'):
            xlsx_file = os.path.join(xlsx_dir, filename)
            workbook = openpyxl.load_workbook(xlsx_file)
            sheet = workbook.active
            csv_filename = os.path.splitext(filename)[0] + '.csv'
            csv_file = os.path.join(csv_dir, csv_filename)

            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                for row in sheet.iter_rows(values_only=True):
                    csv_writer.writerow(row)
            workbook.close()
    print('已全部转换完毕')

if __name__ == '__main__':
    main()