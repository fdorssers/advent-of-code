from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from more_itertools import flatten

from utils import load_data
from utils import print_result


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    dirs: list[Directory] = field(default_factory=list)
    files: list[File] = field(default_factory=list)

    @property
    def size(self) -> int:
        return sum([d.size for d in self.dirs] + [f.size for f in self.files])

    def dir(self, name: str) -> Directory:
        return next(d for d in self.dirs if d.name == name)

    def create_dir(self, name: str) -> None:
        if not any(d.name == name for d in self.dirs):
            self.dirs.append(Directory(name))

    def create_file(self, name: str, size: int) -> None:
        if not any(f.name == name for f in self.files):
            self.files.append(File(name, size))


def get_cwd(structure: Directory, path: list[str]) -> Directory:
    cwd = structure
    for p in path:
        cwd = cwd.dir(p)
    return cwd


def parse_data(lines: list[str]) -> Directory:
    structure = Directory("/")
    current_path: list[str] = []
    cwd = structure
    for line in lines[1:]:
        if line.startswith("$ cd .."):
            current_path = current_path[:-1]
            cwd = get_cwd(structure, current_path)
        elif line.startswith("$ cd "):
            current_path.append(line[5:])
            cwd = get_cwd(structure, current_path)
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir "):
            cwd.create_dir(line[4:])
        else:
            size, name = line.split(" ")
            cwd.create_file(name, int(size))
    return structure


def get_sizes(structure: Directory) -> list[int]:
    return [structure.size] + list(flatten(get_sizes(d) for d in structure.dirs))


def part1(structure: Directory) -> int:
    return sum([size for size in get_sizes(structure) if size <= 100000])


def part2(structure: Directory) -> int:
    space_needed = 30000000 - (70000000 - structure.size)
    return next(size for size in sorted(get_sizes(structure)) if (space_needed - size) < 0)


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 95437
    print_result(1, part1(data))

    assert part2(example_data) == 24933642
    print_result(2, part2(data))
