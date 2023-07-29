

import sys
from pathlib import Path
from normalize import normalize
import uuid
import shutil


CATEGORIES = {
    'images': ['.jpeg', '.png', '.jpg', '.svg'],
    'videos': ['.avi', '.mp4', '.mov', '.mkv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar']
}


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(
            f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)
    print(f'file moved to {target_dir}, new name: {new_name.stem}{file.suffix}')


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return 'other'


def sort_folder(path) -> None:
    for item in path.glob('**/*'):
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def delete_empty_folders(folder: Path) -> None:
    for subfolder in folder.iterdir():
        if subfolder.is_dir():
            delete_empty_folders(subfolder)
    if not any(folder.iterdir()):
        print(f'delete folder: {folder}')
        folder.rmdir()


def unpack_archive(folder: Path) -> None:
    archives_dir = folder.joinpath('archives')
    if not archives_dir.exists():
        return
    for item in archives_dir.glob('**/*'):
        if item.is_file() and item.suffix.lower() in ['.zip', '.gz', '.tar']:
            target_dir = archives_dir.joinpath(item.stem)
            target_dir.mkdir(exist_ok=True)
            shutil.unpack_archive(str(item), str(target_dir))
            item.unlink()
            print(f'archive unpacked in: {target_dir}')


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'No path to folder'

    if not path.exists():
        return f'Folder with path {path} dos\'n exist'

    sort_folder(path)
    delete_empty_folders(path)
    unpack_archive(path)

    return 'All Ok'


if __name__ == '__main__':
    print(main())