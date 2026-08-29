"""Compatibility entry point for the T1.L4 lesson package.

The lesson intentionally groups several mathematical modeling methods in
``methods.py`` rather than defining one domain model.  The course-level lesson
standard, however, expects ``src/model.py`` to exist.  This module re-exports
the public method implementations so generic tooling can treat T1.L4 like the
other lesson packages.
"""

try:
    from .methods import *  # noqa: F401,F403
except ImportError:  # support direct execution with src/ on sys.path
    from methods import *  # type: ignore # noqa: F401,F403
