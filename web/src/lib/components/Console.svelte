<script lang="ts">
  import { logs } from "../stores";
  import { formatTime } from "../utils";
</script>

<!-- Note: Container styling is now handled by the parent in App.svelte mostly, but we ensure internal styles are dark -->
<div class="h-full bg-transparent overflow-hidden flex flex-col">
  <div
    class="flex-grow overflow-y-auto p-4 font-mono text-[10px] leading-relaxed space-y-1"
  >
    {#if $logs.length === 0}
      <div class="text-neutral-700 italic">_awaiting_system_logs...</div>
    {:else}
      {#each $logs as entry (entry.id)}
        <div
          class="flex gap-3 text-neutral-400 border-l-2 border-transparent hover:border-neutral-700 hover:bg-white/5 pl-2 -ml-2 transition-colors"
        >
          <span class="text-neutral-600 flex-shrink-0 w-14"
            >{formatTime(entry.timestamp)}</span
          >
          <span class="break-all">{entry.message}</span>
        </div>
      {/each}
    {/if}
  </div>
</div>
