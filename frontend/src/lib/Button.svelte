<script>
    export let text;
    export let onClick = () => {};
</script>

<button
        on:click={onClick}>
    <div class="text">{text}</div>
</button>


<style>
  button {
    font-family: inherit;
    font-size: inherit;
    padding: 1em 2em;
    color: #da0037;
    background-color: rgba(255, 62, 0, 0.1);
    border-radius: 2em;
    border: 2px solid rgba(255, 62, 0, 0);
    outline: none;
    width: 200px;
    font-variant-numeric: tabular-nums;
    cursor: pointer;
  }

  button:focus {
    border: 2px solid #da0037;
  }

  button:hover {
      background-color:#a00012;
      color: #EDEDED;
  }

  button:active {
    background-color: rgba(255, 62, 0, 0.2);
  }
</style>
