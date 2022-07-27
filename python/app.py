# uvicorn --reload --port 8000 app:app

import socketio

import MeCab
import regex as re
import json
# import edlib
from collections import defaultdict
# from difflib import SequenceMatcher
from cabocha.analyzer import CaboChaAnalyzer

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

ranges2 = [
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
]

ranges3 = [
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
]

katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ" 
kanjiRe = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', re.UNICODE)
japaneseRE = re.compile(r"[\p{Hiragana}\p{Katakana}\p{Han}]+", re.UNICODE)
hir2kat = str.maketrans(hiragana_chart, katakana_chart)
kat2hir  = str.maketrans(katakana_chart, hiragana_chart)

def stripNonHiragana(text):
  ans = "".join([c for c in text if c in hiragana_chart])
  print(f"stripping nonhiragana from {text} -> {ans}")
  return ans

def hirToKat(string):
  return string.translate(hir2kat)

def katToHir(string):
  return string.translate(kat2hir)

def is_only_kana(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges2])

def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def isKanjiKana(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges3])

def hasKanjiKanas(string):
  return any(hasKana(char) for char in string)

def hasOnlyKanji(string):
  return re.matchfull(r'([\p{Han}]+)', string)

def hasJapanese2(string):
  # return any(is_cjk(char) for char in string)
  matches = re.findall(r'([\p{Hiragana}\p{Katakana}\p{Han}]+)', string)
  return len(matches) > 0

def hasKanij(string):
  return getKanjis(string) != ""

def hasKana(string):
  return any(is_only_kana(char) for char in string)

def getKanjis(string):
  return ''.join(kanjiRe.findall(string))

def isOnlyKanji(string):
  return getKanjis(string) == string

def endswithInflect(word):
  for candidate in surfaceToDeinflect:
    if word.endswith(candidate):
      return True

analyzer = CaboChaAnalyzer()
jpToEn = defaultdict(lambda: '')
lookUp = defaultdict(list)
getPOS = defaultdict(set)
kanjisToDef = defaultdict(list)
kanjisToWords = defaultdict(list)
abbrevToMeaning = dict()

for line in tuple(open("./abbreviations.txt", "r")):
  splitted = line.split('\t', 1)
  splitted = [split.strip() for split in splitted]
  abbrevToMeaning[splitted[0]] = splitted[1]

for line in tuple(open("./mecab.txt", "r")):
  pieces = line.split(' ', 1)
  japanese = pieces[0].strip()
  english = pieces[1].strip()
  jpToEn[japanese] = english

for line in tuple(open("./fulldict.txt", "r")):
  pieces = line.split(' ', 1)
  kanji = pieces[0].strip()
  kanjis = getKanjis(kanji)
  definition = pieces[1].strip()
  reading = re.search(r'\[(.*)\]', definition)

  pos = set(re.findall(r'\(([^\(\)]+)\)', definition))
  actualPos = set()
  for piece in pos:
    if ',' in piece:
      actualPos |= set(piece.split(','))
    else:
      actualPos.add(piece)
  pos = set(list(filter(lambda x: x in abbrevToMeaning, actualPos)))

  lookUp[kanji].append(definition)
  getPOS[kanji] |= pos
  if kanjis != "":
    kanjisToDef[kanjis].append(line)
    kanjisToWords[kanjis].append(kanji)
  if reading:
    reading = reading.group(1)
    lookUp[reading].append(definition)
    getPOS[reading] |= pos

conjugations = []
surfaceToDeinflect = defaultdict(set) # {surface: (conjugation, conjugation_type)}
for i, line in enumerate(tuple(open("./deinflect.txt", "r"))):
  if i <= 27:
    conjugations.append(line.strip())
  else:
    pieces = line.split()
    surface = pieces[0]
    lemma = pieces[1]
    conjugation = pieces[-1]
    surfaceToDeinflect[surface].add((lemma, conjugations[int(conjugation)]))
sortedLookUp = sorted(lookUp.keys())

def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()

def diff(a, b):
  return edlib.align(a, b)['editDistance']

def getDefinition(word, labels):
  definitions = lookUp[word]
  # print(definitions)
  # print()
  for definition in definitions:
    kanji = definition.split(' ', 1)[0].strip()
    reading = re.search(r'\[(.*)\]', definition)
    theRest = re.search(r'\/(.+)\/', definition)
    readingOnly = definitionOnly = ""
    if reading:
      readingOnly = reading.group(1)
    if theRest:
      definitionOnly = theRest.group(1)
    lines = definitionOnly.split('/')
    # print(f"{kanji}  {readingOnly}  (< potential or passive < polite negative)")
    print(f"{kanji}  {readingOnly}  (< {' < '.join(labels)})")
    print('; '.join(lines))
    print()

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

@sio.event
async def hasOnlyHiragana(sid, data):
  data, myid = data['data'], data['id']
  await sio.emit('hasOnlyHiraganaRes', json.dumps((myid, re.fullmatch(r'^[\p{Hiragana}]+$', data) != None)), to=sid)

@sio.event
async def hasJapanese(sid, data):
  data, myid = data['data'], data['id']
  test = hasJapanese2(data);
  print(f"hasJapanese2: {test} {data}")
  await sio.emit('hasJapaneseRes', json.dumps((myid, test, data)), to=sid)

@sio.event
def connect(sid, environ):
  print(sid, 'connected')

@sio.event
def disconnect(sid):
  print(sid, 'disconnected')

@sio.event
async def tokenizeFragment(sid, data):
  data, myid = data['data'], data['id']
  # print(f"tokenizing fragment: {data}")
  chunks = analyzer.parse(data)
  tokens = []
  tokenmatches = []
  tokenMatchesDict = dict()
  rawMatches = set()
  kanjiOnlyMatches = set()
  genkeiMatches = set()
  genkeiSubMatches = set()
  wordsWithSameKanjiMatches = set()
  soFarMatches = set()

  # Print chunks
  # res.append(f"{'|'.join(chunk.surface for chunk in chunks)}")

  # Find genkei matches
  for chunk in chunks:
    # res.append(f"tokens in chunk: {'|'.join(','.join([token.surface for token in chunk.tokens]) for chunk in chunks)}")
    for token in chunk:
      # print(token.surface)
      tokens.append(token)
      # description = f"{token.surface}; pos: {jpToEn[token.pos]}, pos1: {jpToEn[token.pos1]}, pos2: {jpToEn[token.pos2]}, pos3: {jpToEn[token.pos3]}, ctype: {jpToEn[token.ctype]}, cform: {jpToEn[token.cform]}, genkei: {token.genkei}, reading: {token.yomi}"
      # tokenmatches.append(description)
      # tokenMatchesDict[token.surface] = description
      # if token.genkei in lookUp:
      #     genkeiMatches.add(token.genkei)
      #     soFarMatches.add(token.genkei)
  
  # # Find genkei submatches
  # for token in tokens:
  #   for entry in lookUp:
  #     if entry in token.genkei and entry not in soFarMatches:
  #       genkeiSubMatches.add(entry)
  #       soFarMatches.add(entry)
  
  # # Find 
  # for entry in lookUp:
  #   if entry in data and  entry not in soFarMatches:
  #     rawMatches.add(entry)
  #     soFarMatches.add(entry)
  #   # if entry in data and entry not in soFarMatches:
  #   #   # Find definable kanjis in word
  #   #   if isOnlyKanji(entry):
  #   #     kanjiOnlyMatches.add(entry)
  #   #     soFarMatches.add(entry)
  #   #   # Find other matches in word
  #   #   else:
  #   #     rawMatches.add(entry)
  #   #     soFarMatches.add(entry)
  
  # # Find words with same kanjis
  # sameKanjis = getKanjis(chunk.surface)
  # if sameKanjis != "":
  #   words = kanjisToWords[sameKanjis]
  #   for word in words:
  #     if word[0] == chunk.surface[0] and len(word) <= len(chunk.surface) and word not in soFarMatches:
  #       wordsWithSameKanjiMatches.add(word)
  #       soFarMatches.add(word)

    # for line in kanjisToDef[sameKanjis]:
    #   pieces = line.split(' ', 1)
    #   dictForm = pieces[0].strip()
    #   # print(line)
    #   # print(pieces)
    #   # print(f"dictForm: {dictForm}")
    #   # print(f"kanjiOnlyMatches: {kanjiOnlyMatches}")
    #   # print(f"dictForm in kanjiOnlyMatches: {dictForm in kanjiOnlyMatches}")
    #   # print(f"wordsWithSameKanjiMatches: {wordsWithSameKanjiMatches}")
    #   if dictForm not in rawMatches and dictForm not in kanjiOnlyMatches and dictForm not in genkeiMatches and dictForm not in wordsWithSameKanjiMatches:
    #     print(dictForm)
    #     wordsWithSameKanjiMatches.append(line)
    # print(f"wordsWithSameKanjiMatches: {wordsWithSameKanjiMatches}")

  # res.append(f"tokens: {'|'.join(token.surface for token in tokens)}")
  # res.append('\n'.join(tokenmatches))
  # res.append(f"genkei matches: {','.join(sorted(genkeiMatches, key=len, reverse=True))}")
  # res.append(f"genkei submatches: {', '.join(sorted(genkeiSubMatches, key=len,reverse=True))}")
  # res.append(f"matches in surface chunk: {','.join(sorted(sorted(rawMatches, key=len, reverse=True), key=isOnlyKanji, reverse=True))}")
  # # res.append(f"other kanji only matches in chunk: {','.join(sorted(kanjiOnlyMatches, key=len, reverse=True))}")
  # res.append(f"words with same kanjis in chunk: {', '.join(sorted(wordsWithSameKanjiMatches, key=len))}")
  # # res.append("words with same kanjis:")
  # # res.append(''.join(wordsWithSameKanjiMatches))

  res = [[] for _ in range(len(tokens))]
  
  for i, token in enumerate(tokens):
    res[i].append(token.surface)
    res[i].append(katToHir(token.yomi))
    res[i].append(jpToEn[token.pos])
    res[i].append(jpToEn[token.pos1])
    res[i].append(jpToEn[token.pos2])
    res[i].append(jpToEn[token.pos3])
    res[i].append(jpToEn[token.ctype])
    res[i].append(jpToEn[token.cform])
    res[i].append(token.genkei)
    # append genkei sub tokens
    # append cross token matches
  
  # for token in tokens:
  #   for entry in lookUp:
  #     if entry in token.genkei and entry not in soFarMatches:
  #       genkeiSubMatches.add(entry)
  #       soFarMatches.add(entry)

  await sio.emit('tokenizeFragmentResult', json.dumps((myid, res)), room=sid)

def getChunkYomi(chunk):
  yomi = ""
  for token in chunk:
    if token.yomi != '*':
      yomi += token.yomi
  ans = katToHir(yomi)
  return stripNonHiragana(ans)

@sio.event
async def tokenize(sid, data):
  data, myid = data['data'], data['id']
  surfaceResult = []
  readingResult = []

  for line in data.split('\n'):
    line = line.strip()
    # print(line)
    # print(f"hasJapanese:{hasJapanese(line)}")
    if hasJapanese2(line):
      chunks = []
      readings = []
      tree = analyzer.parse(line)
      i = 0
      while i < tree.chunk_size:
        chunk = tree.chunks[i]
        tokensInChunk = []
        readingsInChunk = []

        # print(f"CHUNKS: {chunks}")

        # # check if previous chunk surface + current chunk's first genkei is in lookup
        # if chunks:
        #   mergedSurface = ''.join(chunks[-1]) + chunk.surface
        #   mergedGenkei = ''.join(chunks[-1]) + chunk[0].genkei
        #   splitPoint = len(''.join(chunks[-1]))
        #   # print(f"TESTING {mergedSurface} for {startPiece} at {splitPoint}")
        #   # print(f"TESTING {mergedGenkei} for {startPiece} at {splitPoint}")
        #   for word in lookUp:
        #     match = None
        #     start = mergedSurface.find(word)
        #     if start > -1 and start < splitPoint:
        #       matchPointEnd = start + len(word) - 1
        #       if matchPointEnd >= splitPoint:
        #         print(f"mergedSurface: {mergedSurface}; splitpoint: {splitPoint}")
        #         print(word, start, matchPointEnd)
        #         match = word
        #         break
        #     elif mergedGenkei != mergedSurface and word != match:
        #       start = mergedGenkei.find(word)
        #       if start > -1 and start < splitPoint:
        #         matchPointEnd = start + len(word) - 1
        #         if matchPointEnd >= splitPoint and start < splitPoint:
        #           print(f"mergedGenkei: {mergedGenkei}; splitpoint: {splitPoint}")
        #           print(word, start, matchPointEnd)
        #           break
        #   # chunks[-1] += chunk[0]
        #   # for token in chunk:
        #   #   ''.join(chunks[-1].surface += token.surface
        #   #   chunks[-1].yomi += katToHir(token.yomi)

        for token in chunk:
          # print(token.surface, token.yomi)
          tokensInChunk.append(token.surface)
          readingsInChunk.append(katToHir(token.yomi))
        i += 1
        # print('END OF CHUNK')
        chunks.append(tokensInChunk)
        readings.append(readingsInChunk)

      # print('END OF LINE')
      surfaceResult.append(chunks)
      readingResult.append(readings)
    else:
      # print(line)
      # print('END OF NON JAPANESE CHUNK')
      surfaceResult.append([[line]])
      readingResult.append([[]])
  
  # print(surfaceResult)
  # print(readingResult)

  await sio.emit('tokenizeResult', json.dumps((myid, [surfaceResult, readingResult])), to=sid)