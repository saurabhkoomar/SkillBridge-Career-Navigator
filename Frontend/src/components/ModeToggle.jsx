import React from 'react';

function ModeToggle({ useAI, onChange }) {
  return (
    <div className="mode-toggle">
      <div className="mode-toggle-switch">
        <button
          type="button"
          className={`mode-btn ${useAI ? 'active ai' : ''}`}
          onClick={() => onChange(true)}
        >
          🤖 AI Mode
        </button>
        <button
          type="button"
          className={`mode-btn ${!useAI ? 'active manual' : ''}`}
          onClick={() => onChange(false)}
        >
          ⚙️ Manual Mode
        </button>
      </div>
      <p className="mode-description">
        {useAI
          ? 'Powered by Llama 3 via Groq — intelligent analysis with personalized insights'
          : 'Rule-based keyword matching — works offline, no API needed'}
      </p>
    </div>
  );
}

export default ModeToggle;
