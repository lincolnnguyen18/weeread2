# echo "" | cabocha -I0 -O2
import MeCab
import re
import json
from collections import defaultdict

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

def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def hasJapanese(string):
  return any(is_cjk(char) for char in string)

conjugations = []
# {surface: (conjugation, conjugation_type)}
surfaceToDeinflect = defaultdict(set)

for i, line in enumerate(tuple(open("./deinflect.txt", "r"))):
  if i <= 27:
    conjugations.append(line.strip())
  else:
    pieces = line.split()
    surface = pieces[0]
    lemma = pieces[1]
    conjugation = pieces[-1]
    surfaceToDeinflect[surface].add((lemma, conjugations[int(conjugation)]))

def find(L, target):
  start = 0
  end = len(L) - 1

  while start <= end:
    middle = (start + end)//2
    midpoint = L[middle][:len(target)].strip()
    if midpoint > target:
      end = middle - 1
    elif midpoint < target:
      start = middle + 1
    else:
      return midpoint

def findFull(L, target):
  start = 0
  end = len(L) - 1

  while start <= end:
    middle = (start + end)//2
    midpoint = L[middle].strip()
    if midpoint > target:
      end = middle - 1
    elif midpoint < target:
      start = middle + 1
    else:
      return midpoint

kanji = r'[㐀-䶵一-鿋豈-頻]'
hiragana = r'[ぁ-ゟ]'
katakana = r'[゠-ヿ]'

def toKatakana(word):
  tokens = tagger.parse(word).split('\n')
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
  return theWord

def isKanji(character):
	return re.search(kanji, character) != None

def isHiragana(character):
	return re.search(hiragana, character) != None

def isKatakana(character):
	return re.search(katakana, character) != None

def isJapanese(character):
	return isKanji(character) or isHiragana(character) or isKatakana(character)

fullDict = tuple(open("./fulldict.txt", "r"))
abbrevs = tuple(open("./abbreviations.txt", "r"))
lookUp = defaultdict(list)
lookUpAll = defaultdict(list)
getPOS = defaultdict(set)
getAllPOS = defaultdict(set)
abbrevToMeaning = dict()

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
  
  kanjiKey = definition.split(' ', 1)[0].strip()
  if definition not in lookUp[kanjiKey]:
      lookUp[kanjiKey].append(definition)
      lookUpAll[kanjiKey].append(definition)
      getPOS[kanjiKey] |= pos
  
  if reading:
    readingKey = reading.group(1)
    katakanaKey = readingKey.translate(hir2kat)

    if definition not in lookUpAll[readingKey]:
      # lookUp[readingKey].append(definition)
      lookUpAll[readingKey].append(definition)
      getAllPOS[readingKey] |= pos
    if katakanaKey and definition not in lookUpAll[katakanaKey]:
      # lookUp[katakanaKey].append(definition)
      lookUpAll[katakanaKey].append(definition)
      getAllPOS[readingKey] |= pos
  
  # else:
  #   key = definition.split(' ', 1)[0].strip()
  #   lookUp[key].append(definition)
  #   getPOS[key] |= pos

  #   tokens = tagger.parse(key).split('\n')
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
  #   katakanaKey = theWord

  #   if len(katakanaKey) > 0 and katakanaKey != key and definition not in lookUp[katakanaKey]:
  #     lookUp[katakanaKey].append(definition)
  #     getPOS[katakanaKey] |= pos

def addHiragana(hira, kanji):
  getPOS[hira] = getPOS[kanji]
  lookUp[hira] = lookUp[kanji]

# print(lookUp['かわいい'])
addHiragana('する', '為る')
addHiragana('いる', '居る')
addHiragana('なる', '為る')
addHiragana('くる', '來る')
dictEntries = sorted(lookUpAll.keys())
  
def isVerb(word):
  allPOS = len(list(filter(lambda v: re.match(r'^v[^u]', v), getAllPOS[word]))) > 0
  onePOS = len(list(filter(lambda v: re.match(r'^v[^u]', v), getPOS[word]))) > 0
  if len(word) > 1:
    return allPOS or onePOS
  return onePOS

def isAdjective(word):
  allPOS = len(list(filter(lambda v: re.match(r'^adj', v), getAllPOS[word]))) > 0
  onePOS = len(list(filter(lambda v: re.match(r'^adj', v), getPOS[word]))) > 0
  if len(word) > 1:
    return allPOS or onePOS
  return onePOS

def isNoun(word):
  return len(list(filter(lambda v: re.match(r'^n[^u|e^a]', v), getPOS[word]))) > 0

class Word:
  def __init__(self, surface, reading, pos):
    self.surface = surface
    self.reading = reading
    self.lemmas = dict()
    self.pos = pos
  def __str__(self):
    return '\t'.join([self.surface, self.reading, ",".join(self.lemmas),",".join(self.pos)])

class Line:
  def __init__(self):
    self.words = []
  def __str__(self):
    return "|".join([word.surface for word in self.words])
  def withIndices(self):
    return "|".join([f"{word.surface}{i}" for i, word in enumerate(self.words)])
  def lemmas(self):
    return "|".join([f"{','.join(word.lemmas) + '*' + '#'.join([','.join(labels) for labels in word.lemmas.values()])}{i}" if len(word.lemmas) > 0 else f"{word.surface}{i}" for i, word in enumerate(self.words)])
  def json(self):
    ans = []
    for word in self.words:
      ans.append((word.surface, word.lemmas))
    return ans
  def mergeIndices(self, i, j):
    if j > len(self.words) - 1:
      return
    times = j - i
    while times > 0:
      self.words[i].surface += self.words[i+1].surface
      self.words[i].reading += self.words[i+1].reading
      self.words[i].lemmas.update(self.words[i+1].lemmas)
      # if not self.words[i].lemmas
      # self.words[i].lemmas[self.words[i+1].surface] = ["subword"]
      del self.words[i+1]
      times -= 1
  
  # returns lemma and labels
  def getInflectMatch(self, word, i, matches):
    print(f"\nstart getInflectMatch for {word}")

    origin = word

    # Initialize level 1
    level = [(word, [])]
    # Initialize visited endings
    visited = set()
    # # Initialize matches
    # matches = []
    matchPOS = None

    # Search
    while True:
      # For each word in level
      newLevel = []
      for word, labels in level:
        # Get endings
        endings = []
        for candidate in surfaceToDeinflect:
          # Don't search if word is a lemma by itself
          # if word.endswith(candidate) and candidate not in visited and word != candidate:
          # if word.endswith(candidate) and word != candidate:
          # if word.endswith(candidate):
          if word.endswith(candidate) and candidate not in visited:
            endings.append(candidate)
            visited.add(candidate)
        print(f"endings: {endings}")

        # Get new words
        newWords = []
        for ending in endings:
          newEndings = surfaceToDeinflect[ending]
          print(f"new endings: {newEndings} to replace {ending} in {word}")
          for newEnding in newEndings:
            newWord = word.replace(ending, newEnding[0])

            print(f"newWord: {newWord} when {newEnding[0]} replaced {ending} in {word}")
            newLabel = newEnding[1]
            newLabels = [newLabel] + labels
            newTuple = (newWord, newLabels)
            print(f"newTuple: {newTuple} with pos: {getPOS[newWord]}")

            if newWord not in matches and newWord in lookUpAll:
              # if len(newWord) <= 2 and newWord not in lookUp:
              #   print(f"{newWord} is not in lookUp and too short to lookUpAll")
              #   continue

              print(f"NEW WORD MATCHED {newWord} ------------------------------------------------------")

              if matchPOS:
                if isVerb(newWord) and matchPOS != 'verb':
                  continue
                if isAdjective(newWord) and matchPOS != 'adj':
                  continue

              # if mecab says it is verb and match is not verb then invalid
              # if '' and not isVerb(origin):

              print("verb/adjective CHECK")
              print(f"checking if {newWord} is verb {isVerb(newWord)} or adjective {isAdjective(newWord)}")
              # If not verb or adjective not no conjugation
              # if not (isVerb(newWord) or isAdjective(newWord) or '-sugiru' in newLabels):
              if not (isVerb(newWord) or isAdjective(newWord)):
                print('INVALID #######################################################')
                continue

              # Invalid conjugations
              # # sasete -> sasetsu
              # if origin == 'させて' and newWord == 'させつ':
              #   break

              # た	る	2432	14 tabeta -> taberu; past tense; root must be v1	Ichidan verb
              if ending == 'た' and newEnding[0] == 'る':
                print('ta -> ru CHECK")')
                print(f"checking if {newWord} is v1 ichidan verb: is v1 in {getPOS[newWord]}? {'v1' in getPOS[newWord]}")
                if not 'v1' in getPOS[newWord]:
                  print('INVALID #######################################################')
                  continue
              
              # # Invalid POS
              # # Break if sugiru and not verb or adjective
              # if '-sugiru' in newLabels:
              #   print('-sugiru ru CHECK")')
              #   print(f"checking if {newWord} is verb {isVerb(newWord)} or is adjective {isAdjective(newWord)}")
              #   if not (isVerb(newWord) or isAdjective(newWord)):
              #     print('INVALID #######################################################')
              #     continue

              # Break if imperative or verb stem and length of labels != 1 or not verb
              # if 'imperative or verb stem' in newLabels:
              #   print('imperative or verb stem CHECK")')
              #   # print(f"checking if {newWord} length of labels {len(newLabels)} is 1 and verb {isVerb(newWord)}")
              #   # if not (len(newLabels) == 1 and isVerb(newWord)):
              #   print(f"checking if {newWord} length of labels {len(newLabels)} is 1 and verb {isVerb(newWord)}")
              #   if not (len(newLabels) == 1 and isVerb(newWord)):
              #     print('INVALID #######################################################')
              #     print()
              #     continue

              # Break if -te and not verb
              if '-te' in newLabels and not isVerb(newWord):
                print('-te CHECK")')
                print(f"checking if {newWord} is verb {isVerb(newWord)}")
                if not isVerb(newWord):
                  print('INVALID #######################################################')
                  continue
              
              matches += newTuple
            newWords.append(newTuple)
            if isVerb(newWord):
              matchPOS = 'verb'
            elif isAdjective(newWord):
              matchPOS = 'adj'

        # Update new level
        newLevel += newWords
      
      # Update level
      level = newLevel
      print(f"new level: {level}")

      # If level is empty, we're done
      if len(level) == 0:
        break

      # print(f"new level: {level}")
    
    # Return matches
    return matches

  def finalMerge(self):
    print("Starting finalMerge")
    for i in range(len(self.words)):
      if i >= len(self.words):
        break

      # For TESTING
      print("MERGING")
      print(self.words[i].surface, self.words[i].lemmas)

      # Custom merges
      # でくださる lemma -> if verb + 'で' or 'て' + 'くださる' then merge and add 'please' label
      if i + 2 < len(self.words) and any(isVerb(lemma) for lemma in self.words[i].lemmas) and (self.words[i+1].surface == 'で' or self.words[i+1].surface == 'て') and self.words[i+2].surface == 'ください':
        firstLemma = list(self.words[i].lemmas.keys())[0]
        self.words[i].lemmas[firstLemma] += ['please']
        self.mergeIndices(i, i+2)
        continue

      # でくださる lemma -> if verb with '-te' in labels + 'くださる' then merge and add 'please' label
      elif i + 1 < len(self.words) and any('-te' in lemma for lemma in self.words[i].lemmas.values()) and self.words[i+1].surface == 'ください':
        firstLemma = list(self.words[i].lemmas.keys())[0]
        self.words[i].lemmas[firstLemma] += ['please']
        self.mergeIndices(i, i+1)
        continue

      # Initialize longest
      longest = [self.words[i].surface]
      print(''.join(longest))

      # If invalid longest than skip
      if not find(dictEntries, ''.join(longest)):
        # if all(not find(dictEntries, lemma) for lemma in self.words[i].lemmas.keys()):
        #   print(f"{''.join(longest)} is invalid")
        # print()
        continue

      j = i + 1
      # Get longest prefix substring match
      while j < len(self.words):
        # if j >= len(self.words):
        #   break
        longest.append(self.words[j].surface)
        print(f"EXPANDING; range:{i}, {j}")
        print(''.join(longest), find(dictEntries, ''.join(longest)))
        if not find(dictEntries, ''.join(longest)):
          # j -= 1
          break
        j += 1
      
      if j >= len(self.words):
        j -= 1
      
      # Shorten match until valid    
      while True:
        if j < 0 or not longest:
          print("break 1")
          break
        print(f"SHORTENING; range:{i}, {j}")
        shortened = ''.join(word.surface for word in self.words[i:j+1])
        print(''.join(longest), '###', shortened, shortened in lookUpAll, f"range:{i}, {j}")
        if i >= j:
          print("break 2")
          break

        # If valid then merge surfaces
        if shortened in lookUpAll:
          self.mergeIndices(i, j)

        shortenedWithoutLemma = ''.join(word.surface for word in self.words[i:j])
        flag = False

        if j >= len(self.words):
          print("break 3")
          break
        for lemma in self.words[j].lemmas:
          newShortened = shortenedWithoutLemma + lemma
          print('%', newShortened, newShortened in lookUpAll)
          # If valid then merge surfaces
          if newShortened in lookUpAll:
            print(f"MERGING LEMMA; {newShortened} is in lookUpAll")
            print(newShortened in lookUpAll)
            print(lookUpAll[newShortened])
            self.words[i].lemmas[newShortened] = self.words[j].lemmas[lemma]
            flag = True
        if flag:
          self.mergeIndices(i, j)
        longest.pop()
        j -= 1
      
      print()
  
  def endswithInflect(self, word):
    for candidate in surfaceToDeinflect:
      if word.endswith(candidate):
        return True
  
  def preprocess(self):
    # if len(self.words) <= 1:
    #   return
    # print("Starting preprocess")
    # print(len(self.words))
    # print('|'.join([word.surface for word in self.words]))
    for i in range(len(self.words)-1):
      if len(self.words[i+1].surface) != 1:
        continue
      toTest = self.words[i].surface + '|' + self.words[i+1].surface
      joined = self.words[i].surface[-1] + self.words[i+1].surface[0]
      # print(f"is しろ split in {toTest}: {joined == 'しろ'}")
      if joined == 'しろ':
        print(f"old line: {'|'.join([word.surface for word in self.words])}")
        self.words[i].surface = self.words[i].surface[:-1]
        self.words[i+1].surface = 'しろ'
        print("Preprocessed SHIRO")
        print(f"new line: {'|'.join([word.surface for word in self.words])}")

  def deinflect(self):
    for i in range(len(self.words)):
      if i >= len(self.words):
        break
      if any(pos in ['動詞', '形容詞', '名詞', '助詞'] for pos in self.words[i].pos):
        if '助詞' in self.words[i].pos and self.words[i].surface == 'で':
          continue

        surface = [self.words[i].surface]
        startIndex = endIndex = i

        # get all hirgana after word
        for j in range(i+1, len(self.words)):
          if not all(isHiragana(character) for character in self.words[j].surface):
            break
          surface.append(self.words[j].surface)
          endIndex += 1
        print("get all hiragana after")
        print(surface)

        # ensure ending is in deinflect
        while surface and all(isHiragana(character) for character in surface[-1]) and not self.endswithInflect(''.join(surface)):
          surface.pop()
          endIndex -= 1
        # print(''.join(surface))
        print("pop until end in inflection")
        print(surface)

        # # get all endings; for testing
        # endings = []
        # for ending in surfaceToDeinflect:
        #   if ''.join(surface).endswith(ending):
        #     endings.append(ending)
        # for ending in endings:
        #   print(ending, surfaceToDeinflect[ending])

        # pop surface until ending found or no more surface
        print("popping until match inflection")
        result = []
        while surface:
          result += self.getInflectMatch(''.join(surface), startIndex, result)
          print(f"surface: {surface}")
          print(f"result: {result}")

          # Stop when matches found
          if not result:
            surface.pop()
            endIndex -= 1
          else:
            break

          # # Gets all matches
          # surface.pop()
          # endIndex -= 1
        
        # print 
        if result:
          # nonVerbMatches = lookUp[toKatakana(''.join(surface))]
          # if not nonVerbMatches:
          #   nonVerbMatches = lookUp[''.join(surface)]
          # if nonVerbMatches:
          #   print(f"found non-verb matches for: {''.join(surface)}")
            
          #   # for match in nonVerbMatches:
          #   #   print(f"  {match}")
          #   # print()
          
          # FOR TESTING
          print(''.join(surface))
          print(f"found verb matches for: {result}")
          print(f"merge from {startIndex} to {endIndex}")
          # print("word.lemmas:")
          for i, original in enumerate(result):
            if i % 2 == 0:
              self.words[startIndex].lemmas[original] = result[i+1]
              # print(f"{original}: {self.words[startIndex].lemmas[original]}")
          self.mergeIndices(startIndex, endIndex)
          # print('--------------------------------------------------------')

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

jpLines = tuple(open("./sample2.txt", "r"))
output = open("output2.txt", "w")
output = open("output2.txt", "w+")

for jpLine in jpLines:
  if not hasJapanese(jpLine):
    print(jpLine, file=output)
    continue
  print(jpLine.strip(), file=output)
  # print(tagger.parse(jpLine.strip()), file=output)
  # print(tagger.parse(jpLine.strip()))
  tokens = tagger.parse(jpLine.strip()).split('\n')
  numTokens = len(tokens) - 2
  line = Line()
  for i in range(numTokens):
    token = list(filter(None, re.split('\t', tokens[i])))
    token = [token[0]] + token[1].split(',')
    # print(token)
    # surface reading pos
    # print(token)
    # surface form
    # Parts of speech!
    # Part-of-speech subdivision 1!
    # Part-of-speech subdivision 2!
    # Part-of-Speech Subdivision 3!
    # Conjugation type!
    # Conjugation form!
    # Original form
    # Reading
    # Pronunciation!
    # print(token[0])
    # print(token[-1])
    # print(token[1:7])
    # print('------------------------------------------------------------')
    line.words.append(Word(token[0], token[-1], token[1:7]))

  line.preprocess()
  line.deinflect()
  line.finalMerge()
  # print(line, file=output)
  print(line.withIndices(), file=output)
  print(line.lemmas(), file=output)
  print("", file=output)
  # print(line.json(), file=output)

# getDefinition('かもしれない', ["potential or passive", "polite negative"])