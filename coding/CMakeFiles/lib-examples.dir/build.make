# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/rome/h2O

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/rome/h2O

# Utility rule file for lib-examples.

# Include the progress variables for this target.
include CMakeFiles/lib-examples.dir/progress.make

CMakeFiles/lib-examples: examples-http1client
CMakeFiles/lib-examples: examples-simple
CMakeFiles/lib-examples: examples-socket-client

lib-examples: CMakeFiles/lib-examples
lib-examples: CMakeFiles/lib-examples.dir/build.make
.PHONY : lib-examples

# Rule to build all files generated by this target.
CMakeFiles/lib-examples.dir/build: lib-examples
.PHONY : CMakeFiles/lib-examples.dir/build

CMakeFiles/lib-examples.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/lib-examples.dir/cmake_clean.cmake
.PHONY : CMakeFiles/lib-examples.dir/clean

CMakeFiles/lib-examples.dir/depend:
	cd /home/rome/h2O && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/rome/h2O /home/rome/h2O /home/rome/h2O /home/rome/h2O /home/rome/h2O/CMakeFiles/lib-examples.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/lib-examples.dir/depend
