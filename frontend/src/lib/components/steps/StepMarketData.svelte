<svelte:options runes={true} />
<script lang="ts">
  let { data }: {
    data: {
      sources_available?: string[];
      sources_unavailable?: string[];
      trend_summary?: string;
      sentiment_summary?: string;
    }
  } = $props();
</script>

<div class="step-content">
  {#if data.sources_unavailable && data.sources_unavailable.length > 0}
    <p class="warning">⚠ Some sources unavailable: {data.sources_unavailable.join(', ')}</p>
  {/if}
  {#if data.trend_summary}
    <div class="section">
      <h4>Trends</h4>
      <p>{data.trend_summary}</p>
    </div>
  {/if}
  {#if data.sentiment_summary}
    <div class="section">
      <h4>Community Sentiment</h4>
      <p>{data.sentiment_summary}</p>
    </div>
  {/if}
  <p class="sources">Sources available: {(data.sources_available ?? []).join(', ') || 'none'}</p>
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.75rem; }
  .warning { background: #fff8e1; color: #856404; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0; font-size: 0.9rem; }
  .section h4 { margin: 0 0 0.25rem; font-size: 0.9rem; color: #555; text-transform: uppercase; letter-spacing: 0.05em; }
  .section p { margin: 0; font-size: 0.9rem; }
  .sources { font-size: 0.8rem; color: #888; margin: 0; }
</style>
