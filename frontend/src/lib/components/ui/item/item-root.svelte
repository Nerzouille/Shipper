<script lang="ts">
  let { children, class: className = '' } = $props<{ children?: any; class?: string }>();
</script>
<div class="flex items-start gap-3 {className}">{@render children?.()}</div>
