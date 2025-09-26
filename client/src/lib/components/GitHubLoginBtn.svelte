<script lang="ts">
  import { Button } from "flowbite-svelte";
  import { GithubSolid } from "flowbite-svelte-icons";

  function handleGitHubAuth() {
    window.location.href="http://localhost:8000/auth/github"
  }
</script>

<Button color="dark" class="cursor-pointer" onclick={handleGitHubAuth}>
  Log In With <b class="ml-1">GitHub</b> <GithubSolid class="ml-2 h-5 w-5" /> 
</Button>