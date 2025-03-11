import { useState } from "react";
import { useImmer } from "use-immer";
import { Message } from "./types";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

function Chatbot() {
  const [messages, setMessages] = useImmer<Message[]>([]);
  const [newMessageText, setNewMessageText] = useState("");
  const testMessages: Message[] = [
    { text: "message 1", role: "bot" },
    { text: "message 2", role: "user" },
    { text: "message 3", role: "bot" },
    { text: "message 4", role: "user" },
  ];
  const sendNewMessage = () => {
    console.log(newMessageText);
  };

  return (
    <div>
      <ChatMessages message={testMessages} />
      <ChatInput
        newMessageText={newMessageText}
        setNewMessageText={setNewMessageText}
        sendNewMessage={sendNewMessage}
      />
    </div>
  );
}

export default Chatbot;
