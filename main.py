import subprocess
import tempfile
from pathlib import Path


def define_env(env):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]

    @env.macro  # pyright: ignore[reportUnknownMemberType, reportUntypedFunctionDecorator]
    def generate_openapi(oas_path: str):  # pyright: ignore[reportUnusedFunction]
        project_root = Path(env.conf["root_dir"])  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        openapi_path = project_root / oas_path

        print()

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
