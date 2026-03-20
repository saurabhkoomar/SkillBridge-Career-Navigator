import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="page home-page">
      <section className="hero">
        <h1>Bridge the Gap Between Your Skills and Your Dream Role</h1>
        <p className="hero-subtitle">
          AI-powered career navigation that analyzes your profile against real job
          requirements and creates a personalized learning roadmap
        </p>
        <div className="hero-cta">
          <Link to="/profile" className="btn btn-primary btn-lg">
            Create Your Profile
          </Link>
          <Link to="/roles" className="btn btn-outline btn-lg">
            Browse Job Roles
          </Link>
        </div>
      </section>

      <section className="section how-it-works">
        <h2>How It Works</h2>
        <div className="step-cards">
          <div className="card step-card">
            <span className="step-icon">📝</span>
            <h3>Input Your Skills</h3>
            <p>
              Add your skills manually or paste your resume. Our AI extracts relevant
              technical skills automatically.
            </p>
          </div>
          <div className="card step-card">
            <span className="step-icon">🎯</span>
            <h3>Choose Target Role</h3>
            <p>
              Browse 12+ job roles and select the position you're aiming for. See
              required and preferred skills.
            </p>
          </div>
          <div className="card step-card">
            <span className="step-icon">🗺️</span>
            <h3>Get Your Roadmap</h3>
            <p>
              Receive a personalized gap analysis with match score, priority skills, and
              a step-by-step learning path.
            </p>
          </div>
        </div>
      </section>

      <section className="section features">
        <h2>Features</h2>
        <div className="feature-grid">
          <div className="card feature-card">
            <h4>AI-Powered Analysis</h4>
            <p>Intelligent skill matching with personalized insights using Llama 3</p>
          </div>
          <div className="card feature-card">
            <h4>Smart Fallback</h4>
            <p>Rule-based analysis works even when AI is unavailable</p>
          </div>
          <div className="card feature-card">
            <h4>Learning Roadmap</h4>
            <p>Ordered learning path with time estimates and prerequisites</p>
          </div>
          <div className="card feature-card">
            <h4>Course Recommendations</h4>
            <p>Curated courses from top platforms to fill your skill gaps</p>
          </div>
        </div>
      </section>

      <section className="section stats">
        <div className="stat-grid">
          <div className="stat-item">
            <span className="stat-value">12</span>
            <span className="stat-label">Job Roles</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">25+</span>
            <span className="stat-label">Courses</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">AI + Fallback</span>
            <span className="stat-label">Always Works</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">100%</span>
            <span className="stat-label">Free</span>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
