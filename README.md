# BoardGameGeek Scraper and Recommender - README

### bgg_title_scraper.py

This should be run first.

This script goes through the top 10,000 games on boardgamegeek.com, sorted according to their "Geek Rating", which is calculated using a form of Bayesian averaging. For each game, the fields taken by this script are:
- Title,
- Geek Rating,
- URL of the game's individual page on boardgamegeek.com.

The data for each game is appended to a dataframe, which is then written to a .csv file at the end of the script (bgg_titles.csv).

The motivation for running this script before the bgg_main_scraper.py script is that the main scraper is much slower (it will pull data on approximately 1,000 games every hour). In this time, there is potential for games to change their ranking and consequently be included twice or missed by the scraper. For example, the games are listed on BoardGameGeek in pages of 100 each. If game X was at one point ranked number 1000, it would be included at the bottom of page 10. But while the script is working its way through page 10, game X's rank might change to 1001. It will then be at the top of page 11 when this is opened by the script, and so will be included twice in the final dataset. The probability of the above happening within the timeframe of the title scraper is negligible, and additionally, the bgg_titles.csv file can be checked to hold no duplicates and quickly run again if necessary. The links in the bgg_titles.csv file will then be used in bgg_main_scraper.py to scrape the data of each game.

### bgg_main_scraper.py

This should be run after bgg_title_scraper.py.

This script takes the 10,000 games from bgg_titles.csv and uses the "link" field to gather the following for each game:
- Minimum Player Number,
- Maximum Player Number,
- Weight (complexity),
- List of game designers,
- List of game categories,
- List of game mechanics,
- List of games which this game reimplements,
- List of games which reimplement this game.

The data for each game is appended to a dataframe, which is then written to a .csv file at the end of the script (bgg_data.csv).

### Board Game Recommender.ipynb

After you have collected the data, you can run this.

The majority of the notebook is cleaning the data. It then uses a CountVectorizer and cosine similarity to recommend games based on designers, categories and mechanics. The player counts are used to ensure compatibility (if someone asks for recommendations based on a game which has a maximum player count of 3, it is not a good idea to recommend a game which requires a minimum of 4 players). The reimplementation data is used as a basic way to prevent effectively the same game being recommended (e.g. Carcassonne -> Carcassonne: Winter Edition.)