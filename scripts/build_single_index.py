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
    "sprite": data_uri("assets/generated/couple-sprite-final-2f.png", "image/png"),
    "panorama": data_uri("assets/generated/timeline-panorama.jpg", "image/jpeg"),
    "wedding_photo": data_uri("assets/generated/YJH01044.jpg", "image/jpeg"),
    "bgm": data_uri("assets/generated/The_Amber_Path.mp4", "audio/mp4"),
    "forest_back": data_uri(
        "assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-back-trees.png",
        "image/png",
    ),
    "forest_middle": data_uri(
        "assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-middle-trees.png",
        "image/png",
    ),
    "forest_front": data_uri(
        "assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-front-trees.png",
        "image/png",
    ),
    "forest_lights": data_uri(
        "assets/generated/cc0-forest/parallax_forest_pack/layers/parallax-forest-lights.png",
        "image/png",
    ),
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
      .story-panel {
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
      .story-panel.show {
        opacity: 1;
        transform: translateY(0);
      }
      .story-title {
        display: block;
        color: var(--gold);
        font-weight: 800;
        font-size: clamp(14px, 2.1vw, 20px);
        line-height: 1.35;
        margin-bottom: 6px;
      }
      .story-text {
        margin: 0;
        color: #fff8e8;
        font-size: clamp(13px, 1.8vw, 17px);
        line-height: 1.62;
        word-break: keep-all;
        overflow-wrap: anywhere;
      }
      .split-story {
        width: min(45vw, 520px);
        max-width: 520px;
        right: auto;
        margin: 0;
      }
      #story-card-husband {
        top: max(12px, env(safe-area-inset-top));
      }
      #story-card-wife {
        top: calc(50dvh + 12px);
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
      #ending-photo {
        position: fixed;
        inset: 0;
        z-index: 30;
        display: grid;
        place-items: center;
        padding: max(24px, env(safe-area-inset-top)) max(18px, env(safe-area-inset-right)) max(24px, env(safe-area-inset-bottom)) max(18px, env(safe-area-inset-left));
        background: #000;
        opacity: 0;
        pointer-events: none;
        transition: opacity 900ms ease;
      }
      #ending-photo.show {
        opacity: 1;
      }
      #ending-photo img {
        width: min(88vw, 920px);
        max-height: 82dvh;
        object-fit: contain;
        border: 1px solid rgba(255, 225, 154, 0.46);
        border-radius: 8px;
        box-shadow: 0 22px 90px rgba(0, 0, 0, 0.7);
        opacity: 0;
        transform: scale(0.985);
        transition: opacity 1600ms ease 520ms, transform 1600ms ease 520ms;
      }
      #ending-photo.show img {
        opacity: 1;
        transform: scale(1);
      }
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
        .story-panel {
          max-height: min(45dvh, 260px);
          overflow-y: auto;
          overscroll-behavior: contain;
        }
        .split-story {
          width: calc(100vw - 28px - env(safe-area-inset-left) - env(safe-area-inset-right));
          max-width: none;
        }
        #story-card-husband {
          top: max(10px, env(safe-area-inset-top));
        }
        #story-card-wife {
          top: calc(50dvh + 10px);
        }
        #wedding-photo {
          width: min(34vw, 132px);
        }
      }
    </style>
  </head>
  <body>
    <div id="app"><div id="game"></div></div>
    <section id="story-card" class="story-panel" aria-live="polite">
      <img id="wedding-photo" alt="" src="__WEDDING_PHOTO__" />
      <strong id="story-title" class="story-title"></strong>
      <p id="story-text" class="story-text"></p>
    </section>
    <section id="story-card-husband" class="story-panel split-story" aria-live="polite">
      <strong id="story-title-husband" class="story-title"></strong>
      <p id="story-text-husband" class="story-text"></p>
    </section>
    <section id="story-card-wife" class="story-panel split-story" aria-live="polite">
      <strong id="story-title-wife" class="story-title"></strong>
      <p id="story-text-wife" class="story-text"></p>
    </section>
    <section id="ending-photo" aria-hidden="true">
      <img alt="웨딩사진" src="__WEDDING_PHOTO__" />
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
          bgm: "__BGM__"
        };
        const TIMELINE = __EVENTS__;
        const GAME_W = 960;
        const GAME_H = 540;
        const HALF_H = GAME_H / 2;
        const SHARED_SCROLL_Y = 0;
        const SHARED_FOLLOW_Y = GAME_H / 2;
        const WORLD_W = 5360;
        const MEET_X = 3560;
        const END_X = 5200;
        const YEAR_X = {
          1987: 180,
          1994: 1140,
          2001: 1510,
          2012: 2760,
          2017: 3200,
          2020: MEET_X,
          2021: 3850,
          2025: 4920
        };
        const SPLIT_YEAR_ANCHORS = Object.entries(YEAR_X)
          .map(([year, x]) => ({ year: Number(year), x }))
          .sort((a, b) => a.year - b.year);
        const SHARED_YEAR_ANCHORS = [
          { year: 2020, x: YEAR_X[2020] },
          { year: 2021, x: YEAR_X[2021] },
          { year: 2025, x: YEAR_X[2025] },
          { year: 2026, x: END_X }
        ];
        const TOP_GROUND = 430;
        const BOTTOM_GROUND = 970;
        const MERGE_DURATION = 2800;
        const SPEED = 185;
        const JUMP = 470;
        const GRAVITY = 980;
        const SPRITE_FRAME = 220;
        const FRAMES_PER_STAGE = 2;
        const BODY = { width: 84, height: 140, offsetX: 68, offsetY: 50 };
        const SCALE_BY_STAGE = { baby: 0.48, student: 0.54, adult: 0.62, wedding: 0.62 };

        const stageRows = {
          husband: { baby: 0, student: 1, adult: 2, wedding: 6 },
          wife: { baby: 3, student: 4, adult: 5, wedding: 7 }
        };
        const profiles = {
          husband: {
            label: "권영호",
            birthYear: 1987,
            startX: YEAR_X[1987],
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
            startX: YEAR_X[1994],
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
            this.track = new Audio(ASSETS.bgm);
            this.track.loop = true;
            this.track.volume = 0;
            this.started = false;
            this.mode = "soft";
          }
          async start() {
            if (this.started) return;
            this.started = true;
            try {
              await this.track.play();
              this.fadeTo("soft");
            } catch (error) {
              this.started = false;
            }
          }
          fadeTo(mode) {
            this.mode = mode;
            const start = performance.now();
            const fromVolume = this.track.volume;
            const toVolume = mode === "climax" ? 0.44 : 0.34;
            const setVolume = (audio, value) => {
              audio.volume = Phaser.Math.Clamp(value, 0, 1);
            };
            const tick = (now) => {
              const t = Phaser.Math.Clamp((now - start) / 1600, 0, 1);
              const e = 1 - Math.pow(1 - t, 3);
              setVolume(this.track, fromVolume + (toVolume - fromVolume) * e);
              if (t < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
          }
        }

        const storyChannels = {
          shared: {
            card: document.getElementById("story-card"),
            title: document.getElementById("story-title"),
            text: document.getElementById("story-text"),
            timer: 0
          },
          husband: {
            card: document.getElementById("story-card-husband"),
            title: document.getElementById("story-title-husband"),
            text: document.getElementById("story-text-husband"),
            timer: 0
          },
          wife: {
            card: document.getElementById("story-card-wife"),
            title: document.getElementById("story-title-wife"),
            text: document.getElementById("story-text-wife"),
            timer: 0
          }
        };
        const startButton = document.getElementById("start");
        const endingPhoto = document.getElementById("ending-photo");

        function showStory(event, channel = "shared") {
          if (!event) return;
          if (channel === "shared") {
            hideStory("husband");
            hideStory("wife");
          } else {
            hideStory("shared");
          }
          const target = storyChannels[channel] || storyChannels.shared;
          target.title.textContent = `${event.year} · ${event.title}`;
          target.text.textContent = event.text;
          target.card.classList.toggle("with-photo", channel === "shared" && event.id === "wedding");
          target.card.classList.add("show");
          window.clearTimeout(target.timer);
          target.timer = window.setTimeout(() => target.card.classList.remove("show"), event.id === "wedding" ? 7200 : 5600);
        }
        function hideStory(channel) {
          const target = storyChannels[channel];
          if (!target) return;
          window.clearTimeout(target.timer);
          target.card.classList.remove("show");
        }
        function showEndingPhoto() {
          hideStory("shared");
          hideStory("husband");
          hideStory("wife");
          endingPhoto.classList.add("show");
          endingPhoto.setAttribute("aria-hidden", "false");
        }
        function resetOverlays() {
          hideStory("shared");
          hideStory("husband");
          hideStory("wife");
          endingPhoto.classList.remove("show");
          endingPhoto.setAttribute("aria-hidden", "true");
        }
        window.__showEndingPhoto = showEndingPhoto;

        function boundedYear(value) {
          return Math.max(1987, Math.min(2026, Math.floor(value)));
        }

        function yearFromAnchors(x, anchors) {
          if (x <= anchors[0].x) return anchors[0].year;
          for (let i = 0; i < anchors.length - 1; i += 1) {
            const from = anchors[i];
            const to = anchors[i + 1];
            if (x < to.x) {
              const p = Phaser.Math.Clamp((x - from.x) / (to.x - from.x), 0, 1);
              return boundedYear(Phaser.Math.Linear(from.year, to.year, p));
            }
          }
          return anchors[anchors.length - 1].year;
        }

        function yearFor(player, profile, shared) {
          if (shared) {
            return yearFromAnchors(player.x, SHARED_YEAR_ANCHORS);
          }
          if (player.x >= profile.meetX - 2) return 2020;
          const anchors = SPLIT_YEAR_ANCHORS.filter((anchor) => anchor.year >= profile.birthYear && anchor.year <= 2020);
          return yearFromAnchors(player.x, anchors);
        }

        class MainScene extends Phaser.Scene {
          constructor() {
            super("MainScene");
            this.state = "split";
            this.merge = 0;
            this.seen = new Set();
            this.ready = { husband: false, wife: false };
            this.sharedHoldUntil = 0;
            this.started = false;
            this.touch = this.emptyTouch();
            this.music = new MusicDeck();
          }
          preload() {
            this.load.image("bg", ASSETS.panorama);
            this.load.image("forestBack", ASSETS.forestBack);
            this.load.image("forestMiddle", ASSETS.forestMiddle);
            this.load.image("forestFront", ASSETS.forestFront);
            this.load.image("forestLights", ASSETS.forestLights);
            this.load.spritesheet("couple", ASSETS.sprite, { frameWidth: SPRITE_FRAME, frameHeight: SPRITE_FRAME });
          }
          create() {
            window.__scene = this;
            resetOverlays();
            startButton.style.display = "block";
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
            this.time.delayedCall(500, () => {
              if (!this.started) return;
              const hasSplitStory = storyChannels.husband.card.classList.contains("show") || storyChannels.wife.card.classList.contains("show");
              if (this.state === "split" && hasSplitStory) return;
              showStory({
                year: 1987,
                title: "아직 서로를 모르던 첫 장",
                text: "두 사람의 시간은 멀리 떨어진 곳에서 조용히 시작되었습니다. 언젠가 한 문장으로 이어질 줄은, 아무도 알지 못했습니다."
              });
            });
          }
          begin() {
            if (this.started) return;
            this.started = true;
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
            const ground = this.add.rectangle(WORLD_W / 2, y + 17, WORLD_W, 34, 0x3b3a23, 0);
            this.physics.add.existing(ground, true);
            this.platforms.add(ground);
          }
          addMilestones(baseY) {
            const labels = Object.entries(YEAR_X).map(([year, x]) => [Number(year), x]);
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
            this.husband = this.makePlayer("husband", profiles.husband.startX, TOP_GROUND);
            this.wife = this.makePlayer("wife", profiles.wife.startX, BOTTOM_GROUND);
            this.physics.add.collider(this.husband, this.platforms);
            this.physics.add.collider(this.wife, this.platforms);
            for (const owner of ["husband", "wife"]) {
              for (const stage of ["baby", "student", "adult", "wedding"]) {
                const row = stageRows[owner][stage];
                this.anims.create({
                  key: `${owner}-${stage}-walk`,
                  frames: this.anims.generateFrameNumbers("couple", { start: row * FRAMES_PER_STAGE, end: row * FRAMES_PER_STAGE + FRAMES_PER_STAGE - 1 }),
                  frameRate: stage === "baby" ? 4 : 5,
                  repeat: -1
                });
              }
            }
            this.followPoint = { x: MEET_X, y: SHARED_FOLLOW_Y };
          }
          makePlayer(owner, x, groundY) {
            const row = stageRows[owner].baby;
            const sprite = this.physics.add.sprite(x, 0, "couple", row * FRAMES_PER_STAGE)
              .setDepth(20)
              .setScale(SCALE_BY_STAGE.baby)
              .setCollideWorldBounds(true);
            sprite.owner = owner;
            sprite.stage = "baby";
            sprite.groundY = groundY;
            this.configurePlayerBody(sprite);
            this.placeOnGround(sprite, groundY);
            return sprite;
          }
          configurePlayerBody(player) {
            player.body.setSize(BODY.width, BODY.height);
            player.body.setOffset(BODY.offsetX, BODY.offsetY);
          }
          bodyFootOffset(player) {
            return (BODY.offsetY + BODY.height - SPRITE_FRAME / 2) * player.scaleX;
          }
          visualFootY(player) {
            return player.y + this.bodyFootOffset(player);
          }
          isLaneGrounded(player) {
            return player.body.blocked.down || player.body.touching.down || Math.abs(this.visualFootY(player) - player.groundY) <= 26;
          }
          enforceLaneFloor(player, groundY = player.groundY) {
            if (this.visualFootY(player) <= groundY + 5) return;
            this.placeOnGround(player, groundY);
            player.setVelocityY(0);
          }
          placeOnGround(player, groundY = player.groundY) {
            player.groundY = groundY;
            player.y = groundY - this.bodyFootOffset(player);
            if (player.body) player.body.reset(player.x, player.y);
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
          emptyTouch() {
            return {
              shared: { left: false, right: false, jump: false },
              husband: { left: false, right: false, jump: false },
              wife: { left: false, right: false, jump: false }
            };
          }
          clearTouch() {
            this.touch = this.emptyTouch();
          }
          createTouchControls() {
            this.input.on("pointerdown", (pointer) => this.setTouch(pointer, true));
            this.input.on("pointermove", (pointer) => {
              if (pointer.isDown) this.setTouch(pointer, true);
            });
            this.input.on("pointerup", (pointer) => this.setTouch(pointer, false));
            this.input.on("pointerupoutside", (pointer) => this.setTouch(pointer, false));
            window.addEventListener("pointerdown", (event) => this.setTouchFromViewport(event, true), { passive: true });
            window.addEventListener("pointermove", (event) => {
              if (event.buttons || event.pointerType === "touch") this.setTouchFromViewport(event, true);
            }, { passive: true });
            window.addEventListener("pointerup", (event) => this.setTouchFromViewport(event, false), { passive: true });
            window.addEventListener("pointercancel", (event) => this.setTouchFromViewport(event, false), { passive: true });
          }
          setTouch(pointer, active) {
            if (!active) {
              this.clearTouch();
              return;
            }
            const x = pointer.x / GAME_W;
            const y = pointer.y / GAME_H;
            this.applyTouch(x, y);
          }
          setTouchFromViewport(event, active) {
            if (!active) {
              this.clearTouch();
              return;
            }
            if (event.target && event.target.closest && event.target.closest("#start")) return;
            const x = event.clientX / Math.max(1, window.innerWidth);
            const y = event.clientY / Math.max(1, window.innerHeight);
            this.applyTouch(x, y);
          }
          applyTouch(x, y) {
            this.clearTouch();
            const target = this.state === "split" ? (y < 0.5 ? this.touch.husband : this.touch.wife) : this.touch.shared;
            target.left = x < 0.44;
            target.right = x > 0.56;
            target.jump = this.state === "split" ? (y < 0.18 || (y > 0.5 && y < 0.68)) : y < 0.35;
          }
          update() {
            if (Phaser.Input.Keyboard.JustDown(this.keys.restart)) {
              this.scene.restart();
              startButton.style.display = "block";
              return;
            }
            if (!this.started) {
              this.husband.setVelocity(0, 0);
              this.wife.setVelocity(0, 0);
              this.hud.setText("");
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
            if (!this.ready.husband) {
              this.move(this.husband, this.keys.hLeft.isDown || this.touch.husband.left, this.keys.hRight.isDown || this.touch.husband.right, this.keys.hJump, this.touch.husband, false);
            }
            if (!this.ready.wife) {
              this.move(this.wife, this.keys.wLeft.isDown || this.touch.wife.left, this.keys.wRight.isDown || this.touch.wife.right, this.keys.wJump, this.touch.wife, false);
            }
            this.enforceLaneFloor(this.husband, profiles.husband.groundY);
            this.enforceLaneFloor(this.wife, profiles.wife.groundY);
            this.husband.x = Phaser.Math.Clamp(this.husband.x, profiles.husband.startX, profiles.husband.meetX);
            this.wife.x = Phaser.Math.Clamp(this.wife.x, profiles.wife.startX, profiles.wife.meetX);
            if (this.husband.x >= profiles.husband.meetX - 2) this.ready.husband = true;
            if (this.wife.x >= profiles.wife.meetX - 2) this.ready.wife = true;
            if (this.ready.husband) this.lockAtMeet(this.husband, profiles.husband);
            if (this.ready.wife) this.lockAtMeet(this.wife, profiles.wife);
            this.hud.setText(`${profiles.husband.label} ${hy}    ${profiles.wife.label} ${wy}`);
            this.checkPersonalEvents(hy, wy);
            if (this.ready.husband && this.ready.wife) this.startMerge();
          }
          lockAtMeet(player, profile) {
            player.setX(profile.meetX);
            this.placeOnGround(player, profile.groundY);
            player.setVelocity(0, 0);
            this.playAnim(player, false);
          }
          move(player, left, right, jumpKey, touchState, forceWalk) {
            let vx = 0;
            if (right) vx = SPEED;
            else if (left) vx = -SPEED;
            else if (forceWalk) vx = 44;
            player.setVelocityX(vx);
            player.setFlipX(vx < 0);
            if ((Phaser.Input.Keyboard.JustDown(jumpKey) || touchState.jump) && player.body.blocked.down) {
              player.setVelocityY(-JUMP);
              touchState.jump = false;
            }
            this.playAnim(player, Math.abs(vx) > 4);
          }
          updateTogether() {
            if (this.time.now < this.sharedHoldUntil) {
              for (const player of [this.husband, this.wife]) {
                player.setVelocity(0, 0);
                this.playAnim(player, false);
              }
              this.followPoint.x = (this.husband.x + this.wife.x) / 2;
              this.followPoint.y = SHARED_FOLLOW_Y;
              return;
            }
            const sharedTouch = this.touch.shared;
            const left = this.keys.hLeft.isDown || this.keys.wLeft.isDown || sharedTouch.left;
            const right = this.keys.hRight.isDown || this.keys.wRight.isDown || sharedTouch.right;
            const jump = Phaser.Input.Keyboard.JustDown(this.keys.hJump) || Phaser.Input.Keyboard.JustDown(this.keys.wJump) || sharedTouch.jump;
            const vx = right ? SPEED : left ? -SPEED * 0.55 : 48;
            for (const player of [this.husband, this.wife]) {
              player.setVelocityX(vx);
              player.setFlipX(vx < 0);
              if (jump && player.body.blocked.down) player.setVelocityY(-JUMP);
              this.playAnim(player, Math.abs(vx) > 4);
            }
            sharedTouch.jump = false;
            this.enforceLaneFloor(this.husband, TOP_GROUND);
            this.enforceLaneFloor(this.wife, TOP_GROUND);
            this.husband.x = Phaser.Math.Clamp(this.husband.x, MEET_X, END_X);
            this.wife.x = Phaser.Math.Clamp(this.wife.x, MEET_X + 54, END_X + 60);
            if (Math.abs(this.wife.x - this.husband.x) > 74) this.wife.x = Phaser.Math.Linear(this.wife.x, this.husband.x + 62, 0.06);
            this.followPoint.x = (this.husband.x + this.wife.x) / 2;
            this.followPoint.y = SHARED_FOLLOW_Y;
          }
          playAnim(player, moving) {
            player.anims.stop();
            player.setFrame(stageRows[player.owner][player.stage] * FRAMES_PER_STAGE);
          }
          updateStage(player, profile, year) {
            const next = this.state !== "split" && year >= 2025 ? "wedding" : profile.stageForYear(year);
            if (player.stage === next) return;
            const groundY = player.groundY || profile.groundY;
            player.stage = next;
            const row = stageRows[player.owner][next];
            player.setFrame(row * FRAMES_PER_STAGE);
            const wasGrounded = this.isLaneGrounded(player) || this.state !== "split";
            player.setScale(SCALE_BY_STAGE[next]);
            this.configurePlayerBody(player);
            if (wasGrounded) this.placeOnGround(player, groundY);
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
            if (!event || this.seen.has(event.id)) return;
            this.seen.add(event.id);
            const channel = this.state === "split" && event.owner !== "shared" ? event.owner : "shared";
            showStory(event, channel);
          }
          startMerge() {
            if (this.state !== "split") return;
            this.state = "merging";
            this.merge = 0;
            this.ready.husband = true;
            this.ready.wife = true;
            this.clearTouch();
            hideStory("husband");
            hideStory("wife");
            this.husband.setVelocity(0, 0);
            this.wife.setVelocity(0, 0);
            this.husband.setX(MEET_X - 38);
            this.wife.setX(MEET_X + 42);
            this.placeOnGround(this.husband, TOP_GROUND);
            this.placeOnGround(this.wife, BOTTOM_GROUND);
            this.mergeStart = {
              time: this.time.now,
              husbandX: this.husband.x,
              wifeX: this.wife.x,
              husbandGround: TOP_GROUND,
              wifeGround: BOTTOM_GROUND,
              cameraX: this.cameras.main.scrollX,
              cameraY: this.cameras.main.scrollY
            };
            this.wife.setAlpha(1);
            this.husband.setAlpha(1);
            this.playAnim(this.husband, false);
            this.playAnim(this.wife, false);
            this.husband.body.setAllowGravity(false);
            this.wife.body.setAllowGravity(false);
            this.cameras.main.stopFollow();
            this.wifeCam.stopFollow();
            this.fireEvent(TIMELINE.events.find((event) => event.id === "first-meeting"));
            this.music.fadeTo("climax");
          }
          updateMerge() {
            const start = this.mergeStart || {
              time: this.time.now,
              husbandX: MEET_X - 38,
              wifeX: MEET_X + 42,
              husbandGround: TOP_GROUND,
              wifeGround: BOTTOM_GROUND,
              cameraX: this.cameras.main.scrollX,
              cameraY: this.cameras.main.scrollY
            };
            this.merge = Phaser.Math.Clamp((this.time.now - start.time) / MERGE_DURATION, 0, 1);
            const eased = Phaser.Math.Easing.Sine.InOut(this.merge);
            const mainH = Phaser.Math.Linear(HALF_H, GAME_H, eased);
            const wifeH = Phaser.Math.Linear(HALF_H, 0, eased);
            this.cameras.main.setViewport(0, 0, GAME_W, mainH);
            this.wifeCam.setViewport(0, GAME_H - wifeH, GAME_W, Math.max(1, wifeH));
            this.wifeCam.setAlpha(1 - eased);
            this.husband.setX(Phaser.Math.Linear(start.husbandX, MEET_X + 16, eased));
            this.wife.setX(Phaser.Math.Linear(start.wifeX, MEET_X + 78, eased));
            this.placeOnGround(this.husband, TOP_GROUND);
            this.placeOnGround(this.wife, Phaser.Math.Linear(start.wifeGround, TOP_GROUND, eased));
            this.followPoint.x = (this.husband.x + this.wife.x) / 2;
            this.followPoint.y = SHARED_FOLLOW_Y;
            const targetX = MEET_X - GAME_W / 2;
            const targetY = SHARED_SCROLL_Y;
            this.cameras.main.scrollX = Phaser.Math.Linear(start.cameraX, targetX, eased);
            this.cameras.main.scrollY = Phaser.Math.Linear(start.cameraY, targetY, eased);
            if (this.merge >= 1) {
              this.state = "shared";
              this.cameras.remove(this.wifeCam);
              this.cameras.main.setViewport(0, 0, GAME_W, GAME_H);
              this.husband.setX(MEET_X + 16);
              this.wife.setX(MEET_X + 78);
              this.placeOnGround(this.husband, TOP_GROUND);
              this.placeOnGround(this.wife, TOP_GROUND);
              this.husband.setVelocity(0, 0);
              this.wife.setVelocity(0, 0);
              this.husband.body.setAllowGravity(true);
              this.wife.body.setAllowGravity(true);
              this.followPoint.x = (this.husband.x + this.wife.x) / 2;
              this.followPoint.y = SHARED_FOLLOW_Y;
              this.cameras.main.scrollY = SHARED_SCROLL_Y;
              this.cameras.main.startFollow(this.followPoint, true, 0.08, 0.08);
              this.sharedHoldUntil = this.time.now + 900;
            }
          }
          showEnding() {
            this.ending = true;
            this.fireEvent(TIMELINE.events.find((event) => event.id === "ending"));
            this.time.delayedCall(5000, () => {
              hideStory("shared");
              this.cameras.main.fadeOut(2600, 0, 0, 0);
            });
            this.time.delayedCall(7900, () => showEndingPhoto());
          }
        }

        window.__game = new Phaser.Game({
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
    "__BGM__": assets["bgm"],
    "__EVENTS__": json.dumps(events, ensure_ascii=False),
}

for key, value in replacements.items():
    html = html.replace(key, value)

(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"wrote index.html ({len(html.encode('utf-8')):,} bytes)")
