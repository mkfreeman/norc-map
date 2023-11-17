<script lang="ts">
  interface RadioOption {
    value: string;
    label: string;
  }

  export let options: RadioOption[] = [];
  export let selected: string = '';
  export let updateMethod: (selected: string) => void = () => {};
  export let label: string = '';

  function handleRadioChange(event: Event) {
    const target = event.target as HTMLInputElement;
    selected = target.value;
    updateMethod(selected);
  }
</script>

<div class="flex items-center">
  {#if label}
    <strong class="mr-2">{label}</strong>
  {/if}

  {#each options as option}
    <label class="inline-flex items-center mr-4">
      <input
        type="radio"
        class="form-radio text-indigo-600"
        bind:group={selected}
        value={option.value}
        on:change={handleRadioChange}
      />
      <span class="ml-2">{option.label}</span>
    </label>
  {/each}
</div>
