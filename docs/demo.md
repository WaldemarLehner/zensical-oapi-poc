---
hide:
  - navigation
render_macros: true
---

??? tip "Hidden Navigation"

    Note that this page's navigation was hidden with

    ``` yaml
    hide:
    - navigation
    ```

    in the frontmatter.

    The remainder of this page was entirely rendered by invoking the `generate_openapi(pathToOasRelativeToProjectRoot)` script.

{{ generate_openapi("petstore.oas.json") }}
