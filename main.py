import os
import xml.etree.ElementTree as ET

path = 'C:/test_ini'
text = ''
last_conf = ''


def parse_blockly():
    global path, text, last_conf
    entries = os.listdir(path)
    for file in entries:
        main_objects = {file: {}}
        subs = ['Blockly', '_read']
        if all(sub in file for sub in subs):
            conf = file[file.find('Dom1C')+5:file.find('_Blockly')]
            pretty_name = file[file.find('Blockly')+8:file.find('_read')]
            tree = ET.parse('C:/test_ini/' + file)
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
                    objects[block.get("type")] = []
                    for value in block.findall("./value"):
                        if value.get("name") not in ['ТипИС', 'ИмяИС', 'ИдИС']:
                            objects[block.get("type")].append(value.get("name"))

            if last_conf != conf or last_conf == '':
                text = text + conf + '\n'

            last_conf = conf
            text = text + pretty_name + '\n'
            for key, value in objects.items():
                text = text + f"{key}: {value}" + '\n'
            text = text + '\n'
            with open(path + '/file.txt', 'w', encoding='utf-8') as f:
                f.write(text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_blockly()
