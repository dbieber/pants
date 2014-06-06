# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import re

from twitter.common.lang import Compatibility

from pants.base.address import SyntheticAddress
from pants.base.build_environment import get_buildroot
from pants.base.payload import SourcesMixin, Payload, hash_sources
from pants.base.target import Target
# To work around the circular imports issue in Python. :(
import pants.tasks.markdown_to_html

class WikiArtifact(object):
  def __init__(self, wiki, **kwargs):
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

  @property
  def source(self):
    return list(self.payload.sources)[0]

  # This callback needs to yield every 'pants(...)' pointer that we need to have resolved into the
  # build graph. This includes wiki objects in the provided WikiArtifact objects, and any 'pants()'
  # pointers inside of the documents themselves (yes, this can happen).
  @property
  def traversable_specs(self):
    if self.payload.provides:
      for wiki_artifact in self.payload.provides:
        yield wiki_artifact.wiki

    # Parse the entire markdown page, and yield all pants() pointers embedded in wiki links.
    for source_file in self.payload.sources:
      file_contents = open(self.payload.sources_rel_path + "/" + source_file).read()

      for link_payload in re.finditer(pants.tasks.markdown_to_html.WIKILINKS_PATTERN, file_contents):
        pants_spec = pants.tasks.markdown_to_html.MarkdownToHtml.PANTS_LINK.search(link_payload.group(1)).group(1)
        yield pants_spec

  # This callback is used to link up the provided WikiArtifact objects to Wiki objects. In the build
  # file, a 'pants(...)' pointer is specified to the Wiki object. In this method, this string
  # pointer is resolved in the build graph, and an actual Wiki object is swapped in place of the
  # string.
  @property
  def provides(self):
    if not self.payload.provides:
      return None

    for p in self.payload.provides:
      if isinstance(p.wiki, Compatibility.string):
        address = SyntheticAddress(p.wiki, relative_to=self.address.spec_path)
        repo_target = self._build_graph.get_target(address)
        p.wiki = repo_target
      else:
        raise ValueError('A WikiArtifact must depend on a string pointer to a Wiki. Found %s instead.'
                         % p.wiki)
    return self.payload.provides
