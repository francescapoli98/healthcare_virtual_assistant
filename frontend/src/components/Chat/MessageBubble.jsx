export default function MessageBubble({ message }) {
    return (
      <div className={`msg ${message.role}`}>
        {message.text}
      </div>
    );
  }