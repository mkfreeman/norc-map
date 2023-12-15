<script>
  import PlotWrapper from "./PlotWrapper.svelte";
  import * as Plot from "@observablehq/plot";
  export let x = "has_bench";
  export let y = "has_shelter";
  export let data;
</script>

<PlotWrapper
  options={{
    marks: [
      Plot.cell(
        data,
        Plot.group(
          { fill: "count", text: "count" },
          {
            x: (d) => d[x],
            y: (d) => d[y],
            tip: true,
          }
        )
      ),
      Plot.text(
        data,
        Plot.group(
          { text: "count" },
          {
            x: (d) => d[x],
            y: (d) => d[y],
            fill: "white",
            stroke: "black",
          }
        )
      ),
    ],
    x: {
      label: x.replaceAll("_", " "),
      domain: [false, true],
    },
    y: {
      label: y.replaceAll("_", " "),
      domain: [true, false],
    },
    color: {
      scheme: "blues",
    },
    marginLeft: 60,
    width: 200,
    marginTop: 80,
    marginBottom: 50,
    style: { fontSize: "14px" },
  }}
></PlotWrapper>
