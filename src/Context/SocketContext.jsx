import React, {createContext, useState, useEffect} from "react";
import io from "socket.io-client";
import { useTelegram } from "../hooks/useTelegram";

export const SocketContext = createContext();

export const SocketProvider = ({ children }) => 
{
    const [user, setUser] = useState(null);
    const socket = io.connect("https://duo-coin.ru/");
    const {userTg} = useTelegram() 

    useEffect(() =>
    {
        socket.on("connect", () =>
        {
            socket.emit("init_user", {userID: userTg.id});
        });
    }, [])


    const updateUser = (newUserData) => {
        setUser(newUserData);
    };


    return (
        <SocketContext.Provider value={{ user, socket, updateUser }}>
          {children}
        </SocketContext.Provider>
      );
};