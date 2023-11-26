import thesportsdb
import time

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


