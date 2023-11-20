<script lang="ts">
  import { onMount, createEventDispatcher, onDestroy } from "svelte";

  $: sortOrder = -1;
  let maxHeight = "400px";

  export let items = [];
  export let sortBy = "";

  const handleClick = (key: string) => {
    if (sortBy === key) sortOrder *= -1;
    else $: sortBy = key;
  };

  $: tableData = [...items].sort((a, b) => {
    if (a[sortBy] > b[sortBy]) return sortOrder;
    if (a[sortBy] < b[sortBy]) return -sortOrder;
    return 0;
  });
  function downloadCSV() {
    const header = Object.keys(tableData[0]).join(",") + "\n";
    const csv =
      header + tableData.map((obj) => Object.values(obj).join(",")).join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "data.csv");
    document.body.appendChild(link);
    link.click();

    // Clean up
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
</script>

<div class="mb-10">
  {#if tableData && tableData.length > 0}
    <div class="border-t-2 mt-2 py-2 flex justify-between">
      <div>
        The table below shows each NORC, filtered by the controls above
        (currently <strong>{tableData.length} rows</strong>). Click column headers to sort (currently
        <em>{sortBy}</em>).
      </div>
      <button class="whitespace-nowrap" on:click={downloadCSV}
        >Download table</button
      >
    </div>
    <div
      class="border-gray mt-1 overflow-x-auto"
      style="max-height: {maxHeight};"
    >
      <table class="min-w-full">
        <!-- Table Headers -->
        <thead class="sticky top-0 bg-white">
          <tr>
            {#each Object.keys(tableData[0]) as key (key)}
              <th
                class="cursor-pointer px-1 py-1 truncate select-none"
                on:click={() => handleClick(key)}
              >
                <div class="flex items-center">
                  {#if key === sortBy && sortOrder === 1}
                    <svg
                      class="w-4 h-4 ml-1 text-gray-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M5 15l7-7 7 7"
                      />
                    </svg>
                  {:else if key === sortBy && sortOrder === -1}
                    <svg
                      class="w-4 h-4 ml-1 text-gray-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  {:else}
                    <svg
                      class="w-4 h-4 ml-1 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 8h16M4 16h16"
                      />
                    </svg>
                  {/if}
                  {key}
                </div>
              </th>
            {/each}
          </tr>
        </thead>
        <!-- Table Body -->
        <tbody>
          {#each tableData as item}
            <tr>
              {#each Object.values(item) as value}
                <td class="border px-1 py-1 truncate" style="max-width: 240px"
                  >{value}</td
                >
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  /* Add tailwind classes or custom styles here */
  th {
    position: sticky;
    top: 0;
    z-index: 1;
  }
</style>
