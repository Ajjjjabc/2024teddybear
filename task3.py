import pandas as pd


class MedicalFoodRecommender:
    def __init__(self):
        """
        初始化推荐系统，设置所有评分规则
        """
        # 加载数据
        self.product_data = pd.read_excel('result/result2.xlsx')
        self.nutrition_data = pd.read_excel('result/result1.xlsx')

        # 一、必要条件
        self.age_groups = {
            '婴儿': ['0～12月龄', '0-12月龄', '婴儿'],
            '1～10岁': ['1～10岁', '1-10岁', '1\~10岁'],
            '大于10岁': ['10岁以上'],
            '18岁以上': ['18岁以上'],
            '50岁以上': ['50岁以上']
        }

        # 营养含量评分标准
        self.nutrition_content_scores = {
            '蛋白质': {
                'high': {'threshold': 2.5, 'score': 3},
                'medium': {'threshold': 1.2, 'score': 2},
                'low': {'threshold': 0.6, 'score': 1}
            }
        }

        # 二、主要加分项
        self.nutrition_scores = {
            '补充蛋白质': 5,
            '补充碳水化合物': 5,
            '补充水及电解质': 5,
            '补充中链脂肪': 5,
            '补充营养': 3
        }

        self.condition_scores = {
            '进食受限': 4,
            '消化吸收障碍': 4,
            '代谢紊乱': 4,
            '吞咽障碍': 4,
            '营养不良': 4
        }

        self.special_condition_scores = {
            '高风险': 3,
            '术前需求': 3,
            '误吸风险': 3
        }

        self.severity_scores = {
            '重度': 3,
            '中度': 2,
            '轻度': 1
        }

        # 三、次要加分项
        self.secondary_condition_scores = {
            '脱水状态': 2,
            '消化系统问题': 2,
            '电解质需求': 2,
            '特定疾病': 2
        }

        # 四、减分项
        self.major_penalty_scores = {
            '核心需求冲突': -5,
            '不适用成分': -5,
            '特殊禁忌': -5
        }

        self.minor_penalty_scores = {
            '不相关适用症': -3,
            '不相关补充需求': -3,
            '场景不匹配': -3
        }

    def analyze_requirements(self, description):
        """
        分析用户输入的需求描述，转换为系统可处理的格式
        """
        requirements = {}

        # 分析年龄
        if '婴儿' in description:
            requirements['age'] = '婴儿'
        elif '10岁' in description:
            requirements['age'] = '1～10岁'  # 10岁属于1~10岁区间
        elif '18岁以上' in description:
            requirements['age'] = '18岁以上'
        elif '50岁以上' in description:
            requirements['age'] = '50岁以上'

        # 分析症状和需求
        if '蛋白质过敏' in description or '乳蛋白过敏' in description or '食物蛋白过敏' in description:
            requirements['蛋白质过敏'] = True

        if '乳糖不耐受' in description:
            requirements['乳糖不耐受'] = True

        if '补充蛋白质' in description or '需要蛋白质' in description:
            requirements['补充蛋白质'] = True

        if '补充碳水化合物' in description:
            requirements['补充碳水化合物'] = True

        if '补充营养' in description:
            requirements['补充营养'] = True

        return requirements

    def calculate_detailed_score(self, product, requirements):
        """
        计算详细评分
        """
        score_details = {
            '一、必要条件': [],
            '二、基础评分': [],
            '三、主要加分项': [],
            '四、次要加分项': [],
            '五、减分项': [],
            '六、特殊加分': [],
            '七、最终评分': [],
            '八、特殊说明': []
        }

        # 检查必要条件
        essential_check, essential_details = self.check_essential_conditions(product, requirements)
        score_details['一、必要条件'] = essential_details
        if not essential_check:
            return 0, score_details

        total_score = 10  # 基础分
        score_details['二、基础评分'].append(f"满足必要条件基础分：10分")

        description = product['适用人群']

        # 三、主要加分项
        # 1. 营养需求匹配
        for need, score in self.nutrition_scores.items():
            if need in description:
                total_score += score
                score_details['三、主要加分项'].append(f"营养需求匹配 - {need}: +{score}分")

        # 2. 疾病/症状匹配
        for condition, score in self.condition_scores.items():
            if condition in description:
                total_score += score
                score_details['三、主要加分项'].append(f"症状匹配 - {condition}: +{score}分")

        # 3. 特殊状况匹配
        for condition, score in self.special_condition_scores.items():
            if condition in description:
                total_score += score
                score_details['三、主要加分项'].append(f"特殊状况匹配 - {condition}: +{score}分")

        # 4. 营养成分评分
        nutrition_score, nutrition_details = self.calculate_nutrition_score(product, requirements)
        total_score += nutrition_score
        score_details['三、主要加分项'].extend(nutrition_details)

        # 四、次要加分项
        for condition, score in self.secondary_condition_scores.items():
            if condition in description:
                total_score += score
                score_details['四、次要加分项'].append(f"次要症状匹配 - {condition}: +{score}分")

        # 五、减分项
        for penalty, score in self.major_penalty_scores.items():
            if self.check_penalty_condition(product, penalty, requirements):
                total_score += score  # score已经是负数
                score_details['五、减分项'].append(f"主要减分 - {penalty}: {score}分")

        for penalty, score in self.minor_penalty_scores.items():
            if self.check_penalty_condition(product, penalty, requirements):
                total_score += score  # score已经是负数
                score_details['五、减分项'].append(f"次要减分 - {penalty}: {score}分")

        # 六、特殊加分
        special_score, special_details = self.calculate_special_bonus(product, requirements)
        total_score += special_score
        score_details['六、特殊加分'] = special_details

        # 七、最终评分
        score_details['七、最终评分'].append(f"总分：{total_score}")
        if total_score >= 25:
            score_details['七、最终评分'].append("评级：非常推荐")
        elif total_score >= 20:
            score_details['七、最终评分'].append("评级：强烈推荐")
        elif total_score >= 15:
            score_details['七、最终评分'].append("评级：推荐")
        elif total_score >= 10:
            score_details['七、最终评分'].append("评级：可考虑")
        else:
            score_details['七、最终评分'].append("评级：不推荐")

        return total_score, score_details

    def check_essential_conditions(self, product, requirements):
        """
        检查必要条件
        """
        details = []
        description = product['适用人群']

        # 检查年龄匹配
        age_match = False
        target_age = requirements['age']
        age_patterns = self.age_groups[target_age]

        for pattern in age_patterns:
            if pattern in description:
                age_match = True
                details.append(f"年龄段匹配：{pattern}")
                break

        if not age_match:
            return False, ["年龄段不匹配"]

        # 检查必要症状条件
        # 蛋白质过敏检查
        if requirements.get('蛋白质过敏'):
            if not ('食物蛋白过敏' in description or '乳蛋白过敏' in description):
                return False, ["不适用于蛋白质过敏患者"]
            details.append("满足蛋白质过敏要求")

        # 乳糖不耐受检查
        if requirements.get('乳糖不耐受'):
            if '乳糖不耐受' not in description:
                return False, ["不适用于乳糖不耐受患者"]
            details.append("满足乳糖不耐受要求")

        return True, details

    def calculate_nutrition_score(self, product, requirements):
        """
        计算营养成分相关分数
        """
        details = []
        score = 0
        reg_number = product['注册证号']

        try:
            # 获取营养成分数据
            nutrition_info = self.nutrition_data[
                self.nutrition_data['注册证号'] == reg_number
                ].iloc[0]

            # 如果需求包含"补充蛋白质"
            if requirements.get('补充蛋白质'):
                protein_content = nutrition_info['蛋白质(g)']
                if protein_content > 2.5:  # 高于平均值一个标准差
                    score += 3
                    details.append(f"蛋白质含量高（{protein_content:.2f} g/100kJ）: +3分")
                elif protein_content > 1.2:  # 接近平均值
                    score += 2
                    details.append(f"蛋白质含量中等（{protein_content:.2f} g/100kJ）: +2分")
                elif protein_content > 0.6:  # 低于平均值
                    score += 1
                    details.append(f"蛋白质含量一般（{protein_content:.2f} g/100kJ）: +1分")
                else:
                    details.append(f"蛋白质含量较低（{protein_content:.2f} g/100kJ）: +0分")

            # 可以添加其他营养成分的评分...

        except Exception as e:
            details.append(f"营养成分数据获取失败: {str(e)}")

        return score, details

    def check_penalty_condition(self, product, penalty, requirements):
        """
        检查减分条件
        """
        description = product['适用人群']

        # 主要减分情况检查
        if penalty == '核心需求冲突':
            # 例如：需要补充蛋白质，但产品主要用于补充碳水化合物
            if requirements.get('补充蛋白质') and '补充碳水化合物' in description and '补充蛋白质' not in description:
                return True
            # 需要补充碳水化合物，但产品主要用于补充蛋白质
            if requirements.get(
                    '补充碳水化合物') and '补充蛋白质' in description and '补充碳水化合物' not in description:
                return True

        elif penalty == '不适用成分':
            # 检查过敏原
            if requirements.get('蛋白质过敏') and '蛋白质' in description and '蛋白质过敏' not in description:
                return True
            if requirements.get('乳糖不耐受') and '乳糖' in description and '乳糖不耐受' not in description:
                return True

        elif penalty == '特殊禁忌':
            # 检查特殊禁忌症
            forbidden_keywords = ['禁用', '禁忌', '不适用']
            return any(keyword in description for keyword in forbidden_keywords)

        return False

    def calculate_special_bonus(self, product, requirements):
        """
        计算特殊加分
        """
        score = 0
        details = []
        description = product['适用人群']

        # 1. 针对性加分
        if '专门针对' in description or '特异性' in description:
            score += 3
            details.append("专门针对目标人群设计: +3分")

        if '特殊配方' in description or '优化配方' in description:
            score += 2
            details.append("特殊配方优化: +2分")

        if '易于吸收' in description or '利用度高' in description:
            score += 2
            details.append("易于吸收利用: +2分")

        # 2. 安全性加分
        if '安全性高' in description:
            score += 2
            details.append("安全性好: +2分")

        # 3. 适用性加分
        if '使用方便' in description:
            score += 2
            details.append("使用方便: +2分")

        return score, details

    def format_recommendation_result(self, result):
        """
        格式化推荐结果
        """
        product = result['product']
        score = result['score']
        details = result['details']

        output = [
            "\n" + "=" * 50,
            f"\n产品信息：",
            f"产品名称：{product['产品名称']}",
            f"企业名称：{product['企业名称']}",
            f"注册证号：{product['注册证号']}",
            f"适用人群：{product['适用人群']}",
            "\n详细评分："
        ]

        # 添加各部分评分详情
        for section, section_details in details.items():
            if section_details:  # 如果该部分有内容
                output.append(f"\n{section}:")
                for detail in section_details:
                    output.append(f"  {detail}")

        return "\n".join(output)

    def recommend(self, requirements):
        """
        根据需求推荐产品
        """
        print(f"\n开始为以下需求进行推荐：")
        for key, value in requirements.items():
            print(f"{key}: {value}")
        print("\n" + "=" * 50)

        results = []
        for idx, product in self.product_data.iterrows():
            score, details = self.calculate_detailed_score(product, requirements)
            if score > 0:
                results.append({
                    'product': product,
                    'score': score,
                    'details': details
                })

        # 按得分排序
        results.sort(key=lambda x: x['score'], reverse=True)

        # 输出推荐结果
        if results:
            print(f"\n找到 {len(results)} 个推荐产品：")
            for result in results:
                print(self.format_recommendation_result(result))
        else:
            print("\n未找到合适的推荐产品。")

        return results

def main():
    recommender = MedicalFoodRecommender()

    # 客户1：婴儿、蛋白质过敏
    print("\n处理客户1需求...")
    print("客户描述：婴儿、蛋白质过敏")
    description1 = "婴儿、蛋白质过敏"
    requirements1 = recommender.analyze_requirements(description1)
    print(f"提取到的需求：{requirements1}")
    results1 = recommender.recommend(requirements1)

    print("\n" + "=" * 50)

    # 客户2：10岁儿童、需要补充蛋白质、乳糖不耐受
    print("\n处理客户2需求...")
    print("客户描述：10岁儿童、需要补充蛋白质、乳糖不耐受")
    description2 = "10岁儿童、需要补充蛋白质、乳糖不耐受"
    requirements2 = recommender.analyze_requirements(description2)
    print(f"提取到的需求：{requirements2}")
    results2 = recommender.recommend(requirements2)

if __name__ == "__main__":
    main()
