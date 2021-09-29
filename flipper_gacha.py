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
)
from datetime import datetime, timezone, timedelta
import json
import random
import time
from flask_mysqldb import MySQL, MySQLdb
import flask_limiter
from gacha import gacha_pool

load_dotenv()

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
)
mysql = MySQL(app)


def limit_key_func():
    return str(request.headers.get("X-Forwarded-For", "127.0.0.1")).split(",")[0]


limiter = flask_limiter.Limiter(
    app, key_func=limit_key_func, default_limits=["85 per minute"]
)

flipper_gacha_pool = gacha_pool(
    os.path.join(app.config["STATIC_FOLDER"], "flipper_pool")
)

# 可以改成讀取json
pool_data_detal = {
    # "drawing_witch": {"name": "水炭池", "type": "normal"},#關閉水炭池
    # "Thunder-pu": {"name": "雷屬性精選", "type": "attribute"},#關閉雷PU
    "machine_police_girl": {"name": "警察池", "type": "single"},
    "halfanv": {"name": "半周年禮黑", "type": "three_pu"},
}

# Add character temp
character_list_temp = {}


def get_character(name):
    global character_list_temp
    if not bool(character_list_temp):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `character`;")
        rs = cursor.fetchall()
        for row in rs:
            character_list_temp[row['dev_id']] = row
        cursor.close()
    return character_list_temp[name]


def check_pool(pool):
    if pool not in pool_data_detal.keys() or pool is None or pool == "":
        return list(pool_data_detal)[0]
    return pool


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


def get_time():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return dt2.strftime("%Y-%m-%d %H:%M:%S")


@app.route("/", methods=["GET"])
@limiter.exempt
def home():
    return redirect(url_for("roll_display"))


@app.route("/flipper", methods=["GET", "POST"])
@limiter.exempt
def roll_display():
    if "ip_seed" not in session.keys():
        session["ip_seed"] = 0
    pool = request.args.get("pool")
    if pool not in pool_data_detal.keys() or pool is None or pool == "":
        pool = list(pool_data_detal)[0]
    roll = request.values.get("roll")
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}`;"
    )
    pool_roll_data = cur.fetchone()
    if pool_roll_data["all_roll"] is None:
        for key, dic_item in pool_roll_data.items():
            pool_roll_data[key] = 1
    return render_template(
        "flipper_gacha.html",
        pool=pool,
        total=pool_roll_data,
        pool_data=pool_data_detal,
    )


@app.route("/result/pool_list")
def get_pool_list():
    return jsonify(pool_data_detal)


@app.route("/result/roll_data")
def get_pool_roll_data():
    pool = request.args.get("pool")
    sql = f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}`;"
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


@app.route("/result")
def search():
    pool = check_pool(request.args.get("pool"))
    roll = request.args.get("roll")

    if roll is None or not roll.isdigit():
        abort(404)

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `{pool}` WHERE sim_index = {roll};")
    result = cur.fetchone()
    cur.close()

    if result is not None:
        detail = []

        for index in range(1, 11):
            key = f"roll_{index}"
            info = get_character(result[key])

            if (
                    info["rarity"] == 5
                    and info["dev_id"]
                    in flipper_gacha_pool.char_list[pool]["5-pu"]
            ):
                info["rarity"] = "5-pu"

            detail.append({
                "name": f"{info['name']}",
                "id": f"{info['dev_id']}",
                "attri": f"{info['attri']}",
                "rarity": f"{info['rarity']}",
            })
        return jsonify({"data": detail, "sim_index": result["sim_index"]})
    else:
        abort(404, description="記錄不存在!")


@app.route("/roll")
def gacha_row():
    info = {}
    pool = request.args.get("pool")
    ignore = request.args.get("ignore")
    if pool not in pool_data_detal.keys() or pool is None or pool == "":
        pool = list(pool_data_detal)[0]
    now = get_time()
    if ignore != os.getenv("IGNORE_TOKEN"):
        client_ip = limit_key_func()
        #
    else:
        client_ip = "ignore_token"
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
    sql = f"INSERT INTO `{app.config['MYSQL_DB']}`.`{pool}` (`roll_1`, `roll_2`, `roll_3`, `roll_4`, `roll_5`, `roll_6`, `roll_7`, `roll_8`, `roll_9`, `roll_10`, `five_count`, `four_count`, `three_count`, `seed`, `ip`, `time`) VALUES ('{items[0]['id']}', '{items[1]['id']}', '{items[2]['id']}', '{items[3]['id']}', '{items[4]['id']}', '{items[5]['id']}', '{items[6]['id']}', '{items[7]['id']}', '{items[8]['id']}', '{items[9]['id']}', '{items[10]['5星']}', '{items[10]['4星']}', '{items[10]['3星']}', '{items[11]}','{client_ip}','{now}');"
    cur = mysql.connection.cursor()
    cur.execute(sql)
    mysql.connection.commit()
    cur.execute(f"SELECT sim_index FROM `{pool}` ORDER BY sim_index DESC LIMIT 1")
    times = cur.fetchone()
    cur.execute(
        f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}`;"
    )
    pool_roll_data = cur.fetchone()
    for key, item in pool_roll_data.items():
        pool_roll_data[key] = int(pool_roll_data[key])
    cur.close()
    items = items[:-2]
    info["data"] = items
    info["total"] = times["sim_index"]
    info["report"] = pool_roll_data
    return jsonify(info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
