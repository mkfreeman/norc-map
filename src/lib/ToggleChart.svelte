<script lang="ts">
  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  type dataObj = { category: string };
  export let data: dataObj[];
  export let handleClick: (e: any) => void = (e) => null;
  export let selected: string | undefined;
  export let label: string;
  const ariaLabel = (v: dataObj[]) => v[0].category;
  const text = (v: string[]) => v[0];
  $: stroke = (v: dataObj[]) =>
    `${v[0].category}` === selected ? "black" : "none";
  const fillOpacity = (v: dataObj[]) =>
    !selected ? 0.8 : `${v[0].category}` === selected ? 1 : 0.5;
</script>

<div class="mx-1">
  <PlotWrapper
    {handleClick}
    options={{
      width: 200,
      marginTop: 10,
      color: {
        range: ["rgb(104,175,252)", "rgb(164 114 244)"],
        domain: ["Some", "None"],
      },
      marks: [
        Plot.barX(
          data,
          Plot.groupY(
            {
              x: "count",
              ariaLabel,
              stroke,
              fillOpacity,
            },
            {
              y: (d) => 1,
              fill: "category",
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
                text,
                ariaLabel,
              },
              {
                text: "category",
                z: "category",
                inset: 0.5,
                textAnchor: "middle",
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
