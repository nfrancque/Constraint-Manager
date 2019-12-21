from .design import Design
import logging

LOGGER = logging.getLogger(__name__)

def generate(args):
  design = Design(args.design_name)
  constraints = design.gen_constraints()
  if (args.output == 'stdout'):
    print(constraints)
  else:
    with open(str(args.output), 'w+') as f:
      f.write(constraints)   