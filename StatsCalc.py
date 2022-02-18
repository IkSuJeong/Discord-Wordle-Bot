import pandas as pd
import numpy as np
import json
from plotnine import ggplot, aes, geom_boxplot, theme, xlab, ylab, ggtitle, labs, scale_fill_manual
from HTML_Writer import Writer

class UserStats:
    def inputID(self, discord_id, author):
        with open('storage.json', mode = 'r') as file:
            storage = json.load(file)
        self.df = storage[str(discord_id)]
        self.tries = np.array([x if x != 'X' else np.NaN for x in self.df['tries']])
        self.author = author
        
    def getMean(self):
        lst = self.tries
        count = 0
        try:
            while True:
                lst.remove(np.NaN)
                count += 1
        except:
            pass
        mean = np.ma.array(lst, mask = np.isnan(lst)).mean()
        std = np.ma.array(lst, mask = np.isnan(lst)).std()
    
        return f'Average Amount of Tries Needed: {mean:.1f} ± {std:.1f}\n            Incomplete Wordles: {count}'

    def getBoxPlots(self):
        final_df = []
        for idx, line in enumerate(list(self.df.keys())[1:]):
            colordict = self.df[line]
            colordf = pd.DataFrame.from_dict(colordict)
            colordf['index'] = idx + 1
            colordf = pd.melt(colordf, id_vars = ['index'], value_vars = ['Green', 'Yellow', 'Black'])
            
            final_df.append(colordf)
            
        final_df = pd.concat(final_df)
        final_df['value'] = [x if x != 'X' else np.NaN for x in final_df['value']]
        graph = ggplot(final_df) \
        + aes(x = 'factor(index)', y = 'value', fill = 'variable') \
        + geom_boxplot(position = 'dodge2') + theme(figure_size = (10, 5)) \
        + xlab('Line') + ylab('Guess Distribution') + ggtitle(f'{self.author}\'s Guesses Color Distribution') \
        + labs(fill = 'Guess Color') + scale_fill_manual(values = ['#3a3a3c', '#538d4e', '#b59f3b'])
        
        graph.save('boxplot')
        
    def wordle_summary(self):
        tries = [x if str(x) != 'nan' else 'X' for x in self.tries]
        writer = Writer(list(tries))
        writer.writeHTML()
  

if __name__ == '__main__':
    temp = UserStats()
    temp.inputID('TOKEN-HERE', 'ih')
    name = 'hi'
    print(temp.getMean())
    temp.getBoxPlots()
    temp.wordle_summary()
    
