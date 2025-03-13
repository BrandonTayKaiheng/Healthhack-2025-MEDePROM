import "../index.css";
import SendArrow from "../assets/SendArrow.svg";
import { send } from "vite";
interface ChatInputProps {
  newMessageText: string;
  setNewMessageText: (newMessage: string) => void;
  sendNewMessage: () => void;
}

function ChatInput({
  newMessageText,
  setNewMessageText,
  sendNewMessage,
}: ChatInputProps) {
  return (
    <div className="chat-input-container">
      <input
        className="chat-input"
        type="text"
        value={newMessageText}
        onChange={(e) => setNewMessageText(e.target.value)}
        placeholder="Type a message..."
      />
      <img
        className="send-arrow-button"
        src={SendArrow}
        alt="send"
        onClick={sendNewMessage}
      />
    </div>
  );
}

export default ChatInput;
