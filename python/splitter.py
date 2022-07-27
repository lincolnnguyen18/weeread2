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

def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def hasJapanese(string):
  return any(is_cjk(char) for char in string)

analyzer = CaboChaAnalyzer()
result = []
jpToEn = dict()

for line in tuple(open("./mecab.txt", "r")):
  pieces = line.split(' ', 1)
  japanese = pieces[0].strip()
  english = pieces[1].strip()
  jpToEn[japanese] = english

for line in tuple(open("./sample2.txt", "r")):
  line = line.strip()
  if hasJapanese(line):
    chunks = []
    tree = analyzer.parse(line)
    for chunk in tree:
      chunks.append(chunk.surface)
      for token in chunk:
        if token.genkei != token.surface:
          print(token.genkei)
    print(chunks)
    result.append(chunks)
  else:
    print([line])
    result.append([line])
  # print()

# print(result)