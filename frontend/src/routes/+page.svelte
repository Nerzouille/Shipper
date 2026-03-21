<svelte:options runes={true} />
<main>
  <h1>Market Intelligence AI</h1>
  <p class="subtitle">Hackathon MVP — two modes available:</p>

  <nav>
    <a href="/workflow" class="card">
      <h2>Guided Workflow</h2>
      <p>9-step guided analysis with keyword refinement and product validation.</p>
      <span class="badge active">Active</span>
    </a>
    <a href="/" class="card disabled">
      <h2>Live Dashboard</h2>
      <p>Real-time streaming market analysis (SSE dashboard — coming soon).</p>
      <span class="badge">Coming soon</span>
    </a>
    <a href="/components-test" class="card">
      <h2>Component Test Page</h2>
      <p>Visual test of all workflow step components with fake data.</p>
      <span class="badge dev">Dev</span>
    </a>
  </nav>
</main>

<style>
  main { max-width: 600px; margin: 3rem auto; padding: 1rem; font-family: system-ui, sans-serif; }
  h1 { margin-bottom: 0.25rem; }
  .subtitle { color: #666; margin-bottom: 2rem; }
  nav { display: flex; flex-direction: column; gap: 1rem; }
  .card { display: block; padding: 1rem 1.25rem; border: 1px solid #e0e0e0; border-radius: 8px; text-decoration: none; color: inherit; transition: border-color 0.15s; }
  .card:hover { border-color: #0070f3; }
  .card.disabled { opacity: 0.5; pointer-events: none; }
  .card h2 { margin: 0 0 0.25rem; font-size: 1.1rem; }
  .card p { margin: 0 0 0.5rem; font-size: 0.9rem; color: #555; }
  .badge { font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 999px; background: #e0e0e0; color: #555; }
  .badge.active { background: #d4edda; color: #155724; }
  .badge.dev { background: #fff3cd; color: #856404; }
</style>
