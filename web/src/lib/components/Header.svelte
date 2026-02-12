<script lang="ts">
  import { session, formattedTime } from "../stores";
</script>

<header class="flex items-center justify-between">
  <!-- Brand -->
  <div class="flex items-center gap-4">
    <div
      class="relative w-10 h-10 flex items-center justify-center bg-cyan-500/10 rounded-xl border border-cyan-500/20 shadow-[0_0_15px_rgba(6,182,212,0.1)]"
    >
      <span class="text-xl">⚡</span>
      <div
        class="absolute inset-0 border border-cyan-400/30 rounded-xl blur-[1px]"
      ></div>
    </div>
    <div class="flex flex-col">
      <h1
        class="text-2xl font-bold tracking-tight text-white flex items-center gap-2"
      >
        Shocker
        <span
          class="text-[10px] font-mono font-normal text-cyan-500 bg-cyan-500/10 px-1.5 py-0.5 rounded border border-cyan-500/20"
          >AGENT.v1</span
        >
      </h1>
      <p
        class="text-[10px] text-neutral-500 font-mono tracking-widest uppercase"
      >
        AI Candidate Interviewer Interface
      </p>
    </div>
  </div>

  <!-- Status (Visible on Desktop) -->
  <div class="hidden md:flex items-center gap-6">
    <div class="flex flex-col items-end">
      <span class="font-mono text-xs text-neutral-400 font-bold"
        >{$formattedTime}</span
      >
      <span
        class="font-mono text-[10px] text-neutral-600 uppercase tracking-wider"
      >
        {$session.connected ? "Uplink Established" : "Offline"}
      </span>
    </div>
  </div>
</header>
