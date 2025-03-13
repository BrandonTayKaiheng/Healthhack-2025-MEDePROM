import { useState } from "react";
import { useImmer } from "use-immer";
import { Message } from "./types";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

import "../index.css";
import { message } from "antd";

function Chatbot() {
  const [chatId, setChatId] = useState(0);
  const [messages, setMessages] = useImmer<Message[]>([]);
  const [newMessageText, setNewMessageText] = useState("");
  const testMessages: Message[] = [
    { text: "message 1", role: "bot", chatId: 0 },
    { text: "message 2", role: "user", chatId: 0 },
    {
      text: "message 3 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
      role: "bot",
      chatId: 0,
    },
    {
      text: "message 4 Lorem ipsum dolor sit amet, consectetur adipiscing elit",
      role: "user",
      chatId: 0,
    },
    {
      text: "message 5",
      role: "bot",
      chatId: 0,
    },
    {
      text: "message 6",
      role: "user",
      chatId: 0,
    },
    {
      text: "message 7",
      role: "bot",
      chatId: 0,
    },
    {
      text: "message 8",
      role: "user",
      chatId: 0,
    },
    {
      text: "message 9",
      role: "bot",
      chatId: 0,
    },
  ];
  const sendNewMessage = () => {
    const trimmedNewMessage = newMessageText.trim();
    if (trimmedNewMessage === "") return;
    setMessages((draft) => [...draft, { role: "user", text: newMessageText }]);
    setNewMessageText("");
    // const response = await api.sendMessage(chatId, trimmedNewMessage);
    // setMessages((draft) => [...draft, { role: "bot", text: response, chatId = chatId }]);
  };

  return (
    <div className="chatbot-container">
      <div className="chat-header">MEDePROM</div>
      <ChatMessages messages={testMessages} />
      <ChatInput
        newMessageText={newMessageText}
        setNewMessageText={setNewMessageText}
        sendNewMessage={sendNewMessage}
      />
    </div>
  );
}

export default Chatbot;
