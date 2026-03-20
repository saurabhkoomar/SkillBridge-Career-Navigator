import React from 'react';
import { getMatchColor, getMatchLabel } from '../utils/helpers';

function MatchScore({ percentage }) {
  const color = getMatchColor(percentage);
  const label = getMatchLabel(percentage);
  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="match-score">
      <div className="match-score-circle-wrap">
        <svg viewBox="0 0 100 100" className="match-score-svg">
          <circle
            className="match-score-bg"
            cx="50"
            cy="50"
            r="45"
          />
          <circle
            className="match-score-fill"
            cx="50"
            cy="50"
            r="45"
            style={{
              stroke: color,
              strokeDasharray: circumference,
              strokeDashoffset: offset,
            }}
          />
        </svg>
        <div className="match-score-content">
          <span className="match-score-value">{Math.round(percentage)}%</span>
          <span className="match-score-label">Match Score</span>
          <span className="match-score-status" style={{ color }}>{label}</span>
        </div>
      </div>
    </div>
  );
}

export default MatchScore;
