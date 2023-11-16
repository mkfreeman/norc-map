<script lang="ts">
  import { onMount } from "svelte";
  import Leaflet from "./lib/Leaflet.svelte";
  import Marker from "./lib/Marker.svelte";
  import Popup from "./lib/Popup.svelte";
  import PolyLine from "./lib/PolyLine.svelte";
  import Checkbox from "./lib/Checkbox.svelte";
  import type { LatLngExpression } from "leaflet";
  import * as d3 from "d3";

  const stationColor = "black";
  const buildingColor = "blue";
  const initialView: LatLngExpression = [43.70107, -79.397015];
  let centroids;
  let paths;
  let stations;
  let displayStations = true;
  let displayRoutes = true;
  let displayBuildings = true;
  onMount(async () => {
    // TODO: filter down to pre-set bounds    
    centroids = await fetch(
      "./sample_toronto_apartments_CENTROIDS.geojson"
    ).then((res) => res.json());
    paths = await fetch("./sample_toronto_apartments_PATHS.geojson").then(
      (res) => res.json()
    );
    // TODO: load this data from a file
    stations = paths.features.map((d) => d.geometry.coordinates.slice(-1)[0]);
  });
  function toggleStations() {
    displayStations = !displayStations;
  }
  function toggleRoutes() {
    displayRoutes = !displayRoutes;
  }
  function toggleBuildings() {
    displayBuildings = !displayBuildings;
  }
</script>

<div class="w-full h-[calc(100vh-150px)]">
  <form class="flex">
    <!-- TODO: rename checkbox to... buttonToggle? -->
    <Checkbox
      imageUrl="ttc.svg"
      checked={displayStations}
      onClick={toggleStations}
    />
     <Checkbox
      imageUrl="apartment.svg"
      checked={displayBuildings}
      onClick={toggleBuildings}
    />
    <Checkbox   
      imageUrl="route.svg"   
      checked={displayRoutes}
      onClick={toggleRoutes}
    />
   
    <!-- TODO: would be fun to have a slider to filter by distance -->
  </form>
  <Leaflet view={initialView} zoom={11}>
    {#if centroids?.features && displayBuildings}
      {#each centroids.features as norc}
        <!-- TODO: switch lat and long in data -->
        <Marker
          latLng={[
            +norc.geometry.coordinates[1],
            +norc.geometry.coordinates[0],
          ]}
          iconUrl="apartment.svg"
          iconSize={[15,100]}
        >
          <Popup>Building ID: {norc.properties.cat}</Popup>
        </Marker>
      {/each}
    {/if}
    {#if stations && displayStations}
      {#each stations as station}
        <!-- TODO: switch lat and long in data -->
        <Marker latLng={[station[1], station[0]]} iconUrl="ttc.svg" radius={4}>
          <Popup>Building ID: {norc.properties.cat}</Popup>
        </Marker>
      {/each}
    {/if}
    {#if paths?.features && displayRoutes}
      {#each paths.features as path}
        <!-- TODO: switch lat and long in data -->
        <PolyLine
          latLngs={path.geometry.coordinates.map((d) => [+d[1], +d[0]])}
        />
      {/each}
    {/if}
  </Leaflet>
</div>
