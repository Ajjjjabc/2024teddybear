import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def analyze_fat_protein_distribution():
    """
    分析脂肪和蛋白质含量的分布并绘制直方图
    """
    # 读取数据
    print("读取result1.xlsx...")
    df = pd.read_excel('result/result1.xlsx')

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 创建图形
    plt.figure(figsize=(12, 6))

    # 绘制直方图
    # alpha设置透明度，避免完全遮挡
    plt.hist(df['脂肪(g)'], bins='auto', alpha=0.6, color='skyblue',
             label='脂肪含量', edgecolor='black')
    plt.hist(df['蛋白质(g)'], bins='auto', alpha=0.6, color='lightcoral',
             label='蛋白质含量', edgecolor='black')

    # 设置图形属性
    plt.title('特医食品脂肪和蛋白质含量分布', fontsize=14, pad=20)
    plt.xlabel('含量 (g/100kJ)', fontsize=12)
    plt.ylabel('频数', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # 调整布局
    plt.tight_layout()

    # 保存图形
    plt.savefig('result/fat_protein_distribution.png', dpi=300, bbox_inches='tight')
    print("分布图已保存到result/fat_protein_distribution.png")

    # 计算统计指标
    fat_stats = df['脂肪(g)'].describe()
    protein_stats = df['蛋白质(g)'].describe()

    print("\n统计分析：")
    print("\n1. 脂肪含量统计：")
    print(f"样本数量: {int(fat_stats['count'])}个")
    print(f"平均值: {fat_stats['mean']:.3f} g/100kJ")
    print(f"标准差: {fat_stats['std']:.3f} g/100kJ")
    print(f"最小值: {fat_stats['min']:.3f} g/100kJ")
    print(f"最大值: {fat_stats['max']:.3f} g/100kJ")

    print("\n2. 蛋白质含量统计：")
    print(f"样本数量: {int(protein_stats['count'])}个")
    print(f"平均值: {protein_stats['mean']:.3f} g/100kJ")
    print(f"标准差: {protein_stats['std']:.3f} g/100kJ")
    print(f"最小值: {protein_stats['min']:.3f} g/100kJ")
    print(f"最大值: {protein_stats['max']:.3f} g/100kJ")

    # 计算相关系数
    correlation = df['脂肪(g)'].corr(df['蛋白质(g)'])
    print(f"\n3. 脂肪和蛋白质含量的相关系数: {correlation:.3f}")

    # 分析分布特征
    print("\n4. 分布特征分析：")
    print(f"脂肪含量偏度: {df['脂肪(g)'].skew():.3f}")
    print(f"蛋白质含量偏度: {df['蛋白质(g)'].skew():.3f}")
    print(f"脂肪含量峰度: {df['脂肪(g)'].kurtosis():.3f}")
    print(f"蛋白质含量峰度: {df['蛋白质(g)'].kurtosis():.3f}")


def main():
    try:
        analyze_fat_protein_distribution()
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    main()