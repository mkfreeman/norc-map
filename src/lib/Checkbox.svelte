<script>
  export let checked = true;
  export let onClick = () => {};
  export let label = "Label";
</script>

<div class="flex items-start mb-3 font-bold cursor-pointer">
  <div class="flex items-center h-5 cursor-pointer">
    <input
      on:click={onClick}
      {checked}
      id={label}
      type="checkbox"
      class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
    />
  </div>
  <label
    for={label}
    class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
    >{label}</label
  >
</div>
