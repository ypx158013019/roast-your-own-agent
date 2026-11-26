"""Write the make.fun competition entry."""

import errno
import tempfile
from pathlib import Path


FALLBACK_ERRNOS = frozenset({errno.EACCES, errno.EPERM, errno.EROFS})

ROAST = (
    "I asked my AI agent to delete a blank line. "
    "It billed me for a moment of silence."
)


def write_entry(directory: Path) -> None:
    """Stage the roast and atomically replace entry.txt in the given directory."""
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=directory) as staging_directory:
        staged_entry = Path(staging_directory) / "entry.txt"
        staged_entry.write_bytes((ROAST + "\n").encode("utf-8"))
        staged_entry.chmod(0o644)
        staged_entry.replace(directory / "entry.txt")


def main() -> None:
    """Try /output first, then ./output on permission or read-only errors."""
    try:
        write_entry(Path("/output"))
    except OSError as error:
        if error.errno not in FALLBACK_ERRNOS:
            raise
        write_entry(Path("output"))


if __name__ == "__main__":
    main()
