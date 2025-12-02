/**
 * VerificationBadge Component
 *
 * Shows crypto signature verification status
 * - ✅ Verified: Signature valid, shows AI identity
 * - ⏳ Pending: Not yet verified
 * - ❌ Failed: Signature invalid or tampered
 */

import React, { useEffect, useState } from 'react';
import { empiricaClient } from '../api/empirica-client';
import '../styles/badges.css';

interface VerificationBadgeProps {
  sessionId: string;
  aiId: string;
  verified?: boolean;
  timestamp?: string;
  phase?: string;
  round?: number;
  onVerified?: (verified: boolean) => void;
}

export const VerificationBadge: React.FC<VerificationBadgeProps> = ({
  sessionId,
  aiId,
  verified: initialVerified = false,
  timestamp = new Date().toISOString(),
  phase = 'POSTFLIGHT',
  round = 1,
  onVerified
}) => {
  const [isVerified, setIsVerified] = useState(initialVerified);
  const [isChecking, setIsChecking] = useState(!initialVerified);
  const [publicKey, setPublicKey] = useState<string | null>(null);

  useEffect(() => {
    if (!initialVerified) {
      verifySignature();
    }
  }, [sessionId, phase, round]);

  const verifySignature = async () => {
    try {
      setIsChecking(true);
      const result = await empiricaClient.verifyCheckpoint(
        sessionId,
        phase,
        round
      );

      setIsVerified(result.signature_verified);
      if (result.public_key) {
        setPublicKey(result.public_key);
      }
      onVerified?.(result.signature_verified);
    } catch (error) {
      console.error('Verification failed:', error);
      setIsVerified(false);
    } finally {
      setIsChecking(false);
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  if (isChecking) {
    return (
      <div className="verification-badge checking">
        <span className="verification-icon">⏳</span>
        <span className="verification-text">Verifying...</span>
      </div>
    );
  }

  return (
    <div className={`verification-badge ${isVerified ? 'verified' : 'unverified'}`}>
      <div className="verification-content">
        <span className="verification-icon">
          {isVerified ? '✅' : '❌'}
        </span>
        <div className="verification-details">
          <div className="verification-status">
            {isVerified ? 'Verified' : 'Not Verified'}
          </div>
          <div className="verification-info">
            <span className="info-ai">by {aiId}</span>
            <span className="info-date">{formatDate(timestamp)}</span>
          </div>
        </div>
      </div>

      {publicKey && isVerified && (
        <div className="verification-details-tooltip">
          <p className="small-text">
            <strong>Ed25519 Public Key:</strong>
            <br />
            <code>{publicKey}</code>
          </p>
          <p className="small-text">
            This commit's epistemic analysis was cryptographically signed by the
            listed AI system and can be independently verified.
          </p>
        </div>
      )}

      {!isVerified && (
        <button
          className="retry-verify"
          onClick={verifySignature}
          title="Retry verification"
        >
          🔄
        </button>
      )}
    </div>
  );
};

export default VerificationBadge;
