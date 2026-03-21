<svelte:options runes={true} />
<script lang="ts">
  let { data, onAction }: { data: { text?: string }; onAction: (a: object) => void } = $props();
  let description = $state(data.text ?? '');

  function submit(e: SubmitEvent) {
    e.preventDefault();
    if (!description.trim()) return;
    onAction({ type: 'user_input', data: { description } });
  }
</script>

<div class="step-content">
  <p class="hint">Describe the product you want to analyse.</p>
  <form onsubmit={submit}>
    <textarea
      bind:value={description}
      placeholder="e.g. ergonomic desk mats for remote workers"
      rows={3}
    ></textarea>
    <button type="submit" disabled={!description.trim()}>Continue →</button>
  </form>
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.75rem; }
  .hint { color: #666; margin: 0; font-size: 0.9rem; }
  textarea { width: 100%; padding: 0.6rem; font-size: 1rem; border: 1px solid #ccc; border-radius: 6px; resize: vertical; font-family: inherit; box-sizing: border-box; }
  button { align-self: flex-start; padding: 0.5rem 1.25rem; background: #0070f3; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
