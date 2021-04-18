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

# get a list of all events
# events = v.getEvents(region="West Virginia", season="Tower Takeover")
# events = v.getEvents(sku="RE-VRC-19-9747")
events = v.getEvents(get_all=True)

with safe_open_w("events/events.json") as f:
    f.write(json.dumps(events))
    f.close()

for event in events:
    print(event["name"])
    result = {}
    result["event"] = event
    this_sku = event["sku"]
    result["matches"] = v.getMatches(sku=this_sku, get_all=True)
    result["rankings"] = v.getRankings(sku=this_sku, get_all=True)
    result["skills"] = v.getSkills(sku=this_sku, get_all=True)
    result["awards"] = v.getAwards(sku=this_sku, get_all=True)
    filename = f"events/{event['program']}/{event['season']}/{this_sku}.json"
    with safe_open_w(filename) as f:
        f.write(json.dumps(result))
        f.close()
