<script>
    import { isAuth } from "$lib/stores/auth";
    import GitHubLoginBtn from "./GitHubLoginBtn.svelte";
</script>


<!-- This will be used to display Auth Only content -->

{#if $isAuth}
    <slot/>
{:else}
  <section id="places-user-not-logged-section">
    <h2>You must log in to see this page!</h2>
    <GitHubLoginBtn/>
  </section>
{/if}

<style>
  #places-user-not-logged-section {
    /* outline: 1px solid red; */
    padding: 10px;
    display: flex;
    align-items: center;
    flex-direction: column;
    gap: 1dvw;
  }
</style>