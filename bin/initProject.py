from pathlib import Path


class InitProject:
    BASE_DIR = Path(__file__).parent.parent / 'project'

    def __call__(self, *args, **kwargs):
        self.init_users_folder()
        self.init_banners_folder()

    def init_banners_folder(self):
        path = self.BASE_DIR / 'mediacontent' / 'banners'
        if not path.is_dir():
            path.mkdir(parents=True)

    def init_users_folder(self):
        path = self.BASE_DIR / 'mediacontent' / 'users'
        if not path.is_dir():
            path.mkdir(parents=True)


def main():
    init = InitProject()
    init()


if __name__ == "__main__":
    main()
