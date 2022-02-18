import bs4 as BeautifulSoup
from html2image import Html2Image

class Writer:
    def __init__(self, df_guesses):
        guesses = ['X' if str(x) == 'X' else int(x) for x in df_guesses]
        played = len(guesses)
        win_percent = 100 - round(100 * guesses.count('X') / played)
        
        guess_string = ''.join(['Y' if x != 'X' else x for x in guesses])
        streak_list = guess_string.split('X')
        current_streak = len(streak_list[-1])
        max_streak = 0
        for streak in streak_list:
            streak_length = len(streak)
            max_streak = streak_length if streak_length > max_streak else max_streak
        
        dist = [0, 0, 0, 0, 0, 0]
        for i in range(1, 7):
            dist[i - 1] = guesses.count(i)
        
        self.distribution = dist
        self.player_stats = [played, win_percent, current_streak, max_streak]
        for i in reversed(guesses):
            if i != 'X':
                self.latest_guess = i
                break
        
    def writeHTML(self):
        style = '<link rel="stylesheet" href="styles.css">'
        mode = "<body class='nightmode vsc-initialized'>"
        stat_title = '<div class="container"><h1>Statistics</h1>'
        
        
        labels = ['Played', 'Win %', ' Current Streak', 'Max Streak']
        statistics = '<div id="statistics">'
        for i in range(4):
            statistics += '<div class="statistic-container">'
            statistics += f'<div class="statistic">{self.player_stats[i]}</div>'
            statistics += f'<div class="label">{labels[i]}</div>'
            statistics += '</div>'
        statistics += '</div>'
        
        
        guess_distribution_header = '<h1>Guess Distribution</h1>'
        distributions = '<div id="guess-distribution">'
        max_num = max(self.distribution)
        for i in range(1, 7):
            curr_num = self.distribution[i - 1]
            if curr_num == 0:
                percentage = '7'
            else:
                percentage = str(round(curr_num * 100 / max_num))
            
            if self.latest_guess == i:
                addHighlight = ' highlight'
            else:
                addHighlight = ''
            distributions += '<div class="graph-container">'
            distributions += f'<div class="guess">{i}</div>'
            distributions += '<div class="graph">'
            distributions += f'<div class="graph-bar align-right{addHighlight}" style="width: {percentage}%;">'
            distributions += f'<div class="num-guesses">{curr_num}</div>'
            distributions += '</div>'
            distributions += '</div>'
            distributions += '</div>'
        distributions += '</div>'
        
        ending = '<div class="footer"></div></div>'
            
            
            
        html_output = style + mode + stat_title + statistics + guess_distribution_header + distributions + ending
        html_file = open('index.html', 'w')
        html_file.write(html_output)
        html_file.close()
        
        hti = Html2Image()
        hti.screenshot(
            html_file = 'index.html', css_file='styles.css',
            save_as = 'wordle_basic.png', size = (350, 325)
        )
        
        

import json
import numpy as np
if __name__ == '__main__':
    with open('storage.json', mode = 'r') as file:
        storage = json.load(file)
    tries = list(np.array(storage[str(211960973253279744)]['tries']))
    #print(tries)
    writer = Writer(tries)
    writer.writeHTML()
            
            
        