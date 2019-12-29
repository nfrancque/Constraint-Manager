# Constraint Manager

A simple yaml-based tool for generating sdc interface constraints.  No math involved!


## Usage
For immediate usage, try:

`constraint-manager generate test`

This will use a sample interface, part, and design to generate some constraints (not yet validated)

To create new specifications, use 

`constraint-manager create`

and through the cli you can create a new interface, part, and design that reference each other and use generate to test them.



## Goals

Provide an easy to use tool that requires minimal user input when constraining a design and reduce human error significantly.

## Current State

All but mult_path constraints implemented

Can create, list, and generate from cli

Sample design/interface/part (not accurate) provided to generate output


## TODO

Validate constraint equations

Get real example to see if numbers match up


Get ease of use input from others, especially with the variable substitution

Get documentation built

Make it a GUI?


## Development Guide

Prerequisites:

`~/.local/bin` must be in $PATH (python installs binaries here)
setuptools must be installed


To install the module (errors pop up on relative imports when not used as module, current workaround is simply to reinstall for changes):

`python3.8 setup.py install --user`

To use it on the command line:

`constraint-manager -h`

To test for the first time (installs required test modules):

`python3.8 setup.py test`

To fully use framework with all options after setup.py installs, simply use:

`pytest`
