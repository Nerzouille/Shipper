/**
 * SSE stream client — BFF pattern.
 *
 * The browser connects to SvelteKit's /api/sse proxy, never to FastAPI directly.
 * Each named SSE event is dispatched to the appropriate callback after JSON parsing.
 */

import type { ConnectionState, SSEEventName } from './types';

export interface SSEEventCallbacks {
  onEvent: (eventName: SSEEventName, data: unknown) => void;
  onStateChange: (state: ConnectionState) => void;
  onError: (message: string) => void;
}

/**
 * Open an SSE stream for the given keyword.
 * Returns a cleanup function that closes the EventSource.
 */
export function createAnalysisStream(
  keyword: string,
  callbacks: SSEEventCallbacks,
): () => void {
  const url = `/api/sse?keyword=${encodeURIComponent(keyword)}`;
  callbacks.onStateChange('connecting');

  const source = new EventSource(url);

  source.onopen = () => {
    callbacks.onStateChange('streaming');
  };

  // Listen for each named SSE event
  const eventNames: SSEEventName[] = [
    'marketplace_products',
    'viability_score',
    'target_persona',
    'differentiation_angles',
    'competitive_overview',
    'export_ready',
    'source_unavailable',
  ];

  for (const name of eventNames) {
    source.addEventListener(name, (event: Event) => {
      if (!(event instanceof MessageEvent)) return;
      try {
        const data = JSON.parse(event.data as string);
        callbacks.onEvent(name, data);
      } catch {
        callbacks.onError(`Failed to parse ${name} event`);
      }
    });
  }

  // Unnamed messages (fallback)
  source.onmessage = (event: MessageEvent<string>) => {
    try {
      const data = JSON.parse(event.data);
      callbacks.onEvent('marketplace_products', data); // best-effort fallback
    } catch {
      callbacks.onError('Failed to parse SSE message');
    }
  };

  // Named 'error' event from server vs connection drop
  source.addEventListener('error', (event: Event) => {
    if (event instanceof MessageEvent) {
      callbacks.onError((event.data as string) ?? 'Server error');
    } else {
      // Connection drop — stream ended or backend down
      callbacks.onStateChange('complete');
    }
    source.close();
  });

  return () => source.close();
}
