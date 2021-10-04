<script>
    import axios from "axios";

    let mods = 'any';
    let beatmaps = [];
    import Button from './lib/Button.svelte'

    let submit = () => {
        axios
            .get('/beatmaps', {params: {mod: mods}})
            .then((res) => {
                beatmaps = res.data.beatmaps;
                console.log(beatmaps);
            })
    };
</script>

<main>
    <h1>osu! Top 500 Scores Database</h1>

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
    <Button
            text="Get Beatmaps"
            onClick={submit}
    />
    <div class="beatmaps">
        {#each beatmaps as bmap}
            <div class="beatmap-single">
                <div class="beatmap-cover"
                     style="background-image: url('https://assets.ppy.sh/beatmaps/{bmap.beatmapset_id}/covers/cover.jpg')">
                </div>
                <div class="beatmap-details">
                    Avg. PP: {bmap.avg_pp} <br>

                    PlayCount: {bmap.play_count}
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

    .beatmaps {
        margin-top: 3em;
        display: flex;
        flex-direction: column;
        color: #da0037;
    }
    .beatmap-single{
        font-size: x-large;
        display: flex;
        margin: 0 8em 0.7em 8em;
    }

    .beatmap-cover {
        height: 250px;
        width: 900px;
        background-size: cover;
    }
    .beatmap-details{
        margin: auto;
        color: #EDEDED;
    }

    input {
        color: #171717;
    }

    main {
        text-align: center;
        padding: 1em;
        margin: 0 auto;
    }

    h1 {
        color: #da0037;
        font-size: 4rem;
        font-weight: 350;
        line-height: 1.1;
        margin: 2rem auto;
        max-width: 14rem;
    }

    p {
        max-width: 14rem;
        margin: 1rem auto;
        line-height: 1.35;
        color: #EDEDED;
    }

    @media (min-width: 480px) {
        h1 {
            max-width: none;
        }

        p {
            max-width: none;
        }
    }
</style>
