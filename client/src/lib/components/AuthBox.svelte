<script>
    import { isAuth } from "$lib/stores/auth";
</script>


<!-- This will be used to display Auth Only content -->

{#if $isAuth}
    <slot/>
{:else}
  <section id="places-user-not-logged-section">
    <h2>You must log in to see this page!</h2>
  </section>
{/if}