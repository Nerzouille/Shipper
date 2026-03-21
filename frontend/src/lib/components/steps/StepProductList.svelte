<svelte:options runes={true} />
<script lang="ts">
  let { data }: { data: { products?: Array<{title: string; price: string; url: string}> } } = $props();
  const products = $derived(data.products ?? []);
</script>

<div class="step-content">
  <p class="hint">{products.length} product{products.length !== 1 ? 's' : ''} found:</p>
  <ul>
    {#each products as p}
      <li>
        <span class="title">{p.title}</span>
        <span class="price">{p.price}</span>
        <a href={p.url} target="_blank" rel="noopener">View →</a>
      </li>
    {/each}
  </ul>
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.5rem; }
  .hint { color: #666; margin: 0; font-size: 0.9rem; }
  ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.5rem; }
  li { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: #fafafa; border: 1px solid #e0e0e0; border-radius: 6px; }
  .title { flex: 1; font-weight: 500; font-size: 0.9rem; }
  .price { color: #060; font-size: 0.9rem; }
  a { font-size: 0.85rem; color: #0070f3; text-decoration: none; }
</style>
