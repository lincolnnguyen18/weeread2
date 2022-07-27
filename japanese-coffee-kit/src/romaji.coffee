# Japanese Romanization
# Output Hepburn romanization

Romaji = exports? and exports or @Romaji = {}

Romaji.toRomaji = (kanakana) ->
  values = (romaji[val] or val for val in @toHiragana kanakana).join ""
  for rule in transliteration.hepburn
    values = values.replace rule[0], rule[1]
  values

Romaji.toHiragana = (katakana) ->
    kana[val] or val for val in katakana.split ""

kana =
  "ア": "あ", "ァ": "ぁ",
  "イ": "い", "ィ": "ぃ",
  "ウ": "う", "ゥ": "ぅ",
  "エ": "え", "ェ": "ぇ",
  "オ": "お", "ォ": "ぉ",
  "カ": "か", "ガ": "が",
  "キ": "き", "ギ": "ぎ",
  "ク": "く", "グ": "ぐ",
  "ケ": "け", "ゲ": "げ",
  "コ": "こ", "ゴ": "ご",
  "サ": "さ", "ザ": "ざ",
  "シ": "し", "ジ": "じ",
  "ス": "す", "ズ": "ず",
  "セ": "せ", "ゼ": "ぜ",
  "ソ": "そ", "ゾ": "ぞ",
  "タ": "た", "ダ": "だ",
  "チ": "ち", "ヂ": "ぢ",
  "ツ": "つ", "ヅ": "づ", "ッ": "っ",
  "テ": "て", "デ": "で",
  "ト": "と", "ド": "ど",
  "ナ": "な",
  "ニ": "に",
  "ヌ": "ぬ",
  "ネ": "ね",
  "ノ": "の",
  "ハ": "は", "バ": "ば", "パ": "ぱ",
  "ヒ": "ひ", "ビ": "び", "ピ": "ぴ",
  "フ": "ふ", "ブ": "ぶ", "プ": "ぷ",
  "ヘ": "へ", "ベ": "べ", "ペ": "ぺ",
  "ホ": "ほ", "ボ": "ぼ", "ポ": "ぽ",
  "マ": "ま",
  "ミ": "み",
  "ム": "む",
  "メ": "め",
  "モ": "も",
  "ラ": "ら",
  "リ": "り",
  "ル": "る",
  "レ": "れ",
  "ロ": "ろ",
  "ヤ": "や", "ャ": "ゃ",
  "ユ": "ゆ", "ュ": "ゅ",
  "ヨ": "よ", "ョ": "ょ",
  "ワ": "わ",
  "ヲ": "を",
  "ヰ": "ゐ",
  "ゑ": "ゑ",
  "ン": "ん"

romaji =
  "あ": "a", "ぁ": "xa",
  "い": "i", "ぃ": "xi",
  "う": "u", "ぅ": "xu",
  "え": "e", "ぇ": "xe",
  "お": "o", "ぉ": "xo",
  "か": "ka", "が": "ga",
  "き": "ki", "ぎ": "gi",
  "く": "ku", "ぐ": "gu",
  "け": "ke", "げ": "ge",
  "こ": "ko", "ご": "go",
  "さ": "sa", "ざ": "za",
  "し": "si", "じ": "zi",
  "す": "su", "ず": "zu",
  "せ": "se", "ぜ": "ze",
  "そ": "so", "ぞ": "zo",
  "た": "ta", "だ": "da",
  "ち": "ti", "ぢ": "di",
  "つ": "tu", "づ": "du", "っ": "xtu",
  "て": "te", "で": "de",
  "と": "to", "ど": "do",
  "な": "na",
  "に": "ni",
  "ぬ": "nu",
  "ね": "ne",
  "の": "no",
  "は": "ha", "ば": "ba", "ぱ": "pa",
  "ひ": "hi", "び": "bi", "ぴ": "pi",
  "ふ": "fu", "ぶ": "bu", "ぷ": "pu",
  "へ": "he", "べ": "be", "ぺ": "pe",
  "ほ": "ho", "ぼ": "bo", "ぽ": "po",
  "ま": "ma",
  "み": "mi",
  "む": "mu",
  "め": "me",
  "も": "mo",
  "ら": "ra",
  "り": "ri",
  "る": "ru",
  "れ": "re",
  "ろ": "ro",
  "や": "ya", "ゃ": "xya",
  "ゆ": "yu", "ゅ": "xyu",
  "よ": "yo", "ょ": "xyo",
  "わ": "wa",
  "を": "wo",
  "ゐ": "wi",
  "ゑ": "we",
  "ん": "n'",
  "ー": "-"

transliteration =
  hepburn: [
      [/n\'([^aiueoy]|$)/g, "n$1"],
      [/ixy/g, "y"],
      [/z(?:(i)|y)/g, "j$1"],
      [/xtu([a-z])/g, "$1$1"],
      [/s(?:(i)|y)/g, "sh$1"],
      [/t(?:(i)|y)/g, "ch$1"],
      [/tu/g, "tsu"],
      [/d(?:(i)|y)/g, "j$1"],
      [/du/g, "zu"],
      # [/hu/g, "fu"],
      [/o[ou\-]/g, "ō"],
      [/u[u\-]/g, "ū"],
      [/a[a\-]/g, "ā"],
      [/e[e\-]/g, "ē"],
      [/i\-/g, "ī"],
      [/w([ie])/g, "$1"]
    ]
  nihonshiki: [
      [/n\'([^aiueoy]|$)/g, "n$1"],
      [/xtu(.)/g, "$1$1"],
      [/ixy/g, "y"],
      [/o[ou\-]/g, "ô"],
      [/u[u\-]/g, "û"],
      [/a[a\-]/g, "â"],
      [/e[e\-]/g, "ê"],
      [/i\-/g, "î"]
    ]
  kunreishiki: [
      [/n\'([^aiueoy]|$)/g, "n$1"],
      [/xtu(.)/g, "$1$1"],
      [/ixy/g, "y"],
      [/z([iuy])/g, "j$1"],
      [/o[ou\-]/g, "ô"],
      [/u[u\-]/g, "û"],
      [/a[a\-]/g, "â"],
      [/e[e\-]/g, "ê"],
      [/i\-/g, "î"],
      [/w([ieo])/g, "$1"]
    ]
  jsl: [
      [/n\'([^aiueoy]|$)/g, "n$1"],
      [/xtu(.)/g, "$1$1"],
      [/ixy/g, "y"],
      [/o[u\-]/g, "oo"],
      [/u\-/g, "uu"],
      [/a\-/g, "aa"],
      [/e[i\-]/g, "ee"],
      [/i\-/g, "ii"]
    ]
