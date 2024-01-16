import argparse
import os
import platform
import re
import shutil
import subprocess

def run_csxtool(target, indir, outdir):
    # skip if cached
    if os.path.exists(os.path.join(outdir, target + ".txt")):
        return
    # find tool location
    rootdir = os.path.dirname(os.path.abspath(__file__))
    toolext = ".exe" if platform.system() == "Windows" else ""
    exepath = os.path.join(rootdir, "bin", "csxtool" + toolext)
    # execute command
    subprocess.run([exepath, "export", indir], check=True)
    # move output file
    filepath = os.path.join(os.path.dirname(indir), target + ".txt")
    shutil.move(filepath, outdir)

def cleanup_csx_export(target, lines, keep_name):
    res = []
    prev = 0
    for line in lines:
        # format example: "[JP00001] [Haruka] I'm home."
        m = re.match(r"\[JP(\d+)\]\s*(\[.*\])?\s*(.*)", line)
        if not m:
            continue
        index, name, text = m.groups()
        cur = int(index)
        if prev != cur:
            res.append("")
            prev = cur
        if keep_name and name is not None:
            res[-1] += name
        # TODO: we need a space here for non-CJK languages
        res[-1] += text
    return res

def fix_missing_text(target, lines):
    res = []
    cur = 0
    # csxtool missed some actor lines and we gotta fix them here
    for line in lines:
        cur += 1
        if target == "yosuga":
            if 15560 <= cur and cur <= 15597:
                # Nao's extra chapter, which does not exist in the download edition
                # start from すっかり遅くなってしまった。
                # end at 想いが通じたことで、奈緒ちゃんとの距離が近づいたことが、とても嬉しかった。
                continue
            elif cur == 2305:
                # @Hitret id=4605
                res.append("とは言っても、天女目からはまだ何をすればいいのか聞いていない。")
            elif cur == 34889:
                # @Hitret id=37208
                res.append("穹は、初佳さんならうろたえてしまうほど、迷惑オーラを発しているのだが、おばさんには通じていない。")
        elif target == "haruka":
            if cur == 3518:
                # @Hitret id=3526
                res.append("よだれをシーツに染みこませて、がくがくと身体全体を震わせる。")
        res.append(line)
    return res

def is_ks_command(line, cmd):
    return line.strip().lower().startswith(cmd)

def count_talk_command(template):
    res = 0
    for line in template:
        if is_ks_command(line, "@talk"):
            res += 1
    return res

name2voice = {
    "瑛": "AK", "Akira": "AK",
    "車内アナウンス": "AN", "Announcer": "AN",
    "男子生徒Ａ": "DA", "Male　Student　A": "DA",
    "英語教師": "EI", "English　Teacher": "EI",
    "一葉": "KA", "Kazuha": "KA",
    "梢": "KO", "委員長": "KO", "Kozue": "KO", "Class　Rep": "KO",
    "初佳": "MT", "Motoka": "MT",
    "奈緒": "NO", "Nao": "NO",
    "亮平": "RH", "Ryouhei": "RH",
    "一葉の父": "SH", "Kazuha's　Father": "SH", "Man　In　Kimono": "SH",
    "穹": "SR", "Sora": "SR",
    "タカノ店主": "TK", "Shopkeeper": "TK",
    "担任": "TN", "Teacher": "TN",
    "やひろ": "YH", "Yahiro": "YH",
    "月見山": "YM", "Yamanashi": "YM",
}

def replace_talk_command(template, text, verify):
    res = []
    cur = 0
    talk = False
    voice = None
    voicecnt = 0
    matchcnt = 0
    for line in template:
        if talk:
            if is_ks_command(line, "@hit"):
                # verify name matches with voice
                m = re.match(r"\[([^《]*(?:《(.+)》)?[^》]*)\]", text[cur]) if verify else None
                if m is not None:
                    name, altname = m.groups()
                    # special cases: "[声《初佳》]"
                    if altname is not None:
                        name = altname
                    # no voice for hero
                    name = name.replace("悠＆", "")
                    name = name.replace("＆悠", "")
                    if name in name2voice:
                        # either match or ignore NPC voice
                        assert name2voice[name] == voice or voice == "NP"
                        matchcnt += 1
                voice = None
                # exit talk state
                res.append(text[cur] + "\n")
                cur += 1
                talk = False
            else:
                # skip empty line
                assert len(line.strip()) == 0
                continue
        else:
            if is_ks_command(line, "@talk"):
                # enter talk state
                talk = True
                # save voice for later use
                m = re.match(r".*name=([^ ]+)\s+(?:voice=([^ ]+))?", line) if verify else None
                if m is not None:
                    name, audiofile = m.groups()
                    # no voice for hero
                    name = name.replace("Haruka　and　", "")
                    name = name.replace("　and　Haruka", "")
                    # only check for single voice
                    if audiofile is not None:
                        voice = "multiple" if "/" in audiofile else audiofile[:2]
                        voicecnt += 1
                    elif name in name2voice:
                        voice = name2voice[name]
        res.append(line)
    if verify:
        print(f"verified voice={voicecnt} match={matchcnt} skip={voicecnt - matchcnt}")
    assert cur == len(text)
    return res

def fill_ks_template(target, lines, outdir, verify):
    rootdir = os.path.dirname(os.path.abspath(__file__))
    indir = os.path.join(rootdir, "dependencies", target)
    outdir = os.path.join(outdir, "scenario")
    os.makedirs(outdir, exist_ok=True)
    offset = 0
    for filename in sorted(os.listdir(indir)):
        if not filename.endswith(".ks"):
            continue
        print(f"converting {filename}")
        # load template
        inpath = os.path.join(indir, filename)
        with open(inpath, mode="r", encoding="utf-8") as file:
            template = file.readlines()
        # fill template
        cnt = count_talk_command(template)
        res = replace_talk_command(template, lines[offset:offset+cnt], verify)
        offset += cnt
        # save template
        outpath = os.path.join(outdir, filename)
        with open(outpath, mode="w", encoding="utf-8") as file:
            file.writelines(res)
    assert offset == len(lines)

def main():
    # parse command args
    parser = argparse.ArgumentParser(description="Convert CSX to Kirikiri Script and XP3 for Yosuga and Haruka")
    parser.add_argument("-i", "--input", default="./yosuga.csx")
    parser.add_argument("-o", "--output", default="./compile")
    # TODO: support other languages
    parser.add_argument("--debug", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--verify", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)

    # determine processing target
    filename, ext = os.path.splitext(os.path.basename(args.input))
    target = filename.lower()
    assert target == "yosuga" or target == "haruka"
    print(f"Processing {target}")

    # extract text from csx file
    os.makedirs(args.output, exist_ok=True)
    run_csxtool(target, args.input, args.output)
    print(f"CSX file exported")

    # read and process generated text file
    txtfile = os.path.join(args.output, target + ".txt")
    with open(txtfile, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = cleanup_csx_export(target, lines, keep_name=args.verify)
    lines = fix_missing_text(target, lines)
    print(f"TXT file processed")

    # write tmpfile for debugging purpose
    if args.debug:
        tmppath = os.path.join(args.output, "tmp.txt")
        with open(tmppath, mode="w", encoding="utf-8") as file:
            file.write("\n".join(lines))
        print(f"DEBUG file saved")

    # fill text into kirikiri script template
    fill_ks_template(target, lines, args.output, args.verify)
    print(f"KS files generated")

    # TODO: create xp3 patch

if __name__ == "__main__":
    main()
