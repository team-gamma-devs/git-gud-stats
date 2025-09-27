<script lang="ts">
    import { page } from "$app/state";
    import { onMount } from "svelte";
    import AuthBox from "$lib/components/AuthBox.svelte";
    import { isAuth } from "$lib/stores/auth";

    let errorType: String | "Error Not Defined";
    let errorMsg: String | "No Message";

    onMount(() => {
        errorType = page.url.searchParams.get("error") || "Error Not Defined";
        errorMsg = page.url.searchParams.get("message") || "No Message";

        console.warn("Error Type: " + errorType);
    });
</script>

{#if !$isAuth}
    <section id="error-container" class="border-1 border-primary-200 dark:border-gray-600 p-10 rounded-lg bg-bg shadow-md">
        <img src="./octocat_sad.png" class="m-auto mb-10" alt="Octocat Sad" width=300>
        <h1 class="text-2xl font-bold mb-2">{errorType?.toUpperCase()}</h1>
        <h2 class="text-lg text-primary">{errorMsg}</h2>
    </section>
{/if}

