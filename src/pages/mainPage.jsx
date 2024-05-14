import React, { useState, useEffect, useRef, useContext } from "react";
import "../styles/mainPage.css";
import star from "../imgs/star.png";
import map from "../imgs/world-map.png";
import rocket from "../imgs/rocket.png";
import dollar from "../imgs/dollar.png";
import { useNavigate } from "react-router-dom";
import {useTelegram} from "../hooks/useTelegram";
import { SocketContext } from "../context/SocketContext";


function MainPage()
{

    const {user, socket, updateUser} = useContext(SocketContext); 
    const navigate = useNavigate();
    const {userTg, onClose} = useTelegram();
    const [balance, setBalance] = useState(0);
    const [startBalance, setStart] = useState(0);
    const balanceRef = useRef(balance);
    const startRef = useRef(startBalance);
    const [clickSizeP, setClickSize] = useState(1);
    

    useEffect(() =>
    {
        socket.on("get_user", (data) =>
        {
            updateUser(data);
        })
    }, [])

    useEffect(() => {
        if (user) {
          setBalance(user.balance);
          setStart(user.balance);
          setClickSize(user.click_size)
        }
      }, [user]);
 
    useEffect(() =>
    {
        balanceRef.current = balance
    }, [balance])

    useEffect(() =>
    {
        startRef.current = startBalance;
    }, [startBalance])

    useEffect(() =>
    {
        const interval = setInterval(() => {
            socket.emit("click", {userID: userTg.id, clicks: (balanceRef.current - startRef.current)})
        }, 10000)

        return () =>
        clearInterval(interval);
    }, [])
    
    const SingleClick = () =>
    {
        setBalance((prevBalance) => (prevBalance + clickSizeP));
        socket.emit("single_click", {userID: userTg.id, clickSize: clickSizeP});
    }

    const handleBoost = () =>
    {
        console.log(balanceRef.current, startRef.current)
        socket.emit("click", {userID: userTg.id, clicks: (balanceRef.current - startRef.current)});
        navigate('/boost');
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
            <button className="button-item" onClick={() => handleBoost()}>
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