<svelte:options runes={true} />
<script lang="ts">
  import StepRenderer from '$lib/components/StepRenderer.svelte';

  // Fake data for each component type
  const fixtures = [
    {
      title: 'StepDescriptionInput',
      componentType: 'product_description_input',
      stepId: 'product_description',
      data: { text: 'ergonomic desk mats for remote workers' },
    },
    {
      title: 'StepKeywordList',
      componentType: 'keyword_list',
      stepId: 'keyword_refinement',
      data: { keywords: ['ergonomic desk mat', 'office accessories', 'wrist rest pad', 'desk setup'] },
    },
    {
      title: 'StepConfirmation',
      componentType: 'confirmation',
      stepId: 'keyword_confirmation',
      data: { prompt: 'Do these keywords look correct for your product idea?' },
    },
    {
      title: 'StepProductList',
      componentType: 'product_list',
      stepId: 'product_research',
      data: {
        products: [
          { title: 'ProDesk Anti-Fatigue Mat', price: '$34.99', url: 'https://example.com/1' },
          { title: 'ErgoMat Premium Desk Pad', price: '$49.99', url: 'https://example.com/2' },
          { title: 'ComfortPlus Office Mat', price: '$27.99', url: 'https://example.com/3' },
        ],
      },
    },
    {
      title: 'StepMarketData',
      componentType: 'market_data_summary',
      stepId: 'market_research',
      data: {
        sources_available: ['amazon', 'google_trends'],
        sources_unavailable: ['reddit'],
        trend_summary: 'Search volume for "ergonomic desk mat" has grown 24% YoY, with peaks in January and September.',
        sentiment_summary: 'Community discussions highlight comfort and durability as primary purchase drivers.',
      },
    },
    {
      title: 'StepAnalysisStream — Streaming',
      componentType: 'analysis_stream',
      stepId: 'ai_analysis',
      data: { complete: false, content: '' },
      tokens: 'The ergonomic desk mat market shows moderate competition with strong growth potential…',
    },
    {
      title: 'StepAnalysisStream — Complete',
      componentType: 'analysis_stream',
      stepId: 'ai_analysis_done',
      data: {
        complete: true,
        content: 'The market shows 42/100 viability. Key differentiators: eco-friendly materials and customizable sizing. Primary risk: high competition from established brands.',
      },
    },
    {
      title: 'StepFinalCriteria — Go',
      componentType: 'final_criteria',
      stepId: 'final_criteria_go',
      data: {
        summary: 'The product shows solid market potential with identifiable differentiation angles.',
        go_no_go: 'go',
        key_risks: ['High competition from Amazon brands', 'Price sensitivity in mid-market'],
        key_opportunities: ['Eco-friendly niche underserved', 'B2B office supply channel', 'Subscription model for replacements'],
      },
    },
    {
      title: 'StepFinalCriteria — No-Go',
      componentType: 'final_criteria',
      stepId: 'final_criteria_nogo',
      data: {
        summary: 'Market is saturated with low-cost alternatives and low differentiation potential.',
        go_no_go: 'no-go',
        key_risks: ['Margin compression from Asian suppliers', 'Brand recognition barrier', 'High customer acquisition cost'],
        key_opportunities: ['Premium segment niche (small TAM)'],
      },
    },
    {
      title: 'StepFinalCriteria — Conditional',
      componentType: 'final_criteria',
      stepId: 'final_criteria_cond',
      data: {
        summary: 'Viable if product differentiates on eco-certification and targets B2B.',
        go_no_go: 'conditional',
        key_risks: ['Eco-certification cost', 'B2B sales cycle length'],
        key_opportunities: ['Corporate sustainability mandates', 'Government procurement'],
      },
    },
    {
      title: 'StepReport',
      componentType: 'report',
      stepId: 'report_generation',
      data: {
        run_id: 'abc123-fake-run-id',
        markdown_available: false,
        note: 'Report stub — export will be available once business logic is implemented.',
      },
    },
  ];

  let actions = $state<string[]>([]);

  function handleAction(label: string, action: object) {
    actions = [`[${label}] ${JSON.stringify(action)}`, ...actions.slice(0, 9)];
  }
</script>

<main>
  <header>
    <h1>Component Test Page</h1>
    <a href="/">← Home</a>
  </header>
  <p class="subtitle">All workflow step components with fake data. Use this page to verify component rendering before connecting to the WebSocket backend.</p>

  {#if actions.length > 0}
    <section class="action-log">
      <h3>Action Log (last 10)</h3>
      <ul>
        {#each actions as a}
          <li><code>{a}</code></li>
        {/each}
      </ul>
    </section>
  {/if}

  <div class="grid">
    {#each fixtures as f}
      <section class="card">
        <div class="card-header">
          <span class="component-name">{f.title}</span>
          <code class="type-badge">{f.componentType}</code>
        </div>
        <div class="card-body">
          <StepRenderer
            componentType={f.componentType}
            data={f.data}
            tokens={f.tokens}
            stepId={f.stepId}
            onAction={(a) => handleAction(f.title, a)}
          />
        </div>
      </section>
    {/each}
  </div>
</main>

<style>
  main { max-width: 900px; margin: 2rem auto; padding: 1rem; font-family: system-ui, sans-serif; }
  header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
  h1 { margin: 0; }
  a { color: #0070f3; text-decoration: none; font-size: 0.9rem; }
  .subtitle { color: #555; margin-bottom: 1.5rem; }
  .action-log { background: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.75rem; margin-bottom: 1.5rem; }
  .action-log h3 { margin: 0 0 0.5rem; font-size: 0.9rem; }
  .action-log ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.25rem; }
  .action-log code { font-size: 0.8rem; }
  .grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
  @media (min-width: 640px) { .grid { grid-template-columns: 1fr 1fr; } }
  .card { border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; }
  .card-header { display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0.75rem; background: #f8f8f8; border-bottom: 1px solid #e0e0e0; }
  .component-name { font-weight: 600; font-size: 0.85rem; }
  .type-badge { font-size: 0.75rem; background: #e8f0fe; color: #1a56db; padding: 0.15rem 0.5rem; border-radius: 4px; }
  .card-body { padding: 0.75rem; }
</style>
