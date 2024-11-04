import React, { useContext } from "react";
import "./Main.css";
import { assets } from "../../assets/assets";
import { Context } from "../../context/Context";

const Main = () => {
  const {
    onSent,
    recentPrompt,
    showResult,
    loading,
    resultData,
    setInput,
    input,
    newChat,
  } = useContext(Context);

  // Array of question objects with associated icons
  const questions = [
    { text: "What is Mr Muthukumarans email?", icon: assets.icon_email_orange },
    {
      text: "What is the prerequisites for Object Oriented Programming?",
      icon: assets.icon_prerequisite,
    },
    {
      text: "What is the criteria to achieve first class honors?",
      icon: assets.icon_question_mark,
    },
    {
      text: "What is the credit hours for Data Structures and Algorithms?",
      icon: assets.icon_clock,
    },
  ];

  const handleCardClick = (question) => {
    setInput(question);
  };

  return (
    <div className="main">
      <div className="nav">
        <p onClick={() => newChat()} className="titleHeader">
          {" "}
          SunwayGPT{" "}
        </p>

        <img className="sunwayLogo" src={assets.icon_sunway_logo} alt="" />
      </div>

      <div className="main-container">
        {!showResult ? (
          <>
            <div className="div greet">
              <p>
                <span>Hello, User.</span>
              </p>
              <p>Ask me a question!</p>
            </div>
            <div className="cards">
              {questions.map((question, index) => (
                <div
                  key={index}
                  className="card"
                  onClick={() => handleCardClick(question.text)}
                >
                  <p>{question.text}</p>
                  <img src={question.icon} alt="" />
                </div>
              ))}
            </div>
          </>
        ) : (
          <>
            <div className="result">
              <div className="result-title">
                <img src={assets.icon_question_mark} alt="" />
                <p>
                  {recentPrompt.charAt(0).toUpperCase() + recentPrompt.slice(1)}
                </p>
              </div>
              <div className="result-data">
                {loading ? (
                  <div className="loader">
                    <hr />
                    <hr />
                    <hr />
                  </div>
                ) : (
                  <p dangerouslySetInnerHTML={{ __html: resultData }} />
                )}
              </div>
            </div>
          </>
        )}

        <div className="main-bottom">
          <div className="search-box">
            <input
              onChange={(e) => setInput(e.target.value)}
              value={input}
              type="text"
              placeholder="Enter your question..."
            />
            <div>
              {input ? (
                <img
                  class="sendButton"
                  onClick={() => onSent()}
                  src={assets.icon_running_black}
                  alt=""
                />
              ) : null}
            </div>
          </div>

          <p className="bottom-info">
            This is a personal project not an official product of Sunway. Please
            double check any critical information.
          </p>
          <p className="bottom-info">
            Backend is on a free-tier which causes very slow loading times. For
            faster responses run it{" "}
            <a
              href="https://github.com/ocsii/Capstone-Backend-Fine-Tuning"
              target="_blank"
              rel="noopener noreferrer"
            >
              locally
            </a>
            .
          </p>
        </div>
      </div>
      <p className="bottom-info-name"> Christian Cham (2024) </p>
    </div>
  );
};

export default Main;
