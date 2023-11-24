# This is a sample Python script.

# Press F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
from itertools import chain

import thesportsdb

import pyodbc
from Tools.scripts.win_add2path import DEFAULT

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-M2OA26Q;'
                      'Database=thesportsDB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

def double_single_quotes(chaine):
    return chaine.replace("'", "''")

def execute_and_commit_query(chaine, args = None):
    if args == None:
        conn.execute(chaine)
    else:
        conn.execute(chaine, args)
    conn.commit()

def call_thesportsdb(fn, args = None):
    time.sleep(0.5) # Maximum 2 queries per second

    # if query_type == "sports.allSports":
    #     res = thesportsdb.sports.allSports()
    # elif query_type == "thesportsdb.leagues.allLeagues()"
    #     all_sports = thesportsdb.sports.allSports()

    if args == None:
        res = fn()
    else:
        res = fn(*args) #(params)
    # res = fn(params)

    return res

# thesportsdb.leagues.leagueSeasonTable("4328", "2019-2020")
res = call_thesportsdb(thesportsdb.leagues.leagueSeasonTable,["4328", "2019-2020"])
# res = call_thesportsdb("""thesportsdb.leagues.leagueSeasonTable("4328", "2019-2020")""")
# res = call_thesportsdb(thesportsdb.leagues.leagueSeasonTable, ("4328", "2019-2020"))

# Returns a list (with no key)
def get_list_from_query(chaine):
    result = cursor.execute(chaine)
    columns = [column[0] for column in cursor.description]
    list_results = []
    for row in cursor.fetchall():
        list_results.append(dict(zip(columns, row)))
    return list_results

# Returns a dict with the key being the one passed in parameter
def get_dict_from_query(chaine, key):
    list_results = get_list_from_query(chaine)
    dict_result = {}
    for item in list_results:
        id = item[key]
        del item[key]
        dict_result[id] = item
        pass
    return dict_result

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


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
    all_sports = call_thesportsdb(thesportsdb.sports.allSports)
    # all_sports = thesportsdb.sports.allSports()
    print(all_sports)
    conn.execute("TRUNCATE TABLE sports")
    for sport in all_sports["sports"]:
        print(sport)
        chaine = "INSERT INTO sports (idSport, strSport, strFormat, strSportDescription) VALUES(?,?,?,?)"
        args= ( \
                sport["idSport"], \
                sport["strSport"], \
                sport["strFormat"], \
                sport["strSportDescription"] \
              )
        execute_and_commit_query(chaine, args)
        # conn.execute(chaine, args)
        # conn.commit()


# while rows = cursor.fetchone()

# for row in result:
#     country = {}
#     for field_description in result.description:
#         field = field_description[0]
#         # country={}
#         country[field]=row[field]
#         pass
#         # ["print(field[0])
#     # print (row["strSport"])



# t=get_list_from_query("tt")

dict_sports_by_id = get_dict_from_query("SELECT * FROM sports", 'idSport');
dict_sports_by_name = {}

for idSport in dict_sports_by_id:
    sport = dict_sports_by_id[idSport]
    dict_sports_by_name[sport["strSport"]] = idSport

# Get all leagues for a sport
if False:
    list_leagues_for_this_sport = []
    all_leagues = call_thesportsdb(thesportsdb.leagues.allLeagues)
    # thesportsdb.leagues.allLeagues()
    #print(all_leagues)
    for league in all_leagues['leagues']:
        # if league['strSport'] == "Basketball":
        if league['strSport'] == "Soccer":
            list_leagues_for_this_sport.append(league)
            #dict_leagues[""]
            chaine = "INSERT INTO leagues (idLeague, strLeague, idSport, strLeagueAlternate) SELECT ?,?,?,? " \
                     "WHERE NOT EXISTS (SELECT 1 FROM leagues WHERE idLeague = ?)"
            args= ( \
                    league["idLeague"], \
                    double_single_quotes(league["strLeague"]), \
                    dict_sports_by_name[league["strSport"]], \
                    double_single_quotes(league["strLeagueAlternate"]), \
                    \
                    league["idLeague"], \
                  )
            execute_and_commit_query(chaine, args)
            conn.execute(chaine, args)
            conn.commit()

# All countries
# all_countries = thesportsdb.countries.allCountries()
# print(all_countries)


############################
# All seasons for a league #
############################
league_id = 4328

# delete previous entries so that insert into neer fails.
chaine_delete_previous_entries = "DELETE FROM league_seasons WHERE idLeague = " + str(league_id)
# conn.execute\
execute_and_commit_query(chaine_delete_previous_entries)

all = call_thesportsdb(thesportsdb.leagues.allLeagueSeasons,[league_id])
list_seasons_for_league = []
chaine_list_of_seasons = ""
for item in all["seasons"]:
    list_seasons_for_league.append(item["strSeason"])
    chaine_list_of_seasons = chaine_list_of_seasons + "(" + str(league_id) +",'" + item["strSeason"] + "'),"
print(chaine_list_of_seasons)
if len(chaine_list_of_seasons) > 0:
    chaine_list_of_seasons = chaine_list_of_seasons[:-1]
    chaine = "INSERT INTO league_seasons (idLeague, strSeason) VALUES " + chaine_list_of_seasons + ""
    execute_and_commit_query(chaine)
# print(all)
pass

for season in list_seasons_for_league:
    print(season)

    ######################################
    # All event in a league and a season #
    ######################################

    # All events from a league and a season

    # delete previous entries so that insert into neer fails.
    chaine_delete_previous_entries = "DELETE FROM events WHERE idLeague = " + str(league_id) + " AND strSeason ='" + season + "'"
    execute_and_commit_query(chaine_delete_previous_entries)

    all = call_thesportsdb(thesportsdb.events.leagueSeasonEvents, [league_id, season])
    print(all["events"])

    # list_data = []
    chaine_list_data = ""
    for item in all["events"]:
        test = ",\""
        #strEvent_modified = double_single_quotes(item["strEvent"])
        strEvent_modified = double_single_quotes(item["strEvent"])
        if item["strTime"] != None:
            pass
        # dat = str(item["dateEvent"])
        # dat = "2020-10-13T20:13:12"
        dat = item["dateEvent"] + "T00:00:00" # On n'a pas le time en fait !
        season = item["strSeason"]
        intHomeScore = item["intHomeScore"]
        intAwayScore = item["intAwayScore"]
        score_available = 1
        DEFAULT_VALUE_FOR_UNKNOWN_SCORE = 29999
        if intHomeScore == None:
            intHomeScore = DEFAULT_VALUE_FOR_UNKNOWN_SCORE
            score_available = 0
        if intAwayScore == None:
            intAwayScore = DEFAULT_VALUE_FOR_UNKNOWN_SCORE
            score_available = 0
        if intHomeScore == DEFAULT_VALUE_FOR_UNKNOWN_SCORE and intAwayScore == None:
            pass
        # season = "2002-'2023"
        chaine_list_data = chaine_list_data + "(" + str(item["idEvent"]) + "," + str(league_id) + ",\'" + season + "\',\'" + dat   \
                           + "\',\'" + strEvent_modified + "\'," + str(item["idHomeTeam"]) + "," + str(item["idAwayTeam"]) \
                           + "," + str(intHomeScore) + "," + str(intAwayScore) + "," + str(score_available) +"),"
    print(chaine_list_data)
    if len(chaine_list_data) > 0:
        chaine_list_data = chaine_list_data[:-1]
        chaine = "INSERT INTO events (idEvent,idLeague,strSeason,dat,strEvent,idHomeTeam,idAwayTeam,intHomeScore,intAwayScore,scoreAvailable) VALUES " + chaine_list_data + ""
        execute_and_commit_query(chaine)
    # print(all)
    pass

    # for item in all["events"]:
    #     chaine_list_of_seasons = chaine_list_of_seasons + "(" + str(league_id) + ",'" + item["strSeason"] + "'),"
    #     chaine = "INSERT INTO events (idEvent,idLeague,strSeason,strEvent,idHomeTeam,idAwayTeam,dat,intHomeScore,intAwayScore) VALUES " + chaine_list_of_seasons + ""
    #     print(item)
    # pass

pass
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


