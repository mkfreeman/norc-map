<script>
  export let checked = true;
  export let onClick = () => {};
  export let imageUrl = "./ttc.svg";
</script>

<button
  on:click|preventDefault={onClick}
  class={`py-2 mx-2 my-1 hover:border-black border-solid border-2 border-black ${
    checked ? "opacity-100" : "opacity-30 hover:opacity-50"
  }`}
  style="background-image: url({imageUrl});"
/>

<style>
  button {
    height: 40px;
    width: 60px;
    background-repeat: no-repeat;
    background-size: contain;
    background-position: center;
    transition: none;
  }
  button:focus {
    outline: none;
  }
</style>
