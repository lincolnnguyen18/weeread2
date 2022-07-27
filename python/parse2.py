import re
import json
from collections import defaultdict
from collections import OrderedDict
dictEntries = tuple(open("./dict.txt", "r"))
conjugations = []
# {surface: (conjugation, conjugation_type)}
surfaceToDeinflect = OrderedDict()
for i, line in enumerate(tuple(open("./deinflect.txt", "r"))):
  if i <= 27:
    conjugations.append(line.strip())
  else:
    pieces = line.split()
    surface = pieces[0]
    lemma = pieces[1]
    conjugation = pieces[-1]
    if surface not in surfaceToDeinflect:
      surfaceToDeinflect[surface] = [(lemma, conjugations[int(conjugation)])]
    else:
      surfaceToDeinflect[surface].append((lemma, conjugations[int(conjugation)]))

fullDict = tuple(open("./fulldict.txt", "r"))
lookUp = defaultdict(set)

for definition in fullDict:
  reading = re.search(r'\[(.*)\]', definition)
  if reading:
    readingKey = reading.group(1)
    kanjiKey = definition.split(' ', 1)[0].strip()
    lookUp[readingKey].add(definition)
    lookUp[kanjiKey].add(definition)
  else:
    key = definition.split(' ', 1)[0].strip()
    lookUp[key].add(definition)

jpLines = tuple(open("./sample2.txt", "r"))
for jpLine in jpLines:
  line = jpLine.strip()
  tokens = list(line)
  print(line)
  print()

  for key in surfaceToDeinflect:
    if key in line:
      print(key)
      endOfOld = line.index(key)
      if endOfOld == 0:
        continue
      replacement = surfaceToDeinflect[key][0][0]
      newLine = line.replace(key, replacement)
      endOfNew = newLine.index(replacement)
      print(newLine)
      print(endOfNew)

      print()

      print()