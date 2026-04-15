<script lang="ts">
  import { session, jobDescStore, resumeStore } from "../stores";

  let errorMsg = $state("");
  let durationValue = $state(10);
  let durationError = $state("");
  let showConfirmModel = $state(false);

  function handleJdChange(e: Event) {
    const target = e.target as HTMLTextAreaElement;
    jobDescStore.setJobDesc(target.value);
    if (target.value.trim()) {
      errorMsg = "";
    }
  }

  async function handleFileChange(e: Event) {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        const base64String = (reader.result as string).split(",")[1];
        resumeStore.setResume(base64String, file.name);
      };
      reader.readAsDataURL(file);
    } else {
      resumeStore.reset();
    }
  }

  interface Props {
    onStart: (duration: number) => void;
    onStop: () => void;
  }

  let { onStart, onStop }: Props = $props();

  function handleInitialize() {
    if (!$jobDescStore.description.trim()) {
      errorMsg = "Please insert a job description before starting.";
      return;
    }

    if (durationValue < 5) {
      durationError = "Duration cannot be less than 5 minutes.";
      return;
    }
    errorMsg = "";
    onStart(durationValue);
  }

  function handleConfirm() {
    if ($session.remainingTime && $session.remainingTime > 0) {
      showConfirmModel = true;
    } else {
      onStop();
    }
  }

  // Reference to the native HTML element
  let dialogRef = $state<HTMLDialogElement>();

  // This effect watches the state and tells the browser to
  // move the element into the "Top Layer" via showModal()
  $effect(() => {
    if (showConfirmModel) {
      dialogRef?.showModal();
    } else {
      dialogRef?.close();
    }
  });

  const statusConfig = {
    ready: {
      dot: "bg-cyan-500",
      text: "System Ready",
      textColor: "text-cyan-400",
    },
    connecting: {
      dot: "bg-amber-400 animate-pulse",
      text: "Connecting...",
      textColor: "text-amber-400",
    },
    listening: {
      dot: "bg-red-500 animate-pulse",
      text: "Microphone Active",
      textColor: "text-red-400",
    },
    error: {
      dot: "bg-red-600",
      text: "System Error",
      textColor: "text-red-400",
    },
    disconnected: {
      dot: "bg-zinc-600",
      text: "Disconnected",
      textColor: "text-zinc-500",
    },
  };

  let config = $derived(
    statusConfig[$session.status] || statusConfig.disconnected,
  );
</script>

<div class="flex flex-col gap-3">
  <!-- Duration Input -->
  <div class="flex flex-col gap-2">
    <label
      for="duration-input"
      class="text-[10px] font-mono text-white-600 uppercase"
      >Session Duration (Minutes)</label
    >
    <input
      type="number"
      id="duration-input"
      class="w-full p-2 bg-zinc-900 border border-zinc-800 rounded-lg text-xs text-zinc-300 focus:outline-none focus:border-cyan-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-mono"
      placeholder="e.g., 10"
      bind:value={durationValue}
      min="5"
      max="60"
      disabled={$session.connected}
    />
    {#if durationValue}
      <span class="text-[10px] text-red-400 font-mono">{durationError}</span>
    {/if}
  </div>

  <!-- Job Description Input -->
  <div class="flex flex-col gap-2">
    <label for="jd-input" class="text-[10px] font-mono text-white-600 uppercase"
      >Target Job Description</label
    >
    <textarea
      id="jd-input"
      class="w-full h-24 p-2 bg-zinc-900 border {errorMsg
        ? 'border-red-500'
        : 'border-zinc-800'} rounded-lg text-xs text-zinc-300 resize-none focus:outline-none focus:border-cyan-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-zinc-600 font-mono"
      placeholder="Paste the job description here..."
      value={$jobDescStore.description}
      oninput={handleJdChange}
      disabled={$session.connected}
    ></textarea>
    {#if errorMsg}
      <span class="text-[10px] text-red-400 font-mono">{errorMsg}</span>
    {/if}
  </div>

  <!-- Resume File Input -->
  <div class="flex flex-col gap-2">
    <label
      for="resume-input"
      class="text-[10px] font-mono text-white-600 uppercase"
      >Upload Resume for more personalized responses (Optional/PDF)</label
    >
    <div class="flex items-center gap-2">
      <input
        type="file"
        id="resume-input"
        accept="application/pdf"
        onchange={handleFileChange}
        disabled={$session.connected}
        class="w-full text-xs text-zinc-500 font-mono file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-zinc-800 file:text-cyan-400 hover:file:bg-zinc-700 disabled:opacity-50 disabled:cursor-not-allowed"
      />
    </div>
  </div>

  <!-- Buttons -->
  <div class="flex gap-3">
    <button
      onclick={handleInitialize}
      disabled={$session.connected}
      class="flex-1 py-2.5 px-4 text-xs font-bold uppercase tracking-wider bg-cyan-500 text-black rounded-lg
             flex items-center justify-center gap-2 transition-all duration-150
             hover:bg-cyan-400 hover:-translate-y-px
             disabled:opacity-20 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:bg-zinc-700 disabled:text-zinc-500"
    >
      <svg
        class="w-3.5 h-3.5"
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
      onclick={handleConfirm}
      disabled={!$session.connected}
      class="flex-1 py-2.5 px-4 text-xs font-bold uppercase tracking-wider bg-zinc-800 text-zinc-400 rounded-lg
             border border-zinc-700 transition-all duration-150
             hover:bg-red-950 hover:text-red-400 hover:border-red-900
             disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-zinc-800 disabled:hover:text-zinc-400 disabled:hover:border-zinc-700"
    >
      Terminate
    </button>
  </div>

  <!-- Status Row -->
  <div
    class="flex items-center justify-between py-2 px-3 bg-zinc-950 rounded-lg border border-zinc-800"
  >
    <span class="text-[10px] font-mono text-zinc-600 uppercase">Status</span>
    <div class="flex items-center gap-2">
      <span class="w-1.5 h-1.5 rounded-full {config.dot}"></span>
      <span class="text-xs font-mono {config.textColor}">{config.text}</span>
    </div>
  </div>

  {#if $session.connected}
    <div
      class="py-2 px-3 bg-zinc-800 border border-zinc-700 rounded-lg text-[10px] text-zinc-400 text-center font-mono"
    >
      Listening for audio input
    </div>
  {/if}
</div>

<dialog
  bind:this={dialogRef}
  onclose={() => (showConfirmModel = false)}
  class="modal-box"
>
  <div class="modal-content">
    <h3>End Session Early?</h3>
    <p>
      You still have time remaining. Are you sure you want to end the session?
    </p>

    <div class="modal-actions">
      <button
        type="button"
        class="btn-secondary"
        onclick={() => (showConfirmModel = false)}
      >
        Keep Going
      </button>

      <button
        type="button"
        class="btn-primary"
        onclick={() => {
          showConfirmModel = false;
          onStop();
        }}
      >
        Yes, End Session
      </button>
    </div>
  </div>
</dialog>
