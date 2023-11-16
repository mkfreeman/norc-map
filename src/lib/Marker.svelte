<script lang="ts">
  import { onMount, onDestroy, getContext, setContext } from "svelte";
  import L from "leaflet";

  export let fillColor = "blue";
  export let latLng: L.LatLngExpression;
  export let radius = 5;

  let marker: L.CircleMarker | undefined;
  let markerElement: HTMLElement;

  const { getMap }: { getMap: () => L.Map | undefined } = getContext("map");
  const map = getMap();

  setContext("layer", {
    // L.Marker inherits from L.Layer
    getLayer: () => marker,
  });

  onMount(() => {
    // console.log({latLng})
    if (map) {
      marker = L.circleMarker(latLng, {
        radius,
        fillOpacity: 0.6,
        fillColor,
        stroke: false,
      }).addTo(map);
    }
  });

  onDestroy(() => {
    marker?.remove();
    marker = undefined;
  });
</script>

<div bind:this={markerElement}>
  {#if marker}
    <slot />
  {/if}
</div>
