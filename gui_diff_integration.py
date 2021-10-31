from format_xml_recursive import XMLFormatter
from draw_gui_graph import DrawGUIGraph
from gui_diff import GUIDiff
import os


def get_res_path():
    return "D:\\test"


def get_format_task():
    format_tasks = []
    for file in os.listdir(get_res_path()):
        file = os.path.join(get_res_path(), file)
        if os.path.isdir(file):
            task_xml = []
            for _ in os.listdir(file):
                _ = os.path.join(file, _)
                if _.endswith(".xml"):
                    task_xml.append(_)
            if len(task_xml) == 2:
                format_tasks.append(task_xml)
    return format_tasks


def get_format_result_path(file_path):
    return file_path.replace(_.split("\\")[-1], "format_result\\" + _.split("\\")[-1])


def get_diff_result_path(file_path, name_a, name_b):
    result_dir = file_path.replace(file_path.split("\\")[-1], "")
    result_dir = result_dir.removesuffix("\\")
    result_dir = result_dir.replace(result_dir.split("\\")[-1], "diff_result\\")
    return result_dir + name_a + "_" + name_b + ".xml"


def get_draw_result_path(file_path):
    result_dir = file_path.replace(file_path.split("\\")[-1], "")
    result_dir = result_dir.removesuffix("\\")
    result_dir = result_dir.replace(result_dir.split("\\")[-1], "draw_result\\")
    return result_dir


def get_diff_file_name(file_path):
    return file_path.split("\\")[-1].replace(".xml", "")


if __name__ == "__main__":
    format_tasks = get_format_task()
    diff_tasks = []
    draw_tasks = []

    for format_task in format_tasks:
        temp = []
        for _ in format_task:
            format_result_path = get_format_result_path(_)
            xml_format = XMLFormatter(_, format_result_path)
            xml_format.sort()
            temp.append(format_result_path)
        diff_tasks.append(temp)

    for diff_task in diff_tasks:
        apk_name_a = get_diff_file_name(diff_task[0])
        apk_name_b = get_diff_file_name(diff_task[1])
        diff_result_path = get_diff_result_path(diff_task[0], apk_name_a, apk_name_b)
        diff = GUIDiff(diff_task[0], diff_task[1], diff_result_path)
        diff.start_diff()
        draw_tasks.append(diff_result_path)

    for draw_task in draw_tasks:
        dgg = DrawGUIGraph(draw_task, get_draw_result_path(draw_task))
        dgg.start_draw()