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
    <div>
      <input
        type="text"
        value={newMessageText}
        onChange={(e) => setNewMessageText(e.target.value)}
      />
      <button onClick={sendNewMessage}>Send</button>
    </div>
  );
}

export default ChatInput;
