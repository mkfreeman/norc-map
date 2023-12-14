<script>
  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  import * as d3 from "d3";
  export let data;
  export let y = "amenity";
  export let handleClick;
  export let marginLeft = 300;
  export let width = 330;
  export let height = 60;
  export let title = "";
  export let selected = "";
  const getY = (d) => (d.properties && d.properties[y]) || "None";
</script>

<PlotWrapper
  {handleClick}
  options={{
    marks: [
      Plot.text([title], {
        frameAnchor: "top",
        textAnchor: "end",
        fontSize: 12,
        dx: 0,
        dy: -10,
      }),
      Plot.barX(
        data,
        Plot.groupY(
          {
            x: "count",
            ariaLabel: (v) => v[0],
            opacity: (v) => (!selected ? 1 : v[0] === selected ? 1 : 0.2),
          },
          {
            y: getY,
            fill: getY,
            ariaLabel: getY,
            sort: {
              y: "x",
              reverse: true,
            },
            opacity: getY,
          }
        )
      ),
      Plot.text(
        data,
        Plot.groupY(
          {
            x: "count",
            text: "count",
          },
          {
            y: getY,
            dx: 2,
            textAnchor: "start",
            sort: {
              y: "x",
              reverse: true,
            },
          }
        )
      ),
    ],
    marginLeft,
    marginRight: 20,
    x: {
      label: null,
      axis: null,
    },
    width,
    height,
    marginTop: 0,
    marginBottom: 0,
    color: {
      range: d3.schemeBlues[9].slice(3, 7),
      reverse: true,
      domain: [
        "Shelter With Bench Underneath",
        "None",
        "Bench only",
        "Shelter Without Bench",
      ],
    },
    style: {
      cursor: "pointer",
    },
  }}
/>
