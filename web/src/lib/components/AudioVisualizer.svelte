<script lang="ts">
  import { onDestroy } from "svelte";

  export let audioContext: AudioContext | null = null;
  export let sourceNode: AudioNode | null = null;

  let canvas: HTMLCanvasElement;
  let animationId: number;
  let analyser: AnalyserNode;
  let dataArray: Uint8Array<ArrayBuffer>;
  let phase = 0;

  let containerWidth: number;
  let containerHeight: number;

  $: if (canvas && containerWidth && containerHeight) {
    canvas.width = containerWidth;
    canvas.height = containerHeight;
  }

  function setupAnalyzer() {
    if (!audioContext || !sourceNode) return;
    if (animationId) cancelAnimationFrame(animationId);

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 1024; // Better resolution for time domain wave
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
    analyser.getByteTimeDomainData(dataArray);

    const width = canvas.width;
    const height = canvas.height;

    // Fading background for smooth trace
    ctx.fillStyle = "rgba(9, 9, 11, 0.35)";
    ctx.fillRect(0, 0, width, height);

    const bufferLength = analyser.frequencyBinCount;
    const sliceWidth = (width * 1.0) / bufferLength;

    // Calculate intensity from time domain data
    let maxAmp = 0;
    for (let i = 0; i < bufferLength; i++) {
      const amp = Math.abs(dataArray[i] - 128);
      if (amp > maxAmp) maxAmp = amp;
    }

    const intensity = Math.min(1, maxAmp / 64);

    // Update movement phase
    phase -= 0.05 + intensity * 0.15;

    // Draw multiple intertwined waves for analogue feel
    const numWaves = 3;
    for (let w = 0; w < numWaves; w++) {
      ctx.beginPath();
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        // Normalized audio signal (-1 to 1)
        const audioSignal = (dataArray[i] - 128) / 128.0;

        // Artificial ambient sine waves
        const sinePhasePhase = phase + w * Math.PI * 0.7;
        const sineFreq = 0.03 + w * 0.01;
        const sineSignal =
          Math.sin(x * sineFreq + sinePhasePhase) * 0.4 * (1 - w * 0.2);

        // Blend ambient sine waves with real audio data
        const blendFactor = Math.min(1, maxAmp / 10);
        const layerScale = 1 - w * 0.25;
        const blendedSignal =
          sineSignal * (1 - blendFactor) +
          audioSignal * blendFactor * layerScale;

        // Taper ends to look smooth
        const taper = Math.sin((x / width) * Math.PI);

        // Dynamic amplitude burst
        const ampBoost = 1 + intensity * 1.5;

        const yOffset = blendedSignal * (height / 2) * taper * ampBoost;
        const y = height / 2 + yOffset;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
        x += sliceWidth;
      }

      ctx.lineCap = "round";
      ctx.lineJoin = "round";

      const alpha = Math.max(0.15, 1 - w * 0.3);

      // Reactive Colors (Yellow for Highs, Cyan for Normal, Dark Cyan for low/idle)
      if (maxAmp > 40) {
        ctx.strokeStyle = `rgba(250, 204, 21, ${alpha})`; // yellow
        ctx.shadowColor = "#facc15";
      } else if (maxAmp > 15) {
        ctx.strokeStyle = `rgba(34, 211, 238, ${alpha})`; // cyan
        ctx.shadowColor = "#22d3ee";
      } else {
        ctx.strokeStyle = `rgba(6, 182, 212, ${alpha * 0.5})`; // darker cyan
        ctx.shadowColor = "transparent";
      }

      ctx.lineWidth = Math.max(1.5, 3.5 - w);
      ctx.shadowBlur = maxAmp > 10 ? 10 + maxAmp / 3 : 0;
      ctx.stroke();
    }

    // Clear shadow state for background fill on next frame
    ctx.shadowBlur = 0;
  }

  $: if (audioContext && sourceNode && canvas) setupAnalyzer();

  onDestroy(() => {
    cancelAnimationFrame(animationId);
  });
</script>

<div
  bind:clientWidth={containerWidth}
  bind:clientHeight={containerHeight}
  class="relative w-full h-full min-h-[176px] flex items-center justify-center bg-zinc-950 rounded-lg overflow-hidden"
>
  <canvas bind:this={canvas} class="absolute inset-0 z-10 block w-full h-full"
  ></canvas>

  {#if !sourceNode}
    <div
      class="absolute text-zinc-700 text-[10px] font-mono tracking-[0.2em] z-20"
    >
      IDLE
    </div>
  {/if}
</div>
