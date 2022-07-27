import React, { useEffect, useContext, useRef } from "react";
import {SocketContext} from './socket';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

export default function ScrollDialog(props) {
  const socket = useContext(SocketContext);
  const [title, setTitle] = React.useState('Loading...');
  const [start, setStart] = React.useState(null);
  const [highlighted, setHighlighted] = React.useState('rikai-highlight2');
  const scrollBox = useRef(null);

  React.useEffect(() => {
    if (!props.open) {
      setTitle("Loading...");
      setStart(null);
      setHighlighted("no-rikai-highlight");
      props.setDefinitions("Click or tap on any character to search for all possible matching words...");
      console.log(`cleared definitions: ${props.definitions}`)
    } else {
      console.log('OPEN!')
      console.log(props.definitions)
    }
  }, [props.open]);

  React.useEffect(() => {
    console.log(`highlight from ${start} to ${start + props.matchLen}`);
    setHighlighted("rikai-highlight2");
    let newTitle = []
    props.rikaiString.split('').forEach((char, index) => {
      // console.log(char, index);
      newTitle.push((
        <span
          className={index >= start && index < start + props.matchLen ? highlighted : 'riaki-char'}
          onClick={(e) => {
            scrollBox.current?.scrollTo(0, 0);
            console.log(index);
            setStart(index);
            let toSearch  = props.rikaiString.slice(index, index + 20)
            console.log(`rikai-ing ${toSearch}`);
            socket.emit('rikai', toSearch)
          }}
        >{char}</span>
      ))
    })
    setTitle(<div className="rikai-chars-scrollbox"><div className="rikai-chars">{newTitle}</div></div>);
  }, [props.definitions]);

  React.useEffect(() => {
    console.log(props.rikaiString);
    let newTitle = []
    props.rikaiString.split('').forEach((char, index) => {
      // console.log(char, index);
      newTitle.push((
        <span
          className="rikai-char"
          onClick={(e) => {
            props.setDefinitions("Loading...");
            console.log(index);
            setStart(index);
            let toSearch  = props.rikaiString.slice(index, index + 20)
            console.log(`rikai-ing ${toSearch}`);
            socket.emit('rikai', toSearch)
          }}
        >{char}</span>
      ))
    })
    setTitle(<div className="rikai-chars-scrollbox"><div className="rikai-chars">{newTitle}</div></div>);
  }, [props.rikaiString]);

  return (
    <div>
      <Dialog
        // fullScreen='true'
        open={props.open}
        onClose={props.handleClose}
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle id="scroll-dialog-title">{title}</DialogTitle>
        <DialogContent ref={scrollBox} className="dialogContent" dividers={true}>
          {props.definitions}
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
            {[props.definitions]
            .map(
              (definition, index) => `${definition}`,
            )
            .join('JFEIWJFOIWEJFIEO')}
            {props.definitions.map((definition, index) => (
              // <ListItem button key={text}>
              //   <ListItemIcon>{index % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
              //   <ListItemText primary={text} />
              // </ListItem>
              <p>
                {definition}
              </p>
            ))}
          </DialogContentText> */}
        </DialogContent>
        <DialogActions>
          <Button onClick={props.handleClose} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}