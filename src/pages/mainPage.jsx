import React, { useState, useEffect } from "react";
import "../styles/mainPage.css"
import star from "../imgs/star.png"
import map from "../imgs/world-map.png"
import rocket from "../imgs/rocket.png"
import dollar from "../imgs/dollar.png"
import { useNavigate } from "react-router-dom";


function MainPage()
{
    const [balance, setBalance] = useState(10)
    const navigate = useNavigate()

    const navigateToTg = () =>
    {
               
    }
    
    return(
    <div className="main-container">
        <div className="hexagon">
            <p className="balance">{balance}</p>
            <img className="image-balance" style={{width: "55px", height: "55px"}} src={star} alt="star"/>
        </div>
        <div className="img-container">
            <img src={star} alt="star" className="clicker" onClick={() => setBalance((prevBalance) => (prevBalance + 1))}/>
        </div>
        <div className="buttons-container">
            <button className="button-item" onClick={() => navigateToTg()}>
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