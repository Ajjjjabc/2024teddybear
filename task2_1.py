import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_approval_trends():
    """
    分析特医食品获批数量趋势并绘制双折线图
    """
    # 读取数据
    print("读取result2.xlsx...")
    df = pd.read_excel('result/result2.xlsx')

    # 按年份和产品来源统计数量
    stats = df.groupby(['登记年份', '产品来源']).size().unstack(fill_value=0)

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 创建图形
    plt.figure(figsize=(12, 6))

    # 绘制双折线图
    for column in stats.columns:
        plt.plot(stats.index, stats[column], marker='o', label=column)

        # 添加数据标签
        for x, y in zip(stats.index, stats[column]):
            plt.annotate(str(int(y)),
                         (x, y),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

    # 设置图形属性
    plt.title('特医食品历年获批数量趋势', fontsize=14, pad=20)
    plt.xlabel('登记年份', fontsize=12)
    plt.ylabel('获批数量', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left')

    # 调整x轴刻度，确保显示所有年份
    plt.xticks(stats.index, rotation=45)

    # 调整布局，防止标签被截断
    plt.tight_layout()

    # 保存图形
    plt.savefig('result/approval_trends.png', dpi=300, bbox_inches='tight')
    print("趋势图已保存到result/approval_trends.png")

    # 输出统计数据
    print("\n按年份和产品来源统计的获批数量：")
    print(stats)

    # 计算总体统计信息
    total_by_source = stats.sum()
    print("\n总体统计：")
    print(f"进口产品总数：{int(total_by_source['进口产品'])}")
    print(f"国产产品总数：{int(total_by_source['国产产品'])}")

    # 分析年度变化
    annual_total = stats.sum(axis=1)
    max_year = annual_total.idxmax()
    min_year = annual_total.idxmin()

    print(f"\n获批数量最多的年份是{max_year}年，共{int(annual_total[max_year])}个")
    print(f"获批数量最少的年份是{min_year}年，共{int(annual_total[min_year])}个")

    # 计算近年趋势
    recent_years = stats.tail(3)
    print("\n近三年获批情况：")
    print(recent_years)


def main():
    try:
        analyze_approval_trends()
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    main()