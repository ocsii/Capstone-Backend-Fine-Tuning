import { createContext, useState } from "react";

export const Context = createContext();

const ContextProvider = (props) => {
  const API_URL = "http://127.0.0.1:8000/query";

  const [input, setInput] = useState("");
  const [recentPrompt, setRecentPrompt] = useState("");
  const [previousPrompts, setPreviousPrompts] = useState([]);
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(false);
  const [resultData, setResultData] = useState("");

  // Track microphone state
  const [isListening, setIsListening] = useState(false);

  const delayPara = (index, nextWord) => {
    setTimeout(() => {
      setResultData((prev) => prev + nextWord);
    }, 75 * index);
  };

  const newChat = () => {
    setLoading(false);
    setShowResult(false);
  };

  const fetchResponse = async (prompt) => {
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: prompt }),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch from the backend");
      }

      const response = await res.json();
      let responseString = response["answer"];
      return processResponse(responseString);
    } catch (error) {
      console.error(error);
      return "No response from backend | Error parsing response from backend";
    }
  };

  const onSent = async (prompt) => {
    setResultData(""); // Clear previous results

    // Set recent prompt immediately
    if (prompt) {
      setRecentPrompt(prompt);
    } else {
      setRecentPrompt(input);
      setPreviousPrompts((prev) => [...prev, input]); // Store the input
    }

    setLoading(true); // Start loading
    setShowResult(true); // Show result area

    let response;
    // Fetch response based on the prompt
    response = await fetchResponse(prompt || input);

    // After fetching, process the response
    if (response) {
      let newResponseArray = response.split(" ");
      newResponseArray.forEach((nextWord, i) => {
        delayPara(i, nextWord + " "); // Display with delay
      });
    }

    setLoading(false); // Stop loading after processing
    setInput(""); // Clear input after sending
  };

  // Process response / add bold to words
  const processResponse = (responseString) => {
    let responseArray = responseString.split("**");
    let newResponse = "";

    responseArray.forEach((item, i) => {
      if (i === 0 || i % 2 !== 1) {
        newResponse += item;
      } else {
        newResponse += "<b>" + item + "</b>";
      }
    });

    return newResponse;
  };

  // Initialise speech recognition
  const recognition = new (window.SpeechRecognition ||
    window.webkitSpeechRecognition)();

  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  const startListening = () => {
    if (!isListening) {
      setIsListening(true);
      recognition.start();
    }
  };

  const stopListening = () => {
    if (isListening) {
      setIsListening(false);
      recognition.stop();
    }
  };

  // Handle speech recognition results
  recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript.trim();
    const capitalizedText =
      speechToText.charAt(0).toUpperCase() + speechToText.slice(1);
    setInput(capitalizedText);
    setIsListening(false);
    stopListening();
  };

  // Handle speech errors
  recognition.onerror = (event) => {
    console.error("Speech Regonition Error: ", event.error);
    stopListening();
  };

  // Make sure it stops when I click button
  recognition.onend = () => {
    if (isListening) {
      recognition.start();
    }
  };

  // To allow "Enter" on text box
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && input.trim() !== "") {
      onSent();
    }
  };

  // Input card fields into input from cards
  const handleCardClick = (question) => {
    setInput(question);
  };

  const contextValue = {
    previousPrompts,
    setPreviousPrompts,
    onSent,
    setRecentPrompt,
    recentPrompt,
    showResult,
    loading,
    resultData,
    input,
    setInput,
    newChat,
    startListening,
    stopListening,
    isListening,
    handleKeyDown,
    handleCardClick,
  };

  return (
    <Context.Provider value={contextValue}>{props.children}</Context.Provider>
  );
};

export default ContextProvider;
