import os

diff_apk = []


def get_res_path():
    return "D:\\test"


if __name__ == "__main__":
    for file in os.listdir(get_res_path()):
        file = os.path.join(get_res_path(), file)
        for _ in os.listdir(file):
            _ = os.path.join(file, _)
            if "draw_result" in _ and os.path.isdir(_):
                for f in os.listdir(_):
                    if f == "gui_diff":
                        with open(os.path.join(_, f), "r", encoding="utf8") as diff_file:
                            for line in diff_file.readlines():
                                if "color=green" in line or "color=red" in line:
                                    diff_apk.append(file)
                                    break
    print(diff_apk)