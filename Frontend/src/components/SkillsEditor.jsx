import React, { useState } from 'react';

function SkillsEditor({ skills = [], onChange, placeholder = 'Add a skill...' }) {
  const [input, setInput] = useState('');

  const addSkill = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    const exists = skills.some((s) => s.toLowerCase() === trimmed.toLowerCase());
    if (exists) return;
    onChange([...skills, trimmed]);
    setInput('');
  };

  const removeSkill = (index) => {
    onChange(skills.filter((_, i) => i !== index));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSkill();
    }
  };

  return (
    <div className="skills-editor">
      <div className="skills-input-row">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="input skills-input"
        />
        <button type="button" className="btn btn-secondary" onClick={addSkill}>
          Add Skill
        </button>
      </div>
      <div className="skills-tags">
        {skills.map((skill, i) => (
          <span key={`${skill}-${i}`} className="tag tag-skill">
            {skill}
            <button
              type="button"
              className="tag-remove"
              onClick={() => removeSkill(i)}
              aria-label={`Remove ${skill}`}
            >
              ×
            </button>
          </span>
        ))}
      </div>
      <p className="skills-count">{skills.length} skill{skills.length !== 1 ? 's' : ''} added</p>
    </div>
  );
}

export default SkillsEditor;
