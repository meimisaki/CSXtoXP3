
# ISO 639-1 code
lang2code = {
    "czech":      "cz",
    "german":     "de",
    "english":    "en",
    "spanish":    "es",
    "french":     "fr",
    "japanese":   "ja",
    "portuguese": "pt",
    "vietnamese": "vn",
}
for code in list(lang2code.values()):
    lang2code[code] = code

# mapping between localized name and voice file prefix
voice2names = {
    "AK": ["瑛", "Akira"],
    "AN": ["車内アナウンス", "Announcer"],
    "DA": ["男子生徒Ａ", "Male　Student　A"],
    "EI": ["英語教師", "English　Teacher"],
    "KA": ["一葉", "Kazuha"],
    "KO": ["梢", "委員長", "Kozue", "Class　Rep"],
    "MT": ["初佳", "Motoka"],
    "NO": ["奈緒", "Nao"],
    "RH": ["亮平", "Ryouhei"],
    "SH": ["一葉の父", "Kazuha's　Father", "Man　In　Kimono"],
    "SR": ["穹", "Sora"],
    "TK": ["タカノ店主", "Shopkeeper"],
    "TN": ["担任", "Teacher"],
    "YH": ["やひろ", "Yahiro"],
    "YM": ["月見山", "Yamanashi"],
}
name2voice = {}
for voice, names in voice2names.items():
    for name in names:
        name2voice[name] = voice

# translation for missing text and choices
translation = {
    "yosuga": {
        "@Hitret id=4605": {
            "cz": "I když jsme pořád neslyšeli nic o tom, co bychom měli dělat.",
            "de": "Obwohl wir noch keine Neuigkeiten darüber gehört haben, was wir tun sollten.",
            "en": "Although we still haven't heard any news on what we should do.",
            "es": "Aunque aún no habíamos oído qué debíamos hacer.",
            "fr": "Même si nous n'avons toujours pas eu de nouvelles sur ce que nous devrions faire.",
            "ja": "とは言っても、天女目からはまだ何をすればいいのか聞いていない。",
            "pt": "Apesar que nós ainda não escutamos nada do que fazer.",
            "vn": "Mặc dù chúng tôi vẫn chưa nghe bất kỳ tin tức nào về những gì chúng tôi nên làm.",
        },
        "@Hitret id=37208": {
            "cz": "Teď Sora ukazovala její rozčílení tak jasně, že kdyby to bylo mířeno na Motoku, začala by z toho koktat. Její mamce to ale asi nevadilo.",
            "de": "Jetzt, Sora projektiert Ihre Verärgerung so klar dass, wenn es wird an Motoka-san gerichtet, Sie würde an Ihre Wörter gefallen. Ihre Mutter war nicht ärgert von dass.",
            "en": "At this point, Sora was projecting her annoyance so clearly that, were at it directed at Motoka-san, it would've had her stumbling over her words. It didn't seem to bother her mother, though.",
            "es": "Llegados a ese punto, Sora estaba mostrando su enfado de forma tan clara que, si fuera dirigida a Motoka-san, le habría hecho tropezarse con sus palabras. Sin embargo, a su madre no parecía molestarle.",
            "fr": "À ce stade, Sora projetait son agacement tellement clairement que, s'il était dirigé vers Motoka, elle en buterait sur ses mots. Cela ne semblait pas déranger sa mère cependant.",
            "ja": "穹は、初佳さんならうろたえてしまうほど、迷惑オーラを発しているのだが、おばさんには通じていない。",
            "pt": "Nesse momento, Sora estava planejando anunciar claramente que, fosse direcionado à Makoto-san, isso teria feito ela tremer com suas palavras. Apesar que não parecia ter incômoda sua mãe.",
            "vn": "Tại thời điểm này, Sora đã thể hiện sự khó chịu của mình một cách rõ ràng đến nỗi, nó nhắm thẳng vào Motoka-san, chắc chắn cô ấy sẽ vấp phải những lời nói của mình. Tuy nhiên, điều đó dường như không làm mẹ cô bận tâm.",
        },
        "@Hitret id=325": {
            "cz": "Vzhledem k situaci si zatím budeš muset vystačit s chlebem a mlékem.",
            "de": "Weil die Situation, du nur Milch und Brot isst wird.",
            "en": "Given the circumstance, you'll just have to put up with bread and milk for now.",
            "es": "Dadas las circunstancias, tendrás que aguantar con pan y leche por ahora.",
            "fr": "Étant donné les circonstances, tu devras te contenter de pain et de lait pour l'instant.",
            "ja": "さすがにこんな状態なんだから、パンと牛乳だけになるのは我慢してくれよ？",
            "pt": "Dados as circunstâncias, você terá que tolerar com pão e leite por agora.",
            "vn": "Trong hoàn cảnh này, bây giờ bạn sẽ chỉ phải ăn với bánh mì và sữa.",
        },
    },
    "haruka": {
        "@Hitret id=3526": {
            "cz": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "de": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "en": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "es": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "fr": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "ja": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "pt": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
            "vn": "よだれをシーツに染みこませて、がくがくと身体全体を震わせる。",
        },
    },
}
