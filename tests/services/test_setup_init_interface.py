"""Fresh setup must write the same theme default the settings module owns."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dhurandhar.services.settings.interface_settings import DEFAULT_UI_SETTINGS


def test_fresh_init_writes_the_interface_theme_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from dhurandhar.services.path_service import PathService
    from dhurandhar.services.setup import init as setup_init

    service = PathService(workspace_root=tmp_path)
    monkeypatch.setattr(setup_init, "get_path_service", lambda: service)
    monkeypatch.setattr(setup_init, "_seed_default_personas", lambda: None)
    monkeypatch.setattr(
        "dhurandhar.services.config.ensure_runtime_settings_files",
        lambda: None,
    )

    setup_init.init_user_directories()

    interface_file = service.get_settings_file("interface")
    stored = json.loads(interface_file.read_text(encoding="utf-8"))
    assert stored["theme"] == "system"
    assert stored["theme"] == DEFAULT_UI_SETTINGS["theme"]
    assert stored["theme"] == setup_init.DEFAULT_INTERFACE_SETTINGS["theme"]
