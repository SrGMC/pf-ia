configuration = {
"text_size": 400, 
"tile_size": 60, 
"type": "load", #random
"seed": None,
"file": "./student/map.txt",
"map_size": [13, 7],
"delay": 0.1,
"debugMap": False,
"debug": False,
"save": False, #True
"hazards": False,
"basicTile": "street",
"maxBags": 2, 
"agent":{
    "graphics":{ 
        "default": "game/graphics/logistics/bicycle100.png"
        },
    "id": "agent",
    "marker": 'A',
    "start": [0,0],
    },
"maptiles": {
    "street": {
        "graphics":{ 
            "default": "student/images/street.png",
            "traversed": "student/images/street_traversed.png"
            },
        "id":  "street",
        "marker": 'T',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 2, "level": 0},
        },
    "path": {
        "graphics":{ 
            "default": "student/images/path.png",
            "traversed": "student/images/path_traversed.png"
            },
        "id":  "path",
        "marker": 'H',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 4, "level": 0},
        },
    "bike_street": {
        "graphics":{ 
            "default": "student/images/bike_street.png",
            "traversed": "student/images/bike_street_traversed.png"
            },
        "id":  "bike_street",
        "marker": 'B',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1},
        },
    "broken_road": {
        "graphics":{ 
            "default": "student/images/broken_road.png",
            "traversed": "student/images/broken_road_traversed.png"
            },
        "id":  "broken_road",
        "marker": 'R',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 7},
        },
    "easy_bridge": {
        "graphics":{ 
            "default": "student/images/easy_bridge.png",
            "traversed": "student/images/easy_bridge_traversed.png"
            },
        "id":  "easy_bridge",
        "marker": 'E',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 4},
        },
    "difficult_bridge": {
        "graphics":{ 
            "default": "student/images/diff_bridge.png",
            "traversed": "student/images/diff_bridge_traversed.png"
            },
        "id":  "difficult_bridge",
        "marker": 'D',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 6},
        },
    "pedestrian_walk": {
        "graphics":{ 
            "default": "student/images/pedestrian.png",
            "traversed": "student/images/pedestrian_traversed.png"
            },
        "id":  "pedestrian_walk",
        "marker": 'I',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1.5, "level": 0},
        },
    "pizza": {
        "graphics":{ 
            "default": "game/graphics/logistics/restaurant100.png",
            "traversed": "game/graphics/logistics/restaurant100.png"
            },
        "id":  "pizza",
        "marker": 'Z',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "level": 0},
        },
    "customer0": {
        "graphics":{ 
            "default": "game/graphics/logistics/customer100.png",
            "traversed": "game/graphics/logistics/customer100.png"
            },
        "id":  "customer0",
        "marker": '0',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 0},
        },
    "customer1": {
        "graphics":{ 
            "default": "game/graphics/logistics/customer100_1.png",
            "traversed": "game/graphics/logistics/customer100_1.png"
            },
        "id":  "customer1",
        "marker": '1',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 1},
        },
    "customer2": {
        "graphics":{ 
            "default": "game/graphics/logistics/customer100_2.png",
            "traversed": "game/graphics/logistics/customer100_2.png"
            },
        "id":  "customer2",
        "marker": '2',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 2},
        },
    "customer3": {
        "graphics":{ 
            "default": "game/graphics/logistics/customer100_3.png",
            "traversed": "game/graphics/logistics/customer100_3.png"
            },
        "id":  "customer3",
        "marker": '3',
        "num": 3,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "unload": True, "objects": 3},
        },
    "start": {
        "graphics":{ 
            "default": "game/graphics/logistics/base100.png",
            "traversed": "game/graphics/logistics/base100.png"
            },
        "id":  "start",
        "marker": 'W',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1},
        },
    "building": {
        "graphics":{ 
            "default": "game/graphics/logistics/building100.png",
            "traversed": "game/graphics/logistics/building100.png"
            },
        "id":  "building",
        "marker": 'X',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "blocked": True},
        },
    "fountain": {
        "graphics":{ 
            "default": "student/images/font.png",
            "traversed": "student/images/font.png"
            },
        "id":  "fountain",
        "marker": 'F',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "blocked": True},
        },
    "water": {
        "graphics":{ 
            "default": "student/images/water.png",
            "traversed": "student/images/water.png"
            },
        "id":  "water",
        "marker": 'G',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "blocked": True},
        },
    "water_rocks": {
        "graphics":{ 
            "default": "student/images/water_rocks.png",
            "traversed": "student/images/water_rocks.png"
            },
        "id":  "water_rocks",
        "marker": 'S',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "blocked": True},
        },
    "trees": {
        "graphics":{ 
            "default": "student/images/trees.png",
            "traversed": "student/images/trees.png"
            },
        "id":  "trees",
        "marker": 'O',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "blocked": True},
        },
    "charger": {
        "graphics":{ 
            "default": "student/images/charger.png",
            "traversed": "student/images/charger_traversed.png"
            },
        "id":  "charger",
        "marker": 'C',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 1, "recharge": True, "level": 0},
        },
    "level1": {
        "graphics":{ 
            "default": "student/images/level1.png",
            "traversed": "student/images/level1_traversed.png"
            },
        "id":  "level1",
        "marker": '6',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 2, "level": 1},
        },
    "level2": {
        "graphics":{ 
            "default": "student/images/level2.png",
            "traversed": "student/images/level2_traversed.png"
            },
        "id":  "level2",
        "marker": '7',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 2, "level": 2},
        },
    "level3": {
        "graphics":{ 
            "default": "student/images/level3.png",
            "traversed": "student/images/level3_traversed.png"
            },
        "id":  "level3",
        "marker": '8',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 2, "level": 3},
        },
    "level4": {
        "graphics":{ 
            "default": "student/images/level4.png",
            "traversed": "student/images/level4_traversed.png"
            },
        "id":  "level4",
        "marker": '9',
        "num": 0,
        "state":
            {"agent":None,"image": "default"},
        "attributes":
            {"cost": 2, "level": 4},
        }
    }

}
