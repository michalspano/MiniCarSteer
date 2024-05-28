## Developers Note - `src` folder

This document provides further instructions for developers (or anyone
interested in the development process) on the different functionalities
and components placed in the `src` folder.

## Table of Contents

- [Components](#components)
  - [datasets](#datasets)
  - [gym/rf.py](#gymrfpy)
    - [Modifyinig the parameters](#modifyinig-the-parameters)
  - [models](#models)
  - [opendlv](#opendlv)
  - [tests](#tests)
  - [tools](#tools)
  - [app.py](#apppy)
  - [frameData.py](#framedatapy)
  - [predict.py](#predictpy)

## Components

See the following sections for a detailed explanation of each component.

## datasets/*

These are the "raw" datasets of each recording file. Each file contains
a set of columns, with each column denoting a particular **feature**. The
features are:

```txt
groundSteeringRequest
angularVelocityX, angularVelocityY, angularVelocityZ
magneticFieldX, magneticFieldY, magneticFieldZ
accelerationX, accelerationY, accelerationZ
heading
pedal
voltage
distance
```

The delimeter is a comma (`,`). You can treat these as `CSV` files.

## gym/rf.py

This module is responsible for training the Random Forest Regressor learning
model. It produces a `.joblib` file as an artefact. You can invoke training with this module,
with the default parameters, as follows:

```sh
python3 ./src/gym/rf.py
```

### Modifying the hyperparameters

You can adjust any of the following ranges that are used for Grid Search training, this is the default configuration:

```py
param_grid = {
    "n_estimators": [
        500,
    ],
    "max_depth": [None, 2, 3, 4,],
    "min_samples_split": [2, 3,],
    "min_samples_leaf": [1, 2, 3],
    "bootstrap": [True],
}
```

If you would like to expand the number of hyperparameters used during training, you can consult the documentation of
[`scikitlearn`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html).

## models/*

Where the produced modules are stored by default. We provide two *"home-made"*
models, namely `MissingFive.joblib` and `Thor.joblib` (where `Thor` is the
latest model and is the default model and best-performing model used in the program).

## opendlv/*

This module contains the boilerplate transpiled source code from the original
`OpenDLV` (and `libcluon`) `C++` implementation. Additionally,
`OD4Session_init.py`, `OD4callback.py` are extra wrappers that are customised
for the needs of the project. These wrappers employ the distributed `OpenDLV`
implementation.

## tests/*

A set of tests that are used to validate the correctness of the program. The
tests are written in `pytest`. You can navigate to the root and type:

```sh
pytest
```

to run the tests.

## tools/*

A collection of **utility/auxiliary** function used in the project.

## app.py

The **main entry point** of the program. See [`README.md`](../README.md) for
more information about the project as a whole.

## frameData.py

A shareable module that contains the `FrameData` dictionary (i.e. *"object"*)
used among different modules in the project. It contains frame-per-frame data
that is used in the prediction process.

## predict.py

A helper module that employes the model, the selected features, and computes a prediction. T
his module is used in the main entry point of the program (`app.py`).
