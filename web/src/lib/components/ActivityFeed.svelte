<script lang="ts">
  import { activities } from "../stores";
  import { formatTime } from "../utils";

  const iconMap: Record<string, string> = {
    stt: "🎤",
    agent: "🤖",
    tts: "🔊",
    tool: "🔧",
  };

  const colorMap: Record<string, { bg: string; label: string }> = {
    stt: { bg: "bg-cyan-950", label: "text-cyan-400" },
    agent: { bg: "bg-purple-950", label: "text-purple-400" },
    tts: { bg: "bg-orange-950", label: "text-orange-400" },
    tool: { bg: "bg-blue-950", label: "text-blue-400" },
  };
</script>

<div class="h-full flex flex-col relative w-full">
  <!-- Clear button -->
  {#if $activities.length > 0}
    <button
      onclick={() => activities.clear()}
      class="absolute top-[-35px] right-4 text-[10px] uppercase tracking-wider text-zinc-600 hover:text-red-400 transition-colors z-20 cursor-pointer"
    >
      Clear
    </button>
  {/if}

  <div class="flex-grow overflow-y-auto p-5 space-y-5 w-full">
    {#if $activities.length === 0}
      <div
        class="h-full flex flex-col items-center justify-center text-zinc-700 gap-3 py-20"
      >
        <div class="text-3xl">⚡</div>
        <div class="text-[10px] font-mono uppercase tracking-widest">
          Awaiting events...
        </div>
      </div>
    {:else}
      {#each $activities as item (item.id)}
        <div class="flex items-start gap-4 animate-slideIn w-full">
          <!-- Timestamp -->
          <div class="hidden sm:block w-12 pt-0.5 text-right flex-shrink-0">
            <span class="font-mono text-[10px] text-zinc-600"
              >{formatTime(item.timestamp)}</span
            >
          </div>

          <!-- Icon -->
          <div
            class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0 {colorMap[
              item.type
            ]?.bg}"
          >
            {iconMap[item.type] || "📋"}
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0 pt-0.5">
            <div class="flex items-center gap-2 mb-1">
              <span
                class="text-[10px] font-bold uppercase tracking-wider {colorMap[
                  item.type
                ]?.label}"
              >
                {item.label}
              </span>
              <span class="sm:hidden font-mono text-[9px] text-zinc-600"
                >{formatTime(item.timestamp)}</span
              >
            </div>

            <div
              class="text-sm text-zinc-300 leading-relaxed break-words font-light"
            >
              {item.text}
            </div>

            {#if item.args}
              <div
                class="mt-2 rounded-lg bg-zinc-950 border border-zinc-800 overflow-hidden max-w-full"
              >
                <div
                  class="px-3 py-1 border-b border-zinc-800 text-[9px] font-mono text-zinc-600 uppercase"
                >
                  Arguments
                </div>
                <pre
                  class="p-3 font-mono text-[10px] text-emerald-400 overflow-x-auto custom-scrollbar whitespace-pre-wrap break-all">{JSON.stringify(
                    item.args,
                    null,
                    2,
                  )}</pre>
              </div>
            {/if}
          </div>
        </div>
      {/each}
    {/if}
  </div>
</div>

<style>
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-slideIn {
    animation: slideIn 0.25s ease-out;
  }

  .custom-scrollbar::-webkit-scrollbar {
    height: 4px;
    background: transparent;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #3f3f46;
    border-radius: 2px;
  }
</style>
