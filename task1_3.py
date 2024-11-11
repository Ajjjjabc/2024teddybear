import pandas as pd


def classify_population(text):
    """
    根据适用人群文本判断类别
    参数：
        text: 适用人群文本
    返回：
        '特医婴配食品' 或 '1岁以上特医食品'
    """
    # 定义婴儿关键词
    infant_keywords = [
        '婴儿',
    ]

    # 如果适用人群为空，返回1岁以上特医食品
    if pd.isna(text):
        return '1岁以上特医食品'

    # 检查是否包含婴儿相关关键词
    text = str(text).lower()  # 转换为小写，统一处理
    for keyword in infant_keywords:
        if keyword in text:
            return '特医婴配食品'

    return '1岁以上特医食品'


def process_classification():
    """
    处理文件并添加适用人群类别
    """
    try:
        # 读取result2.xlsx
        print("读取result2.xlsx...")
        df = pd.read_excel('result/result2.xlsx')

        # 添加适用人群类别列
        print("正在进行适用人群分类...")
        df['适用人群类别'] = df['适用人群'].apply(classify_population)

        # 保存结果
        df.to_excel('result/result2.xlsx', index=False)
        print("结果已保存到result2.xlsx")

        # 统计两个类别的数量
        category_counts = df['适用人群类别'].value_counts()
        print("\n分类统计结果：")
        print(f"特医婴配食品数量: {category_counts.get('特医婴配食品', 0)}")
        print(f"1岁以上特医食品数量: {category_counts.get('1岁以上特医食品', 0)}")

        # 显示一些示例
        print("\n部分分类示例：")
        samples = df[['注册证号', '适用人群', '适用人群类别']].head()
        print(samples)

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    process_classification()