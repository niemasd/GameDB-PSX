# GameDB-PSX
Sony PlayStation (PSX), part of [GameDB](https://github.com/niemasd/GameDB).

## Structured Downloads
* **[`PSX.data.json`](https://github.com/niemasd/GameDB-PSX/releases/latest/download/PSX.data.json):** All data, structured in the JSON format
* **[`PSX.data.tsv`](https://github.com/niemasd/GameDB-PSX/releases/latest/download/PSX.data.tsv):** All data, structured in the TSV format
* **[`PSX.release_dates.pdf`](https://github.com/niemasd/GameDB-PSX/releases/latest/download/PSX.release_dates.pdf):** Histogram of release dates, stratified by region
* **[`PSX.titles.json`](https://github.com/niemasd/GameDB-PSX/releases/latest/download/PSX.titles.json):** Mapping of serial numbers to game titles, structured in the JSON format

# Notes

## Uniquely Identifying Games

Most PSX games have a file in the root directory of the disc with a naming structure like `SXXX_XXX.XX`, where `SXXX-XXXXX` is the game's serial (i.e., how the game folders in [`games`](games) are named). This file is the game's executable, and this file's name can be trivially converted to the game's serial, which can easily uniquely identify the game. See the [relevant part of the GameID PSX identification code](https://github.com/niemasd/GameID/blob/d038079574c2679de8f437101bcea056b9114646/GameID.py#L262-L273) for implementation details.

Some games have an executable that doesn't follow this naming scheme. In *some* of these cases, the disc's volume ID (sometimes known as the "label") contains the serial. See the [relevant part of the GameID PSX identification code](https://github.com/niemasd/GameID/blob/d038079574c2679de8f437101bcea056b9114646/GameID.py#L275-L283) for implementation details.

If *neither* of these is the case, you might be able to use some combination of the game disc's UUID, volume ID, and file list to uniquely identify the game, but GameID doesn't currently explore those.

# Sources
* [GameFAQs](https://gamefaqs.gamespot.com/)
* [Glitchwave](https://glitchwave.com/)
* [MiSTer Addons](https://misteraddons.com/)
* [MobyGames](https://www.mobygames.com/)
* [PlayStation Datacenter](https://psxdatacenter.com/)
* [Redump](http://redump.org/)
* [Redump Wiki](http://wiki.redump.org/)
* [SerialStation](https://www.serialstation.com/)
* [VGArchive](https://vgarchive.org/)
