from items import *
from map import rooms

inventory = [item_id, item_laptop, item_money]
inventory_weight = item_id["mass"] + item_laptop["mass"] + item_money["mass"]
inventory_max_weight = 25
# Start game at the reception
current_room = rooms["Reception"]
