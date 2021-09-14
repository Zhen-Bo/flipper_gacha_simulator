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
    SECRET_KEY=os.getenv("SECRET_KEY"),
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    STATIC_FOLDER=os.getenv("STATIC_FOLDER"),
    MYSQL_HOST=os.getenv("SEVER_IP"),
    MYSQL_USER=os.getenv("DB_USER"),
    MYSQL_PASSWORD=os.getenv("DB_PASS"),
    MYSQL_DB=os.getenv("DB_TABLE"),
    MYSQL_CURSORCLASS="DictCursor",
)
mysql = MySQL(app)


def limit_key_func():
    return str(request.headers.get("X-Forwarded-For", "127.0.0.1")).split(",")[0]


limiter = flask_limiter.Limiter(
    app, key_func=limit_key_func, default_limits=["65 per minute"]
)

flipper_gacha_pool = gacha_pool(
    os.path.join(app.config["STATIC_FOLDER"], "flipper_pool")
)

# 可以改成讀取json
pool_data = ["drawing_witch", "machine_police_girl"]


def get_time():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return dt2.strftime("%Y-%m-%d %H:%M:%S")


@app.route("/wf", methods=["GET"])
@limiter.exempt
def home():
    return redirect(url_for("roll_display"))


@app.route("/wf/flipper", methods=["GET"])
@limiter.exempt
def roll_display():
    print(limit_key_func())
    pool = request.args.get("pool")
    if pool not in pool_data or pool is None or pool == "":
        pool = pool_data[0]
    roll = request.values.get("roll")
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}`;"
    )
    pool_roll_data = cur.fetchone()
    if pool_roll_data["all_roll"] is None:
        for key, dic_item in pool_roll_data.items():
            pool_roll_data[key] = 1
    return render_template("flipper_gacha.html", pool=pool, total=pool_roll_data)


@app.route("/wf/result")
@limiter.exempt
def search():
    pool = request.args.get("pool")
    roll = request.args.get("roll")
    if pool not in pool_data or pool is None or pool == "":
        pool = pool_data[0]
    if not roll.isdigit():
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM `{pool}` WHERE sim_index = {roll};")
    result = cur.fetchone()
    if result is not None:
        rarity_total = {"3星": 0, "4星": 0, "5星": 0}
        detal = []
        for index in range(1, 11):
            key = f"roll_{index}"
            cur.execute(f"SELECT * FROM `character` WHERE dev_id = '{result[key]}';")
            character_dict = cur.fetchone()
            info = {
                "name": f"{character_dict['name']}",
                "id": f"{character_dict['dev_id']}",
                "attri": f"{character_dict['attri']}",
                "rarity": f"{character_dict['rarity']}",
            }
            if character_dict["rarity"] == 3:
                rarity_total["3星"] += 1
            elif character_dict["rarity"] == 4:
                rarity_total["4星"] += 1
            elif character_dict["rarity"] == 5:
                rarity_total["5星"] += 1
            if (
                character_dict["rarity"] == 5
                and character_dict["dev_id"]
                in flipper_gacha_pool.char_list[pool]["5-pu"]
            ):
                info["rarity"] = "5-pu"
            detal.append(info)
        detal.append(rarity_total)
        detal.append(result["sim_index"])
        cur.execute(
            f"SELECT SUM(five_count) AS all_five,SUM(four_count) AS all_four,SUM(three_count) AS all_three ,SUM(five_count)+SUM(four_count)+SUM(three_count) AS all_roll FROM `{pool}`;"
        )
        pool_roll_data = cur.fetchone()
        for key, item in pool_roll_data.items():
            pool_roll_data[key] = int(pool_roll_data[key])
        cur.close()
        detal.append(pool_roll_data)
        return render_template(
            "flipper_gacha.html", pool=pool, total=pool_roll_data, result=detal
        )
    else:
        abort(404)


@app.route("/wf/roll")
def gacha_row():
    pool = request.args.get("pool")
    if pool not in pool_data or pool is None or pool == "":
        pool = pool_data[0]
    items = flipper_gacha_pool.gacha(pool, 10)
    now = get_time()
    sql = f"INSERT INTO `{app.config['MYSQL_DB']}`.`{pool}` (`roll_1`, `roll_2`, `roll_3`, `roll_4`, `roll_5`, `roll_6`, `roll_7`, `roll_8`, `roll_9`, `roll_10`, `five_count`, `four_count`, `three_count`,`seed`,`time`) VALUES ('{items[0]['id']}', '{items[1]['id']}', '{items[2]['id']}', '{items[3]['id']}', '{items[4]['id']}', '{items[5]['id']}', '{items[6]['id']}', '{items[7]['id']}', '{items[8]['id']}', '{items[9]['id']}', '{items[10]['5星']}', '{items[10]['4星']}', '{items[10]['3星']}', '{items[11]}','{now}');"
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
    items = items[:-1]
    items.append(times["sim_index"])
    items.append(pool_roll_data)
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
