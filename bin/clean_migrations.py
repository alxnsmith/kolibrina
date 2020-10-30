import os, shutil


def get_project_path():
    path = os.getcwd()  # current dir
    path = os.path.dirname(path)  # to parent dir
    path = os.path.join(path, 'project')
    return path


def migrations_walker():
    walker = os.walk(get_project_path())
    for i in walker:
        if os.path.basename(i[0]) == 'migrations':
            yield i


def contain(directory):
    new = {'dir': '', 'elems': []}
    for index, i in enumerate(directory):
        if index == 0:
            new['dir'] = i
            continue
        if type(i) in (list, tuple):
            for subdir in i:
                new['elems'].append(subdir)
    return new


def delete_migrations_and_cache(walker):
    for directory in walker:
        directory = contain(directory)

        elems = directory['elems']
        elems.pop(elems.index('__init__.py'))
        directory = directory['dir']

        for elem in elems:
            path = os.path.join(directory, elem)
            try:
                os.remove(path)
            except IsADirectoryError:
                shutil.rmtree(path)
            print('Deleted: ', path)


def delete_db():
    os.remove(os.path.join(get_project_path(), 'db.sqlite3'))
    print('DATABASE deleted')


if __name__ == '__main__':
    walker = migrations_walker()

    delete_migrations_and_cache(walker)
    delete_db()