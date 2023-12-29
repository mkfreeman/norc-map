<script lang="ts">
  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  export let data;
  export let handleClick;
  export let selected:string | undefined;
  export let label:string;
  export let prop:string;
</script>

<div class="mx-1">
  <PlotWrapper
    {handleClick}
    options={{
      width: 200,
      marginTop: 10,
      color: {
        range: ["rgb(104,175,252)", "rgb(164 114 244)"],
        domain: prop === "wheelchair_boarding" ? ["Some", "None"]: ["true", "false"],
      },
      marks: [
        Plot.barX(
          data,
          Plot.groupY(
            {
              x: "count",
              ariaLabel: (v) => v[0][prop],
              stroke: (v) =>
                `${v[0][prop]}` === selected ? "black" : "none",
              fillOpacity: (v) =>
                !selected
                  ? 0.8
                  : `${v[0][prop]}` === selected
                    ? 1
                    : 0.5,
            },
            {
              y: (d) => 1,
              fill: (d) => `${d[prop]}`,
            }
          )
        ),
        Plot.text([label], {
          frameAnchor: "top",
          textAnchor: "start",
          fontSize: 12,
          dx: -98,
          dy: -10,
        }),
        Plot.textX(
          data,
          Plot.stackX(
            Plot.groupZ(
              {
                x: "count",
                text: (v) => v[0][prop],
                id: (v) => v[0].id,
                ariaLabel: (v) => v[0],
              },
              {
                z: (d) => d[prop],
                inset: 0.5,
                textAnchor: "middle",
                id: (d) => d[prop],
                ariaLabel: (d) => d[prop],
              }
            )
          )
        ),
      ],
      marginBottom: 0,
      x: { label, axis: null },
      y: { axis: null },
      height: 55,
      style: { cursor: "pointer" },
    }}
  />
</div>
