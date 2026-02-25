<script lang="ts">
  import { currentTurn } from "../stores";
  import { formatDuration } from "../utils";

  interface StageState {
    active: boolean;
    complete: boolean;
    time: string;
  }

  let stt = $derived<StageState>({
    active: !!$currentTurn.sttStartTs && !$currentTurn.sttEndTs,
    complete: !!$currentTurn.sttEndTs,
    time:
      $currentTurn.sttEndTs && $currentTurn.sttStartTs
        ? formatDuration($currentTurn.sttEndTs - $currentTurn.sttStartTs)
        : $currentTurn.sttStartTs
          ? "..."
          : "—",
  });

  let agent = $derived<StageState>({
    active: !!$currentTurn.agentStartTs && !$currentTurn.agentEndTs,
    complete: !!$currentTurn.agentEndTs,
    time:
      $currentTurn.agentEndTs && $currentTurn.agentStartTs
        ? formatDuration($currentTurn.agentEndTs - $currentTurn.agentStartTs)
        : $currentTurn.agentStartTs
          ? "..."
          : "—",
  });

  let tts = $derived<StageState>({
    active: !!$currentTurn.ttsStartTs && !$currentTurn.ttsEndTs,
    complete: !!$currentTurn.ttsEndTs,
    time:
      $currentTurn.ttsEndTs && $currentTurn.ttsStartTs
        ? formatDuration($currentTurn.ttsEndTs - $currentTurn.ttsStartTs)
        : $currentTurn.ttsStartTs
          ? "..."
          : "—",
  });

  function stageClasses(
    state: StageState,
    color: "cyan" | "purple" | "orange",
  ): string {
    const ringMap = {
      cyan: "ring-cyan-500",
      purple: "ring-purple-500",
      orange: "ring-orange-500",
    };

    let classes = `w-12 h-12 rounded-xl flex items-center justify-center text-xl
                   bg-zinc-800 border border-zinc-700 transition-all duration-300`;

    if (state.active) {
      classes += ` ring-2 ${ringMap[color]} scale-105`;
    } else if (state.complete) {
      classes += " opacity-50";
    }

    return classes;
  }
</script>

<div class="flex items-center justify-center gap-4 py-3">
  <!-- STT -->
  <div class="flex flex-col items-center gap-2">
    <div class={stageClasses(stt, "cyan")}>🎤</div>
    <div class="text-[10px] font-medium uppercase tracking-wider text-zinc-500">
      STT
    </div>
    <div class="font-mono text-[10px] text-zinc-600">{stt.time}</div>
  </div>

  <div class="text-zinc-700 text-base">→</div>

  <!-- Agent -->
  <div class="flex flex-col items-center gap-2">
    <div class={stageClasses(agent, "purple")}>🤖</div>
    <div class="text-[10px] font-medium uppercase tracking-wider text-zinc-500">
      Agent
    </div>
    <div class="font-mono text-[10px] text-zinc-600">{agent.time}</div>
  </div>

  <div class="text-zinc-700 text-base">→</div>

  <!-- TTS -->
  <div class="flex flex-col items-center gap-2">
    <div class={stageClasses(tts, "orange")}>🔊</div>
    <div class="text-[10px] font-medium uppercase tracking-wider text-zinc-500">
      TTS
    </div>
    <div class="font-mono text-[10px] text-zinc-600">{tts.time}</div>
  </div>
</div>
