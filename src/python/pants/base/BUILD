# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'abbreviate_target_ids',
  sources = ['abbreviate_target_ids.py'],
)

python_library(
  name = 'address',
  sources = ['address.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants(':build_file'),
  ]
)

python_library(
  name = 'build_environment',
  sources = ['build_environment.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
    pants('src/python/pants/version'),
    pants('src/python/pants/scm:all'),
    pants(':build_root'),
  ]
)

python_library(
  name = 'build_file',
  sources = ['build_file.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.python'),
  ]
)

python_library(
  name = 'build_file_parser',
  sources = ['build_file_parser.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.python'),
    pants(':build_file'),
    pants(':address'),
  ]
)

python_library(
  name = 'build_graph',
  sources = ['build_graph.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants(':address'),
  ]
)

python_library(
  name = 'build_invalidator',
  sources = ['build_invalidator.py'],
  dependencies = [
    pants(':hash_utils'),
    pants(':target'), # XXX(fixme)
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants('3rdparty/python/twitter/commons:twitter.common.python'),
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
    pants('src/python/pants/fs'),
  ]
)

python_library(
  name = 'build_manual',
  sources = ['build_manual.py'],
)

python_library(
  name = 'build_root',
  sources = ['build_root.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
  ],
)

python_library(
  name = 'cache_manager',
  sources = ['cache_manager.py'],
  dependencies = [
    pants(':build_graph'),
    pants(':build_invalidator'),
    pants(':target'),
  ],
)

python_library(
  name = 'config',
  sources = ['config.py'],
  dependencies = [
    pants(':build_environment'),
  ]
)

python_library(
  name = 'dev_backend_loader',
  sources = ['dev_backend_loader.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
  ]
)

python_library(
  name = 'double_dag',
  sources = ['double_dag.py'],
  dependencies = [
    pants(':abbreviate_target_ids'),
  ]
)

python_library(
  name = 'exceptions',
  sources = ['exceptions.py'],
  dependencies = [
    pants(':build_manual'),
  ]
)

python_library(
  name = 'fingerprint_strategy',
  sources = ['fingerprint_strategy.py'],
)

python_library(
  name = 'generator',
  sources = ['generator.py'],
  dependencies = [
    pants(':mustache'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
  ]
)

python_library(
  name = 'hash_utils',
  sources = ['hash_utils.py'],
)

python_library(
  name = 'mustache',
  sources = ['mustache.py'],
  dependencies = [
    pants('3rdparty/python:pystache'),
  ]
)

python_library(
  name = 'payload',
  sources = ['payload.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants(':build_environment'),
  ]
)

python_library(
  name = 'rcfile',
  sources = ['rcfile.py'],
  dependencies = [
    pants(':config'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
  ]
)

python_library(
  name = 'revision',
  sources = ['revision.py'],
)

python_library(
  name = 'run_info',
  sources = ['run_info.py'],
  dependencies = [
    pants(':build_environment'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
  ],
)

python_library(
  name = 'spec_parser',
  sources = ['spec_parser.py'],
  dependencies = [
    pants(':address'),
    pants(':build_file'),
  ],
)

python_library(
  name = 'source_root',
  sources = ['source_root.py'],
  dependencies = [
    pants(':build_environment'),
    pants(':exceptions'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
  ],
)

python_library(
  name = 'target',
  sources = ['target.py'],
  dependencies = [
    pants(':address'),
    pants(':build_environment'),
    pants(':build_manual'),
    pants(':fingerprint_strategy'),
    pants(':hash_utils'),
    pants(':source_root'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
  ],
)

python_library(
  name = 'worker_pool',
  sources = ['worker_pool.py'],
  dependencies = [
    pants('src/python/pants/reporting:report'), # TODO(pl): Bust this out
  ],
)

python_library(
  name = 'workunit',
  sources = ['workunit.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/rwbuf'),
  ],
)
