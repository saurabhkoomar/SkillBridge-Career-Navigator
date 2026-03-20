import React, { useState, useEffect } from 'react';

function ResumeInput({ sampleResumes = [], onSelectSample, onPaste, currentValue }) {
  const [activeTab, setActiveTab] = useState('paste');
  const [selectedId, setSelectedId] = useState('');
  const [pasteText, setPasteText] = useState(currentValue || '');
  useEffect(() => setPasteText(currentValue || ''), [currentValue]);

  const handleUseSample = () => {
    if (selectedId) {
      const resume = sampleResumes.find((r) => r.id === selectedId);
      if (resume) {
        onSelectSample?.(resume);
      }
    }
  };

  const handlePasteChange = (e) => {
    const val = e.target.value;
    setPasteText(val);
    onPaste?.(val);
  };

  const selectedResume = sampleResumes.find((r) => r.id === selectedId);

  return (
    <div className="resume-input">
      <div className="resume-tabs">
        <button
          type="button"
          className={`tab-btn ${activeTab === 'sample' ? 'active' : ''}`}
          onClick={() => setActiveTab('sample')}
        >
          Sample Resume
        </button>
        <button
          type="button"
          className={`tab-btn ${activeTab === 'paste' ? 'active' : ''}`}
          onClick={() => setActiveTab('paste')}
        >
          Paste Resume
        </button>
      </div>

      {activeTab === 'sample' && (
        <div className="resume-sample-section">
          <select
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
            className="select resume-select"
          >
            <option value="">Select a sample resume...</option>
            {sampleResumes.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} - {r.skills?.length || 0} skills
              </option>
            ))}
          </select>
          {selectedResume && (
            <div className="resume-preview-card">
              <h4>{selectedResume.name}</h4>
              <p className="resume-summary">{selectedResume.summary}</p>
              <div className="resume-skills-preview">
                {selectedResume.skills?.slice(0, 6).map((s) => (
                  <span key={s} className="tag tag-small">
                    {s}
                  </span>
                ))}
                {selectedResume.skills?.length > 6 && (
                  <span className="tag tag-small">+{selectedResume.skills.length - 6}</span>
                )}
              </div>
              <button type="button" className="btn btn-primary" onClick={handleUseSample}>
                Use This Resume
              </button>
            </div>
          )}
        </div>
      )}

      {activeTab === 'paste' && (
        <div className="resume-paste-section">
          <textarea
            value={pasteText}
            onChange={handlePasteChange}
            placeholder="Paste your resume text here..."
            rows={10}
            className="textarea resume-textarea"
          />
          <p className="char-count">{pasteText.length} / 10,000 characters</p>
          {pasteText.length > 0 && pasteText.length < 50 && (
            <p className="input-warning">Resume should be at least 50 characters</p>
          )}
        </div>
      )}
    </div>
  );
}

export default ResumeInput;
