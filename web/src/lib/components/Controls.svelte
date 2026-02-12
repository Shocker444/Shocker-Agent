<script lang="ts">
  import { session } from "../stores";

  interface Props {
    onStart: () => void;
    onStop: () => void;
  }

  let { onStart, onStop }: Props = $props();

  /* 
       Updated status config for dark mode.
       Using glows and brighter colors against dark background.
    */
  const statusConfig = {
    ready: {
      dot: "bg-cyan-500 shadow-[0_0_8px_theme(colors.cyan.500)]",
      text: "System Ready",
      textColor: "text-cyan-400",
    },
    connecting: {
      dot: "bg-yellow-400 animate-pulse",
      text: "Establishing Handshake...",
      textColor: "text-yellow-400",
    },
    listening: {
      dot: "bg-red-500 shadow-[0_0_12px_theme(colors.red.500)] animate-pulse",
      text: "Microphone Active",
      textColor: "text-red-400",
    },
    error: {
      dot: "bg-red-600",
      text: "System Failure",
      textColor: "text-red-500",
    },
    disconnected: {
      dot: "bg-neutral-600",
      text: "Disconnected",
      textColor: "text-neutral-500",
    },
  };

  let config = $derived(
    statusConfig[$session.status] || statusConfig.disconnected,
  );
</script>

<div class="flex flex-col gap-4">
  <div class="flex gap-3">
    <button
      onclick={onStart}
      disabled={$session.connected}
      class="flex-1 py-3 px-4 text-xs font-bold uppercase tracking-wider bg-cyan-500 text-black rounded-lg
             shadow-[0_0_15px_rgba(6,182,212,0.3)]
             flex items-center justify-center gap-2 transition-all duration-200
             hover:bg-cyan-400 hover:shadow-[0_0_20px_rgba(6,182,212,0.5)] hover:-translate-y-0.5
             disabled:opacity-20 disabled:cursor-not-allowed disabled:shadow-none disabled:hover:translate-y-0 disabled:bg-neutral-800 disabled:text-neutral-500"
    >
      <svg
        class="w-4 h-4"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
      >
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
      </svg>
      Initialize
    </button>

    <button
      onclick={onStop}
      disabled={!$session.connected}
      class="flex-1 py-3 px-4 text-xs font-bold uppercase tracking-wider bg-neutral-800 text-neutral-400 rounded-lg
             border border-neutral-700 transition-all duration-200
             hover:bg-red-500/20 hover:text-red-400 hover:border-red-500/50
             disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-neutral-800 disabled:hover:text-neutral-400 disabled:hover:border-neutral-700"
    >
      Terminate
    </button>
  </div>

  <!-- Status Indicator -->
  <div
    class="flex items-center justify-between py-2 px-3 bg-black/20 rounded-lg border border-neutral-800/50"
  >
    <span class="text-[10px] font-mono text-neutral-600 uppercase">Status</span>
    <div class="flex items-center gap-2">
      <span
        class="w-2 h-2 rounded-full transition-all duration-300 {config.dot}"
      ></span>
      <span class="text-xs font-mono font-bold {config.textColor}"
        >{config.text}</span
      >
    </div>
  </div>

  {#if $session.connected}
    <div
      class="py-2 px-3 bg-cyan-500/5 border border-cyan-500/10 rounded-lg text-[10px] text-cyan-400/80 text-center font-mono animate-pulse"
    >
      /// LISTENING FOR AUDIO INPUT ///
    </div>
  {/if}
</div>
