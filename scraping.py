import urllib2
import json


def build_url(function):
    url = "http://www.theyworkforyou.com/api/%s?key=%s&output=js" % (function, "F8cN3CG2CfGWHFPBpoAWfFcW")
    if function == 'getMPs':
        url += '&date=30-03-2015'
    return url


def parse_url_json(url):
    return json.loads(urllib2.urlopen(url).read().decode('iso-8859-1'))


def get_ids(position):
    return [member['person_id'] for member in parse_url_json(build_url('get%ss' % position))]


def get_members(position):
    ids = get_ids(position)

    return [parse_url_json(build_url('get%s' % position) + "&id=" + person_id) for person_id in ids]


def get_everything():
    global positions

    for position in positions:
        print json.dumps(get_members(position))


def read_everything():
    global positions
    people = {'people': {"mps": [], 'mlas': [], 'lords': [], 'msps': []}}

    for position in positions:
        with open('%ss.json' % position.lower()) as f:
            people['people'][position] = json.load(f)

    return people


positions = ['MSP']
people = read_everything()