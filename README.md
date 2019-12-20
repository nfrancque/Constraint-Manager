# Constraint Manager

A simple yaml-based tool for generating sdc interface constraints.  No math involved!

## Goals

Provide an easy to use tool that requires minimal user input when constraining a design and reduce human error significantly.

## Current State

Rudimentary support for create_generated_clk and set_input_delay -max

Output is created, frameworks all set up, need to refine

Sample design/interface/part (not accurate) provided to generate output


## TODO

Finish out constraint equations

Get ease of use input from others, especially with the variable substitution

Get documentation built

Make it a GUI?

## Development Guide

To install the module (errors pop up on relative imports when not used as module, current workaround is simply to reinstall for changes):

`python3.8 setup.py install --user`

To use it on the command line:

`constraint-manager -h`

To test:

`pytest`
