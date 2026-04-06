import type { AgentInstance } from './agent.ts';

export type AgentTreeNode = {
  agent: AgentInstance;
  children: AgentTreeNode[];
};

export class AgentHierarchy {
  private agents: Map<string, AgentInstance>;
  private children: Map<string, Set<string>>; // parent_id -> child_ids

  constructor() {
    this.agents = new Map();
    this.children = new Map();
  }

  addAgent(agent: AgentInstance): void {
    this.agents.set(agent.id, agent);

    // Track parent-child relationship
    const parentId = agent.agent.parent_id;
    if (parentId) {
      if (!this.children.has(parentId)) {
        this.children.set(parentId, new Set());
      }
      this.children.get(parentId)!.add(agent.id);
    }
  }

  removeAgent(agentId: string): void {
    const agent = this.agents.get(agentId);
    if (!agent) return;

    // Recursively remove all children first
    const childIds = this.children.get(agentId);
    if (childIds) {
      for (const childId of Array.from(childIds)) {
        this.removeAgent(childId);
      }
      this.children.delete(agentId);
    }

    // Remove from parent's children set
    const parentId = agent.agent.parent_id;
    if (parentId) {
      const siblings = this.children.get(parentId);
      if (siblings) {
        siblings.delete(agentId);
      }
    }

    // Remove the agent
    this.agents.delete(agentId);
  }

  getAgent(agentId: string): AgentInstance | undefined {
    return this.agents.get(agentId);
  }

  getChildren(agentId: string): AgentInstance[] {
    const childIds = this.children.get(agentId);
    if (!childIds) return [];

    return Array.from(childIds)
      .map((id) => this.agents.get(id))
      .filter((agent): agent is AgentInstance => agent !== undefined);
  }

  getParent(agentId: string): AgentInstance | undefined {
    const agent = this.agents.get(agentId);
    if (!agent?.agent.parent_id) return undefined;

    return this.agents.get(agent.agent.parent_id);
  }

  getPrimary(): AgentInstance | undefined {
    // Find the agent with no parent
    for (const agent of this.agents.values()) {
      if (agent.agent.parent_id === null) {
        return agent;
      }
    }
    return undefined;
  }

  getAllAgents(): AgentInstance[] {
    return Array.from(this.agents.values());
  }

  getActiveAgents(): AgentInstance[] {
    return this.getAllAgents().filter((agent) => agent.status === 'active');
  }

  /**
   * Get the full tree structure for display
   */
  getTree(): AgentTreeNode {
    const primary = this.getPrimary();
    if (!primary) {
      throw new Error('No primary agent found in hierarchy');
    }

    return this.buildTreeNode(primary);
  }

  private buildTreeNode(agent: AgentInstance): AgentTreeNode {
    const children = this.getChildren(agent.id);
    return {
      agent,
      children: children.map((child) => this.buildTreeNode(child)),
    };
  }
}
