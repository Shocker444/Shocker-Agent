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

    const voiceSession = createVoiceSession();
    const visualizerState = voiceSession.visualizerStore;
</script>

<div
    class="min-h-screen bg-zinc-950 text-zinc-200 p-4 md:p-6 font-sans selection:bg-cyan-500/20"
>
    <div class="max-w-7xl mx-auto flex flex-col gap-5 h-full">
        <!-- Header -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl px-6 py-4">
            <Header />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
            <!-- LEFT COLUMN: CONTROLS & VISUALS (4 cols) -->
            <div class="lg:col-span-4 flex flex-col gap-5 sticky top-5">
                <!-- Control Panel -->
                <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5">
                    <div class="flex items-center gap-2 mb-5">
                        <span class="w-0.5 h-4 bg-cyan-500 rounded-full"></span>
                        <h2
                            class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest"
                        >
                            Controls
                        </h2>
                    </div>
                    <Controls
                        onStart={() => voiceSession.start()}
                        onStop={() => voiceSession.stop()}
                    />
                </div>

                <!-- Audio Visualizer -->
                <div
                    class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden"
                >
                    <AudioVisualizer
                        audioContext={$visualizerState.ctx}
                        sourceNode={$visualizerState.node}
                    />
                </div>

                <!-- Pipeline Telemetry -->
                <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5">
                    <div class="flex items-center gap-2 mb-4">
                        <span class="w-0.5 h-4 bg-zinc-600 rounded-full"></span>
                        <h2
                            class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest"
                        >
                            Pipeline Telemetry
                        </h2>
                    </div>
                    <PipelineCard />
                </div>
            </div>

            <!-- RIGHT COLUMN: FEED & LOGS (8 cols) -->
            <div class="lg:col-span-8 flex flex-col gap-5">
                <!-- Activity Feed -->
                <div
                    class="bg-zinc-900 border border-zinc-800 rounded-xl min-h-[600px] flex flex-col overflow-hidden"
                >
                    <div
                        class="px-5 py-3 border-b border-zinc-800 flex items-center justify-between"
                    >
                        <div class="flex items-center gap-2">
                            <span class="w-0.5 h-4 bg-zinc-600 rounded-full"
                            ></span>
                            <h2
                                class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest"
                            >
                                Live Interaction Log
                            </h2>
                        </div>
                    </div>
                    <div class="flex-grow relative">
                        <div class="absolute inset-0 overflow-auto">
                            <ActivityFeed />
                        </div>
                    </div>
                </div>

                <!-- System Console -->
                <div
                    class="bg-zinc-950 border border-zinc-800 rounded-xl overflow-hidden"
                >
                    <div
                        class="px-4 py-2.5 border-b border-zinc-800 flex items-center gap-2"
                    >
                        <span class="w-0.5 h-4 bg-zinc-700 rounded-full"></span>
                        <h2
                            class="text-[10px] font-mono font-bold text-zinc-600 uppercase tracking-widest"
                        >
                            system_console
                        </h2>
                    </div>
                    <Console />
                </div>
            </div>
        </div>
    </div>
</div>
