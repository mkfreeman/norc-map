<script lang="ts">
  import { onMount, onDestroy, getContext } from "svelte";
  import L from "leaflet";

  let popup: L.Popup | undefined;
  let popupElement: HTMLElement;
  let isOpen = false;
  export let startOpen = false;

  const { getLayer }: { getLayer: () => L.Layer | undefined } =
    getContext("layer");
  const layer = getLayer();

  onMount(() => {
    popup = L.popup().setContent(popupElement);
    if (layer) {
      layer.bindPopup(popup);
      layer.on("popupopen", () => (isOpen = true));
      layer.on("popupclose", () => (isOpen = false));
      if (startOpen) layer?.openPopup();
    }
  });

  $: {
    if (startOpen && layer) layer?.openPopup();
    else if (layer) layer.closePopup();
  }

  onDestroy(() => {
    layer?.unbindPopup();
    popup?.remove();
    popup = undefined;
  });
</script>

<div use={startOpen} bind:this={popupElement}>
  {#if isOpen}
    <slot />
  {/if}
</div>
