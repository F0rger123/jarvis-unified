import type { AgentInstance } from './agent.ts';
import type { Commitment } from '../vault/commitments.ts';
import { createCommitment } from '../vault/commitments.ts';
import { sendMessage, type MessagePriority } from './messaging.ts';

export type DelegationResult = {
  success: boolean;
  agent_id: string;
  commitment_id: string;
  message?: string;
};

/**
 * Delegate a task from parent to child agent
 */
export function delegateTask(
  parent: AgentInstance,
  child: AgentInstance,
  task: {
    what: string;
    context: string;
    priority?: 'low' | 'normal' | 'high' | 'critical';
    deadline?: number;
  }
): DelegationResult {
  // Verify parent-child relationship
  if (child.agent.parent_id !== parent.id) {
    return {
      success: false,
      agent_id: child.id,
      commitment_id: '',
      message: 'Agent is not a child of the parent agent',
    };
  }

  // Verify parent has authority to spawn children
  if (!parent.agent.authority.can_spawn_children) {
    return {
      success: false,
      agent_id: child.id,
      commitment_id: '',
      message: 'Parent agent does not have authority to delegate tasks',
    };
  }

  // Create a commitment for the child agent
  const commitment = createCommitment(task.what, {
    context: task.context,
    priority: task.priority ?? 'normal',
    when_due: task.deadline,
    assigned_to: child.id,
    created_from: parent.id,
  });

  // Send a task message to the child
  const message = sendMessage(parent.id, child.id, 'task', task.what, {
    priority: (task.priority === 'critical' ? 'urgent' : task.priority ?? 'normal') as MessagePriority,
    requires_response: true,
    deadline: task.deadline,
  });

  // Set the task on the child agent
  child.setTask(task.what);

  return {
    success: true,
    agent_id: child.id,
    commitment_id: commitment.id,
    message: `Task delegated successfully (message: ${message.id})`,
  };
}

/**
 * Report task completion back to parent
 */
export function reportCompletion(
  child: AgentInstance,
  parent: AgentInstance,
  result: {
    success: boolean;
    summary: string;
    details?: string;
  }
): void {
  // Verify parent-child relationship
  if (child.agent.parent_id !== parent.id) {
    throw new Error('Agent is not a child of the specified parent');
  }

  // Build report content
  const content = JSON.stringify({
    task: child.agent.current_task,
    success: result.success,
    summary: result.summary,
    details: result.details,
  });

  // Send a report message to the parent
  sendMessage(child.id, parent.id, 'report', content, {
    priority: result.success ? 'normal' : 'high',
    requires_response: false,
  });

  // Clear the child's current task
  child.clearTask();
  child.idle();
}
