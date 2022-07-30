<script>
  import RangeSlider from "svelte-range-slider-pips";

  const allMods = [
    { text: "NM", req: "" },
    { text: "Any", req: "any" },
    { text: "HR", req: "hr" },
    { text: "DT", req: "dt" },
  ];

  // settings
  let currentMods = "any";
  let unicode = false;
  let includeHD = false;
  let ppRange = [500, 800];
  //

  let page = 1;
  let beatmaps = [];
</script>

<main class="flex flex-col gap-4 w-full max-w-2xl">
  <p class="font-semibold text-2xl text-center">osu! Top 1000 Scores Database</p>

  <div class="flex flex-col gap-4 ">
    <div class="flex flex-col md:flex-row items-center justify-around gap-4">
      <div class="flex flex-col gap-2">
        <p class="setting-title">Mods</p>
        <div class="flex gap-2">
          {#each allMods as mod}
            <div class="relative flex items-center justify-center">
              <input
                class="appearance-none rounded-full border-2 border-neutral-700 h-12 w-12 checked:border-red-primary transition-colors"
                type="radio"
                bind:group={currentMods}
                name="mods"
                id={mod.text}
                value={mod.req}
              />
              <label class="absolute select-none" for={mod.text}>{mod.text}</label>
            </div>
          {/each}
        </div>
      </div>
  
      <div class="flex flex-col gap-2">
        <div class="checkbox-container">
          <input class="checkbox" type="checkbox" id="unicode" bind:checked={unicode} />
          <label class="checkbox-label" for="unicode">Unicode Titles</label>
        </div>
        <div class="checkbox-container">
          <input class="checkbox" type="checkbox" id="includeHD" bind:checked={includeHD} />
          <label class="checkbox-label" for="includeHD">Include HD</label>
        </div>
      </div>
    </div>


    <div>
      <p class="setting-title">PP Range</p>
      <RangeSlider range float pushy step={5} min={400} max={1300} bind:values={ppRange} />
    </div>

    <button class="bg-red-primary rounded-md p-2 hover:bg-neutral-800 transition-colors col-span-2">Get Beatmaps</button>
  </div>
</main>

<!-- <script>
    let beatmaps = [];
    let pp_range = [500, 800]
    let page = 1;

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
 -->
