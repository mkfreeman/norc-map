<script lang="ts">
  import { onMount, onDestroy, getContext, setContext } from "svelte";
  import L from "leaflet";
  export let latLngs: number[][];

  let polyLine: L.Polyline | undefined;
  let polyLineElement: HTMLElement;

  const { getMap }: { getMap: () => L.Map | undefined } = getContext("map");
  const map = getMap();

  setContext("layer", {
    // L.polyLine inherits from L.Layer
    getLayer: () => polyLine,
  });

  onMount(() => {
    if (map) {
      polyLine = L.polyline(latLngs, { color: "black", weight: 2, opacity: 0.8 }).addTo(
        map
      );
    }
  });

  onDestroy(() => {
    polyLine?.remove();
    polyLine = undefined;
  });
</script>

<div bind:this={polyLineElement}>
  {#if polyLine}
    <slot />
  {/if}
</div>
