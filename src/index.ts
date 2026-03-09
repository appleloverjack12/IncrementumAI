import type { Project } from '@elizaos/core';
import { marketResearchAgent } from './agents/market-research-agent.js';
import { outreachAgent } from './agents/outreach-agent.js';
import { contentAgent } from './agents/content-agent.js';
import { leadQualifierAgent } from './agents/lead-qualifier-agent.js';
import { strategyCoordinatorAgent } from './agents/strategy-coordinator-agent.js';

const project: Project = {
  agents: [
    strategyCoordinatorAgent,
    marketResearchAgent,
    outreachAgent,
    contentAgent,
    leadQualifierAgent
  ],
};

export default project;