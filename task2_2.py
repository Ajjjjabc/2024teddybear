import pandas as pd
import plotly.graph_objects as go


def create_sunburst_chart():
    """
    创建旭日图并进行数据分析
    """
    # 读取数据
    print("读取result2.xlsx...")
    df = pd.read_excel('result/result2.xlsx')

    # 统计每个组合的数量
    grouped_data = df.groupby(['适用人群类别', '产品来源']).size().reset_index(name='数量')

    # 计算内层（适用人群类别）的总数
    category_total = df['适用人群类别'].value_counts()

    # 准备旭日图数据
    labels = []  # 所有标签
    parents = []  # 父节点
    values = []  # 数值

    # 添加内层数据（适用人群类别）
    for category in category_total.index:
        labels.append(category)
        parents.append("")  # 内层节点没有父节点
        values.append(category_total[category])

    # 添加外层数据（产品来源）
    for _, row in grouped_data.iterrows():
        # 构建标签（显示具体数量）
        label = f"{row['产品来源']}({row['数量']}个)"
        labels.append(label)
        parents.append(row['适用人群类别'])
        values.append(row['数量'])

    # 创建旭日图
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",  # 显示实际数值而不是百分比
    ))

    # 设置图形标题和样式
    fig.update_layout(
        title={
            'text': '特医食品产品来源与适用人群类别分布',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        width=800,
        height=800,
    )

    # 保存为HTML文件（交互式）
    fig.write_html("result/sunburst_chart.html")
    print("旭日图已保存到result/sunburst_chart.html")

    # 输出统计分析
    print("\n数据统计与分析：")
    print("\n1. 适用人群类别统计：")
    for category, count in category_total.items():
        print(f"{category}: {count}个")

    print("\n2. 详细分布统计：")
    for _, row in grouped_data.iterrows():
        percentage = (row['数量'] / len(df)) * 100
        print(f"{row['适用人群类别']} - {row['产品来源']}: {row['数量']}个 "
              f"(占总数的{percentage:.1f}%)")

    # 计算每个类别中的国产/进口比例
    print("\n3. 各类别中的国产/进口比例：")
    for category in df['适用人群类别'].unique():
        category_data = df[df['适用人群类别'] == category]
        source_ratio = category_data['产品来源'].value_counts()
        total = len(category_data)
        print(f"\n{category}:")
        for source, count in source_ratio.items():
            ratio = (count / total) * 100
            print(f"  {source}: {count}个 ({ratio:.1f}%)")


def main():
    try:
        create_sunburst_chart()
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    main()