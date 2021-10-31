from xmldiff import main, formatting
import os


class GUIDiff:
    def __init__(self, xml_file_a, xml_file_b, res_file_path):
        self.xml_file_a = xml_file_a
        self.xml_file_b = xml_file_b
        self.res_file_path = res_file_path
        self.format_file_path(self.res_file_path)

    @staticmethod
    def format_file_path(file_path):
        file_path = file_path.replace(file_path.split("\\")[-1], "")
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    def start_diff(self):
        formatter = formatting.XMLFormatter(normalize=formatting.WS_BOTH, pretty_print=True)
        diffs = main.diff_files(self.xml_file_a, self.xml_file_b,
                                diff_options={'F': 0.5, 'ratio_mode': 'accurate'},
                                formatter=formatter)
        with open(self.res_file_path, "w", encoding="utf8") as f:
            f.write(diffs)


if __name__ == "__main__":
    diff = GUIDiff("res\\apk_format.xml", "res\\base_apk_format.xml", "res\\res.xml")
    diff.start_diff()
