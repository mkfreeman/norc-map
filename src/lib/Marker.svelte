<script lang="ts">
  import { onMount, onDestroy, getContext, setContext } from "svelte";
  import L, { type PointExpression } from "leaflet";

  export let latLng: L.LatLngExpression;
  export let iconUrl: string = "";
  export let iconSize: PointExpression = [50, 50];
  export let radius = 4;
  export let fillColor = "blue";

  let marker: L.CircleMarker | L.Marker | undefined;
  let markerElement: HTMLElement;

  const { getMap }: { getMap: () => L.Map | undefined } = getContext("map");
  const map: L.Map | undefined = getMap();

  setContext("layer", {
    getLayer: () => marker,
  });

  function makeMarker() {
    marker = !map
      ? undefined
      : iconUrl
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
            fillOpacity: 0.6,
          }).addTo(map);
  }

  onMount(() => {
    if (map) makeMarker();
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
