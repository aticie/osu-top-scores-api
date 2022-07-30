<script>
  import axios from "axios";
  import RangeSlider from "svelte-range-slider-pips";
  import InfiniteLoading from "svelte-infinite-loading";

  const allMods = [
    { text: "NM", req: "" },
    { text: "Any", req: "any" },
    { text: "HR", req: "hr" },
    { text: "DT", req: "dt" },
  ];

  // settings
  let mod = "any";
  let unicode = false;
  let includeHD = true;
  let ppRange = [500, 800];
  //

  let page = 1;
  let beatmaps = [];

  const getBeatmaps = async () => {
    const response = await axios.get("/beatmaps", {
      params: {
        mod,
        page,
        pp_range: ppRange,
        include_hd: includeHD,
      },
    });

    beatmaps = [...beatmaps, ...response.data.beatmaps];
    page++;

    return beatmaps.length;
  };

  const loadBeatmaps = async ({ detail: { loaded, complete } }) => {
    let length = await getBeatmaps();
    if (length) {
      loaded();
    } else {
      complete();
    }
  };
</script>

<main class="flex flex-col gap-4 w-full max-w-2xl">
  <p class="font-semibold text-2xl text-center">osu! Top 1000 Scores Database</p>

  <div class="flex flex-col gap-4 ">
    <div class="flex flex-col md:flex-row items-center justify-around gap-4">
      <div class="flex flex-col gap-2">
        <p class="setting-title">Mods</p>
        <div class="flex gap-2">
          {#each allMods as mods}
            <div class="relative flex items-center justify-center">
              <input
                class="appearance-none rounded-full border-2 border-neutral-700 h-12 w-12 checked:border-red-primary transition-colors"
                type="radio"
                bind:group={mod}
                name="mods"
                id={mods.text}
                value={mods.req}
              />
              <label class="absolute select-none" for={mods.text}>{mods.text}</label>
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

    <button
      on:click={getBeatmaps}
      class="bg-red-primary rounded-md p-2 hover:bg-neutral-800 transition-colors col-span-2">Get Beatmaps</button
    >
  </div>

  <div>
    {#each beatmaps as bmap}
      <a href="https://osu.ppy.sh/b/${bmap.beatmap_id}" class="rounded-full overflow-hidden relative">
        <div class="w-full h-32 rounded-md bg-cover" style="background-image: url({bmap.cover_url})" >
          <div class="flex justify-between items-end absolute inset-3 z-10">
            <div class="flex flex-col justify-between h-full">
              <p>{bmap.artist}</p>
              <div>
                <p class="font-semibold">{ bmap.title }</p>
                <p>{bmap.difficulty}</p>
              </div>
            </div>

            <div class="flex gap-4">
              <div class="text-center">
                <p class="font-semibold">Average PP</p>
                <p>{bmap.avg_pp.toFixed(2)}</p>
              </div>
              <div class="text-center">
                <p class="font-semibold">Play Count</p>
                <p>{bmap.play_count}</p>
              </div>
            </div>
          </div>

          <div class="absolute inset-0 bg-black bg-opacity-70" />
        </div>
      </a>
    {/each}
  </div>

  <InfiniteLoading on:infinite={loadBeatmaps} />
</main>
