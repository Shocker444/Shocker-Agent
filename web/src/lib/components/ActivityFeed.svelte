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
    // Dark mode colors
    stt: { bg: "bg-cyan-500/10", label: "text-cyan-400" },
    agent: { bg: "bg-purple-500/10", label: "text-purple-400" },
    tts: { bg: "bg-orange-500/10", label: "text-orange-400" },
    tool: { bg: "bg-blue-500/10", label: "text-blue-400" },
  };
</script>

<div class="h-full flex flex-col relative w-full">
  <!-- Clear button floating in top right -->
  {#if $activities.length > 0}
    <button
      onclick={() => activities.clear()}
      class="absolute top-[-35px] right-4 text-[10px] uppercase tracking-wider text-neutral-600 hover:text-red-400 transition-colors z-20 cursor-pointer"
    >
      Clear Log
    </button>
  {/if}

  <div class="flex-grow overflow-y-auto p-4 space-y-4 scroll-smooth w-full">
    {#if $activities.length === 0}
      <div
        class="h-full flex flex-col items-center justify-center text-neutral-700 gap-2 opacity-50"
      >
        <div class="text-4xl">⚡</div>
        <div class="text-xs font-mono uppercase tracking-widest">
          Waiting for input event...
        </div>
      </div>
    {:else}
      {#each $activities as item (item.id)}
        <div class="flex items-start gap-4 animate-slideIn group w-full">
          <!-- Timestamp Column -->
          <div class="hidden sm:block w-12 pt-1 text-right flex-shrink-0">
            <span
              class="font-mono text-[10px] text-neutral-600 group-hover:text-neutral-400 transition-colors"
            >
              {formatTime(item.timestamp)}
            </span>
          </div>

          <!-- Icon -->
          <div
            class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0 border border-white/5 shadow-inner {colorMap[
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
              <!-- Mobile timestamp -->
              <span class="sm:hidden font-mono text-[9px] text-neutral-600"
                >{formatTime(item.timestamp)}</span
              >
            </div>

            <div
              class="text-sm text-neutral-300 leading-relaxed break-words font-light"
            >
              {item.text}
            </div>

            {#if item.args}
              <div
                class="mt-2 rounded-lg bg-black/40 border border-neutral-800 overflow-hidden max-w-full"
              >
                <div
                  class="bg-neutral-900/50 px-3 py-1 border-b border-neutral-800 text-[9px] font-mono text-neutral-500 uppercase"
                >
                  Arguments
                </div>
                <pre
                  class="p-3 font-mono text-[10px] text-green-400/90 overflow-x-auto custom-scrollbar whitespace-pre-wrap break-all">{JSON.stringify(
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
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-slideIn {
    animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Custom nicer scrollbar for code blocks */
  .custom-scrollbar::-webkit-scrollbar {
    height: 4px;
    background: transparent;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 2px;
  }
</style>
