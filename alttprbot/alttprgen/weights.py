weights = {
    'casual': {
        'randomizer': {
            'item': 1,
            'entrance': .5
        },
        'difficulty': {
            'easy': 1,
            'normal': 1,
            'hard': .5
        },
        'goal_item': {
            'ganon': 1,
            'dungeons': 1,
            'pedestal': 1,
            'triforce-hunt': 1
        },
        'goal_entrance': {
            'ganon': 1,
            'crystals': 1,
            'dungeons': 1,
            'pedestal': 1,
            'triforcehunt': 1
        },
        'mode_item': {
            'standard': 1,
            'open': 1,
            'inverted': .25
        },
        'mode_entrance': {
            'swordless': .2,
            'open': 1
        },
        'weapons': {
            'randomized': 1,
            'uncle': 1,
            'swordless': .2
        },
        'shuffle': {
            'simple': 1,
            'restricted': 1,
            'full': .25,
            'crossed': .25,
        },
        'variation': {
            'none': 1,
            'key-sanity': 1,
            'retro': .25
        },
        'enemizer_enabled': {
            True: .25,
            False: 1
        },
        'enemizer_enemy': {
            True: 1,
            False: 1
        },
        'enemizer_enemy_health': {
            0: 1,
            1: 1,
            2: .25,
        },
        'enemizer_pot_shuffle': {
            True: 1,
            False: 1,
        },
        'enemizer_palette_shuffle': {
            True: 1,
            False: 1
        },
        'enemizer_enemy_damage': {
            'off': 1,
            'shuffle': .5,
            'chaos': .25,
        },
        'enemizer_boss': {
            'off': 1,
            'basic': 1,
            'normal': 1,
            'chaos': .5
        }
    },
    'weighted': {
        'randomizer': {
            'item': 1,
            'entrance': 1
        },
        'difficulty': {
            'easy': .25,
            'normal': 1,
            'hard': 1,
            'expert': .5,
            'insane': .1
        },
        'goal_item': {
            'ganon': 1,
            'dungeons': 1,
            'pedestal': 1,
            'triforce-hunt': 1
        },
        'goal_entrance': {
            'ganon': 1,
            'crystals': 1,
            'dungeons': 1,
            'pedestal': 1,
            'triforcehunt': 1
        },
        'mode_item': {
            'standard': 1,
            'open': 1,
            'inverted': .75
        },
        'mode_entrance': {
            'swordless': .2,
            'open': .8
        },
        'weapons': {
            'randomized': .4,
            'uncle': .4,
            'swordless': .2
        },
        'shuffle': {
            'simple': 0.75,
            'restricted': 0.75,
            'full': 1,
            'crossed': 1,
            'insanity': .25
        },
        'variation': {
            'none': 1,
            'key-sanity': 1,
            'retro': .25
        },
        'enemizer_enabled': {
            True: 0.75,
            False: 1
        },
        'enemizer_enemy': {
            True: 1,
            False: 1
        },
        'enemizer_enemy_health': {
            0: 1,
            1: 1,
            2: 1,
            3: 0.5,
            4: 0.25
        },
        'enemizer_pot_shuffle': {
            True: 1,
            False: 1,
        },
        'enemizer_palette_shuffle': {
            True: 1,
            False: 1
        },
        'enemizer_enemy_damage': {
            'off': 1,
            'shuffle': 1,
            'chaos': 0.5,
        },
        'enemizer_boss': {
            'off': 1,
            'basic': 1,
            'normal': 1,
            'chaos': 1
        }
    },
    'unweighted': {
        'randomizer': {
            'item': 1,
            'entrance': 1
        },
        'difficulty': {
            'easy': 1,
            'normal': 1,
            'hard': 1,
            'expert': 1,
            'insane': 1
        },
        'goal_item': {
            'ganon': 1,
            'dungeons': 1,
            'pedestal': 1,
            'triforce-hunt': 1
        },
        'goal_entrance': {
            'ganon': 1,
            'crystals': 1,
            'dungeons': 1,
            'pedestal': 1,
            'triforcehunt': 1
        },
        'mode_item': {
            'standard': 1,
            'open': 1,
            'inverted': 1
        },
        'mode_entrance': {
            'swordless': 1,
            'open': 1
        },
        'weapons': {
            'randomized': 1,
            'uncle': 1,
            'swordless': 1
        },
        'shuffle': {
            'simple': 1,
            'restricted': 1,
            'full': 1,
            'crossed': 1,
            'insanity': 1
        },
        'variation': {
            'none': 1,
            'key-sanity': 1,
            'retro': 1
        },
        'enemizer_enabled': {
            True: 1,
            False: 1
        },
        'enemizer_enemy': {
            True: 1,
            False: 1
        },
        'enemizer_enemy_health': {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1
        },
        'enemizer_pot_shuffle': {
            True: 1,
            False: 1,
        },
        'enemizer_palette_shuffle': {
            True: 1,
            False: 1
        },
        'enemizer_enemy_damage': {
            'off': 1,
            'shuffle': 1,
            'chaos': 1,
        },
        'enemizer_boss': {
            'off': 1,
            'basic': 1,
            'normal': 1,
            'chaos': 1
        }
    }
}