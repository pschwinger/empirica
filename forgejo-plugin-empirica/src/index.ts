// Empirica Epistemic Insight Plugin for Forgejo
// Main entry point

export { CommitInsight } from './components/CommitInsight';
export { ConfidenceBadge } from './components/ConfidenceBadge';
export { LearningDelta } from './components/LearningDelta';
export { VerificationBadge } from './components/VerificationBadge';
export { EmpericaClient } from './api/empirica-client';

// Plugin initialization
export const pluginName = 'empirica-epistemic-insight';
export const pluginVersion = '1.0.0';

export interface PluginConfig {
  apiUrl?: string;
  verifySignatures?: boolean;
  confidenceThreshold?: number;
  showHeatmap?: boolean;
  autoRefreshInterval?: number;
}

export const initializePlugin = (config?: PluginConfig) => {
  console.log('Initializing Empirica Epistemic Insight Plugin', config);
  return {
    name: pluginName,
    version: pluginVersion,
    config: config || {}
  };
};
