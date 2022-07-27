import React from "react";
import socketIOClient from "socket.io-client";

export const socket = socketIOClient();
export const SocketContext = React.createContext();