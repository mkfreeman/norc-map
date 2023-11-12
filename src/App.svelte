<script lang="ts">
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from '/vite.svg'
  import Counter from './lib/Counter.svelte'
  import Leaflet from './lib/Leaflet.svelte'
  import type { LatLngExpression } from 'leaflet';
  const initialView: LatLngExpression = [43.651070, -79.347015]; // Dortmund, Germany
</script>

<div class="w-full h-screen">
  <Leaflet view={initialView} zoom={13}/>
</div>
  

