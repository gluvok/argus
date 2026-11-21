"""deploy.py — 1-command remote Pi deploy for Argus: compile, systemd, purge source."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.core.logging import logger
from scripts.deploy_commands import (
    EXCLUDES,
    TARGET,
    build_compile_cmd,
    build_prep_cmd,
    build_service_install_cmd,
    generate_systemd_unit,
)


def run_cmd(cmd: list[str], dry_run: bool = False) -> None:
    """Execute shell command or log in dry-run mode."""
    if dry_run:
        logger.info(f"[DRY-RUN] {' '.join(cmd)}")
        return
    if (code := subprocess.run(cmd, check=False).returncode) != 0:
        logger.error(f"[Deploy] Command failed ({code}): {' '.join(cmd)}")
        sys.exit(code)


def deploy_remote(host: str, dry_run: bool = False) -> None:
    """Execute 4-stage deployment pipeline to remote Pi."""
    user = host.split("@")[0] if "@" in host else os.environ.get("USER", "gluvok")
    logger.info(f"[Deploy] 1. Preparing {TARGET} on {host}...")
    run_cmd(["ssh", "-t", host, build_prep_cmd()], dry_run)

    logger.info(f"[Deploy] 2. Syncing source & model weights to {host}:{TARGET}...")
    run_cmd(["rsync", "-avz", "--delete", *EXCLUDES, f"{_ROOT}/", f"{host}:{TARGET}/"], dry_run)

    logger.info("[Deploy] 3. Compiling app module with Nuitka and purging source...")
    run_cmd(["ssh", "-t", host, build_compile_cmd()], dry_run)

    logger.info("[Deploy] 4. Provisioning systemd service...")
    dist_dir = Path(_ROOT) / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    svc_file = dist_dir / "argus.service"
    svc_file.write_text(generate_systemd_unit(user), encoding="utf-8")
    run_cmd(["scp", str(svc_file), f"{host}:/tmp/argus.service"], dry_run)
    run_cmd(["ssh", "-t", host, build_service_install_cmd()], dry_run)
    logger.info(f"[Deploy] Complete! Argus service configured on {host}.")


def main() -> None:
    p = argparse.ArgumentParser(description="Argus 1-Command Pi Deployer")
    p.add_argument("--host", default="gluvok@hermes.local", help="SSH host (e.g. gluvok@hermes.local)")
    p.add_argument("--dry-run", action="store_true", help="Print commands without executing them")
    args = p.parse_args()
    deploy_remote(args.host, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
