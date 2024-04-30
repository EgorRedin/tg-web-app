import { useState } from "react"
import dollar from "../imgs/dollar.png"
import "../styles/tradePage.css"


function TradePage()
{
    const [duocoins, setDoucoins] = useState("");
    const [coins, setCoins] = useState("")
    const changeText = (e) =>
    {
        setCoins(e.target.value);
        setDoucoins(parseFloat(e.target.value) / 1000.0);
    }


    return(
        <div className="trade-container">
            <div className="trade-header">
                <h1 className="">Trade</h1>
                <img src={dollar} alt="dollar" style={{width: "75px", height: "75px", transform: "translateY(10%)"}}/>
            </div>
            <div className="trade-window">
                <input className="input-in" value={coins} type="number" placeholder="Кол-во монет" autoComplete="off" onChange={(e) => changeText(e)}/>
                <p style={{fontSize: "40px", color: "white"}}>=</p>
                <input className="input-out" value={duocoins} type="number" placeholder="Кол-во Duocoin" readOnly="true" autoComplete="off"/>
            </div>
            <p style={{fontSize: "20px", color: "white"}}>(1000 монет = 1 DUO)</p>
            <button className="trade-button">Trade</button>
        </div>
    )
}

export default TradePage