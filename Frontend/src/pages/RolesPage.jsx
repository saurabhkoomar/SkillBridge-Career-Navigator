import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getRoles } from '../services/api';
import RoleSearch from '../components/RoleSearch';

function RolesPage() {
  const navigate = useNavigate();
  const [roles, setRoles] = useState([]);
  const [filteredRoles, setFilteredRoles] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [industry, setIndustry] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [skill, setSkill] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    getRoles().then((r) => {
      setRoles(r.data || []);
      setFilteredRoles(r.data || []);
    });
  }, []);

  useEffect(() => {
    const params = {
      keyword: keyword || undefined,
      industry: industry || undefined,
      experience_level: experienceLevel || undefined,
      skill: skill || undefined,
    };
    getRoles(params).then((r) => setFilteredRoles(r.data || []));
  }, [keyword, industry, experienceLevel, skill]);

  const handleClearFilters = () => {
    setKeyword('');
    setIndustry('');
    setExperienceLevel('');
    setSkill('');
  };

  const handleAnalyze = (role) => {
    navigate('/analyze', { state: { targetRoleId: role.id } });
  };

  return (
    <div className="page roles-page">
      <h1>Browse Job Roles</h1>

      <RoleSearch
        keyword={keyword}
        onKeywordChange={setKeyword}
        industry={industry}
        onIndustryChange={setIndustry}
        experienceLevel={experienceLevel}
        onExperienceLevelChange={setExperienceLevel}
        skill={skill}
        onSkillChange={setSkill}
        resultCount={filteredRoles.length}
        totalCount={roles.length}
        onClear={handleClearFilters}
      />

      <div className="roles-grid">
        {filteredRoles.map((role) => (
          <div key={role.id} className="card role-card">
            <h3>{role.title}</h3>
            <span className="badge company-type">{role.company_type}</span>
            <span className="badge experience-level">{role.experience_level}</span>
            <p className="role-salary">{role.salary_range}</p>
            <span className="badge industry">{role.industry}</span>
            <div className="role-skills-tags">
              {role.required_skills?.slice(0, 5).map((s) => (
                <span key={s} className="tag tag-small">{s}</span>
              ))}
              {role.required_skills?.length > 5 && (
                <span className="tag tag-more">+{role.required_skills.length - 5}</span>
              )}
            </div>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => setExpandedId(expandedId === role.id ? null : role.id)}
            >
              {expandedId === role.id ? 'Hide Details' : 'View Details'}
            </button>
            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={() => handleAnalyze(role)}
            >
              Analyze Against This Role
            </button>

            {expandedId === role.id && (
              <div className="role-expanded">
                <p>{role.description}</p>
                <div className="expanded-skills">
                  <strong>Required:</strong>
                  {role.required_skills?.map((s) => (
                    <span key={s} className="tag">{s}</span>
                  ))}
                </div>
                {role.preferred_skills?.length > 0 && (
                  <div className="expanded-skills">
                    <strong>Preferred:</strong>
                    {role.preferred_skills.map((s) => (
                      <span key={s} className="tag tag-preferred">{s}</span>
                    ))}
                  </div>
                )}
                <p className="typical-tools">
                  <strong>Tools:</strong> {role.typical_tools?.join(', ')}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default RolesPage;
