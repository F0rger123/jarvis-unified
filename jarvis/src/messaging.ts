import { getDb, generateId } from '../vault/schema.ts';

export type MessageType = 'task' | 'report' | 'question' | 'escalation';
export type MessagePriority = 'low' | 'normal' | 'high' | 'urgent';

export type AgentMessage = {
  id: string;
  from_agent: string;
  to_agent: string;
  type: MessageType;
  content: string;
  priority: MessagePriority;
  requires_response: boolean;
  deadline: number | null;
  created_at: number;
};

type MessageRow = {
  id: string;
  from_agent: string;
  to_agent: string;
  type: MessageType;
  content: string;
  priority: MessagePriority;
  requires_response: number;
  deadline: number | null;
  created_at: number;
};

/**
 * Convert database row to AgentMessage
 */
function parseMessage(row: MessageRow): AgentMessage {
  return {
    ...row,
    requires_response: row.requires_response === 1,
  };
}

/**
 * Send a message between agents (persisted to SQLite)
 */
export function sendMessage(
  from: string,
  to: string,
  type: MessageType,
  content: string,
  opts?: {
    priority?: MessagePriority;
    requires_response?: boolean;
    deadline?: number;
  }
): AgentMessage {
  const db = getDb();
  const id = generateId();
  const now = Date.now();
  const priority = opts?.priority ?? 'normal';
  const requiresResponse = opts?.requires_response ?? false;
  const deadline = opts?.deadline ?? null;

  const stmt = db.prepare(
    'INSERT INTO agent_messages (id, from_agent, to_agent, type, content, priority, requires_response, deadline, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
  );

  stmt.run(
    id,
    from,
    to,
    type,
    content,
    priority,
    requiresResponse ? 1 : 0,
    deadline,
    now
  );

  return {
    id,
    from_agent: from,
    to_agent: to,
    type,
    content,
    priority,
    requires_response: requiresResponse,
    deadline,
    created_at: now,
  };
}

/**
 * Get messages for an agent
 */
export function getMessages(
  agentId: string,
  opts?: {
    type?: MessageType;
    limit?: number;
  }
): AgentMessage[] {
  const db = getDb();
  const conditions: string[] = ['to_agent = ?'];
  const params: unknown[] = [agentId];

  if (opts?.type) {
    conditions.push('type = ?');
    params.push(opts.type);
  }

  const where = conditions.join(' AND ');
  const limitClause = opts?.limit ? `LIMIT ${opts.limit}` : '';

  const stmt = db.prepare(
    `SELECT * FROM agent_messages WHERE ${where} ORDER BY created_at DESC ${limitClause}`
  );

  const rows = stmt.all(...params as string[]) as MessageRow[];
  return rows.map(parseMessage);
}

/**
 * Get unread/pending messages (all messages for now - could add read tracking)
 */
export function getPendingMessages(agentId: string): AgentMessage[] {
  return getMessages(agentId);
}
