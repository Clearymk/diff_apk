import os


def get_stored_path():
    return "D:\\apk_pure\\result"


if __name__ == "__main__":
    for file in os.listdir(get_stored_path()):
        file = os.path.join(get_stored_path(), file)
        flag = False
        for _ in os.listdir(file):
            _ = os.path.join(file, _)
            if _.endswith("json"):
                if os.path.getsize(_) > 359:
                    print(_)
                    flag = True
        if flag:
            for _ in os.listdir(file):
                _ = os.path.join(file, _)
                if _.endswith(".apk"):
                    print(os.path.getsize(_))
            print("--------------------")
