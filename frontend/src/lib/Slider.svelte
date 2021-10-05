<script>
    import { createEventDispatcher } from 'svelte';

    let current_value = 5;
    const dispatch = createEventDispatcher();

    function sendValue() {
        console.log('Sending ' + {current_value})
        dispatch('message', current_value);
    }
</script>

<div class="slidecontainer">
    <div class="slidertitle">
        Show {#if current_value === 100}∞{:else }{current_value}{/if} number of results!
    </div>
    <div class="sliderbody">
        <input type="range" min="1" max="100" bind:value={current_value} on:input={sendValue} class="slider">
    </div>
</div>

<style>
    .slidecontainer {
        width: 100%;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .slidertitle{
        color: #EDEDED;
    }

    .slider {
        max-width: 500px;
        -webkit-appearance: none;
        width: 100%;
        height: 25px;
        background: #373737;
        outline: none;
        opacity: 0.9;
        -webkit-transition: .2s;
        transition: opacity .2s;
    }

    .slider:hover {
        opacity: 1;
    }

    .slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 25px;
        height: 25px;
        background: #da0037;
        cursor: pointer;
    }

    .slider::-moz-range-thumb {
        width: 25px;
        height: 25px;
        background: #da0037;
        cursor: pointer;
    }
</style>