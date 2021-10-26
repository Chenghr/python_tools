import os

def count_lines(file_path: str, strict=False):
    """统计单个python文件内的有效代码行数

    Args:
        file_path: 文件所在未知的绝对路径；
        strict: true 表示严格统计，排除注释、空行等，只统计纯代码行数；false 则仅排除空行
    Returns:
        count: 代码行数计数
    """
    # 判断文件是否存在
    if os.path.isfile(file_path) == False:
        # 输出文件读取异常的信息
        func_path = os.path.abspath(".")
        raise FileNotFoundError(f"\n File path: {file_path} \n Function path: {func_path} \n Path mismatch.")
    
    count = 0
    tag = False  # 标记是否处于多行注释中

    with open(file_path, encoding='utf-8') as f:

        for line in f:

            line = line.lstrip(' \t')  # 去除字符串左边的空格、制表符
            line = line.rstrip('\n')  # 去除字符串右边的换行

            if not line:
                # 空行则跳过
                continue

            if strict:
                # 执行严格的代码筛选

                if tag == False:
                    # 不处于多行注释中
                    if line[ : 3] == '"""':
                        
                        if len(line) > 3 and line[-3:] != '"""':
                            # 排除一行注释结束的情况，进入多行注释
                            tag = True

                        continue
                    
                    # 排除注释语句
                    if line[0:1] == "#":
                        continue
                    
                    # 排除import语句
                    if line[0:6] == "import" or line[0:4] == "from":
                        continue

                else:
                    # 处在多行注释中，判断是否来到结束终点
                    if line.find('"""') != -1:
                        tag = False
                    continue

            count += 1 

    return count

def count_dir(dir_path: str, detail=True, strict=False):
    """统计文件夹内的有效代码行数

    Args:
        dir_path : str, 要统计的文件夹的绝对路径
        detail : bool, True表示输出每个文件的代码行数；False表示只输出总行数
        strict: bool, true 表示严格统计，排除注释、空行等，只统计纯代码行数；false 则仅排除空行
    Returns:
        fileNum : 文件夹内所有python文件数目
        totalCount : 所有文件代码行数总计
    """
    if os.path.isdir(dir_path) == False:
        raise ValueError("Dir_path not exit.")

    fileNum = 0
    totalCount = 0

    for root, dirs, files in os.walk(dir_path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for file in files:
            file_type = file.split('.')[-1]

            if file_type != 'py':
                continue

            file_path = os.path.join(root, file)

            count = count_lines(file_path, strict)

            fileNum += 1
            totalCount += count

            if detail:
                print(f'{file_path} : {count}')

    return fileNum, totalCount

if __name__ == '__main__':

    dir_path = '/Users/chr/Code/SBT'

    fileNum, totalCount = count_dir(dir_path, detail=True, strict=True)

    #输出结果
    print ("\n------------------------------------")
    print (f'Total python files : {fileNum}')
    print (f'Total lines : {totalCount}')
    print ("------------------------------------")