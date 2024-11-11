import pandas as pd


def parse_registration_number(reg_number):
    """
    解析注册证号，提取产品来源和登记年份
    参数：
        reg_number: 注册证号（如：国食注字TY20175001）
    返回：
        tuple: (产品来源, 登记年份)
    """
    try:
        # 找到"TY"的位置，便于准确定位
        ty_pos = reg_number.find('TY')
        if ty_pos == -1:
            return "", ""

        # 提取年份（TY后面的4位）
        year = reg_number[ty_pos + 2:ty_pos + 6]

        # 提取顺序号第一位（年份后的第一位）
        first_digit = reg_number[ty_pos + 6]

        # 判断产品来源
        source = "进口产品" if first_digit == "5" else "国产产品"

        return source, year
    except:
        # 如果解析失败，返回空值
        return "", ""


def process_registration_info():
    """
    处理注册证号信息并更新Excel文件
    """
    try:
        # 读取result2.xlsx
        print("读取result2.xlsx...")
        df = pd.read_excel('result/result2.xlsx')

        # 解析每个注册证号
        print("正在解析注册证号...")
        results = [parse_registration_number(reg_num) for reg_num in df['注册证号']]

        # 添加产品来源和登记年份列
        df['产品来源'] = [result[0] for result in results]
        df['登记年份'] = [result[1] for result in results]

        # 保存结果
        df.to_excel('result/result2.xlsx', index=False)
        print("结果已保存到result2.xlsx")

        # 统计产品来源
        source_counts = df['产品来源'].value_counts()
        print("\n产品来源统计：")
        print(f"进口产品数量: {source_counts.get('进口产品', 0)}")
        print(f"国产产品数量: {source_counts.get('国产产品', 0)}")

        # 显示前5款特医食品的结果
        print("\n前5款特医食品的结果：")
        columns = ['企业名称', '产品名称', '注册证号', '产品来源', '登记年份']
        print(df[columns].head())

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    process_registration_info()