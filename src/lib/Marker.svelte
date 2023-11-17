<script lang="ts">
  import {
    onMount,
    onDestroy,
    getContext,
    setContext,
    beforeUpdate,
    afterUpdate,
  } from "svelte";
  import L from "leaflet";

  export let latLng: L.LatLngExpression;
  export let iconUrl;
  export let iconSize = [50, 50];
  export let radius = 4;
  export let fillColor = "blue";

  let marker: L.CircleMarker | undefined;
  let markerElement: HTMLElement;

  const { getMap }: { getMap: () => L.Map | undefined } = getContext("map");
  const map = getMap();

  setContext("layer", {
    // L.Marker inherits from L.Layer
    getLayer: () => marker,
  });

  function makeMarker() {
    marker = iconUrl
      ? L.marker(latLng, {
          icon: L.icon({
            iconUrl,
            iconSize,
          }),
        }).addTo(map)
      : L.circleMarker(latLng, {
          radius,
          fillColor,
          stroke: false,
          fillOpacity: 1,
        }).addTo(map);
  }

  onMount(() => {
    if (map) makeMarker();
  });

  // TODO: this is redundant....
  afterUpdate(() => {
    if (marker && map) {
      marker.remove();
      makeMarker();
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
