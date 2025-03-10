import asyncio
from datetime import datetime
import math
# import logging

from alttprbot.alttprgen import mystery, preset, spoilers
from alttprbot.database import spoiler_races, tournament_results
from alttprbot.tournament import league, alttpr
from racetime_bot import monitor_cmd

from .core import SahasrahBotCoreHandler


class GameHandler(SahasrahBotCoreHandler):
    async def race_data(self, data):
        self.data = data.get('race')

        if self.data.get('status', {}).get('value') == 'in_progress':
            await self.in_progress()

        if self.data.get('status', {}).get('value') in ['open', 'invitational']:
            await self.intro()

        pending_entrants = [e for e in self.data['entrants'] if e.get('status', {}).get('value', {}) == 'requested']
        for entrant in pending_entrants:
            if self.tournament:
                if entrant['user']['id'] in self.tournament.player_racetime_ids:
                    await self.accept_request(entrant['user']['id'])

                elif await alttpr.can_gatekeep(entrant['user']['id'], self.data['name']):
                    await self.accept_request(entrant['user']['id'])
                    await self.add_monitor(entrant['user']['id'])

    async def begin(self):
        self.state['locked'] = False

        if self.tournament is None:
            race = await tournament_results.get_active_tournament_race(self.data.get('name'))
            if race:
                try:
                    self.tournament = await alttpr.TournamentRace.construct(episodeid=race['episode_id'])
                except alttpr.UnableToLookupEpisodeException:
                    self.logger.exception("Error while association tournament race to handler.")

        # re-establish a spoiler race countdown if bot is restarted/crashes
        in_progress_spoiler_race = await spoiler_races.get_spoiler_race_by_id_started(self.data.get('name'))
        if in_progress_spoiler_race:
            loop = asyncio.get_running_loop()
            started_time = in_progress_spoiler_race['started']
            now_time = datetime.utcnow()
            remaining_duration = (
                started_time - now_time).total_seconds() + in_progress_spoiler_race['studytime']
            loop.create_task(self.countdown_timer(
                duration_in_seconds=remaining_duration,
                beginmessage=True,
            ))

    async def in_progress(self):
        await self.send_spoiler_log()
        await league.process_league_race_start(self)

    async def ex_preset(self, args, message):
        # if league.is_league_race(self.data.get('name')):
        #     await self.send_message('This is a league race room, please use !leaguerace to roll')
        #     return
        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return
        await self.roll_game(preset_name=preset_name, message=message, allow_quickswap=False)

    async def ex_race(self, args, message):
        # if league.is_league_race(self.data.get('name')):
        #     await self.send_message('This is a league race room, please use !leaguerace to roll')
        #     return
        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return
        await self.roll_game(preset_name=preset_name, message=message, allow_quickswap=False)

    # async def ex_leaguerace(self, args, message):
    #     if await self.is_locked(message):
    #         return

    #     await league.process_league_race(
    #         handler=self,
    #         episodeid=args[0] if len(args) >= 1 else None,
    #         week=args[1] if len(args) == 2 else None
    #     )

    async def ex_tournamentrace(self, args, message):
        if await self.is_locked(message):
            return

        await alttpr.process_tournament_race(
            handler=self,
            episodeid=args[0] if len(args) >= 1 else None
        )

    async def ex_quickswaprace(self, args, message):
        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return
        await self.roll_game(preset_name=preset_name, message=message, allow_quickswap=True)

    async def ex_spoiler(self, args, message):
        # if league.is_league_race(self.data.get('name')):
        #     await self.send_message('This is a league race room, please use !leaguerace to roll')
        #     return

        if await self.is_locked(message):
            return

        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return

        await self.send_message("Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        try:
            seed, preset_dict, spoiler_log_url = await spoilers.generate_spoiler_game(preset_name)
        except preset.PresetNotFoundException as e:
            await self.send_message(str(e))
            return

        try:
            studytime = int(args[1])
        except IndexError:
            studytime = preset_dict.get('studytime', 900)

        await self.set_raceinfo(f"spoiler {preset_name} - {seed.url} - ({'/'.join(seed.code)})")
        await self.send_message(seed.url)
        await self.send_message(f"The spoiler log for this race will be sent after the race begins in this room.  A {studytime}s countdown timer at that time will begin.")
        await spoiler_races.insert_spoiler_race(self.data.get('name'), spoiler_log_url, studytime)
        self.seed_rolled = True

    async def ex_progression(self, args, message):
        # if league.is_league_race(self.data.get('name')):
        #     await self.send_message('This is a league race room, please use !leaguerace to roll')
        #     return

        if await self.is_locked(message):
            return

        try:
            preset_name = args[0]
        except IndexError:
            await self.send_message(
                'You must specify a preset!'
            )
            return

        await self.send_message("Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        try:
            seed, _, spoiler_log_url = await spoilers.generate_spoiler_game(preset_name, spoiler_type='progression')
        except preset.PresetNotFoundException as e:
            await self.send_message(str(e))
            return

        await self.set_raceinfo(f"spoiler {preset_name} - {seed.url} - ({'/'.join(seed.code)})")
        await self.send_message(seed.url)
        await self.send_message(f"The progression spoiler for this race will be sent after the race begins in this room.")
        await spoiler_races.insert_spoiler_race(self.data.get('name'), spoiler_log_url, 0)
        self.seed_rolled = True

    async def ex_mystery(self, args, message):
        # if league.is_league_race(self.data.get('name')):
        #     await self.send_message('This is a league race room, please use !leaguerace to roll')
        #     return

        if await self.is_locked(message):
            return

        weightset = args[0] if args else 'weighted'

        await self.send_message("Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        try:
            seed = await mystery.generate_random_game(
                weightset=weightset,
                tournament=True,
                spoilers="mystery"
            )
        except mystery.WeightsetNotFoundException as e:
            await self.send_message(str(e))
            return

        await self.set_raceinfo(f"mystery {weightset} - {seed.url} - ({'/'.join(seed.code)})")
        await self.send_message(seed.url)
        await self.send_message("Seed rolling complete.  See race info for details.")
        self.seed_rolled = True

    @monitor_cmd
    async def ex_cancel(self, args, message):
        self.seed_rolled = False
        await self.set_raceinfo("New Race", overwrite=True)
        await tournament_results.delete_active_tournament_race(self.data.get('name'))
        await spoiler_races.delete_spoiler_race(self.data.get('name'))
        await self.send_message("Reseting bot state.  You may now roll a new game.")

    async def ex_cc(self, args, message):
        await self.roll_game(preset_name="standard", message=message, allow_quickswap=True)

    async def ex_help(self, args, message):
        await self.send_message("Available commands:\n\"!race <preset>\" to generate a race preset.\n\"!mystery <weightset>\" to generate a mystery game.\n\"!spoiler <preset>\" to generate a spoiler race.  Check out https://sahasrahbot.synack.live/rtgg.html for more info.")

    async def ex_register(self, args, message):
        await self.send_message("Lazy Kid ain't got nothing compared to me.")

    async def ex_vt(self, args, message):
        await self.send_message("You summon Veetorp, he looks around confused and curses your next game with bad (CS)PRNG.")

    async def ex_synack(self, args, message):
        await self.send_message("You need to be more creative.")

    async def send_spoiler_log(self):
        name = self.data.get('name')
        race = await spoiler_races.get_spoiler_race_by_id(name)
        if race:
            await spoiler_races.start_spoiler_race(name)
            await self.send_message('Sending spoiler log...')
            await self.send_message('---------------')
            await self.send_message(f"This race\'s spoiler log: {race['spoiler_url']}")
            await self.send_message('---------------')
            await self.send_message('GLHF! :mudora:')
            loop = asyncio.get_running_loop()
            loop.create_task(self.countdown_timer(
                duration_in_seconds=race['studytime'],
                beginmessage=True,
            ))

    async def countdown_timer(self, duration_in_seconds, beginmessage=False):
        loop = asyncio.get_running_loop()

        reminders = [1800, 1500, 1200, 900, 600, 300,
                     120, 60, 30, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        start_time = loop.time()
        end_time = loop.time() + duration_in_seconds
        while True:
            # logging.info(datetime.datetime.now())
            timeleft = math.ceil(
                start_time - loop.time() + duration_in_seconds)
            # logging.info(timeleft)
            if timeleft in reminders:
                minutes = math.floor(timeleft/60)
                seconds = math.ceil(timeleft % 60)
                if minutes == 0 and seconds > 10:
                    msg = f'{seconds} second(s) remain!'
                elif minutes == 0 and seconds <= 10:
                    msg = f"{seconds} second(s) remain!"
                else:
                    msg = f'{minutes} minute(s), {seconds} seconds remain!'
                await self.send_message(msg)
                reminders.remove(timeleft)
            if loop.time() >= end_time:
                if beginmessage:
                    await self.send_message('Log study has finished.  Begin racing!')
                break
            await asyncio.sleep(.5)

    async def roll_game(self, preset_name, message, allow_quickswap=False):
        if await self.is_locked(message):
            return

        await self.send_message("Generating game, please wait.  If nothing happens after a minute, contact Synack.")
        try:
            seed, _ = await preset.get_preset(preset_name, randomizer='alttpr', spoilers="off", allow_quickswap=allow_quickswap)
        except preset.PresetNotFoundException as e:
            await self.send_message(str(e))
            return

        race_info = f"{preset_name} - {seed.url} - ({'/'.join(seed.code)})"
        if allow_quickswap:
            race_info += " - Quickswap Enabled"
        await self.set_raceinfo(race_info)
        await self.send_message(seed.url)
        await self.send_message("Seed rolling complete.  See race info for details.")
        self.seed_rolled = True
