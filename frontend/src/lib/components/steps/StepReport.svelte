<svelte:options runes={true} />
<script lang="ts">
  let { data }: { data: { run_id?: string; markdown_available?: boolean; note?: string } } = $props();
</script>

<div class="step-content">
  <p class="done">✓ Report generated</p>
  {#if data.run_id}
    <p class="meta">Run ID: <code>{data.run_id}</code></p>
  {/if}
  {#if data.note}
    <p class="note">{data.note}</p>
  {/if}
  {#if data.markdown_available}
    <a href="/api/export/md?run_id={data.run_id}" class="export-btn">Export Markdown</a>
  {:else}
    <p class="soon">Export not yet available (stub).</p>
  {/if}
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.75rem; }
  .done { color: #155724; background: #d4edda; padding: 0.5rem 0.75rem; border-radius: 6px; margin: 0; font-weight: 500; }
  .meta { font-size: 0.85rem; color: #555; margin: 0; }
  code { background: #f0f0f0; padding: 0.1rem 0.4rem; border-radius: 4px; }
  .note { font-size: 0.85rem; color: #888; margin: 0; }
  .soon { font-size: 0.85rem; color: #888; font-style: italic; margin: 0; }
  .export-btn { display: inline-block; padding: 0.5rem 1.25rem; background: #0070f3; color: white; text-decoration: none; border-radius: 6px; font-size: 0.9rem; }
</style>
