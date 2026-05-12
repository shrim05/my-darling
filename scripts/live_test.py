from __future__ import annotations

from pathlib import Path
import os

from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "live-test"
OUT.mkdir(parents=True, exist_ok=True)

URL = os.environ.get("TEST_URL", "http://127.0.0.1:4173/")

VIEWPORTS = [
    ("desktop", 1180, 720, False),
    ("galaxy-s23", 360, 780, True),
    ("ipad", 820, 1180, True),
    ("galaxy-tab", 800, 1280, True),
]


def screenshot_stats(path: Path) -> dict[str, int]:
    im = Image.open(path).convert("RGB").resize((160, 90))
    colors = im.getcolors(maxcolors=160 * 90)
    return {
        "unique_colors": len(colors or []),
        "dark_pixels": sum(count for count, rgb in (colors or []) if sum(rgb) < 70),
    }


def run_case(browser, name: str, width: int, height: int, is_mobile: bool) -> dict:
    errors: list[str] = []
    page = browser.new_page(
        viewport={"width": width, "height": height},
        is_mobile=is_mobile,
        has_touch=is_mobile,
        device_scale_factor=3 if width <= 420 else 2,
    )
    page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
    page.on("console", lambda msg: errors.append(f"console error: {msg.text}") if msg.type == "error" else None)
    page.goto(URL, wait_until="networkidle", timeout=60_000)
    page.wait_for_selector("canvas", timeout=30_000)
    page.wait_for_function("window.__scene && window.__scene.husband && window.__scene.wife", timeout=30_000)
    page.locator("#start").click(timeout=10_000)
    page.wait_for_timeout(900)

    initial = OUT / f"{name}-initial.png"
    page.screenshot(path=initial, full_page=True)

    before_x = page.evaluate("window.__scene.husband.x")
    page.keyboard.down("d")
    page.wait_for_timeout(650)
    page.keyboard.up("d")
    after_x = page.evaluate("window.__scene.husband.x")

    page.evaluate(
        """() => {
          window.__scene.fireEvent({
            id: 'live-card-' + Math.random(),
            year: 2025,
            title: '약속이 별처럼 놓인 날',
            text: '긴 문장이 들어와도 화면 밖으로 달아나지 않는지 확인합니다. 작은 휴대폰 화면에서도 마음이 잘리지 않도록, 이 문장은 조심스럽게 여러 줄로 접혀야 합니다.'
          });
        }"""
    )
    page.wait_for_timeout(450)
    card_box = page.locator("#story-card").bounding_box()
    card_visible = page.locator("#story-card").evaluate("el => el.classList.contains('show')")
    card_shot = OUT / f"{name}-card.png"
    page.screenshot(path=card_shot, full_page=True)

    page.evaluate("window.__scene.startMerge()")
    page.wait_for_timeout(2600)
    merge_state = page.evaluate(
        """() => ({
          state: window.__scene.state,
          hasWifeCam: !!window.__scene.wifeCam && window.__scene.cameras.cameras.includes(window.__scene.wifeCam),
          husbandY: window.__scene.husband.y,
          wifeY: window.__scene.wife.y
        })"""
    )
    merge_shot = OUT / f"{name}-merge.png"
    page.screenshot(path=merge_shot, full_page=True)

    within_card = bool(
        card_box
        and card_box["x"] >= -1
        and card_box["y"] >= -1
        and card_box["x"] + card_box["width"] <= width + 1
        and card_box["y"] + card_box["height"] <= height + 1
    )

    result = {
        "viewport": [width, height],
        "errors": errors,
        "canvas_count": page.locator("canvas").count(),
        "movement_delta": round(after_x - before_x, 2),
        "card_visible": card_visible,
        "card_within_viewport": within_card,
        "merge_state": merge_state,
        "initial_stats": screenshot_stats(initial),
        "card_stats": screenshot_stats(card_shot),
        "merge_stats": screenshot_stats(merge_shot),
    }
    page.close()
    return result


def main() -> None:
    with sync_playwright() as p:
        browser = None
        launch_errors = []
        for browser_name in ["chromium", "firefox", "webkit"]:
          try:
              browser = getattr(p, browser_name).launch()
              print(f"browser={browser_name}")
              break
          except Exception as exc:
              launch_errors.append(f"{browser_name}: {exc}")
        if browser is None:
            print("BROWSER LAUNCH FAILURES")
            for error in launch_errors:
                print(error)
            raise SystemExit(2)
        results = [run_case(browser, *case) for case in VIEWPORTS]
        browser.close()

    failures = []
    for name, result in zip([case[0] for case in VIEWPORTS], results):
        if result["errors"]:
            failures.append(f"{name}: browser errors {result['errors']}")
        if result["canvas_count"] != 1:
            failures.append(f"{name}: expected 1 canvas, got {result['canvas_count']}")
        if result["movement_delta"] <= 5:
            failures.append(f"{name}: right touch/mouse did not move player enough ({result['movement_delta']})")
        if not result["card_visible"] or not result["card_within_viewport"]:
            failures.append(f"{name}: story card not safely visible {result['card_visible']} {result['card_within_viewport']}")
        if result["merge_state"]["state"] not in {"merging", "shared"}:
            failures.append(f"{name}: merge did not start {result['merge_state']}")
        if result["initial_stats"]["unique_colors"] < 180:
            failures.append(f"{name}: initial screenshot looks too flat {result['initial_stats']}")

    print("LIVE TEST RESULTS")
    for name, result in zip([case[0] for case in VIEWPORTS], results):
        print(name, result)
    if failures:
        print("FAILURES")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
