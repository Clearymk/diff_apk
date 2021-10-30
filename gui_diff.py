from xmldiff import main, formatting

formatter = formatting.XMLFormatter(normalize=formatting.WS_BOTH, pretty_print=True)
diffs = main.diff_files("res/apk_format.xml", "res/base_apk_format.xml",
                        diff_options={'F': 0.9, 'ratio_mode': 'accurate'},
                        formatter=formatter)
with open("res/diff_res.xml", "w", encoding="utf8") as f:
    f.write(diffs)
