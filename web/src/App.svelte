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
    // Reactive access to the store
    const visualizerState = voiceSession.visualizerStore;
</script>

<div
    class="min-h-screen bg-neutral-950 text-neutral-200 p-4 md:p-6 font-sans selection:bg-cyan-500/30"
>
    <div class="max-w-7xl mx-auto flex flex-col gap-6 h-full">
        <!-- Header Section -->
        <div
            class="bg-neutral-900/40 backdrop-blur-md border border-neutral-800 rounded-2xl p-6 shadow-xl relative overflow-hidden"
        >
            <div
                class="absolute inset-0 bg-gradient-to-r from-cyan-900/10 to-purple-900/10 pointer-events-none"
            ></div>
            <Header />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            <!-- LEFT COLUMN: CONTROLS & VISUALS (4 cols) -->
            <div class="lg:col-span-4 flex flex-col gap-6 sticky top-6">
                <!-- Main Control Card -->
                <div
                    class="bg-neutral-900/40 backdrop-blur-md border border-neutral-800 rounded-2xl p-6 shadow-2xl relative overflow-hidden group"
                >
                    <div
                        class="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-transparent pointer-events-none opacity-50 group-hover:opacity-100 transition-opacity"
                    ></div>

                    <div class="flex items-center gap-2 mb-4">
                        <div
                            class="w-1.5 h-1.5 rounded-full bg-cyan-500 shadow-[0_0_8px_rgba(6,182,212,0.6)] animate-pulse"
                        ></div>
                        <h2
                            class="text-[10px] font-bold text-cyan-500/80 uppercase tracking-widest"
                        >
                            Control Systems
                        </h2>
                    </div>

                    <Controls
                        onStart={() => voiceSession.start()}
                        onStop={() => voiceSession.stop()}
                    />
                </div>

                <!-- Visualizer Card -->
                <div
                    class="bg-neutral-900/40 backdrop-blur-md border border-neutral-800 rounded-2xl p-1 shadow-xl overflow-hidden relative"
                >
                    <AudioVisualizer
                        audioContext={$visualizerState.ctx}
                        sourceNode={$visualizerState.node}
                    />
                </div>

                <!-- Pipeline Telemetry -->
                <div
                    class="bg-neutral-900/40 backdrop-blur-md border border-neutral-800 rounded-2xl p-6 shadow-xl"
                >
                    <div class="flex items-center gap-2 mb-4">
                        <span class="text-cyan-400">⚡</span>
                        <h2
                            class="text-[10px] font-bold text-neutral-500 uppercase tracking-widest"
                        >
                            Pipeline Telemetry
                        </h2>
                    </div>
                    <PipelineCard />
                </div>
            </div>

            <!-- RIGHT COLUMN: FEED & LOGS (8 cols) -->
            <div class="lg:col-span-8 flex flex-col gap-6">
                <!-- Activity Feed -->
                <div
                    class="bg-neutral-900/40 backdrop-blur-md border border-neutral-800 rounded-2xl shadow-2xl min-h-[600px] flex flex-col relative overflow-hidden"
                >
                    <!-- Decor -->
                    <div
                        class="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-cyan-500/20 to-transparent"
                    ></div>

                    <div
                        class="p-4 border-b border-neutral-800/50 bg-neutral-900/30 flex items-center justify-between backdrop-blur-sm z-10"
                    >
                        <div class="flex items-center gap-2">
                            <span class="text-neutral-500">➜</span>
                            <h2
                                class="text-[10px] font-bold text-neutral-400 uppercase tracking-widest"
                            >
                                Live Interaction Log
                            </h2>
                        </div>
                        <div class="flex gap-1.5">
                            <span class="w-1 h-1 rounded-full bg-neutral-700"
                            ></span>
                            <span class="w-1 h-1 rounded-full bg-neutral-700"
                            ></span>
                            <span class="w-1 h-1 rounded-full bg-neutral-700"
                            ></span>
                        </div>
                    </div>
                    <div class="flex-grow p-0 relative">
                        <div class="absolute inset-0 overflow-auto">
                            <ActivityFeed />
                        </div>
                    </div>
                </div>

                <!-- System Console -->
                <div
                    class="bg-black/40 border border-neutral-800 rounded-xl overflow-hidden backdrop-blur-sm"
                >
                    <div
                        class="bg-neutral-900/80 px-4 py-2 border-b border-neutral-800 flex items-center justify-between"
                    >
                        <h2
                            class="text-[10px] font-mono text-neutral-500 uppercase flex items-center gap-2"
                        >
                            <span>_system_console</span>
                        </h2>
                    </div>
                    <div class="p-0">
                        <Console />
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
