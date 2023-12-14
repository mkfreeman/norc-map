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

  interface dataObj {
    properties: {
      id: number;
      wheelchair_boarding: "Some" | "None";
      Address: string;
      "Age 65+ Total": number;
      "% of Seniors": number;
      amenity: string;
      source: string;
      stop_name: string;
      stop_lat: number;
      stop_lon: number;
      distance: number;
      latitude: number;
      longitude: number;
    };
    geometry: {
      coordinates: number[][];
    };
  }
  interface dataJson {
    features: dataObj[];
    type: "FeatureCollection";
    crs: {
      type: "name";
      properties: {
        name: string;
      };
    };
  }
  type filterProp =
    | "wheelchair_boarding"
    | "amenity"
    | "distance"
    | "Age 65+ Total"
    | "% of Seniors";
  interface filterObj {
    prop: filterProp;
    value: string | number[];
  }

  interface histogramOption {
    prop: "distance" | "Age 65+ Total" | "% of Seniors" | "% of Seniors";
    label: string;
    tickFormat: (n: number) => string;
  }

  let initialView: LatLngExpression = [43.70107, -79.397015];
  let view: LatLngExpression;
  let zoom: number = 11;
  let displayStations = true;
  let displayRoutes = true;
  let displayBuildings = true;
  let data: dataJson;
  let selectedIndex: number;
  let filters: filterObj[] = [];

  const histogramOptions: histogramOption[] = [
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
    data = await fetch("./norcs_with_closest_stops_merged_new.geojson").then(
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
  function getStreetViewUrl(lat: number, lng: number) {
    return `http://maps.google.com/maps?q=&layer=c&cbll=${lat},${lng}&cbp=11,0,0,0,0`;
  }

  // Data filters
  $: mapData = data?.features.filter((d: dataObj) => {
    return filters.every((f: filterObj) => {
      return typeof f.value === "string"
        ? `${d.properties[f.prop]}` == (f.value === "None" ? "null" : f.value)
        : Array.isArray(f.value)
          ? +d.properties[f.prop] >= f.value[0] &&
            +d.properties[f.prop] <= f.value[1]
          : false;
    });
  });

  // Click functionality for zooming the map
  $: view = selectedIndex
    ? [
        mapData[selectedIndex + 1].properties.latitude, // TODO: 0 index the id
        mapData[selectedIndex + 1].properties.longitude,
      ]
    : initialView;
  $: zoom = selectedIndex ? 14 : 11;

  function toggleFilter(prop: filterProp, value: string | number[]) {
    if (
      filters.find(
        (f) => f.prop === prop && (f.value === value || value === null)
      )
    ) {
      filters = filters.filter((f) => f.prop !== prop);
    } else {
      filters = [...filters.filter((f) => f.prop !== prop), { prop, value }];
    }
  }
  function getPopupContent(building: dataObj) {
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
      <em>Amenity</em>: ${building.properties.amenity || "None"}<br/>
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
      <ToggleChart
        prop={"wheelchair_boarding"}
        label={"Wheelchair boarding"}
        selected={filters.find((d) => d.prop === "wheelchair_boarding")?.value}
        {data}
        handleClick={(event) =>
          !event.target.ariaLabel
            ? null
            : toggleFilter("wheelchair_boarding", event.target.ariaLabel)}
      />
      <BarChart
        data={data.features}
        y={"amenity"}
        marginLeft={200}
        width={300}
        selected={filters.find((d) => d.prop === "amenity")?.value.toString()}
        handleClick={(event) =>
          !event.target.ariaLabel
            ? null
            : toggleFilter("amenity", event.target.ariaLabel)}
      />
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
                <Popup startOpen={index + 1 === selectedIndex}
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
      items={mapData.map((d) => ({
        ...d.properties,
        "% of Seniors": d3.format(".1%")(d.properties["% of Seniors"]),
      }))}
      sortBy="Distance"
      rowClick={(row) =>
        selectedIndex === row.id
          ? (selectedIndex = null)
          : (selectedIndex = row.id)}
      selectedRow={selectedIndex}
    />
  {/if}
  <div>
    <h1 class="flex pb-0 pt-2 text-2xl border-t">Stops</h1>
    <p class="text-start m0">
      <em>Top 40 stops by number of seniors served, by amenity</em>
    </p>
    {#if mapData}
      <PlotWrapper
        options={{
          width: 900,
          marginLeft: 300,
          inset: 2,
          fx: {
            domain: [
              "Shelter With Bench Underneath",
              "Shelter Without Bench",
              "Bench only",
              "None",
            ],
          },
          marks: [
            Plot.frame(),
            Plot.barX(mapData, {
              x: (d) => d.properties["Age 65+ Total"],
              y: (d) => d.properties["stop_name"],
              fx: (d) => d.properties.amenity || "None",

              channels: {
                NORC: (d) => d.properties.Address,
                "Num. Seniors": (d) => d.properties["Age 65+ Total"],
              },
              tip: {
                format: {
                  y: false,
                  fx: false,
                  x: false,
                },
              },
              stroke: "white",
              fill: (d) => d.properties.amenity || "None",
              sort: {
                y: "x",
                reverse: true,
                limit: 40,
              },
            }),
          ],
          color: {
            range: d3.schemeBlues[9].slice(3, 7),
            reverse: true,
            domain: [
              "Shelter With Bench Underneath",
              "Shelter Without Bench",
              "Bench only",
              "None",
            ],
          },
          style: {
            width: "90%",
          },
        }}
      />
    {/if}
  </div>
</div>
