// Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
// Licensed under the Apache License, Version 2.0 (see LICENSE).

package com.pants.testproject.javasources;

public class JavaSource {

  public String doStuff() {
      // this should not trigger a missing dependency warning
      // since we actually depend on the scala library
      return new JavaDependsOnThis().toString();
  }

}
