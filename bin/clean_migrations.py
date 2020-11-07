from pathlib import Path
import shutil

project = Path().resolve().parent / 'project'


def print_deleted(path):
    print('Deleted:', path)


def delete_migrations(path):
    for i in path.iterdir():
        if i.is_dir():
            delete_migrations(i)
        if i.resolve().parent.name == 'migrations':
            if i.name == '__pycache__':
                shutil.rmtree(i)
                print_deleted(i)
            elif i.name != '__init__.py':
                i.unlink()
                print_deleted(i)
        if i.name.endswith('.sqlite3'):
            i.unlink()
            print_deleted(i)


if __name__ == '__main__':
    delete_migrations(project)
    print('SUCCESS!')
