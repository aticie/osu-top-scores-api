<script>
    export let text;
    export let unicode = false;
</script>

<div class="squaredThree">
<input type=checkbox id="squaredThree" bind:checked={unicode}>{text}
</div>

<style>
</style>
