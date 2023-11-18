<script lang="ts">
  import * as Plot from "@observablehq/plot";

  export let options;
  export let handleClick = (event:PointerEvent) => {};

  function myplot(node:HTMLElement) {
    node.appendChild(Plot.plot(options));
  }

</script>

{#key options}
  <div on:click={handleClick} use:myplot {...$$restProps} />
{/key}
