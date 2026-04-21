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
          AGENT.v1.1
        </span>
      </h1>
      <p class="text-[10px] text-zinc-600 font-mono tracking-widest uppercase">
        AI Candidate Interviewer Interface
      </p>
    </div>
  </div>

  <!-- Status & Changelog -->
  <div class="flex items-center gap-3 md:gap-6">
    <button
      onclick={showchangelog}
      class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-zinc-800 bg-zinc-900 hover:bg-zinc-800 hover:text-white transition-colors text-[10px] font-mono text-zinc-400 cursor-pointer"
      aria-label="See what's new"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-cyan-500">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="16" y1="13" x2="8" y2="13"></line>
        <line x1="16" y1="17" x2="8" y2="17"></line>
        <polyline points="10 9 9 9 8 9"></polyline>
      </svg>
      <span class="hidden sm:inline">What's new</span>
    </button>

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
          <li><strong class="text-zinc-300">Interactive Sessions:</strong> New interactive voice sessions with dynamic job description inputs.</li>
          <li><strong class="text-zinc-300">Svelte Web UI:</strong> New Svelte web UI and integrated time management parameters into the agent's pipeline.</li>
          <li><strong class="text-zinc-300">Feedback & Controls:</strong> New feedback section for honest user feedback and a session termination pop-up.</li>
        </ul>
      </section>

      <!-- Improvements -->
      <section>
        <h4 class="text-white font-bold text-lg mb-4 flex items-center gap-2">
          Improvements (Refinements & Enhancements)
        </h4>
        <ul class="space-y-3 text-sm text-zinc-400 list-disc list-outside ml-6 marker:text-amber-500">
          <li><strong class="text-zinc-300">Conversational Flow:</strong> Overall conversation output and turn-taking (using flux) much more optimized and suited for more natural pauses.</li>
          <li><strong class="text-zinc-300">Agent Logic & Prompting:</strong> Improved agent response and context awareness.</li>
          <li><strong class="text-zinc-300">Speech-to-Text:</strong> Updated and improved STT (Speech-to-Text) handling.</li>
          <li><strong class="text-zinc-300">UI/UX:</strong> Updated the user interface and improved effective transitions between states.</li>
        </ul>
      </section>

      <!-- Fixes -->
      <section>
        <h4 class="text-white font-bold text-lg mb-4 flex items-center gap-2">
          Fixes (Bug Resolutions)
        </h4>
        <ul class="space-y-3 text-sm text-zinc-400 list-disc list-outside ml-6 marker:text-emerald-500">
          <li><strong class="text-zinc-300">Time Management:</strong> Synchronized frontend and backend session timers to fix time management issues.</li>
          <li><strong class="text-zinc-300">Prompt injection:</strong> Fixed user prompt injection. Agent has full control of the conversation.</li>
          <li><strong class="text-zinc-300">Responsiveness:</strong> Improved overall system and UI responsiveness.</li>
        </ul>
      </section>

    </div>
  </div>
</dialog>
