/**
 * Utility functions for Skill-Bridge Career Navigator.
 */

export const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

export const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + '...';
};

export const getMatchColor = (percentage) => {
  if (percentage >= 75) return 'var(--color-success)';
  if (percentage >= 50) return 'var(--color-warning)';
  if (percentage >= 25) return 'var(--color-orange, #f97316)';
  return 'var(--color-error)';
};

export const getMatchLabel = (percentage) => {
  if (percentage >= 75) return 'Strong Match ✨';
  if (percentage >= 50) return 'Moderate Match 💪';
  if (percentage >= 25) return 'Building Up 🔨';
  return 'Just Starting 🚀';
};

export const getDifficultyColor = (difficulty) => {
  if (!difficulty) return 'var(--color-muted)';
  const d = difficulty.toLowerCase();
  if (d === 'beginner') return 'var(--color-success)';
  if (d === 'intermediate') return 'var(--color-warning)';
  if (d === 'advanced') return 'var(--color-error)';
  return 'var(--color-muted)';
};

export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};
