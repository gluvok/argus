"""Shell command templates and systemd unit generator for remote Pi deployment."""

TARGET = "/opt/argus"
PORT = 8000
EXCLUDES: list[str] = [
    "--exclude=.venv", "--exclude=.env*", "--exclude=__pycache__", "--exclude=.git",
    "--exclude=tests", "--exclude=docs", "--exclude=debug_crops", "--exclude=debug_output",
    "--exclude=.cache", "--exclude=.coverage", "--exclude=.pytest_cache",
    "--exclude=.ruff_cache", "--exclude=compiled_dist", "--exclude=dist",
]


def build_prep_cmd(target: str = TARGET) -> str:
    """Remote command to prepare directory, install ccache, and bootstrap uv."""
    return (
        f"sudo mkdir -p {target} && sudo chown -R $USER:$USER {target}; "
        f"command -v ccache >/dev/null || (sudo apt-get update -qq && sudo apt-get install -y -qq ccache) || true; "
        f'export PATH="$HOME/.local/bin:$PATH"; command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh'
    )


def build_compile_cmd(target: str = TARGET, port: int = PORT) -> str:
    """Remote command to compile app via Nuitka, write run.sh, and purge source .py files."""
    return (
        f'set -e; export PATH="$HOME/.local/bin:$PATH"; cd {target} && uv sync && '
        f"uv run python -m nuitka --module --include-package=app --nofollow-imports "
        f"--remove-output --lto=yes --python-flag=no_docstrings --output-dir={target}/dist app && "
        f"mv -f {target}/dist/app*so {target}/ && "
        f"printf '#!/usr/bin/env bash\\nset -e\\ncd {target}\\nexec {target}/.venv/bin/fastapi run --host 127.0.0.1 --port {port}\\n' > {target}/run.sh && "
        f"chmod +x {target}/run.sh; "
        f"rm -rf {target}/app {target}/dist {target}/tests {target}/docs {target}/debug_crops {target}/scripts; "
        f"find {target} -maxdepth 1 -name '*.py' -delete; "
        f"echo '[Deploy] Source purged! Only app.*.so and run.sh remain at {target}.'"
    )


def generate_systemd_unit(user: str, target: str = TARGET) -> str:
    """Render systemd service unit string for Argus."""
    return (
        f"[Unit]\nDescription=Argus ANPR FastAPI Microservice\nAfter=network.target\n\n"
        f"[Service]\nType=simple\nUser={user}\nWorkingDirectory={target}\n"
        f"ExecStart={target}/run.sh\nRestart=always\nRestartSec=5\n"
        f"Environment=PYTHONUNBUFFERED=1\n\n[Install]\nWantedBy=multi-user.target\n"
    )


def build_service_install_cmd() -> str:
    """Remote command to install systemd unit and restart argus service."""
    return (
        "sudo mv /tmp/argus.service /etc/systemd/system/argus.service && "
        "sudo systemctl daemon-reload && sudo systemctl enable --now argus && sudo systemctl restart argus"
    )
