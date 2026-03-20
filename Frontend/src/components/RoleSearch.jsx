import React, { useState, useCallback, useEffect } from 'react';
import { debounce } from '../utils/helpers';

function RoleSearch({ keyword, onKeywordChange, industry, onIndustryChange, experienceLevel, onExperienceLevelChange, skill, onSkillChange, resultCount, totalCount, onClear }) {
  const [localKeyword, setLocalKeyword] = useState(keyword || '');
  useEffect(() => setLocalKeyword(keyword || ''), [keyword]);
  const debouncedKeyword = useCallback(
    debounce((v) => onKeywordChange?.(v), 300),
    [onKeywordChange]
  );

  const handleKeywordChange = (e) => {
    const v = e.target.value;
    setLocalKeyword(v);
    debouncedKeyword(v);
  };

  return (
    <div className="role-search">
      <input
        type="text"
        placeholder="Search roles by keyword..."
        value={localKeyword}
        onChange={handleKeywordChange}
        className="input search-input"
      />
      <select
        value={industry || ''}
        onChange={(e) => onIndustryChange?.(e.target.value)}
        className="select filter-select"
      >
        <option value="">All Industries</option>
        <option value="Technology">Technology</option>
        <option value="Finance">Finance</option>
        <option value="Healthcare">Healthcare</option>
      </select>
      <select
        value={experienceLevel || ''}
        onChange={(e) => onExperienceLevelChange?.(e.target.value)}
        className="select filter-select"
      >
        <option value="">All Levels</option>
        <option value="Entry-Level">Entry-Level</option>
        <option value="Mid-Level">Mid-Level</option>
        <option value="Senior">Senior</option>
      </select>
      <input
        type="text"
        placeholder="Filter by skill..."
        value={skill || ''}
        onChange={(e) => onSkillChange?.(e.target.value)}
        className="input skill-filter-input"
      />
      <button type="button" className="btn btn-secondary" onClick={onClear}>
        Clear Filters
      </button>
      <p className="result-count">Showing {resultCount} of {totalCount} roles</p>
    </div>
  );
}

export default RoleSearch;
