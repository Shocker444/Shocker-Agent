<script lang="ts">
  import { onDestroy } from "svelte";

  // Pass the raw audio buffer or connect to your audioPlayback store context
  export let audioContext: AudioContext | null = null;
  export let sourceNode: AudioNode | null = null;

  let canvas: HTMLCanvasElement;
  let animationId: number;
  let analyser: AnalyserNode;
  let dataArray: Uint8Array<ArrayBuffer>;

  // Initialize Audio Analyzer
  function setupAnalyzer() {
    if (!audioContext || !sourceNode) return;
    // Clear any existing animation loop to prevent duplicates
    if (animationId) cancelAnimationFrame(animationId);

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 64; // Low number for chunkier "tech" look
    sourceNode.connect(analyser);

    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    draw();
  }

  function draw() {
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    animationId = requestAnimationFrame(draw);
    analyser.getByteFrequencyData(dataArray);

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = 30; // Radius of the inner core

    // Clear with a fade effect for trails
    ctx.fillStyle = "rgba(24, 24, 27, 0.2)"; // Zinc-950 with fade
    ctx.fillRect(0, 0, width, height);

    // 1. Draw Inner Glowing Core
    const avgFreq = dataArray.reduce((a, b) => a + b) / dataArray.length;
    const pulseSize = (avgFreq / 255) * 10; // Core pulses with volume

    ctx.beginPath();
    ctx.arc(centerX, centerY, radius + pulseSize, 0, 2 * Math.PI);
    ctx.fillStyle = "#06b6d4"; // Cyan-500
    ctx.shadowBlur = 20 + pulseSize * 2;
    ctx.shadowColor = "#06b6d4";
    ctx.fill();

    // 2. Draw Radiating Frequency Bars
    const bars = 20; // Number of bars around the circle
    const step = (Math.PI * 2) / bars;

    for (let i = 0; i < bars; i++) {
      // Map frequency data to bars (mirroring half the data)
      const value = dataArray[i % dataArray.length];
      const barHeight = (value / 255) * 40; // Max height 40px

      // Calculate angle
      const angle = i * step;

      // Start point (on circle edge)
      const x1 = centerX + Math.cos(angle) * (radius + 5);
      const y1 = centerY + Math.sin(angle) * (radius + 5);

      // End point (radiating out)
      const x2 = centerX + Math.cos(angle) * (radius + 5 + barHeight);
      const y2 = centerY + Math.sin(angle) * (radius + 5 + barHeight);

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);

      // Style: Electric Shocker Yellow/Blue gradient feel
      ctx.strokeStyle = value > 150 ? "#facc15" : "#22d3ee"; // Yellow if loud, Cyan if quiet
      ctx.lineWidth = 4;
      ctx.lineCap = "round";
      ctx.shadowBlur = 10;
      ctx.shadowColor = ctx.strokeStyle;
      ctx.stroke();
    }
  }

  // Reactive re-setup if props change, ensuring canvas is ready
  $: if (audioContext && sourceNode && canvas) setupAnalyzer();

  onDestroy(() => {
    cancelAnimationFrame(animationId);
  });
</script>

<div
  class="relative w-full h-48 flex items-center justify-center bg-zinc-950 rounded-lg border border-zinc-800 overflow-hidden group"
>
  <div
    class="absolute inset-0 opacity-10"
    style="background-image: radial-gradient(#22d3ee 1px, transparent 1px); background-size: 20px 20px;"
  ></div>

  <canvas bind:this={canvas} width={300} height={200} class="relative z-10"
  ></canvas>

  {#if !sourceNode}
    <div
      class="absolute text-cyan-500/30 text-xs font-mono tracking-[0.2em] animate-pulse"
    >
      SYSTEM_IDLE
    </div>
  {/if}
</div>
