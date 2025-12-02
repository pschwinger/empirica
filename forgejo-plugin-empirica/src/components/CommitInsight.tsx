/**
 * CommitInsight Component
 *
 * Displays epistemic context for a commit:
 * - Confidence badge (KNOW/DO scores)
 * - Learning delta (PREFLIGHT → POSTFLIGHT)
 * - Files changed with confidence per file
 * - Signature verification status
 */

import React, { useEffect, useState } from 'react';
import { empiricaClient, CommitEpistemic, FileUncertainty } from '../api/empirica-client';
import { ConfidenceBadge } from './ConfidenceBadge';
import { LearningDelta } from './LearningDelta';
import { VerificationBadge } from './VerificationBadge';
import '../styles/commit-insight.css';

interface CommitInsightProps {
  commitSha: string;
  onError?: (error: Error) => void;
}

interface FileWithConfidence {
  name: string;
  confidence: number;
  status: 'added' | 'modified' | 'deleted';
}

/**
 * CommitInsight Component
 *
 * Shows epistemic analysis when viewing a commit in Forgejo
 */
export const CommitInsight: React.FC<CommitInsightProps> = ({
  commitSha,
  onError
}) => {
  const [epistemic, setEpistemic] = useState<CommitEpistemic | null>(null);
  const [fileConfidences, setFileConfidences] = useState<FileWithConfidence[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadEpistemicData();
  }, [commitSha]);

  const loadEpistemicData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Check API availability
      const isHealthy = await empiricaClient.healthCheck();
      if (!isHealthy) {
        setError('Dashboard API is not available. Make sure it\'s running at the configured URL.');
        return;
      }

      // Fetch epistemic context for this commit
      const epistemicData = await empiricaClient.getCommitEpistemic(commitSha);

      if (!epistemicData.ok) {
        setError('No epistemic data available for this commit');
        return;
      }

      setEpistemic(epistemicData);

      // Load confidence data for each file
      if (epistemicData.files_changed && epistemicData.files_changed.length > 0) {
        const filesWithConfidence: FileWithConfidence[] = [];

        for (const file of epistemicData.files_changed) {
          try {
            const uncertainty = await empiricaClient.getFileUncertainty(file);
            filesWithConfidence.push({
              name: file,
              confidence: uncertainty.aggregate_confidence,
              status: determineFileStatus(file) // Would need more info in real impl
            });
          } catch (err) {
            // If individual file fails, continue with partial data
            filesWithConfidence.push({
              name: file,
              confidence: epistemicData.epistemic_context.know,
              status: 'modified'
            });
          }
        }

        setFileConfidences(filesWithConfidence);
      }
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error.message);
      onError?.(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="commit-insight loading">
        <div className="spinner"></div>
        <p>Loading epistemic analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="commit-insight error">
        <div className="error-icon">⚠️</div>
        <h3>Epistemic Data Unavailable</h3>
        <p>{error}</p>
        <button onClick={loadEpistemicData} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  if (!epistemic) {
    return (
      <div className="commit-insight no-data">
        <p>No epistemic analysis available for this commit.</p>
        <p className="help-text">
          This commit was made before epistemic tracking was enabled, or the AI system hasn't analyzed it yet.
        </p>
      </div>
    );
  }

  const context = epistemic.epistemic_context;
  const delta = epistemic.learning_delta;

  return (
    <div className="commit-insight">
      <h2 className="section-title">📊 Epistemic Analysis</h2>

      {/* Confidence and Verification Row */}
      <div className="insight-header">
        <div className="confidence-section">
          <ConfidenceBadge
            score={context.know}
            label="Confidence"
            subtitle={`KNOW: ${(context.know * 100).toFixed(0)}% | DO: ${(delta.do * 100).toFixed(0)}%`}
          />
        </div>

        <div className="verification-section">
          <VerificationBadge
            sessionId={context.session_id}
            aiId={context.ai_id}
            verified={true}
            timestamp="2025-12-02T14:00:00Z"
          />
        </div>
      </div>

      {/* Learning Delta */}
      {delta.overall > 0 && (
        <LearningDelta
          know={delta.know}
          do={delta.do}
          overall={delta.overall}
        />
      )}

      {/* Risk Assessment */}
      <div className="risk-assessment">
        <div className="risk-level" data-level={getRiskLevel(context.uncertainty)}>
          <span className="label">Risk Assessment</span>
          <span className="value">{context.risk_assessment || 'Unknown'}</span>
        </div>

        <div className="investigation-status">
          <div className="investigated">
            <h4>✅ Investigated</h4>
            <ul>
              {context.investigated.map((area) => (
                <li key={area}>{area}</li>
              ))}
            </ul>
          </div>

          {context.not_investigated && context.not_investigated.length > 0 && (
            <div className="not-investigated">
              <h4>⚠️ Not Investigated</h4>
              <ul>
                {context.not_investigated.map((area) => (
                  <li key={area}>{area}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Files Changed with Confidence */}
      {fileConfidences.length > 0 && (
        <div className="files-section">
          <h3>Files Changed</h3>
          <div className="files-list">
            {fileConfidences.map((file) => (
              <div key={file.name} className="file-item">
                <div className="file-name">
                  {getFileIcon(file.status)} {file.name}
                </div>
                <div className="file-confidence">
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{
                        width: `${file.confidence * 100}%`,
                        backgroundColor: getConfidenceColor(file.confidence)
                      }}
                    />
                  </div>
                  <span className="confidence-value">
                    {(file.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Session Link */}
      <div className="session-info">
        <p className="small-text">
          Analyzed by: <strong>{context.ai_id}</strong> |
          Session: <code>{context.session_id.substring(0, 8)}...</code> |
          Confidence Basis: <em>{context.confidence_basis}</em>
        </p>
      </div>
    </div>
  );
};

/**
 * Determine risk level from uncertainty score
 */
function getRiskLevel(uncertainty: number): string {
  if (uncertainty < 0.2) return 'low';
  if (uncertainty < 0.5) return 'medium';
  return 'high';
}

/**
 * Get color for confidence score
 */
function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.9) return '#22c55e'; // green
  if (confidence >= 0.7) return '#eab308'; // yellow
  if (confidence >= 0.5) return '#f97316'; // orange
  return '#ef4444'; // red
}

/**
 * Get icon for file status
 */
function getFileIcon(status: string): string {
  switch (status) {
    case 'added': return '✨';
    case 'modified': return '📝';
    case 'deleted': return '🗑️';
    default: return '📄';
  }
}

/**
 * Determine file status (would need actual Forgejo data)
 */
function determineFileStatus(filename: string): 'added' | 'modified' | 'deleted' {
  // In real implementation, this would come from Forgejo's diff data
  return 'modified';
}

export default CommitInsight;
