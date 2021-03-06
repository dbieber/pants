# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)
import os
import tempfile
import time

from twitter.common.python.pex_builder import PEXBuilder

from pants.backend.python.python_chroot import PythonChroot
from pants.backend.python.targets.python_binary import PythonBinary
from pants.backend.python.tasks.python_task import PythonTask
from pants.base.exceptions import TaskError


class PythonBinaryCreate(PythonTask):
  @staticmethod
  def is_binary(target):
    return isinstance(target, PythonBinary)

  @classmethod
  def setup_parser(cls, option_group, args, mkflag):
    super(PythonBinaryCreate, cls).setup_parser(option_group, args, mkflag)

  def __init__(self, context, workdir):
    super(PythonBinaryCreate, self).__init__(context, workdir)
    self._distdir = self.context.config.getdefault('pants_distdir')

  def execute(self):
    binaries = self.context.targets(self.is_binary)

    # Check for duplicate binary names, since we write the pexes to <dist>/<name>.pex.
    names = {}
    for binary in binaries:
      name = binary.name
      if name in names:
        raise TaskError('Cannot build two binaries with the same name in a single invocation. '
                        '%s and %s both have the name %s.' % (binary, names[name], name))
      names[name] = binary

    for binary in binaries:
      self.create_binary(binary)

  def create_binary(self, binary):
    if binary.compatibility:
      interpreter = self.select_interpreter(binary.compatibility)
    else:
      interpreter = self.interpreter

    distpath = tempfile.mktemp(dir=self._distdir, prefix=binary.name)

    run_info = self.context.run_tracker.run_info
    build_properties = {}
    build_properties.update(run_info.add_basic_info(run_id=None, timestamp=time.time()))
    build_properties.update(run_info.add_scm_info())

    pexinfo = binary.pexinfo.copy()
    pexinfo.build_properties = build_properties
    builder = PEXBuilder(distpath, pex_info=pexinfo, interpreter=interpreter)

    chroot = PythonChroot(
      targets=[binary],
      builder=builder,
      platforms=binary.platforms,
      interpreter=interpreter,
      conn_timeout=self.conn_timeout)

    pex_path = os.path.join(self._distdir, '%s.pex' % binary.name)
    builder = chroot.dump()
    try:
      builder.build(pex_path)
    finally:
      builder.chroot().delete()
