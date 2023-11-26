
import pyodbc
from Tools.scripts.win_add2path import DEFAULT

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-M2OA26Q;'
                      'Database=thesportsDB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

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



def execute_and_commit_query(chaine, args = None):
    if args == None:
        conn.execute(chaine)
    else:
        conn.execute(chaine, args)
    conn.commit()


