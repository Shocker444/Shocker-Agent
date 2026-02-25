<script lang="ts">
  import { onDestroy } from "svelte";

  export let audioContext: AudioContext | null = null;
  export let sourceNode: AudioNode | null = null;

  let canvas: HTMLCanvasElement;
  let animationId: number;
  let analyser: AnalyserNode;
  let dataArray: Uint8Array<ArrayBuffer>;

  function setupAnalyzer() {
    if (!audioContext || !sourceNode) return;
    if (animationId) cancelAnimationFrame(animationId);

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 64;
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
    const radius = 30;

    ctx.fillStyle = "rgba(9, 9, 11, 0.25)"; // zinc-950 with fade
    ctx.fillRect(0, 0, width, height);

    // Inner Core
    const avgFreq = dataArray.reduce((a, b) => a + b) / dataArray.length;
    const pulseSize = (avgFreq / 255) * 10;

    ctx.beginPath();
    ctx.arc(centerX, centerY, radius + pulseSize, 0, 2 * Math.PI);
    ctx.fillStyle = "#06b6d4";
    ctx.shadowBlur = 0;
    ctx.shadowColor = "transparent";
    ctx.fill();

    // Frequency Bars
    const bars = 20;
    const step = (Math.PI * 2) / bars;

    for (let i = 0; i < bars; i++) {
      const value = dataArray[i % dataArray.length];
      const barHeight = (value / 255) * 40;
      const angle = i * step;

      const x1 = centerX + Math.cos(angle) * (radius + 5);
      const y1 = centerY + Math.sin(angle) * (radius + 5);
      const x2 = centerX + Math.cos(angle) * (radius + 5 + barHeight);
      const y2 = centerY + Math.sin(angle) * (radius + 5 + barHeight);

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = value > 150 ? "#facc15" : "#22d3ee";
      ctx.lineWidth = 3;
      ctx.lineCap = "round";
      ctx.shadowBlur = 0;
      ctx.stroke();
    }
  }

  $: if (audioContext && sourceNode && canvas) setupAnalyzer();

  onDestroy(() => {
    cancelAnimationFrame(animationId);
  });
</script>

<div
  class="relative w-full h-44 flex items-center justify-center bg-zinc-950 rounded-lg overflow-hidden"
>
  <canvas bind:this={canvas} width={300} height={180} class="relative z-10"
  ></canvas>

  {#if !sourceNode}
    <div class="absolute text-zinc-700 text-[10px] font-mono tracking-[0.2em]">
      IDLE
    </div>
  {/if}
</div>
