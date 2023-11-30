import re


# This class represents directories
class SystemDir:
    def __init__(self, name, parentDir):
        self.type = "directory"
        self.name = name
        self.children = set([])
        self.parentDir = parentDir
        if self.parentDir:
            self.depth = parentDir.depth + 1
        else:
            self.depth = 0

    # Returns self and children
    def __str__(self):
        if self.name == "":
            name = "/"
        else:
            name = self.name
        output = "{}- {} (dir, size={}))".format("  " *
                                                 self.depth, name, self.get_size())
        for child in self.children:
            output += "\n" + str(child)
        return output

    # Add a child node, can be a directory or a file
    def add_child(self, child):
        self.children.add(child)

    # Get the total size of all children
    def get_size(self):
        total_size = 0
        for child in self.children:
            if child.type == "file":
                total_size += child.size
            if child.type == "directory":
                total_size += child.get_size()
        return total_size

    # Get the full path including name
    def get_path_name(self):
        path = ""
        if self.parentDir:
            path += self.parentDir.get_path_name() + "/"
        return "{}{}".format(path, self.name)

    # Recursively build a list of directories within the maximum size constraint
    def get_dirs_set(self, dirs_set, max_size):
        if self.get_size() <= max_size:
            dirs_set.add(self)
        for child in self.children:
            if child.type == "directory":
                dirs_set = child.get_dirs_set(dirs_set, max_size)
        return dirs_set


# This class represents files
class SystemFile:
    def __init__(self, size, name, parentDir):
        self.type = "file"
        self.size = int(size)
        self.name = name
        self.parentDir = parentDir
        if self.parentDir:
            self.depth = parentDir.depth + 1
        else:
            self.depth = 0

    def __str__(self):
        return "{}- {} (file, size={})".format("  " * self.depth, self.name, self.size)


# Scan the terminal output and build a tree that represents the system
def build_system(terminal_output):

    # The root node is hard coded to be the working directory at the start
    root_dir = SystemDir("", None)
    cwd = root_dir
    latest_command = None

    for line in terminal_output:

        elem = re.split(" ", line.strip())

        # Change the working directory
        if elem[0] == "$":
            latest_command = elem

            if elem[1] == "cd":
                if elem[2] == "/":
                    cwd = root_dir
                elif elem[2] == ".." and cwd.parentDir:
                    cwd = cwd.parentDir
                else:
                    for child in cwd.children:
                        if child.name == elem[2]:
                            cwd = child
                            break

        # Use output from the "ls" command to create directories and files at the working directory
        elif latest_command[0] == "$":

            if elem[0] == "dir":
                new_child_dir = SystemDir(elem[1], cwd)
                cwd.add_child(new_child_dir)

            else:
                new_child_file = SystemFile(elem[0], elem[1], cwd)
                cwd.add_child(new_child_file)

    return root_dir


# Sum the total size of directories within the maximum size constraint
def sum_dirs_set(root_dir, max_size):
    dir_set = set([])
    dir_set = root_dir.get_dirs_set(dir_set, max_size)

    sum = 0
    for dir in dir_set:
        sum += dir.get_size()
    return sum


# Find the smallest directory within the maximum and minimum size constraints
def find_smallest_dir(root_dir, max_size, min_size):
    dir_set = set([])
    dir_set = root_dir.get_dirs_set(dir_set, max_size)

    dir_set = sorted(dir_set, key=lambda s: s.get_size())
    for dir in dir_set:
        if dir.get_size() > min_size:
            return dir


with open('07/input.txt') as file:
    terminal_output = file.readlines()

# Build then print a representation of the system
root_dir = build_system(terminal_output)
print("This is what the system looks like:\n\n{}".format(root_dir))

# Part 1 - Finding the sum total size of directories within a size constraint
max_size = 100000

total_size_under_max_size = sum_dirs_set(root_dir, max_size)
print(
    "\nSum of total size of directories with a total size of at most {}: {}".format(
        max_size, total_size_under_max_size
    )
)

# Part 2 - Finding the smallest sized directory that can be deleted to free up enough space
disk_space = 70000000
required_free_disk_space = 30000000

# Find the minimum size constraint
used_disk_space = root_dir.get_size()
free_disk_space = disk_space - used_disk_space
min_required_deletion_size = required_free_disk_space - free_disk_space

# Print out the provided and calculated constraints
print("\nTotal disk space: {}".format(disk_space))
print("Required free disk space: {}".format(required_free_disk_space))
print("Used disk space: {}".format(used_disk_space))
print("Free disk space: {}".format(free_disk_space))
print("Minimum deletion size: {}".format(min_required_deletion_size))

# Find the directory to delete
dir_to_delete = find_smallest_dir(
    root_dir, disk_space, min_required_deletion_size)
print(
    "Total size of smallest directory that can be deleted ({}): {}".format(
        dir_to_delete.get_path_name(),
        dir_to_delete.get_size()
    )
)
