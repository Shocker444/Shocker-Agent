import { writable } from "svelte/store";

const initialResume = {
    fileBase64: "",
    fileName: ""
};

function createResumeStore() {
    const { subscribe, set } = writable(initialResume);

    return {
        subscribe,
        setResume(fileBase64: string, fileName: string) {
            set({
                fileBase64,
                fileName
            });
        },
        reset() {
            set(initialResume);
        }
    };
}

export const resumeStore = createResumeStore();
