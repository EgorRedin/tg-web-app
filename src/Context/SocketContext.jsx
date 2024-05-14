import React, {createContext, useState, useEffect} from "react";
import io from "socket.io-client";

export const SocketContext = createContext();

export const SocketProvider = ({ children }) => 
{
    const [user, setUser] = useState(null);
    const socket = io("https://147.45.187.204/");

    useEffect(() =>
    {
        socket.on("connect", () =>
        {
            socket.emit("init_user", {userID: user.id});
        });
        
        socket.on("get_user", () =>
        {
            setUser(user);
        })
    })

    return (
        <SocketContext.Provider value={{ user, socket }}>
          {children}
        </SocketContext.Provider>
      );
};