import { Button } from "antd";
import { useNavigate } from "react-router";
import ChatIcon from "../assets/ChatIcon.svg";
import CallIcon from "../assets/CallIcon.svg";

function StartPage() {
  const navigate = useNavigate();
  return (
    <div className="start-page-container">
      <div className="start-page-card">
        <Button
          size="large"
          className="chat-button"
          onClick={() => navigate("/chat")}
        >
          Chat
          <img src={ChatIcon} alt="call" />
        </Button>
        <Button
          size="large"
          className="call-button"
          onClick={() => navigate("/chat")}
        >
          Call
          <img src={CallIcon} alt="call" />
        </Button>
      </div>
    </div>
  );
}
export default StartPage;
