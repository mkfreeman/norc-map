<script lang="ts">
  import { onMount } from "svelte";
  import {
    scaleLinear,
    select,
    axisBottom,
    axisLeft,
    bin,
    brushX,
    extent,
    format,
    type D3BrushEvent,
  } from "d3";

  interface tf {
    (n: number): string;
  }
  export let data: number[] = Array.from({ length: 100 }, (_, i) => i);
  export let width = 200;
  export let height = 75;
  export let tickFormat = format(".2s");
  export let onUpdate: (e: any) => void = (e) => null;
  export let label = "Value →"; // Default x-axis label with arrow pointing right
  let el: HTMLDivElement;
  onMount(() => {
    const margin = { top: 15, right: 30, bottom: 30, left: 30 };

    const svg = select(el)
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    const x = scaleLinear()
      .domain(extent(data) as [number, number])
      .range([margin.left, width - margin.right])
      .nice();

    const histogramData = bin()
      .domain(x.domain() as [number, number])
      .thresholds(x.ticks(20))(data);

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
      .attr("x", (d) => x(d.x0 ? d.x0 : 0) + 1)
      .attr("width", (d) => Math.max(0, x(d.x1!) - x(d.x0!) - 1))
      .attr("y", (d) => y(d.length))
      .attr("height", (d) => y(0) - y(d.length))
      .attr("fill", "rgb(104,175,252)")
      .attr("fill-opacity", 0.8);

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
      .attr("x", 2)
      .attr("y", 9)
      .attr("text-anchor", "start")
      .attr("font-size", "12px")
      .style("font-family", "system-ui, sans-serif")
      .text(label);

    svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(axisBottom(x).ticks(4).tickFormat(tickFormat));

    svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(axisLeft(y).ticks(2));

    function brushed(event: D3BrushEvent<any>) {
      if (event.selection) {
        const [x0, x1] = event.selection as [number, number];
        bars.attr("fill-opacity", (d) => {
          const barX = x(d.x0!) + 1;
          return barX >= x0 && barX <= x1 ? 1 : 0.3;
        });
        if (onUpdate) {
          onUpdate([x.invert(x0), x.invert(x1)]); // Call the provided onUpdate function with selected range
        }
      }
    }

    function brushEnded(event: D3BrushEvent<any>) {
      if (!event.selection) {
        bars.attr("fill-opacity", 1); // Reset all bars to original opacity when brush is cleared
        if (onUpdate) {
          onUpdate(null); // Notify that brush has been cleared
        }
      }
    }
  });
</script>

<div bind:this={el} class="histogram mx-1" />

<style>
  .histogram {
    font-family: Arial, sans-serif;
  }
</style>
