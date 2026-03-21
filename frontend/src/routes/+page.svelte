<svelte:options runes={true} />

<script lang="ts">
  import { createAnalysisStream } from '$lib/sse';
  import type { ConnectionState, SSEEventName } from '$lib/types';

  // Single $state object — workaround for svelte-check 4.4.5 bug:
  // variable name must contain 'state' for rune detection.
  let pageState = $state({
    conn: 'idle' as ConnectionState,
    keyword: '',
    events: [] as Array<{ name: SSEEventName; data: unknown; ts: number }>,
    errorMsg: '',
  });

  let cleanup: (() => void) | null = null;

  const isRunning = $derived(
    pageState.conn === 'connecting' || pageState.conn === 'streaming',
  );

  function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    if (!pageState.keyword.trim()) return;

    cleanup?.();
    pageState.events = [];
    pageState.errorMsg = '';

    cleanup = createAnalysisStream(pageState.keyword, {
      onEvent(name, data) {
        pageState.events = [...pageState.events, { name, data, ts: Date.now() }];
        if (name === 'export_ready') {
          pageState.conn = 'complete';
        }
      },
      onStateChange(state) {
        pageState.conn = state;
      },
      onError(msg) {
        pageState.errorMsg = msg;
        pageState.conn = 'error';
      },
    });
  }

  function handleReset() {
    cleanup?.();
    cleanup = null;
    pageState.conn = 'idle';
    pageState.keyword = '';
    pageState.events = [];
    pageState.errorMsg = '';
  }

  $effect(() => () => cleanup?.());
</script>

<main>
  <h1>Market Intelligence AI</h1>
  <p class="subtitle">Enter a product idea to analyse the market in real time.</p>

  {#if pageState.conn !== 'complete'}
    <form onsubmit={handleSubmit}>
      <input
        type="text"
        bind:value={pageState.keyword}
        placeholder="e.g. eco-friendly bamboo skincare"
        disabled={isRunning}
        aria-label="Product keyword"
      />
      <button type="submit" disabled={isRunning || !pageState.keyword.trim()}>
        {isRunning ? 'Analysing…' : 'Analyse'}
      </button>
    </form>
  {:else}
    <button class="reset" onclick={handleReset}>New analysis</button>
  {/if}

  {#if pageState.errorMsg}
    <p class="error">{pageState.errorMsg}</p>
  {/if}

  {#if pageState.conn === 'connecting'}
    <p class="status">Connecting…</p>
  {/if}

  {#if pageState.events.length > 0}
    <section class="events">
      <h2>SSE events ({pageState.events.length})</h2>
      <ul>
        {#each pageState.events as ev (ev.ts)}
          <li>
            <span class="badge">{ev.name}</span>
            <pre>{JSON.stringify(ev.data, null, 2)}</pre>
          </li>
        {/each}
      </ul>
    </section>
  {/if}

  {#if pageState.conn === 'complete'}
    <p class="done">✓ Analysis complete — export buttons will appear here.</p>
  {/if}
</main>

<style>
  main {
    max-width: 800px;
    margin: 2rem auto;
    padding: 1rem;
    font-family: system-ui, sans-serif;
  }

  h1 { margin-bottom: 0.25rem; }
  .subtitle { color: #666; margin-top: 0; margin-bottom: 1.5rem; }

  form {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  input {
    flex: 1;
    padding: 0.5rem 0.75rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 6px;
  }

  input:disabled { background: #f5f5f5; }

  button {
    padding: 0.5rem 1.25rem;
    font-size: 1rem;
    cursor: pointer;
    border: none;
    border-radius: 6px;
    background: #0070f3;
    color: white;
  }

  button:disabled { opacity: 0.5; cursor: not-allowed; }
  button.reset { background: #555; }

  .status { color: #888; font-style: italic; }
  .error { color: #c00; background: #fee; padding: 0.5rem 0.75rem; border-radius: 4px; }
  .done { color: #060; background: #efe; padding: 0.5rem 0.75rem; border-radius: 4px; }

  .events h2 { font-size: 1rem; margin-bottom: 0.5rem; }

  ul { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }

  li {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    overflow: hidden;
  }

  .badge {
    display: block;
    background: #0070f3;
    color: white;
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
    font-family: monospace;
  }

  pre {
    margin: 0;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
    background: #fafafa;
    overflow-x: auto;
  }
</style>
