import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { analyzeSkills, getProfiles, getRoles } from '../services/api';
import SkillsEditor from '../components/SkillsEditor';
import RoleSelector from '../components/RoleSelector';
import ModeToggle from '../components/ModeToggle';
import MatchScore from '../components/MatchScore';
import SkillRadarChart from '../components/SkillRadarChart';
import GapAnalysis from '../components/GapAnalysis';
import CourseList from '../components/CourseList';

function AnalysisPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedProfileId, setSelectedProfileId] = useState('');
  const [skills, setSkills] = useState([]);
  const [resumeText, setResumeText] = useState('');
  const [targetRoleId, setTargetRoleId] = useState('');
  const [useAI, setUseAI] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getProfiles(), getRoles()]).then(([rP, rR]) => {
      setProfiles(rP.data || []);
      setRoles(rR.data || []);
    });
  }, []);

  useEffect(() => {
    const state = location.state;
    if (state) {
      if (state.skills?.length) setSkills(state.skills);
      if (state.resumeText) setResumeText(state.resumeText);
      if (state.targetRoleId) setTargetRoleId(state.targetRoleId);
      if (state.profileId) setSelectedProfileId(state.profileId);
    }
  }, [location.state]);

  useEffect(() => {
    if (selectedProfileId) {
      const p = profiles.find((pr) => pr.id === selectedProfileId);
      if (p) {
        setSkills(p.skills || []);
        setResumeText(p.resume_text || '');
        setTargetRoleId(p.target_role_id || '');
      }
    }
  }, [selectedProfileId, profiles]);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (skills.length === 0 || !targetRoleId) {
      setError('Please add at least one skill and select a target role.');
      return;
    }
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      const res = await analyzeSkills({
        user_skills: skills,
        resume_text: resumeText || undefined,
        target_role_id: targetRoleId,
        use_ai: useAI,
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleViewRoadmap = () => {
    navigate('/roadmap', { state: { analysis: result } });
  };

  const currentSkills = selectedProfileId
    ? (profiles.find((p) => p.id === selectedProfileId)?.skills || skills)
    : skills;

  return (
    <div className="page analysis-page">
      <h1>Skill Gap Analysis</h1>

      <div className="analysis-input-section card">
        <div className="input-row">
          <div className="input-col">
            <label className="label">Profile or Skills</label>
            <select
              value={selectedProfileId}
              onChange={(e) => {
                setSelectedProfileId(e.target.value);
                if (!e.target.value) setSkills([]);
              }}
              className="select"
            >
              <option value="">Enter skills manually</option>
              {profiles.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.skills?.length || 0} skills)
                </option>
              ))}
            </select>
            {!selectedProfileId && (
              <SkillsEditor skills={skills} onChange={setSkills} />
            )}
          </div>
          <div className="input-col">
            <RoleSelector
              roles={roles}
              value={targetRoleId}
              onChange={setTargetRoleId}
            />
          </div>
        </div>
        <ModeToggle useAI={useAI} onChange={setUseAI} />
        <button
          type="button"
          className="btn btn-primary btn-lg analyze-btn"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? 'Analyzing your skills...' : '🔍 Analyze Skills'}
        </button>
        {loading && <div className="spinner" />}
      </div>

      {error && (
        <div className="card error-card">
          <p className="error-text">{error}</p>
        </div>
      )}

      {result && (
        <div className="analysis-results">
          <div className="analysis-mode-badge" data-mode={result.analysis_mode}>
            {result.analysis_mode === 'ai' ? '🤖 AI Analysis' : '⚙️ Fallback Analysis'}
          </div>

          <div className="results-row match-row">
            <MatchScore percentage={result.match_percentage} />
            <div className="radar-col">
              <SkillRadarChart
                requiredSkills={result.required_skills}
                matchingSkills={result.matching_skills}
              />
            </div>
          </div>

          <GapAnalysis result={result} />

          <div className="course-section">
            <CourseList courses={result.recommended_courses || []} />
          </div>

          <div className="cta-row">
            <button className="btn btn-primary btn-lg" onClick={handleViewRoadmap}>
              View Full Learning Roadmap →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalysisPage;
