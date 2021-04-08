# -*- coding: UTF-8 -*-
import os
import re


def get_plurals_files(file_dir: str, end_width='plurals_strings.xml'):
    """
    获取单复数字符串文件
    :param file_dir:
    :param end_width:
    :return:
    """
    file_list = []
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            filepath = os.path.join(parent, filename)
            filepath = filepath.replace('\\', '/')
            if filepath.endswith('plurals_strings.xml'):
                file_list.append(filepath)
    return file_list


def move_string(source_dir: str, dest_dir: str, string: str):
    """
    移动字符串
    :param source_dir:
    :param dest_dir:
    :param string:
    :return:
    """
    '''
    <plurals name="duration_hours_relative">
        <item quantity="other">%d 小时前</item>
    </plurals>
    '''
    source_plurals_files = get_plurals_files(source_dir)
    dest_plurals_files = get_plurals_files(dest_dir)
    lang_pattern = r'/res/(?P<lang>values.*?)/plurals_strings.xml'
    # 起点
    start_value = '<plurals name="%s"' % string
    # 内容
    item_value = '<item'
    # 终点
    end_value = '</plurals>'
    print(source_plurals_files)
    print(dest_plurals_files)
    for source_file in source_plurals_files:
        source_search = re.search(lang_pattern, source_file)
        for dest_file in dest_plurals_files:
            # 判断是否未同一个语言
            dest_search = re.search(lang_pattern, dest_file)
            if source_search and dest_search and source_search.group(0) == dest_search.group(0):
                print('同一个语言：[%s, %s]' % (source_file, dest_file))
                with open(source_file, 'r', encoding='utf-8') as sf:
                    source_lines = sf.readlines()
                source_lines_copy = source_lines.copy()
                is_start = False
                is_end = False
                remove_lines_index = []
                last_line = '###'
                for index, source_line in enumerate(source_lines):
                    if start_value in source_line:
                        is_start = True
                        is_end = False
                        if not last_line or not last_line.strip():
                            # 上一行为空
                            remove_lines_index.append(index - 1)
                        remove_lines_index.append(index)
                    if not is_start:
                        # 未开始
                        last_line = source_line
                        continue
                    if is_start and item_value in source_line:
                        # 内容
                        remove_lines_index.append(index)
                    if is_start and end_value in source_line:
                        # 终点
                        is_end = True
                        remove_lines_index.append(index)
                    if is_end:
                        # 开始删除字符串
                        is_start = False
                        is_end = False
                        for idx, remove_index in enumerate(remove_lines_index):
                            pop = source_lines.pop(remove_index - idx)
                            print(pop)
                        with open(source_file, 'w', encoding='utf-8') as sf:
                            sf.writelines(source_lines)


if __name__ == '__main__':
    source_dir = 'E:/AndroidSpace/LanguageDemo/ConponentReady/src/main/res'
    dest_dir = 'E:/AndroidSpace/LanguageDemo/Conponent/src/main/res'
    string = 'duration_days_shortest'
    move_string(source_dir, dest_dir, string)
