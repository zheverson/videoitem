brands = {'Bobbi Brown', 'Chanel', 'Clinique', 'Cover FX', 'Cover Girl', 'It Cosmetics', 'Jordana', 'LA Girl',
          'Lime Crime', 'LOreal', 'MAC', 'Makeup For Ever', 'Maybelline', 'Milani', 'Physicians Formula', 'Too Faced',
          'Makeup Geek', 'Nars', 'Nugg', 'NYX', 'Real Techniques', 'Revlon', 'Rimmel', 'Sigma', 'Urban Decay',
          'Wet and Wild', 'ELF', 'NYC'
          }

categories = {
    "lip",
    "powder",
    "concealer",
    "contourstick",
    "blush",
    "spray",
    "mist",
    "bronzer",
    "gloss",
    "palette",
    "nailpolish",
    "eyeshadow",
    "foundation",
    "brush",
    "mascara",
    "cream",
    "pen",
    "primer",
    "pigment",
    "cleanser",
    "eyeliner"
}

brandslower = {''.join(i.split(' ')).lower() for i in brands}

data = []

desc = re.finditer(r'(.+?)\n{2,}', c, re.S)
for i in desc:
    p = re.finditer(r'(.+?)\n', i.group(1), re.S)
    try:
        wordsrow = ''.join(re.split('[\W]', next(p).group(1).lower()))
        if not any((word in wordsrow for word in {'items', 'products'})):
            continue
        else:
            for j in p:
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
