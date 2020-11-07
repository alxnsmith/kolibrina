from pathlib import Path

project_dir = Path().resolve().parent / 'project'


def delete_pycache(path):
    for i in path.iterdir():
        if i.is_dir():
            delete_pycache(i)
        elif i.name.endswith('.pyc'):
            i.unlink()
            print('Deleted:', i.absolute())


if __name__ == "__main__":
    delete_pycache(project_dir)
    print('SUCCESS!')
