<script lang="ts">
  import { currentTurn } from "../stores";
  import Pipeline from "./Pipeline.svelte";
  import LatencyWaterfall from "./LatencyWaterfall.svelte";
</script>

<div
  class="text-neutral-200 transition-opacity duration-300
         {$currentTurn.active ? '' : 'opacity-60 grayscale-[0.5]'}"
>
  <div class="flex items-center justify-between mb-4">
    <!-- Header title is handled by parent container now, so we can hide or change this -->
    <div class="hidden"></div>

    <span
      class="ml-auto font-mono text-[9px] uppercase tracking-widest py-1 px-2 rounded border
             {$currentTurn.active
        ? 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20 shadow-[0_0_10px_rgba(6,182,212,0.2)]'
        : 'text-neutral-500 bg-neutral-900 border-neutral-800'}"
    >
      {$currentTurn.active ? "● Processing Active" : "○ System Idle"}
    </span>
  </div>

  <Pipeline />
  <LatencyWaterfall />
</div>
