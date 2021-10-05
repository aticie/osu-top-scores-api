<script>
    import axios from "axios";

    let top_n = 5;
    let mods = 'any';
    let unicode = false;
    let include_hd = true;
    let beatmaps = [];
    import Button from './lib/Button.svelte'
    import Slider from "./lib/Slider.svelte";

    function setSliderValue(event) {
        if (event.detail === 100) {
            top_n = -1;
        }
        else{
            top_n = event.detail
        }
    }

    let submit = () => {
        axios
            .get('/beatmaps', {params: {mod: mods, include_hd: include_hd, top_n: top_n}})
            .then((res) => {
                beatmaps = res.data.beatmaps;
            })
    };
</script>

<main>
    <h1>osu! Top 1000 Scores Database</h1>

    <p>
        <input type=radio bind:group={mods} name="mods" value={'any'}>
        Any
        <input type=radio bind:group={mods} name="mods" value={''}>
        NM
        <input type=radio bind:group={mods} name="mods" value={'HR'}>
        HR
        <input type=radio bind:group={mods} name="mods" value={'DT'}>
        DT

    </p>
    <div class="checkboxes">

        <div class="checkbox-single">
            <input type="checkbox" bind:checked={unicode}/> Show titles in local language
        </div>
        <div class="checkbox-single">
            <input type="checkbox" bind:checked={include_hd}/> Include hidden plays
        </div>
    </div>
    <Slider on:message={setSliderValue}/>
    <Button
            text="Get Beatmaps"
            onClick={submit}
    />
    <div class="beatmaps">
        {#each beatmaps as bmap}
            <div class="beatmap-single">
                <a class="beatmap-url" href="https://osu.ppy.sh/b/{bmap.beatmap_id}">
                    <div class="beatmap-cover"
                         style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{bmap.cover_url}')">
                        <span>{#if unicode}{bmap.artist_unicode}
                            {:else }{bmap.artist}{/if}</span>
                        <br>
                        <span>{#if unicode}{bmap.title_unicode}
                            {:else }{bmap.title}{/if}</span>
                        <p>{bmap.difficulty}</p>
                    </div>
                </a>
                <div class="beatmap-details">
                    <div class="beatmap-detail">
                        <div class="detail-title">
                            Average PP
                        </div>
                        <div class="detail-value">
                            {(Math.round(bmap.avg_pp * 100) / 100).toFixed(2)}
                        </div>
                    </div>
                    <div class="beatmap-detail">
                        <div class="detail-title">
                            Play Count
                        </div>
                        <div class="detail-value">
                            {bmap.play_count}
                        </div>
                    </div>

                </div>
            </div>
        {/each}
    </div>
</main>

<style>
    :root {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        background: #171717;
    }

    .checkboxes{
        color: #EDEDED;
        line-height: 200%;
    }

    .beatmaps {
        margin-top: 3rem;
        display: flex;
        flex-direction: column;
        color: #da0037;
    }

    .beatmap-single {
        font-size: x-large;
        display: flex;
        margin: 0.5rem 0;
        justify-content: center;
    }

    .beatmap-url {
        display: flex;
        flex-grow: 1;
        text-decoration: none;
        color: #fff;
        max-width: 900px;
    }

    .beatmap-cover {
        display: flex;
        min-height: 5rem;
        padding: 1rem;
        flex-grow: 1;
        border-radius: 2rem;
        text-align: center;
        flex-direction: column;
        justify-content: center;
        background-size: cover;
        background-position: center;
    }

    .beatmap-details {
        display: flex;
        flex-direction: column;
        margin-left: 1em;
        color: #EDEDED;
    }

    .beatmap-detail {
        margin: 2em auto;
    }

    .detail-title {
        font-weight: bold;
    }

    input {
        color: #171717;
    }

    main {
        text-align: center;
        padding: 1rem;
        margin: 0 auto;
    }

    h1 {
        color: #da0037;
        font-size: 4rem;
        font-weight: 350;
        line-height: 1.1;
        margin: 2rem auto;
    }

    p {
        margin: 1rem auto;
        line-height: 1.35;
        color: #EDEDED;
    }

    span {
        font-weight: bold;
    }

    @media (max-width: 576px) {
        .beatmap-single {
            flex-direction: column;
        }

        .beatmap-details {
            margin-left: 0;
            flex-direction: row;
        }

    }
</style>
