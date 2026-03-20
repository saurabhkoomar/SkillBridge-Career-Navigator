import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import Roadmap from '../components/Roadmap';

function RoadmapPage() {
  const location = useLocation();
  const analysis = location.state?.analysis;

  if (!analysis) {
    return (
      <div className="page roadmap-page">
        <h1>Your Learning Roadmap</h1>
        <div className="card roadmap-empty-state">
          <p>Run an analysis first to generate your learning roadmap.</p>
          <Link to="/analyze" className="btn btn-primary">
            Go to Analysis
          </Link>
        </div>
      </div>
    );
  }

  const roadmap = analysis.learning_roadmap || [];
  const totalWeeks = roadmap.reduce((acc, s) => acc + (s.estimated_weeks || 0), 0);

  return (
    <div className="page roadmap-page">
      <h1>Your Learning Roadmap</h1>

      <div className="roadmap-summary-bar">
        <span className="summary-item">
          <strong>Target:</strong> {analysis.target_role}
        </span>
        <span className="summary-item">
          <strong>Match:</strong> {Math.round(analysis.match_percentage)}%
        </span>
        <span className="summary-item">
          <strong>Skills to learn:</strong> {analysis.missing_skills?.length || 0}
        </span>
        <span className="summary-item">
          <strong>Est. weeks:</strong> {totalWeeks}
        </span>
      </div>

      <Roadmap
        roadmap={roadmap}
        courses={analysis.recommended_courses || []}
        completedUpTo={0}
      />
    </div>
  );
}

export default RoadmapPage;
