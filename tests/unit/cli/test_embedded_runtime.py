"""Embedded CLI runtime does not start IM channel connections (#1192)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from octop.cli.repl import embedded_session


async def test_embedded_runtime_skips_im_channels(monkeypatch: pytest.MonkeyPatch) -> None:
    server = MagicMock()
    server.start = AsyncMock()
    server.stop = AsyncMock()
    factory = MagicMock(return_value=server)
    monkeypatch.setattr(embedded_session, "OctopServer", factory)
    monkeypatch.setattr(embedded_session, "_server", None)
    monkeypatch.setattr(embedded_session, "_refs", 0)

    async with embedded_session.embedded_runtime() as started:
        assert started is server

    factory.assert_called_once_with(register_im_channels=False)
    server.start.assert_awaited_once()
    server.stop.assert_awaited_once()
