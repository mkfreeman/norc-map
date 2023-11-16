<script lang="ts">
  import { onMount } from "svelte";
  import Leaflet from "./lib/Leaflet.svelte";
  import Marker from "./lib/Marker.svelte";
  import Popup from "./lib/Popup.svelte";
  import Histogram from "./lib/Histogram.svelte";
  import PolyLine from "./lib/PolyLine.svelte";
  import Checkbox from "./lib/Checkbox.svelte";
  import type { LatLngExpression } from "leaflet";

  const initialView: LatLngExpression = [43.70107, -79.397015];
  let centroids;
  let allPaths;
  let stations;
  let displayStations = true;
  let displayRoutes = true;
  let displayBuildings = true;
  let distances;
  let distanceLimits: [number, number] = [0, 1];
  onMount(async () => {
    // TODO: filter down to pre-set bounds
    centroids = await fetch(
      "./sample_toronto_apartments_CENTROIDS.geojson"
    ).then((res) => res.json());
    allPaths = await fetch("./sample_toronto_apartments_PATHS.geojson").then(
      (res) => res.json()
    );
    // TODO: load this data from a file
    stations = allPaths.features.map(
      (d) => d.geometry.coordinates.slice(-1)[0]
    );
    distances = allPaths.features.map((d) => d.properties.dist);
    distanceLimits = [0, Math.max(...distances)];
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
  function setDistanceLimit(range: [number, number]) {
    distanceLimits = range || [0, Math.max(...distances)];
  }
  $: paths = allPaths?.features.filter((d) => {
    return (
      d.properties.dist >= distanceLimits[0] &&
      d.properties.dist <= distanceLimits[1]
    );
  });
</script>

<div class="w-full">
  <h1 class="flex pb-2 text-2xl">Naturally Occuring Retirement Communities</h1>
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
    {#if distances}
      <Histogram
        data={distances}
        label="Distance →"
        onUpdate={setDistanceLimit}
      />
    {/if}

    <!-- TODO: would be fun to have a slider to filter by distance -->
  </form>
  <div class="h-[calc(100vh-250px)]">
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
            iconSize={[15, 100]}
          >
            <Popup>Building ID: {norc.properties.cat}</Popup>
          </Marker>
        {/each}
      {/if}
      {#if stations && displayStations}
        {#each stations as station}
          <!-- TODO: switch lat and long in data -->
          <Marker
            latLng={[station[1], station[0]]}
            iconUrl="ttc.svg"
            radius={4}
          >
            <Popup>Building ID: {norc.properties.cat}</Popup>
          </Marker>
        {/each}
      {/if}
      {#if paths && displayRoutes}
        {#each paths as path}
          <!-- TODO: switch lat and long in data -->
          <PolyLine
            latLngs={path.geometry.coordinates.map((d) => [+d[1], +d[0]])}
          />
        {/each}
      {/if}
    </Leaflet>
  </div>
</div>
