![pipeline status](https://git.chalmers.se/courses/dit638/students/2024-group-09/badges/main/pipeline.svg)

# Cyber-Physical Systems, System of Systems -- Group 9

TODO: add missing sections about the project and the product.

**Improved formatting**

<!-- TODO: Using Docker instead? Revisit the feasibility of the current
     instructions. -->

## Prerequisites

- [`git`][git]
- A compatible `C++` [compiler][cpp-compiler] (e.g. `g++`)
- [`CMake`][cmake]
- [`Docker`][docker]

<!-- LINKS -->
[git]: https://git-scm.com/downloads
[cpp-compiler]: https://gcc.gnu.org/
[cmake]: https://cmake.org/
[docker]: https://docs.docker.com/get-docker/

## Clone the Repository

```sh
git clone git@git.chalmers.se:courses/dit638/students/2024-group-09.git
```

## Build and Run the Program

```sh
# Make an out-of-tree build folder
mkdir build

# Navigate to the build directory
cd build

# Create "Makefile" using the CMakeLists.txt that resides in the root
cmake ..

# Build the program using the generated make
make

# Run the program
./helloworld <integer argument>
```

# Workflow

Our team will use a `Gitlab`-based workflow (with `git` being a central part of
the workflow). Each **feature** will be contained in a separate issue created in
the project's repository hosted on `Gitlab`.

A member of the team (that the issue is assigned to) will be responsible for
the issue. A new *"feature"*-branch will be created for each feature. Once the
feature is completed, a merge request will be initialized and assigned a reviewer
from the team. The reviewer is responsible for (i) providing meaningful feedback on
the changes (ii) and ensuring that the changes are in line with the project
requirements.
Once a merge request is approved, the branch will be merged to the `main` branch.
The `main` branch must, at all times, contain a *"stable"* version of the product.
> When a stable version of the project is created, a tag in the form of `vX.Y.Z`
> will be created. The tag will be created by the team member responsible for
> the issue. The tag will be created after the merge request is approved and the
> branch is merged to the `main` branch. Note that `X`, `Y`, and `Z` are integers
> and represent the major, minor, and patch versions of the project, respectively.

In the case that the pipeline is failing, a merge to the `main` branch is not
allowed. In case that an unexpected behavior occurs on `main` branch, team
members create a new issue and resolve the problem.

## Commit Policy

Each commit message shall include the **number of the issue** and how the commit
is related to that issue. That is:

```sh
git commit -m "#<Issue number> <Commit message>" -m "<Commit description>"
```

## Development team

- @alesaf
- @arumeel
- @spano
- @omidk
