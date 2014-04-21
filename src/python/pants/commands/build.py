# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import sys
import traceback

from twitter.common.collections import OrderedSet

from pants.base.address import BuildFileAddress, parse_spec
from pants.base.build_file import BuildFile
from pants.base.config import Config
from pants.base.target import Target
from pants.commands.command import Command
from pants.python.interpreter_cache import PythonInterpreterCache
from pants.python.python_builder import PythonBuilder


class Build(Command):
  """Builds a specified target."""

  __command__ = 'build'

  def setup_parser(self, parser, args):
    parser.set_usage("\n"
                     "  %prog build (options) [spec] (build args)\n"
                     "  %prog build (options) [spec]... -- (build args)")
    parser.add_option("-t", "--timeout", dest="conn_timeout", type="int",
                      default=Config.load().getdefault('connection_timeout'),
                      help="Number of seconds to wait for http connections.")
    parser.add_option('-i', '--interpreter', dest='interpreter', default=None,
                      help='The interpreter requirement for this chroot.')
    parser.add_option('-v', '--verbose', dest='verbose', default=False, action='store_true',
                      help='Show verbose output.')
    parser.disable_interspersed_args()
    parser.epilog = ('Builds the specified Python target(s). Use ./pants goal for JVM and other '
                     'targets.')

  def __init__(self, run_tracker, root_dir, parser, argv):
    Command.__init__(self, run_tracker, root_dir, parser, argv)

    if not self.args:
      self.error("A spec argument is required")

    self.config = Config.load()
    self.interpreter_cache = PythonInterpreterCache(self.config, logger=self.debug)
    self.interpreter_cache.setup()
    interpreters = self.interpreter_cache.select_interpreter(
        list(self.interpreter_cache.matches([self.options.interpreter]
            if self.options.interpreter else [b''])))
    if len(interpreters) != 1:
      self.error('Unable to detect suitable interpreter.')
    else:
      self.debug('Selected %s' % interpreters[0])
    self.interpreter = interpreters[0]

    try:
      specs_end = self.args.index('--')
      if len(self.args) > specs_end:
        self.build_args = self.args[specs_end+1:len(self.args)+1]
      else:
        self.build_args = []
    except ValueError:
      specs_end = 1
      self.build_args = self.args[1:] if len(self.args) > 1 else []

    self.targets = OrderedSet()
    for spec in self.args[0:specs_end]:
      try:
        spec_path, target_name = parse_spec(spec)
        build_file = BuildFile(root_dir, spec_path)
        address = BuildFileAddress(build_file, target_name)
      except:
        self.error("Problem parsing spec %s: %s" % (spec, traceback.format_exc()))

      try:
        self.build_file_parser.inject_spec_closure_into_build_graph(spec, self.build_graph)
        target = self.build_graph.get_target(address)
      except:
        self.error("Problem parsing BUILD target %s: %s" % (address, traceback.format_exc()))

      if not target:
        self.error("Target %s does not exist" % address)
      self.targets.add(target)

  def debug(self, message):
    if self.options.verbose:
      print(message, file=sys.stderr)

  def execute(self):
    print("Build operating on targets: %s" % self.targets)

    python_targets = OrderedSet()
    for target in self.targets:
      if target.is_python:
        python_targets.add(target)
      else:
        self.error("Cannot build target %s" % target)

    if python_targets:
      status = self._python_build(python_targets)
    else:
      status = -1

    return status

  def _python_build(self, targets):
    try:
      executor = PythonBuilder(self.run_tracker, self.root_dir)
      return executor.build(
        targets,
        self.build_args,
        interpreter=self.interpreter,
        conn_timeout=self.options.conn_timeout)
    except:
      self.error("Problem executing PythonBuilder for targets %s: %s" % (targets,
                                                                         traceback.format_exc()))
