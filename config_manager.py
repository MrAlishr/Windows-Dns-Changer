#  /*******************************************************************************
#   *
#   *  * Copyright (c)  2024.
#   *  * All Credits Goes to MrAlishr
#   *  * Email : Alishariatirad@gmail.com
#   *  * Github: github.com/MrAlishr
#   *  * Telegram : Alishrr
#   *  *
#   *
#   ******************************************************************************/

import json


def load_config(file_path='dns_config.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Default DNS settings
        return {
            'Shecan': ('178.22.122.100', '185.51.200.2'),
            'Begzar': ('185.55.226.26', '185.55.225.25'),
            'Shatel': ('85.15.1.14', '85.15.1.15'),
            'Electro': ('78.157.42.101', '78.157.42.100'),
            'Radar': ('10.202.10.10', '10.202.10.11'),
            '403': ('10.202.10.202', '10.202.10.202')
        }


def save_config(config, file_path='dns_config.json'):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)
