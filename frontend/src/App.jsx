// src/App.jsx
import React from "react";
import ChatTitle from "./components/ChatTitle";
import ChatInput from "./components/ChatInput";
import "./styles/Chat.css";

const App = () => {
  return (
    <div className="app-container">
      <ChatTitle />
      <ChatInput />
    </div>
  );
};

export default App;
