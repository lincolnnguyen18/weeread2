import React, {useContext} from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import {SocketContext} from './socket';

async function translate(source) {
  const sourceLanguage = "en";
  const targetLanguage = "ja";

  const url =
    "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q=" +
    encodeURI(source);

  const result = await fetch(url);
  const json = await result.json();

  try {
    // console.log(`json: ${json}`);
    return json[0][0][0];
  } catch (error) {
    return error.message;
  }
}

export default function TextArea(props) {
  const [value, setValue] = React.useState(props.value);
  const socket = useContext(SocketContext);

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <form noValidate autoComplete="off" id="form">
      <div id="formSub">
        <TextField
          id="outlined-multiline-static"
          label="Enter Japanese text here"
          multiline
          rows={10}
          defaultValue={value}
          variant="outlined"
          onChange={handleChange}
        />
        <Button variant="contained" color="primary" component="span" id="analyzeButton" onClick={() => {
          console.log('emitting');
          props.setReader([[[["Loading..."]]], [[[""]]]]);
          // setTimeout(() => {
          //   socket.emit('tokenize', value);
          // }, 3000);
          // console.log(`the value is ${value}`)

          // iterate line by line through value
          // const lines = value.split('\n');
          // lines.forEach(async (line) => {
          //   console.log(`line: ${line}`);
          //   const translated = await translate(line);
          //   console.log(`translated: ${translated}`);
          // });

          // translate(value).then(result => {
          //   console.log(`translation: ${result}`);
          // });
          socket.emit('tokenize', value);
        }}>
          Analyze
        </Button>
      </div>
    </form>
  );
}
