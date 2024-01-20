# Yosuga no Sora Patch Conversion

This program was created to convert the older versions of Yosuga no Sora and Haruka na Sora based on the EntisGLS Engine to the newer format based on the KiriKiri Engine.

This entire process is detailed in the [wiki](https://github.com/EnormousSpud/YnS-Wiki/wiki).

The English patch for Yosuga no Sora can be found in the English YNS [Discord](https://discord.gg/yosuga-no-sora).

# Instructions

Step 1 - Clone this repo to your local folder and enter it.

Step 2 - Download a `yosuga.csx` or `Haruka.csx` file from somewhere online (such as a translation group), then place the CSX file into the same folder.

Step 3 - Run command `python main.py -i yosuga.csx -l en` or `python main.py -i Haruka.csx -l en` and wait until finished.

Step 4 - You can find all generated KiriKiri scripts under the `compile/scenario` folder, and the packed XP3 file at `compile/patch.xp3`.

_**Please report any errors that are found with the FORMATTING of the text or names by making a pull request on GitHub.**_

_**DO NOT report translation errors in the text to me, that data comes from the CSX file you supplied.**_

# Credits

The current version is a complete rewrite by [meimisaki](https://github.com/meimisaki).

The original Yosuga no Sora Conversion Tool written by [MrWicked](https://github.com/TheRealMrWicked) under [GPL License](LICENSE).

CSXtool written by Amanojaku.

[Xp3Pack](https://github.com/arcusmaximus/KirikiriTools) written by [arcusmaximus](https://github.com/arcusmaximus).
