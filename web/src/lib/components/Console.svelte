<script lang="ts">
  import { logs } from "../stores";
  import { formatTime } from "../utils";
</script>

<div class="h-full bg-transparent overflow-hidden flex flex-col">
  <div
    class="flex-grow overflow-y-auto p-4 font-mono text-[10px] leading-relaxed space-y-1"
  >
    {#if $logs.length === 0}
      <div class="text-zinc-700 italic">_awaiting_system_logs...</div>
    {:else}
      {#each $logs as entry (entry.id)}
        <div
          class="flex gap-3 text-zinc-500 border-l-2 border-transparent hover:border-zinc-700 hover:bg-zinc-800/50 pl-2 -ml-2 transition-colors rounded-r"
        >
          <span class="text-zinc-700 flex-shrink-0 w-14"
            >{formatTime(entry.timestamp)}</span
          >
          <span class="break-all text-zinc-400">{entry.message}</span>
        </div>
      {/each}
    {/if}
  </div>
</div>
