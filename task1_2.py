import pdfplumber
import pandas as pd
from pathlib import Path


def extract_label_content(text, label):
    """
    从文本中提取指定标签的内容，并清理标点符号
    参数：
        text: PDF文本内容
        label: 要提取的标签（如【产品类别】）
    返回：
        清理后的内容，如果没找到返回空字符串
    """
    try:
        # 查找标签的起始位置
        start_idx = text.find(label)
        if start_idx == -1:
            return ''

        # 从标签后开始查找内容
        content_start = start_idx + len(label)

        # 查找下一个【标签】作为内容结束
        next_label = text.find('【', content_start)

        # 提取内容
        if next_label == -1:
            # 如果没有找到下一个标签，查找下一个换行
            line_end = text.find('\n', content_start)
            if line_end == -1:
                content = text[content_start:].strip()
            else:
                content = text[content_start:line_end].strip()
        else:
            content = text[content_start:next_label].strip()

        # 清理内容，去除句号
        content = content.rstrip('。').rstrip('.')

        return content

    except Exception as e:
        print(f"提取{label}时出错: {str(e)}")
        return ''


def extract_pdf_info(pdf_path):
    """
    从PDF文件中提取产品类别、组织状态和适用人群信息
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # 提取所有页面文本
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'

            # 提取三个标签的内容
            category = extract_label_content(text, '【产品类别】')
            state = extract_label_content(text, '【组织状态】')
            population = extract_label_content(text, '【适用人群】')

            # 记录提取结果到日志
            log_entry = f"文件: {pdf_path.name}\n"
            log_entry += f"产品类别: {category}\n"
            log_entry += f"组织状态: {state}\n"
            log_entry += f"适用人群: {population}\n"
            log_entry += "-" * 50 + "\n"

            with open('result/info.txt', 'a', encoding='utf-8') as f:
                f.write(log_entry)

            return {
                '产品类别': category,
                '组织状态': state,
                '适用人群': population
            }

    except Exception as e:
        print(f"处理文件 {pdf_path} 时出错: {str(e)}")
        return {'产品类别': '', '组织状态': '', '适用人群': ''}


def process_all_files():
    """
    处理所有文件并生成结果
    """
    # 创建新的info.txt文件
    with open('result/info.txt', 'w', encoding='utf-8') as f:
        f.write("提取结果日志\n")
        f.write("=" * 50 + "\n")

    # 读取原始数据
    print("读取data.xlsx...")
    df = pd.read_excel('DATA/data.xlsx')

    # 用于存储提取的信息
    extracted_info = []

    # 处理每个PDF文件
    total_files = len(df)
    print(f"开始处理PDF文件，共{total_files}个文件")

    for index, row in df.iterrows():
        reg_number = row['注册证号']
        pdf_path = Path(f"DATA/books/{reg_number}.pdf")

        print(f"正在处理: {reg_number} ({index + 1}/{total_files})")

        # 提取PDF信息
        info = extract_pdf_info(pdf_path)
        extracted_info.append(info)

    # 将提取的信息添加到DataFrame中
    for key in ['产品类别', '组织状态', '适用人群']:
        df[key] = [info[key] for info in extracted_info]

    # 保存结果
    df.to_excel('result/result2.xlsx', index=False)
    print("\n结果已保存到: result/result2.xlsx")

    # 打印前5款特医食品的结果
    print("\n前5款特医食品的结果：")
    print(df.head()[['企业名称', '产品名称', '注册证号', '有效期至', '产品类别', '组织状态', '适用人群']])

    # 统计特殊情况
    empty_category = df['产品类别'].isna().sum()
    empty_state = df['组织状态'].isna().sum()
    empty_population = df['适用人群'].isna().sum()

    print("\n特殊情况统计：")
    print(f"缺少产品类别的文件数: {empty_category}")
    print(f"缺少组织状态的文件数: {empty_state}")
    print(f"缺少适用人群的文件数: {empty_population}")


if __name__ == "__main__":
    process_all_files()