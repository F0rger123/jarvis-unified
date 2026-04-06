/**
 * Role Discovery — Specialist Role Loader
 *
 * Discovers specialist roles from a directory of YAML files.
 * Returns a map of role definitions and a formatted list for system prompts.
 */

import { join } from 'node:path';
import { loadRolesFromDir } from '../roles/loader.ts';
import type { RoleDefinition } from '../roles/types.ts';

/** Package root — resolves correctly whether running from repo or global install */
const PACKAGE_ROOT = join(import.meta.dir, '../..');

/**
 * Discover specialist roles from a directory.
 * Resolves relative paths against the package root (not CWD).
 */
export function discoverSpecialists(dir: string): Map<string, RoleDefinition> {
  const resolved = dir.startsWith('/') ? dir : join(PACKAGE_ROOT, dir);
  return loadRolesFromDir(resolved);
}

/**
 * Format the specialist map into a human-readable list for system prompts.
 * The PA sees this and knows what specialists it can delegate to.
 */
export function formatSpecialistList(specialists: Map<string, RoleDefinition>): string {
  if (specialists.size === 0) {
    return '';
  }

  const lines: string[] = ['## Available Specialists', ''];

  for (const [id, role] of specialists) {
    const desc = role.description.split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 0)[0] ?? '';
    const tools = role.tools.join(', ');
    lines.push(`- **${role.name}** (\`${id}\`): ${desc} [tools: ${tools}]`);
  }

  lines.push('');
  lines.push('## Delegation Strategy');
  lines.push('');
  lines.push('**Quick tasks** (research a question, write a draft, analyze data):');
  lines.push('Use `delegate_task` — spawns a specialist, runs to completion, returns result. Blocks until done.');
  lines.push('');
  lines.push('**Complex / parallel work** (research + write, compare multiple topics, multi-step analysis):');
  lines.push('Use `manage_agents`:');
  lines.push('1. `spawn` the specialists you need');
  lines.push('2. `assign` tasks to them (they run in the background in parallel)');
  lines.push('3. `status` to check progress');
  lines.push('4. `collect` results when done');
  lines.push('5. `terminate` agents when no longer needed');
  lines.push('');
  lines.push('**When to delegate:** When a task falls into a specialist\'s domain and benefits from focused expertise.');
  lines.push('For simple questions, handle them yourself. The user can explicitly ask to delegate.');

  return lines.join('\n');
}
