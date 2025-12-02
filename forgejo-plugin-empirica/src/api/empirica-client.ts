/**
 * Empirica Dashboard API Client
 *
 * Wrapper around the Dashboard API (Phase 3.3) endpoints
 * Used by plugin components to fetch epistemic data
 */

import axios, { AxiosInstance, AxiosError } from 'axios';

export interface EpistemicVector {
  know: number;
  do: number;
  context?: number;
  clarity?: number;
  coherence?: number;
  signal?: number;
  density?: number;
  state?: number;
  change?: number;
  completion?: number;
  impact?: number;
  engagement?: number;
  uncertainty: number;
}

export interface SessionDelta {
  ok: boolean;
  session_id: string;
  deltas: Record<string, { preflight: number; postflight: number; delta: number }>;
  learning_velocity: {
    know_per_minute: number;
    overall_per_minute: number;
  };
  git_correlation: {
    commit_sha: string;
    files_changed: string[];
    lines_added: number;
    lines_removed: number;
    correlation_strength: string;
  };
}

export interface CommitEpistemic {
  ok: boolean;
  commit_sha: string;
  commit_message: string;
  files_changed: string[];
  lines_added: number;
  lines_removed: number;
  epistemic_context: {
    session_id: string;
    ai_id: string;
    know: number;
    uncertainty: number;
    investigated: string[];
    not_investigated: string[];
    confidence_basis: string;
    risk_assessment: string;
  };
  learning_delta: {
    know: number;
    do: number;
    overall: number;
  };
}

export interface VerificationResult {
  ok: boolean;
  checkpoint_id: string;
  git_note_sha: string;
  signature_verified: boolean;
  signed_by: string;
  signature_date: string;
  public_key: string;
  content_hash: string;
  verification_method: string;
}

export interface FileUncertainty {
  ok: boolean;
  filepath: string;
  uncertainty_metrics: {
    overall_uncertainty: number;
    know: number;
    do: number;
    investigated_areas: string[];
    not_investigated: string[];
    risk_level: string;
  };
  changes_made: Array<{
    session_id: string;
    commit_sha: string;
    lines_added: number;
    lines_removed: number;
    confidence: number;
    timestamp: string;
  }>;
  aggregate_confidence: number;
}

export interface AILearningCurve {
  ok: boolean;
  ai_id: string;
  total_sessions: number;
  time_period: string;
  learning_trajectory: Array<{
    session_id: string;
    timestamp: string;
    know: number;
    do: number;
    uncertainty: number;
    overall_confidence: number;
  }>;
  statistics: {
    average_know: number;
    average_uncertainty: number;
    learning_velocity: number;
    trend: string;
  };
}

/**
 * Empirica Dashboard API Client
 *
 * Provides typed access to all Dashboard API endpoints
 */
export class EmpericaClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8000/api/v1') {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });
  }

  /**
   * Get epistemic context for a specific commit
   */
  async getCommitEpistemic(commitSha: string): Promise<CommitEpistemic> {
    try {
      const response = await this.client.get<CommitEpistemic>(
        `/commits/${commitSha}/epistemic`
      );
      return response.data;
    } catch (error) {
      this.handleError(error, `Failed to fetch commit epistemic: ${commitSha}`);
      throw error;
    }
  }

  /**
   * Get learning deltas for a session
   */
  async getSessionDeltas(sessionId: string): Promise<SessionDelta> {
    try {
      const response = await this.client.get<SessionDelta>(
        `/sessions/${sessionId}/deltas`
      );
      return response.data;
    } catch (error) {
      this.handleError(error, `Failed to fetch session deltas: ${sessionId}`);
      throw error;
    }
  }

  /**
   * Verify signature of a checkpoint
   */
  async verifyCheckpoint(
    sessionId: string,
    phase: string,
    round: number,
    publicKey?: string
  ): Promise<VerificationResult> {
    try {
      const params = publicKey ? { public_key: publicKey } : {};
      const response = await this.client.get<VerificationResult>(
        `/checkpoints/${sessionId}/${phase}/${round}/verify`,
        { params }
      );
      return response.data;
    } catch (error) {
      this.handleError(
        error,
        `Failed to verify checkpoint: ${sessionId}/${phase}/${round}`
      );
      throw error;
    }
  }

  /**
   * Get file uncertainty/confidence metrics
   */
  async getFileUncertainty(filepath: string): Promise<FileUncertainty> {
    try {
      const response = await this.client.get<FileUncertainty>(
        `/files/${encodeURIComponent(filepath)}/uncertainty`
      );
      return response.data;
    } catch (error) {
      this.handleError(error, `Failed to fetch file uncertainty: ${filepath}`);
      throw error;
    }
  }

  /**
   * Get AI learning curve over time
   */
  async getAILearningCurve(
    aiId: string,
    since?: string,
    limit?: number
  ): Promise<AILearningCurve> {
    try {
      const params: Record<string, string | number> = {};
      if (since) params.since = since;
      if (limit) params.limit = limit;

      const response = await this.client.get<AILearningCurve>(
        `/ai/${aiId}/learning-curve`,
        { params }
      );
      return response.data;
    } catch (error) {
      this.handleError(error, `Failed to fetch AI learning curve: ${aiId}`);
      throw error;
    }
  }

  /**
   * Compare learning curves across multiple AIs
   */
  async compareAIs(
    aiIds: string[],
    since?: string,
    metric?: string
  ): Promise<any> {
    try {
      const params: Record<string, string> = {
        ai_ids: aiIds.join(',')
      };
      if (since) params.since = since;
      if (metric) params.metric = metric;

      const response = await this.client.get('/compare-ais', { params });
      return response.data;
    } catch (error) {
      this.handleError(error, `Failed to compare AIs: ${aiIds.join(', ')}`);
      throw error;
    }
  }

  /**
   * Health check - verify API is available
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await axios.get(`${this.baseUrl.replace('/api/v1', '')}/health`);
      return response.status === 200;
    } catch (error) {
      console.warn('Dashboard API health check failed', error);
      return false;
    }
  }

  /**
   * Get API base URL
   */
  getBaseUrl(): string {
    return this.baseUrl;
  }

  /**
   * Handle API errors with logging
   */
  private handleError(error: unknown, message: string): void {
    if (axios.isAxiosError(error)) {
      console.error(message, {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      });
    } else {
      console.error(message, error);
    }
  }
}

// Export singleton instance
export const empiricaClient = new EmpericaClient();
