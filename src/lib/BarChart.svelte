<script>    
  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  export let data;
  export let getX = (d) => d.x;
  export let getY = (d) => d.y;
  export let getZ = (d) => d.z;
  export let getFill = (d) => d.fill;
  export let marginLeft = 300;
  export let width = 600;
  export let title = ""


</script>

<PlotWrapper
  options={{
    marks: [
      Plot.barX(
        data,
        Plot.stackX({
          ...Plot.groupY(
            { x: "sum", reverse: true },
            {
              y: getY,
              x: getX,
              z: getZ,
              sort: { y: "x", limit: 40, reverse: true },
              stroke: "white",
              fill: getFill,
              channels: {
                NORC: (d) => d[0].properties.Address,
                "Has bench or shelter": (d) =>
                  d[0].properties.has_shelter_with_bench ||
                  d[0].properties.has_bench ||
                  d[0].properties.has_shelter,
              },
              order: "x",
              tip: {
                format: {
                  NORC: true,
                  y: false,
                  fill: false,
                },
              },
            }
          ),
          reverse: true,
        })
      ),
    ],
    x: {
      label: "Number of seniors served",
    },
    marginLeft,
    width,
    marginTop: -5,
    title,
    color: {
      legend: true,
      range: ["rgb(104,175,252)", "rgb(164 114 244)"],
      domain: [true, false],
    },
  }}
/>
