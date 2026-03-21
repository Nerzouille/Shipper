<svelte:options runes={true} />
<script lang="ts">
  let { data, onAction, stepId }: {
    data: { prompt?: string };
    onAction: (a: object) => void;
    stepId: string;
  } = $props();

  function confirm(confirmed: boolean) {
    onAction({ type: 'confirmation', step_id: stepId, confirmed });
  }
</script>

<div class="step-content">
  <p class="prompt">{data.prompt ?? 'Does this look correct?'}</p>
  <div class="actions">
    <button class="yes" onclick={() => confirm(true)}>Yes, continue →</button>
    <button class="no" onclick={() => confirm(false)}>No, redo</button>
  </div>
</div>

<style>
  .step-content { display: flex; flex-direction: column; gap: 0.75rem; }
  .prompt { font-weight: 500; margin: 0; }
  .actions { display: flex; gap: 0.75rem; }
  button { padding: 0.5rem 1.25rem; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; }
  .yes { background: #0070f3; color: white; }
  .no { background: #eee; color: #333; }
</style>
