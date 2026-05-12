const { test, expect } = require("@playwright/test");

const baseURL = process.env.TEST_URL || "http://127.0.0.1:4173/";

function rounded(value) {
  return Math.round(value * 10) / 10;
}

test("year-by-year split lane flow stays stable before merge", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(String(error)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  await page.goto(baseURL, { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__scene && window.__scene.husband && window.__scene.wife);

  const beforeStart = await page.evaluate(() => {
    const scene = window.__scene;
    return {
      husbandX: Math.round(scene.husband.x),
      wifeX: Math.round(scene.wife.x),
      husbandY: Math.round(scene.husband.y * 10) / 10,
      wifeY: Math.round(scene.wife.y * 10) / 10,
      husbandVelocityY: Math.round(scene.husband.body.velocity.y * 10) / 10,
      wifeVelocityY: Math.round(scene.wife.body.velocity.y * 10) / 10,
      husbandStage: scene.husband.stage,
      wifeStage: scene.wife.stage,
      hud: scene.hud.text,
    };
  });
  expect(beforeStart).toMatchObject({
    husbandX: 180,
    wifeX: 1140,
    husbandVelocityY: 0,
    wifeVelocityY: 0,
    husbandStage: "baby",
    wifeStage: "baby",
    hud: "",
  });
  expect(beforeStart.husbandY).toBeLessThan(500);
  expect(beforeStart.wifeY).toBeGreaterThan(900);

  await page.locator("#start").click();
  await page.waitForTimeout(300);

  await page.keyboard.down("d");
  for (let i = 0; i < 35; i += 1) {
    await page.waitForTimeout(120);
    const state = await page.evaluate(() => {
      const scene = window.__scene;
      return {
        x: Math.round(scene.husband.x * 10) / 10,
        y: Math.round(scene.husband.y * 10) / 10,
        stage: scene.husband.stage,
        bottom: Math.round(scene.husband.body.bottom * 10) / 10,
        velocityY: Math.round(scene.husband.body.velocity.y * 10) / 10,
        yearText: scene.hud.text,
      };
    });
    expect(state.y).toBeLessThan(520);
    expect(state.bottom).toBeLessThan(470);
    expect(Math.abs(state.velocityY)).toBeLessThan(120);
  }
  await page.keyboard.up("d");

  const husbandAfter1994 = await page.evaluate(() => {
    const scene = window.__scene;
    return {
      x: Math.round(scene.husband.x * 10) / 10,
      y: Math.round(scene.husband.y * 10) / 10,
      stage: scene.husband.stage,
      wifeX: Math.round(scene.wife.x * 10) / 10,
      wifeY: Math.round(scene.wife.y * 10) / 10,
      wifeStage: scene.wife.stage,
      text: scene.hud.text,
    };
  });
  expect(husbandAfter1994.x).toBeGreaterThan(900);
  expect(husbandAfter1994.y).toBeLessThan(520);
  expect(husbandAfter1994.wifeX).toBe(1140);
  expect(husbandAfter1994.wifeY).toBeGreaterThan(900);
  expect(husbandAfter1994.wifeStage).toBe("baby");

  await page.keyboard.down("ArrowRight");
  let sawWifeStudent = false;
  for (let i = 0; i < 55; i += 1) {
    await page.waitForTimeout(120);
    const state = await page.evaluate(() => {
      const scene = window.__scene;
      return {
        x: Math.round(scene.wife.x * 10) / 10,
        y: Math.round(scene.wife.y * 10) / 10,
        stage: scene.wife.stage,
        bottom: Math.round(scene.wife.body.bottom * 10) / 10,
        velocityY: Math.round(scene.wife.body.velocity.y * 10) / 10,
      };
    });
    expect(state.y).toBeGreaterThan(900);
    expect(state.y).toBeLessThan(950);
    expect(state.bottom).toBeLessThan(1010);
    expect(Math.abs(state.velocityY)).toBeLessThan(120);
    if (state.stage === "student") sawWifeStudent = true;
  }
  await page.keyboard.up("ArrowRight");
  expect(sawWifeStudent).toBeTruthy();
  expect(errors).toEqual([]);
});

test("split touch control targets only the touched lane", async ({ page }) => {
  await page.goto(baseURL, { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__scene && window.__scene.husband && window.__scene.wife);
  await page.locator("#start").click();
  await page.waitForTimeout(300);

  const start = await page.evaluate(() => ({
    husbandX: window.__scene.husband.x,
    wifeX: window.__scene.wife.x,
  }));

  await page.mouse.move(760, 160);
  await page.mouse.down();
  await page.waitForTimeout(450);
  await page.mouse.up();
  await page.waitForTimeout(120);

  const afterTopTouch = await page.evaluate(() => ({
    husbandX: window.__scene.husband.x,
    wifeX: window.__scene.wife.x,
  }));
  expect(afterTopTouch.husbandX - start.husbandX).toBeGreaterThan(30);
  expect(Math.abs(afterTopTouch.wifeX - start.wifeX)).toBeLessThan(3);

  await page.mouse.move(760, 520);
  await page.mouse.down();
  await page.waitForTimeout(450);
  await page.mouse.up();

  const afterBottomTouch = await page.evaluate(() => ({
    husbandX: window.__scene.husband.x,
    wifeX: window.__scene.wife.x,
  }));
  expect(afterBottomTouch.wifeX - afterTopTouch.wifeX).toBeGreaterThan(30);
  expect(Math.abs(afterBottomTouch.husbandX - afterTopTouch.husbandX)).toBeLessThan(8);
});

test("animation-frame audit keeps husband on the top lane through 1994", async ({ page }) => {
  await page.goto(baseURL, { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__scene && window.__scene.husband && window.__scene.wife);
  await page.locator("#start").click();
  await page.waitForTimeout(300);
  await page.keyboard.down("d");
  const samples = await page.evaluate(
    () =>
      new Promise((resolve) => {
        const rows = [];
        const step = () => {
          const scene = window.__scene;
          rows.push({
            x: scene.husband.x,
            y: scene.husband.y,
            footY: scene.visualFootY(scene.husband),
            bottom: scene.husband.body.bottom,
            stage: scene.husband.stage,
            wifeX: scene.wife.x,
            wifeY: scene.wife.y,
          });
          if (rows.length >= 430 || scene.husband.x >= 1220) resolve(rows);
          else requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      })
  );
  await page.keyboard.up("d");

  expect(samples.length).toBeGreaterThan(300);
  expect(samples.some((sample) => sample.x < 1140 && sample.stage === "baby")).toBeTruthy();
  expect(samples.some((sample) => sample.x >= 1140 && sample.stage === "student")).toBeTruthy();
  for (const sample of samples) {
    expect(sample.y).toBeLessThan(520);
    expect(sample.bottom).toBeLessThan(470);
    expect(Math.abs(sample.footY - 430)).toBeLessThanOrEqual(6);
    expect(sample.wifeX).toBe(1140);
    expect(sample.wifeY).toBeGreaterThan(900);
  }
});
