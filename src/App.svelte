<script lang="ts">
  import { onMount } from "svelte";
  import Leaflet from "./lib/Leaflet.svelte";
  import Marker from "./lib/Marker.svelte";
  import Popup from "./lib/Popup.svelte";
  import Histogram from "./lib/Histogram.svelte";
  import PolyLine from "./lib/PolyLine.svelte";
  import Checkbox from "./lib/Checkbox.svelte";
  import Radio from "./lib/Radio.svelte";
  import type { LatLngExpression } from "leaflet";
  import * as d3 from "d3";

  const initialView: LatLngExpression = [43.70107, -79.397015];
  let displayStations = true;
  let displayRoutes = true;
  let displayBuildings = true;
  let distances: number[];
  let numSeniors: number[];
  let distanceLimits: [number, number] = [0, 1];
  let numSeniorsLimit: [number, number] = [0, 1];
  let data;

  function handleUpdate(selected: string) {
    selectedOption = selected;
  }

  $: selectedOption = "wheelchair_boarding";
  const radioOptions = [
    { value: "wheelchair_boarding", label: "Wheelchair boarding" },
    { value: "has_shelter", label: "Has shelter" },
    { value: "has_shelter_with_bench", label: "Has shelter with bench" },
    { value: "has_bench", label: "Has bench" },
  ];
  onMount(async () => {
    data = await fetch("./output_paths_with_data.geojson").then((res) =>
      res.json()
    );
    distances = data.features.map((d) => d.properties.distance);
    numSeniors = data.features.map((d) => d.properties["Age 65+ Total"]);
    distanceLimits = [0, Math.max(...distances)];
    numSeniorsLimit = [0, Math.max(...numSeniors)];    
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
  function setNumSeniorsLimit(range: [number, number]) {
    numSeniorsLimit = range || [0, Math.max(...numSeniors)];
  }
  $: mapData = data?.features.filter((d) => {
    return (
      d.properties.distance >= distanceLimits[0] &&
      d.properties.distance <= distanceLimits[1] &&
      d.properties["Age 65+ Total"] >= numSeniorsLimit[0] &&
      d.properties["Age 65+ Total"] <= numSeniorsLimit[1]
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
    <div class="flex">
      {#if distances}
        <Histogram
          data={distances}
          label="Distance →"
          onUpdate={setDistanceLimit}
        />
      {/if}
      {#if numSeniors}
        <Histogram
          data={numSeniors}
          label="Num. Seniors →"
          onUpdate={setNumSeniorsLimit}
        />
      {/if}
    </div>
  </form>
  <div class="h-[calc(100vh-250px)]">
    <Leaflet view={initialView} zoom={11}>
      {#if mapData}
        {#each mapData as building (building.properties.id)}
          {#if displayBuildings}
            <Marker
              latLng={[
                +building.properties.latitude,
                +building.properties.longitude,
              ]}
              iconUrl="apartment.svg"
              iconSize={[15, 100]}
            >
              <Popup>Building ID: {building.properties.Address}</Popup>
            </Marker>
          {/if}
          {#if displayStations}
            <Marker
              latLng={[
                +building.properties.stop_lat,
                +building.properties.stop_lon,
              ]}
              radius={4}
              fillColor="red"
            >
              <Popup>Stop: {building.properties.stop_name}</Popup>
            </Marker>
          {/if}
          {#if displayRoutes}
            <PolyLine
              latLngs={building.geometry.coordinates.map((d) => [+d[1], +d[0]])}
            />
          {/if}
        {/each}
      {/if}
    </Leaflet>
  </div>
</div>
