# Zensical OpenAPI PoC

This is a minimal repro showcasing how one can generate an OpenAPI Documentation by reimplementing [`neoteroi.mkdocsoad`](https://www.neoteroi.dev/mkdocs-plugins/web/oad/){target=_blank} as a Macro.
Macro support was added in [Zensical `v0.0.40`](https://zensical.org/docs/compatibility/mkdocs/plugins/?h=macros#macros){target=_blank}.

## Demo

The demo file contains the following contents:

``` md

{{ generate_openapi("petstore.oas.json") }}
```

[Go to demo](./demo.md)

## Setup

!!! tip ""

    These Docs assume `uv`, adjust as needed for `pip`…

1.  Add `macros` into your list of plugins

    ``` diff
    + plugins = [
    +   "macros"
    + ]
    ```

2.  Add the required dependency `essentials-openapi` with the `full` features:

    ``` sh
    uv add essentials-openapi --extra full 
    ```

3.  Create a `main.py` with the following contents:
    ``` py
    import subprocess
    import tempfile
    from pathlib import Path


    def define_env(env):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]

        @env.macro  # pyright: ignore[reportUnknownMemberType, reportUntypedFunctionDecorator]
        def generate_openapi(oas_path: str):  # pyright: ignore[reportUnusedFunction]
            project_root = Path(env.conf["root_dir"])  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
            openapi_path = project_root / oas_path

            if not openapi_path.is_file():
                return (
                    '!!! danger "Failed to generate OAS"\n\n'
                    + f"    Cannot find File at `{openapi_path}`"
                )

            with tempfile.NamedTemporaryFile(suffix=".md") as f:
                _ = subprocess.run(
                    [
                        "oad",
                        "gen-docs",
                        "-s",
                        openapi_path.resolve().absolute(),
                        "-d",
                        f.name,
                    ],
                    check=True,
                )

                return Path(f.name).read_text()
    ```
4.  Copy the `neoteroi-mkdocs.css` from [`https://github.com/Neoteroi/mkdocs-plugins/releases/tag/v1.2.0`](https://github.com/Neoteroi/mkdocs-plugins/releases/tag/v1.2.0) [(raw file)](https://github.com/Neoteroi/mkdocs-plugins/releases/download/v1.2.0/css-v1.2.0.css) and add it to the extra css in `zensical.toml`:
    ``` diff
    + extra_css = ["css/neoteroi-mkdocs.css"]
    ```

    This adds the coloured highlights to the OAS.

???+ tip "Opt-in to Macros"

    The use of `[[…]]` may conflict with other plugins. Consider "opting into" a specific page being macro-enabled instead of the usual opt-out flow:

    ``` diff
    - plugins = [
    -   "macros"
    - ]

    + [project.plugins.macros]
    + render_by_default = false
    ```

    Then add the key to the page's frontmatter:

    ``` diff
      ---
      hide:
      - navigation
    + render_macros: true
      ---
      ... markdown content
    ```
