import remote_db
import local_db
import shared as s
# import re
from datetime import datetime

def string_is_date(str):
    #test_str = '04-01-1997'
    # pattern_str = r'^\d{4}-\d{2}-\d{2}$'
    # if re.match(pattern_str, str):
    #     return True
    # else:
    #     return False
    format = "%Y-%m-%d"
    res = True
    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(str, format))
    except ValueError:
        res = False
    return res

def string_is_time(str):
    # test_str = '00:00:00'
    pattern_str = r'^\d{2}:\d{2}:\d{2}.\d{2}:\d{2}$'
    if re.match(pattern_str, str):
        return True
    else:
        return False

# Double the single quotes. ' becomes '' in strings before being put into queries.
def double_single_quotes(chaine):
    if chaine != None:
        return chaine.replace("'", "''")
    else:
        return None

#
# def load_teams_from_local_db():
#     ret = local_db.conn.execute("SELECT idTeam,strTeam FROM teams")
#     for dict_team_names

def get_all_sports():
    s.all_sports = remote_db.call_thesportsdb(remote_db.thesportsdb.sports.allSports)
    # all_sports = thesportsdb.sports.allSports()
    # print(all_sports)
    local_db.conn.execute("TRUNCATE TABLE sports")
    for sport in s.all_sports["sports"]:
        print(sport)
        chaine = "INSERT INTO sports (idSport, strSport, strFormat, strSportDescription) VALUES(?,?,?,?)"
        args = ( \
            sport["idSport"], \
            sport["strSport"], \
            sport["strFormat"], \
            sport["strSportDescription"] \
            )
        local_db.execute_and_commit_query(chaine, args)
    # return s.all_sports

# Returns a list of league ids
def get_all_leagues():
    list_leagues = []
    s.all_leagues = remote_db.call_thesportsdb(remote_db.thesportsdb.leagues.allLeagues)
    # thesportsdb.leagues.allLeagues()
    #print(all_leagues)
    for league in s.all_leagues['leagues']:
        # if league['strSport'] == "Basketball":
        # if league['strSport'] == "Soccer":
        s.list_leagues.append(league["idLeague"])
        #dict_leagues[""]

        # La table des sports contient ESports et non Esports !!!
        if league["strSport"] == "Esports":
            league["strSport"] = "ESports"
        if league["strSport"] == "Olympics":
            league["strSport"] = "Multi Sports"
        if league["strSport"] == "MotorSport":
            league["strSport"] = "Motorsport"

        # print(league["idLeague"])
        chaine = "INSERT INTO leagues (idLeague, strLeague, idSport, strLeagueAlternate) SELECT ?,?,?,? " \
                 "WHERE NOT EXISTS (SELECT 1 FROM leagues WHERE idLeague = ?)"
        args = ( \
                league["idLeague"], \
                double_single_quotes(league["strLeague"]), \
                s.dict_sports_by_name[league["strSport"]], \
                double_single_quotes(league["strLeagueAlternate"]), \
                \
                league["idLeague"], \
              )
        local_db.execute_and_commit_query(chaine, args)
        # local_db
        # local_db.conn.execute(chaine, args)
        # local_db.conn.commit()
    # s.list_leagues = list_leagues
    return list_leagues

############################
# All seasons for a league #
############################

# Used by get_all_events_for_league()

def get_all_seasons_for_league(league_id):
    # delete previous entries so that insert into neer fails.
    chaine_delete_previous_entries = "DELETE FROM league_seasons WHERE idLeague = " + str(league_id)
    local_db.execute_and_commit_query(chaine_delete_previous_entries)

    all = remote_db.call_thesportsdb(remote_db.thesportsdb.leagues.allLeagueSeasons,[league_id])
    list_seasons_for_league = []
    chaine_list_of_seasons = ""
    if all["seasons"] != None:
        for item in all["seasons"]:
            list_seasons_for_league.append(item["strSeason"])
            chaine_list_of_seasons = chaine_list_of_seasons + "(" + str(league_id) +",'" + item["strSeason"] + "'),"
        # print(chaine_list_of_seasons)
        if len(chaine_list_of_seasons) > 0:
            chaine_list_of_seasons = chaine_list_of_seasons[:-1]
            chaine = "INSERT INTO league_seasons (idLeague, strSeason) VALUES " + chaine_list_of_seasons + ""
            local_db.execute_and_commit_query(chaine)
        # print(all)
        pass
    else:
        print("")
    return list_seasons_for_league

############################
# All events for a league #
############################

# Returns
def get_all_events_for_league(league_id):

    list_seasons_for_league = get_all_seasons_for_league(league_id)

    for season in list_seasons_for_league:
        # print(season)

        ######################################
        # All event in a league and a season #
        ######################################

        # All events from a league and a season

        # delete previous entries so that insert into neer fails.
        chaine_delete_previous_entries = "DELETE FROM events WHERE idLeague = " + str(league_id) + " AND strSeason ='" + season + "'"
        local_db.execute_and_commit_query(chaine_delete_previous_entries)

        all = remote_db.call_thesportsdb(remote_db.thesportsdb.events.leagueSeasonEvents, [league_id, season])
        # print(all["events"])

        chaine_list_teams = ""
        chaine_list_data = ""
        compteur_items = 0
        compteur_remaining_items = len(all["events"])
        # if compteur_remaining_items >= 1000:
        #     print (compteur_remaining_items)
        for item in all["events"]:
            strEvent_modified = double_single_quotes(item["strEvent"])
            # print(item["strTime"])
            # Time (what if it goes wrong?)
            # if item["strTime"] == None:
            #     strTime = "00:00:00"
            # elif string_is_time(item["strTime"]):
            #     strTime = item["strTime"]
            # else:
            #     strTime !!!!!!!= "00:00:00"
            strTime = "00:00:00"

            # Date (what if it goes wrong?)
            if item["dateEvent"] == None:
                strDateEvent = "1970-01-01"
            elif string_is_date(item["dateEvent"]):
                strDateEvent = item["dateEvent"]
            else:
                strDateEvent = "1970-01-01"

            # dat = str(item["dateEvent"])
            # dat = "2020-10-13T20:13:12"
            dat = strDateEvent + "T" + strTime #00:00:00" # On n'a pas le time en fait !
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

            # idHomeTeam sometimes is equal to None...
            if item["idHomeTeam"] == None:
                idHomeTeam = 0
                strHomeTeam = ""
            else:
                idHomeTeam = item["idHomeTeam"]
                strHomeTeam = item["strHomeTeam"]
            if item["idAwayTeam"] == None:
                idAwayTeam = 0
                strAwayTeam = ""
            else:
                idAwayTeam = item["idAwayTeam"]
                strAwayTeam = item["strAwayTeam"]

            if not idHomeTeam in s.dict_team_names:
                s.dict_team_names[idHomeTeam] = {'strTeam' : strHomeTeam}
                chaine_list_teams = chaine_list_teams + "(" + str(idHomeTeam) + ",'" + double_single_quotes(strHomeTeam) + "'),"
            if not idAwayTeam in s.dict_team_names:
                s.dict_team_names[idAwayTeam] = {'strTeam' : strAwayTeam}
                chaine_list_teams = chaine_list_teams + "(" + str(idAwayTeam) + ",'" + double_single_quotes(strAwayTeam) + "'),"

            compteur_items += 1
            chaine_list_data = chaine_list_data + "(" + str(item["idEvent"]) + "," + str(league_id) + ",\'" + season + "\',\'" + dat   \
                               + "\',\'" + strEvent_modified + "\'," + str(idHomeTeam) + "," + str(idAwayTeam) \
                               + "," + str(intHomeScore) + "," + str(intAwayScore) + "," + str(score_available) +"),"
            # print(chaine_list_data)

            if compteur_items == 1000 or compteur_items == compteur_remaining_items:
                compteur_remaining_items = compteur_remaining_items - compteur_items
                compteur_items = 0
                # Insertion des nouvelles équipes dans la table teams
                if len(chaine_list_teams) > 0:
                    chaine_list_teams = chaine_list_teams[:-1]
                    chaine = "INSERT INTO teams (idTeam,strTeam) VALUES " + chaine_list_teams
                    local_db.execute_and_commit_query(chaine)
                    chaine_list_teams = ""

                if len(chaine_list_data) > 0:
                    chaine_list_data = chaine_list_data[:-1]
                    chaine = "INSERT INTO events (idEvent,idLeague,strSeason,dat,strEvent,idHomeTeam,idAwayTeam,intHomeScore,intAwayScore,scoreAvailable) VALUES " + chaine_list_data + ""
                    local_db.execute_and_commit_query(chaine)
                    chaine_list_data = ""
                # print(all)

        print(str(len(all["events"])) + " events added for league " + str(league_id) + " and season " +  season)

        pass

        # for item in all["events"]:
        #     chaine_list_of_seasons = chaine_list_of_seasons + "(" + str(league_id) + ",'" + item["strSeason"] + "'),"
        #     chaine = "INSERT INTO events (idEvent,idLeague,strSeason,strEvent,idHomeTeam,idAwayTeam,dat,intHomeScore,intAwayScore) VALUES " + chaine_list_of_seasons + ""
        #     print(item)
        # pass

pass