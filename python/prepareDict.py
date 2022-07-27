import re
from collections import defaultdict
import MeCab
tagger = MeCab.Tagger()
# dict with key as reading and kanji and value as full definition

words = tuple(open("./fulldict.txt", "r"))
lookUp = defaultdict(list)
readingToDefinitions = defaultdict(set)
definitionToReadings = defaultdict(set)
getPOS = defaultdict(set)
katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ" 
hir2kat = str.maketrans(hiragana_chart, katakana_chart)
kat2hir  = str.maketrans(katakana_chart, hiragana_chart)
abbrevToMeaning = dict()
# print(string.translate(kat2hir))

abbrevs = tuple(open("./abbreviations.txt", "r"))

for line in abbrevs:
  splitted = line.split('\t', 1)
  splitted = [split.strip() for split in splitted]
  abbrevToMeaning[splitted[0]] = splitted[1]
  # print(splitted)

for definition in words:
  definition = definition.strip()
  reading = re.search(r'\[(.*)\]', definition)
  definitionOnly = re.search(r'\/(.+)\/', definition)
  if definitionOnly:
    definitionOnly = definitionOnly.group(1)
  # if definitionOnly:
  #   print(f"definitionOnly: {definitionOnly.group(1)}")
  
  # regex to get string inside first pair of parenthesis
  pos = set(re.findall(r'\(([^\(\)]+)\)', definition))
  toAdd = set()
  for piece in pos:
    if ',' in piece:
      toAdd |= set(piece.split(','))
  pos |= toAdd
  pos = set(list(filter(lambda x: x in abbrevToMeaning, pos)))
  # print(definition)
  # print(pos)

  if reading:
    readingKey = reading.group(1)
    kanjiKey = definition.split(' ', 1)[0].strip()
    katakanaKey = readingKey.translate(hir2kat)
    # print(katakanaKey)
    # print(readingKey)
    # print()

    # 塔にいた頃 -> 塔|にい|た|頃 bullshit 
    # if definition not in lookUp[readingKey]:
    #   lookUp[readingKey].append(definition)
    #   readingToDefinitions[readingKey].add(definitionOnly)
    #   # if definitionOnly and readingKey not in definitionToReadings[definitionOnly + '/(P)']:
    #   definitionToReadings[definitionOnly].add(readingKey)
    #   getPOS[readingKey] |= pos
    if definition not in lookUp[kanjiKey]:
      lookUp[kanjiKey].append(definition)
      readingToDefinitions[kanjiKey].add(definitionOnly)
      # if definitionOnly and kanjiKey not in definitionToReadings[definitionOnly + '/(P)']:
      definitionToReadings[definitionOnly].add(kanjiKey)
      getPOS[kanjiKey] |= pos
    if katakanaKey and definition not in lookUp[katakanaKey]:
      lookUp[katakanaKey].append(definition)
      readingToDefinitions[katakanaKey].add(definitionOnly)
      getPOS[katakanaKey] |= pos
  else:
    key = definition.split(' ', 1)[0].strip()
    lookUp[key].append(definition)
    readingToDefinitions[key].add(definitionOnly)
    # if definitionOnly and key not in definitionToReadings[definitionOnly + '/(P)']:
    definitionToReadings[definitionOnly].add(key)
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
      readingToDefinitions[katakanaKey].add(definitionOnly)
      getPOS[katakanaKey] |= pos
      # print(key)
      # print(katakanaKey)
      # print(katakanaKey.translate(kat2hir))
      # print()

print(getPOS['為る'])

# print(lookUp['シコル'])
# print(readingToDefinitions['シコル'])

# # print(lookUp['シコる'])
# # print(readingToDefinitions['シコる'])
# # print(getPOS['シコル'])

# # print(abbrevToMeaning.keys())
# # print(getPOS['れる'])

# # for definition in lookUp['ムズカシイ']:
# #   print(definition)

# def toKatakana(word):
#   tokens = tagger.parse(word).split('\n')
#   numTokens = len(tokens) - 2
#   theWord = ""
#   for i in range(numTokens):
#     token = list(filter(None, re.split('\t|,', tokens[i])))
#     pronunciation = token[-2]
#     surface = token[0]
#     if pronunciation != '*':
#       theWord += pronunciation
#     else:
#       theWord += surface
#   return theWord

# def printDefinitionOfWord(word):
#   definitionsToReadingsAns = dict()
#   print(toKatakana(word))
#   for definition in readingToDefinitions[toKatakana(word)]:
#     definitionsToReadingsAns[definition] = definitionToReadings[definition]

#   # remove duplicate readings
#   for definition, reading in definitionsToReadingsAns.items():
#     if definition.endswith('/(P)'):
#       nonP = definition.replace('/(P)', '')
#       for definition in definitionsToReadingsAns:
#         if definition.endswith(nonP):
#           intersection = definitionsToReadingsAns[definition].intersection(reading)
#           # print(f"duplicates: {intersection}")
#           definitionsToReadingsAns[definition] -= intersection
#           # print(f"new: {definitionsToReadingsAns[definition]}")

#   toReturn = []

#   # Append common readings first
#   for definition, reading in definitionsToReadingsAns.items():
#     if definition.endswith('/(P)'):
#       toReturn.append((list(reading), definition))

#   for definition, reading in definitionsToReadingsAns.items():
#     if not definition.endswith('/(P)'):
#       possiblePVersion = definition + '/(P)'
#       # Append less common readings
#       for definitionP in definitionsToReadingsAns:
#         if possiblePVersion.endswith(definitionP) or definitionP.endswith(possiblePVersion):
#           for piece in toReturn:
#             if definitionP in piece[1]:
#               piece[0].extend(['uncommon'] + list(reading))
#               break
#           break
#       # Else append both reading and definition normally
#       else:
#         toReturn.append((reading, definition))

#   for definition in toReturn:
#     readings = definition[0]
#     common = []
#     uncommon = []
#     flag = False
#     for reading in readings:
#       if reading == 'uncommon':
#         flag = True
#         continue
#       if flag:
#         uncommon.append(reading)
#       else:
#         common.append(reading)

#     print(', '.join(sorted(common)))
#     if uncommon:
#       print(', '.join(sorted(uncommon)))
#     print(definition[1])
#     print()

# printDefinitionOfWord('憑く')
# print(lookUp['憑く'])
# maxWord = max(lookUp, key=len)
# print(lookUp['特定独立行政法人等の労働関係に関する法律'])
# print(len('特定独立行政法人等の労働関係に関する法律'))