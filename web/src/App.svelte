<script lang="ts">
    import { Controls, Console, ActivityFeed, Header} from './lib/components';
    import { createVoiceSession } from './lib/websocket';

    const voiceSession = createVoiceSession();
</script>

<div class="max-w-3x1 mx-auto">
    <Header />
    <Controls onStart={() => voiceSession.start()} onStop={() => voiceSession.stop()} />
    <ActivityFeed />
    <Console />
</div>