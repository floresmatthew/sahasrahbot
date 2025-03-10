import argparse
import shlex
import sys
import random

import ircmessage

from alttprbot.alttprgen import preset, smz3multi, smvaria
from alttprbot.alttprgen.randomizer import smdash
from alttprbot.database import spoiler_races, srl_races, tournament_results
from alttprbot.exceptions import SahasrahBotException
# from alttprbot.tournament import league
from alttprbot.util.srl import get_race, srl_race_id


async def handler(target, source, message, client):
    if not message[0] == '$':
        return

    try:
        args = await parse_args(message)
    except argparse.ArgumentError as err:
        if not target == '#speedrunslive':
            await client.message(target, err.message)
        return

    post_start_message = None

    if args.command in ['$preset', '$race'] and target.startswith('#srl-'):
        srl_id = srl_race_id(target)
        srl = await get_race(srl_id)
        await client.message(target, "Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        race = await srl_races.get_srl_race_by_id(srl_id)

        if race:
            raise SahasrahBotException(
                "There is already a game generated for this room.  To cancel it, use the $cancel command.")

        if srl['game']['abbrev'] in ['supermetroid', 'supermetroidhacks']:
            randomizer = 'sm'
        else:
            raise SahasrahBotException("This game is not yet supported.")

        seed, preset_dict = await preset.get_preset(
            args.preset,
            randomizer=randomizer,
            hints=args.hints,
            spoilers="off",
            allow_quickswap=True if args.command == "$quickswaprace" else False
        )
        goal = preset_dict['goal_name']

        pre_race_goal = goal

        pre_race_goal += f" - {seed.url}"
        if seed.code is not None:
            pre_race_goal += f" - ({'/'.join(seed.code)})" if isinstance(
                seed.code, list) else f" - ({seed.code})"

        if args.silent:
            await client.message(target, pre_race_goal)
        else:
            await client.message(target, f".setgoal {pre_race_goal}")

        await srl_races.insert_srl_race(srl_id, goal, post_start_message)

    if args.command == '$smmulti' and target.startswith('#srl-'):
        srl_id = srl_race_id(target)
        srl = await get_race(srl_id)
        await client.message(target, "Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        race = await srl_races.get_srl_race_by_id(srl_id)

        if race:
            raise SahasrahBotException("There is already a game generated for this room.  To cancel it, use the $cancel command.")

        if srl['game']['abbrev'] in ['supermetroid', 'supermetroidhacks']:
            # verify team sizes are equal
            if len({len(t) for t in args.team}) != 1:
                await client.message(target, "Team sizes are uneven.  Aborting!")
                return

            seed_number = random.randint(0, 2147483647)

            for team in args.team:
                seed = await smz3multi.generate_multiworld(args.preset, team, tournament=True, randomizer='sm', seed_number=seed_number)
                await client.message(target, f"Team {', '.join(team)}: {seed.url}")

            goal = "sm multiworld - DO NOT RECORD"
        else:
            raise SahasrahBotException("This game is not supported.")

        await srl_races.insert_srl_race(srl_id, goal)

    if args.command == '$smdash' and target.startswith('#srl-'):
        srl_id = srl_race_id(target)
        srl = await get_race(srl_id)
        await client.message(target, "Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        race = await srl_races.get_srl_race_by_id(srl_id)

        if race:
            raise SahasrahBotException("There is already a game generated for this room.  To cancel it, use the $cancel command.")

        if srl['game']['abbrev'] in ['supermetroid', 'supermetroidhacks']:
            url = await smdash.create_smdash(mode=args.preset)
            goal = "item randomizer"
            await client.message(target, f".setgoal {goal} - {url}")
        else:
            raise SahasrahBotException("This game is not supported.")

        await srl_races.insert_srl_race(srl_id, goal)

    if args.command == '$smvaria' and target.startswith('#srl-'):
        srl_id = srl_race_id(target)
        srl = await get_race(srl_id)
        await client.message(target, "Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        race = await srl_races.get_srl_race_by_id(srl_id)

        if race:
            raise SahasrahBotException("There is already a game generated for this room.  To cancel it, use the $cancel command.")

        if srl['game']['abbrev'] in ['supermetroid', 'supermetroidhacks']:
            seed = await smvaria.generate_preset(args.settings, args.skills, race=True)
            goal = "item randomizer"
            await client.message(target, f".setgoal {goal} - {seed.url}")
        else:
            raise SahasrahBotException("This game is not supported.")

        await srl_races.insert_srl_race(srl_id, goal)

    if args.command == '$smleagueplayoff' and target.startswith('#srl-'):
        srl_id = srl_race_id(target)
        srl = await get_race(srl_id)
        await client.message(target, "Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        race = await srl_races.get_srl_race_by_id(srl_id)

        if race:
            raise SahasrahBotException("There is already a game generated for this room.  To cancel it, use the $cancel command.")

        if srl['game']['abbrev'] in ['supermetroid', 'supermetroidhacks']:
            seed = await smvaria.generate_league_playoff(args.majors, args.area, args.bosses)
            goal = "item randomizer"
            await client.message(target, f".setgoal {goal} - {seed.url}")
        else:
            raise SahasrahBotException("This game is not supported.")

        await srl_races.insert_srl_race(srl_id, goal)

    if args.command == '$cancel' and target.startswith('#srl-'):
        srl_id = srl_race_id(target)
        await srl_races.delete_srl_race(srl_id)
        await spoiler_races.delete_spoiler_race(srl_id)
        await tournament_results.delete_active_tournament_race(srl_id)
        await client.message(target, "Current race cancelled.")
        await client.message(target, ".setgoal new race")

    if args.command == '$help':
        await client.message(target, "For documentation on using this bot, visit https://sahasrahbot.synack.live/srl.html")

    if args.command == '$joinroom':
        await client.join(args.channel)

    if args.command == '$leave' and target.startswith('#srl-'):
        await client.part(target)

    if args.command == '$vt' and target.startswith('#srl-'):
        await client.message(target, "You summon VT, he looks around confused and curses your next game with bad RNG.")


async def parse_args(message):
    split_msg = ['sb'] + shlex.split(message)

    parser = SrlArgumentParser()
    parser.add_argument('base', type=str)

    subparsers = parser.add_subparsers(dest="command")

    parser_preset = subparsers.add_parser('$preset')
    parser_preset.add_argument('preset')
    parser_preset.add_argument('--silent', action='store_true')

    parser_race = subparsers.add_parser('$race')
    parser_race.add_argument('preset')
    parser_race.add_argument('--silent', action='store_true')

    # Namespace(preset='normal', team=[['player1', 'player2'], ['player3', 'player4']])
    parser_smmulti = subparsers.add_parser('$smmulti')
    parser_smmulti.add_argument('preset')
    parser_smmulti.add_argument('--team', nargs='*', action='append', required=True)

    parser_smvaria = subparsers.add_parser('$smvaria')
    parser_smvaria.add_argument('skills')
    parser_smvaria.add_argument('settings')

    parser_smplayoffs = subparsers.add_parser('$smleagueplayoff')
    parser_smplayoffs.add_argument('majors')
    parser_smplayoffs.add_argument('area')
    parser_smplayoffs.add_argument('bosses')

    parser_smdash = subparsers.add_parser('$smdash')
    parser_smdash.add_argument('preset', default='mm')

    parser_join = subparsers.add_parser('$joinroom')
    parser_join.add_argument('channel')

    subparsers.add_parser('$leave')

    subparsers.add_parser('$cancel')

    subparsers.add_parser('$vt')

    parser_echo = subparsers.add_parser('$echo')
    parser_echo.add_argument('message')

    subparsers.add_parser('$help')

    args = parser.parse_args(split_msg)

    return args


class SrlArgumentParser(argparse.ArgumentParser):
    def _get_action_from_name(self, name):
        """Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is
        passed as it's first arg...
        """
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action

    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc
        # super(SrlArgumentParser, self).error(message)
