// src/components/ChatInput.jsx
import React, { useState } from "react";
import "../styles/Chat.css";

const ChatInput = () => {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState(""); // State to store API response

  // Replace this with your actual Lambda API URL
  const API_URL = "http://127.0.0.1:8000/query";

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSend = async () => {
    console.log("Sending message:", input);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }), // Sending the input as JSON
      });

      if (!res.ok) throw new Error("Failed to fetch from the API.");

      const data = await res.json();
      console.log("Response data:", data); // Log the response data
      setResponse(data["Answer: "] || "No response"); // Update state with API response
    } catch (error) {
      console.error("Error:", error);
      setResponse("Something went wrong. Please try again.");
    }

    setInput(""); // Clear input after sending
  };

  return (
    <div className="chat-input-container">
      <input
        type="text"
        value={input}
        onChange={handleInputChange}
        placeholder="Type your message here..."
        className="chat-input"
      />
      <button onClick={handleSend} className="chat-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="white"
        >
          <path d="M2 21l21-9L2 3v7l15 2-15 2v7z" />
        </svg>
      </button>
      <div className="response-container">
        <p>{response}</p> {/* Display the API response */}
      </div>
    </div>
  );
};

export default ChatInput;
