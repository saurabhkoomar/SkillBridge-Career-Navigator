import React, { useState, useEffect, useCallback } from 'react';
import { createProfile, updateProfile, getProfiles, deleteProfile, getSampleResumes, getRoles } from '../services/api';
import SkillsEditor from '../components/SkillsEditor';
import ResumeInput from '../components/ResumeInput';
import RoleSelector from '../components/RoleSelector';
import ProfileCard from '../components/ProfileCard';

function ProfilePage() {
  const [profiles, setProfiles] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({
    name: '',
    skills: [],
    resume_text: '',
    target_role_id: '',
  });

  const loadData = useCallback(() => {
    Promise.all([getSampleResumes(), getRoles(), getProfiles()])
      .then(([resResumes, resRoles, resProfiles]) => {
        setResumes(resResumes.data || []);
        setRoles(resRoles.data || []);
        setProfiles(resProfiles.data || []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSelectSampleResume = (resume) => {
    setForm((f) => ({
      ...f,
      resume_text: resume.resume_text || '',
      skills: resume.skills || [],
      name: resume.name || f.name,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.name.trim() || form.skills.length === 0) return;

    const payload = {
      name: form.name.trim(),
      skills: form.skills,
      resume_text: form.resume_text || null,
      target_role_id: form.target_role_id || null,
    };

    if (editingId) {
      updateProfile(editingId, payload)
        .then(() => {
          setEditingId(null);
          setForm({ name: '', skills: [], resume_text: '', target_role_id: '' });
          loadData();
        })
        .catch(console.error);
    } else {
      createProfile(payload)
        .then(() => {
          setForm({ name: '', skills: [], resume_text: '', target_role_id: '' });
          loadData();
        })
        .catch(console.error);
    }
  };

  const handleEdit = (profile) => {
    setForm({
      name: profile.name,
      skills: profile.skills || [],
      resume_text: profile.resume_text || '',
      target_role_id: profile.target_role_id || '',
    });
    setEditingId(profile.id);
  };

  const handleDelete = (id) => {
    if (!window.confirm('Delete this profile?')) return;
    deleteProfile(id).then(() => loadData()).catch(console.error);
  };

  return (
    <div className="page profile-page">
      <h1>{editingId ? 'Edit Profile' : 'Create Your Profile'}</h1>

      <form onSubmit={handleSubmit} className="profile-form card">
        <div className="form-group">
          <label className="label">Name</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            placeholder="Enter your full name"
            className="input"
          />
        </div>

        <div className="form-group">
          <label className="label">Resume</label>
          <ResumeInput
            sampleResumes={resumes}
            onSelectSample={handleSelectSampleResume}
            onPaste={(text) => setForm((f) => ({ ...f, resume_text: text }))}
            currentValue={form.resume_text}
          />
        </div>

        <div className="form-group">
          <label className="label">Skills</label>
          <SkillsEditor
            skills={form.skills}
            onChange={(skills) => setForm((f) => ({ ...f, skills }))}
          />
        </div>

        <div className="form-group">
          <RoleSelector
            roles={roles}
            value={form.target_role_id}
            onChange={(id) => setForm((f) => ({ ...f, target_role_id: id }))}
          />
        </div>

        <button type="submit" className="btn btn-primary">
          {editingId ? 'Save Profile' : 'Create Profile'}
        </button>
      </form>

      <section className="saved-profiles">
        <h2>Your Saved Profiles</h2>
        <div className="profile-grid">
          {profiles.map((p) => (
            <ProfileCard
              key={p.id}
              profile={p}
              targetRole={roles.find((r) => r.id === p.target_role_id)}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </div>
      </section>
    </div>
  );
}

export default ProfilePage;
