import os
from xml.etree.ElementTree import ElementTree, Element
def read_txt(path):
    file = open(path, 'r')
    data = file.readlines()
    dict = { }
    for data_line in data:
        fileName = data_line.split(' ')[0]
        axis = data_line.split(' ')[1:5]
        dict[fileName] = axis
    return dict

def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def get_selected_bbox(tree, num):
    nodes = tree.findall('object')
    if num > len(nodes):
        print('超限')
        return -1
    node = nodes[num-1]
    xmin = int(node.find('bndbox/xmin').text)
    ymin = int(node.find('bndbox/ymin').text)
    xmax = int(node.find('bndbox/xmax').text)
    ymax = int(node.find('bndbox/ymax').text)
    bbox = [xmin, ymin, xmax, ymax]
    # print(bbox)
    return bbox

def get_bbox(tree):
    nodes = tree.findall('object')
    bbox = []
    for node in nodes:
        xmin = int(node.find('bndbox/xmin').text)
        ymin = int(node.find('bndbox/ymin').text)
        xmax = int(node.find('bndbox/xmax').text)
        ymax = int(node.find('bndbox/ymax').text)
        bbox.append([xmin, ymin, xmax, ymax])
    return bbox

def write_xml(tree, out_path):
    tree.write(out_path)

def set_filename(tree, newname):
    node = tree.find('filename')
    node.text = newname

def set_axis(tree, axis, type):
    nodes = tree.findall('object')
    i = 0
    for node in nodes:
        name = node.find('name')
        name.text = type
        xmin = node.find('bndbox/xmin')
        xmin.text = str(axis[i + 0])
        ymin = node.find('bndbox/ymin')
        ymin.text = str(axis[i + 3])
        xmax = node.find('bndbox/xmax')
        xmax.text = str(axis[i + 1])
        ymax = node.find('bndbox/ymax')
        ymax.text = str(axis[i + 2])
        i = i + 4

def main():
    path = 'I:\\冷轧钢数据\\msos（第二次数据）\\'
    mould_xml = 'mould.xml'
    tree = read_xml(mould_xml)
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            dir_path = os.path.join(path, dir)
            dict = read_txt(dir_path + '\\defect.txt')
            for key in dict:
                set_filename(tree, key + '.jpg')
                set_axis(tree, dict[key], dir)
                out_path = dir_path + '\\' + key + '.xml'
                write_xml(tree, out_path)

def main1():
    path = 'E:\\判级系统\\C608第二批样本\\样本001'
    mould_xml = 'mould.xml'
    tree = read_xml(mould_xml)
    dict = read_txt(path + '\\MSOS.txt')
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            dir_path = os.path.join(path, dir)
            for file in os.listdir(dir_path):
                file = file[0:-4]
                if file in dict.keys():
                    set_filename(tree, file + '.jpg')
                    set_axis(tree, dict[file], dir)
                    out_path = dir_path + '\\' + file + '.xml'
                    write_xml(tree, out_path)

#  批量修改后缀
def modifyName():
    path = 'E:\\判级系统\\C608第二批样本\\样本001'
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            dir_path = os.path.join(path, dir)
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path,file)
                if '.tif' in file_path:
                    newName = file_path[0:-4] + '.jpg'
                    os.rename(file_path, newName)

def fun():
    path = r'E:\判级系统\冷轧钢数据\斑迹'
    # rename
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if '.tif' in file_path:
            newName = file_path[0:-4] + '.jpg'
            os.rename(file_path, newName)

    #remove
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if '.xml' in file_path:
            jpgpath = file_path[0:-4] + '.jpg'
            if not os.path.exists(jpgpath):
                os.remove(file_path)

if __name__ == '__main__':
    # main1()

    # import shutil
    # path = 'E:\\判级系统\\C608第二批样本\\样本001'
    # dstpath = 'E:\\判级系统\\楚'
    # for dir in os.listdir(path):
    #     dirpath = os.path.join(path, dir)
    #     if os.path.isdir(dirpath):
    #         dstdirpath = os.path.join(dstpath, dir)
    #         if not os.path.exists(dstdirpath):
    #             os.makedirs(dstdirpath)
    #         if os.path.isdir(dirpath):
    #             for xmlfile in os.listdir(dirpath):
    #                 if '.xml' in xmlfile:
    #                     xmlpath = dirpath + "\\" + xmlfile
    #                     dstxml = dstdirpath + "\\" + xmlfile
    #                     shutil.copy(xmlpath, dstxml)

    tree = read_xml(r'E:\判级系统\dataProcess\2.xml')
    root = tree.getroot()
    # annotation = tree.find('annotation')

    element = Element('train', {'name': 'wang'})
    one = Element('id')
    one.text = '1'  # 二级目录的值 #结果展示：<id>1</id>
    element.append(one)  # 将二级目录加到一级目录里
    root.append(element)
    tree.write(r'E:\判级系统\dataProcess\2.xml', encoding='utf-8', xml_declaration=True)


    # get_selected_bbox(tree,1)
    # get_bbox(tree)




