<script lang="ts">
  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  export let data;
  export let handleClick;
  export let selected;
  export let label;
  export let prop;

  $: console.log(selected);
</script>

<div class="mx-1">
  <PlotWrapper
    {handleClick}
    options={{
      width: 200,
      marginTop: 10,
      color: {        
        range: ["rgb(104,175,252)", "rgb(164 114 244)"]
      },
      marks: [
        Plot.barX(
          data.features,
          Plot.groupY(
            {
              x: "count",
              ariaLabel: (v) => v[0].properties[prop],
              fillOpacity: (v) =>
                !selected
                  ? 0.8
                  : `${v[0].properties[prop]}` === selected
                  ? 1
                  : 0.5,
            },
            {
              y: (d) => 1,
              fill: (d) => d.properties[prop],
            }
          )
        ),
        Plot.text([label], {
          frameAnchor: "top",
          textAnchor: "start",
          fontSize: 12,
          dx: -70,
          dy: -10,
        }),
        Plot.textX(
          data.features,
          Plot.stackX(
            Plot.groupZ(
              {
                x: "count",
                text: (v) => v[0].properties[prop],
                id: (v) => v[0].id,
                ariaLabel: (v) => v[0],
              },
              {
                z: (d) => d.properties[prop],
                inset: 0.5,
                textAnchor: "middle",
                id: (d) => d.properties[prop],
                ariaLabel: (d) => d.properties[prop],
              }
            )
          )
        ),
      ],
      marginBottom: 10,
      x: { label, axis: null },
      y: { axis: null },
      height: 50,
      style: { cursor: "pointer" },
    }}
  />
</div>
