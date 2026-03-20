import React from 'react';
import { truncateText } from '../utils/helpers';

function RoleSelector({ roles = [], value, onChange, placeholder = 'Select target role...' }) {
  const selectedRole = roles.find((r) => r.id === value);

  return (
    <div className="role-selector">
      <label className="label">Target Role</label>
      <select
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        className="select role-select"
      >
        <option value="">{placeholder}</option>
        {roles.map((r) => (
          <option key={r.id} value={r.id}>
            {r.title} ({r.required_skills?.length || 0} required skills)
          </option>
        ))}
      </select>
      {selectedRole && (
        <div className="role-preview-card">
          <h4>{selectedRole.title}</h4>
          <p className="role-desc">{truncateText(selectedRole.description, 120)}</p>
          <div className="role-skills">
            <span className="skill-label">Required:</span>
            {selectedRole.required_skills?.slice(0, 5).map((s) => (
              <span key={s} className="tag tag-required">{s}</span>
            ))}
            {selectedRole.required_skills?.length > 5 && (
              <span className="tag tag-more">+{selectedRole.required_skills.length - 5}</span>
            )}
          </div>
          {selectedRole.preferred_skills?.length > 0 && (
            <div className="role-skills preferred">
              <span className="skill-label">Preferred:</span>
              {selectedRole.preferred_skills?.slice(0, 3).map((s) => (
                <span key={s} className="tag tag-preferred">{s}</span>
              ))}
            </div>
          )}
          <div className="role-meta">
            <span>{selectedRole.salary_range}</span>
            <span>{selectedRole.experience_level}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default RoleSelector;
