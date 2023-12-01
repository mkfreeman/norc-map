<script lang="ts">
  import { onMount } from "svelte";
  import Leaflet from "./lib/Leaflet.svelte";
  import Marker from "./lib/Marker.svelte";
  import ToggleChart from "./lib/ToggleChart.svelte";
  import Popup from "./lib/Popup.svelte";
  import Histogram from "./lib/Histogram.svelte";
  import PolyLine from "./lib/PolyLine.svelte";
  import Checkbox from "./lib/Checkbox.svelte";
  import Table from "./lib/Table.svelte";
  import type { LatLngExpression } from "leaflet";
  import * as d3 from "d3";

  const initialView: LatLngExpression = [43.70107, -79.397015];
  let displayStations = true;
  let displayRoutes = true;
  let displayBuildings = true;
  let distances: number[];
  let numSeniors: number[];
  let data;
  let filters = [];
  const filterOptions = [
    { prop: "wheelchair_boarding", label: "Wheelchair boarding" },
    { prop: "has_shelter", label: "Has shelter" },
    { prop: "has_shelter_with_bench", label: "Has shelter with bench" },
    { prop: "has_bench", label: "Has bench" },
  ];

  onMount(async () => {
    data = await fetch("./output_paths_with_data.geojson").then((res) =>
      res.json()
    );
    distances = data.features.map((d) => d.properties.distance);
    numSeniors = data.features.map((d) => d.properties["Age 65+ Total"]);
  });
  // Map element visibility
  function toggleStations() {
    displayStations = !displayStations;
  }
  function toggleRoutes() {
    displayRoutes = !displayRoutes;
  }
  function toggleBuildings() {
    displayBuildings = !displayBuildings;
  }

  // Data filters
  $: mapData = data?.features.filter((d) => {
    return filters.every((f) => {
      return typeof f.value === "string"
        ? `${d.properties[f.prop]}` == f.value
        : Array.isArray(f.value)
        ? d.properties[f.prop] >= f.value[0] &&
          d.properties[f.prop] <= f.value[1]
        : false;
    });
  });

  function toggleFilter(prop, value) {
    if (
      filters.find(
        (f) => f.prop === prop && (f.value === value || value === null)
      )
    ) {
      $: filters = filters.filter((f) => f.prop !== prop);
    } else {
      $: filters = [...filters.filter((f) => f.prop !== prop), { prop, value }];
    }
  }
  function getPopupContent(building) {
    return `
      <em>Building: </em><a target="_blank" href="http://maps.google.com/maps?q=&layer=c&cbll=${building.properties.latitude},${building.properties.longitude}&cbp=11,0,0,0,0">${building.properties.Address}</a><br/>
      <em>Stop</em>: <a target="_blank" href="http://maps.google.com/maps?q=&layer=c&cbll=${building.properties.stop_lat},${building.properties.stop_lon}&cbp=11,0,0,0,0">${building.properties.stop_name}</a><br/>
      <em>Distance</em>: ${building.properties.distance}m
    `;
  }
</script>

<div class="w-full">
  <h1 class="flex pb-0 text-2xl">Naturally Occuring Retirement Communities</h1>
  <p class="text-start border-b"><em>Use the controls below to explore the data in the map and table.</em></p>
  {#if data}
    <div class="flex flex-wrap mt-3">
      {#each filterOptions as option}
        <ToggleChart
          prop={option.prop}
          label={option.label}
          selected={filters.find((d) => d.prop === option.prop)?.value}
          {data}
          handleClick={(event) =>
            !event.target.ariaLabel
              ? null
              : toggleFilter(option.prop, event.target.ariaLabel)}
        />
      {/each}
      {#if distances}
        <Histogram
          data={distances}
          label="Distance →"
          onUpdate={(range) => toggleFilter("distance", range)}
        />
      {/if}
      {#if numSeniors}
        <Histogram
          data={numSeniors}
          label="Num. Seniors →"
          onUpdate={(range) => toggleFilter("Age 65+ Total", range)}
        />
      {/if}
    </div>
  {/if}
  <div class="flex">
    <div style="width: 80px;">
      <form class="flex flex-wrap">
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
      </form>
    </div>
    <div class="w-[calc(100%-80px)] h-[calc(50vh)]">
      <Leaflet view={initialView} zoom={11}>
        {#if mapData}
          {#each mapData as building (building.properties.id)}
            {#if displayBuildings}
              <Marker
                latLng={[
                  +building.properties.latitude,
                  +building.properties.longitude,
                ]}
                radius={4}
                fillColor="black"
              >
                <Popup>{@html getPopupContent(building)}</Popup>
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
                <Popup>{@html getPopupContent(building)}</Popup>
              </Marker>
            {/if}
            {#if displayRoutes}
	    {#if building.geometry}
              <PolyLine
                latLngs={building.geometry.coordinates.map((d) => [
                  +d[1],
                  +d[0],
                ])}
              >
                <Popup>{@html getPopupContent(building)}</Popup>
              </PolyLine>
            {/if}
	    {/if}
          {/each}
        {/if}
      </Leaflet>
    </div>
  </div>
  {#if mapData}
    <Table
      items={mapData.map((d) => ({
        Address: d.properties.Address,
        "Nearest Stop": d.properties.stop_name,
        Distance: +d.properties.distance,
        "# Seniors": d.properties["Age 65+ Total"],
        "# People": d.properties.All_Persons,
        "% seniors": d3.format(".1%")(d.properties["% of Seniors"]),
        "Wheelchair Boarding": d.properties.wheelchair_boarding,
        "Has Shelter": d.properties.has_shelter,
        "Shelter + Bench": d.properties.has_shelter_with_bench,
        "Has Bench": d.properties.has_bench,
      }))}
      sortBy="Distance"
    />
  {/if}
</div>
