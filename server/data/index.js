const fs = require('fs');

function RcxDict() {}
RcxDict.prototype = {
  config: {},
  fileReadAsync: function (url, asArray) {
    return fs.readFileSync(url, "utf8", (err, res) => {
      if (!asArray) {
        return res;
      } else {
        const array = res
          .split('\n')
          .filter((o) => o && o.length > 0)
        console.log(array)
      }
    });
  },
  loadDIF: function () {
    this.difReasons = [];
    this.difRules = [];
    this.difExact = [];

    let buffer = this.fileReadAsync(
      './deinflect.dat',
      true
    ).split('\n')
    let prevLen = -1;
    let g;
    let o;
    
    
    // i = 1: skip header
    for (let i = 1; i < buffer.length; ++i) {
      const f = buffer[i].split('\t');

      if (f.length === 1) {
        this.difReasons.push(f[0]);
      } else if (f.length === 4) {
        o = {};
        o.from = f[0];
        o.to = f[1];
        o.type = f[2];
        o.reason = f[3];

        if (prevLen !== o.from.length) {
          prevLen = o.from.length;
          g = [];
          g.flen = prevLen;
          this.difRules.push(g);
        }
        g.push(o);
      }
    }
  },
  loadFileToTarget: function (file, isArray, target) {
    const url = './' + file;

    let data = this.fileReadAsync(url, isArray)
    this[target] = data;
    console.log('async read complete for ' + target);
  },
  loadDictionary: function (includeNames) {
    this.loadFileToTarget('./dict.dat', false, 'wordDict');
    this.loadFileToTarget('./dict.idx', false, 'wordIndex');
    this.loadFileToTarget('./kanji.dat', false, 'kanjiData');
    this.loadFileToTarget('./radicals.dat', true, 'radData');
    if (includeNames) {
      this.loadFileToTarget('./names.dat', true, 'nameDict');
      this.loadFileToTarget('./names.idx', false, 'nameIndex');
    }
  },
  init: function (loadNames) {
    this.loadDictionary(loadNames);
    this.loadDIF();
  }, 
  find: function (data, text) {
    const tlen = text.length;
    let beg = 0;
    let end = data.length - 1;
    let i;
    let mi;
    let mis;

    while (beg < end) {
      mi = (beg + end) >> 1;
      i = data.lastIndexOf('\n', mi) + 1;

      mis = data.substr(i, tlen);
      if (text < mis) end = i - 1;
      else if (text > mis) beg = data.indexOf('\n', mi + 1) + 1;
      else return data.substring(i, data.indexOf('\n', mi + 1));
    }
    return null;
  },
  loadNames: function () {
    if (this.nameDict && this.nameIndex) return;
    this.nameDict = this.fileRead('./names.dat');
    this.nameIndex = this.fileRead('./names.idx');
  },
  deinflect: function (word) {
    const r = [];
    const have = [];
    let o;

    o = {};
    o.word = word;
    o.type = 0xff;
    o.reason = '';
    // o.debug = 'root';
    r.push(o);
    have[word] = 0;

    let i;
    let j;
    let k;

    i = 0;
    do {
      word = r[i].word;
      const wordLen = word.length;
      const type = r[i].type;

      // console.log(this.difRules)

      for (j = 0; j < this.difRules.length; ++j) {
        const g = this.difRules[j];
        if (g.flen <= wordLen) {
          const end = word.substr(-g.flen);
          for (k = 0; k < g.length; ++k) {
            const rule = g[k];
            if (type & rule.type && end === rule.from) {
              const newWord =
                word.substr(0, word.length - rule.from.length) + rule.to;
              if (newWord.length <= 1) continue;
              o = {};
              if (have[newWord] !== undefined) {
                o = r[have[newWord]];
                o.type |= rule.type >> 8;

                // o.reason += ' / ' + r[i].reason + ' ' +
                // this.difReasons[rule.reason]; o.debug += ' @ ' + rule.debug;
                continue;
              }
              have[newWord] = r.length;
              if (r[i].reason.length)
                o.reason =
                  this.difReasons[rule.reason] + ' &lt; ' + r[i].reason;
              else o.reason = this.difReasons[rule.reason];
              o.type = rule.type >> 8;
              o.word = newWord;
              // o.debug = r[i].debug + ' $ ' + rule.debug;
              r.push(o);
            }
          }
        }
      }
    } while (++i < r.length);

    return r;
  },

  // katakana -> hiragana conversion tables
  ch: [
    0x3092,
    0x3041,
    0x3043,
    0x3045,
    0x3047,
    0x3049,
    0x3083,
    0x3085,
    0x3087,
    0x3063,
    0x30fc,
    0x3042,
    0x3044,
    0x3046,
    0x3048,
    0x304a,
    0x304b,
    0x304d,
    0x304f,
    0x3051,
    0x3053,
    0x3055,
    0x3057,
    0x3059,
    0x305b,
    0x305d,
    0x305f,
    0x3061,
    0x3064,
    0x3066,
    0x3068,
    0x306a,
    0x306b,
    0x306c,
    0x306d,
    0x306e,
    0x306f,
    0x3072,
    0x3075,
    0x3078,
    0x307b,
    0x307e,
    0x307f,
    0x3080,
    0x3081,
    0x3082,
    0x3084,
    0x3086,
    0x3088,
    0x3089,
    0x308a,
    0x308b,
    0x308c,
    0x308d,
    0x308f,
    0x3093,
  ],
  cv: [
    0x30f4,
    0xff74,
    0xff75,
    0x304c,
    0x304e,
    0x3050,
    0x3052,
    0x3054,
    0x3056,
    0x3058,
    0x305a,
    0x305c,
    0x305e,
    0x3060,
    0x3062,
    0x3065,
    0x3067,
    0x3069,
    0xff85,
    0xff86,
    0xff87,
    0xff88,
    0xff89,
    0x3070,
    0x3073,
    0x3076,
    0x3079,
    0x307c,
  ],
  cs: [0x3071, 0x3074, 0x3077, 0x307a, 0x307d],

  wordSearch: function (word, doNames, max) {
    let i;
    let u;
    let v;
    let r;
    let p;
    const trueLen = [0];
    const entry = {};

    // half & full-width katakana to hiragana conversion
    // note: katakana vu is never converted to hiragana

    p = 0;
    r = '';
    for (i = 0; i < word.length; ++i) {
      u = v = word.charCodeAt(i);

      // // Skip Zero-width non-joiner used in Google Docs between every
      // // character.
      // if (u === 8204) {
      //   p = 0;
      //   continue;
      // }

      if (u <= 0x3000) break;

      // full-width katakana to hiragana
      if (u >= 0x30a1 && u <= 0x30f3) {
        u -= 0x60;
      } else if (u >= 0xff66 && u <= 0xff9d) {
        // half-width katakana to hiragana
        u = this.ch[u - 0xff66];
      } else if (u === 0xff9e) {
        // voiced (used in half-width katakana) to hiragana
        if (p >= 0xff73 && p <= 0xff8e) {
          r = r.substr(0, r.length - 1);
          u = this.cv[p - 0xff73];
        }
      } else if (u === 0xff9f) {
        // semi-voiced (used in half-width katakana) to hiragana
        if (p >= 0xff8a && p <= 0xff8e) {
          r = r.substr(0, r.length - 1);
          u = this.cs[p - 0xff8a];
        }
      } else if (u === 0xff5e) {
        // ignore J~
        p = 0;
        continue;
      }

      r += String.fromCharCode(u);
      // need to keep real length because of the half-width semi/voiced
      // conversion
      trueLen[r.length] = i + 1;
      p = v;
    }
    word = r;

    let dict;
    let index;
    let maxTrim;
    const cache = [];
    const have = [];
    let count = 0;
    let maxLen = 0;

    if (doNames) {
      // check: split this

      this.loadNames();
      dict = this.nameDict;
      index = this.nameIndex;
      maxTrim = 20; // this.config.namax;
      entry.names = 1;
      console.log('doNames');
    } else {
      dict = this.wordDict;
      index = this.wordIndex;
      maxTrim = 7;
    }

    if (max != null) maxTrim = max;

    entry.data = [];

    while (word.length > 0) {
      const showInf = count !== 0;
      let trys;

      if (doNames) trys = [{ word: word, type: 0xff, reason: null }];
      else trys = this.deinflect(word);

      for (i = 0; i < trys.length; i++) {
        u = trys[i];

        let ix = cache[u.word];
        if (!ix) {
          ix = this.find(index, u.word + ',');
          if (!ix) {
            cache[u.word] = [];
            continue;
          }
          ix = ix.split(',');
          cache[u.word] = ix;
        }

        for (let j = 1; j < ix.length; ++j) {
          const ofs = ix[j];
          if (have[ofs]) continue;

          const dentry = dict.substring(ofs, dict.indexOf('\n', ofs));

          let ok = true;
          if (i > 0) {
            // > 0 a de-inflected word

            // ex:
            // /(io) (v5r) to finish/to close/
            // /(v5r) to finish/to close/(P)/
            // /(aux-v,v1) to begin to/(P)/
            // /(adj-na,exp,int) thank you/many thanks/
            // /(adj-i) shrill/

            let w;
            const x = dentry.split(/[,()]/);
            const y = u.type;
            let z = x.length - 1;
            if (z > 10) z = 10;
            for (; z >= 0; --z) {
              w = x[z];
              if (y & 1 && w === 'v1') break;
              if (y & 4 && w === 'adj-i') break;
              if (y & 2 && w.substr(0, 2) === 'v5') break;
              if (y & 16 && w.substr(0, 3) === 'vs-') break;
              if (y & 8 && w === 'vk') break;
            }
            ok = z !== -1;
          }
          if (ok) {
            if (count >= maxTrim) {
              entry.more = 1;
            }

            have[ofs] = 1;
            ++count;
            if (maxLen === 0) maxLen = trueLen[word.length];

            if (trys[i].reason) {
              if (showInf) r = '&lt; ' + trys[i].reason + ' &lt; ' + word;
              else r = '&lt; ' + trys[i].reason;
            } else {
              r = null;
            }

            entry.data.push([dentry, r]);
          }
        } // for j < ix.length
        if (count >= maxTrim) break;
      } // for i < trys.length
      if (count >= maxTrim) break;
      word = word.substr(0, word.length - 1);
    } // while word.length > 0

    if (entry.data.length === 0) return null;

    entry.matchLen = maxLen;
    return entry;
  },
  translate: function (text) {
    let e;
    const o = {};
    let skip;

    o.data = [];
    o.textLen = text.length;

    while (text.length > 0) {
      e = this.wordSearch(text, false, 1);
      if (e != null) {
        if (o.data.length >= 7) {
          o.more = 1;
          break;
        }
        //				o.data = o.data.concat(e.data);
        o.data.push(e.data[0]);
        skip = e.matchLen;
      } else {
        skip = 1;
      }
      text = text.substr(skip, text.length - skip);
    }

    if (o.data.length === 0) {
      return null;
    }

    o.textLen -= text.length;
    return o;
  },
  bruteSearch: function (text, doNames) {
    let r;
    let d;
    let j;
    let wb;
    let we;
    let max;

    r = 1;
    if (text.charAt(0) === ':') {
      text = text.substr(1, text.length - 1);
      if (text.charAt(0) !== ':') r = 0;
    }
    if (r) {
      if (text.search(/[\u3000-\uFFFF]/) !== -1) {
        wb = we = '[\\s\\[\\]]';
      } else {
        wb = '[\\)/]\\s*';
        we = '\\s*[/\\(]';
      }
      if (text.charAt(0) === '*') {
        text = text.substr(1, text.length - 1);
        wb = '';
      }
      if (text.charAt(text.length - 1) === '*') {
        text = text.substr(0, text.length - 1);
        we = '';
      }
      text =
        wb +
        text.replace(/[[\\^$.|?*+()]/g, function (c) {
          return '\\' + c;
        }) +
        we;
    }

    const e = { data: [], reason: [], kanji: 0, more: 0 };

    if (doNames) {
      e.names = 1;
      max = 20; // this.config.namax;
      this.loadNames();
      d = this.nameDict;
    } else {
      e.names = 0;
      max = 7;
      d = this.wordDict;
    }

    r = new RegExp(text, 'igm');
    while (r.test(d)) {
      if (e.data.length >= max) {
        e.more = 1;
        break;
      }
      j = d.indexOf('\n', r.lastIndex);
      e.data.push([
        d.substring(d.lastIndexOf('\n', r.lastIndex - 1) + 1, j),
        null,
      ]);
      r.lastIndex = j + 1;
    }

    return e.data.length ? e : null;
  },

  kanjiSearch: function (kanji) {
    const hex = '0123456789ABCDEF';
    let i;

    i = kanji.charCodeAt(0);
    if (i < 0x3000) return null;

    const kde = this.find(this.kanjiData, kanji);
    if (!kde) return null;

    const a = kde.split('|');
    if (a.length !== 6) return null;

    const entry = {};
    entry.kanji = a[0];

    entry.misc = {};
    entry.misc.U =
      hex[(i >>> 12) & 15] +
      hex[(i >>> 8) & 15] +
      hex[(i >>> 4) & 15] +
      hex[i & 15];

    const b = a[1].split(' ');
    for (i = 0; i < b.length; ++i) {
      if (b[i].match(/^([A-Z]+)(.*)/)) {
        if (!entry.misc[RegExp.$1]) {
          entry.misc[RegExp.$1] = RegExp.$2;
        } else {
          entry.misc[RegExp.$1] += ' ' + RegExp.$2;
        }
        // format heisig keyword additions prettily
        if (RegExp.$1.startsWith('L')) {
          entry.misc[RegExp.$1] = entry.misc[RegExp.$1].replace(/[:_]/g, ' ');
        }
      }
    }

    entry.onkun = a[2].replace(/\s+/g, '\u3001 ');
    entry.nanori = a[3].replace(/\s+/g, '\u3001 ');
    entry.bushumei = a[4].replace(/\s+/g, '\u3001 ');
    entry.eigo = a[5];

    return entry;
  },

  kanjiInfoLabelList: [
    /*
				'C', 	'Classical Radical',
				'DR',	'Father Joseph De Roo Index',
				'DO',	'P.G. O\'Neill Index',
				'O', 	'P.G. O\'Neill Japanese Names Index',
				'Q', 	'Four Corner Code',
				'MN',	'Morohashi Daikanwajiten Index',
				'MP',	'Morohashi Daikanwajiten Volume/Page',
				'K',	'Gakken Kanji Dictionary Index',
				'W',	'Korean Reading',
		*/
    'H',
    'Halpern',
    'L',
    'Heisig 5th Edition',
    'DN',
    'Heisig 6th Edition',
    'E',
    'Henshall',
    'DK',
    'Kanji Learners Dictionary',
    'N',
    'Nelson',
    'V',
    'New Nelson',
    'Y',
    'PinYin',
    'P',
    'Skip Pattern',
    'IN',
    'Tuttle Kanji &amp; Kana',
    'I',
    'Tuttle Kanji Dictionary',
    'U',
    'Unicode',
  ],
};

// Usage:
let dict = new RcxDict();
// array = dict.fileReadAsync('./dict.dat', true)
// console.log(array)
// dict.loadFileToTarget('dict.dat', false, 'wordDict');
// console.log(dict['wordDict']);
// dict.loadDIF();
// dict.init(true);
dict.init(false)
text = 'では酒が大いに不味くなることだろう'
e = dict.wordSearch(text, false);
// e = dict.deinflect(text);
console.log(e)