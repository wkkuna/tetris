#!/bin/bash
if [ -z "$DOCS_DIR" ] || [ -z "$BUILD_DIR" ]; then
  echo "Documentation or build directory not specified. Exiting... "
  exit 1
fi

sphinx-build -M html $DOCS_DIR $BUILD_DIR