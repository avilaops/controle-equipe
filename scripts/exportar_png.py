"""Render the SVG plugin icons as transparent 256 px PNG files."""

from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


ROOT = Path(__file__).resolve().parents[1]


async def main() -> None:
    icons = sorted((ROOT / "plugins").glob("*/assets/plugin-icon.svg"))
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(channel="chrome", headless=True)
        page = await browser.new_page(viewport={"width": 256, "height": 256})
        for icon in icons:
            svg = icon.read_text(encoding="utf-8")
            await page.set_content(f'<style>html,body{{margin:0;width:256px;height:256px;background:transparent}}svg{{display:block}}</style>{svg}')
            await page.locator("svg").screenshot(path=str(icon.with_suffix(".png")), omit_background=True)
        await page.goto((ROOT / "docs/GALERIA.html").as_uri())
        await page.set_viewport_size({"width": 1440, "height": 1000})
        await page.screenshot(path=str(ROOT / "docs/GALERIA.png"), full_page=True)
        await browser.close()
    print(f"{len(icons)} PNGs exportados")


if __name__ == "__main__":
    asyncio.run(main())
