import React from 'react';
import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="navbar-brand">
          <span className="navbar-icon">🧭</span>
          <span>Skill-Bridge</span>
        </NavLink>
        <div className="navbar-links">
          <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')} end>
            Home
          </NavLink>
          <NavLink to="/profile" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Profile
          </NavLink>
          <NavLink to="/analyze" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Analysis
          </NavLink>
          <NavLink to="/roles" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Roles
          </NavLink>
          <NavLink to="/roadmap" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Roadmap
          </NavLink>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
