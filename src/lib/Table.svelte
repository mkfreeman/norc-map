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
</script>

<div class="overflow-x-auto" style="max-height: {maxHeight};">
  {#if tableData}
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
