/**
 * LearningDelta Component
 *
 * Shows epistemic changes from PREFLIGHT to POSTFLIGHT
 * Displays delta bars for each vector with positive/negative indicators
 */

import React from 'react';
import '../styles/learning-delta.css';

interface LearningDeltaProps {
  know: number;
  do: number;
  overall: number;
  context?: number;
  clarity?: number;
}

export const LearningDelta: React.FC<LearningDeltaProps> = ({
  know,
  do: doScore,
  overall,
  context,
  clarity
}) => {
  const deltas = [
    { label: 'KNOW', value: know, emoji: '📚' },
    { label: 'DO', value: doScore, emoji: '⚙️' },
    ...(context !== undefined ? [{ label: 'CONTEXT', value: context, emoji: '🗺️' }] : []),
    ...(clarity !== undefined ? [{ label: 'CLARITY', value: clarity, emoji: '✨' }] : [])
  ];

  return (
    <div className="learning-delta">
      <h3 className="delta-title">📈 Learning Progress</h3>

      <div className="overall-delta">
        <div className="delta-metric">
          <span className="metric-label">Overall Learning</span>
          <div className="metric-bar">
            <div
              className="metric-fill positive"
              style={{ width: `${Math.min(overall * 100, 100)}%` }}
            />
          </div>
          <span className="metric-value">+{(overall * 100).toFixed(0)}%</span>
        </div>
      </div>

      <div className="delta-breakdown">
        {deltas.map((delta) => (
          <div key={delta.label} className="delta-item">
            <div className="delta-header">
              <span className="delta-emoji">{delta.emoji}</span>
              <span className="delta-label">{delta.label}</span>
              <span className={`delta-value ${delta.value > 0 ? 'positive' : 'negative'}`}>
                {delta.value > 0 ? '+' : ''}{(delta.value * 100).toFixed(0)}%
              </span>
            </div>
            <div className="delta-bar">
              <div
                className={`delta-bar-fill ${delta.value > 0 ? 'positive' : 'negative'}`}
                style={{
                  width: `${Math.abs(delta.value) * 100}%`
                }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className="delta-interpretation">
        <p className="interpretation-text">
          {overall > 0.2 && (
            <>
              ✅ <strong>Significant learning</strong> occurred during this session. The AI developed
              new understanding and capability.
            </>
          )}
          {overall > 0.1 && overall <= 0.2 && (
            <>
              ✓ <strong>Moderate learning</strong> occurred. The AI gained some new confidence.
            </>
          )}
          {overall <= 0.1 && (
            <>
              → <strong>Minimal learning</strong> or refactoring work. The AI was mostly working
              within existing confidence bounds.
            </>
          )}
        </p>
      </div>
    </div>
  );
};

export default LearningDelta;
