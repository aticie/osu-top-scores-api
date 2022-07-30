<script>
    import axios from "axios";
    import InfiniteLoading from 'svelte-infinite-loading';
    import Button from './lib/Button.svelte';
    import Slider from "./lib/Slider.svelte";

    const all_mods = [
        {text: "Any", req: "any"},
        {text: "NM", req: ""},
        {text: "HR", req: "hr"},
        {text: "DT", req: "dt"},
    ];

    let mods = 'any';
    let unicode = false;
    let include_hd = true;
    let beatmaps = [];
    let pp_range = [500, 800]
    let page = 1;

    const setSliderValue = (event) => {
        console.log('New pp range: ' + pp_range)
        console.log(event)
        pp_range = event.detail
    }

    const infiniteHandler = ({detail: {loaded, complete}}) => {
        axios
            .get('/beatmaps', {params: {mod: mods, pp_range: pp_range, include_hd: include_hd, page: page}})
            .then((res) => {
                if (res.data.beatmaps.length) {
                    beatmaps = [...beatmaps, ...res.data.beatmaps];
                    page++;
                    loaded();
                } else {
                    complete();
                }
            });
    }

    const submit = () => {
        beatmaps = [];
        page = 1;
        axios
            .get('/beatmaps', {params: {mod: mods, pp_range: pp_range, include_hd: include_hd, page: page}})
            .then((res) => {
                beatmaps = [...beatmaps, ...res.data.beatmaps];
                page++;
            });
    };
</script>

<main>
    <div>
        <h1>osu! Top 1000 Scores Database</h1>
    </div>

    <div class="settings">
        <div class="mods">
            {#each all_mods as mod}
                <div class="btn-mods">
                    <input type=radio bind:group={mods} name="mods" id={mod.text} value={mod.req}>
                    <label for={mod.text}>{mod.text}</label>
                </div>
            {/each}
        </div>
        <div class="checkboxes">
            <div class="checkbox-single">
                <input class="checkbox" type="checkbox" bind:checked={unicode}/> Unicode Titles
            </div>
            <div class="checkbox-single">
                <input class="checkbox" type="checkbox" bind:checked={include_hd}/> Include HD
            </div>
        </div>
        <Button
                text="Get Beatmaps"
                onClick={submit}
        />
        <Slider on:message={setSliderValue}/>
    </div>
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

    <InfiniteLoading on:infinite={infiniteHandler}/>
</main>

