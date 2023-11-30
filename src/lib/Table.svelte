<script lang="ts">
  import { onMount, createEventDispatcher, onDestroy } from "svelte";

  $: sortOrder = -1;
  let maxHeight = "400px";

  export let items = [];
  export let sortBy = "";
  export let selectedRow;
  export let searchTerm = "";
  export let rowClick = () => {};
  const handleClick = (key: string) => {
    if (sortBy === key) sortOrder *= -1;
    else $: sortBy = key;
  };

  $: tableData = [...items]
    .filter((item) =>
      Object.values(item)
        .filter((d) => typeof d === "string")
        .join(" ")
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
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
  <div class="border-t mt-2 pt-2 flex justify-between text-start">
    <div>
      NORCs filtered by the controls above and search below (currently <strong
        >{tableData.length} rows</strong
      >). Click column headers to sort (currently
      <em>{sortBy}.</em>). Click a row to zoom the map.
    </div>
    <div>
      <button
        on:click={downloadCSV}
        type="button"
        class="py-2.5 px-5 me-2
      text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg
      border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10
      focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800
      dark:text-gray-400 dark:border-gray-600 dark:hover:text-white
      dark:hover:bg-gray-700 whitespace-nowrap">Download Table</button
      >
    </div>
  </div>
  <form class="flex mb-2">
    <label
      for="default-search"
      class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white"
      >Search stops or buildings</label
    >
    <div class="relative w-60">
      <div
        class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none"
      >
        <svg
          class="w-4 h-4 text-gray-500 dark:text-gray-400"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 20 20"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
      </div>
      <input
        on:input={(event) => (searchTerm = event.target.value)}
        type="search"
        id="default-search"
        class="block w-full p-2 ps-10
        text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50"
        placeholder="Search stops or buildings"
      />
    </div>
  </form>
  {#if tableData && tableData.length > 0}
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
                class="cursor-pointer px-1 py-1 border truncate select-none"
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
            <tr
              class={`cursor-pointer ${
                item.index === selectedRow ? "bg-orange-300" : ""
              }`}
              on:click={() => rowClick(item)}
            >
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
