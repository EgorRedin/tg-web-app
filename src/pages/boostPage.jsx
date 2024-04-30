import "../styles/boostPage.css"
import rocket from "../imgs/rocket.png"
import robot from "../imgs/robot.png"
import back from "../imgs/back_arrow.png";
import { useNavigate } from "react-router-dom";

function BoostPage()
{
    const navigate = useNavigate()
    return(
        <div className="boost-container">
            <div className="back-container" onClick={() => navigate("/")}>
                <img alt="back arrow" src={back}/>
            </div>
            <div className="header-container">
                <h1>Boost</h1>
                <img className="img-header" src={rocket} alt="rocket"/>
            </div>
            <div className="improve-container">
                <div className="button-item">
                    <img src={rocket} style={{width: "65px", height: "65px"}}/>
                </div>
                <p className="improvment">
                    Купить "+5" монет к каждому нажатию
                </p>
            </div>
            <div className="improve-container">
                <div className="button-item">
                    <img src={robot} style={{width: "65px", height: "65px"}}/>
                </div>
                <p className="improvment">
                    Купить автоматический майнинг
                </p>
            </div>
        </div>
    )
}

export default BoostPage