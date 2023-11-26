# This is a sample Python script.

# Press F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import fn
import local_db
import shared as s

# import time
from itertools import chain

# thesportsdb.leagues.leagueSeasonTable("4328", "2019-2020")
# res = call_thesportsdb(thesportsdb.leagues.leagueSeasonTable,["4328", "2019-2020"])
# res = call_thesportsdb("""thesportsdb.leagues.leagueSeasonTable("4328", "2019-2020")""")
# res = call_thesportsdb(thesportsdb.leagues.leagueSeasonTable, ("4328", "2019-2020"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# NOTA
# I had to change API_KEY from "1" to "3" in settings.py in thesportsdb folder
# (in C:\Users\Nicolas\AppData\Local\Programs\Python\Python39\Lib\site-packages\thesportsdb)
# Before that, all requests were giving Error 404.
# NOTA

# ATTENTION
# L'API n'accepte que 100 requêtes par minute (2 par seconde max en fait).
# Il faut ralentir d'une manière ou d'une autre.
# ATTENTION

#thesportsdb.settings

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=DESKTOP-M2OA26Q;'
#                       'Database=Greyhound;'
#                       'Trusted_Connection=yes;')


# Populating sports table (from empty table, reset everytime)
if True:
    fn.get_all_sports()

s.dict_sports_by_id = local_db.get_dict_from_query("SELECT * FROM sports", 'idSport');
s.dict_team_names = local_db.get_dict_from_query("SELECT idTeam,strTeam FROM teams",'idTeam');

for idSport in s.dict_sports_by_id:
    sport = s.dict_sports_by_id[idSport]
    s.dict_sports_by_name[sport["strSport"]] = idSport

fn.get_all_leagues()

# t=get_list_from_query("tt")

# dict_sports_by_name = {}


# Get all leagues for a sport
if False:
    pass

# All countries
# all_countries = thesportsdb.countries.allCountries()
# print(all_countries)

for idSport in s.dict_sports_by_id:
    pass

for league_id in s.list_leagues:
    if int(league_id) < 4671: # 4380
        print(league_id)
        fn.get_all_events_for_league(league_id)
        pass
# league_id = 4337 # 4328

# event_ifo=thesportsdb.events.eventInfo("1008672")
# event_result=thesportsdb.events.eventResult("1008695")
# previous_events=thesportsdb.events.lastLeagueEvents("4328")
# events_for_league_season20192020=thesportsdb.events.leagueSeasonEvents("4328", "2019-2020")
# upcoming_soccer_events=thesportsdb.events.nextLeagueEvents("4328")
# all_countries=thesportsdb.countries.allCountries()
# all_leagues=thesportsdb.leagues.allLeagues()
# EPL_info=thesportsdb.leagues.leagueInfo("4328")
# EPL_standings=thesportsdb.leagues.leagueSeasonTable("4328", "2019-2020")
# soccer_leagues=thesportsdb.leagues.sportLeagues("102")
# Team_sports=thesportsdb.sports.TeamVsTeamSports()
# all_sports=thesportsdb.sports.allSports()
# nonTeamSports=thesportsdb.sports.nonTeamVsTeamSports()
# sport_details=thesportsdb.sports.sportInfo("102")
# EPL_teams=thesportsdb.teams.leagueTeams("4328")
# team_details_ManC=thesportsdb.teams.teamInfo("133613")
# ## print(thesportsdb)


