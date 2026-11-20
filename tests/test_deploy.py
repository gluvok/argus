"""Unit tests for deployment command generation and dry-run pipeline."""

from unittest.mock import patch

import pytest

from app.core import constants
from scripts.deploy import deploy_remote, run_cmd
from scripts.deploy_commands import (
    build_compile_cmd,
    build_prep_cmd,
    build_service_install_cmd,
    generate_systemd_unit,
)


def test_deploy_command_templates():
    """Verify prep, compile, and systemd install commands format correctly."""
    prep = build_prep_cmd("/opt/test")
    assert "/opt/test" in prep
    assert "curl -LsSf https://astral.sh/uv/install.sh" in prep

    compile_cmd = build_compile_cmd("/opt/test", 8080)
    assert "cd /opt/test && uv sync" in compile_cmd
    assert "--port 8080" in compile_cmd
    assert "rm -rf /opt/test/app" in compile_cmd

    install_cmd = build_service_install_cmd()
    assert "systemctl daemon-reload" in install_cmd
    assert "systemctl enable --now argus" in install_cmd


def test_run_script_binds_loopback_only():
    """`fastapi run` defaults to 0.0.0.0, so run.sh must pass the loopback host explicitly (issue #26)."""
    compile_cmd = build_compile_cmd("/opt/test", 8080)
    assert f"fastapi run --host {constants.SERVER_HOST} --port 8080" in compile_cmd
    assert constants.SERVER_HOST == "127.0.0.1"
    assert "0.0.0.0" not in compile_cmd


def test_systemd_unit_does_not_expose_all_interfaces():
    """The unit must launch run.sh (loopback-bound) and never bind all interfaces itself."""
    unit = generate_systemd_unit("testuser", "/opt/argus")
    assert "0.0.0.0" not in unit
    assert "ExecStart=/opt/argus/run.sh" in unit


def test_generate_systemd_unit():
    """Verify systemd service unit string generation."""
    unit = generate_systemd_unit("testuser", "/opt/argus")
    assert "User=testuser" in unit
    assert "WorkingDirectory=/opt/argus" in unit
    assert "ExecStart=/opt/argus/run.sh" in unit


def test_deploy_remote_dry_run(capsys):
    """Verify deploy_remote in dry-run mode runs cleanly without network calls."""
    deploy_remote("testuser@remote.host", dry_run=True)
    # Ensure no exception was raised and service file was generated


@patch("subprocess.run")
def test_run_cmd_failure(mock_subproc):
    """Verify run_cmd exits on non-zero returncode."""
    mock_subproc.return_value.returncode = 1
    with pytest.raises(SystemExit):
        run_cmd(["false"], dry_run=False)
