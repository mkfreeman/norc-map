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
  import PlotWrapper from "./lib/PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  import BarChart from "./lib/BarChart.svelte";
  import CellChart from "./lib/CellChart.svelte";

  let initialView: LatLngExpression = [43.70107, -79.397015];
  let zoom: number = 11;
  let displayStations = true;
  let displayRoutes = true;
  let displayBuildings = true;
  let data;
  let currentZoom: LatLngExpression;
  let selectedIndex: number;
  let filters = [];
  const filterOptions = [
    { prop: "wheelchair_boarding", label: "Wheelchair boarding" },
    { prop: "has_shelter", label: "Has shelter" },
    { prop: "has_shelter_with_bench", label: "Has shelter with bench" },
    { prop: "has_bench", label: "Has bench" },
  ];

  const histogramOptions = [
    { prop: "distance", label: "Distance", tickFormat: d3.format(".2s") },
    {
      prop: "Age 65+ Total",
      label: "Num. Seniors",
      tickFormat: d3.format(".2s"),
    },
    {
      prop: "% of Seniors",
      label: "Pct. Seniors",
      tickFormat: d3.format(".0%"),
    },
  ];

  onMount(async () => {
    data = await fetch("./norcs_with_closest_stops_merged.geojson").then(
      (res) => res.json()
    );
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

  // url generation based on this answer: https://stackoverflow.com/questions/387942/google-street-view-url
  function getStreetViewUrl(lat, lng) {
    return `http://maps.google.com/maps?q=&layer=c&cbll=${lat},${lng}&cbp=11,0,0,0,0`;
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

  // Click functionality for zooming the map
  $: view = selectedIndex
    ? [
        mapData[selectedIndex].properties.latitude,
        mapData[selectedIndex].properties.longitude,
      ]
    : initialView;
  $: zoom = selectedIndex ? 14 : 11;

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
      <em>Building: </em><a target="_blank" href="${getStreetViewUrl(
        building.properties.latitude,
        building.properties.longitude
      )}">${building.properties.Address}</a><br/>
      <em>Pct. Seniors: </em>${d3.format(".1%")(
        building.properties["% of Seniors"]
      )}<br/>
<em>Stop</em>: <a target="_blank" href="${getStreetViewUrl(
      building.properties.stop_lat,
      building.properties.stop_lon
    )}">${building.properties.stop_name}</a><br/>
      <em>Distance</em>: ${building.properties.distance}m<br/>
      <em>Source</em>: ${building.properties.source}
    `;
  }
</script>

<div class="w-full">
  <h1 class="flex pb-0 text-2xl">Naturally Occuring Retirement Communities</h1>
  <p class="text-start border-b">
    <em>Use the controls below to explore the data in the map and table.</em>
  </p>
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
    </div>
    <div class="flex flex-wrap mt-3">
      {#each histogramOptions as option}
        <Histogram
          data={data.features.map((d) => d.properties[option.prop])}
          label={`${option.label} →`}
          onUpdate={(range) => toggleFilter(option.prop, range)}
          tickFormat={option.tickFormat}
        />
      {/each}
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
      <Leaflet {view} {zoom}>
        {#if mapData}
          {#each mapData as building, index (building.properties.id)}
            {#if displayBuildings}
              <Marker
                latLng={[
                  +building.properties.latitude,
                  +building.properties.longitude,
                ]}
                radius={4}
                fillColor="black"
              >
                <Popup startOpen={index === selectedIndex}
                  >{@html getPopupContent(building)}</Popup
                >
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
      items={mapData.map((d, index) => ({
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
        latitude: +d.properties.latitude,
        longitude: +d.properties.longitude,
        index,
      }))}
      sortBy="Distance"
      rowClick={(row) =>
        selectedIndex === row.index
          ? (selectedIndex = null)
          : (selectedIndex = row.index)}
      selectedRow={selectedIndex}
    />
  {/if}
  <h1 class="flex pb-0 pt-2 text-2xl border-t">Stops</h1>
  <p class="text-start m0"><em>Top 40 stops by number of seniors served</em></p>
  {#if data}
    <div class="flex">
      <BarChart
        data={data.features}
        getY={(d) => `${d.properties.stop_name} (#${d.properties.id})`}
        getX={(d) => d.properties["Age 65+ Total"]}
        getZ={(d) => d.properties.Address}
        getFill={(d) => d.properties.has_shelter_with_bench}
        title="Has shelter with bench"
      />
      <BarChart
        data={data.features}
        getY={(d) => `${d.properties.stop_name} (#${d.properties.id})`}
        getX={(d) => d.properties["Age 65+ Total"]}
        getZ={(d) => d.properties.Address}
        getFill={(d) => d.properties.has_shelter}
        marginLeft={0}
        width={300}
        title={"Has shelter"}
      />
      <BarChart
        data={data.features}
        getY={(d) => `${d.properties.stop_name} (#${d.properties.id})`}
        getX={(d) => d.properties["Age 65+ Total"]}
        getZ={(d) => d.properties.Address}
        getFill={(d) => d.properties.has_bench}
        marginLeft={0}
        width={300}
        title={"Has bench only"}
      />
    </div>
  {/if}
  {#if data}
    <div class="flex mb-16">
      <CellChart
        data={data.features}
        x="has_shelter"
        y="has_shelter_with_bench"
      />
      <CellChart data={data.features} x="has_shelter" y="has_bench" />
      <CellChart
        data={data.features}
        x="has_shelter_with_bench"
        y="has_bench"
      />
    </div>
  {/if}
</div>
