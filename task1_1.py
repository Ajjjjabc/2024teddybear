import pdfplumber
import pandas as pd
import os
import re
from pathlib import Path

# 定义需要提取的营养成分及其单位，使用严格匹配
NUTRIENTS = [
    ('能量', 'kJ', ['能量', '能量(kJ)']),
    ('脂肪', 'g', ['脂肪', '脂肪(g)']),
    ('碳水化合物', 'g', ['碳水化合物', '碳水化合物(g)']),
    ('蛋白质', 'g', ['蛋白质', '蛋白质(g)', '蛋白质（等同物）']),
    ('钠', 'mg', ['钠', '钠(mg)']),
    ('氯', 'mg', ['氯', '氯(mg)']),
    ('钾', 'mg', ['钾', '钾(mg)']),
    ('磷', 'mg', ['磷', '磷(mg)'])
]


def clean_text(text):
    """
    清理文本，去除多余的空格和特殊字符
    """
    return ' '.join(text.split())


def find_value_for_100kJ(text_lines, nutrient_name, match_texts):
    """
    在文本行中查找特定营养成分每100kJ的值
    处理两种不同的表格格式：
    1. 营养成分 每100g 每100mL 每100kJ
    2. 营养成分 每100g 每100kJ 每份
    """
    try:
        # 找到表头行（包含"每100kJ"的行）
        header_idx = -1
        for i, line in enumerate(text_lines):
            if '每100kJ' in line:
                header_idx = i
                break

        if header_idx == -1:
            return 0

        # 获取表头行，确定"每100kJ"的位置
        header = clean_text(text_lines[header_idx])
        header_parts = header.split()
        kj_col_idx = header_parts.index('每100kJ')

        # 在表头行之后的行中查找目标营养成分
        for i in range(header_idx + 1, len(text_lines)):
            line = clean_text(text_lines[i])
            if not line:  # 跳过空行
                continue

            parts = line.split()
            if not parts:  # 跳过空行
                continue

            # 检查是否匹配目标营养成分
            if any(text in parts[0] for text in match_texts):
                try:
                    # 使用"每100kJ"列的索引获取对应的值
                    value = float(parts[kj_col_idx])
                    return value
                except (IndexError, ValueError):
                    continue

    except Exception as e:
        print(f"提取{nutrient_name}值时出错: {str(e)}")

    return 0


def extract_nutrition_data(pdf_path):
    """
    从PDF文件中提取营养成分数据
    """
    result = {f"{nutrient}({unit})": 0 for nutrient, unit, _ in NUTRIENTS}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ''
            for page in pdf.pages:
                all_text += page.extract_text() + '\n'

            text_lines = all_text.split('\n')

            # 寻找营养成分表部分
            table_lines = []
            in_table = False
            for i, line in enumerate(text_lines):
                # 开始标记
                if '营养成分表' in line:
                    in_table = True
                    continue

                # 结束标记
                if in_table and ('】' in line or '备注' in line):
                    break

                if in_table:
                    table_lines.append(line)

            # 处理每个营养成分
            if table_lines:
                for nutrient, unit, match_texts in NUTRIENTS:
                    value = find_value_for_100kJ(table_lines, nutrient, match_texts)
                    result[f"{nutrient}({unit})"] = value

    except Exception as e:
        print(f"处理文件 {pdf_path} 时出错: {str(e)}")

    return result


def process_all_pdfs():
    """
    处理所有PDF文件并生成结果Excel
    """
    # 创建结果DataFrame的列名
    columns = ['注册证号'] + [f"{nutrient}({unit})" for nutrient, unit, _ in NUTRIENTS]

    # 获取所有PDF文件路径
    pdf_folder = Path("DATA/books")
    pdf_files = list(pdf_folder.glob("*.pdf"))

    # 处理每个PDF文件
    results = []
    total_files = len(pdf_files)

    print(f"开始处理PDF文件，共{total_files}个文件")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"正在处理: {pdf_file.name} ({i}/{total_files})")

        # 从文件名获取注册证号
        reg_number = pdf_file.stem

        # 提取营养成分数据
        nutrition_data = extract_nutrition_data(pdf_file)

        # 添加注册证号
        nutrition_data['注册证号'] = reg_number

        # 将结果添加到列表中
        results.append(nutrition_data)

    # 创建DataFrame
    df = pd.DataFrame(results)

    # 重新排列列顺序
    df = df[columns]

    # 保存到Excel文件
    df.to_excel('result/result1.xlsx', index=False)
    print(f"\n结果已保存到: result/result1.xlsx")

    # 找出蛋白质含量最高的三种特医食品
    # 输出注册证号、能量、脂肪、碳水化合物、蛋白质、钠、氯、钾、磷
    top_3_protein = df.nlargest(3, '蛋白质(g)')
    print("\n蛋白质含量最高的三种特医食品：")
    
    # 打印表头
    print("注册证号\t能量(kJ)\t脂肪(g)\t碳水化合物(g)\t蛋白质(g)\t钠(mg)\t氯(mg)\t钾(mg)\t磷(mg)")
    
    # 打印每个食品的详细信息
    for index, row in top_3_protein.iterrows():
        print(f"{row['注册证号']}\t{row['能量(kJ)']}\t{row['脂肪(g)']}\t{row['碳水化合物(g)']}\t{row['蛋白质(g)']}\t{row['钠(mg)']}\t{row['氯(mg)']}\t{row['钾(mg)']}\t{row['磷(mg)']}")
    
    print("\n")
    


if __name__ == "__main__":
    process_all_pdfs()