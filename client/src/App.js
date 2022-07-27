import React, { useEffect } from "react";
import {SocketContext, socket} from './components/socket';
// import StatusAccordion from './components/StatusAccordion';
import TextArea from './components/TextArea';
import TooltipView from './components/TooltipView';
import ScrollDialog from "./components/ScrollDialog";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import RikaiDialog from './components/RikaiDialog';
import {getRuby} from './components/commonFunctions';
import {formatDefinitions, hasJapanese, hasOnlyHiragana} from './components/commonFunctions';
import './App.css';
// import Kuroshiro from "kuroshiro";
// import KuromojiAnalyzer from "kuroshiro-analyzer-kuromoji";
import { disableBodyScroll, enableBodyScroll, clearAllBodyScrollLocks } from 'body-scroll-lock';

function App() {
  // const [value, setValue] = React.useState(`具体的には、今説明したメリットを享受(きょうじゅ)するためには、１００日ごとに魂のエネルギーの一定額を納めてもらうことになる。いわば、家賃の支払いだな。
  // Specifically, in order to enjoy the benefits I just described, you will be asked to pay a certain amount of your soul energy every 100 days. In other words, it's a rent payment.`);
  const [value, setValue] = React.useState(`やはり、此方をじぃと見つめながら頬をあげるエルディスは、何処までも悪戯げだ。息を、漏らす。吐息はすぐさま白色に変色し、そうして風に流されるように宙に散った。
  I'm not sure what to make of it, but I think it's a good idea. I'm not sure what to say. I'm not sure what to make of that.
  やめよう、とてもではないが小手先だけでは言いくるめられる様子ではない。エルディスも女王としての責務をこなしていく内、随分と口先が達者になったらしい。塔にいた頃と違い、やけにその舌が回る。下手に踏み込めば手痛い仕返しを食らうかもしれない。
  I don't want to do this, but I don't think I can be talked into it with just a few tricks. It seems that Erdis has become much more eloquent in the course of her duties as queen. Unlike when she was in the tower, her tongue was spinning. If she were to step in unwisely, she might suffer a painful reprisal.
  それに、もはやフリムスラト山脈の背、その中頃を踏み抜いているのだ。此処から一人でお帰り願って、そうして何処かで遭難されました、では酒が大いに不味くなることだろう。
  Besides, we are now stepping over the back of the Flimsulat Mountains, in the middle of them. If I had to ask you to go home alone from here, and then you got lost somewhere, the drink would have tasted very bad.`);
  const [openDialog, setOpenDialog] = React.useState(false);
  const [openRikaiDialog, setOpenRikaiDialog] = React.useState(false);
  const [definitions, setDefinitions] = React.useState("Loading...");
  const [matchLen, setMatchLen] = React.useState(null);
  const [reader, setReader] = React.useState([[[]], [[]]]);
  const [dialogTokens, setDialogTokens] = React.useState([]);
  const [rikaiString, setRikaiString] = React.useState("");

  useEffect(async () => {
    // let test = await hasJapanese(socket, 'Besides, we are now stepping over the back of the Flimsulat Mountains, in the middle of them. If I had to ask you to go home alone from here, and then you got lost somewhere, the drink would have tasted very bad.')
    // let test = await hasOnlyHiragana(socket, 'See for yourself if the Karubonara (・・・・・・) of Konbini (・・・・) exists.')
    // console.log(test)
    socket.on('message', (msg) => {
      // console.log(`Received message: ${msg}`)
    });
    socket.on('tokenizeResult', async (res) => {
      setReader(res);
    });
    socket.on('tokenizeFragmentResult', async (res) => {
      // console.log(res)
      setDialogTokens(res)
      // res.forEach((token) => {
      //   console.log(token)
      // })
    });
    socket.on('rikaiResult', async (res) => {
      formatDefinitions(res, setDefinitions, setMatchLen);
    //   console.log(res)
    //   let newDefinitions = []
    //   if (res) {
    //     console.log(res['matchLen'])
    //     setMatchLen(res['matchLen'])
    //     console.log(`Rikai result: ${res['data']}`)
    //     console.log(res['data'])
    //     let test = []
    //     res['data'].forEach((item) => {
    //       let definition = item[0]
    //       let conjugation = item[1]
    //       console.log(`OLD LABEL: ${conjugation}`)
    //       let label = conjugation ? '(' + conjugation.replace(/&lt;/g,'<') + ')' : ""
    //       console.log(`NEW LABEL: ${label}`)
    //       let reading = definition.match(/ \[(.+)\] \//);
    //       if (reading) {
    //         reading = reading[1]
    //       } else {
    //         reading = null
    //       }
    //       let kanji = definition.split(' ')[0]
    //       console.log(kanji, reading)
    //       let splitted = definition.split(/\s*[\/+]+/);
    //       let pieces = splitted[0].split(' ');
    //       if (reading) {
    //         kanji = getRuby(kanji, reading)
    //       }
    //       let definitions = splitted.slice(1, splitted.length).filter(Boolean).join('; ');
    //       console.log("NEW DEFINITIONS:")
    //       console.log(kanji, label)
    //       newDefinitions.push(<p><span dangerouslySetInnerHTML={{__html:kanji}}></span> <span className="label">{label}</span><br /><span className="definitions">{definitions}</span></p>)
    //       // newDefinitions.push((<ListItem button>{<ListItemText primary="Inbox" />}</ListItem>));
    //     });
    //     // setDefinitions(res['data'])
    //     setDefinitions(newDefinitions)
    //   } else {
    //     console.log('no match found')
    //     setDefinitions("No match found.")
    //   }
    });
  }, []);

  return (
    <SocketContext.Provider value={socket}>
      <div id="appContainer">
          {/* <StatusAccordion id="statusAccordion" /> */}
          <TextArea value={value} setReader={setReader} />
          <TooltipView reader={reader} setRikaiString={setRikaiString} openDialog={openDialog} setOpenDialog={setOpenDialog} openRikaiDialog={openRikaiDialog} setOpenRikaiDialog={setOpenRikaiDialog} />
          <ScrollDialog
            id="scrollDialog"
            open={openDialog}
            handleOpen={() => {
              setOpenDialog(true)
              disableBodyScroll(document.querySelector('#scrollDialog'))
            }}
            handleClose={() => {
              setOpenDialog(false)
              enableBodyScroll(document.querySelector('#scrollDialog'))
            }}
            dialogTokens={dialogTokens}
            setDialogTokens={setDialogTokens}
            definitions={definitions}
            setDefinitions={setDefinitions} />
          <RikaiDialog
            id="rikaiDialog"
            open={openRikaiDialog}
            handleOpen={() => {
              setOpenRikaiDialog(true)
              disableBodyScroll(document.querySelector('#rikaiDialog'))
            }}
            handleClose={() => {
              setOpenRikaiDialog(false)
              enableBodyScroll(document.querySelector('#rikaiDialog'))
            }}
            rikaiString={rikaiString}
            setRikaiString={setRikaiString}
            definitions={definitions}
            setDefinitions={setDefinitions}
            matchLen={matchLen}
            setMatchLen={setMatchLen} />
      </div>
    </SocketContext.Provider>
  );
}

export default App;