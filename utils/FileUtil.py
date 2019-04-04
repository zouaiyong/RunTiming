import os

class FileUtil:
    def __init__(self):
        dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(dir_name)
        print('切换到目录', dir_name)
    def read_file(self, file_path):
        #file_path = '../' + file_path
        file_content = open(file_path, mode='r',encoding='utf-8').read()
        return file_content
    def create_file(self, file_path, file_content):
        #file_path = '../' + file_path
        # 如果路径不存在时创建目录
        file_parent = os.path.split(file_path)[0]
        if not os.path.exists(file_parent):
            os.makedirs(file_parent)
        f = open(file_path, 'a',encoding='utf-8')
        f.write(file_content)
        f.close()
if __name__ == '__main__':
    a = FileUtil()
    print(a.read_file('config'+os.sep+'jenkins_config.ini'))
    a.create_file('config'+os.sep+'testdir'+os.sep+'jenkins_config.txt','jdkwljglw')