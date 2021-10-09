<script>
    import { createEventDispatcher } from 'svelte';
    import RangeSlider from "svelte-range-slider-pips";

    let current_value = 5;
    export let initial_values = [500, 800]
    const dispatch = createEventDispatcher();

    function sendValue() {
        console.log('Sending ' + {current_value})
        dispatch('message', current_value);
    }
</script>

<div class="slidecontainer">
    <div class="slidertitle">
        Show between {initial_values[0]}pp - {initial_values[1]}pp
    </div>
    <div class="sliderbody">
        <RangeSlider range float pushy bind:values={initial_values} step={10} min={0} max={1300}/>
    </div>
</div>

<style>
    .slidecontainer {
        width: 100%;
        justify-content: center;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .slidertitle{
        color: #EDEDED;
    }

    .sliderbody {
        max-width: 500px;
        -webkit-appearance: none;
        width: 100%;
        height: 20px;
        background: #373737;
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