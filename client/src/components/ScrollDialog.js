import React, { useEffect, useContext, useRef } from "react";
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { useTheme } from '@material-ui/core/styles';
import {SocketContext} from './socket';
import { fit } from 'furigana';
import {formatDefinitions} from './commonFunctions';
import {getRuby} from './commonFunctions';
const xregexp = require("xregexp")

export default function ScrollDialog(props) {
  const socket = useContext(SocketContext);
  const [read, setRead] = React.useState("Loading...");
  const [currentToken, setCurrentToken] = React.useState(null);
  const [pos, setPos] = React.useState(null);
  const [selected, setSelected] = React.useState(0);
  const [definitions, setDefinitions] = React.useState(null);
  const [firstLoad, setFirstLoad] = React.useState(true);
  var hiraRx = new xregexp("^[-\\p{Hiragana}]+$");
  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down('sm'));
  const scrollBox = useRef(null);

  React.useEffect(() => {
    socket.on('rikaiMiniResult', (res) => {
      console.log("rikaiMiniResult")
      if (res) {
        formatDefinitions(res, setDefinitions, null)
        // console.log(res['data'])
        // setDefinitions(res['data'])
      } else {
        console.log('no match found')
        setDefinitions("No match found.")
      }
    })
  }, []);

  const handelClosePre = () => {
    setRead("Loading...");
    setCurrentToken(null);
    props.setDialogTokens([]);
    setPos(null);
    setSelected(0);
    setDefinitions(null);
    props.setDefinitions(null);
    // setRead(null);
    // setCurrentToken(null);
    setFirstLoad(true);
    // alert('RESET!')
    props.handleClose();
  }

  React.useEffect(async () => {
    if (!currentToken && props.open && firstLoad) {
      await setCurrentToken(props.dialogTokens[0])
      await setSelected(0)
      if (props.dialogTokens[0]) {
        let genkei = props.dialogTokens[0][8]
        let surface = props.dialogTokens[0][0]
        // alert(`updating current token to ${props.dialogTokens[0][0]}`)
        if (genkei != '*') {
          console.log(genkei, selected)                 
          await socket.emit('rikaiMini', genkei)
        } else {
          console.log(surface, selected)
          await socket.emit('rikaiMini', surface)
        }
      }
      setFirstLoad(false);
    }
    await updateDialogTokens();
    await updatePos();
  }, [props.dialogTokens, selected]);

  const updatePos = () => {
    console.log(`updatePos for currentToken: ${currentToken}`)
    if (currentToken) {
      let pos = currentToken[2] ? <span><b>Part of speech: </b>{[currentToken[2],currentToken[3],currentToken[4],currentToken[5]].filter(Boolean).join(', ')}</span> : null;
      let conjugationType = currentToken[6] ? <span><br /><b>Conjugation type: </b>{currentToken[6]}</span> : null;
      let conjugationForm = currentToken[7] ? <span><br /><b>Conjugation form: </b>{currentToken[7]}</span> : null;
      let unconjugated = currentToken[8] != '*' && currentToken[8] != currentToken[0] ? <span><br /><b>Unconjugated: </b>{currentToken[8]}</span> : null;
      setPos(<div id="pos">{pos}{conjugationType}{conjugationForm}{unconjugated}</div>);
    }
  }

  const updateDialogTokens = () => {
    if (props.dialogTokens) {
      // setCurrentToken(props.dialogTokens[0]);
      // console.log(props.dialogTokens);

      let newRead = [];
      let counter = 0;

      props.dialogTokens.forEach((token, index) => {
        let surface = token[0];
        let reading = token[1];
        let pos = token[2];
        let pos1 = token[3];
        let pos2 = token[4];
        let pos3 = token[5];
        let ctype = token[6];
        let cform = token[7];
        let genkei = token[8];
        let fragment = getRuby(surface, reading)
        let theMatch = fragment.match(/[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]/)

        if (index == 0) {
          console.log(`updatePos for token: ${pos} ${pos1} ${pos2} ${pos3} ${ctype} ${cform} ${genkei}`)
          // console.log(ctype)
          let newPos = pos ? <span><b>Part of speech: </b>{[pos,pos1,pos2,pos3].filter(Boolean).join(', ')}</span> : null;
          // console.log(newPos)
          let conjugationType = token[6] ? <span><br /><b>Conjugation type: </b>{token[6]}</span> : null;
          let conjugationForm = token[7] ? <span><br /><b>Conjugation form: </b>{token[7]}</span> : null;
          let unconjugated = token[8] != '*' && token[8] != token[0] ? <span><br /><b>Unconjugated: </b>{token[8]}</span> : null;
          setPos(<div id="pos">{newPos}{conjugationType}{conjugationForm}{unconjugated}</div>);
        }

        // if (firstLoad) {
        //   alert(selected)
        // }

        if (theMatch && theMatch[0].trim() != '') {
          newRead.push((
            <span
              key={counter++}
              // className={["tooltip", index == selected ? 'rikai-highlight': null].join(' ')}
              className={['tooltip', index == selected ? 'rikai-highlight' : null].join(' ')}
              id={"scroll-tooltip-" + index}
              onClick={(e) => {
                scrollBox.current?.scrollTo(0,0);
                setSelected(index);
                if (genkei != '*') {
                  console.log(genkei, selected)                 
                  socket.emit('rikaiMini', genkei)
                } else {
                  console.log(surface, selected)
                  socket.emit('rikaiMini', surface)
                }
                setCurrentToken(token)
              }}
              dangerouslySetInnerHTML={{__html: fragment}}
              ></span>
          ));
        } else {
          newRead.push((
            <span key={counter++} class="tooltip2">{fragment}</span>
          ))
        }
      })
      if (newRead.length > 0) {
        setRead(newRead);
      }
    }
  };

  return (
    <div>
      {/* <Button onClick={props.handleClickOpen}>scroll=paper</Button> */}
      <Dialog
        open={props.open}
        onClose={handelClosePre}
        scroll='paper'
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
        // fullScreen={fullScreen}
      >
        <DialogTitle id="scroll-dialog-title">{read}<br />{pos}</DialogTitle>
        <DialogContent ref={scrollBox} className="dialogContent" dividers={true}>
          {/* {definitions ? definitions.join(<br />) : 'Loading...'} */}
          {/* <List component="nav">
            {definitions ? definitions
              .map(definition => <><ListItem button>{definition}</ListItem><Divider /></>) : "Loading..."}
          </List> */}
          {/* <DialogContentText
            id="scroll-dialog-description"
          >
            {[...new Array(50)]
              .map(
                () => `Cras mattis consectetur purus sit amet fermentum.
Cras justo odio, dapibus ac facilisis in, egestas eget quam.
Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
Praesent commodo cursus magna, vel scelerisque nisl consectetur et.`,
              )
              .join('\n')}
            <List component="nav">
              {["<span><ruby>悪<rt>あく</rt></ruby><ruby>戯<rt>ぎ</rt></ruby></span>", 'right', 'top', 'bottom'].map((label) => (
                <React.Fragment key={label}>
                  <ListItem button>
                    <p dangerouslySetInnerHTML={{__html: label}}><b></b></p>
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          </DialogContentText> */}
          {definitions}
        </DialogContent>
        <DialogActions>
          <Button onClick={handelClosePre} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}