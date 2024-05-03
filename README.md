![pipeline status](https://git.chalmers.se/courses/dit638/students/2024-group-09/badges/main/pipeline.svg)

# Cyber-Physical Systems, System of Systems -- Group 9

TODO: add missing sections about the project and the product.

## Prerequisites

- [`git`][git]
- [`Docker`][docker]
- [`Python`][python] (for local development)
- A **web browser** (preferably Chrome or Firefox)

<!-- LINKS -->
[git]: https://git-scm.com/downloads
[docker]: https://docs.docker.com/get-docker/
[python]: https://www.python.org/downloads/

## Installation

Initially, you have to `pull` the image:

```sh
# TODO: add the registry
```

Having installed the image, you can use a **shell script** to run it:
```sh
# Default command-line arguments
./scripts/run.sh

# See the usage, pass command-line arguments
./scripts/run.sh --help
```

If you prefer to **build** the image locally, you can use this script instead:
```sh
./scripts/build.sh
```

## Local Development

You're similarly encouraged to locally engage with the system. You may start
cloning repository:

```sh
git clone git@git.chalmers.se:courses/dit638/students/2024-group-09.git
# TODO: add GiHub mirror
```

### Run the program

It is preferred to create a `python`-based virtual environment, hence:
```sh
# 1.) From the root
python3 -m venv venv

# 2.) Activate the venv
source ./venv/bin/activate

# 3.) Install the dependencies inside venv
pip3 install -r requirements.txt

# 4.) Naviagate to the source directory
cd src

# 5.) Run the program
./app.py
# or python3 app.py

# 6.) See program's usage
./app.py --help
```

### Miscellaneous

There's some additional functionality that you can use:

```sh
# 1.) Run the application with `--graph` flag
./app.py --graph
# ./app.py -g
# This will create a log file with the parameters.

# 2.) Compute a performance metric
# Generates a static PNG file with the performance metric in the current
# directory.
./src/tools/graph-generator/app.py
```

Additionally, more related to the development process, you can use the
following:

```sh
# 1.) Run the tests
# TODO: add instructions

# 2.) Run the coverage report generation
# Generate an HTML-based report in the current directory.
cd src
../scripts/coverage.sh
```

## Microservices

Our program is combined with two other microservices, each responsible for a
specific task. The microservices are:

- [`OpenDLV-Vehicle-View`][opendlv-vehicle-view]
- [`OpenDLV-Video-H264-Decoder`][opendlv-video-h264-decoder]

<!-- LINKS -->
[opendlv-vehicle-view]: https://github.com/chalmers-revere/opendlv-vehicle-view
[opendlv-video-h264-decoder]: https://github.com/chalmers-revere/opendlv-video-h264-decoder

Ensure that you have the required microservices installed and running.
You can use the following **shell scripts** to start the microservices:

```sh
# 1.) Start OpenDLV-Vehicle-View
./scripts/init_opendlv.sh

# 2.) Start OpenDLV-Video-H264-Decoder
./scripts/init_h264-decoder.sh
```

Afterwards, navigate to your browser and open `localhost` (or it's equivalent)
with the port `8081` and select a `.rec` file to instantiate the vehicle view.

Please consult the [Chalmers ReVeRe](https://github.com/chalmers-revere) GitHub
repositories for more information in terms of the microservices.

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

---
