
from configparser import ConfigParser
import os


class ConfigParserUtils():

    def __init__(self):
        self.conf = ConfigParser(allow_no_value=True, delimiters='=')
        dir_name = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        # os.chdir(self.dir_name)
        self.confile = dir_name + os.sep + 'config' + os.sep + 'jenkins_config.ini'
        print('切换到目录', dir_name)
    def get_config_value_by_key(self, section, key):
        self.conf.read(self.confile,encoding='utf-8')
        # 获取指定的section， 指定的option的值
        key_value = self.conf.get(section, key)
        print('获取%s 节点，%s 的值为 %s' % (section, key, key_value))
        return key_value

    # 获取所有的section
    def get_all_sections_from_config_file(self):
        self.conf.read(self.confile,encoding='utf-8')
        sections = self.conf.sections()
        return sections

    # 更新指定section, option的值
    def update_value_by_section_and_key(
            self, section_name, key, key_value):
        self.conf.read(self.confile,encoding='utf-8')
        self.conf.set(section_name, key, key_value)
        self.conf.write(open(self.confile, 'w'))

    def get_section_value(self, section):
        self.conf.read(self.confile,encoding='utf-8')
        value = self.conf.items(section)
        print(value)

    def readConfigureFile(self):

        # 读取脚本配置文件
        # print("readConfigureFile读取配置文件")
        dictConfMsgTotal = {}
        dictConfMsg = {}
        self.conf.read(self.confile,encoding='utf-8')
        try:
            listSectionName = self.conf.sections()
        except BaseException:
            print("读取配置文件出错")

        else:
            for sectionItem in listSectionName:
                listKeyName = self.conf.options(sectionItem)
                print(listKeyName)
                sectionObj = self.conf[sectionItem]
                if (len(listKeyName) != 0):
                    for keyItem in listKeyName:
                        valueItem = sectionObj[keyItem]
                        if (valueItem is None):
                            dictConfMsg[sectionItem] = listKeyName
                        else:
                            dictConfMsg[keyItem] = valueItem
                else:
                    dictConfMsg[sectionItem] = ''
            # print(dictConfMsg)
        dictConfMsgTotal.update(dictConfMsg)
        # print("dictConfMsgTotal如下")
        # print(dictConfMsgTotal)
        if (len(dictConfMsgTotal) == 0):
            print("未获取到配置文件内容")
        else:
            print("读取到的配置文件信息如下: ")
            print(str(dictConfMsgTotal))
        return dictConfMsgTotal


if __name__ == '__main__':
    C = ConfigParserUtils()
    C.readConfigureFile()
    # C.get_config_value_by_key(
    #     'jenkins_config',
    #     'config' +
    #     os.sep +
    #     'jenkins_config.ini',
    #     'jenkins_url')
    # C.get_section_value(
    #     'config' +
    #     os.sep +
    #     'jenkins_config.ini',
    #     'jenkins_config')
