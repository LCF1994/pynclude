import os, re

try:
    ROOT = os.path.join(os.environ['BD'], 'dados')
except KeyError:
    ROOT = os.path.join('.', 'test','dados')


# Tested

def extrac_mul_orders(content:list) -> list:
    order_list = []
    for line in content:
        if 'ORDEM' in line:
            try:  
                order_list.extend(re.findall(r'\d+', line))
            except AttributeError:
                continue
    return order_list 


def build_mul_comment(include_orders:list) -> str:
    return f"   ; {', '.join(include_orders)}"


def comment_with_order_values(folder:str) -> None:
    try:
        file_path = os.path.join(ROOT, folder, 'mul.dat')
        with open(file_path, 'r+') as f:
            content = f.readlines()
            order_values = extrac_mul_orders(content)
            comment = build_mul_comment(order_values)
            return comment
    except FileNotFoundError:
        print('mul not found')


def list_all_folders_to_include(root_path:str) -> list:
    return [ item for item in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, item)) and 'dump' not in item ]


def list_dats_in_folder(folder_path:str) -> list:
    return [ file for file in os.listdir(folder_path) if file.endswith('.dat') ]


def add_all() -> None:
    folder_list = list_all_folders_to_include(ROOT)

    for folder in folder_list:
        add_from_folder(folder)


def add_from_folder(folder:str) -> None:
    folder_path = os.path.join(ROOT, folder)
    dats = list_dats_in_folder(folder_path)
    
    for dat in dats:
        if 'mul' not in dat:
            add_include(folder, dat)
        else:
            add_include(folder, dat)


def read_file(file_path:str) -> list:
    with open(file_path, 'r+') as file:
        return file.readlines()


def write_file(file_path:str, content:list) -> None:
    with open(file_path, 'w+') as file:
        file.writelines(content)


def add_include(folder:str, dat:str) -> None:
    path_dat_root = os.path.join(ROOT, dat)
    include = f'#include {folder}/{dat}\n'

    if os.path.isfile(path_dat_root):
        content = read_file(path_dat_root)
            
        if include not in content:
            content.insert(0, include)
            write_file(path_dat_root, content)

    else:
        write_file(path_dat_root, include)


def locate_include(content:list, target:str):
    try:
        return content.index(target)
    except ValueError:
        return None

# In Test



# Not Tested  

# def update_content(include_location: int, file_content:list) -> str:
#     file_content.pop(include_location)
#     return '\n'.join(file_content)


# def rewrite_file(new_content:str, target_file_path:str, tmp_file_path:str) -> None:
#     with open(tmp_file_path, 'w') as tmp_file:
#         tmp_file.write(new_content)
#     os.remove(target_file_path)
#     os.rename(tmp_file_path, target_file_path)


# def remove_include(target_file_path:str, folder:str, dat:str, tmp_file_path:str) -> None:
#     include_location, file_content = locate_include(target_file_path, folder, dat)
#     if include_location != None:
#         new_content = update_content(include_location, file_content)
#         if new_content:
#             rewrite_file(new_content, tmp_file_path)
#         else:
#             os.remove(target_file_path)
            

# def remove_from_folder(folder:str) -> None:
#     folder_path = os.path.join(ROOT, folder)
#     dats = [ file for file in os.listdir(folder_path) if file.endswith('.dat') ]
    
#     for dat in dats:
#         root_dat_path = os.path.join(ROOT, dat)
#         tmp_dat_path = os.path.join(ROOT, 'tmp_' + dat)
#         remove_include(root_dat_path, folder, dat, tmp_dat_path)


def remove_all() -> None:
    path_list = [ os.path.join(ROOT, dat) for dat in list_dats_in_folder(ROOT)]

    for dat_path in path_list:
        os.remove(dat_path)


if __name__ == '__main__':
    remove_all()
    add_all()
