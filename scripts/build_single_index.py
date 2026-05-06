from __future__ import annotations

import base64
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data_uri(path: str, mime: str) -> str:
    raw = (ROOT / path).read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


events = json.loads((ROOT / "assets/data/events.json").read_text(encoding="utf-8"))

assets = {
    "sprite": data_uri("assets/generated/couple-sprite-clean.png", "image/png"),
    "panorama": data_uri("assets/generated/timeline-panorama.jpg", "image/jpeg"),
    "wedding_photo": data_uri("assets/imgs/wedding_pics/DSC00038.jpg", "image/jpeg"),
    "soft_bgm": data_uri("assets/generated/timeline-soft.wav", "audio/wav"),
    "climax_bgm": data_uri("assets/generated/timeline-climax.wav", "audio/wav"),
    "forest_back": data_uri("assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-back-trees.png", "image/png"),
    "forest_middle": data_uri("assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-middle-trees.png", "image/png"),
    "forest_front": data_uri("assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-front-trees.png", "image/png"),
    "forest_lights": data_uri("assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-lights.png", "image/png"),
}

html = """<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no" />
    <title>우리의 시간</title>
    <style>
      :root {
        color-scheme: dark;
        --page: #101318;
        --ink: #fff7e6;
        --paper: rgba(22, 20, 24, 0.84);
        --gold: #ffe19a;
      }
      * { box-sizing: border-box; }
      html, body {
        width: 100%;
        height: 100%;
        margin: 0;
        overflow: hidden;
        background: var(--page);
        color: var(--ink);
        touch-action: none;
        -webkit-user-select: none;
        user-select: none;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      }
      #app {
        position: fixed;
        inset: 0;
        display: grid;
        place-items: center;
        background: radial-gradient(circle at 50% 20%, #2b3239 0%, #101318 70%);
      }
      #game {
        width: 100vw;
        height: 100dvh;
        max-width: 1180px;
        max-height: 720px;
        aspect-ratio: 16 / 9;
      }
      canvas {
        display: block;
        width: 100%;
        height: 100%;
        image-rendering: pixelated;
      }
      #story-card {
        position: fixed;
        left: max(14px, env(safe-area-inset-left));
        right: max(14px, env(safe-area-inset-right));
        top: max(12px, env(safe-area-inset-top));
        z-index: 10;
        max-width: 760px;
        margin: 0 auto;
        padding: clamp(12px, 2.4vw, 20px) clamp(14px, 3vw, 24px);
        border: 1px solid rgba(255, 225, 154, 0.7);
        border-radius: 8px;
        background: var(--paper);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.32);
        backdrop-filter: blur(8px);
        pointer-events: none;
        opacity: 0;
        transform: translateY(-10px);
        transition: opacity 220ms ease, transform 220ms ease;
      }
      #story-card.show {
        opacity: 1;
        transform: translateY(0);
      }
      #story-title {
        display: block;
        color: var(--gold);
        font-weight: 800;
        font-size: clamp(14px, 2.1vw, 20px);
        line-height: 1.35;
        margin-bottom: 6px;
      }
      #story-text {
        margin: 0;
        color: #fff8e8;
        font-size: clamp(13px, 1.8vw, 17px);
        line-height: 1.62;
        word-break: keep-all;
        overflow-wrap: anywhere;
      }
      #wedding-photo {
        width: min(28vw, 180px);
        aspect-ratio: 16 / 10;
        object-fit: cover;
        border: 1px solid rgba(255, 225, 154, 0.55);
        border-radius: 6px;
        float: right;
        margin: 2px 0 8px 14px;
        display: none;
      }
      #story-card.with-photo #wedding-photo { display: block; }
      #start {
        position: fixed;
        left: 50%;
        top: 50%;
        z-index: 20;
        transform: translate(-50%, -50%);
        width: min(88vw, 420px);
        padding: 18px 22px;
        border: 1px solid rgba(255, 225, 154, 0.8);
        border-radius: 8px;
        background: rgba(18, 18, 22, 0.86);
        color: #fff7e6;
        box-shadow: 0 20px 80px rgba(0, 0, 0, 0.5);
        font: inherit;
        text-align: center;
      }
      #start strong {
        display: block;
        font-size: 22px;
        margin-bottom: 8px;
        color: var(--gold);
      }
      #start span {
        display: block;
        font-size: 14px;
        line-height: 1.5;
      }
      #touch-hints {
        position: fixed;
        left: 0;
        right: 0;
        bottom: max(10px, env(safe-area-inset-bottom));
        z-index: 11;
        display: none;
        justify-content: space-between;
        padding: 0 max(16px, env(safe-area-inset-left)) 0 max(16px, env(safe-area-inset-right));
        pointer-events: none;
        opacity: 0.6;
      }
      .hint {
        width: 54px;
        height: 54px;
        display: grid;
        place-items: center;
        border: 1px solid rgba(255, 255, 255, 0.32);
        border-radius: 50%;
        background: rgba(18, 18, 22, 0.34);
        font-size: 24px;
      }
      @media (pointer: coarse) {
        #touch-hints { display: flex; }
      }
      @media (max-width: 760px) {
        #game {
          width: 100vw;
          height: 100dvh;
          max-width: none;
          max-height: none;
        }
        #story-card {
          max-height: min(38dvh, 210px);
          overflow: hidden;
        }
        #wedding-photo {
          width: min(34vw, 132px);
        }
      }
    </style>
  </head>
  <body>
    <div id="app"><div id="game"></div></div>
    <section id="story-card" aria-live="polite">
      <img id="wedding-photo" alt="" src="__WEDDING_PHOTO__" />
      <strong id="story-title"></strong>
      <p id="story-text"></p>
    </section>
    <button id="start" type="button">
      <strong>우리의 시간</strong>
      <span>화면을 누르면 음악과 함께 시작합니다.<br />PC는 A/D/W, 방향키를 쓰고 모바일은 좌우 영역을 눌러 걸어요.</span>
    </button>
    <div id="touch-hints"><div class="hint">‹</div><div class="hint">›</div></div>
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.90.0/dist/phaser.min.js"></script>
    <script>
      (() => {
        const ASSETS = {
          sprite: "__SPRITE__",
          panorama: "__PANORAMA__",
          forestBack: "__FOREST_BACK__",
          forestMiddle: "__FOREST_MIDDLE__",
          forestFront: "__FOREST_FRONT__",
          forestLights: "__FOREST_LIGHTS__",
          softBgm: "__SOFT_BGM__",
          climaxBgm: "__CLIMAX_BGM__"
        };
        const TIMELINE = __EVENTS__;
        const GAME_W = 960;
        const GAME_H = 540;
        const HALF_H = GAME_H / 2;
        const WORLD_W = 5360;
        const MEET_X = 3560;
        const END_X = 5200;
        const TOP_GROUND = 430;
        const BOTTOM_GROUND = 970;
        const SPEED = 185;
        const JUMP = 470;
        const GRAVITY = 980;

        const stageRows = {
          husband: { baby: 0, student: 1, adult: 2 },
          wife: { baby: 3, student: 4, adult: 5 }
        };
        const profiles = {
          husband: {
            label: "권영호",
            birthYear: 1987,
            startX: 140,
            meetX: MEET_X - 36,
            groundY: TOP_GROUND,
            stageForYear(year) {
              if (year < 1994) return "baby";
              if (year < 2012) return "student";
              return "adult";
            }
          },
          wife: {
            label: "방은지",
            birthYear: 1994,
            startX: 140,
            meetX: MEET_X + 36,
            groundY: BOTTOM_GROUND,
            stageForYear(year) {
              if (year < 2001) return "baby";
              if (year < 2017) return "student";
              return "adult";
            }
          }
        };

        class MusicDeck {
          constructor() {
            this.soft = new Audio(ASSETS.softBgm);
            this.climax = new Audio(ASSETS.climaxBgm);
            this.soft.loop = true;
            this.climax.loop = true;
            this.soft.volume = 0;
            this.climax.volume = 0;
            this.started = false;
            this.mode = "soft";
          }
          async start() {
            if (this.started) return;
            this.started = true;
            try {
              await this.soft.play();
              await this.climax.play();
              this.fadeTo("soft");
            } catch (error) {
              this.started = false;
            }
          }
          fadeTo(mode) {
            this.mode = mode;
            const start = performance.now();
            const fromSoft = this.soft.volume;
            const fromClimax = this.climax.volume;
            const toSoft = mode === "soft" ? 0.34 : 0.05;
            const toClimax = mode === "climax" ? 0.44 : 0;
            const tick = (now) => {
              const t = Math.min(1, (now - start) / 1600);
              const e = 1 - Math.pow(1 - t, 3);
              this.soft.volume = fromSoft + (toSoft - fromSoft) * e;
              this.climax.volume = fromClimax + (toClimax - fromClimax) * e;
              if (t < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
          }
        }

        const storyCard = document.getElementById("story-card");
        const storyTitle = document.getElementById("story-title");
        const storyText = document.getElementById("story-text");
        const startButton = document.getElementById("start");
        let storyTimer = 0;

        function showStory(event) {
          if (!event) return;
          storyTitle.textContent = `${event.year} · ${event.title}`;
          storyText.textContent = event.text;
          storyCard.classList.toggle("with-photo", event.id === "wedding");
          storyCard.classList.add("show");
          window.clearTimeout(storyTimer);
          storyTimer = window.setTimeout(() => storyCard.classList.remove("show"), event.id === "wedding" ? 7200 : 5600);
        }

        function roundedYear(value) {
          return Math.max(1987, Math.min(2026, Math.round(value)));
        }

        function yearFor(player, profile, shared) {
          if (shared) {
            const p = Phaser.Math.Clamp((player.x - MEET_X) / (END_X - MEET_X), 0, 1);
            return roundedYear(Phaser.Math.Linear(2020, 2026, p));
          }
          const p = Phaser.Math.Clamp((player.x - profile.startX) / (profile.meetX - profile.startX), 0, 1);
          return roundedYear(Phaser.Math.Linear(profile.birthYear, 2020, p));
        }

        class MainScene extends Phaser.Scene {
          constructor() {
            super("MainScene");
            this.state = "split";
            this.merge = 0;
            this.seen = new Set();
            this.touch = { left: false, right: false, jump: false };
            this.music = new MusicDeck();
          }
          preload() {
            this.load.image("bg", ASSETS.panorama);
            this.load.image("forestBack", ASSETS.forestBack);
            this.load.image("forestMiddle", ASSETS.forestMiddle);
            this.load.image("forestFront", ASSETS.forestFront);
            this.load.image("forestLights", ASSETS.forestLights);
            this.load.spritesheet("couple", ASSETS.sprite, { frameWidth: 180, frameHeight: 180 });
          }
          create() {
            this.physics.world.setBounds(0, 0, WORLD_W, 1080);
            this.createWorld();
            this.createPlayers();
            this.createCameras();
            this.createHud();
            this.createControls();
            this.createTouchControls();
            this.input.keyboard.once("keydown", () => this.begin());
            this.input.once("pointerdown", () => this.begin());
            startButton.addEventListener("click", () => this.begin(), { once: true });
            this.time.delayedCall(500, () => showStory({
              year: 1987,
              title: "아직 서로를 모르던 첫 장",
              text: "두 사람의 시간은 멀리 떨어진 곳에서 조용히 시작되었습니다. 언젠가 한 문장으로 이어질 줄은, 아무도 알지 못했습니다."
            }));
          }
          begin() {
            startButton.style.display = "none";
            this.music.start();
          }
          createWorld() {
            for (const y of [270, 810]) {
              this.add.image(WORLD_W / 2, y, "bg").setDisplaySize(WORLD_W, 540).setDepth(0);
              this.add.rectangle(WORLD_W / 2, y + 180, WORLD_W, 76, 0x1e2419, 0.26).setDepth(1);
              this.addForestParallax(y);
            }
            this.platforms = this.physics.add.staticGroup();
            this.addGround(TOP_GROUND);
            this.addGround(BOTTOM_GROUND);
            this.addMilestones(TOP_GROUND);
            this.addMilestones(BOTTOM_GROUND);
          }
          addForestParallax(centerY) {
            const x = 4820;
            const width = 1180;
            this.add.tileSprite(x, centerY - 88, width, 236, "forestBack")
              .setTileScale(1.9, 1.9)
              .setAlpha(0.22)
              .setDepth(2);
            this.add.tileSprite(x, centerY - 30, width, 260, "forestMiddle")
              .setTileScale(2.05, 2.05)
              .setAlpha(0.28)
              .setDepth(3);
            this.add.tileSprite(x, centerY + 30, width, 300, "forestFront")
              .setTileScale(2.25, 2.25)
              .setAlpha(0.25)
              .setDepth(6);
            this.add.tileSprite(x, centerY - 96, width, 236, "forestLights")
              .setTileScale(2.1, 2.1)
              .setAlpha(0.2)
              .setDepth(7);
          }
          addGround(y) {
            const ground = this.add.rectangle(WORLD_W / 2, y + 18, WORLD_W, 34, 0x3b3a23, 0);
            this.physics.add.existing(ground, true);
            this.platforms.add(ground);
          }
          addMilestones(baseY) {
            const labels = [
              [1987, 180], [1994, 1140], [2001, 1510], [2012, 2760],
              [2017, 3200], [2020, MEET_X], [2021, 3850], [2025, 4920]
            ];
            for (const [year, x] of labels) {
              this.add.rectangle(x, baseY - 48, 8, 60, 0xffe19a, 0.7).setDepth(4);
              this.add.text(x - 28, baseY - 92, String(year), {
                fontFamily: "monospace",
                fontSize: "14px",
                color: "#241d18",
                backgroundColor: "#ffe19a",
                padding: { x: 5, y: 3 }
              }).setDepth(5);
            }
          }
          createPlayers() {
            this.husband = this.makePlayer("husband", profiles.husband.startX, TOP_GROUND - 86);
            this.wife = this.makePlayer("wife", profiles.wife.startX, BOTTOM_GROUND - 86);
            this.physics.add.collider(this.husband, this.platforms);
            this.physics.add.collider(this.wife, this.platforms);
            for (const owner of ["husband", "wife"]) {
              for (const stage of ["baby", "student", "adult"]) {
                const row = stageRows[owner][stage];
                this.anims.create({
                  key: `${owner}-${stage}-walk`,
                  frames: this.anims.generateFrameNumbers("couple", { start: row * 4, end: row * 4 + 3 }),
                  frameRate: 7,
                  repeat: -1
                });
              }
            }
            this.followPoint = { x: MEET_X, y: TOP_GROUND - 116 };
          }
          makePlayer(owner, x, y) {
            const row = stageRows[owner].baby;
            const sprite = this.physics.add.sprite(x, y, "couple", row * 4)
              .setDepth(20)
              .setScale(0.7)
              .setCollideWorldBounds(true);
            sprite.owner = owner;
            sprite.stage = "baby";
            sprite.body.setSize(76, 124);
            sprite.body.setOffset(52, 38);
            return sprite;
          }
          createCameras() {
            this.cameras.main.setViewport(0, 0, GAME_W, HALF_H);
            this.cameras.main.setBounds(0, 0, WORLD_W, 1080);
            this.cameras.main.startFollow(this.husband, true, 0.08, 0.08, 0, 16);
            this.wifeCam = this.cameras.add(0, HALF_H, GAME_W, HALF_H);
            this.wifeCam.setBounds(0, 0, WORLD_W, 1080);
            this.wifeCam.startFollow(this.wife, true, 0.08, 0.08, 0, 16);
          }
          createHud() {
            this.hud = this.add.text(16, 14, "", {
              fontFamily: "monospace",
              fontSize: "18px",
              color: "#fff7e6",
              backgroundColor: "rgba(16,19,24,0.62)",
              padding: { x: 10, y: 6 }
            }).setDepth(1000).setScrollFactor(0);
          }
          createControls() {
            this.keys = this.input.keyboard.addKeys({
              hLeft: Phaser.Input.Keyboard.KeyCodes.A,
              hRight: Phaser.Input.Keyboard.KeyCodes.D,
              hJump: Phaser.Input.Keyboard.KeyCodes.W,
              wLeft: Phaser.Input.Keyboard.KeyCodes.LEFT,
              wRight: Phaser.Input.Keyboard.KeyCodes.RIGHT,
              wJump: Phaser.Input.Keyboard.KeyCodes.UP,
              restart: Phaser.Input.Keyboard.KeyCodes.R
            });
          }
          createTouchControls() {
            this.input.on("pointerdown", (pointer) => this.setTouch(pointer, true));
            this.input.on("pointermove", (pointer) => {
              if (pointer.isDown) this.setTouch(pointer, true);
            });
            this.input.on("pointerup", (pointer) => this.setTouch(pointer, false));
            this.input.on("pointerupoutside", (pointer) => this.setTouch(pointer, false));
          }
          setTouch(pointer, active) {
            if (!active) {
              this.touch.left = false;
              this.touch.right = false;
              this.touch.jump = false;
              return;
            }
            const x = pointer.x / GAME_W;
            const y = pointer.y / GAME_H;
            this.touch.left = x < 0.44;
            this.touch.right = x > 0.56;
            this.touch.jump = y < 0.35;
          }
          update() {
            if (Phaser.Input.Keyboard.JustDown(this.keys.restart)) {
              this.scene.restart();
              startButton.style.display = "block";
              return;
            }
            const hy = yearFor(this.husband, profiles.husband, this.state !== "split");
            const wy = yearFor(this.wife, profiles.wife, this.state !== "split");
            this.updateStage(this.husband, profiles.husband, hy);
            this.updateStage(this.wife, profiles.wife, wy);
            if (this.state === "split") {
              this.updateSplit(hy, wy);
              return;
            }
            if (this.state === "merging") this.updateMerge();
            else this.updateTogether();
            const year = yearFor(this.husband, profiles.husband, true);
            this.hud.setText(`함께 걷는 시간  ${year}`);
            this.checkSharedEvents(year);
            if (year >= 2026 && !this.ending) this.showEnding();
          }
          updateSplit(hy, wy) {
            this.move(this.husband, this.keys.hLeft.isDown || this.touch.left, this.keys.hRight.isDown || this.touch.right, this.keys.hJump, false);
            this.move(this.wife, this.keys.wLeft.isDown || this.touch.left, this.keys.wRight.isDown || this.touch.right, this.keys.wJump, false);
            this.husband.x = Phaser.Math.Clamp(this.husband.x, profiles.husband.startX, profiles.husband.meetX);
            this.wife.x = Phaser.Math.Clamp(this.wife.x, profiles.wife.startX, profiles.wife.meetX);
            this.hud.setText(`${profiles.husband.label} ${hy}    ${profiles.wife.label} ${wy}`);
            this.checkPersonalEvents(hy, wy);
            if (this.husband.x >= profiles.husband.meetX - 2 && this.wife.x >= profiles.wife.meetX - 2) this.startMerge();
          }
          move(player, left, right, jumpKey, forceWalk) {
            let vx = 0;
            if (right) vx = SPEED;
            else if (left) vx = -SPEED;
            else if (forceWalk) vx = 44;
            player.setVelocityX(vx);
            player.setFlipX(vx < 0);
            if ((Phaser.Input.Keyboard.JustDown(jumpKey) || this.touch.jump) && player.body.blocked.down) {
              player.setVelocityY(-JUMP);
              this.touch.jump = false;
            }
            this.playAnim(player, Math.abs(vx) > 4);
          }
          updateTogether() {
            const left = this.keys.hLeft.isDown || this.keys.wLeft.isDown || this.touch.left;
            const right = this.keys.hRight.isDown || this.keys.wRight.isDown || this.touch.right;
            const jump = Phaser.Input.Keyboard.JustDown(this.keys.hJump) || Phaser.Input.Keyboard.JustDown(this.keys.wJump) || this.touch.jump;
            const vx = right ? SPEED : left ? -SPEED * 0.55 : 48;
            for (const player of [this.husband, this.wife]) {
              player.setVelocityX(vx);
              player.setFlipX(vx < 0);
              if (jump && player.body.blocked.down) player.setVelocityY(-JUMP);
              this.playAnim(player, Math.abs(vx) > 4);
            }
            this.touch.jump = false;
            this.husband.x = Phaser.Math.Clamp(this.husband.x, MEET_X, END_X);
            this.wife.x = Phaser.Math.Clamp(this.wife.x, MEET_X + 54, END_X + 60);
            if (Math.abs(this.wife.x - this.husband.x) > 74) this.wife.x = Phaser.Math.Linear(this.wife.x, this.husband.x + 62, 0.06);
            this.followPoint.x = (this.husband.x + this.wife.x) / 2;
            this.followPoint.y = TOP_GROUND - 116;
          }
          playAnim(player, moving) {
            if (moving && player.body.blocked.down) player.anims.play(`${player.owner}-${player.stage}-walk`, true);
            else {
              player.anims.stop();
              player.setFrame(stageRows[player.owner][player.stage] * 4);
            }
          }
          updateStage(player, profile, year) {
            const next = profile.stageForYear(year);
            if (player.stage === next) return;
            player.stage = next;
            const row = stageRows[player.owner][next];
            player.setFrame(row * 4);
            const scale = next === "baby" ? 0.56 : next === "student" ? 0.62 : 0.72;
            player.setScale(scale);
            player.body.setSize(76, 124);
            player.body.setOffset(52, 38);
          }
          checkPersonalEvents(hy, wy) {
            for (const event of TIMELINE.events) {
              if (this.seen.has(event.id)) continue;
              if (event.owner === "husband" && hy >= event.year) this.fireEvent(event);
              if (event.owner === "wife" && wy >= event.year) this.fireEvent(event);
            }
          }
          checkSharedEvents(year) {
            for (const event of TIMELINE.events) {
              if (!this.seen.has(event.id) && event.owner === "shared" && year >= event.year) this.fireEvent(event);
            }
          }
          fireEvent(event) {
            this.seen.add(event.id);
            showStory(event);
          }
          startMerge() {
            this.state = "merging";
            this.husband.setVelocity(0, 0);
            this.wife.setVelocity(0, 0);
            this.husband.setPosition(MEET_X - 38, TOP_GROUND - 86);
            this.wife.setPosition(MEET_X + 42, BOTTOM_GROUND - 86);
            this.husband.body.setAllowGravity(false);
            this.wife.body.setAllowGravity(false);
            this.cameras.main.stopFollow();
            this.wifeCam.stopFollow();
            this.fireEvent(TIMELINE.events.find((event) => event.id === "first-meeting"));
            this.music.fadeTo("climax");
            this.tweens.add({ targets: this.wife, y: TOP_GROUND - 86, duration: 1550, ease: "Sine.InOut" });
          }
          updateMerge() {
            this.merge = Phaser.Math.Linear(this.merge, 1, 0.035);
            const mainH = Phaser.Math.Linear(HALF_H, GAME_H, this.merge);
            const wifeH = Phaser.Math.Linear(HALF_H, 0, this.merge);
            this.cameras.main.setViewport(0, 0, GAME_W, mainH);
            this.wifeCam.setViewport(0, GAME_H - wifeH, GAME_W, Math.max(1, wifeH));
            this.wifeCam.setAlpha(1 - this.merge);
            const targetX = MEET_X - GAME_W / 2;
            const targetY = TOP_GROUND - GAME_H / 2 + 46;
            this.cameras.main.scrollX = Phaser.Math.Linear(this.cameras.main.scrollX, targetX, 0.045);
            this.cameras.main.scrollY = Phaser.Math.Linear(this.cameras.main.scrollY, targetY, 0.045);
            if (this.merge > 0.985) {
              this.state = "shared";
              this.cameras.remove(this.wifeCam);
              this.cameras.main.setViewport(0, 0, GAME_W, GAME_H);
              this.cameras.main.startFollow(this.followPoint, true, 0.08, 0.08);
              this.husband.body.setAllowGravity(true);
              this.wife.body.setAllowGravity(true);
              this.husband.setX(MEET_X + 16);
              this.wife.setPosition(MEET_X + 78, TOP_GROUND - 86);
            }
          }
          showEnding() {
            this.ending = true;
            showStory({
              year: 2026,
              title: "아직 쓰이지 않은 편지",
              text: "우리가 지나온 모든 계절은 이 문장을 쓰기 위한 연습이었는지도 모릅니다. 이제 다음 장은, 같은 손을 잡고 천천히 써 내려가요."
            });
            this.time.delayedCall(5000, () => this.cameras.main.fadeOut(2600, 16, 19, 24));
          }
        }

        new Phaser.Game({
          type: Phaser.AUTO,
          parent: "game",
          width: GAME_W,
          height: GAME_H,
          backgroundColor: "#101318",
          pixelArt: true,
          roundPixels: true,
          physics: {
            default: "arcade",
            arcade: { gravity: { y: GRAVITY }, debug: false }
          },
          scale: {
            mode: Phaser.Scale.FIT,
            autoCenter: Phaser.Scale.CENTER_BOTH
          },
          scene: [MainScene]
        });
      })();
    </script>
  </body>
</html>
"""

replacements = {
    "__SPRITE__": assets["sprite"],
    "__PANORAMA__": assets["panorama"],
    "__FOREST_BACK__": assets["forest_back"],
    "__FOREST_MIDDLE__": assets["forest_middle"],
    "__FOREST_FRONT__": assets["forest_front"],
    "__FOREST_LIGHTS__": assets["forest_lights"],
    "__WEDDING_PHOTO__": assets["wedding_photo"],
    "__SOFT_BGM__": assets["soft_bgm"],
    "__CLIMAX_BGM__": assets["climax_bgm"],
    "__EVENTS__": json.dumps(events, ensure_ascii=False),
}

for key, value in replacements.items():
    html = html.replace(key, value)

(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"wrote index.html ({len(html.encode('utf-8')):,} bytes)")
