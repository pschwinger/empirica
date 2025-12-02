/**
 * ConfidenceBadge Component
 *
 * Displays AI confidence as a color-coded badge
 * - Green (0.9+): High confidence
 * - Yellow (0.7-0.89): Moderate confidence
 * - Orange (0.5-0.69): Low confidence
 * - Red (<0.5): Not investigated
 */

import React from 'react';
import '../styles/badges.css';

interface ConfidenceBadgeProps {
  score: number; // 0-1
  label?: string;
  subtitle?: string;
  size?: 'small' | 'medium' | 'large';
}

export const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({
  score,
  label = 'Confidence',
  subtitle,
  size = 'medium'
}) => {
  const percentage = Math.round(score * 100);
  const confidenceLevel = getConfidenceLevel(score);
  const color = getConfidenceColor(score);

  return (
    <div className={`confidence-badge ${size} ${confidenceLevel}`}>
      <div className="badge-content">
        <div className="badge-percentage" style={{ color }}>
          {percentage}%
        </div>
        <div className="badge-label">{label}</div>
        {subtitle && <div className="badge-subtitle">{subtitle}</div>}
      </div>
      <div className="badge-indicator" style={{ backgroundColor: color }} />
    </div>
  );
};

/**
 * Get confidence level name
 */
function getConfidenceLevel(score: number): string {
  if (score >= 0.9) return 'high';
  if (score >= 0.7) return 'moderate';
  if (score >= 0.5) return 'low';
  return 'none';
}

/**
 * Get color for confidence score
 */
function getConfidenceColor(score: number): string {
  if (score >= 0.9) return '#22c55e'; // green
  if (score >= 0.7) return '#eab308'; // yellow
  if (score >= 0.5) return '#f97316'; // orange
  return '#ef4444'; // red
}

export default ConfidenceBadge;
