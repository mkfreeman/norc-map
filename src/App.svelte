<script lang="ts">
  import { onMount } from "svelte"
  import Leaflet from './lib/Leaflet.svelte'
  import Marker from './lib/Marker.svelte'
  import type { LatLngExpression } from 'leaflet';
  const initialView: LatLngExpression = [43.651070, -79.397015];
  import * as d3 from "d3";
	let data;
  onMount(
		async () => {
      // TODO: filter down to pre-set bounds
			data = await d3.csv('./stops.txt')
		}
	)
</script>

<div class="w-full h-screen">
  <Leaflet view={initialView} zoom={14}>
    {#if data}
      {#each data as stop}
        <Marker latLng={[+stop.stop_lat, +stop.stop_lon]} width={20} height={20}>
          <div class="bg-black w-3 h-3 rounded-full"></div>
        </Marker>
      {/each}
    {/if}
    </Leaflet>

</div>
  

