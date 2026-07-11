import gzip


def open_log_file(path):

    if path.endswith(".gz"):

        return gzip.open(
            path,
            "rt",
            encoding="utf-8"
        )


    return open(
        path,
        "r",
        encoding="utf-8"
    )