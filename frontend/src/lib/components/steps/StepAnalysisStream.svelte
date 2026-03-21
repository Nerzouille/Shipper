<svelte:options runes={true} />
<script lang="ts">
  let { data, tokens }: { data: { complete?: boolean; content?: string }; tokens?: string } = $props();
  const content = $derived(data.content ?? tokens ?? '');
  const isComplete = $derived(data.complete ?? false);
</script>

<div class="step-content">
  {#if !isComplete && content === ''}
    <p class="loading">Analysing…</p>
  {/if}
  {#if content}
    <div class="content" class:streaming={!isComplete}>
      <p>{content}</p>
    </div>
  {/if}
  {#if isComplete}
    <span class="badge">✓ Analysis complete</span>
  {/if}
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.5rem; }
  .loading { color: #888; font-style: italic; margin: 0; }
  .content { background: #fafafa; border: 1px solid #e0e0e0; border-radius: 6px; padding: 0.75rem; }
  .content.streaming { border-color: #0070f3; }
  .content p { margin: 0; font-size: 0.9rem; line-height: 1.6; white-space: pre-wrap; }
  .badge { font-size: 0.8rem; color: #060; background: #efe; padding: 0.2rem 0.6rem; border-radius: 999px; }
</style>
