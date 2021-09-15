import time
import random
import json
import os


class gacha_pool:
    def __init__(self, pool_path):
        self.char_list = self.read_list(pool_path)

    def read_list(self, pool_path):
        pool_dict = {}
        for pool_data in os.listdir(pool_path):
            if "json" in pool_data:
                with open(
                    os.path.join(pool_path, pool_data), mode="r", encoding="utf-8"
                ) as jf:
                    pool_dict[pool_data.split(".")[0]] = json.loads(jf.read())
        return pool_dict

    def gacha_uncommon(self, pool, amount):
        if amount > 10:
            amount = 10
        info = {"5星": 0, "4星": 0, "3星": 0}
        rnd_seed = round(time.time(), 3)
        random.seed(rnd_seed)
        items = []
        for i in range(amount):
            rnd = random.randint(0, 100000)
            rnd /= 1000
            if i != amount - 1:
                if rnd >= 0 and rnd <= 2:
                    item = random.choice(self.char_list[pool]["five_pu"])
                    info["5星"] += 1
                elif rnd > 2 and rnd <= 5:
                    item = random.choice(self.char_list[pool]["five"])
                    info["5星"] += 1
                elif rnd > 5 and rnd <= 15:
                    item = random.choice(self.char_list[pool]["four_pu"])
                    info["4星"] += 1
                elif rnd > 15 and rnd <= 30:
                    item = random.choice(self.char_list[pool]["four"])
                    info["4星"] += 1
                elif rnd > 30 and rnd <= 58:
                    item = random.choice(self.char_list[pool]["three_pu"])
                    info["3星"] += 1
                elif rnd > 58 and rnd <= 100:
                    item = random.choice(self.char_list[pool]["three"])
                    info["3星"] += 1
            else:
                if rnd >= 0 and rnd <= 2:
                    item = random.choice(self.char_list[pool]["five_pu"])
                    info["5星"] += 1
                elif rnd > 2 and rnd <= 5:
                    item = random.choice(self.char_list[pool]["five"])
                    info["5星"] += 1
                elif rnd > 5 and rnd <= 43:
                    item = random.choice(self.char_list[pool]["four_pu"])
                    info["4星"] += 1
                elif rnd > 43 and rnd <= 100:
                    item = random.choice(self.char_list[pool]["four"])
                    info["4星"] += 1
            items.append(item)
        for i in range(10 - amount):
            items.append("")
        items.append(info)
        items.append(rnd_seed)
        return items

    def gacha(self, pool, amount):
        if amount > 10:
            amount = 10
        info = {"5星": 0, "4星": 0, "3星": 0}
        rnd_seed = round(time.time(), 3)
        random.seed(rnd_seed)
        items = []
        for i in range(amount):
            rnd = random.randint(0, 1000000)
            if i != amount - 1:
                if rnd >= 0 and rnd <= 20000:
                    item = random.choice(self.char_list[pool]["five_pu"])
                    info["5星"] += 1
                elif rnd > 20000 and rnd <= 50000:
                    item = random.choice(self.char_list[pool]["five"])
                    info["5星"] += 1
                elif rnd > 50000 and rnd <= 90000:
                    item = random.choice(self.char_list[pool]["four_pu"])
                    info["4星"] += 1
                elif rnd > 90000 and rnd <= 300000:
                    item = random.choice(self.char_list[pool]["four"])
                    info["4星"] += 1
                elif rnd > 300000 and rnd <= 335000:
                    item = random.choice(self.char_list[pool]["three_pu"])
                    info["3星"] += 1
                elif rnd > 335000 and rnd <= 1000000:
                    item = random.choice(self.char_list[pool]["three"])
                    info["3星"] += 1
            else:
                if rnd >= 0 and rnd <= 20000:
                    item = random.choice(self.char_list[pool]["five_pu"])
                    info["5星"] += 1
                elif rnd > 20000 and rnd <= 50000:
                    item = random.choice(self.char_list[pool]["five"])
                    info["5星"] += 1
                elif rnd > 50000 and rnd <= 202040:
                    item = random.choice(self.char_list[pool]["four_pu"])
                    info["4星"] += 1
                elif rnd > 202040 and rnd <= 1000000:
                    item = random.choice(self.char_list[pool]["four"])
                    info["4星"] += 1
            items.append(item)
        for i in range(10 - amount):
            items.append("")
        items.append(info)
        items.append(rnd_seed)
        return items
