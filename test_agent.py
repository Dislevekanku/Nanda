#!/usr/bin/env python3
"""Utility script to exercise the MedSpa Agent API."""

import asyncio
from typing import Any

import httpx


API_BASE = "http://127.0.0.1:8000"


def _print(title: str, data: Any) -> None:
    print("\n" + title)
    print("=" * len(title))
    print(data)


async def health_check() -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/health")
        _print("Health", response.json())


async def main() -> None:
    await health_check()


if __name__ == "__main__":
    asyncio.run(main())
