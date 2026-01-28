const workletCode = `

class PCMProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.buffer = [];
        this.targetSampleRate = 16000; // Target sample rate for deepgram
        this.resampleRatio = sampleRate / this.targetSampleRate;
        this.resampleIndex = 0;
    }

    process(inputs) {
        const input = inputs[0];
        if (!input || !input[0]) return true;
        
        const channelData = input[0];
        
        for (let i = 0; i < channelData.length; i++) {
            this.resampleIndex += 1;
            if (this.resampleIndex >= this.resampleRatio) {
                this.resampleIndex -= this.resampleRatio;
                let sample = channelData[i];
                // Clamp the sample to [-1, 1]
                sample = Math.max(-1, Math.min(1, sample));
                // Convert to 16-bit PCM
                const intSample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
                this.buffer.push(intSample);
            }
        }
        
        const CHUNK_SIZE = 1600;
        while (this.buffer.length >= CHUNK_SIZE) {
            const chunk = this.buffer.splice(0, CHUNK_SIZE);
            const int16Array = new Int16Array(chunk);
            this.port.postMessage(int16Array.buffer, [int16Array.buffer]);
        }
        
        return true;
    }
}

registerProcessor('pcm-processor', PCMProcessor);
`;

export interface AudioCapture {
    start: (onChunk: (chunk: ArrayBuffer) => void) => Promise<void>;
    stop: () => void;
}

export function createAudioCapture(): AudioCapture {
    let audioContext: AudioContext | null = null;
    let workletNode: AudioWorkletNode | null = null;
    let mediaStream: MediaStream | null = null;

    async function start(onChunk: (chunk: ArrayBuffer) => void): Promise<void> {

        if (!audioContext) {
            audioContext = new AudioContext({"sampleRate": 16000});
            const blob = new Blob([workletCode], { type: "application/javascript"});
            const workletUrl = URL.createObjectURL(blob);
            await audioContext.audioWorklet.addModule(workletUrl);
            URL.revokeObjectURL(workletUrl);
        }

        // Resume if suspended
        if (audioContext.state === "suspended") {
            await audioContext.resume();
        }

        // Get mic access
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
        }
        });

        const sourceNode = audioContext.createMediaStreamSource(mediaStream);
        workletNode = new AudioWorkletNode(audioContext, 'pcm-processor');

        workletNode.port.onmessage = (event) => {
            onChunk(event.data);
        };

        sourceNode.connect(workletNode);
    }

    function stop(): void {
        if (workletNode) {
            workletNode.disconnect();
            workletNode = null;
        }

        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            mediaStream = null;
        }

        // 🔴 FIX: Close the AudioContext to release the hardware
        if (audioContext) {
            audioContext.close();
            audioContext = null;
        }
    }   

    return {
        start,
        stop
    };
}