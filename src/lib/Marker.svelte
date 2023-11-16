<script lang="ts">
  import { onMount, onDestroy, getContext, setContext } from "svelte";
  import L from "leaflet";
  
  export let latLng: L.LatLngExpression;  
  export let iconUrl = "./ttc.svg";
  export let iconSize = [50, 50];

  let marker: L.CircleMarker | undefined;
  let markerElement: HTMLElement;

  const { getMap }: { getMap: () => L.Map | undefined } = getContext("map");
  const map = getMap();
  
  setContext("layer", {
    // L.Marker inherits from L.Layer
    getLayer: () => marker,
  });

  onMount(() => {
    if (map) {		
      let icon = L.icon({
        iconUrl,
        iconSize,
      });
      marker = L.marker(latLng, { icon }).addTo(map);     
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
