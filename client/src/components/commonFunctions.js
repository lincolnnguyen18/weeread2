import React, { useContext } from "react";
const { fit } = require('furigana');
// const xregexp = require("xregexp");
// var hiraRx = new xregexp("^[-\\p{Hiragana}]+$");
// var containsKanjiRx = new xregexp("^[-\\w\\p{Han}]+$");
const unicode = require('unicode-regex');
const hiraRx = unicode({ Script_Extensions: ['Hiragana'] }).toRegExp();
const kataRx = unicode({ Script_Extensions: ['Katakana'] }).toRegExp();
const hanRx = unicode({ Script_Extensions: ['Han'] }).toRegExp();

export const hasJapanese = (string) => {
  return string.split('').some((char) => {
    if (hiraRx.test(char) && char !== '・') {
      // console.log(`${char} in ${string} is hira`);
      return true;
    } else if (kataRx.test(char) && char !== '・') {
      // console.log(`${char} in ${string} is kata`);
      return true;
    } else if (hanRx.test(char) && char !== '・') {
      // console.log(`${char} in ${string} is han`);
      return true;
    }
  })
}

export const hasOnlyHiragana = (string) => {
  string.split('').forEach((char) => {
    if (!hiraRx.test(char)) {
      return false;
    }
  })
  return true;
}

export const containsKanji = (string) => {
  // return xregexp.test(string, containsKanjiRx);
  return hanRx.test(string);
}

export const formatDefinitions = (definitions, setDefinitions, setMatchLen) => {
  let res = definitions;
  // console.log(res)
  let newDefinitions = []
  let newDefinitions2 = []
  if (res) {
    // console.log(res['matchLen'])
    if (setMatchLen) {
      setMatchLen(res['matchLen'])
    }
    // console.log(`Rikai result: ${res['data']}`)
    // console.log(res['data'])
    let test = []
    res['data'].forEach((item) => {
      let definition = item[0]
      let conjugation = item[1]
      // console.log(`OLD LABEL: ${conjugation}`)
      let label = conjugation ? '(' + conjugation.replace(/&lt;/g,'<') + ')' : ""
      // console.log(`NEW LABEL: ${label}`)
      let reading = definition.match(/ \[(.+)\] \//);
      if (reading) {
        reading = reading[1]
      } else {
        reading = null
      }
      let kanji = definition.split(' ')[0]
      // console.log(kanji, reading)
      let splitted = definition.split(/\s*[\/+]+/);
      let pieces = splitted[0].split(' ');
      if (reading) {
        kanji = getRuby(kanji, reading)
      }
      let sliced = splitted.slice(1, splitted.length).filter(Boolean).join('; ');
      // console.log("NEW DEFINITIONS:")
      // console.log(kanji, label)
      let tags = [...sliced.matchAll(/\(([\w]+)\)/gm)]
      let hasP = false
      // tags.forEach(tag => {
      //   console.log(tag[0], tag[1])
      //   if (tag[1] === 'P') {
      //     console.log('HERE')
      //     hasP = true
      //   }
      // });
      // console.log(hasP)
      if (hasP) {
        newDefinitions.push(<p><span dangerouslySetInnerHTML={{__html:kanji}}></span> <span className="label">{label}</span><br /><span className="definitions">{sliced}</span></p>)
      } else {
        newDefinitions2.push(<p><span dangerouslySetInnerHTML={{__html:kanji}}></span> <span className="label">{label}</span><br /><span className="definitions">{sliced}</span></p>)
      }
    });
    // console.log('SORT THESE')
    // console.log(newDefinitions)
    // console.log(newDefinitions2)
    // setDefinitions(res['data'])
    setDefinitions(newDefinitions.concat(newDefinitions2))
  } else {
    // console.log('no match found')
    setDefinitions("No match found.")
  }
}

// 取[と]り 寄[よ]せる
// <ruby>取<rt>と</rt>り</ruby>
// <ruby>寄<rt>よ</rt>せる</ruby>
export const getRuby = (string, reading) => {
  // return string
  // Ensure string only has kanji, kana, and numbers
  try {
    if (hasOnlyHiragana(reading)) {
      // console.log(`try fitting ${string} with${reading}`);
      let fitted = fit(string, reading);
      if (fitted != string) {
        let result = "<ruby>"
        let pieces = fitted.split(' ')
        // console.log(pieces)
        pieces.forEach((piece, index) => {
          piece = piece.replaceAll('[', '<rt>');
          piece = piece.replaceAll(']', '</rt>');
          result += `${piece}</ruby>`
          if (index < pieces.length - 1) {
            result += '<ruby>'
          }
        })
        return result
      }
    }
    return string
  } catch (e) {
    // console.log(e);
    return string
  }
}