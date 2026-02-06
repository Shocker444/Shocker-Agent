<script lang="ts">
  import { currentTurn, waterfallData, computedStats, latencyStats } from '../stores';
  import { formatDuration } from '../utils';

  // Use current turn if active, otherwise preserved waterfall data
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
    isActiveNow: boolean
  ): BarStyle {
    if (!startTs) return { left: '0%', width: '0%', opacity: 0 };

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

  function getDuration(startTs: number | null, endTs: number | null, isActiveNow: boolean): string {
    if (!startTs) return '—';
    if (!endTs && isActiveNow) return formatDuration(Date.now() - startTs);
    if (!endTs) return '—';
    return formatDuration(endTs - startTs);
  }

  let bars = $derived.by(() => {
    if (!data?.turnStartTs) return null;

    const baseTime = data.turnStartTs;
    const now = Date.now();
    const isActive = $currentTurn.active;

    // Calculate end time for scaling
    let endTime = baseTime;
    if (data.ttsEndTs) endTime = Math.max(endTime, data.ttsEndTs);
    else if (data.agentEndTs) endTime = Math.max(endTime, data.agentEndTs);
    else if (data.sttEndTs) endTime = Math.max(endTime, data.sttEndTs);
    if (isActive) endTime = Math.max(endTime, now);

    const totalDuration = Math.max(endTime - baseTime, 500);

    return {
      stt: {
        style: getBarStyle(baseTime, totalDuration, data.sttStartTs, data.sttEndTs, isActive && !!data.sttStartTs && !data.sttEndTs),
        duration: getDuration(data.sttStartTs, data.sttEndTs, isActive && !!data.sttStartTs && !data.sttEndTs),
      },
      agent: {
        style: getBarStyle(baseTime, totalDuration, data.agentStartTs, data.agentEndTs, isActive && !!data.agentStartTs && !data.agentEndTs),
        duration: getDuration(data.agentStartTs, data.agentEndTs, isActive && !!data.agentStartTs && !data.agentEndTs),
      },
      tts: {
        style: getBarStyle(baseTime, totalDuration, data.ttsStartTs, data.ttsEndTs, isActive && !!data.ttsStartTs && !data.ttsEndTs),
        duration: getDuration(data.ttsStartTs, data.ttsEndTs, isActive && !!data.ttsStartTs && !data.ttsEndTs),
      },
    };
  });

  let totalLatencyDisplay = $derived.by(() => {
    if (!data) return '—';
    if (data.sttStartTs && data.ttsEndTs) {
      return formatDuration(data.ttsEndTs - data.sttStartTs);
    }
    if ($currentTurn.active && data.sttStartTs) {
      return formatDuration(Date.now() - data.sttStartTs);
    }
    return '—';
  });
</script>

<div class="mt-5 pt-5 border-t border-zinc-800">
  <div class="flex items-center gap-2 mb-4 text-cyan-400">
    <span class="text-xs">⚡</span>
    <span class="text-[11px] font-bold uppercase tracking-wider text-cyan-300 drop-shadow-[0_0_5px_rgba(34,211,238,0.5)]">System Latency</span>
    <span class="ml-auto font-mono text-sm font-bold text-yellow-400 drop-shadow-[0_0_8px_rgba(250,204,21,0.6)]">{totalLatencyDisplay}</span>
  </div>

  <div class="mb-4 space-y-3">
    {#if bars}
      {#each [
        // STT: Neon Yellow (Input Energy)
        { label: 'Input', bar: bars.stt, color: 'bg-yellow-400', shadow: 'shadow-[0_0_10px_rgba(250,204,21,0.6)]' },
        // Agent: Electric Blue (Processing Core)
        { label: 'Core', bar: bars.agent, color: 'bg-cyan-400', shadow: 'shadow-[0_0_10px_rgba(34,211,238,0.6)]' },
        // TTS: Hot Pink/Purple (Output/Voice)
        { label: 'Label', bar: bars.tts, color: 'bg-fuchsia-500', shadow: 'shadow-[0_0_10px_rgba(217,70,239,0.6)]' },
      ] as row}
        <div class="flex items-center group">
          <div class="w-10 flex-shrink-0 text-[10px] font-bold uppercase tracking-wider text-zinc-500 group-hover:text-zinc-300 transition-colors">
            {row.label}
          </div>
          <div class="flex-1 h-3 bg-zinc-900/80 rounded-full relative overflow-hidden ring-1 ring-white/5">
            <div
              class="absolute h-full rounded-full {row.color} {row.shadow} transition-all duration-75 ease-linear min-w-[2px]"
              style="left: {row.bar.style.left}; width: {row.bar.style.width}; opacity: {row.bar.style.opacity}"
            ></div>
          </div>
          <div class="w-14 flex-shrink-0 text-right font-mono text-[10px] text-zinc-400 pl-2">
            {row.bar.duration}
          </div>
        </div>
      {/each}
    {:else}
      <div class="text-center py-4 text-zinc-700 text-xs font-mono">WAITING FOR INPUT...</div>
    {/if}
  </div>

  <div class="grid grid-cols-4 gap-2 pt-3 border-t border-zinc-800">
    {#each [
        { label: 'Turns', value: $latencyStats.turns },
        { label: 'Avg', value: $computedStats.avg ? formatDuration($computedStats.avg) : '—' },
        { label: 'Min', value: $computedStats.min ? formatDuration($computedStats.min) : '—' },
        { label: 'Max', value: $computedStats.max ? formatDuration($computedStats.max) : '—' }
    ] as stat}
    <div class="flex flex-col items-center p-1 rounded bg-zinc-900/50 border border-zinc-800">
      <span class="text-[9px] font-bold uppercase tracking-wider text-zinc-500">{stat.label}</span>
      <span class="font-mono text-xs text-cyan-400/90">{stat.value}</span>
    </div>
    {/each}
  </div>
</div>