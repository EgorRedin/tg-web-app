import React, { useState, useEffect, useRef } from "react";
import "../styles/mainPage.css";
import star from "../imgs/star.png";
import map from "../imgs/world-map.png";
import rocket from "../imgs/rocket.png";
import dollar from "../imgs/dollar.png";
import { useNavigate } from "react-router-dom";
import {useTelegram} from "../hooks/useTelegram"
import io from 'socket.io-client'

let socket = null;

function getSocket()
{
    if(socket === null)
    {
        socket = io.connect("http://localhost:8000/");
    }
    return socket;
}

function MainPage()
{
    const [balance, setBalance] = useState(0);
    const navigate = useNavigate();
    const [startBalance, setStart] = useState(0);
    const {user, onClose, tg} = useTelegram();
    const balanceRef = useRef(balance);
    const startRef = useRef(startBalance);
    const socket = getSocket()

    useEffect(() =>
    {
        balanceRef.current = balance;
    }, [balance])

    useEffect(() =>
    {
        startRef.current = startBalance;
    }, [startBalance])

    useEffect(() =>
    {
        socket.on("connect", () => {
            socket.emit("init_user", {userID: user.id})
          });
        
        socket.on("get_user", (data) => {
            setStart(data.balance);
            setBalance(data.balance);
            }
        )

        tg.ready()
    }, []);


    useEffect(() =>
    {
        const interval = setInterval(() => {
            socket.emit("click", {userID: user.id, clicks: (balanceRef.current - startRef.current)})
        }, 10000)

        return () =>
        clearInterval(interval);
    }, [])
    
    const SingleClick = () =>
    {
        setBalance((prevBalance) => (prevBalance + 1));
        socket.emit("single_click", user.id);
    }

    return(
    <div className="main-container">
        <div className="hexagon">
            <p className="balance">{balance}</p>
            <img className="image-balance" style={{width: "55px", height: "55px"}} src={star} alt="star"/>
        </div>
        <div className="img-container">
            <img src={star} alt="star" className="clicker" onClick={() => SingleClick()}/>
        </div>
        <div className="buttons-container">
            <button className="button-item" onClick={() => onClose()}>
                <img  className="img-button" src={map} alt="map"/>
                <p className="p-button">Tg</p>
            </button>
            <button className="button-item" onClick={() => navigate('/boost')}>
                <img className="img-button" src={rocket} alt="rocket"/>
                <p className="p-button">Boost</p>
            </button>
            <button className="button-item" onClick={() => navigate('/trade')}>
                <img className="img-button" src={dollar} alt="dollar"/>
                <p className="p-button">Trade</p>
            </button>
        </div>
    </div>
    )

}

export default MainPage