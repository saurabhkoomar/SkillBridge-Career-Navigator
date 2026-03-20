import React from 'react';

function GapAnalysis({ result }) {
  if (!result) return null;

  const { matching_skills = [], missing_skills = [], ai_insights, priority_skills = [] } = result;

  return (
    <div className="gap-analysis">
      <div className="skills-comparison-row">
        <div className="card skills-card matching">
          <h4>✅ Matching Skills</h4>
          <div className="skills-tags">
            {matching_skills.length > 0 ? (
              matching_skills.map((s) => (
                <span key={s} className="tag tag-matching">
                  {s}
                </span>
              ))
            ) : (
              <p className="no-skills">No matching skills yet</p>
            )}
          </div>
        </div>
        <div className="card skills-card missing">
          <h4>❌ Missing Skills</h4>
          <div className="skills-tags">
            {missing_skills.length > 0 ? (
              missing_skills.map((s) => (
                <span key={s} className="tag tag-missing">
                  {s}
                </span>
              ))
            ) : (
              <p className="no-skills">You have all required skills!</p>
            )}
          </div>
        </div>
      </div>

      {ai_insights && (
        <div className="card insights-card">
          <h4>💡 Insights</h4>
          <p className="insights-text">{ai_insights}</p>
        </div>
      )}

      {priority_skills.length > 0 && (
        <div className="card priority-card">
          <h4>🎯 Priority Skills to Learn</h4>
          <ol className="priority-list">
            {priority_skills.map((skill, i) => (
              <li key={skill}>
                <span className="priority-badge">{i + 1}</span>
                {skill}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default GapAnalysis;
