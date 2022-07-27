import MeCab
import re
from collections import defaultdict

fullDict = tuple(open("./fulldict.txt", "r"))
abbrevs = tuple(open("./abbreviations.txt", "r"))
lookUp = defaultdict(list)
getPOS = defaultdict(set)
getAllPOS = defaultdict(set)
abbrevToMeaning = dict()
tagger = MeCab.Tagger()
katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ" 
ranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
  {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
  {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
  {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]
hir2kat = str.maketrans(hiragana_chart, katakana_chart)
kat2hir  =str.maketrans(katakana_chart, hiragana_chart)

for line in abbrevs:
  splitted = line.split('\t', 1)
  splitted = [split.strip() for split in splitted]
  abbrevToMeaning[splitted[0]] = splitted[1]

for definition in fullDict:
  definition = definition.strip()
  reading = re.search(r'\[(.*)\]', definition)

  pos = set(re.findall(r'\(([^\(\)]+)\)', definition))
  toAdd = set()
  for piece in pos:
    if ',' in piece:
      toAdd |= set(piece.split(','))
  pos |= toAdd
  pos = set(list(filter(lambda x: x in abbrevToMeaning, pos)))

  # # GOOD
  # kanjiKey = definition.split(' ', 1)[0].strip()
  # if definition not in lookUp[kanjiKey]:
  #   lookUp[kanjiKey].append(definition)
  #   getPOS[kanjiKey] |= pos
  
  # BAD
  if reading:
    readingKey = reading.group(1)
    kanjiKey = definition.split(' ', 1)[0].strip()
    katakanaKey = readingKey.translate(hir2kat)

    if definition not in lookUp[readingKey]:
      lookUp[readingKey].append(definition)
      getAllPOS[readingKey] |= pos
    if definition not in lookUp[kanjiKey]:
      lookUp[kanjiKey].append(definition)
      getPOS[kanjiKey] |= pos
    if katakanaKey and definition not in lookUp[katakanaKey]:
      lookUp[katakanaKey].append(definition)
      # getPOS[katakanaKey] |= pos
  else:
    key = definition.split(' ', 1)[0].strip()
    lookUp[key].append(definition)
    getPOS[key] |= pos

    tokens = tagger.parse(key).split('\n')
    numTokens = len(tokens) - 2
    theWord = ""
    for i in range(numTokens):
      token = list(filter(None, re.split('\t|,', tokens[i])))
      pronunciation = token[-2]
      surface = token[0]
      if pronunciation != '*':
        theWord += pronunciation
      else:
        theWord += surface
    katakanaKey = theWord

    if len(katakanaKey) > 0 and katakanaKey != key and definition not in lookUp[katakanaKey]:
      lookUp[katakanaKey].append(definition)
      getPOS[katakanaKey] |= pos

# print(lookUp['かわいい'])
getPOS['する'] = getPOS['為る']
lookUp['する'] = lookUp['為る']
dictEntries = sorted(lookUp.keys())

print(lookUp('示す'))