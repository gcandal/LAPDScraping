import urllib2
import json
import codecs

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
    #positions = ['MSP', 'Lord', 'MP', 'MLA']
    positions = ['MLA']

    for position in positions:
        with open('teste.json', 'w') as f:
            members = get_members(position)
            print json.dumps(members)
            f.write(json.dumps(members))
            f.close()


def read_everything():
    #positions = ['MSP', 'Lord', 'MP', 'MLA']
    positions = ['Lord', 'MSP', 'MLA']

    people = {'people': {"mps": [], 'mlas': [], 'lords': [], 'msps': []}}

    for position in positions:
        with open('%ss.json' % position.lower()) as f:
            people['people'][position] = json.load(f)

    return people


def write_person_debates(person, f):
    f.write('\t\t<Debates>\n')
    f.write('\t\t</Debates>\n')


def write_person_memberships(person, f):
    for membership in person:
        f.write('\t\t<Membership id="%s">\n' % membership['member_id'])
        f.write('\t\t\t<Party>%s</Party>\n' % membership['party'])
        f.write('\t\t\t<Constituency>%s</Constituency>\n' % membership['party'])
        f.write('\t\t\t<Title>%s</Title>\n' % membership['title'])
        f.write('\t\t\t<EnteredHouse>%s</EnteredHouse>\n' % filter_date(membership['entered_house']))
        f.write('\t\t\t<LeftHouse>%s</LeftHouse>\n' % membership['left_house'])
        f.write('\t\t\t<EnteredReason>%s</EnteredReason>\n' % membership['entered_reason'])
        f.write('\t\t\t<LeftReason>%s</LeftReason>\n' % filter_date(membership['left_reason']))
        f.write('\t\t</Membership>\n')


def write_person_details(person, f):
    f.write('\t\t<Name>%s</Name>\n' % person[0]['full_name'])
    write_person_debates(person, f)
    write_person_memberships(person, f)


def write_person(people, f, type):
    for person in people['people'][type]:
        f.write('\t<%s id="%s">\n' % (type, person[0]['person_id']))
        write_person_details(person, f)
        f.write('\t</%s>\n' % type)


def write_xml(people, filename):
    positions = ['Lord', 'MSP', 'MLA']

    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<Westminster xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n\txsi:noNamespaceSchemaLocation="Westminster.xsd">\n')
        for position in positions:
            write_person(people, f, position)
        f.write('</Westminster>\n')
        f.close()


def filter_date(date):
    if date[4:] == '-00-00':
        return date[:4] + '-01-01'
    else:
        return date


#get_everything()
write_xml(read_everything(), 'Westminster.xml')
