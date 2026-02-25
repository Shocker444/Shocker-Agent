<script lang="ts">
  import { currentTurn } from "../stores";
  import Pipeline from "./Pipeline.svelte";
  import LatencyWaterfall from "./LatencyWaterfall.svelte";
</script>

<div
  class="text-zinc-200 transition-opacity duration-300 {$currentTurn.active
    ? ''
    : 'opacity-50'}"
>
  <div class="flex items-center justify-end mb-4">
    <span
      class="font-mono text-[9px] uppercase tracking-widest py-1 px-2.5 rounded-full border
             {$currentTurn.active
        ? 'text-cyan-400 bg-cyan-950/50 border-cyan-800'
        : 'text-zinc-600 bg-zinc-950 border-zinc-800'}"
    >
      {$currentTurn.active ? "● Processing" : "○ Idle"}
    </span>
  </div>

  <Pipeline />
  <LatencyWaterfall />
</div>
