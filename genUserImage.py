import random
from datetime import datetime

# 配置参数
NUM_USERS = 1000
OUTPUT_FILE = "user_images.txt"

# 数据分布配置
PREFERENCES = {
    "科技": {"weight": 0.18, "word_range": (8000, 30000)},
    "文学": {"weight": 0.15, "word_range": (5000, 20000)},
    "历史": {"weight": 0.12, "word_range": (10000, 50000)},
    "艺术": {"weight": 0.10, "word_range": (5000, 25000)},
    "体育": {"weight": 0.13, "word_range": (3000, 15000)},
    "娱乐": {"weight": 0.20, "word_range": (1000, 10000)},
    "财经": {"weight": 0.07, "word_range": (8000, 35000)},
    "教育": {"weight": 0.03, "word_range": (5000, 20000)},
    "健康": {"weight": 0.02, "word_range": (3000, 15000)}
}

GENDERS = ["Male", "Female"]

def generate_age():
    """生成符合人口年龄分布的数值（18-65岁）"""
    age = int(random.triangular(18, 65, 32))
    return min(max(age, 18), 65)

def generate_preferred_words(preference):
    """根据偏好生成对应的字数偏好"""
    min_words, max_words = PREFERENCES[preference]["word_range"]
    return random.randint(min_words, max_words)

def generate_active_time():
    """生成符合人类作息的时间段（包含周末效应）"""
    is_weekend = random.random() < 0.3  # 30%概率是周末
    
    if is_weekend:
        hour = random.choices(
            population=[9, 10, 11, 15, 16, 20, 21, 22],
            weights=[2, 3, 3, 4, 4, 5, 5, 4],
            k=1
        )[0]
    else:
        hour = random.choices(
            population=[7, 8, 12, 13, 18, 19, 20],
            weights=[5, 6, 4, 3, 7, 6, 5],
            k=1
        )[0]
    
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def generate_users(num_users):
    """生成用户画像数据集"""
    # 处理偏好权重
    pref_items = list(PREFERENCES.keys())
    pref_weights = [PREFERENCES[pref]["weight"] for pref in pref_items]
    
    for user_id in range(1, num_users + 1):
        preference = random.choices(pref_items, pref_weights)[0]
        yield {
            "user_id": user_id,
            "preference": preference,
            "gender": random.choice(GENDERS),
            "age": generate_age(),
            "喜好阅读字数": generate_preferred_words(preference),
            "Active time": generate_active_time()
        }

def save_to_txt(users, filename):
    """保存数据到文本文件"""
    with open(filename, "w", encoding="utf-8") as f:
        # 写入列头
        f.write("user_id,preference,gender,age,喜好阅读字数,Active time\n")
        
        # 写入数据行
        for user in users:
            line = (
                f"{user['user_id']},"
                f"{user['preference']},"
                f"{user['gender']},"
                f"{user['age']},"
                f"{user['喜好阅读字数']},"
                f"{user['Active time']}\n"
            )
            f.write(line)

if __name__ == "__main__":
    # 生成用户数据
    users = generate_users(NUM_USERS)
    
    # 保存到文件
    save_to_txt(users, OUTPUT_FILE)
    print(f"成功生成 {NUM_USERS} 条用户画像数据到 {OUTPUT_FILE}")