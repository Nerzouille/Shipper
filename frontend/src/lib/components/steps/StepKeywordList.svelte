<svelte:options runes={true} />
<script lang="ts">
  let { data }: { data: { keywords?: string[] } } = $props();
  const keywords = $derived(data.keywords ?? []);
</script>

<div class="step-content">
  <p class="hint">Refined keywords based on your description:</p>
  <ul>
    {#each keywords as kw}
      <li><span class="chip">{kw}</span></li>
    {/each}
  </ul>
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.5rem; }
  .hint { color: #666; margin: 0; font-size: 0.9rem; }
  ul { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 0.5rem; }
  li { margin: 0; }
  .chip { display: inline-block; background: #e8f0fe; color: #1a56db; padding: 0.3rem 0.75rem; border-radius: 999px; font-size: 0.9rem; }
</style>
