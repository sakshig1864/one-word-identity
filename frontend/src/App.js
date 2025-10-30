import React from "react";
import OneWordForm from "./components/OneWordForm";
import "./App.css";

function App() {
  return (
    <div className="app">
      <h2>🧠 One-Word Identity</h2>
      <p>Give one word that best describes you today and explain why.</p>
      <OneWordForm />
    </div>
  );
}

export default App;
