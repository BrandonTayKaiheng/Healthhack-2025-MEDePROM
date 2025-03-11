import { Message } from "../types";
import { Card } from "antd";
import "../index.css";
interface ChatMessageProps {
  message: Message[];
}

function ChatMessages({ message }: ChatMessageProps) {
  console.log(message);
  return (
    <div className="styles-messages-box">
      {message.map((m) => (
        <div
          className={
            m.role === "bot" ? "message-card-bot" : "message-card-user"
          }
          key={m.text}
        >
          {m.text}
        </div>
      ))}
    </div>
  );
}

{
  /* <Card className="user-message-card"> {msg[0].role} helloooo </Card>; */
}
export default ChatMessages;
