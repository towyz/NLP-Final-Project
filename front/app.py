from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random
import json

app = Flask(__name__)


# 模拟热搜数据
def generate_trending_topics():
    base_topics = [
        (
            "Japan Just Gave Ukraine $3 Billion from Russian assets",
            "https://reddit.com/r/worldnews/comments/1k2olxh/japan_just_gave_ukraine_3_billion_from_russian/",
        ),
        (
            "THE DALLAS MAVERICKS HAVE BEEN ELIMINATED FROM THE 2025 NBA CHAMPIONSHIP CONTENTION",
            "https://reddit.com/r/nba/comments/1k2nr7a/the_dallas_mavericks_have_been_eliminated_from/",
        ),
        (
            "Wholesome ex-couple",
            "https://reddit.com/r/MadeMeSmile/comments/1k2m06j/wholesome_excouple/",
        ),
        (
            "So….I found this in my garage this morning. Ummm",
            "https://reddit.com/r/cats/comments/1k2l5mh/soi_found_this_in_my_garage_this_morning_ummm/",
        ),
        (
            "NASAs first six women astronauts. February 1979",
            "https://reddit.com/r/OldSchoolCool/comments/1k2lkbj/nasas_first_six_women_astronauts_february_1979/",
        ),
        (
            "Shine on.",
            "https://reddit.com/r/BlackPeopleTwitter/comments/1k2ln0e/shine_on/",
        ),
        (
            "Boston’s Old North Church on the 250th anniversary of Paul Revere’s midnight ride",
            "https://reddit.com/r/pics/comments/1k2ldt3/bostons_old_north_church_on_the_250th_anniversary/",
        ),
        (
            "Trump brags gas is down to $1.98 a gallon in a ‘couple of states.’ It isn’t — anywhere",
            "https://reddit.com/r/politics/comments/1k2lf5y/trump_brags_gas_is_down_to_198_a_gallon_in_a/",
        ),
        (
            "On the Old North Church last night in Boston.",
            "https://reddit.com/r/interestingasfuck/comments/1k2kmg6/on_the_old_north_church_last_night_in_boston/",
        ),
        (
            "Kneecap open Coachella Gig with strong Messaging",
            "https://reddit.com/r/Fauxmoi/comments/1k2kvqk/kneecap_open_coachella_gig_with_strong_messaging/",
        ),
    ]
    # 每天的热搜稍有不同
    random.seed(datetime.now().strftime("%Y%m%d%H%M%S"))
    trending = random.sample(base_topics, 5)

    # 添加一些热度标记
    # return [f"{topic} ({random.randint(1, 5)}00万)" for topic in trending]
    # 随机 返回5条话题和链接
    return [
        {
            "topic": topic[0],
            "url": topic[1],
            "hotness": f"{random.randint(1, 5)}00万",
        }
        for topic in trending
    ]


# 模拟推荐数据
def generate_recommandation_topics():
    base_topics = [
        (
            """New Rule: Do Not ask for Medical Advice""",
            """https://reddit.com/r/Basketball/comments/1jo7aau/new_rule_do_not_ask_for_medical_advice/""",
        ),
        (
            """Official Shoes, Gear, Equipment, etc... Megathread""",
            """https://reddit.com/r/Basketball/comments/1k1izx2/official_shoes_gear_equipment_etc_megathread/""",
        ),
        (
            """why just wnba balls smaller and not anything else?""",
            """https://reddit.com/r/Basketball/comments/1k2fidh/why_just_wnba_balls_smaller_and_not_anything_else/""",
        ),
        (
            """Adam Silver Says Mavs Aren't Leaving Dallas, No 'Ulterior Motives' for Luka Trade""",
            """https://reddit.com/r/Basketball/comments/1k2b0ti/adam_silver_says_mavs_arent_leaving_dallas_no/""",
        ),
        (
            """Lost my College Intramural Championship for calling a timeout when we didn't have one :(""",
            """https://reddit.com/r/Basketball/comments/1k2qvcv/lost_my_college_intramural_championship_for/""",
        ),
        (
            """how should i start watching matches??(idk)""",
            """https://reddit.com/r/Basketball/comments/1k2ofyn/how_should_i_start_watching_matchesidk/""",
        ),
        (
            """Is it a double dribble if I receive the ball while moving then taking 2 steps then start dribbling?""",
            """https://reddit.com/r/Basketball/comments/1k2iur6/is_it_a_double_dribble_if_i_receive_the_ball/""",
        ),
        (
            """how to start playing basketball as absolute beginner as a girl?""",
            """https://reddit.com/r/Basketball/comments/1k2hyjd/how_to_start_playing_basketball_as_absolute/""",
        ),
        (
            """Is it a foul if you run into someone to shoot and push them over without extending?""",
            """https://reddit.com/r/Basketball/comments/1k2iogx/is_it_a_foul_if_you_run_into_someone_to_shoot_and/""",
        ),
        (
            """Suns 2025-2026 championship squad""",
            """https://reddit.com/r/Basketball/comments/1k2ovv0/suns_20252026_championship_squad/""",
        ),
        (
            """Here's the swearing in of DJT! """,
            """https://reddit.com/r/trump/comments/1i5vjor/heres_the_swearing_in_of_djt/""",
        ),
        (
            """Donald J Trump is now the 47th President! """,
            """https://reddit.com/r/trump/comments/1i5v404/donald_j_trump_is_now_the_47th_president/""",
        ),
        (
            """You'd think they'd be happy. An el salvador citizen is finally home.""",
            """https://reddit.com/r/trump/comments/1k2gw8t/youd_think_theyd_be_happy_an_el_salvador_citizen/""",
        ),
        (
            """Yes Sir! 🇺🇸🇺🇸🇺🇸""",
            """https://reddit.com/r/trump/comments/1k2n82s/yes_sir/""",
        ),
        ("""Agreed! 👊🇺🇸""", """https://reddit.com/r/trump/comments/1k2om2r/agreed/"""),
        (
            """Brutal lol. Yes it's real.""",
            """https://reddit.com/r/trump/comments/1k29jsl/brutal_lol_yes_its_real/""",
        ),
        (
            """Where’s the media backlash about this gesture Bernie Sanders recently made? 🤔""",
            """https://reddit.com/r/trump/comments/1k26izg/wheres_the_media_backlash_about_this_gesture/""",
        ),
        (
            """I’m Sure You are Back From El Salvador……""",
            """https://reddit.com/r/trump/comments/1k2egcs/im_sure_you_are_back_from_el_salvador/""",
        ),
        (
            """Trump with the prime minister of Italy.""",
            """https://reddit.com/r/trump/comments/1k23m5m/trump_with_the_prime_minister_of_italy/""",
        ),
        (
            """Troller-in-Chief""",
            """https://reddit.com/r/trump/comments/1k2i6fi/trollerinchief/""",
        ),
    ]
    random.seed(datetime.now().strftime("%Y%m%d%H%M%S"))
    recommendations = random.sample(base_topics, 10)

    # 随机 返回10条话题和链接
    return [
        {
            "topic": topic[0],
            "url": topic[1],
            "hotness": f"{random.randint(1, 5)}00万",
        }
        for topic in recommendations
    ]


# 模拟搜索功能
def mock_search(query):
    # 这里应该是实际的搜索逻辑
    # 为了演示，我们返回一些模拟结果
    results = []

    for i in range(1, 6):
        results.append(
            {
                "title": f"{query} 相关结果 {i}",
                "url": f"https://example.com/{query.replace(' ', '-')}-{i}",
                "snippet": f"这是关于 {query} 的第 {i} 个模拟结果。这里包含了一些关于 {query} 的详细信息...",
            }
        )

    return results


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "")
    results = mock_search(query)
    return jsonify(results)


@app.route("/api/trending")
def trending():
    topics = generate_trending_topics()
    return jsonify(topics)


@app.route("/api/get_recommendations")
def recommendations():
    topics = generate_recommandation_topics()
    return jsonify(topics)


if __name__ == "__main__":
    app.run(debug=True)
