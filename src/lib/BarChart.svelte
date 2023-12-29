<script lang="ts">
  interface dataElement {
    y: string;
  }

  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  export let data: dataElement[];
  export let handleClick: (e: any) => void = (e) => null;
  export let marginLeft = 300;
  export let width = 330;
  export let height = 60;
  export let title = "";
  export let fill = "black";
  export let selected = "";
  const ariaLabel = (v: any) => v[0];
  $: opacity = (v: any) => (!selected ? 1 : v[0] === selected ? 1 : 0.2);
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
            ariaLabel,
            opacity,
          },
          {
            y: "y",
            fill,
            ariaLabel: (d) => d.y,
            opacity: (d) => d.y,
            sort: {
              y: "x",
              reverse: true,
            },
          }
        )
      ),
      Plot.text(
        data,
        Plot.groupY(
          {
            x: "count",
            text: "count",
            ariaLabel,
          },
          {
            y: "y",
            ariaLabel: "y",
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
    y: {
      label: null,
    },
    width,
    height,
    marginTop: 0,
    marginBottom: 0,
    style: {
      cursor: "pointer",
      userSelect: "none",
    },
  }}
/>
