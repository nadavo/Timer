#!/bin/bash
set -x
PACKAGE=syct-0.4.4*
pip install --upgrade build twine
python -m build
python -m twine upload dist/${PACKAGE}
