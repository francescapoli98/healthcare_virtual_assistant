import MessageBubble from "./MessageBubble";

export default function MessageList({ messages }) {
  return (
    <div className="chat-box">
      {messages.map((m, i) => (
        <MessageBubble key={i} message={m} />
      ))}
    </div>
  );
}