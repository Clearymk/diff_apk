import os

tasks = []


def get_stored_path():
    return "G:\\apk_pure\\t"


def run_jar(apk_1, apk_2):
    os.chdir("G:\\apk_pure")
    command = "java -jar SimiDroid.jar %s %s" % (apk_1, apk_2)
    print(os.popen(command).read())


def get_task():
    for file in os.listdir(get_stored_path()):
        file = os.path.join(get_stored_path(), file)
        if os.path.isdir(file):
            task = []
            for _ in os.listdir(file):
                _ = os.path.join(file, _)
                if _.endswith(".apk"):
                    task.append(_)
            tasks.append(task)


if __name__ == "__main__":
    get_task()
    for task in tasks:
        run_jar(task[0], task[1])
