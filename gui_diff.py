from xmldiff import main, formatting

formatter = formatting.XMLFormatter(normalize=formatting.WS_BOTH)
diffs = main.diff_files("apk.xml", "base_apk.xml", diff_options={'F': 1, 'ratio_mode': 'accurate'},
                        formatter=formatter)
print(diffs)
