import runpy
from unittest import mock

import pytest


def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("granian.Granian", mock.Mock())
    runpy.run_module("app.__main__", run_name="__main__")
