"""
 * @2021-06-25 15:42:33
 * @Author       : mahf
 * @LastEditTime : 2022-04-18 16:16:38
 * @FilePath     : /epicgames-claimer/config-yaml.py
 * @Copyright 2021 mahf, All Rights Reserved.
"""
from ruamel.yaml import YAML


def read_yaml_file(file_path):
    """
    读取yaml文件
    :param file_path:
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

        # 解析yaml文件
        # 类型：ordereddict
        yaml = YAML()
        result = yaml.load(data)
        # print(result)
        return result


def write_to_yaml_file(content, file_path):
    """
    写入到yaml文件中
    :param content:
    :param file_path:
    :return:
    """

    # 写入到文件中
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml = YAML()
        yaml.dump(content, file)

if __name__ == '__main__':
    ret = read_yaml_file(r'./ptconfig.yaml')
    print(ret['pterclub'])