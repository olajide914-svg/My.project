# python-template

This is a very simple boilerplate for an installable Python project
with a command line interface (CLI), using [pyproject.toml](pyproject.toml)
to define the project's dependencies, the metadata, and the configuration of
linters and formatters.

The template is functional. To test it:

- Create a new virtual environment and activate it.
- Go to the base directory of the project and call `pip install .`.
- After that, you can call the script in your shell with
`pytemplate <arguments>`; e.g.: `pytemplate --help`.

The name `pytemplate` of the script, and the entry point, are defined
in the [pyproject.toml](pyproject.toml) section `[project.scripts]`.

For development, you also need a code linter and formatter
installed. In this project, `ruff` is used for both tasks. To install
it, call `pip install ".[dev]"` to additionally install the optional
dependencies for code development, defined in the section
`[project.optional-dependencies]` in [pyproject.toml](pyproject.toml).
`ruff` is configured in the respective `tool.ruff` sections in
[pyproject.toml](pyproject.toml).

- To run the linter, call `ruff check`.
- To see what the formatter would change, run `ruff format --diff`.
- To actually run the code formatter, call `ruff format`.


Take a look at the original gitlab [README.md](README_gitlab_template.md)
template, which you can use as reference for the `README.md` of your own
project.

---
