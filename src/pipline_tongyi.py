# -*- coding: utf-8 -*-
import os
import re
import praw
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from full_pipeline_demo import (
    get_content,
    get_posts_by_keywords,
    get_hot_posts,
    extract_post_id,
    reddit
)


os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

CLIENT = OpenAI(
    api_key="sk-9167273d6cbf47f69a2e847133779bba",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# reddit = praw.Reddit(
#                 client_id="oJd0bJxDJiyBpsGOi7u0rg",
#                 client_secret="sPJ3VJqMavUNUfXbB7b0ipU34Z-H1g",
#                 user_agent="testscript by u/fakebot3",
#             )

USER_IMAGE_PATH = "./user_images.txt"  # 用户画像文件路径

# 对话的基本流程
def chat_demo():
    completion = CLIENT.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"},
        ],
    )

    print(completion.choices[0].message.content)


# 调用的 langchain
def get_keywords_set(keyword):
    prompt_format = f"""我需要你根据用户输入的喜好领域，生成尽可能多相关的细分关键词。请遵循以下规则：

            1. 输出格式：纯文本，逗号分隔，不编号
            2. 关键词类型需包含：
            - 核心术语
            - 相关子领域
            - 工具/设备
            - 技术/方法
            - 流派/风格
            - 知名品牌
            - 代表人物
            - 关联概念
            3. 数量要求：至少30个，最多40个不重复关键词

            参考案例：
            输入：旅游
            输出：[自由行, 背包客, 自驾游, 民宿体验, 景点打卡, 旅行摄影, 当地美食, 徒步路线, 文化遗产, 免税购物, 签证攻略, 旅行保险, 航拍设备, 旅行博主, 穷游指南, 邮轮度假, 户外装备, 语言翻译APP, 时差调整, 旅行纪念品, 地理定位, 生态旅游, 沙发客, 旅行vlog, 旅行穿搭, 货币兑换, 旅行插头转换器, 孤独星球指南, 旅行急救包, 数字游民]

            输入：咖啡
            输出：[手冲咖啡, 拉花艺术, 咖啡烘焙度, 单品豆, 意式浓缩, 冷萃技术, 咖啡因含量, 咖啡渣利用, 摩卡壶, 法压壶, 咖啡师认证, 咖啡豆产区, 第三波咖啡浪潮, 咖啡杯测, 咖啡因过敏, 咖啡馆设计, 挂耳咖啡, 咖啡调糖, 咖啡伴侣, 咖啡机维护, 咖啡品鉴术语, 咖啡因代谢, 咖啡主题旅行, 咖啡烘焙机, 咖啡师大赛, 咖啡冥想, 咖啡因耐受, 咖啡渣去角质, 咖啡风味轮, 咖啡豆保存罐]

            现在请处理新输入：
            输入：{keyword}
            输出：[]
            """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI assistant, please answer user's question."),
            ("user", prompt_format),
        ]
    )

    chat = ChatTongyi(
        model="qwen-plus",
        top_p=0.8,
        temperature=1,
        api_key="sk-9167273d6cbf47f69a2e847133779bba",
    )

    response = chat(prompt)
    response = (
        response.content.replace("[]", "")
        .replace("，", ",")
        .replace(" ", "")
        .replace("\n", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
    )
    print(response)


# 另外一个不调用 langchain 的版本
def get_keywords_set_without_langchain(keyword):
    prompt_format = f"""我需要你根据用户输入的喜好领域，生成尽可能多相关的细分关键词。请遵循以下规则：

            1. 输出格式：纯文本，逗号分隔，不编号
            2. 关键词类型需包含：
            - 核心术语
            - 相关子领域
            - 工具/设备
            - 技术/方法
            - 流派/风格
            - 知名品牌
            - 代表人物
            - 关联概念
            3. 数量要求：至少30个，最多40个不重复关键词

            参考案例：
            输入：旅游
            输出：[自由行, 背包客, 自驾游, 民宿体验, 景点打卡, 旅行摄影, 当地美食, 徒步路线, 文化遗产, 免税购物, 签证攻略, 旅行保险, 航拍设备, 旅行博主, 穷游指南, 邮轮度假, 户外装备, 语言翻译APP, 时差调整, 旅行纪念品, 地理定位, 生态旅游, 沙发客, 旅行vlog, 旅行穿搭, 货币兑换, 旅行插头转换器, 孤独星球指南, 旅行急救包, 数字游民]

            输入：咖啡
            输出：[手冲咖啡, 拉花艺术, 咖啡烘焙度, 单品豆, 意式浓缩, 冷萃技术, 咖啡因含量, 咖啡渣利用, 摩卡壶, 法压壶, 咖啡师认证, 咖啡豆产区, 第三波咖啡浪潮, 咖啡杯测, 咖啡因过敏, 咖啡馆设计, 挂耳咖啡, 咖啡调糖, 咖啡伴侣, 咖啡机维护, 咖啡品鉴术语, 咖啡因代谢, 咖啡主题旅行, 咖啡烘焙机, 咖啡师大赛, 咖啡冥想, 咖啡因耐受, 咖啡渣去角质, 咖啡风味轮, 咖啡豆保存罐]

            现在请处理新输入：
            输入：{keyword}
            输出：[]
            """
    completion = CLIENT.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant, please answer user's question.",
            },
            {"role": "user", "content": prompt_format.format(keyword=keyword)},
        ],
    )

    # print(completion.choices[0].message.content)
    response = completion.choices[0].message.content
    response = (
        response.replace("[]", "")
        .replace("，", ",")
        .replace(" ", "")
        .replace("\n", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
    )

    response = re.findall(r"[^,]+", response)
    return response


def translate(keywordsList):
    """
    将关键词列表翻译为中文或英文\n
    :param keywordsList: 关键词列表
    :return: 翻译后的关键词列表
    """
    # 使用 deepseek_chat 进行翻译
    wordStr = "[" + ", ".join(keywordsList) + "]"
    prompt = f"""我需要你根据参考格式将以下中文关键词翻译为英文，或将英文关键词翻译为中文: {wordStr}
        参考格式1（中译英）：
        输入：[自由行, 背包客, 自驾游, 民宿体验, 景点打卡, 旅行摄影, 当地美食, 徒步路线, 文化遗产, 免税购物, 签证攻略, 旅行保险, 航拍设备, 旅行博主, 穷游指南, 邮轮度假, 户外装备, 语言翻译APP, 时差调整, 旅行纪念品, 地理定位, 生态旅游, 沙发客, 旅行vlog, 旅行穿搭, 货币兑换, 旅行插头转换器, 孤独星球指南, 旅行急救包, 数字游民]
        输出：[Free travel, Backpacker, Self-driving tour, Homestay experience, Scenic spot check-in, Travel photography, Local food, Hiking route, Cultural heritage, Duty-free shopping, Visa guide, Travel insurance, Aerial photography equipment, Travel blogger, Budget travel guide, Cruise vacation, Outdoor equipment, Language translation APP, Jet lag adjustment, Travel souvenirs, Geolocation, Ecotourism, Couchsurfing, Travel vlog, Travel outfit, Currency exchange, Travel plug adapter, Lonely Planet guidebook, Travel first aid kit, Digital nomad]

        参考格式2（英译中）：
        输入：[Digital camera, SLR camera, micro single camera, lens selection, aperture control, shutter speed, ISO sensitivity, composition skills, Light use, portrait photography, landscape photography, documentary photography, street photography, night shooting, long exposure, HDR technology, panoramic shooting, drone aerial photography, tripod use, Filter Effects, Post Repainting, Lightroom tutorial, Photoshop tips, Black and White Photography, film camera, Darkroom techniques, Studio Lighting, Reflector Use, Photography Backpack, Memory Card Selection, Battery life, Photography competitions, Photography Exhibitions, photography Books, Photography magazines, Photographer Community, Photography Workshop, Photography Travel, Underwater photography, Macro photography, Time-lapse photography, photography copyright, Photo printing, Photo frame selection, Photography history, famous photographers, photography genres, Photography Ethics, photography equipment rental, Photography APP recommendation]
        输出：[数码相机, 单反相机, 微单相机, 镜头选择, 光圈控制, 快门速度, ISO感光度, 构图技巧, 光线运用, 人像摄影, 风景摄影, 纪实摄影, 街头摄影, 夜景拍摄, 长曝光, HDR技术, 全景拍摄, 无人机航拍, 三脚架使用, 滤镜效果, 后期修图, Lightroom教程, Photoshop技巧, 黑白摄影, 胶片相机, 暗房技术, 摄影棚灯光, 反光板运用, 摄影背包, 存储卡选择, 电池续航, 摄影比赛, 摄影展览, 摄影书籍, 摄影杂志, 摄影师社区, 摄影工作坊, 摄影旅行, 水下摄影, 微距摄影, 延时摄影, 摄影版权, 照片打印, 相框选择, 摄影历史, 著名摄影师, 摄影流派, 摄影伦理, 摄影器材租赁, 摄影APP推荐]

        注意：只需要输出[]中的内容，其他的内容都不需要。
    """
    # print(prompt)

    completion = CLIENT.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant, please answer user's question.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    response = completion.choices[0].message.content
    response = (
        response.replace("[]", "")
        .replace("，", ",")
        .replace("\n", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
    )

    if response:
        response = response.split(", ")
    else:
        response = []

    return response


def filter(user_image, content):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI assistant, please answer user's question."),
            (
                "user",
                f"""我需要你扮演用户画像分析师，评估给定的用户画像与主流媒体文案的匹配程度。请按照以下规则处理：

                            <评估规则>
                            1. 评分范围：0-10分（允许小数点），10分为完全契合
                            2. 核心维度：
                            - 关键词重叠度（显性需求匹配）
                            - 情感倾向一致性（积极/消极/中性）
                            - 价值观契合度（生活理念、消费观念）
                            - 场景关联性（使用场景匹配程度）
                            - 语言风格适配度（正式/口语化/技术流）
                            3. 输出格式：
                            - 最终评分：x
                            - 维度拆解：用符号▸列出各维度得分及依据（每项不超过15字）
                            </评估规则>

                            <示例集>
                            案例1：
                            [用户画像] 女性，28岁，健身爱好者，关注低卡饮食，喜欢居家锻炼，购物时注重成分表分析
                            [媒体文案] "Keep年度健身报告：83%用户选择清晨训练，蛋白粉销量增长200%，瑜伽垫材质升级带来更好防滑体验"
                            输出：
                            最终评分：9.2  
                            维度拆解：
                            ▸关键词 9.5（健身/低卡/居家）  
                            ▸情感 9.0（积极健康导向）  
                            ▸价值观 8.8（科学健身理念）  
                            ▸场景 9.2（居家锻炼场景）  
                            ▸语言 9.0（专业术语适配）  

                            案例2：
                            [用户画像] 男性，35岁，数码极客，热衷DIY装机，常逛专业论坛，年度消费电子支出超5万元
                            [媒体文案] "小红书爆款推荐：萌妹必备粉色键盘，十种呼吸灯模式让你的桌面瞬间可爱！"
                            输出：
                            最终评分：3.5  
                            维度拆解：
                            ▸关键词 2.0（缺失专业装机术语）  
                            ▸情感 4.5（萌系vs极客理性）  
                            ▸价值观 3.0（外观导向vs性能导向）  
                            ▸场景 5.0（桌面美化非核心需求）  
                            ▸语言 3.0（萌系用语不匹配） 
                            </示例集>

                            <当前任务>
                            请分析以下输入的匹配度：
                            [用户画像] {user_image}
                            [媒体文案] {content}
                            输出：
            """,
            ),
        ]
    )
    chat = ChatTongyi(
        model="qwen-plus",
        top_p=0.8,
        temperature=1,
        api_key="sk-9167273d6cbf47f69a2e847133779bba",
    )
    response = chat(prompt)
    print(response)

    print(response.content.split(" ")[0].split("：")[1])
    response = float(response.content.split(" ")[0].split("：")[1])
    return response


def filter_without_langchain(user_image, content):
    prompt = f"""我需要你扮演用户画像分析师，评估给定的用户画像与主流媒体文案的匹配程度。请按照以下规则处理：

                            <评估规则>
                            1. 评分范围：0-10分（允许小数点），10分为完全契合
                            2. 核心维度：
                            - 关键词重叠度（显性需求匹配）
                            - 情感倾向一致性（积极/消极/中性）
                            - 价值观契合度（生活理念、消费观念）
                            - 场景关联性（使用场景匹配程度）
                            - 语言风格适配度（正式/口语化/技术流）
                            3. 输出格式：
                            - 最终评分：x
                            - 维度拆解：用符号▸列出各维度得分及依据（每项不超过15字）
                            </评估规则>

                            <示例集>
                            案例1：
                            [用户画像] 女性，28岁，健身爱好者，关注低卡饮食，喜欢居家锻炼，购物时注重成分表分析
                            [媒体文案] "Keep年度健身报告：83%用户选择清晨训练，蛋白粉销量增长200%，瑜伽垫材质升级带来更好防滑体验"
                            输出：
                            最终评分：9.2  
                            维度拆解：
                            ▸关键词 9.5（健身/低卡/居家）  
                            ▸情感 9.0（积极健康导向）  
                            ▸价值观 8.8（科学健身理念）  
                            ▸场景 9.2（居家锻炼场景）  
                            ▸语言 9.0（专业术语适配）  

                            案例2：
                            [用户画像] 男性，35岁，数码极客，热衷DIY装机，常逛专业论坛，年度消费电子支出超5万元
                            [媒体文案] "小红书爆款推荐：萌妹必备粉色键盘，十种呼吸灯模式让你的桌面瞬间可爱！"
                            输出：
                            最终评分：3.5  
                            维度拆解：
                            ▸关键词 2.0（缺失专业装机术语）  
                            ▸情感 4.5（萌系vs极客理性）  
                            ▸价值观 3.0（外观导向vs性能导向）  
                            ▸场景 5.0（桌面美化非核心需求）  
                            ▸语言 3.0（萌系用语不匹配） 
                            </示例集>

                            <当前任务>
                            请分析以下输入的匹配度：
                            [用户画像] {user_image}
                            [媒体文案] {content}
                            输出：
            """
    completion = CLIENT.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant, please answer user's question.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    response = completion.choices[0].message.content
    response = float(response.split(' ')[0].split('：')[1])
    return response

if __name__ == "__main__":
    
    with open(USER_IMAGE_PATH, 'r', encoding='utf-8') as f:
            epoch = 0
            while True:
                line = f.readline()
                if not line:
                    break
                user_image = {}
                print(line)
                user_id, preference, female, age, readnum, active_time = line.strip().split(',')

                user_image[user_id] = user_id
                user_image[preference] = preference
                user_image[female] = female
                user_image[age] = age
                user_image[readnum] = readnum
                user_image[active_time] = active_time

                keywords = get_keywords_set_without_langchain(user_image[preference])
                print(keywords)
                keywords = translate(keywords) + keywords
                print(keywords)
                posts = get_posts_by_keywords(keywords)
                print(posts)

                num = 0
                sum_score = 0
                for post in posts:
                    print(f"标题: {post['标题']}")
                    content = get_content(extract_post_id(post['链接']))
                    print(content)
                    score = filter_without_langchain(line, content)
                    sum_score += score
                    num +=1

                if num == 0:
                    print(r"tongyi: 0")
                else:
                    print(r"tongyi: " + str(sum_score/num))
                epoch += 1
                if epoch >= 10:
                    break