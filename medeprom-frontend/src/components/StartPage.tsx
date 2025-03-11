import { Button } from "antd";
import { useNavigate } from "react-router";

function StartPage() {
  const navigate = useNavigate();
  return (
    <div className="start-page-container">
      <Button onClick={() => navigate("/chat")}>Start Chat</Button>
    </div>
  );
}
export default StartPage;
