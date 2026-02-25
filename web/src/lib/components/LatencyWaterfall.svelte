<script lang="ts">
  import {
    currentTurn,
    waterfallData,
    computedStats,
    latencyStats,
  } from "../stores";
  import { formatDuration } from "../utils";

  let data = $derived($currentTurn.active ? $currentTurn : $waterfallData);

  interface BarStyle {
    left: string;
    width: string;
    opacity: number;
  }

  function getBarStyle(
    baseTime: number,
    totalDuration: number,
    startTs: number | null,
    endTs: number | null,
    isActiveNow: boolean,
  ): BarStyle {
    if (!startTs) return { left: "0%", width: "0%", opacity: 0 };

    const now = Date.now();
    const left = ((startTs - baseTime) / totalDuration) * 100;

    let end: number;
    if (endTs) {
      end = endTs;
    } else if (isActiveNow) {
      end = now;
    } else {
      end = startTs;
    }

    const width = Math.max(((end - startTs) / totalDuration) * 100, 0.5);
    return { left: `${left}%`, width: `${width}%`, opacity: 1 };
  }

  function getDuration(
    startTs: number | null,
    endTs: number | null,
    isActiveNow: boolean,
  ): string {
    if (!startTs) return "—";
    if (!endTs && isActiveNow) return formatDuration(Date.now() - startTs);
    if (!endTs) return "—";
    return formatDuration(endTs - startTs);
  }

  let bars = $derived.by(() => {
    if (!data?.turnStartTs) return null;

    const baseTime = data.turnStartTs;
    const now = Date.now();
    const isActive = $currentTurn.active;

    let endTime = baseTime;
    if (data.ttsEndTs) endTime = Math.max(endTime, data.ttsEndTs);
    else if (data.agentEndTs) endTime = Math.max(endTime, data.agentEndTs);
    else if (data.sttEndTs) endTime = Math.max(endTime, data.sttEndTs);
    if (isActive) endTime = Math.max(endTime, now);

    const totalDuration = Math.max(endTime - baseTime, 500);

    return {
      stt: {
        style: getBarStyle(
          baseTime,
          totalDuration,
          data.sttStartTs,
          data.sttEndTs,
          isActive && !!data.sttStartTs && !data.sttEndTs,
        ),
        duration: getDuration(
          data.sttStartTs,
          data.sttEndTs,
          isActive && !!data.sttStartTs && !data.sttEndTs,
        ),
      },
      agent: {
        style: getBarStyle(
          baseTime,
          totalDuration,
          data.agentStartTs,
          data.agentEndTs,
          isActive && !!data.agentStartTs && !data.agentEndTs,
        ),
        duration: getDuration(
          data.agentStartTs,
          data.agentEndTs,
          isActive && !!data.agentStartTs && !data.agentEndTs,
        ),
      },
      tts: {
        style: getBarStyle(
          baseTime,
          totalDuration,
          data.ttsStartTs,
          data.ttsEndTs,
          isActive && !!data.ttsStartTs && !data.ttsEndTs,
        ),
        duration: getDuration(
          data.ttsStartTs,
          data.ttsEndTs,
          isActive && !!data.ttsStartTs && !data.ttsEndTs,
        ),
      },
    };
  });

  let totalLatencyDisplay = $derived.by(() => {
    if (!data) return "—";
    if (data.sttStartTs && data.ttsEndTs) {
      return formatDuration(data.ttsEndTs - data.sttStartTs);
    }
    if ($currentTurn.active && data.sttStartTs) {
      return formatDuration(Date.now() - data.sttStartTs);
    }
    return "—";
  });
</script>

<div class="mt-5 pt-5 border-t border-zinc-800">
  <div class="flex items-center gap-2 mb-4">
    <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-500"
      >Latency</span
    >
    <span class="ml-auto font-mono text-sm font-bold text-zinc-200"
      >{totalLatencyDisplay}</span
    >
  </div>

  <div class="mb-4 space-y-3">
    {#if bars}
      {#each [{ label: "STT", bar: bars.stt, color: "bg-cyan-500" }, { label: "Agent", bar: bars.agent, color: "bg-purple-500" }, { label: "TTS", bar: bars.tts, color: "bg-orange-500" }] as row}
        <div class="flex items-center gap-2 group">
          <div
            class="w-10 flex-shrink-0 text-[10px] font-mono text-zinc-600 group-hover:text-zinc-400 transition-colors"
          >
            {row.label}
          </div>
          <div
            class="flex-1 h-2 bg-zinc-900 rounded-full relative overflow-hidden ring-1 ring-zinc-800"
          >
            <div
              class="absolute h-full rounded-full {row.color} transition-all duration-75 ease-linear min-w-[2px]"
              style="left: {row.bar.style.left}; width: {row.bar.style
                .width}; opacity: {row.bar.style.opacity}"
            ></div>
          </div>
          <div
            class="w-14 flex-shrink-0 text-right font-mono text-[10px] text-zinc-500"
          >
            {row.bar.duration}
          </div>
        </div>
      {/each}
    {:else}
      <div class="text-center py-4 text-zinc-700 text-[10px] font-mono">
        Waiting for input...
      </div>
    {/if}
  </div>

  <div class="grid grid-cols-4 gap-2 pt-3 border-t border-zinc-800">
    {#each [{ label: "Turns", value: $latencyStats.turns }, { label: "Avg", value: $computedStats.avg ? formatDuration($computedStats.avg) : "—" }, { label: "Min", value: $computedStats.min ? formatDuration($computedStats.min) : "—" }, { label: "Max", value: $computedStats.max ? formatDuration($computedStats.max) : "—" }] as stat}
      <div
        class="flex flex-col items-center p-2 rounded-lg bg-zinc-950 border border-zinc-800"
      >
        <span
          class="text-[9px] font-bold uppercase tracking-wider text-zinc-600"
          >{stat.label}</span
        >
        <span class="font-mono text-xs text-zinc-300">{stat.value}</span>
      </div>
    {/each}
  </div>
</div>
