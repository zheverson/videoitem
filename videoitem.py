import youtube_dl
import json
from brain import brandslower, categories
import re
from scrapeinfo import getupc, getpinimage


def start(csvpath):
    creatorurls = geturls(csvpath)

    for i in creatorurls:
        for j in i['urls']:
            downloadvideo(i['creator'], j)
            itemsinfo, videodict = getitems("~/youtube/{}/{}/*.json".format(i['creator'], j), {'url': j})
            items_with_upc = getupc(itemsinfo, 1.5)
            items_with_image = getpinimage(items_with_upc, 1.5)
            break
    return videodict, items_with_image


def geturls(filepath):
    data = []
    with open(filepath, 'r') as file:
        for row in file:
            array = row.split(',')
            [data.append({'creator': i, 'urls': []}) for i in array if i != '' and i != '\n']
            break

        for row in file:
            array = row.split(',')
            for index, i in enumerate(array):
                if i != '' and i != '\n':
                    data[index]['urls'].append(i)
    return data


def downloadvideo(creator, url):
    ydl_opts = {
        'writeinfojson': True,
        'writeautomaticsub': True,
        'outtmpl': 'youtube/{}/{}/{}.%(ext)s'.format(creator, url)
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def getitems(jsonfile, videodict):
    descjson = json.load(open(jsonfile))
    videodict.update({'title': descjson['title'], 'thumbnail': descjson['thumbnail']})
    desc = descjson['desc']
    data = []
    section = re.finditer(r'(.+?)\n{2,}', desc, re.S)
    for i in section:
        line = re.finditer(r'(.+?)\n', i.group(1), re.S)
        try:
            words = ''.join(re.split('[\W]', next(line).group(1).lower()))
            if not any((word in words for word in {'items', 'products'})):
                continue
            else:
                for j in line:
                    row = ''.join(re.split('[\W]', j.group(1).lower()))
                    try:
                        brand = next((word for word in brandslower if word in row))
                        try:
                            category = next((cat for cat in categories if cat in row))
                            data.append({'brand': brand, 'category': category, 'name': j.group(1)})
                        except StopIteration:
                            data.append({'brand': brand, 'name': j.group(1)})
                    except StopIteration:
                        try:
                            category = next((cat for cat in categories if cat in row))
                            data.append({'category': category, 'name': j.group(1)})
                        except StopIteration:
                            data.append({'name': j.group(1)})
        except StopIteration:
            pass
    return data, videodict
