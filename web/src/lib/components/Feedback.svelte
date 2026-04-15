<script lang="ts">
  let name = $state("");
  let feedback = $state("");
  let status = $state<"idle" | "loading" | "success" | "error">("idle");

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  async function handleSubmit() {
    if (!feedback.trim()) return;
    status = "loading";
    try {
      const res = await fetch(`${API_URL}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.trim() || "Anonymous",
          feedback: feedback.trim(),
        }),
      });
      if (!res.ok) throw new Error();
      status = "success";
      name = "";
      feedback = "";
      setTimeout(() => {
        status = "idle";
      }, 3000);
    } catch {
      status = "error";
    }
  }
</script>

<div class="flex flex-col gap-3">
  <div class="flex flex-col gap-1.5">
    <label
      for="feedback-name"
      class="text-[10px] font-mono font-bold text-zinc-500 uppercase tracking-widest"
      >Name (Optional)</label
    >
    <input
      id="feedback-name"
      type="text"
      bind:value={name}
      placeholder="Your name"
      class="w-full p-2 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-300 focus:outline-none focus:border-cyan-500 transition-colors placeholder:text-zinc-700 font-mono"
    />
  </div>

  <div class="flex flex-col gap-1.5">
    <label
      for="feedback-text"
      class="text-[10px] font-mono font-bold text-zinc-500 uppercase tracking-widest"
      >Feedback</label
    >
    <textarea
      id="feedback-text"
      bind:value={feedback}
      placeholder="How was the interview? Any thoughts or issues..."
      rows="4"
      class="w-full p-2 bg-zinc-950 border border-zinc-800 rounded-lg text-xs text-zinc-300 resize-none focus:outline-none focus:border-cyan-500 transition-colors placeholder:text-zinc-700 font-mono"
    ></textarea>
  </div>

  {#if status === "success"}
    <p class="text-[10px] font-mono text-cyan-400">
      Feedback received. Thank you!
    </p>
  {:else if status === "error"}
    <p class="text-[10px] font-mono text-red-400">
      Failed to submit. Please try again.
    </p>
  {/if}

  <button
    type="button"
    onclick={handleSubmit}
    disabled={status === "loading" || !feedback.trim()}
    class="w-full py-2.5 px-4 text-xs font-bold uppercase tracking-wider bg-cyan-500 text-black rounded-lg
           transition-all duration-150 hover:bg-cyan-400 hover:-translate-y-px
           disabled:opacity-20 disabled:cursor-not-allowed flex items-center justify-center gap-2"
  >
    {#if status === "loading"}
      <div
        class="w-3 h-3 border-2 border-black border-t-transparent rounded-full animate-spin"
      ></div>
      Sending...
    {:else}
      Submit Feedback
    {/if}
  </button>
</div>
