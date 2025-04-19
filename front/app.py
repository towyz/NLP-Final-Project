from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# 模拟热搜数据
def generate_trending_topics():
    base_topics = [
        "Python Flask教程",
        "2023年最新科技趋势",
        "如何学习人工智能",
        "健康饮食指南",
        "最新电影推荐",
        "旅游景点排行",
        "股票市场分析",
        "编程语言排行榜",
        "健身锻炼方法",
        "环保生活小贴士",
        "Python Django教程",
        "2025年最新科技趋势",
        "如何学习大数据",
        "减肥饮食计划",
        "近期热门电影盘点",
        "国内小众旅游景点推荐",
        "基金投资策略",
        "前端编程语言盘点",
        "瑜伽锻炼技巧",
        "低碳生活小窍门",
        "Java开发实战技巧",
        "人工智能在医疗领域的应用",
        "如何学习区块链技术",
        "营养早餐搭配方案",
        "经典老电影重温推荐",
        "全球最美海滩排行",
        "期货市场解读",
        "编程语言性能对比",
        "力量训练方法分享",
        "旧物改造环保妙招",
        "Go语言入门教程",
        "量子计算发展现状",
        "怎样学习机器学习",
        "孕期饮食注意事项",
        "即将上映的电影预告",
        "城市周边游好去处",
        "黄金市场走势分析",
        "脚本语言使用技巧",
        "普拉提健身方法",
        "环保购物袋使用指南",
        "Ruby语言基础教程",
        "新能源科技新突破",
        "如何学习云计算",
        "高血压饮食调理",
        "口碑好的文艺片推荐",
        "古镇旅游景点排名",
        "债券投资入门",
        "汇编语言基础介绍",
        "跑步健身注意事项",
        "家庭环保清洁用品自制",
        "PHP开发常用框架",
        "太空探索最新成果",
        "学习数据分析的方法",
        "素食营养搭配指南",
        "高票房喜剧电影推荐",
        "山区旅游景点精选",
        "股票短线操作技巧",
        "移动开发编程语言盘点",
        "健身操减肥攻略",
        "环保型家居装修建议"
    ]
    
    # 每天的热搜稍有不同
    random.seed(datetime.now().strftime("%Y%m%d%H%M%S"))
    trending = random.sample(base_topics, 5)
    
    # 添加一些热度标记
    return [f"{topic} ({random.randint(1, 5)}00万)" for topic in trending]

# 模拟搜索功能
def mock_search(query):
    # 这里应该是实际的搜索逻辑
    # 为了演示，我们返回一些模拟结果
    results = []
    
    for i in range(1, 6):
        results.append({
            "title": f"{query} 相关结果 {i}",
            "url": f"https://example.com/{query.replace(' ', '-')}-{i}",
            "snippet": f"这是关于 {query} 的第 {i} 个模拟结果。这里包含了一些关于 {query} 的详细信息..."
        })
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    results = mock_search(query)
    return jsonify(results)

@app.route('/api/trending')
def trending():
    topics = generate_trending_topics()
    return jsonify(topics)

if __name__ == '__main__':
    app.run(debug=True)