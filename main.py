import argparse
import os
import platform
import re
import shutil
import subprocess
from config import lang2code, name2voice, translation

rootdir = os.path.dirname(os.path.abspath(__file__))

def run_csxtool(infile, outdir):
    csxname, csxext = os.path.splitext(os.path.basename(infile))
    outfile = os.path.join(outdir, f"{csxname}.txt")
    # skip if cached
    if os.path.exists(outfile):
        return outfile
    # csxtool always writes to the same directory as input
    tmpfile = shutil.copy(infile, outdir)
    # execute csxtool command
    toolext = ".exe" if platform.system() == "Windows" else ""
    exefile = os.path.join(rootdir, "bin", f"csxtool{toolext}")
    subprocess.run([exefile, "export", tmpfile], check=True)
    # cleanup everything
    os.remove(tmpfile)
    return outfile

def cleanup_csx_export(target, lines, lang):
    res = []
    prev = 0
    for line in lines:
        # format example: "[JP00001] [Haruka] I'm home."
        m = re.match(r"\[JP(\d+)\]\s?(.*)", line)
        if not m:
            continue
        index, text = m.groups()
        cur = int(index)
        if prev != cur:
            res.append("")
            prev = cur
        # add line break for multi-line text
        if len(res[-1]) > 0:
            res[-1] += "\n"
        res[-1] += text
    return res

def fix_missing_text(target, lines, lang):
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
                res.append(translation[target]["@Hitret id=4605"][lang])
            elif cur == 34889:
                res.append(translation[target]["@Hitret id=37208"][lang])
            elif cur == 37465 and lang != "ja":
                res.append(translation[target]["@Hitret id=325"][lang])
        elif target == "haruka":
            if cur == 3518:
                res.append(translation[target]["@Hitret id=3526"][lang])
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

def normalize_name(name):
    # standardize whitespaces
    name = re.sub(r"\s+", "　", name)
    # no voice for hero
    name = re.sub(r"(悠|Haruka)\s*(＆|&|and)\s*", "", name)
    name = re.sub(r"\s*(＆|&|and)\s*(悠|Haruka)", "", name)
    return name.strip()

def find_voice_from_command(line):
    # command example: "@Talk name=Sora voice=SR000001"
    m = re.match(r".*name=([^ \n\r]+)\s+(?:voice=([^ \n\r]+))?", line)
    if m is None:
        return None
    name, audio = m.groups()
    name = normalize_name(name)
    if audio is not None:
        return audio[:2] if "/" not in audio else audio
    else:
        return name2voice.get(name)

def find_name_from_dialogue(line):
    # dialogue example: "[Haruka] I'm home."
    m = re.match(r"\[([^《]*(?:《(.+)》)?[^》]*)\]", line)
    if m is None:
        return None
    name, altname = m.groups()
    # special cases: "[声《初佳》]"
    if altname is not None:
        name = altname
    return normalize_name(name)

def replace_talk_command(template, text):
    res = []
    cur = 0
    talk = None
    voicecnt = 0
    matchcnt = 0
    for line in template:
        if talk is not None:
            if is_ks_command(line, "@hit"):
                # verify whether name matches with voice
                voice = find_voice_from_command(talk)
                name = find_name_from_dialogue(text[cur])
                if voice is not None:
                    voicecnt += 1
                if name in name2voice:
                    # either match or ignore NPC voice
                    assert name2voice[name] == voice or voice == "NP", f"name and voice not match: {name} vs {voice}"
                    matchcnt += 1
                # insert translated text
                body = re.sub(r"^\[.+\]\s?", "", text[cur])
                res.append(body + "\n")
                cur += 1
                # exit talk state
                talk = None
            else:
                # skip empty line
                assert len(line.strip()) == 0, f"unknown text between @Talk and @Hitret command: {line}"
                continue
        else:
            if is_ks_command(line, "@talk"):
                # enter talk state
                talk = line
        res.append(line)
    print(f"verified voice={voicecnt} match={matchcnt} skip={voicecnt - matchcnt}")
    assert cur == len(text), f"@Talk command and translation text not match: {cur} vs {len(text)}"
    return res

def fill_ks_template(target, lines, lang, outdir):
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
        # fill dialogue text
        cnt = count_talk_command(template)
        res = replace_talk_command(template, lines[offset:offset+cnt])
        offset += cnt
        # replace choice text
        res = "".join(res)
        choices = translation[target].get("@AddSelect", {})
        choices_src = choices.get("en", [])
        choices_dst = choices.get(lang, [])
        for original, localized in zip(choices_src, choices_dst):
            res = res.replace(original, localized)
        # save result
        outpath = os.path.join(outdir, filename)
        with open(outpath, mode="w", encoding="utf-8") as file:
            file.write(res)
    assert offset == len(lines), f"unused translation text detected: {len(lines) - offset}"
    return outdir

def run_xp3pack(indir, outdir):
    exdir = os.path.join(rootdir, "dependencies", "extras")
    tmpdir = os.path.join(outdir, "patch")
    # xp3pack always writes to cwd
    cwd = os.getcwd()
    os.chdir(outdir)
    # combine input and extras
    os.makedirs(tmpdir, exist_ok=True)
    shutil.copytree(exdir, tmpdir, dirs_exist_ok=True)
    shutil.copytree(indir, tmpdir, dirs_exist_ok=True)
    # execute xp3pack command
    monocmd = [] if platform.system() == "Windows" else ["mono"]
    exefile = os.path.join(rootdir, "bin", "xp3pack.exe")
    subprocess.run(monocmd + [exefile, tmpdir], check=True)
    # cleanup everything
    shutil.rmtree(tmpdir)
    os.chdir(cwd)
    return os.path.join(outdir, "patch.xp3")

def main():
    # parse command args
    parser = argparse.ArgumentParser(description="Convert CSX to Kirikiri Script and XP3 for Yosuga and Haruka")
    parser.add_argument("-i", "--input", default="./yosuga.csx")
    parser.add_argument("-o", "--output", default="./compile")
    parser.add_argument("-l", "--lang", default="ja")
    args = parser.parse_args()
    args.input = os.path.abspath(args.input)
    args.output = os.path.abspath(args.output)
    args.lang = args.lang.lower()

    # convert language to 2 letter code
    assert args.lang in lang2code, f"unsupported language: {args.lang}, must be one of {list(lang2code.keys())}"
    args.lang = lang2code[args.lang]

    # determine processing target
    csxname, csxext = os.path.splitext(os.path.basename(args.input))
    target = csxname.lower()
    assert target == "yosuga" or target == "haruka", f"unrecognized processing target {target}, must be yosuga.csx or Haruka.csx"
    print(f"Processing {target}")

    # extract text from csx file
    os.makedirs(args.output, exist_ok=True)
    txtfile = run_csxtool(args.input, args.output)
    print(f"CSX file exported to: {txtfile}")

    # read and process generated text file
    with open(txtfile, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = cleanup_csx_export(target, lines, args.lang)
    lines = fix_missing_text(target, lines, args.lang)
    print(f"TXT file processed")

    # write tmpfile for debugging purpose
    tmppath = os.path.join(args.output, "tmp.txt")
    with open(tmppath, mode="w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"DEBUG file saved to {tmppath}")

    # fill text into kirikiri script template
    ksdir = fill_ks_template(target, lines, args.lang, args.output)
    print(f"KS files generated in {ksdir}")

    # pack output as xp3 format
    xp3file = run_xp3pack(ksdir, args.output)
    print(f"XP3 patch created at {xp3file}")

if __name__ == "__main__":
    main()
