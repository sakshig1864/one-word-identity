import React, { useState, useEffect } from "react";
import axios from "axios";

function OneWordForm() {
  const [word, setWord] = useState("");
  const [explanation, setExplanation] = useState("");
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(120); // 2 minutes = 120 seconds
  const [isTimerActive, setIsTimerActive] = useState(false);

  // Timer countdown
  useEffect(() => {
    if (!isTimerActive || timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          handleAutoSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isTimerActive, timeLeft]);

  // Start timer when user starts typing
  const handleWordChange = (e) => {
    setWord(e.target.value);
    if (!isTimerActive && e.target.value.length > 0) {
      setIsTimerActive(true);
    }
  };

  const handleExplanationChange = (e) => {
    setExplanation(e.target.value);
    if (!isTimerActive && e.target.value.length > 0) {
      setIsTimerActive(true);
    }
  };

  const handleAutoSubmit = async () => {
    if (word.trim() && explanation.trim()) {
      await handleSubmit(null);
    }
    setIsTimerActive(false);
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", {
        word,
        explanation,
      });
      setResult(response.data);
      setIsTimerActive(false);
    } catch (error) {
      console.error("Error analyzing:", error);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="form-container">
      {isTimerActive && timeLeft > 0 && (
        <div className="timer">
          ⏱️ Time remaining: <strong>{formatTime(timeLeft)}</strong>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <label>Your One Word:</label>
        <input
          type="text"
          value={word}
          onChange={handleWordChange}
          placeholder='e.g. "Determined", "Curious"'
          required
        />

        <label>Explain why:</label>
        <textarea
          value={explanation}
          onChange={handleExplanationChange}
          placeholder="Write a short explanation..."
          required
        ></textarea>

        <button type="submit">Analyze</button>
      </form>

      {result && (
        <div className="result">
          <h3>📊 Analysis Result</h3>

          <div className="scores">
            <div className="score-item">
              <span className="score-label">Overall Score</span>
              <span className="score-value">{result.rating}/10</span>
            </div>
            <div className="score-item">
              <span className="score-label">Word Score</span>
              <span className="score-value">{result.word_sentiment}/10</span>
            </div>
            <div className="score-item">
              <span className="score-label">Explanation Score</span>
              <span className="score-value">
                {result.explanation_sentiment}/10
              </span>
            </div>
          </div>

          <div className="feedback">
            <strong>Feedback:</strong>
            <p>{result.feedback}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default OneWordForm;
