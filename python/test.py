import regex as re
# japaneseRE = re.compile(r"[\p{Hiragana}\p{Katakana}\p{Han}]+", re.UNICODE)

# hasKanji = re.findall(r'([\p{Han}]+)', string)
# hasKatakana = re.findall(r'([\p{Katakana}]+)', string)
hasOnlyHiragana = re.fullmatch(r'^[\p{Hiragana}]+$', 'See for yourself if the Karubonara (・・・・・・) of Konbini (・・・・) exists.') != None
hasJapanese = re.findall(r'([\p{Hiragana}\p{Katakana}\p{Han}]+)', 'Besides, we are now stepping over the back of the Flimsulat Mountains, in the middle of them. If I had to ask you to go home alone from here, and then you got lost somewhere, the drink would have tasted very bad.')

print(hasJapanese)