# Constraint Manager

A simple yaml-based tool for generating sdc interface constraints.  No math involved!

## Installation

Prerequisites:

`setuptools`

`Python>=3.6`

To install the module

`python setup.py install`

## Usage
For immediate usage, try:

`constraint-manager generate sample`

This will use a sample interface, part, and design to generate some constraints (not yet validated) and just print them to the console.

An example flow for generating your own interface, part and design:

```
constraint-manager create interface test
constraint-manager create part test --interfaces test
constraint-manager create design test --interfaces test
```
Manually edit constraint\_manager\_out/designs/test_test.yaml to say `part: test`

`constraint-manager generate test`

The generated constraints will be empty, but this shows the flow and you can manually modify the yaml's to your liking to try out something new - be sure to regenerate parts and designs after modifying an interface.

Ideally, all local repositories will be merged back upstream to store them in the tool.  This is where the real benefit of it comes into play.



## Goals

Provide an easy to use tool that requires minimal user input when constraining a design and reduce human error significantly.

## Current State

All but mult_path constraints implemented

Can create, list, and generate from cli

Sample design/interface/part (not accurate) provided to generate output


## TODO

- [ ] Validate constraint equations

- [ ] Get real example to see if numbers match up

- [ ] Improve unit testing

- [ ] Get ease of use input from others, especially with the variable substitution

- [ ] Get documentation built

- [ ] Programmatic editing of configuration files

- [ ] Figure out why argcomplete doesn't work

- [ ] Better design generation - give interfaces a name, set part at creation time

- [ ] Make it a GUI?


## Development Guide

Constraint Manager uses pytest.

To test for the first time (installs required test modules):

`python3.8 setup.py test`

To fully use framework with all options after setup.py installs, simply use:

`pytest`

## Contributing

I welcome any and all contributions.  The tests in particular need overhauled, they are only very simple sanity checks as of now.

