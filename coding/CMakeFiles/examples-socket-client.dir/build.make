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

# Include any dependencies generated for this target.
include CMakeFiles/examples-socket-client.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/examples-socket-client.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/examples-socket-client.dir/flags.make

CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o: CMakeFiles/examples-socket-client.dir/flags.make
CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o: examples/libh2o/socket-client.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/rome/h2O/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o   -c /home/rome/h2O/examples/libh2o/socket-client.c

CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/rome/h2O/examples/libh2o/socket-client.c > CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.i

CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/rome/h2O/examples/libh2o/socket-client.c -o CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.s

CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.requires:
.PHONY : CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.requires

CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.provides: CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.requires
	$(MAKE) -f CMakeFiles/examples-socket-client.dir/build.make CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.provides.build
.PHONY : CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.provides

CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.provides.build: CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o

# Object files for target examples-socket-client
examples__socket__client_OBJECTS = \
"CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o"

# External object files for target examples-socket-client
examples__socket__client_EXTERNAL_OBJECTS =

examples-socket-client: CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o
examples-socket-client: CMakeFiles/examples-socket-client.dir/build.make
examples-socket-client: libh2o.a
examples-socket-client: /usr/local/lib/libssl.a
examples-socket-client: /usr/local/lib/libcrypto.a
examples-socket-client: /usr/lib/x86_64-linux-gnu/libuv.so
examples-socket-client: CMakeFiles/examples-socket-client.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable examples-socket-client"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/examples-socket-client.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/examples-socket-client.dir/build: examples-socket-client
.PHONY : CMakeFiles/examples-socket-client.dir/build

CMakeFiles/examples-socket-client.dir/requires: CMakeFiles/examples-socket-client.dir/examples/libh2o/socket-client.c.o.requires
.PHONY : CMakeFiles/examples-socket-client.dir/requires

CMakeFiles/examples-socket-client.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/examples-socket-client.dir/cmake_clean.cmake
.PHONY : CMakeFiles/examples-socket-client.dir/clean

CMakeFiles/examples-socket-client.dir/depend:
	cd /home/rome/h2O && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/rome/h2O /home/rome/h2O /home/rome/h2O /home/rome/h2O /home/rome/h2O/CMakeFiles/examples-socket-client.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/examples-socket-client.dir/depend

