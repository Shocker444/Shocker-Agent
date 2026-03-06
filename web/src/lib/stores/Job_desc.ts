import { writable } from "svelte/store";
import { JobDesc } from "../types";

const initialJobDesc: JobDesc = {
    id: "",
    title: "",
    description: ""
};

function createJobDescStore() {
    const { subscribe, set } = writable<JobDesc>(initialJobDesc);

    return {
        subscribe,

        setJobDesc(jobDesc: string) {
            set({
                ...initialJobDesc,
                description: jobDesc
            })
        }
    };
}


export const jobDescStore = createJobDescStore();