<script lang="ts">
  import { session, formattedTime } from "../stores";

  let changelogstate = $state(false);
  console.log(formattedTime);

  function showchangelog() {
    changelogstate = true;
  }

  let dialogref = $state<HTMLDialogElement>();

  $effect(() => {
    if (changelogstate) {
      dialogref?.showModal();
    } else {
      dialogref?.close();
    }
  })


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
          AGENT.v2
        </span>
      </h1>
      <p class="text-[10px] text-zinc-600 font-mono tracking-widest uppercase">
        AI Candidate Interviewer Interface
      </p>
    </div>
  </div>

  <div>
    <button
      onclick={showchangelog}
      class="text-[10px] cursor-pointer hover:text-zinc-100 font-mono font-normal text-zinc-400 bg-zinc-800 px-1.5 py-0.5 rounded border border-zinc-700"
    >
      See what's new
    </button>
  </div>

  <!-- Status -->
  <div class="flex items-center gap-4 md:gap-6">
    <div class="hidden sm:flex flex-col items-end">
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


<dialog 
  bind:this={dialogref}
  onclose={() => changelogstate = false}
  class="w-full max-w-3xl p-0 bg-transparent m-auto backdrop:bg-black/80"
>
  <div class="bg-zinc-950 border border-zinc-800 rounded-xl overflow-hidden shadow-2xl text-left">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/50">
      <div>
        <h3 class="text-xl font-bold text-white flex items-center gap-2">
          Changelog
        </h3>
        <p class="text-sm text-zinc-400 mt-1">Here's what's new in Shocker:</p>
      </div>
      <form method="dialog">
        <button aria-label="Close changelog" class="text-zinc-500 hover:text-white transition-colors cursor-pointer rounded-md hover:bg-zinc-800 p-1">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </form>
    </div>

    <!-- Body -->
    <div class="px-8 py-6 max-h-[70vh] overflow-y-auto space-y-8">
      
      <!-- Features -->
      <section>
        <h4 class="text-white font-bold text-lg mb-4 flex items-center gap-2">
          Features (New Additions)
        </h4>
        <ul class="space-y-3 text-sm text-zinc-400 list-disc list-outside ml-6 marker:text-cyan-500">
          <li><strong class="text-zinc-300">Resume Integration:</strong> Added resume upload functionality and integrated resume-based personalization into the interview prompt.</li>
          <li><strong class="text-zinc-300">Voice Session Management:</strong> Implemented WebSocket-based voice sessions handling audio capture, playback, and server events.</li>
          <li><strong class="text-zinc-300">Interactive Sessions:</strong> Added interactive voice sessions with dynamic job description inputs.</li>
          <li><strong class="text-zinc-300">Multi-Phase Workflow:</strong> Implemented a multi-phase agent workflow (including technical and closing phases) with time-based transitions.</li>
          <li><strong class="text-zinc-300">Svelte Web UI:</strong> Implemented a new Svelte web UI and integrated time management parameters into the agent's pipeline.</li>
          <li><strong class="text-zinc-300">Feedback & Controls:</strong> Added a new feedback section and a session termination pop-up.</li>
        </ul>
      </section>

      <!-- Improvements -->
      <section>
        <h4 class="text-white font-bold text-lg mb-4 flex items-center gap-2">
          Improvements (Refinements & Enhancements)
        </h4>
        <ul class="space-y-3 text-sm text-zinc-400 list-disc list-outside ml-6 marker:text-amber-500">
          <li><strong class="text-zinc-300">Conversational Flow:</strong> Improved overall conversation output and turn-taking (using flux), and optimized endpointing values for more natural pauses.</li>
          <li><strong class="text-zinc-300">Agent Logic & Prompting:</strong> Refined technical interview prompts, updated assessment criteria to handle unsatisfactory answers, and restructured agent state machine transitions.</li>
          <li><strong class="text-zinc-300">Speech-to-Text:</strong> Updated and improved STT (Speech-to-Text) handling.</li>
          <li><strong class="text-zinc-300">UI/UX:</strong> Updated the user interface and improved effective transitions between states.</li>
          <li><strong class="text-zinc-300">Privacy/Cleanup:</strong> Removed pipeline telemetry for users.</li>
        </ul>
      </section>

      <!-- Fixes -->
      <section>
        <h4 class="text-white font-bold text-lg mb-4 flex items-center gap-2">
          Fixes (Bug Resolutions)
        </h4>
        <ul class="space-y-3 text-sm text-zinc-400 list-disc list-outside ml-6 marker:text-emerald-500">
          <li><strong class="text-zinc-300">Time Management:</strong> Synchronized frontend and backend session timers to fix time management issues.</li>
          <li><strong class="text-zinc-300">Prompting:</strong> Fixed missing/incorrect prompt tags.</li>
          <li><strong class="text-zinc-300">Responsiveness:</strong> Improved overall system and UI responsiveness.</li>
          <li><strong class="text-zinc-300">General Maintenance:</strong> Removed stray comments and resolved Issue #6.</li>
        </ul>
      </section>

    </div>
  </div>
</dialog>
