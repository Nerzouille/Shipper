<svelte:options runes={true} />
<script lang="ts">
  import { createWorkflowConnection, type WorkflowConnection } from '$lib/ws';
  import StepRenderer from '$lib/components/StepRenderer.svelte';
  import type { StepState, WsStatus } from '$lib/workflow-types';

  const WS_URL = 'ws://localhost:8000/ws/workflow';

  let workflowState = $state({
    status: 'idle' as WsStatus,
    description: '',
    totalSteps: 0,
    steps: [] as StepState[],
    activeStepId: '',
    errorMsg: '',
    runId: '',
  });

  let conn: WorkflowConnection | null = null;

  function findOrCreateStep(step_id: string): StepState {
    let s = workflowState.steps.find((s) => s.step_id === step_id);
    if (!s) {
      s = { step_id, step_number: 0, label: step_id, status: 'pending' };
      workflowState.steps = [...workflowState.steps, s];
    }
    return s;
  }

  function updateStep(step_id: string, patch: Partial<StepState>) {
    workflowState.steps = workflowState.steps.map((s) =>
      s.step_id === step_id ? { ...s, ...patch } : s,
    );
  }

  function startWorkflow(e: SubmitEvent) {
    e.preventDefault();
    if (!workflowState.description.trim()) return;

    workflowState.steps = [];
    workflowState.errorMsg = '';
    workflowState.runId = '';

    conn = createWorkflowConnection(WS_URL, {
      onStatusChange(status) {
        workflowState.status = status;
      },
      onError(err) {
        workflowState.errorMsg = err;
      },
      onMessage(msg) {
        if (msg.type === 'workflow_started') {
          workflowState.totalSteps = msg.total_steps;
        } else if (msg.type === 'step_activated') {
          const s = findOrCreateStep(msg.step_id);
          s.step_number = msg.step_number;
          s.label = msg.label;
          updateStep(msg.step_id, { step_number: msg.step_number, label: msg.label, status: 'active' });
          workflowState.activeStepId = msg.step_id;
        } else if (msg.type === 'step_processing') {
          updateStep(msg.step_id, { status: 'processing' });
        } else if (msg.type === 'step_streaming_token') {
          workflowState.steps = workflowState.steps.map((s) =>
            s.step_id === msg.step_id
              ? { ...s, tokens: (s.tokens ?? '') + msg.token, status: 'processing' }
              : s,
          );
        } else if (msg.type === 'step_result') {
          updateStep(msg.step_id, {
            status: 'complete',
            component_type: msg.component_type,
            data: msg.data as Record<string, unknown>,
          });
        } else if (msg.type === 'confirmation_request') {
          updateStep(msg.step_id, {
            status: 'confirmation',
            component_type: msg.component_type,
            data: msg.data as Record<string, unknown>,
          });
        } else if (msg.type === 'step_error') {
          updateStep(msg.step_id, { status: 'error', error: msg.error });
          workflowState.errorMsg = msg.error;
        } else if (msg.type === 'workflow_complete') {
          workflowState.runId = msg.run_id;
          workflowState.status = 'closed';
        }
      },
    });

    conn.send({ type: 'start', description: workflowState.description });
  }

  function handleStepAction(action: object) {
    conn?.send(action);
    // Optimistically update UI for confirmation
    const a = action as { type: string; step_id?: string; confirmed?: boolean };
    if (a.type === 'confirmation' && a.step_id) {
      updateStep(a.step_id, { status: 'complete' });
    }
  }

  function reset() {
    conn?.close();
    conn = null;
    workflowState = {
      status: 'idle',
      description: '',
      totalSteps: 0,
      steps: [],
      activeStepId: '',
      errorMsg: '',
      runId: '',
    };
  }

  $effect(() => () => conn?.close());
</script>

<main>
  <header>
    <h1>Guided Analysis</h1>
    <a href="/">← Home</a>
  </header>

  {#if workflowState.status === 'idle' || workflowState.status === 'closed'}
    {#if workflowState.status === 'closed'}
      <p class="done">✓ Workflow complete (run: {workflowState.runId})</p>
      <button onclick={reset}>Start new analysis</button>
    {:else}
      <form onsubmit={startWorkflow}>
        <input
          type="text"
          bind:value={workflowState.description}
          placeholder="Describe your product idea…"
          aria-label="Product description"
        />
        <button type="submit" disabled={!workflowState.description.trim()}>Start</button>
      </form>
    {/if}
  {:else}
    {#if workflowState.totalSteps > 0}
      <p class="progress">
        Step {workflowState.steps.filter((s) => s.status === 'complete' || s.status === 'confirmation').length}
        / {workflowState.totalSteps}
      </p>
    {/if}

    {#if workflowState.errorMsg}
      <p class="error">{workflowState.errorMsg}</p>
    {/if}

    <div class="steps">
      {#each workflowState.steps as step (step.step_id)}
        <section class="step step--{step.status}">
          <div class="step-header">
            <span class="step-num">{step.step_number}</span>
            <span class="step-label">{step.label}</span>
            {#if step.status === 'processing'}
              <span class="spinner">●</span>
            {/if}
          </div>

          {#if (step.status === 'result' || step.status === 'complete' || step.status === 'confirmation') && step.component_type}
            <div class="step-body">
              <StepRenderer
                componentType={step.component_type}
                data={step.data ?? {}}
                tokens={step.tokens}
                stepId={step.step_id}
                onAction={handleStepAction}
              />
            </div>
          {/if}

          {#if step.status === 'error'}
            <p class="step-error">{step.error}</p>
          {/if}
        </section>
      {/each}
    </div>
  {/if}
</main>

<style>
  main { max-width: 720px; margin: 2rem auto; padding: 1rem; font-family: system-ui, sans-serif; }
  header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
  h1 { margin: 0; }
  a { color: #0070f3; text-decoration: none; font-size: 0.9rem; }
  form { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
  input { flex: 1; padding: 0.5rem 0.75rem; font-size: 1rem; border: 1px solid #ccc; border-radius: 6px; }
  button { padding: 0.5rem 1.25rem; background: #0070f3; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .progress { font-size: 0.85rem; color: #888; margin-bottom: 1rem; }
  .error { background: #fee; color: #c00; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 1rem; }
  .done { background: #efe; color: #060; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 1rem; }
  .steps { display: flex; flex-direction: column; gap: 0.75rem; }
  .step { border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }
  .step--active { border-color: #0070f3; }
  .step--processing { border-color: #f0a000; }
  .step--error { border-color: #c00; }
  .step--complete { border-color: #ccc; }
  .step-header { display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 0.75rem; background: #fafafa; }
  .step--active .step-header { background: #e8f0fe; }
  .step--processing .step-header { background: #fff8e1; }
  .step-num { background: #0070f3; color: white; width: 1.5rem; height: 1.5rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; }
  .step-label { font-weight: 500; font-size: 0.9rem; flex: 1; }
  .spinner { animation: pulse 1s infinite; color: #f0a000; }
  @keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:0.3 } }
  .step-body { padding: 0.75rem; }
  .step-error { color: #c00; font-size: 0.85rem; padding: 0.5rem 0.75rem; margin: 0; }
</style>
