import pandas as pd
import numpy as np
import json
from plotnine import ggplot, aes, geom_boxplot, theme, xlab, ylab, ggtitle, labs, scale_fill_manual

class UserStats:
    def inputID(self, discord_id, author):
        with open('storage.json', mode = 'r') as file:
            storage = json.load(file)
    
        self.tries = np.array(storage[str(discord_id)]['tries'])
        self.df = storage[str(discord_id)]
        self.author = author
        
    def getMean(self):
        lst = self.tries
        count = 0
        try:
            while True:
                lst.remove('X')
                count += 1
        except:
            pass
        mean = np.ma.array(lst, mask = np.isnan(lst)).mean()
        std = np.ma.array(lst, mask = np.isnan(lst)).std()
    
        return f'Average Amount of Tries Needed: {mean:.1f} ± {std:.1f}            Incomplete Wordles: {count}'

    def getBoxPlots(self):
        final_df = []
        for idx, line in enumerate(list(self.df.keys())[1:]):
            colordict = self.df[line]
            colordf = pd.DataFrame.from_dict(colordict)
            colordf['index'] = idx + 1
            colordf = pd.melt(colordf, id_vars = ['index'], value_vars = ['Green', 'Yellow', 'Black'])
            
            final_df.append(colordf)
            
        final_df = pd.concat(final_df)
        graph = ggplot(final_df) \
        + aes(x = 'factor(index)', y = 'value', fill = 'variable') \
        + geom_boxplot(position = 'dodge2') + theme(figure_size = (10, 5)) \
        + xlab('Line') + ylab('Guess Distribution') + ggtitle(f'{self.author}\'s Guesses Color Distribution') \
        + labs(fill = 'Guess Color') + scale_fill_manual(values = ['#3a3a3c', '#538d4e', '#b59f3b'])
        
        graph.save('boxplot')
        
        

if __name__ == '__main__':
    temp = UserStats()
    temp.inputID('211960973253279744', 'ih')
    name = 'hi'
    print(temp.getMean())
    temp.getBoxPlots()
    
