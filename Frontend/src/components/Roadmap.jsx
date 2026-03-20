import React from 'react';
import { getDifficultyColor } from '../utils/helpers';

function Roadmap({ roadmap = [], courses = [], completedUpTo = 0 }) {
  if (roadmap.length === 0) {
    return (
      <div className="roadmap-empty">
        <p>Run an analysis first to generate your learning roadmap.</p>
        <a href="/analyze" className="btn btn-primary">
          Go to Analysis
        </a>
      </div>
    );
  }

  const getCourseForSkill = (skill) => {
    const skillLower = skill.toLowerCase();
    return courses.find(
      (c) =>
        c.skill_covered?.toLowerCase() === skillLower ||
        c.related_skills?.some((s) => s.toLowerCase() === skillLower)
    );
  };

  return (
    <div className="roadmap">
      <div className="roadmap-timeline">
        {roadmap.map((step, idx) => {
          const isCompleted = step.order <= completedUpTo;
          const isCurrent = step.order === completedUpTo + 1;
          const course = getCourseForSkill(step.skill);

          return (
            <div
              key={step.order}
              className={`roadmap-step ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''}`}
            >
              <div className="roadmap-node">
                <span className="node-number">{step.order}</span>
              </div>
              <div className="roadmap-content">
                <div className="roadmap-card">
                  <h4>{step.skill}</h4>
                  <p className="step-reason">{step.reason}</p>
                  <div className="step-badges">
                    <span className="badge weeks">{step.estimated_weeks} weeks</span>
                    <span
                      className="badge difficulty"
                      style={{ backgroundColor: getDifficultyColor(step.difficulty) }}
                    >
                      {step.difficulty}
                    </span>
                  </div>
                  {course && (
                    <div className="step-course">
                      <p className="course-title">{course.title}</p>
                      <a
                        href={course.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="course-link"
                      >
                        View Course →
                      </a>
                    </div>
                  )}
                </div>
              </div>
              {idx < roadmap.length - 1 && <div className="roadmap-connector" />}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Roadmap;
