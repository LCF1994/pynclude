import os
ROOT = os.path.join(os.environ['BD'], 'dados')

def add_include(folder:str, dat:str, target_file_path:str) -> None:
    try:
        with open(target_file_path, 'r+') as f:
            content = f.readlines()
            include = f'#include {folder}/{dat}'
            if include not in content:
                new_content = '\n'.join([include, content])
                f.seek(0)
                f.write(new_content)
    except FileNotFoundError:
        with open(target_file_path, 'w') as f:
            include = f'#include {folder}/{dat}'
            f.write(include)


def locate_include(target_file_path:str, folder:str, dat:str) -> tuple:
    with open(target_file_path, 'r') as main_file:
        content = main_file.readlines()
        include = f'#include {folder}/{dat}'
        for index, line in enumerate(content):
            if include in line:
                return index, content
        return None, content

def compute_mul_order(content) -> None:
    pass


def update_content(include_location: int, file_content:list) -> str:
    file_content.pop(include_location)
    return '\n'.join(file_content)


def rewrite_file(new_content:str, target_file_path:str, tmp_file_path:str) -> None:
    with open(tmp_file_path, 'w') as tmp_file:
        tmp_file.write(new_content)
    os.remove(target_file_path)
    os.rename(tmp_file_path, target_file_path)


def remove_include(target_file_path:str, folder:str, dat:str, tmp_file_path:str) -> None:
    include_location, file_content = locate_include(target_file_path, folder, dat)
    if include_location != None:
        new_content = update_content(include_location, file_content)
        if new_content:
            rewrite_file(new_content, tmp_file_path)
        else:
            os.remove(target_file_path)
            
def add_from_folder(folder:str) -> None:
    folder_path = os.path.join(ROOT, folder)
    dats = [ file for file in os.listdir(folder_path) if file.endswith('.dat') ]
    
    for dat in dats:
        root_dat_path = os.path.join(ROOT, dat)
        add_include(folder, dat, root_dat_path)

def remove_from_folder(folder:str) -> None:
    folder_path = os.path.join(ROOT, folder)
    dats = [ file for file in os.listdir(folder_path) if file.endswith('.dat') ]
    
    for dat in dats:
        root_dat_path = os.path.join(ROOT, dat)
        tmp_dat_path = os.path.join(ROOT, 'tmp_' + dat)
        remove_include(root_dat_path, folder, dat, tmp_dat_path)


def add_all() -> None:
    #folder_list = list(filter(lambda x: os.path.isdir(os.path.join(ROOT, x)) and not ('dump' in x), os.listdir(ROOT)))
    folder_list = [ item for item in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT,item)) and 'dump' not in item ]

    for folder in folder_list:
        add_from_folder(folder)


def remove_all() -> None:
    from subprocess import run
    run('rm -rf $BD/dados/*.dat', shell=True)


if __name__ == '__main__':
    remove_all()
    add_all()
