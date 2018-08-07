import json
import urllib2
import time

def etd(pl):
    if is_no_show_hours():
        return [{'contents': ''}]
    try:
        content = get_next_arrivals()
        return [{'contents': content}]
    except:
        return [{'contents': ''}]

def is_no_show_hours():
    hour = int(time.strftime('%H'))
    weekday = int(time.strftime('%w'))
    return (weekday is 0 or weekday is 6) or (hour >= 11 and hour <= 17)

def is_after_noon():
    hour = int(time.strftime('%H'))
    return hour >= 12

def get_next_arrivals():
    show = []
    if not is_after_noon():
        show.append(u'\uf0f7')
        show.append(wrap_get_etd('warm', 'daly', 'WARM'))
        show.append(wrap_get_etd('dbrk', 'mlbr', 'DBRK'))
    else:
        show.append(u'\ue617')
        warm = wrap_get_etd('civc', 'warm', 'WARM')
        if warm:
            show.append(warm)
        else:
            show.append(wrap_get_etd('civc', 'dubl', 'DUBL'))

        rich = wrap_get_etd('civc', 'rich', 'RICH')
        if rich:
            show.append(rich)
        else:
            show.append(wrap_get_etd('civc', 'antc', 'ANTC'))
            show.append(wrap_get_etd('civc', 'phil', 'PHIL'))
            show.append(wrap_get_etd('civc', 'pitt', 'PITT'))
            show.append(wrap_get_etd('civc', 'ncon', 'NCON'))
    return ' '.join([s for s in show if s])

def wrap_get_etd(orig, dest, pref):
    try:
        return get_etd(orig, dest, pref)
    except:
        return None

def get_etd(orig, dest, pref):
    url = 'https://api.bart.gov/api/etd.aspx'
    url += '?cmd=etd&key=MW9S-E7SL-26DU-VV8V&json=y'
    url += '&orig={}'.format(orig.upper())
    resp = json.load(urllib2.urlopen(url, timeout=1))

    dest = dest.upper()
    filt = lambda x: x['abbreviation'] == dest
    dest_etd = filter(filt, resp['root']['station'][0]['etd'])[0]

    get_time = lambda x: x['minutes']
    times = map(get_time, dest_etd['estimate'])
    times = filter(lambda x: x.isdigit(), times)
    times = map(int, times)

    first_two = map(str, sorted(times)[:2])

    return '{}:{}'.format(pref, ','.join(first_two))
