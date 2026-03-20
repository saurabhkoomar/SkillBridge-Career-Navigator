import React, { useState } from 'react';
import { getDifficultyColor } from '../utils/helpers';

function CourseList({ courses = [] }) {
  const [sortBy, setSortBy] = useState('rating');

  const sorted = [...courses].sort((a, b) => {
    if (sortBy === 'rating') return (b.rating || 0) - (a.rating || 0);
    if (sortBy === 'duration') return (a.duration_hours || 0) - (b.duration_hours || 0);
    if (sortBy === 'cost') {
      const aFree = (a.cost || '').toLowerCase() === 'free' ? 0 : 1;
      const bFree = (b.cost || '').toLowerCase() === 'free' ? 0 : 1;
      return aFree - bFree;
    }
    return 0;
  });

  return (
    <div className="course-list">
      <div className="course-list-header">
        <h4>📚 Recommended Courses</h4>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="select sort-select"
        >
          <option value="rating">Sort by Rating</option>
          <option value="duration">Sort by Duration</option>
          <option value="cost">Sort by Cost (Free first)</option>
        </select>
      </div>
      <div className="course-grid">
        {sorted.map((course) => (
          <div key={course.id} className="card course-card">
            <h5>{course.title}</h5>
            <div className="course-badges">
              <span
                className="badge platform"
                style={{ backgroundColor: 'var(--color-border)' }}
              >
                {course.platform}
              </span>
              <span
                className="badge difficulty"
                style={{ backgroundColor: getDifficultyColor(course.difficulty) }}
              >
                {course.difficulty}
              </span>
              <span className="badge cost">
                {course.cost?.toLowerCase() === 'free' ? 'Free' : course.cost}
              </span>
            </div>
            <p className="course-meta">
              {course.duration_hours}h • ⭐ {course.rating}
            </p>
            {course.skill_covered && (
              <span className="tag tag-skill-cover">{course.skill_covered}</span>
            )}
            <p className="course-desc">{course.description}</p>
            <a
              href={course.url}
              target="_blank"
              rel="noopener noreferrer"
              className="course-link"
            >
              View Course →
            </a>
          </div>
        ))}
      </div>
      {courses.length === 0 && (
        <p className="no-courses">No recommended courses for your missing skills.</p>
      )}
    </div>
  );
}

export default CourseList;
