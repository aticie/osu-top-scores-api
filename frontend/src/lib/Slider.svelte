<script>
    import { createEventDispatcher } from 'svelte';
    import RangeSlider from "svelte-range-slider-pips";

    let values = [500, 800]
    const dispatch = createEventDispatcher();

    function sendValue() {
        console.log('Sending ' + values);
        dispatch('message', values);
    }
</script>

<div class="slidecontainer">
    <div class="slidertitle">
        PP:
    </div>
    <div class="sliderbody">
        <RangeSlider range float pushy bind:values={values} step={5} min={400} max={1300} on:change={sendValue}/>
    </div>
</div>

<style>
    :root{
        --range-slider: #EDEDED;
        --range-handle-inactive: #da0037;
        --range-handle-focus:#ff5361;
        --range-range: #da0037;
        --range-handle:#da0037;
    }
    .slidecontainer {
        width: 100%;
        justify-content: center;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: row;
    }
    .slidertitle{
        vertical-align: middle;
        color: #EDEDED;
        line-height: 35px;
    }

    .sliderbody {
        max-width: 500px;
        align-self: center;
        -webkit-appearance: none;
        width: 100%;
        outline: none;
        opacity: 0.9;
        -webkit-transition: .2s;
        border-radius: 2rem;
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
        border-radius: 2rem;;
        cursor: pointer;
    }

    .slider::-moz-range-thumb {
        width: 25px;
        height: 25px;
        background: #da0037;
        cursor: pointer;
    }
</style>