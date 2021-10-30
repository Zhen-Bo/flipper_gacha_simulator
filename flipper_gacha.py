import os
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session,
    Response,
    jsonify,
    abort,
    send_from_directory,
)
from datetime import datetime, timezone, timedelta
import json
import random
import time
import flask_limiter
import redis
from flask_mysqldb import MySQL, MySQLdb
from gacha import gacha_pool
from datetime import date

load_dotenv()

# vue build file
# app = Flask(__name__, static_folder="./dist", template_folder="./templates")
app = Flask(__name__)

app.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE="application/json;charset=utf-8",
    SECRET_KEY=os.getenv("SECRET_KEY"),
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    STATIC_FOLDER=os.getenv("STATIC_FOLDER"),
    MYSQL_HOST=os.getenv("SEVER_IP"),
    MYSQL_USER=os.getenv("DB_USER"),
    MYSQL_PASSWORD=os.getenv("DB_PASS"),
    MYSQL_DB=os.getenv("DB_NAME"),
    MYSQL_CURSORCLASS="DictCursor",
    DATA_FOLDER=os.getenv("DATA_FOLDER"),
)
mysql = MySQL(app)

# 取得使用者IP
def limit_key_func():
    return str(request.headers.get("X-Forwarded-For", "127.0.0.1")).split(",")[0]


# 設定flask-limiter
limiter = flask_limiter.Limiter(
    app, key_func=limit_key_func, default_limits=["85 per minute"]
)

# 初始化卡池資料
flipper_gacha_pool = gacha_pool(os.path.join(app.config["DATA_FOLDER"], "flipper_pool"))

# 可以改成讀取json
pool_data_detal = {
    # "drawing_witch": {"name": "水炭池", "type": "normal"},#關閉水炭池
    # "Thunder-pu": {"name": "雷屬性精選", "type": "attribute"},#關閉雷PU
    # "machine_police_girl": {"name": "警察池", "type": "single"},
    # "halfanv": {"name": "半周年禮黑", "type": "three_pu"},
    # "light-pu": {"name": "光屬性精選", "type": "attribute"},
    # "fire-pu": {"name": "火屬性精選", "type": "attribute"},
    # "princess": {"name": "公主連結", "type": "three_pu"},
    "summer1": {"name": "泳裝1期", "type": "normal"},
    "summer2": {"name": "泳裝2期", "type": "normal"},
}

# 連接redis
redis_pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True)
redis_data = redis.Redis(connection_pool=redis_pool)


def get_character(name):
    try:
        return json.loads(redis_data.get("character_info"))[name]
    except:
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT dev_id AS id,name,rarity,attri FROM `character`;")
        rs = cursor.fetchall()
        cursor.close()
        character_info = {}
        for row in rs:
            character_info[row["id"]] = row
        redis_data.set("character_info", json.dumps(character_info))
        redis_data.expire("character_info", 86400)
        return character_info[name]


def set_redis_record(pool):
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT dev_id AS id,name,rarity,attri FROM `character` ORDER BY id ASC;"
    )
    rs = cur.fetchall()

    cur.execute(
        f"SELECT dev_id AS id, COUNT(*) AS total FROM `{pool}_roll` GROUP BY id ORDER BY id ASC"
    )
    character_report = cur.fetchall()
    cur.close()
    result_dict = {}
    count_dict = {}
    for row in character_report:
        count_dict[row["id"]] = row
    for row in rs:
        try:
            row["total"] = count_dict[row["id"]]["total"]
        except:
            row["total"] = 0
        finally:
            if (
                row["rarity"] == 5
                and row["id"] in flipper_gacha_pool.char_list[pool]["5-pu"]
            ):
                row["rarity"] = "5-pu"
            else:
                row["rarity"] = str(row["rarity"])
            result_dict[row["id"]] = row
    redis_data.set(f"{pool}_record", json.dumps(result_dict), ex=180)
    return result_dict


def check_pool(pool):
    if pool not in pool_data_detal.keys() or pool is None or pool == "":
        return list(pool_data_detal)[0]
    return pool


def get_time():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return dt2.strftime("%Y-%m-%d %H:%M:%S")


def convert_to_character_output(char):
    return {
        "name": f"{char['name']}",
        "id": f"{char['dev_id']}",
        "attri": f"{char['attri']}",
        "rarity": f"{char['rarity']}",
    }


@app.errorhandler(404)
@limiter.exempt
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/result/pool_list")
@limiter.exempt
def get_pool_list():
    return jsonify(pool_data_detal)


@app.route("/result/roll_data")
@limiter.exempt
def get_pool_roll_data():
    pool = request.args.get("pool")
    sql = f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}_record`;"
    cur = mysql.connection.cursor()
    cur.execute(sql)
    pool_roll_data = cur.fetchone()
    cur.close()
    if pool_roll_data["all_roll"] is None:
        pool_roll_data = {
            "all_five": 0,
            "all_four": 0,
            "all_three": 0,
            "all_roll": 0,
        }
    else:
        for key in pool_roll_data:
            pool_roll_data[key] = int(pool_roll_data[key])
    return jsonify(pool_roll_data)


@app.route("/result/character_report")
@limiter.exempt
def character_report():
    pool = check_pool(request.args.get("pool"))
    try:
        record = json.loads(redis_data.get(f"{pool}_record"))
    except:
        record = set_redis_record(pool)
    return jsonify({"report": list(record.values())})


@app.route("/result")
@limiter.exempt
def search():
    pool = check_pool(request.args.get("pool"))
    roll = request.args.get("roll")

    if roll is None or not roll.isdigit():
        abort(404)

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `{pool}_roll` WHERE sim_index = {roll};")
    result = list(cur.fetchall())
    cur.close()

    try:
        record = json.loads(redis_data.get(f"{pool}_record"))
    except:
        record = set_redis_record(pool)

    if result is not None:
        detail = []
        for roll_data in result:
            detail.append(record[roll_data["dev_id"]])
        return jsonify({"data": detail, "sim_index": roll})
    else:
        abort(404, description="記錄不存在!")


@app.route("/roll")
def gacha_row():
    info = {}
    pool = request.args.get("pool")
    ignore = request.args.get("ignore")
    header_referer = request.referrer
    if header_referer != "https://www.paverschlev.link/wf/flipper":
        return "請使用瀏覽器進行模擬抽卡\n如有疑慮請截圖後到巴哈主串附圖回報"
    if pool not in pool_data_detal.keys() or pool is None or pool == "":
        pool = list(pool_data_detal)[0]
    now = get_time()
    if pool_data_detal[pool]["type"] == "normal":
        items = flipper_gacha_pool.gacha(pool, 10)
    elif pool_data_detal[pool]["type"] == "single":
        items = flipper_gacha_pool.gacha_single(pool, 10)
    elif pool_data_detal[pool]["type"] == "three_pu":
        items = flipper_gacha_pool.gacha_three(pool, 10)
    elif pool_data_detal[pool]["type"] == "attribute":
        items = flipper_gacha_pool.gacha_attribute(pool, 10)
    else:
        abort(404)
    sql = f"""INSERT INTO `{pool}_record` (`five_count`, `four_count`, `three_count`, `seed`, `ip`, `time`) 
                VALUES ('{items[10]['5星']}', '{items[10]['4星']}', '{items[10]['3星']}', '{items[11]}','{limit_key_func()}','{now}');"""
    cur = mysql.connection.cursor()
    cur.execute(sql)
    mysql.connection.commit()
    times = cur.lastrowid
    sql = f"""INSERT INTO `{pool}_roll`
                VALUES 
                ({times},'{items[0]['id']}'),
                ({times},'{items[1]['id']}'),
                ({times},'{items[2]['id']}'),
                ({times},'{items[3]['id']}'),
                ({times},'{items[4]['id']}'),
                ({times},'{items[5]['id']}'),
                ({times},'{items[6]['id']}'),
                ({times},'{items[7]['id']}'),
                ({times},'{items[8]['id']}'),
                ({times},'{items[9]['id']}')"""
    cur.execute(sql)
    mysql.connection.commit()

    try:
        record = json.loads(redis_data.get(f"{pool}_record"))
    except:
        record = set_redis_record(pool)
    for i in range(0, 10):
        record[items[i]["id"]]["total"] += 1
    redis_data.set(f"{pool}_record", json.dumps(record), ex=180)

    cur.execute(
        f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}_record`;"
    )
    pool_roll_data = cur.fetchone()
    for key, item in pool_roll_data.items():
        pool_roll_data[key] = int(pool_roll_data[key])
    cur.close()
    items = items[:-2]
    info["data"] = items
    info["total"] = times
    info["report"] = pool_roll_data
    return jsonify(info)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@limiter.exempt
def catch_all(path):
    return render_template("index.html")
