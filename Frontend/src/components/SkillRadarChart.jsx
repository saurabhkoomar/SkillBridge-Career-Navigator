import React from 'react';
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';

function SkillRadarChart({ requiredSkills = [], matchingSkills = [] }) {
  const skillsToShow = requiredSkills.slice(0, 10);
  const matchingSet = new Set(matchingSkills.map((s) => s.toLowerCase()));

  const data = skillsToShow.map((skill) => ({
    skill: skill.length > 12 ? skill.slice(0, 12) + '...' : skill,
    fullLabel: skill,
    Your: matchingSet.has(skill.toLowerCase()) ? 100 : 0,
    Required: 100,
  }));

  if (data.length === 0) return null;

  return (
    <div className="skill-radar-chart">
      <h4>Skill Comparison</h4>
      <ResponsiveContainer width="100%" height={320}>
        <RechartsRadarChart data={data} margin={{ top: 20, right: 30, left: 30, bottom: 20 }}>
          <PolarGrid stroke="var(--color-border)" />
          <PolarAngleAxis
            dataKey="skill"
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 11 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: 'var(--color-text-muted)' }}
          />
          <Radar
            name="Your Skills"
            dataKey="Your"
            stroke="var(--color-primary)"
            fill="var(--color-primary)"
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <Radar
            name="Required"
            dataKey="Required"
            stroke="var(--color-warning)"
            fill="var(--color-warning)"
            fillOpacity={0.2}
            strokeWidth={1}
            strokeDasharray="4 4"
          />
          <Legend />
          <Tooltip
            content={({ payload }) => {
              if (payload?.[0]) {
                const item = payload[0].payload;
                return (
                  <div className="radar-tooltip">
                    <strong>{item.fullLabel}</strong>
                    <br />
                    Your match: {item.Your === 100 ? '✓ Yes' : '✗ No'}
                  </div>
                );
              }
              return null;
            }}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SkillRadarChart;
