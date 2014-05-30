# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from twitter.common.lang import Compatibility

from pants.base.address import SyntheticAddress
from pants.base.build_environment import get_buildroot
from pants.base.payload import ResourcesPayload, SourcesMixin, Payload, hash_sources
from pants.base.target import Target

class WikiArtifact(object):
  def __init__(self, wiki, **kwargs):
    # if not isinstance(wiki, Wiki):
    #   raise ValueError('The 1st argument must be a wiki target, given: %s' % wiki)
    #self.wiki = self.get_wiki_dependencies()
    self.wiki = wiki
    self.config = kwargs


class Wiki(Target):
  """Target that identifies a wiki where pages can be published."""

  def __init__(self, name, url_builder, exclusives=None, **kwargs):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`pants.base.address.Address`.
    :param url_builder: Function that accepts a page target and an optional wiki config dict.
    :returns: A tuple of (alias, fully qualified url).
    """
    Target.__init__(self, name, exclusives=exclusives, **kwargs)
    self.url_builder = url_builder

  @property
  def traversable_specs(self):
    yield self



class Page(Target):
  """Describes a single documentation page.

  Example: ::

     page(name='mypage',
       source='mypage.md',
       provides=[
         wiki_artifact(wiki='address/of/my/wiki',
                      space='my_space',
                      title='my_page',
                      parent='my_parent'),
       ],
     )
  """

  class PagePayload(SourcesMixin, Payload):
    def __init__(self, sources_rel_path, source, resources=None, provides=None):
      self.sources_rel_path = sources_rel_path
      self.sources = [source]
      self.resources = list(resources or [])
      self.provides = list(provides or [])

    def invalidation_hash(self):
      return hash_sources(get_buildroot(), self.sources_rel_path, self.sources)



  def __init__(self, source, resources=None, provides=None, **kwargs):
    """
    :param string name: The name of this target, which combined with this
      build file defines the target :class:`pants.base.address.Address`.
    :param source: Source of the page in markdown format.
    :param dependencies: List of :class:`pants.base.target.Target` instances
      this target depends on.
    :type dependencies: list of targets
    :param resources: An optional list of Resources objects.
    """

    payload = self.PagePayload(sources_rel_path=kwargs.get('address').spec_path,
                               source=source,
                               resources=resources,
                               provides=provides)
    super(Page, self).__init__(payload=payload, **kwargs)

    if not isinstance(provides[0], WikiArtifact):
      raise ValueError('Page must provide a wiki_artifact. Found instead: %s' % provides)
    #self.provides = provides

  @property
  def source(self):
    return list(self.payload.sources)[0]

  # @property
  # def traversable_specs(self):
  #   for p in self.provides:
  #     yield p.wiki
  #     deps = self.get_wiki_dependencies()
  #     print("haha")
  #
  # def get_wiki_dependencies(self):
  #   wiki_deps = set()
  #   def collect_wiki_deps(target):
  #     print("Walked target %s" % target)
  #     if isinstance(target, Wiki):
  #       wiki_deps.update(target)
  #
  #   self.walk(work=collect_wiki_deps)
  #   return wiki_deps

  @property
  def provides(self):
    if not self.payload.provides:
      return None

    # TODO(pl): This is an awful hack
    for p in self.payload.provides:
      if isinstance(p.wiki, Compatibility.string):
        address = SyntheticAddress(p.wiki, relative_to=self.address.spec_path)
        # The problem is that the Wiki object isn't getting into the _build_graph. It seems like the traversable_specs()
        # callback is never invoked.
        repo_target = self._build_graph.get_target(address)
        p.wiki = repo_target
    return self.payload.provides
