import React, { useEffect, useContext } from "react";
import IconButton from '@material-ui/core/IconButton';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';
// import Tooltip from '@material-ui/core/Tooltip';
// import { isJapanese, isKanji, isKana } from 'wanakana';
import {SocketContext} from './socket';
import ClickAwayListener from '@material-ui/core/ClickAwayListener';
import { fit } from 'furigana';
import {getRuby, hasJapanese} from './commonFunctions';

export default function TooltipView(props) {
  const socket = useContext(SocketContext);
  const [value, setValue] = React.useState(props.value);
  const [read, setRead] = React.useState([]);
  
  let test = `痛める [やめる] /(v1,vi) (arch) to hurt/to ache/

  廃める [やめる] /(v1,vt) (uk) to cancel/to abandon/to give up/to abolish/to abstain/to refrain/

  止める [やめる] /(v1,vt) (1) (uk) to stop (an activity)/to cease/to discontinue/to end/to quit/(2) (uk) to cancel/to abandon/to give up/to abolish/to abstain/to refrain/(P)/

  病める [やめる] /(exp,adj-f) (1) sick/ill/ailing/(v1,vi) (2) (arch) to hurt/to ache/

  罷める [やめる] /(v1,vt) to resign/to retire/to quit/to leave (one's job, etc.)/

  辞める [やめる] /(v1,vt) to resign/to retire/to quit/to leave (one's job, etc.)/(P)/

  退める [やめる] /(iK) (v1,vt) to resign/to retire/to quit/to leave (one's job, etc.)/

  已める [やめる] /(v1,vt) (1) (uk) to stop (an activity)/to cease/to discontinue/to end/to quit/(2) (uk) to cancel/to abandon/to give up/to abolish/to abstain/to refrain/`

  // useEffect(async () => {
  //   socket.on('rikaiResult', (msg) => {
  //     console.log(`Received rikaiResult: ${msg}`)
  //   });
  // }, []);

  useEffect(async () => {
    // console.log(props.reader)

    let surfaceLines = props.reader[0]
    let readingLines = props.reader[1]

    let newRead = []
    let counter = 0;
    for (let i = 0; i < surfaceLines.length; i++) {
      let line = surfaceLines[i]
      let reading = readingLines[i]
      for (let j = 0; j < line.length; j++) {
        let chunkTokens = line[j]
        let chunkReadings = reading[j]
        // console.log(chunkTokens)
        // console.log(chunkReadings)

        let actualFragment = ''

        chunkTokens.forEach((token, index) => {
          let reading = chunkReadings[index]
          // console.log(token, getRuby(token, reading))
          // console.log(token, reading)
          actualFragment += getRuby(token, reading)
        })

        actualFragment += '</ruby>'

        // console.log(actualFragment)

        let fragment = chunkTokens.join('')

        // let theMatch = fragment.match(/[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]/)

        if (fragment === 'Loading...') {
          break;
        } else {
          setRead("Loading...")
        }
        
        let test = await hasJapanese(fragment)
        // console.log(`${fragment} HAS JAPANESE:${test}`)

        if (test) {
          newRead.push((
            <span
              key={counter++}
              className="tooltip "
              onClick={(e) => {
                props.setOpenDialog(true)
                // console.log(`openDialog:${props.openDialog}`)
                // setTimeout(() => {
                //   socket.emit('tokenizeFragment', fragment)
                // }, 500);
                socket.emit('tokenizeFragment', fragment)
                // console.log(fragment)
              }}
              dangerouslySetInnerHTML={{ __html: actualFragment }}
            >
            </span>
          ))
        } else {
          newRead.push((
            <span key={counter++} className="tooltip2">{fragment}</span>
          ))
        }
        let trimmed = line.join('').trim()
        if (j == line.length - 1 && fragment.trim() != '' && trimmed.length > 0 && trimmed != 'Loading...' && test) {
          newRead.push(
          <IconButton
            color="primary"
            size="small"
            className="rikaiButton"
            onClick={(e) => {
              props.setOpenRikaiDialog(true)
              let actualLine = "";
              line.forEach((chunk, index) => {
                actualLine += chunk.join('')
              })
              // console.log(actualLine)
              props.setRikaiString(actualLine)
            }}
            aria-label="rikai mode">
            <HelpOutlineIcon />
          </IconButton>)
        }
      }
      newRead.push(<br />)
      // if (i % 2 == 1) {
      //   newRead.push(<br />)
      // }
    }
    setRead(newRead)
  }, [props.reader]);

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <div id="readContainer">
      <div>
        {read}
      </div>
    </div>
  );
}