# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.base.target import Target


class Credentials(Target):
  """Supplies credentials for a maven repository on demand.

  The ``jar-publish`` section of your ``pants.ini`` file can refer to one
  or more of these.
  """

  def __init__(self, username=None, password=None, **kwargs):
    """
    :param string name: The name of these credentials.
    :param username: Either a constant username value or else a callable that can fetch one.
    :type username: string or callable
    :param password: Either a constant password value or else a callable that can fetch one.
    :type password: string or callable
    """
    super(Credentials, self).__init__(**kwargs)
    self._username = username if callable(username) else lambda: username
    self._password = password if callable(password) else lambda: password

  def username(self, repository):
    """Returns the username in java system property argument form."""
    return self._username(repository)

  def password(self, repository):
    """Returns the password in java system property argument form."""
    return self._password(repository)
