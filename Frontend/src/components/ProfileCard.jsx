import React from 'react';
import { useNavigate } from 'react-router-dom';
import { formatDate } from '../utils/helpers';

function ProfileCard({ profile, targetRole, onEdit, onDelete }) {
  const navigate = useNavigate();

  const handleAnalyze = () => {
    navigate('/analyze', {
      state: {
        profileId: profile.id,
        skills: profile.skills,
        resumeText: profile.resume_text,
        targetRoleId: profile.target_role_id || targetRole?.id,
      },
    });
  };

  return (
    <div className="card profile-card">
      <div className="profile-card-body">
        <h4>{profile.name}</h4>
        <p className="profile-meta">
          {profile.skills?.length || 0} skills
          {profile.target_role_id && ` • Target: ${targetRole?.title || 'Role'}`}
        </p>
        <p className="profile-date">Updated {formatDate(profile.updated_at)}</p>
      </div>
      <div className="profile-card-actions">
        <button type="button" className="btn btn-secondary btn-sm" onClick={() => onEdit?.(profile)}>
          Edit
        </button>
        <button type="button" className="btn btn-primary btn-sm" onClick={handleAnalyze}>
          Analyze
        </button>
        <button type="button" className="btn btn-danger btn-sm" onClick={() => onDelete?.(profile.id)}>
          Delete
        </button>
      </div>
    </div>
  );
}

export default ProfileCard;
