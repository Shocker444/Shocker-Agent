<script lang="ts">
  import { session, formattedTime } from "../stores";
</script>

<header class="flex items-center justify-between">
  <!-- Brand -->
  <div class="flex items-center gap-3">
    <div
      class="w-9 h-9 flex items-center justify-center bg-zinc-800 rounded-lg border border-zinc-700"
    >
      <span class="text-lg">⚡</span>
    </div>
    <div class="flex flex-col">
      <h1
        class="text-xl font-bold tracking-tight text-zinc-100 flex items-center gap-2"
      >
        Shocker
        <span
          class="text-[10px] font-mono font-normal text-zinc-400 bg-zinc-800 px-1.5 py-0.5 rounded border border-zinc-700"
        >
          AGENT.v1
        </span>
      </h1>
      <p class="text-[10px] text-zinc-600 font-mono tracking-widest uppercase">
        AI Candidate Interviewer Interface
      </p>
    </div>
  </div>

  <!-- Status -->
  <div class="hidden md:flex items-center gap-6">
    <div class="flex flex-col items-end">
      <span class="font-mono text-xs text-zinc-400 font-bold"
        >{$formattedTime}</span
      >
      <span
        class="font-mono text-[10px] text-zinc-600 uppercase tracking-wider"
      >
        {$session.connected ? "Connected" : "Offline"}
      </span>
    </div>
    <div
      class="flex items-center gap-2 px-3 py-1.5 rounded-lg border {$session.connected
        ? 'border-emerald-800 bg-emerald-950/50'
        : 'border-zinc-800 bg-zinc-900'}"
    >
      <span
        class="w-1.5 h-1.5 rounded-full {$session.connected
          ? 'bg-emerald-500'
          : 'bg-zinc-600'}"
      ></span>
      <span
        class="text-[10px] font-mono {$session.connected
          ? 'text-emerald-400'
          : 'text-zinc-500'}"
      >
        {$session.connected ? "Live" : "Idle"}
      </span>
    </div>
  </div>
</header>
