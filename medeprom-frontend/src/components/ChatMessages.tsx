import { Message } from "../types";
import { Card } from "antd";
import "../index.css";
interface ChatMessageProps {
  message: Message[];
}

function ChatMessages({ message }: ChatMessageProps) {
  return (
    <div className="chat-messages-container">
      {message.map((m) => (
        <div
          className={`message-card ${
            m.role === "bot" ? "message-card-bot" : "message-card-user"
          }`}
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
