from collections import defaultdict

lines = tuple(open("./deinflect.txt", "r"))
conjugations = []
# {surface: [(conjugation, conjugation_type)]}
surfaceToDeinflect = defaultdict(set)

for i, line in enumerate(lines):
  if i <= 27:
    conjugations.append(line.strip())
  else:
    pieces = line.split()
    surface = pieces[0]
    lemma = pieces[1]
    conjugation = pieces[-1]
    surfaceToDeinflect[surface].add((lemma, conjugations[int(conjugation)]))

for k, v in surfaceToDeinflect.items():
  print(k, v)