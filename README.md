# Cyber-Physical Systems, System of Systems -- Group 9

TODO: add missing sections about the project and the product.

<!-- TODO: Using Docker instead? Revisit the feasibility of the current
     instructions. -->
## Setup `Python` Virtual Environment

Create a `Python` virtual environment:
```sh
python3 -m venv <name> # `venv` is commonly used as <name>
```

*Activate*/ *deactivate* the virtual environment:
```sh
# Activate the venv
source ./<name>/bin/activate

# Deactivate the venv
deactivate
```

## Clone the Repository

```sh
git clone git@git.chalmers.se:courses/dit638/students/2024-group-09.git
```

## Install `pip` Dependencies

```sh
pip3 install -r requirements.txt
```

## Execute the `main` Module

```sh
python3 main.py
# or
./main.py
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
