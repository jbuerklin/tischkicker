from django.contrib.staticfiles.finders import AppDirectoriesFinder


class ViteAwareFinder(AppDirectoriesFinder):
    """Doesn't list js and css files because they are handled by vite."""

    def list(self, ignore_patterns):
        for path, storage in super().list(ignore_patterns):
            ext = path.split(".")[-1]
            if not path.startswith("admin/") and ext in ("js", "css", "scss"):
                continue
            yield path, storage
