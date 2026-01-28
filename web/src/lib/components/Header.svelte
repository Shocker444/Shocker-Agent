<script lang="ts">
  import { session, formattedTime } from '../stores';
</script>

<header class="flex items-center justify-between mb-7">
  <div class="flex items-center gap-3">
    <span class="text-3xl">⚡</span>
    <div class="flex flex-col">
      <h1 class="text-2xl font-semibold tracking-tight text-gray-900">Shocker</h1>
      <p class="text-xs text-gray-500 font-medium">AI Candidate Interviewer</p>
    </div>
  </div>
  <div class="flex items-center gap-3">
    <div class="flex flex-col items-end">
      <span class="font-mono text-sm text-gray-400">{$formattedTime}</span>
      <span class="font-mono text-xs text-gray-500">
        {$session.connected ? 'Interview Active' : 'Waiting to Connect'}
      </span>
    </div>
    <span
      class="w-3 h-3 rounded-full transition-all duration-300 {$session.connected
        ? 'bg-green-500 shadow-[0_0_8px_theme(colors.green.500)]'
        : 'bg-gray-400'}"
    ></span>
  </div>
</header>

<style>
  header {
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    padding-bottom: 1rem;
  }
</style>