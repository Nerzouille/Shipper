<svelte:options runes={true} />
<script lang="ts">
  let { data }: {
    data: {
      summary?: string;
      go_no_go?: 'go' | 'no-go' | 'conditional';
      key_risks?: string[];
      key_opportunities?: string[];
    }
  } = $props();

  const verdict = $derived(data.go_no_go ?? 'conditional');
  const verdictClass = $derived(
    verdict === 'go' ? 'go' : verdict === 'no-go' ? 'nogo' : 'conditional'
  );
</script>

<div class="step-content">
  <div class="verdict {verdictClass}">
    {#if verdict === 'go'}✓ Go{:else if verdict === 'no-go'}✗ No-Go{:else}⚠ Conditional{/if}
  </div>
  {#if data.summary}
    <p class="summary">{data.summary}</p>
  {/if}
  {#if data.key_opportunities && data.key_opportunities.length}
    <div class="section">
      <h4>Opportunities</h4>
      <ul>{#each data.key_opportunities as o}<li>{o}</li>{/each}</ul>
    </div>
  {/if}
  {#if data.key_risks && data.key_risks.length}
    <div class="section">
      <h4>Risks</h4>
      <ul>{#each data.key_risks as r}<li>{r}</li>{/each}</ul>
    </div>
  {/if}
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.75rem; }
  .verdict { display: inline-block; padding: 0.4rem 1rem; border-radius: 6px; font-weight: 700; font-size: 1rem; }
  .go { background: #d4edda; color: #155724; }
  .nogo { background: #f8d7da; color: #721c24; }
  .conditional { background: #fff3cd; color: #856404; }
  .summary { margin: 0; font-size: 0.9rem; }
  .section h4 { margin: 0 0 0.25rem; font-size: 0.85rem; color: #555; text-transform: uppercase; }
  ul { list-style: disc; padding-left: 1.25rem; margin: 0; font-size: 0.9rem; }
  li { margin-bottom: 0.2rem; }
</style>
