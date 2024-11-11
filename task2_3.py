import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_product_categories():
    """
    分析不同产品类别的获批数量并绘制柱状图
    """
    # 读取数据
    print("读取result2.xlsx...")
    df = pd.read_excel('result/result2.xlsx')

    # 统计产品类别数量并降序排列
    category_counts = df['产品类别'].value_counts()

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 创建图形
    plt.figure(figsize=(12, 6))

    # 使用自定义颜色绘制柱状图
    colors = sns.color_palette("husl", len(category_counts))
    bars = plt.bar(range(len(category_counts)), category_counts.values, color=colors)

    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    # 设置图形属性
    plt.title('特医食品不同产品类别获批数量分布', fontsize=14, pad=20)
    plt.xlabel('产品类别', fontsize=12)
    plt.ylabel('获批数量', fontsize=12)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # 设置x轴刻度标签
    plt.xticks(range(len(category_counts)), category_counts.index, rotation=45, ha='right')

    # 调整布局，防止标签被截断
    plt.tight_layout()

    # 保存图形
    plt.savefig('result/product_categories.png', dpi=300, bbox_inches='tight')
    print("柱状图已保存到result/product_categories.png")

    # 输出统计分析
    print("\n产品类别统计分析：")
    print("\n1. 各类别获批数量：")
    for category, count in category_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{category}: {count}个 (占比{percentage:.1f}%)")

    # 计算其他统计指标
    print(f"\n2. 总体情况：")
    print(f"产品类别总数: {len(category_counts)}种")
    print(f"最多获批数量: {category_counts.max()}个 (类别: {category_counts.index[0]})")
    print(f"最少获批数量: {category_counts.min()}个 (类别: {category_counts.index[-1]})")

    # 计算集中度
    top_3_percentage = (category_counts.head(3).sum() / len(df)) * 100
    print(f"\n3. 集中度分析：")
    print(f"前三类别合计占比: {top_3_percentage:.1f}%")


def main():
    try:
        analyze_product_categories()
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    main()