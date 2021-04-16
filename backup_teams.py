import vexdb as v
import json, os, errno

# https://stackoverflow.com/a/23794010
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

teams = v.getTeams(get_all=True)
# teams = v.getTeams(team="SQL")

with safe_open_w("./teams.json") as f:
    f.write(json.dumps(teams))
    f.close()

for team in teams:
    print(f"{team['number']} {team['team_name']}")
    result = {}
    result["team"] = team
    this_no = team["number"]
    result["events"] = v.getEvents(team=this_no, get_all=True)
    result["matches"] = v.getMatches(team=this_no, get_all=True)
    result["rankings"] = v.getRankings(team=this_no, get_all=True)
    result["season_rankings"] = v.getSeasonRankings(team=this_no, get_all=True)
    result["awards"] = v.getAwards(team=this_no, get_all=True)
    result["skills"] = v.getSkills(team=this_no, get_all=True)
    with safe_open_w(f"teams/{this_no}.json") as f:
        f.write(json.dumps(result))
        f.close()

