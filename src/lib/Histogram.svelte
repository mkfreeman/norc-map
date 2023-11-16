<script>
  import { onMount } from "svelte";
  import {
    scaleLinear,
    select,
    axisBottom,
    axisLeft,
    bin,
    brushX,
    extent,
  } from "d3";

  export let data = Array.from({ length: 100 }, (_, i) => i);
  export let width = 400;
  export let height = 75;
  export let onUpdate = null;
  export let label = "Value →"; // Default x-axis label with arrow pointing right

  onMount(() => {
    const margin = { top: 10, right: 30, bottom: 30, left: 30 };

    const svg = select(".histogram")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    const x = scaleLinear()
      .domain(extent(data))
      .range([margin.left, width - margin.right]);

    const histogramData = bin().domain(x.domain()).thresholds(x.ticks(20))(
      data
    );

    const maxBinCount = Math.max(...histogramData.map((d) => d.length));

    const y = scaleLinear()
      .domain([0, maxBinCount])
      .nice()
      .range([height - margin.bottom, margin.top]);

    const bars = svg
      .selectAll("rect")
      .data(histogramData)
      .enter()
      .append("rect")
      .attr("x", (d) => x(d.x0) + 1)
      .attr("width", (d) => Math.max(0, x(d.x1) - x(d.x0) - 1))
      .attr("y", (d) => y(d.length))
      .attr("height", (d) => y(0) - y(d.length))
      .attr("fill", "#69b3a2")
      .attr("fill-opacity", 1);

    const brush = brushX()
      .extent([
        [margin.left, margin.top],
        [width - margin.right, height - margin.bottom],
      ])
      .on("brush", brushed)
      .on("end", brushEnded);

    svg.append("g").attr("class", "brush").call(brush);

    svg
      .append("text") // X-axis label
      .attr("x", width - margin.right)
      .attr("y", height - 5)
      .attr("text-anchor", "end")
      .attr("font-size", "10px")
      .text(label);

    svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(axisBottom(x));

    svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(axisLeft(y).ticks(1));

    function brushed(event) {
      if (event.selection) {
        const [x0, x1] = event.selection;
        bars.attr("fill-opacity", (d) => {
          const barX = x(d.x0) + 1;
          return barX >= x0 && barX <= x1 ? 1 : 0.3;
        });
        if (onUpdate) {
          onUpdate([x.invert(x0), x.invert(x1)]); // Call the provided onUpdate function with selected range
        }
      }
    }

    function brushEnded(event) {
      if (!event.selection) {
        bars.attr("fill-opacity", 1); // Reset all bars to original opacity when brush is cleared
        if (onUpdate) {
          onUpdate(null); // Notify that brush has been cleared
        }
      }
    }
  });
</script>

<div class="histogram" />

<style>
  .histogram {
    font-family: Arial, sans-serif;
  }
</style>
