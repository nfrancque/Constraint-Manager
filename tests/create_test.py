import sys
from os.path import exists as path_exists
from os.path import join as path_join
from shutil import rmtree

import pytest

from constraint_manager import create
from helpers.utils import *


class Object(object):
  pass

obj = Object()


def test_create_interface():
  obj.create_command = 'interface'
  obj.output_dir = 'tmp'
  obj.interface_name = 'test'
  out = create.create(obj)
  assert(path_exists(path_join('tmp', 'interfaces', 'test.yaml')))
  rmtree('tmp')


def test_create_part():
  obj.create_command = 'part'
  obj.output_dir = 'tmp'
  obj.part_name = 'test'
  obj.interfaces = ['rgmii']
  out = create.create(obj)
  assert(path_exists(path_join('tmp', 'parts', 'test.yaml')))
  rmtree('tmp')


def test_create_design():
  obj.create_command = 'design'
  obj.output_dir = 'tmp'
  obj.design_name = 'test'
  obj.interfaces = ['rgmii']
  out = create.create(obj)
  assert(path_exists(path_join('tmp', 'designs', 'test', 'test_rgmii.yaml')))
  rmtree('tmp')
