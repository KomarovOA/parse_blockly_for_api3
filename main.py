import os
import xml.etree.ElementTree as ET
import json

path_in = 'C:\\Repository\\ini_1c_blockly'
path_out = 'C:\\test_ini\\'
text = ''
last_conf = ''
wrong_obj_without_api3 = ''



def parse_blockly():
    global path_in, text, last_conf, wrong_obj_without_api3

    with open("api3_accord", "r", encoding="utf-8") as f:
        api3_accord = json.load(f)

    for root_dir, dirs, files in os.walk(path_in):  # '.' — текущая папка
        for file in files:
            main_objects = {file: {}}
            subs = ['Blockly', '_read']
            if all(sub in file for sub in subs):
                conf = file[file.find('Dom1C')+5:file.find('_Blockly')]
                pretty_name = file[file.find('Blockly')+8:file.find('_read')]
                tree = ET.parse(root_dir + '\\' + file)
                root = tree.getroot()

                def strip_ns(elem):
                    if isinstance(elem.tag, str) and elem.tag.startswith("{"):
                        elem.tag = elem.tag.split("}", 1)[1]
                    for child in list(elem):
                        strip_ns(child)

                strip_ns(root)
                objects = main_objects[file]
                for block in root.findall(".//block[@type]"):
                    if "type" in block.attrib and "api3_" in block.get("type") and not "api3_link" == block.get("type"):
                        if objects.get(block.get("type")) is None:
                            objects[block.get("type")] = []
                        for value in block.findall("./value"):
                            if value.get("name") not in ['ТипИС', 'ИмяИС', 'ИдИС', 'INIT_VALUE', 'ИдСБИС', 'ИмяСБИС']:
                                objects[block.get("type")].append(value.get("name"))

                check_conf = last_conf != conf or last_conf == ''
                conf_name = last_conf + '\n' if check_conf else ''
                last_conf = conf

                if objects:
                    if check_conf:
                        text = text + conf + '\n'

                    text = text + pretty_name + '\n'
                    for key, value in objects.items():
                        # if api3_accord.get(key) is None:
                        #     print(key)
                        text = text + f"{api3_accord.get(key)}: {value}" + '\n'
                    text = text + '\n'
                else:
                    conf_name = last_conf + '\n' if check_conf else ''
                    wrong_obj_without_api3 = wrong_obj_without_api3 + conf_name + '     ' + pretty_name + '\n'

    #  Записываем список объектов по конфам где какие реквизиты в каких АПИ3 объектах используется
    with open(path_out + '\\СписокРеквизитовВсехЗагружаемыхОбъектов.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    #  Записываю в каких инишках вообще нет используемых АПИ3 объектов. Значит такие блоки необходимо создать
    with open(path_out + '\\ВозможныеДоработки.txt', 'w', encoding='utf-8') as fail:
        fail.write(wrong_obj_without_api3)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_blockly()
