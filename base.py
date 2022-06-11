from asyncio.windows_events import NULL
import json
from pickle import APPEND, TRUE
from urllib.request import urlopen
from pprint import pprint
from datetime import datetime, date, timedelta
import ctypes
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
import time
from RGBMatrixEmulator.adapters import ADAPTER_TYPES
from RGBMatrixEmulator.emulators.options import RGBMatrixEmulatorConfig
from PIL import Image
import re
from math import trunc

from numpy import append

matrix = RGBMatrix(options = RGBMatrixOptions())
canvas = matrix.CreateFrameCanvas()
colors_json = open('colors/teams.json')
team_colors = json.load(colors_json)

font_1 = graphics.Font()
font_2 = graphics.Font()
font_1.LoadFont("assets/fonts/patched/4x6.bdf")
font_2.LoadFont("assets/fonts/patched/5x7.bdf")
textColor = graphics.Color(255, 255, 255)

logo = "assets/wnba.png"
logo = Image.open(logo)
matrix.SetImage(logo.convert("RGB"))
time.sleep(4)
logo.close()

while True:    
    def _render_pregame(today_games):
        home_name = today_games['h']['ta']
        home_record = '(' + today_games['h']['re'] + ')'
        vis_name = today_games['v']['ta']
        vis_record = '(' + today_games['v']['re'] + ')'
        tip_time = (datetime.strptime(today_games['utctm'],"%H:%M") - timedelta(hours=5)).strftime("%#I:%M %p")
        game_location = today_games['ac'] + ', ' + today_games['as']
        home_text_Color = graphics.Color(team_colors[today_games['h']['ta']]["text"]["r"], team_colors[today_games['h']['ta']]["text"]["g"], team_colors[today_games['h']['ta']]["text"]["b"])
        vis_text_Color = graphics.Color(team_colors[today_games['v']['ta']]["text"]["r"], team_colors[today_games['v']['ta']]["text"]["g"], team_colors[today_games['v']['ta']]["text"]["b"])
        while True:
            for x in range(2,43):
                for y in range(0,8):
                    canvas.SetPixel(x, y, team_colors[today_games['h']['ta']]["banner"]["r"], team_colors[today_games['h']['ta']]["banner"]["g"], team_colors[today_games['h']['ta']]["banner"]["b"])
            for x in range(0,2):
                for y in range(0,8):
                    canvas.SetPixel(x, y, team_colors[today_games['h']['ta']]["accent"]["r"], team_colors[today_games['h']['ta']]["accent"]["g"], team_colors[today_games['h']['ta']]["accent"]["b"])
            for x in range(2,43):
                for y in range(9,17):
                    canvas.SetPixel(x, y, team_colors[today_games['v']['ta']]["banner"]["r"], team_colors[today_games['v']['ta']]["banner"]["g"], team_colors[today_games['v']['ta']]["banner"]["b"])
            for x in range(0,2):
                for y in range(9,17):
                    canvas.SetPixel(x, y, team_colors[today_games['v']['ta']]["accent"]["r"], team_colors[today_games['v']['ta']]["accent"]["g"], team_colors[today_games['v']['ta']]["accent"]["b"])
            graphics.DrawText(canvas, font_2, 3, 7, home_text_Color, home_name)
            graphics.DrawText(canvas, font_2, 3, 16, vis_text_Color, vis_name)
            graphics.DrawText(canvas, font_1, 19, 7, home_text_Color, home_record)
            graphics.DrawText(canvas, font_1, 19, 16, vis_text_Color, vis_record)
            graphics.DrawText(canvas, font_1, 1, 24, textColor, tip_time)
            graphics.DrawText(canvas, font_1, 1, 30, textColor, game_location)
            matrix.SwapOnVSync(canvas)
    

    def _render_game(today_games):
        home_name = today_games['hls']['ta']
        home_score = str(today_games['hls']['s'])
        vis_name = today_games['vls']['ta']
        vis_score = str(today_games['vls']['s'])
        quarter = 'Q' + str(today_games['p'])
        last_play_clock = today_games['lpla']['cl']
        try:
            last_play_clock = datetime.strptime(last_play_clock,"%M:%S.%f").strftime("%#S.%f")[:-5]
        except ValueError:
            last_play_clock = last_play_clock
        
        last_play_desc = re.sub(' : ',':',re.sub('(.*\] )','',re.sub(' +', ' ',today_games['lpla']['de'])))
        if len(last_play_desc) >= 15:
            last_play_desc_1 = last_play_desc[:15] + '-'
            last_play_desc_2 = last_play_desc[15:]
        else:
            last_play_desc_1 = last_play_desc
            last_play_desc_2 = ''
        home_text_Color = graphics.Color(team_colors[today_games['hls']['ta']]["text"]["r"], team_colors[today_games['hls']['ta']]["text"]["g"], team_colors[today_games['hls']['ta']]["text"]["b"])
        vis_text_Color = graphics.Color(team_colors[today_games['vls']['ta']]["text"]["r"], team_colors[today_games['vls']['ta']]["text"]["g"], team_colors[today_games['vls']['ta']]["text"]["b"])
        for x in range(2,31):
            for y in range(0,8):
                canvas.SetPixel(x, y, team_colors[today_games['hls']['ta']]["banner"]["r"], team_colors[today_games['hls']['ta']]["banner"]["g"], team_colors[today_games['hls']['ta']]["banner"]["b"])
        for x in range(0,2):
            for y in range(0,8):
                canvas.SetPixel(x, y, team_colors[today_games['hls']['ta']]["accent"]["r"], team_colors[today_games['hls']['ta']]["accent"]["g"], team_colors[today_games['hls']['ta']]["accent"]["b"])
        for x in range(2,31):
            for y in range(9,17):
                canvas.SetPixel(x, y, team_colors[today_games['vls']['ta']]["banner"]["r"], team_colors[today_games['vls']['ta']]["banner"]["g"], team_colors[today_games['vls']['ta']]["banner"]["b"])
        for x in range(0,2):
            for y in range(9,17):
                canvas.SetPixel(x, y, team_colors[today_games['vls']['ta']]["accent"]["r"], team_colors[today_games['vls']['ta']]["accent"]["g"], team_colors[today_games['vls']['ta']]["accent"]["b"])
        if (int(today_games['hls']['ftout'])) >= 1:
            for x in range(35,36):
                for y in range(2,2 + int(today_games['vls']['ftout'])):
                    canvas.SetPixel(x, y, 255, 255, 0)
        if (int(today_games['vls']['ftout'])) >= 1:
            for x in range(35,36):
                for y in range(11,11 + int(today_games['vls']['ftout'])):
                    canvas.SetPixel(x, y, 255, 255, 0)
        
        score_x = 21
        if int(today_games['hls']['s']) >= 100 or int(today_games['hls']['s']) >= 100:
            score_x = 19

        graphics.DrawText(canvas, font_2, 3, 7, home_text_Color, home_name)
        graphics.DrawText(canvas, font_2, 3, 16, vis_text_Color, vis_name)
        graphics.DrawText(canvas, font_1, score_x, 7, home_text_Color, home_score)
        graphics.DrawText(canvas, font_1, score_x, 16, vis_text_Color, vis_score)
        graphics.DrawText(canvas, font_1, 46, 12, textColor, quarter)
        graphics.DrawText(canvas, font_1, 40, 6, textColor, last_play_clock)
        graphics.DrawText(canvas, font_1, 1, 23, textColor, last_play_desc_1)
        graphics.DrawText(canvas, font_1, 1, 31, textColor, last_play_desc_2)
        matrix.SwapOnVSync(canvas)

    def _render_postgame(today_games):
        home_name = today_games['h']['ta']
        home_record = '(' + today_games['h']['re'] + ')'
        home_score = today_games['h']['s']
        vis_name = today_games['v']['ta']
        vis_record = '(' + today_games['v']['re'] + ')'
        vis_score = today_games['v']['s']
        home_text_Color = graphics.Color(team_colors[today_games['h']['ta']]["text"]["r"], team_colors[today_games['h']['ta']]["text"]["g"], team_colors[today_games['h']['ta']]["text"]["b"])
        vis_text_Color = graphics.Color(team_colors[today_games['v']['ta']]["text"]["r"], team_colors[today_games['v']['ta']]["text"]["g"], team_colors[today_games['v']['ta']]["text"]["b"])
        while True:
            for x in range(2,64):
                for y in range(0,8):
                    canvas.SetPixel(x, y, team_colors[today_games['h']['ta']]["banner"]["r"], team_colors[today_games['h']['ta']]["banner"]["g"], team_colors[today_games['h']['ta']]["banner"]["b"])
            for x in range(0,2):
                for y in range(0,8):
                    canvas.SetPixel(x, y, team_colors[today_games['h']['ta']]["accent"]["r"], team_colors[today_games['h']['ta']]["accent"]["g"], team_colors[today_games['h']['ta']]["accent"]["b"])
            for x in range(2,64):
                for y in range(9,17):
                    canvas.SetPixel(x, y, team_colors[today_games['v']['ta']]["banner"]["r"], team_colors[today_games['v']['ta']]["banner"]["g"], team_colors[today_games['v']['ta']]["banner"]["b"])
            for x in range(0,2):
                for y in range(9,17):
                    canvas.SetPixel(x, y, team_colors[today_games['v']['ta']]["accent"]["r"], team_colors[today_games['v']['ta']]["accent"]["g"], team_colors[today_games['v']['ta']]["accent"]["b"])
            graphics.DrawText(canvas, font_2, 3, 7, home_text_Color, home_name)
            graphics.DrawText(canvas, font_2, 3, 16, vis_text_Color, vis_name)
            graphics.DrawText(canvas, font_1, 19, 7, home_text_Color, home_record)
            graphics.DrawText(canvas, font_1, 19, 16, vis_text_Color, vis_record)
            graphics.DrawText(canvas, font_1, 55, 7, home_text_Color, home_score)
            graphics.DrawText(canvas, font_1, 55, 16, vis_text_Color, vis_score)
            graphics.DrawText(canvas, font_1, 1, 24, textColor, "Final")
            matrix.SwapOnVSync(canvas)

    def _render_no_games():
        home_name = 'Sorry, no games today :('
        graphics.DrawText(canvas, font_1, 2, 7, textColor, home_name)
        matrix.SwapOnVSync(canvas)
        time.sleep(10)

    def _get_game_detail(game_id):
        game_id = "".join(game_id)
        url = "https://data.wnba.com/data/10s/v2015/json/mobile_teams/wnba/2022/scores/gamedetail/" + game_id + "_gamedetail.json"
        response = urlopen(url)
        game_detail = json.loads(response.read())['g']
        return game_detail

    ## Pull In Schedule For Given Day
    date_today = date.today().strftime("%Y-%m-%d")
    url = "https://data.wnba.com/data/5s/v2015/json/mobile_teams/wnba/2022/league/10_full_schedule.json"
    response = urlopen(url)
    data_json = json.loads(response.read())

    all_games = []

    league_schedule = data_json["lscd"]
    for month in league_schedule:
        month_schedule = month['mscd']
        for game in month_schedule['g']:
            all_games.append(game)

    today_games = [x for x in all_games if (x['gdte'] == date_today)]
    preference_games = [x for x in all_games if (x['gdte'] == date_today) and (x['h']['ta'] == 'MIN')]

    if (len(preference_games) == 1):
        game_id = preference_games[0]['gid']
        live_game = _get_game_detail(game_id)

    canvas.Clear()
    if len(preference_games) == 1:
        if (live_game['hls']['s'] == '' and live_game['vls']['s'] == ''):
            _render_pregame(preference_games[0])
        else:
            if (preference_games[0]['stt'] != 'Final'):
                while True:
                    game_id = preference_games[0]['gid']
                    live_game = _get_game_detail(game_id)
                    canvas.Clear()
                    _render_game(live_game)
                    time.sleep(10)
            else:
                canvas.Clear()
                _render_postgame(preference_games[0])

    else:
        if (len(today_games) >= 1):
            today_game_ids = []
            live_game_ids = []
            not_live_game_ids = []
            for g in today_games:
                append_this = [str(g['gid'])]
                today_game_ids.append(append_this)
            for l in 0,len(today_game_ids)-1:
                live_game = _get_game_detail(today_game_ids[l])
                if ((live_game['hls']['s'] != '0' and live_game['vls']['s'] != '0') and live_game['stt'] != 'Final'):
                    live_game_ids.append(today_game_ids[l])
                else:
                    not_live_game_ids.append(today_game_ids[l])

                if len(live_game_ids) >= 1:
                    #Loop trhough live games
                    for l_1 in live_game_ids:
                        live_game = _get_game_detail(l_1)
                        _render_game(live_game)
                        time.sleep(10)
                else:
                    #Loop through final and pregame games
                    for l_2 in not_live_game_ids:
                        live_game = _get_game_detail(l_2)
                        
                        if (live_game['stt'] != 'Final'):
                            pregame_game = [x for x in all_games if (x['gid'] == "".join(l_2))]
                            _render_pregame(pregame_game[0])
                        
                        if (live_game['stt'] == 'Final'):
                            _render_postgame(live_game)
                        
                        time.sleep(10)
        
        else:
            _render_no_games()
    
    time.sleep(3)