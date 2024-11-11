import pandas as pd
import jieba
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


def create_word_cloud():
    """
    创建并保存词云图，分析适用人群特征
    """
    # 读取数据
    print("读取result2.xlsx...")
    df = pd.read_excel('result/result2.xlsx')

    # 添加自定义词组
    custom_words = [
        # 年龄段
        "0～12月龄",
        "1岁以上",
        "10岁以上",
        "18岁以上",
        "1～10岁",
        "50岁以上",
        "10～14岁",

        # 疾病和状况
        "早产/低出生体重",
        "低出生体重",
        "消化吸收障碍",
        "代谢紊乱",
        "进食受限",
        "苯丙酮尿症",
        "乳糖不耐受",
        "乳蛋白过敏",
        "食物蛋白过敏",
        "吞咽障碍",
        "轻至中度脱水",

        # 补充需求
        "补充营养",
        "补充蛋白质",
        "补充碳水化合物",
        "补充水及电解质",
        "补充中链脂肪",
        "限制脂肪摄入",

        # 特殊状况
        "特定疾病",
        "医学状况",
        "误吸风险"
    ]

    # 将自定义词组添加到jieba词典
    for word in custom_words:
        jieba.add_word(word)

    # 定义停用词
    stop_words = {
         '适用', '人群', '的', '和', '与', '及', '或',
        '如', '等', '有', '在', '需要', '。', '，',
        '、', '；', '）', '（', '为', '时', '中',
        '对', '由', '所', '个', '例', '因', '于',
        '下', '月', '人', '群', '需', '要', '岁',
        '以上', '或者', '状况', '月龄', '～', '/',
        '-', '\\', '~', '导致', '造成', '状态',
        '0', '1', '10', '12', '14', '18', '50',
        '原因', '补充', '术前', '进行', '低', '出生',
        '体重', '术', '前', '上', '致', '者', '于',
        '性', '量', '以', '并', '可', '种','水', '存在'
    }

    # 合并所有适用人群文本
    text = ' '.join(df['适用人群'].dropna().astype(str))

    # 使用jieba分词
    words = jieba.cut(text)

    # 过滤停用词并合并
    words_filtered = [word for word in words if word not in stop_words]

    # 统计词频并保存
    word_freq = pd.Series(words_filtered).value_counts()

    # 保存词频到文件
    with open('result/word_frequencies.txt', 'w', encoding='utf-8') as f:
        f.write("词语\t频次\t频率\n")
        total_words = len(words_filtered)
        for word, count in word_freq.items():
            frequency = count / total_words
            f.write(f"{word}\t{count}\t{frequency:.4f}\n")

    # 将词频系列转换为词频字典，用于生成词云
    words_filtered = ' '.join(words_filtered)

    # 设置字体路径（使用Windows系统自带的微软雅黑字体）
    font_path = r'C:\Windows\Fonts\msyh.ttc'

    # 创建词云对象
    wc = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        max_words=100,
        max_font_size=200,
        min_font_size=10,
        random_state=42,
        font_path=r'C:\Windows\Fonts\msyh.ttc',
        collocations=False,  # 设置为False防止词语重复
        prefer_horizontal=0.7  # 70%的词横向显示
    )

    # 生成词云
    wc.generate(words_filtered)

    # 创建图形
    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴

    # 保存词云图
    plt.savefig('result/wordcloud.png', dpi=300, bbox_inches='tight')
    print("词云图已保存到result/wordcloud.png")

    # 输出词频统计和分析
    print("\n词频统计（top 20）：")
    print(word_freq.head(20))

    # 计算适用人群文本的基本统计
    text_lengths = df['适用人群'].str.len()

    print("\n适用人群文本统计：")
    print(f"最短描述长度: {text_lengths.min()} 字符")
    print(f"最长描述长度: {text_lengths.max()} 字符")
    print(f"平均描述长度: {text_lengths.mean():.1f} 字符")

    # 分析空值情况
    null_count = df['适用人群'].isna().sum()
    print(f"\n缺失值数量: {null_count}")

    # 输出一些典型的适用人群描述示例
    print("\n典型适用人群描述示例：")
    examples = df['适用人群'].dropna().sample(min(5, len(df)))
    for i, example in enumerate(examples, 1):
        print(f"\n示例{i}：{example}")


def main():
    try:
        create_word_cloud()
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()  # 打印详细错误信息


if __name__ == "__main__":
    main()