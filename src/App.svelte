<script lang="ts">
  import { onMount } from "svelte";
  import Leaflet from "./lib/Leaflet.svelte";
  import Marker from "./lib/Marker.svelte";
  import Popup from "./lib/Popup.svelte";
  import type { LatLngExpression } from "leaflet";
  const initialView: LatLngExpression = [43.65107, -79.397015];
  import * as d3 from "d3";
  let data;
  let mapData;
  let stations;
  let accessibleOnly = true;
  let subwayOnly = true;
  onMount(async () => {
    // TODO: filter down to pre-set bounds
    data = await d3.csv("./stops.txt");
    mapData = data;
  });
  function toggleSubway() {
    subwayOnly = !subwayOnly;
  }
  function handleClick() {
    accessibleOnly = !accessibleOnly;
  }
  $: mapData = !data
    ? []
    : data.filter((d) => {
        const isSubway = d.stop_name.includes("Station");
        const isaccessible = d.wheelchair_boarding === "1";
        return (
          (subwayOnly ? isSubway : true) &&
          (accessibleOnly ? isaccessible : true)
        );
      });
</script>

<div class="w-full h-[calc(100vh-150px)]">
  <form>
    <div class="flex items-start mb-3 font-bold cursor-pointer">
      <div class="flex items-center h-5 cursor-pointer">
        <input
          on:click={toggleSubway}
          checked={subwayOnly}
          id="subway"
          type="checkbox"
          class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
        />
      </div>
      <label
        for="subway"
        class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Subway only (<em>a little slow</em>)</label
      >
    </div>
    <div class="flex items-start mb-3 font-bold cursor-pointer">
      <div class="flex items-center h-5 cursor-pointer">
        <input
          on:click={handleClick}
          checked={accessibleOnly}
          id="accessible"
          type="checkbox"
          class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
        />
      </div>
      <label
        for="accessible"
        class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
        >Accessible only</label
      >
    </div>
  </form>
  <Leaflet view={initialView} zoom={14}>
    {#if mapData}
      {#each mapData as stop}
        <Marker
          latLng={[+stop.stop_lat, +stop.stop_lon]}
          width={20}
          height={20}
        >
          <div class="bg-black w-3 h-3 rounded-full" />
          <Popup>{stop.stop_name}</Popup>
        </Marker>
      {/each}
    {/if}
  </Leaflet>
</div>
