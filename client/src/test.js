const unicode = require('unicode-regex');
const hiraRx = unicode({ Script_Extensions: ['Hiragana'] }).toRegExp();
const kataRx = unicode({ Script_Extensions: ['Katakana'] }).toRegExp();
const hanRx = unicode({ Script_Extensions: ['Han'] }).toRegExp();

const hasJapanese = (string) => {
  return string.split('').some((char) => {
    if (hiraRx.test(char) && char !== '・') {
      console.log(`${char} in ${string} is hira`);
      return true;
    } else if (kataRx.test(char) && char !== '・') {
      console.log(`${char} in ${string} is kata`);
      return true;
    } else if (hanRx.test(char) && char !== '・') {
      console.log(`${char} in ${string} is han`);
      return true;
    }
  })
}

console.log(hasJapanese('おはよう'))