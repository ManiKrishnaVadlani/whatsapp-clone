import { useEffect, useState } from "react";

function App() {
  const [conversations, setConversations] = useState([]);
  const [activeConv, setActiveConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  // Fetch conversation list
  useEffect(() => {
    fetch(import.meta.env.VITE_BACKEND_URL + "/conversations")
      .then((res) => res.json())
      .then((data) => setConversations(data))
      .catch((err) => console.error(err));
  }, []);

  // Open a conversation
  const openConversation = (id) => {
    setActiveConv(id);
    fetch(`${import.meta.env.VITE_BACKEND_URL}/conversations/${id}`)
      .then((res) => res.json())
      .then((data) => setMessages(data))
      .catch((err) => console.error(err));
  };

  return (
    <div className="h-screen flex">
      {/* Left Sidebar */}
      <div className="w-1/3 border-r bg-gray-50 overflow-y-auto">
        <div className="p-4 font-bold text-lg border-b bg-green-600 text-white">
          WhatsApp Clone
        </div>
        {conversations.map((conv) => (
          <div
            key={conv._id}
            onClick={() => openConversation(conv._id)}
            className={`p-4 cursor-pointer hover:bg-gray-200 ${
              activeConv === conv._id ? "bg-gray-300" : ""
            }`}
          >
            <p className="font-semibold">{conv.name}</p>
            <p className="text-sm text-gray-600 truncate">
              {conv.last_message}
            </p>
          </div>
        ))}
      </div>

      {/* Right Chat Window */}
      <div className="flex-1 flex flex-col">
        <div className="p-4 border-b font-bold bg-gray-100">
          {activeConv
            ? conversations.find((c) => c._id === activeConv)?.name
            : "Select a conversation"}
        </div>

        <div className="flex-1 p-4 overflow-y-auto bg-gray-200">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`mb-2 flex ${
                msg.from_me ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`p-2 rounded-lg max-w-xs ${
                  msg.from_me ? "bg-green-500 text-white" : "bg-white"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        {activeConv && (
          <div className="p-4 border-t bg-white flex">
            <input
              type="text"
              placeholder="Type a message"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              className="flex-1 border rounded-lg p-2 mr-2"
            />
            <button
              onClick={() => {
                setMessages([...messages, { from_me: true, text: newMessage }]);
                setNewMessage("");
              }}
              className="bg-green-600 text-white px-4 py-2 rounded-lg"
            >
              Send
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
