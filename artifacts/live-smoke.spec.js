const fs = require("fs");
const path = require("path");
const { test, expect } = require("@playwright/test");

const outDir = path.join(__dirname, "live-test");
fs.mkdirSync(outDir, { recursive: true });
const baseURL = process.env.TEST_URL || "http://127.0.0.1:4173/";

const cases = [
  ["desktop", { width: 1180, height: 720 }, false],
  ["galaxy-s23", { width: 360, height: 780 }, true],
  ["galaxy-s23-landscape", { width: 780, height: 360 }, true],
  ["ipad", { width: 820, height: 1180 }, true],
  ["galaxy-tab", { width: 800, height: 1280 }, true],
];

test("timeline data and asset wiring match requested story gaps and media", async () => {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "assets/data/events.json"), "utf8"));
  for (const owner of ["husband", "wife"]) {
    const years = data.events
      .filter((event) => event.owner === owner || event.owner === "shared")
      .map((event) => event.year)
      .sort((a, b) => a - b);
    for (let index = 1; index < years.length; index += 1) {
      expect(years[index] - years[index - 1], `${owner} gap ${years[index - 1]}-${years[index]}`).toBeLessThan(5);
    }
  }

  const eventIds = data.events.map((event) => event.id);
  expect(new Set(eventIds).size).toBe(eventIds.length);
  const sharedYears = data.events
    .filter((event) => event.owner === "shared")
    .map((event) => event.year)
    .sort((a, b) => a - b);
  expect(sharedYears).toEqual([2020, 2021, 2022, 2023, 2024, 2025, 2026]);
  expect(fs.existsSync(path.join(__dirname, "..", "assets/generated/cover.png"))).toBeTruthy();

  for (const sourceFile of ["scripts/build_single_index.py", "src/main.js"]) {
    const source = fs.readFileSync(path.join(__dirname, "..", sourceFile), "utf8");
    expect(source).toContain("assets/generated/The_Amber_Path.mp4");
    expect(source).toContain("assets/generated/YJH01044.jpg");
    expect(source).not.toContain("Everything_We_Built.mp3");
    expect(source).not.toContain("Where_The_Tide_Meets_Home.mp3");
    expect(source).not.toContain("DSC00038.jpg");
  }

  const buildSource = fs.readFileSync(path.join(__dirname, "..", "scripts/build_single_index.py"), "utf8");
  expect(buildSource).toContain("og:image");
  expect(buildSource).toContain("assets/generated/cover.png");
  expect(buildSource).toContain("https://shrim05.github.io/my-darling/");
});

for (const [name, viewport, isMobile] of cases) {
  test(`${name} proposal game smoke`, async ({ browser }) => {
    const context = await browser.newContext({
      viewport,
      isMobile,
      hasTouch: isMobile,
      deviceScaleFactor: viewport.width <= 420 ? 3 : 2,
    });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (error) => errors.push(String(error)));
    page.on("console", (msg) => {
      if (msg.type() === "error") errors.push(msg.text());
    });

    await page.goto(baseURL, { waitUntil: "networkidle" });
    await page.waitForSelector("canvas");
    await page.waitForFunction(() => window.__scene && window.__scene.husband && window.__scene.wife);
    await page.waitForTimeout(800);
    const preStartState = await page.evaluate(() => ({
      seenCount: window.__scene.seen.size,
      husbandStoryVisible: document.getElementById("story-card-husband").classList.contains("show"),
      wifeStoryVisible: document.getElementById("story-card-wife").classList.contains("show"),
      sharedStoryVisible: document.getElementById("story-card").classList.contains("show"),
    }));
    expect(preStartState.seenCount).toBe(0);
    expect(preStartState.husbandStoryVisible).toBeFalsy();
    expect(preStartState.wifeStoryVisible).toBeFalsy();
    expect(preStartState.sharedStoryVisible).toBeFalsy();
    await page.locator("#start").click();
    await page.waitForTimeout(700);
    await page.screenshot({ path: path.join(outDir, `${name}-initial.png`), fullPage: true });

    const spriteState = await page.evaluate(() => {
      const scene = window.__scene;
      return {
        husbandStartX: Math.round(scene.husband.x),
        wifeStartX: Math.round(scene.wife.x),
        husbandStudentFrames: scene.anims.get("husband-student-walk").frames.length,
        wifeAdultFrames: scene.anims.get("wife-adult-walk").frames.length,
        groomFrames: scene.anims.get("husband-wedding-walk").frames.map((frame) => frame.frame.name),
        brideFrames: scene.anims.get("wife-wedding-walk").frames.map((frame) => frame.frame.name),
        sharedCardVisible: document.getElementById("story-card").classList.contains("show"),
      };
    });
    expect(spriteState.husbandStartX).toBeLessThan(300);
    expect(spriteState.wifeStartX - spriteState.husbandStartX).toBeGreaterThan(800);
    expect(spriteState.sharedCardVisible).toBeFalsy();
    expect(spriteState.husbandStudentFrames).toBe(2);
    expect(spriteState.wifeAdultFrames).toBe(2);
    expect(spriteState.groomFrames).toEqual([12, 13]);
    expect(spriteState.brideFrames).toEqual([14, 15]);

    const yearBoundaryState = await page.evaluate(() => {
      const scene = window.__scene;
      const foot = (player) => Math.round(scene.visualFootY(player));
      scene.husband.setX(1138);
      scene.placeOnGround(scene.husband, scene.husband.groundY);
      scene.update();
      const husbandBefore1994 = {
        stage: scene.husband.stage,
        footY: foot(scene.husband),
        sawElementary: scene.seen.has("husband-elementary"),
      };
      scene.husband.setX(1140);
      scene.placeOnGround(scene.husband, scene.husband.groundY);
      scene.update();
      const husbandAt1994 = {
        stage: scene.husband.stage,
        footY: foot(scene.husband),
        sawElementary: scene.seen.has("husband-elementary"),
      };
      scene.husband.y = 780;
      scene.husband.body.setVelocityY(300);
      scene.update();
      const husbandRecoveredFootY = foot(scene.husband);
      scene.wife.setX(1509);
      scene.placeOnGround(scene.wife, scene.wife.groundY);
      scene.update();
      const wifeBefore2001 = {
        stage: scene.wife.stage,
        footY: foot(scene.wife),
        sawElementary: scene.seen.has("wife-elementary"),
      };
      scene.wife.setX(1510);
      scene.placeOnGround(scene.wife, scene.wife.groundY);
      scene.update();
      const wifeAt2001 = {
        stage: scene.wife.stage,
        footY: foot(scene.wife),
        sawElementary: scene.seen.has("wife-elementary"),
      };
      return { husbandBefore1994, husbandAt1994, husbandRecoveredFootY, wifeBefore2001, wifeAt2001 };
    });
    expect(yearBoundaryState.husbandBefore1994.stage).toBe("baby");
    expect(yearBoundaryState.husbandBefore1994.sawElementary).toBeFalsy();
    expect(yearBoundaryState.husbandAt1994.stage).toBe("student");
    expect(yearBoundaryState.husbandAt1994.sawElementary).toBeTruthy();
    expect(Math.abs(yearBoundaryState.husbandAt1994.footY - 430)).toBeLessThanOrEqual(1);
    expect(Math.abs(yearBoundaryState.husbandRecoveredFootY - 430)).toBeLessThanOrEqual(1);
    expect(yearBoundaryState.wifeBefore2001.stage).toBe("baby");
    expect(yearBoundaryState.wifeBefore2001.sawElementary).toBeFalsy();
    expect(yearBoundaryState.wifeAt2001.stage).toBe("student");
    expect(yearBoundaryState.wifeAt2001.sawElementary).toBeTruthy();
    expect(Math.abs(yearBoundaryState.wifeAt2001.footY - 970)).toBeLessThanOrEqual(1);

    const beforeX = await page.evaluate(() => window.__scene.husband.x);
    await page.keyboard.down("d");
    await page.waitForTimeout(650);
    await page.keyboard.up("d");
    const afterX = await page.evaluate(() => window.__scene.husband.x);
    expect(afterX - beforeX).toBeGreaterThan(5);

    await page.evaluate(() => {
      window.__scene.fireEvent({
        id: "live-husband-card",
        owner: "husband",
        year: 2005,
        title: "왼쪽에서 오는 문장",
        text: "영호의 문장은 위쪽 자기 자리에서만 조용히 펼쳐져야 합니다.",
      });
      window.__scene.fireEvent({
        id: "live-wife-card",
        owner: "wife",
        year: 2013,
        title: "아래쪽에서 오는 문장",
        text: "은지의 문장은 아래쪽 자기 자리에서만 따로 빛나야 합니다.",
      });
    });
    await page.waitForTimeout(450);
    for (const selector of ["#story-card-husband", "#story-card-wife"]) {
      const box = await page.locator(selector).boundingBox();
      const visible = await page.locator(selector).evaluate((el) => el.classList.contains("show"));
      expect(visible).toBeTruthy();
      expect(box.x).toBeGreaterThanOrEqual(0);
      expect(box.y).toBeGreaterThanOrEqual(0);
      expect(box.x + box.width).toBeLessThanOrEqual(viewport.width + 1);
      expect(box.y + box.height).toBeLessThanOrEqual(viewport.height + 1);
    }
    const husbandCardBox = await page.locator("#story-card-husband").boundingBox();
    const wifeCardBox = await page.locator("#story-card-wife").boundingBox();
    expect(husbandCardBox.y + husbandCardBox.height).toBeLessThanOrEqual(wifeCardBox.y);
    const compactSplitCards = isMobile && (viewport.width <= 760 || viewport.height <= 430);
    if (compactSplitCards) {
      for (const box of [husbandCardBox, wifeCardBox]) {
        expect(box.x + box.width).toBeLessThanOrEqual(viewport.width * 0.72);
        expect(box.height).toBeLessThanOrEqual(viewport.height * 0.24);
      }
      if (viewport.height > viewport.width) {
        expect(wifeCardBox.y).toBeGreaterThanOrEqual(viewport.height * 0.68);
      }
    }
    await page.screenshot({ path: path.join(outDir, `${name}-split-cards.png`), fullPage: true });

    await page.evaluate(() => window.__scene.startMerge());
    await page.waitForTimeout(900);
    const midMergeState = await page.evaluate(() => ({
      state: window.__scene.state,
      husbandY: Math.round(window.__scene.husband.y),
      wifeY: Math.round(window.__scene.wife.y),
    }));
    expect(midMergeState.state).toBe("merging");
    expect(midMergeState.wifeY - midMergeState.husbandY).toBeGreaterThan(120);
    expect(midMergeState.wifeY).toBeLessThan(900);

    await page.waitForTimeout(2700);
    const mergeState = await page.evaluate(() => ({
      state: window.__scene.state,
      hasWifeCam: !!window.__scene.wifeCam && window.__scene.cameras.cameras.includes(window.__scene.wifeCam),
      husbandX: Math.round(window.__scene.husband.x),
      wifeX: Math.round(window.__scene.wife.x),
      husbandY: Math.round(window.__scene.husband.y),
      wifeY: Math.round(window.__scene.wife.y),
      scrollY: Math.round(window.__scene.cameras.main.scrollY),
      visibleWorldBottom: Math.round(window.__scene.cameras.main.scrollY + window.__scene.cameras.main.height),
    }));
    expect(mergeState.state).toBe("shared");
    expect(mergeState.hasWifeCam).toBeFalsy();
    expect(Math.abs(mergeState.wifeX - mergeState.husbandX)).toBeLessThanOrEqual(80);
    expect(Math.abs(mergeState.wifeY - mergeState.husbandY)).toBeLessThanOrEqual(12);
    expect(mergeState.scrollY).toBeLessThanOrEqual(1);
    expect(mergeState.visibleWorldBottom).toBeLessThanOrEqual(541);
    await page.screenshot({ path: path.join(outDir, `${name}-merged.png`), fullPage: true });

    await page.evaluate(() => {
      const scene = window.__scene;
      scene.husband.setX(5020);
      scene.wife.setX(5082);
      scene.updateStage(scene.husband, { stageForYear: () => "adult" }, 2025);
      scene.updateStage(scene.wife, { stageForYear: () => "adult" }, 2025);
    });
    const weddingState = await page.evaluate(() => ({
      husbandStage: window.__scene.husband.stage,
      wifeStage: window.__scene.wife.stage,
      husbandFrame: window.__scene.husband.frame.name,
      wifeFrame: window.__scene.wife.frame.name,
    }));
    expect(weddingState.husbandStage).toBe("wedding");
    expect(weddingState.wifeStage).toBe("wedding");
    expect([12, 13]).toContain(weddingState.husbandFrame);
    expect([14, 15]).toContain(weddingState.wifeFrame);

    await page.evaluate(() => window.__showEndingPhoto());
    await page.waitForTimeout(1000);
    const endingPhotoState = await page.locator("#ending-photo").evaluate((el) => ({
      shown: el.classList.contains("show"),
      opacity: Number.parseFloat(getComputedStyle(el).opacity),
    }));
    expect(endingPhotoState.shown).toBeTruthy();
    expect(endingPhotoState.opacity).toBeGreaterThan(0.5);

    expect(errors).toEqual([]);
    await context.close();
  });
}

test("desktop ending flow uses the timeline ending and fades in the photo", async ({ browser }) => {
  const context = await browser.newContext({
    viewport: { width: 1180, height: 720 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (error) => errors.push(String(error)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  await page.goto(baseURL, { waitUntil: "networkidle" });
  await page.waitForSelector("canvas");
  await page.waitForFunction(() => window.__scene && window.__scene.husband && window.__scene.wife);
  await page.locator("#start").click();
  await page.waitForTimeout(500);

  const endingState = await page.evaluate(() => {
    const scene = window.__scene;
    scene.state = "shared";
    scene.sharedHoldUntil = 0;
    scene.husband.setX(5200);
    scene.wife.setX(5260);
    scene.placeOnGround(scene.husband, scene.husband.groundY);
    scene.placeOnGround(scene.wife, scene.husband.groundY);
    scene.seen.delete("ending");
    scene.ending = false;
    scene.update();
    return {
      ending: scene.ending,
      seenEnding: scene.seen.has("ending"),
      title: document.getElementById("story-title").textContent,
      text: document.getElementById("story-text").textContent,
      visible: document.getElementById("story-card").classList.contains("show"),
    };
  });
  expect(endingState.ending).toBeTruthy();
  expect(endingState.seenEnding).toBeTruthy();
  expect(endingState.visible).toBeTruthy();
  expect(endingState.title).toContain("2026 · 함께 사는 오늘");
  expect(endingState.text).toContain("결혼 후의 삶은 거창한 장면보다");

  await page.waitForTimeout(9200);
  const photoState = await page.locator("#ending-photo").evaluate((el) => ({
    shown: el.classList.contains("show"),
    opacity: Number.parseFloat(getComputedStyle(el).opacity),
    ariaHidden: el.getAttribute("aria-hidden"),
  }));
  expect(photoState.shown).toBeTruthy();
  expect(photoState.opacity).toBeGreaterThan(0.9);
  expect(photoState.ariaHidden).toBe("false");
  expect(errors).toEqual([]);
  await context.close();
});
