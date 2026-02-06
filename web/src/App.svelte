<script lang="ts">
    import {
        Controls,
        Console,
        ActivityFeed,
        Header,
        PipelineCard,
        AudioVisualizer,
    } from "./lib/components";
    import { createVoiceSession } from "./lib/websocket";
    // Audio playback is handled inside voiceSession

    const voiceSession = createVoiceSession();
    const visualizerState = voiceSession.visualizerStore;
    console.log("Initial state:", $visualizerState);
    console.log($visualizerState.node);
</script>

<div class="max-w-3x1 mx-auto">
    <Header />
    <Controls
        onStart={() => voiceSession.start()}
        onStop={() => voiceSession.stop()}
    />
    <AudioVisualizer
        audioContext={$visualizerState.ctx}
        sourceNode={$visualizerState.node}
    />
    <PipelineCard />
    <ActivityFeed />
    <Console />
</div>
