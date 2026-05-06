const GAME_WIDTH = 960;
const GAME_HEIGHT = 540;
const HALF_HEIGHT = GAME_HEIGHT / 2;
const MEET_X = 3720;
const HUSBAND_START_X = 160;
const WIFE_START_X = 7280;
const END_X = 7040;
const TOP_GROUND_Y = 438;
const BOTTOM_GROUND_Y = 980;
const PLAYER_SCALE = 3;
const WALK_SPEED = 170;
const JUMP_SPEED = 445;
const GRAVITY_Y = 980;

const PROFILE = {
  husband: {
    label: "2P 권영호",
    birthYear: 1987,
    meetYear: 2020,
    startX: HUSBAND_START_X,
    meetX: MEET_X,
    direction: 1,
    groundY: TOP_GROUND_Y,
    color: {
      hair: "#25222a",
      skin: "#e2a77e",
      shirt: "#346fd1",
      pants: "#202735",
      accent: "#f2d166"
    }
  },
  wife: {
    label: "1P 방은지",
    birthYear: 1994,
    meetYear: 2020,
    startX: WIFE_START_X,
    meetX: MEET_X + 88,
    direction: -1,
    groundY: BOTTOM_GROUND_Y,
    color: {
      hair: "#33232f",
      skin: "#f0b88d",
      shirt: "#e35f8f",
      pants: "#273447",
      accent: "#fff0a6"
    }
  }
};

function clampYear(year) {
  return Math.max(1987, Math.min(2026, Math.round(year)));
}

function getLifeStage(profile, year) {
  const age = year - profile.birthYear;
  if (age < 4) return "baby";
  if (age < 15) return "child";
  return "adult";
}

function yearForPlayer(player, profile, merged) {
  if (merged) {
    const progress = Phaser.Math.Clamp((player.x - MEET_X) / (END_X - MEET_X), 0, 1);
    return clampYear(Phaser.Math.Linear(2020, 2026, progress));
  }

  const travel = Math.abs(profile.meetX - profile.startX);
  const moved = profile.direction === 1
    ? player.x - profile.startX
    : profile.startX - player.x;
  const progress = Phaser.Math.Clamp(moved / travel, 0, 1);
  return clampYear(Phaser.Math.Linear(profile.birthYear, profile.meetYear, progress));
}

function xForEvent(owner, year) {
  if (owner === "shared") {
    const progress = Phaser.Math.Clamp((year - 2020) / 6, 0, 1);
    return Phaser.Math.Linear(MEET_X, END_X, progress);
  }

  const profile = PROFILE[owner];
  const progress = Phaser.Math.Clamp((year - profile.birthYear) / (profile.meetYear - profile.birthYear), 0, 1);
  return profile.direction === 1
    ? Phaser.Math.Linear(profile.startX, profile.meetX, progress)
    : Phaser.Math.Linear(profile.startX, profile.meetX, progress);
}

function makePixelSheet(scene, key, colors, stage) {
  const frameWidth = 20;
  const frameHeight = 28;
  const frames = 4;
  const canvas = scene.textures.createCanvas(`${key}-canvas`, frameWidth * frames, frameHeight);
  const ctx = canvas.getContext();

  ctx.imageSmoothingEnabled = false;

  for (let frame = 0; frame < frames; frame += 1) {
    const ox = frame * frameWidth;
    const step = frame % 2 === 0 ? 0 : 1;
    const bodyTop = stage === "baby" ? 12 : 11;
    const headY = stage === "baby" ? 4 : 3;
    const bodyHeight = stage === "adult" ? 10 : 8;
    const legTop = bodyTop + bodyHeight;
    const headSize = stage === "baby" ? 9 : 8;

    ctx.fillStyle = "rgba(0, 0, 0, 0)";
    ctx.fillRect(ox, 0, frameWidth, frameHeight);

    ctx.fillStyle = "rgba(0, 0, 0, 0.28)";
    ctx.fillRect(ox + 5, 25, 11, 2);

    ctx.fillStyle = colors.hair;
    ctx.fillRect(ox + 6, headY, headSize, 4);
    ctx.fillRect(ox + 5, headY + 3, 2, 6);

    ctx.fillStyle = colors.skin;
    ctx.fillRect(ox + 7, headY + 4, headSize - 2, 7);
    ctx.fillRect(ox + 5, bodyTop + 2, 2, 5);
    ctx.fillRect(ox + 14, bodyTop + 2, 2, 5);

    ctx.fillStyle = "#272028";
    ctx.fillRect(ox + 9, headY + 7, 1, 1);
    ctx.fillRect(ox + 13, headY + 7, 1, 1);

    ctx.fillStyle = colors.shirt;
    ctx.fillRect(ox + 7, bodyTop, 7, bodyHeight);
    ctx.fillStyle = colors.accent;
    ctx.fillRect(ox + 10, bodyTop + 1, 2, 2);

    ctx.fillStyle = colors.pants;
    ctx.fillRect(ox + 7, legTop, 3, 6 + step);
    ctx.fillRect(ox + 11, legTop, 3, 7 - step);

    if (stage === "baby") {
      ctx.fillStyle = colors.accent;
      ctx.fillRect(ox + 6, 20, 9, 4);
    }

    if (stage === "child") {
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(ox + 13, bodyTop + 1, 2, 3);
    }

    if (stage === "adult") {
      ctx.fillStyle = "#f7f0d4";
      ctx.fillRect(ox + 8, bodyTop + bodyHeight - 2, 5, 1);
    }
  }

  canvas.refresh();
  scene.textures.addSpriteSheet(key, canvas.canvas, {
    frameWidth,
    frameHeight,
    endFrame: frames - 1
  });
}

function makePixelatedTexture(scene, sourceKey, targetKey, width, height, paletteSteps = 8) {
  const source = scene.textures.get(sourceKey).getSourceImage();
  const canvas = scene.textures.createCanvas(targetKey, width, height);
  const ctx = canvas.getContext();

  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(source, 0, 0, width, height);

  const image = ctx.getImageData(0, 0, width, height);
  const step = 255 / Math.max(2, paletteSteps - 1);
  for (let index = 0; index < image.data.length; index += 4) {
    image.data[index] = Math.round(image.data[index] / step) * step;
    image.data[index + 1] = Math.round(image.data[index + 1] / step) * step;
    image.data[index + 2] = Math.round(image.data[index + 2] / step) * step;
  }
  ctx.putImageData(image, 0, 0);
  canvas.refresh();
}

class BootScene extends Phaser.Scene {
  constructor() {
    super("BootScene");
  }

  preload() {
    this.load.json("timelineEvents", "assets/data/events.json");
    this.load.image("conceptRef", "assets/imgs/concept.jpg");
    this.load.image("weddingPhoto", "assets/imgs/wedding_pics/DSC00038.jpg");
  }

  create() {
    ["husband", "wife"].forEach((owner) => {
      ["baby", "child", "adult"].forEach((stage) => {
        makePixelSheet(this, `${owner}-${stage}`, PROFILE[owner].color, stage);
      });
    });

    const ground = this.textures.createCanvas("ground-tile", 64, 20);
    const ctx = ground.getContext();
    ctx.fillStyle = "#5e6f49";
    ctx.fillRect(0, 0, 64, 7);
    ctx.fillStyle = "#344232";
    ctx.fillRect(0, 7, 64, 13);
    ctx.fillStyle = "#82925a";
    for (let x = 0; x < 64; x += 8) ctx.fillRect(x, 2, 4, 2);
    ground.refresh();

    const sparkle = this.textures.createCanvas("sparkle", 8, 8);
    const sctx = sparkle.getContext();
    sctx.fillStyle = "#ffe188";
    sctx.fillRect(3, 0, 2, 8);
    sctx.fillRect(0, 3, 8, 2);
    sctx.fillStyle = "#ffffff";
    sctx.fillRect(3, 3, 2, 2);
    sparkle.refresh();

    makePixelatedTexture(this, "weddingPhoto", "wedding-pixel", 192, 128, 7);
    makePixelatedTexture(this, "conceptRef", "concept-pixel", 192, 128, 7);

    this.scene.start("TimelineScene");
  }
}

class TimelineMusic {
  constructor() {
    this.context = null;
    this.nodes = [];
    this.mode = "soft";
    this.started = false;
  }

  start() {
    if (this.started || !window.AudioContext) return;
    this.context = new window.AudioContext();
    this.started = true;
    this.setMode("soft");
  }

  setMode(mode) {
    this.mode = mode;
    if (!this.context) return;
    this.stop();

    const now = this.context.currentTime;
    const master = this.context.createGain();
    master.gain.setValueAtTime(0.0001, now);
    master.gain.exponentialRampToValueAtTime(mode === "climax" ? 0.07 : 0.035, now + 1.2);
    master.connect(this.context.destination);

    const freqs = mode === "climax" ? [261.63, 329.63, 392, 523.25] : [196, 246.94, 329.63];
    freqs.forEach((freq, index) => {
      const osc = this.context.createOscillator();
      const gain = this.context.createGain();
      osc.type = index % 2 === 0 ? "sine" : "triangle";
      osc.frequency.value = freq;
      gain.gain.value = 0.22 / freqs.length;
      osc.connect(gain);
      gain.connect(master);
      osc.start(now + index * 0.04);
      this.nodes.push(osc, gain);
    });
    this.nodes.push(master);
  }

  stop() {
    this.nodes.forEach((node) => {
      if (typeof node.stop === "function") {
        try {
          node.stop();
        } catch (error) {
          // Oscillators can only be stopped once.
        }
      }
      if (typeof node.disconnect === "function") {
        try {
          node.disconnect();
        } catch (error) {
          // Already disconnected.
        }
      }
    });
    this.nodes = [];
  }
}

class TimelineScene extends Phaser.Scene {
  constructor() {
    super("TimelineScene");
  }

  create() {
    this.state = "split";
    this.mergeProgress = 0;
    this.seenEvents = new Set();
    this.eventsData = this.cache.json.get("timelineEvents").events;
    this.music = new TimelineMusic();

    this.physics.world.setBounds(0, 0, WIFE_START_X + 480, 1180);
    this.createWorld();
    this.createPlayers();
    this.createControls();
    this.createCameras();
    this.createHud();
    this.createEventMarkers();
    this.createParticles();

    this.input.keyboard.once("keydown", () => this.music.start());
    this.input.once("pointerdown", () => this.music.start());
  }

  createWorld() {
    this.add.rectangle((WIFE_START_X + 480) / 2, 215, WIFE_START_X + 480, 430, 0x8fb8d9);
    this.add.rectangle((WIFE_START_X + 480) / 2, 757, WIFE_START_X + 480, 430, 0xd7a7b3);
    this.add.rectangle((WIFE_START_X + 480) / 2, 464, WIFE_START_X + 480, 44, 0x15171b);

    this.drawSkyline(0, TOP_GROUND_Y - 220, 0x486985, 0x30455c);
    this.drawSkyline(0, BOTTOM_GROUND_Y - 220, 0x7e5d7c, 0x51415f);
    this.drawSharedRoad();
    this.addPhotoLandmarks();

    this.platforms = this.physics.add.staticGroup();
    this.addGround(TOP_GROUND_Y);
    this.addGround(BOTTOM_GROUND_Y);
  }

  drawSkyline(offsetX, baseY, nearColor, farColor) {
    for (let x = offsetX; x < WIFE_START_X + 480; x += 240) {
      const farHeight = 60 + ((x / 240) % 4) * 14;
      this.add.rectangle(x + 90, baseY + 100 - farHeight / 2, 130, farHeight, farColor).setAlpha(0.62);
      const nearHeight = 88 + ((x / 120) % 5) * 10;
      this.add.rectangle(x + 182, baseY + 128 - nearHeight / 2, 80, nearHeight, nearColor).setAlpha(0.82);
    }
  }

  drawSharedRoad() {
    for (let x = MEET_X; x <= END_X + 200; x += 96) {
      this.add.rectangle(x, TOP_GROUND_Y - 24, 52, 4, 0xf5e9b7).setAlpha(0.75);
    }
  }

  addPhotoLandmarks() {
    const concept = this.add.image(820, TOP_GROUND_Y - 155, "concept-pixel")
      .setDisplaySize(192, 128)
      .setDepth(3)
      .setAlpha(0.82);
    concept.setCrop(96, 0, 96, 128);
    this.add.rectangle(820, TOP_GROUND_Y - 155, 204, 140, 0x211f24, 0)
      .setStrokeStyle(3, 0xf7e7b4)
      .setDepth(4);

    const weddingX = xForEvent("shared", 2025);
    this.add.rectangle(weddingX, TOP_GROUND_Y - 160, 246, 176, 0x211f24, 0.84)
      .setStrokeStyle(4, 0xffdf7d)
      .setDepth(4);
    this.add.image(weddingX, TOP_GROUND_Y - 170, "wedding-pixel")
      .setDisplaySize(216, 144)
      .setDepth(5);
    this.add.text(weddingX - 101, TOP_GROUND_Y - 76, "2025.02.08", {
      fontFamily: "monospace",
      fontSize: "14px",
      color: "#ffe188"
    }).setDepth(6);
  }

  addGround(y) {
    for (let x = 32; x < WIFE_START_X + 480; x += 64) {
      const tile = this.add.tileSprite(x, y + 10, 64, 20, "ground-tile");
      this.physics.add.existing(tile, true);
      this.platforms.add(tile);
    }
  }

  createPlayers() {
    this.husband = this.createPlayer("husband", HUSBAND_START_X, TOP_GROUND_Y - 55);
    this.wife = this.createPlayer("wife", WIFE_START_X, BOTTOM_GROUND_Y - 55);
    this.wife.setFlipX(true);

    this.physics.add.collider(this.husband, this.platforms);
    this.physics.add.collider(this.wife, this.platforms);

    ["husband", "wife"].forEach((owner) => {
      ["baby", "child", "adult"].forEach((stage) => {
        const texture = `${owner}-${stage}`;
        this.anims.create({
          key: `${texture}-walk`,
          frames: this.anims.generateFrameNumbers(texture, { start: 0, end: 3 }),
          frameRate: 7,
          repeat: -1
        });
      });
    });

    this.followPoint = { x: MEET_X, y: TOP_GROUND_Y - 90 };
  }

  createPlayer(owner, x, y) {
    const sprite = this.physics.add.sprite(x, y, `${owner}-baby`, 0)
      .setScale(PLAYER_SCALE)
      .setDepth(20)
      .setCollideWorldBounds(true);

    sprite.owner = owner;
    sprite.body.setSize(13, 23);
    sprite.body.setOffset(3, 5);
    return sprite;
  }

  createControls() {
    this.keys = this.input.keyboard.addKeys({
      husbandLeft: Phaser.Input.Keyboard.KeyCodes.A,
      husbandRight: Phaser.Input.Keyboard.KeyCodes.D,
      husbandJump: Phaser.Input.Keyboard.KeyCodes.W,
      wifeLeft: Phaser.Input.Keyboard.KeyCodes.LEFT,
      wifeRight: Phaser.Input.Keyboard.KeyCodes.RIGHT,
      wifeJump: Phaser.Input.Keyboard.KeyCodes.UP,
      restart: Phaser.Input.Keyboard.KeyCodes.R
    });
  }

  createCameras() {
    const main = this.cameras.main;
    main.setViewport(0, 0, GAME_WIDTH, HALF_HEIGHT);
    main.setBounds(0, 0, WIFE_START_X + 480, 1180);
    main.startFollow(this.husband, true, 0.08, 0.08);
    main.setZoom(1);

    this.wifeCam = this.cameras.add(0, HALF_HEIGHT, GAME_WIDTH, HALF_HEIGHT);
    this.wifeCam.setBounds(0, 0, WIFE_START_X + 480, 1180);
    this.wifeCam.startFollow(this.wife, true, 0.08, 0.08);
  }

  createHud() {
    this.husbandHud = this.add.text(0, 0, "", {
      fontFamily: "monospace",
      fontSize: "18px",
      color: "#fff4d1",
      backgroundColor: "rgba(21, 23, 27, 0.72)",
      padding: { x: 10, y: 6 }
    }).setDepth(100);

    this.wifeHud = this.add.text(0, 0, "", {
      fontFamily: "monospace",
      fontSize: "18px",
      color: "#fff4d1",
      backgroundColor: "rgba(21, 23, 27, 0.72)",
      padding: { x: 10, y: 6 }
    }).setDepth(100);

    this.centerText = this.add.text(MEET_X, TOP_GROUND_Y - 180, "", {
      fontFamily: "monospace",
      fontSize: "22px",
      color: "#ffffff",
      align: "center",
      backgroundColor: "rgba(21, 23, 27, 0.8)",
      padding: { x: 14, y: 10 },
      wordWrap: { width: 500 }
    }).setOrigin(0.5).setDepth(120).setAlpha(0);
  }

  createEventMarkers() {
    this.eventsData.forEach((event) => {
      const x = xForEvent(event.owner, event.year);
      const y = event.owner === "wife" ? BOTTOM_GROUND_Y - 50 : TOP_GROUND_Y - 50;
      const color = event.owner === "shared" ? 0xffdf7d : event.owner === "wife" ? 0xf09ab5 : 0x6fa5ef;
      this.add.rectangle(x, y, 8, 58, color).setDepth(6);
      this.add.triangle(x + 16, y - 22, 0, 0, 34, 12, 0, 24, color).setDepth(7);
      this.add.text(x - 34, y - 65, String(event.year), {
        fontFamily: "monospace",
        fontSize: "13px",
        color: "#211f24",
        backgroundColor: "#f7e7b4",
        padding: { x: 5, y: 3 }
      }).setDepth(8);
    });
  }

  createParticles() {
    this.sparkles = this.add.particles(0, 0, "sparkle", {
      lifespan: 650,
      speed: { min: 35, max: 95 },
      angle: { min: 220, max: 320 },
      gravityY: 180,
      scale: { start: 1.3, end: 0 },
      emitting: false
    }).setDepth(90);
  }

  update() {
    if (Phaser.Input.Keyboard.JustDown(this.keys.restart)) {
      this.scene.restart();
      return;
    }

    const husbandYear = yearForPlayer(this.husband, PROFILE.husband, this.state !== "split");
    const wifeYear = yearForPlayer(this.wife, PROFILE.wife, this.state !== "split");

    this.updateCharacterStage(this.husband, PROFILE.husband, husbandYear);
    this.updateCharacterStage(this.wife, PROFILE.wife, wifeYear);

    if (this.state === "split") {
      this.updateSplitMovement();
      this.updateSplitHud(husbandYear, wifeYear);
      this.checkPreMeetEvents(husbandYear, wifeYear);
      this.checkMeeting();
      return;
    }

    if (this.state === "merging") {
      this.updateMerging();
    } else {
      this.updateSharedMovement();
    }

    const sharedYear = yearForPlayer(this.husband, PROFILE.husband, true);
    this.updateSharedHud(sharedYear);
    this.checkSharedEvents(sharedYear);
    this.checkEnding(sharedYear);
  }

  updateSplitMovement() {
    this.movePlayer(this.husband, this.keys.husbandLeft.isDown, this.keys.husbandRight.isDown, this.keys.husbandJump, 1);
    this.movePlayer(this.wife, this.keys.wifeLeft.isDown, this.keys.wifeRight.isDown, this.keys.wifeJump, -1);

    this.husband.x = Math.min(this.husband.x, PROFILE.husband.meetX);
    this.wife.x = Math.max(this.wife.x, PROFILE.wife.meetX);
  }

  updateSharedMovement() {
    const left = this.keys.husbandLeft.isDown || this.keys.wifeLeft.isDown;
    const right = this.keys.husbandRight.isDown || this.keys.wifeRight.isDown;
    const jumpPressed = Phaser.Input.Keyboard.JustDown(this.keys.husbandJump)
      || Phaser.Input.Keyboard.JustDown(this.keys.wifeJump);

    const speed = right ? WALK_SPEED : left ? -WALK_SPEED * 0.45 : 38;
    [this.husband, this.wife].forEach((player, index) => {
      player.setVelocityX(speed);
      player.setFlipX(speed < 0);
      if (jumpPressed && player.body.blocked.down) player.setVelocityY(-JUMP_SPEED);
      this.playWalkAnimation(player, Math.abs(speed) > 5);
      if (index === 1 && Math.abs(this.wife.x - this.husband.x) > 74) {
        this.wife.x = Phaser.Math.Linear(this.wife.x, this.husband.x + 58, 0.04);
      }
    });

    this.husband.x = Phaser.Math.Clamp(this.husband.x, MEET_X, END_X + 80);
    this.wife.x = Phaser.Math.Clamp(this.wife.x, MEET_X + 50, END_X + 140);
    this.followPoint.x = (this.husband.x + this.wife.x) / 2;
    this.followPoint.y = TOP_GROUND_Y - 102;
  }

  movePlayer(player, leftDown, rightDown, jumpKey, facingDirection) {
    if (leftDown) {
      player.setVelocityX(-WALK_SPEED);
      player.setFlipX(true);
    } else if (rightDown) {
      player.setVelocityX(WALK_SPEED);
      player.setFlipX(false);
    } else {
      player.setVelocityX(0);
    }

    if (Phaser.Input.Keyboard.JustDown(jumpKey) && player.body.blocked.down) {
      player.setVelocityY(-JUMP_SPEED);
    }

    if (facingDirection === -1 && !leftDown && !rightDown) player.setFlipX(true);
    this.playWalkAnimation(player, Math.abs(player.body.velocity.x) > 5);
  }

  playWalkAnimation(player, moving) {
    const texture = player.texture.key;
    if (moving && player.body.blocked.down) {
      player.anims.play(`${texture}-walk`, true);
    } else {
      player.anims.stop();
      player.setFrame(0);
    }
  }

  updateCharacterStage(player, profile, year) {
    const stage = getLifeStage(profile, year);
    const texture = `${player.owner}-${stage}`;
    if (player.texture.key !== texture) {
      const frame = player.frame.name || 0;
      player.setTexture(texture, Number(frame) || 0);
    }
  }

  updateSplitHud(husbandYear, wifeYear) {
    this.husbandHud.setText(`${PROFILE.husband.label}  ${husbandYear}`);
    this.wifeHud.setText(`${PROFILE.wife.label}  ${wifeYear}`);
    this.husbandHud.setPosition(this.cameras.main.scrollX + 16, this.cameras.main.scrollY + 14);
    this.wifeHud.setPosition(this.wifeCam.scrollX + 16, this.wifeCam.scrollY + 14);
  }

  updateSharedHud(year) {
    this.husbandHud.setText(`함께 걷는 시간  ${year}`);
    this.husbandHud.setPosition(this.cameras.main.scrollX + 16, this.cameras.main.scrollY + 14);
    this.wifeHud.setText("");
  }

  checkPreMeetEvents(husbandYear, wifeYear) {
    this.eventsData.forEach((event) => {
      if (event.owner === "husband" && husbandYear >= event.year) this.triggerEvent(event, this.husband);
      if (event.owner === "wife" && wifeYear >= event.year) this.triggerEvent(event, this.wife);
    });
  }

  checkSharedEvents(sharedYear) {
    this.eventsData.forEach((event) => {
      if (event.owner === "shared" && sharedYear >= event.year) {
        this.triggerEvent(event, this.husband, true);
      }
    });
  }

  triggerEvent(event, player, centered = false) {
    if (this.seenEvents.has(event.id)) return;
    this.seenEvents.add(event.id);

    const x = centered ? (this.husband.x + this.wife.x) / 2 : player.x;
    const y = centered ? TOP_GROUND_Y - 175 : player.y - 125;
    this.sparkles.emitParticleAt(x, y + 30, 18);
    this.showBubble(x, y, event);
  }

  showBubble(x, y, event) {
    const bubble = this.add.container(x, y).setDepth(130);
    const width = 420;
    const panel = this.add.rectangle(0, 0, width, 94, 0x211f24, 0.9)
      .setStrokeStyle(3, 0xf7e7b4);
    const title = this.add.text(-width / 2 + 18, -34, `${event.year}  ${event.title}`, {
      fontFamily: "monospace",
      fontSize: "17px",
      color: "#ffe188"
    });
    const body = this.add.text(-width / 2 + 18, -7, event.text, {
      fontFamily: "monospace",
      fontSize: "15px",
      color: "#f7f0d4",
      wordWrap: { width: width - 36 }
    });
    bubble.add([panel, title, body]);
    bubble.setScale(0.92);
    bubble.setAlpha(0);

    this.tweens.add({
      targets: bubble,
      y: y - 14,
      alpha: 1,
      scale: 1,
      duration: 240,
      ease: "Cubic.Out",
      yoyo: true,
      hold: 2700,
      onComplete: () => bubble.destroy()
    });
  }

  checkMeeting() {
    const husbandReady = this.husband.x >= PROFILE.husband.meetX - 4;
    const wifeReady = this.wife.x <= PROFILE.wife.meetX + 4;
    if (!husbandReady || !wifeReady) return;

    this.state = "merging";
    this.husband.setVelocity(0, 0);
    this.wife.setVelocity(0, 0);
    this.husband.setPosition(MEET_X - 38, TOP_GROUND_Y - 55);
    this.wife.setPosition(MEET_X + 38, BOTTOM_GROUND_Y - 55);
    this.husband.body.setAllowGravity(false);
    this.wife.body.setAllowGravity(false);
    this.cameras.main.stopFollow();
    this.wifeCam.stopFollow();
    this.triggerEvent(this.eventsData.find((event) => event.id === "first-meeting"), this.husband, true);
    this.music.setMode("climax");

    this.tweens.add({
      targets: this.wife,
      y: TOP_GROUND_Y - 55,
      duration: 1500,
      ease: "Sine.InOut"
    });
  }

  updateMerging() {
    this.mergeProgress = Phaser.Math.Linear(this.mergeProgress, 1, 0.035);
    const mainHeight = Phaser.Math.Linear(HALF_HEIGHT, GAME_HEIGHT, this.mergeProgress);
    const wifeHeight = Phaser.Math.Linear(HALF_HEIGHT, 0, this.mergeProgress);
    this.cameras.main.setViewport(0, 0, GAME_WIDTH, mainHeight);
    this.wifeCam.setViewport(0, GAME_HEIGHT - wifeHeight, GAME_WIDTH, Math.max(1, wifeHeight));
    this.wifeCam.setAlpha(1 - this.mergeProgress);

    const targetX = (this.husband.x + this.wife.x) / 2;
    const targetY = TOP_GROUND_Y - 105;
    this.cameras.main.scrollX = Phaser.Math.Linear(this.cameras.main.scrollX, targetX - GAME_WIDTH / 2, 0.04);
    this.cameras.main.scrollY = Phaser.Math.Linear(this.cameras.main.scrollY, targetY - GAME_HEIGHT / 2, 0.04);

    if (this.mergeProgress > 0.985) {
      this.state = "shared";
      this.cameras.remove(this.wifeCam);
      this.cameras.main.setViewport(0, 0, GAME_WIDTH, GAME_HEIGHT);
      this.cameras.main.startFollow(this.followPoint, true, 0.08, 0.08);
      this.husband.body.setAllowGravity(true);
      this.wife.body.setAllowGravity(true);
      this.wife.setY(TOP_GROUND_Y - 55);
      this.husband.setX(MEET_X + 16);
      this.wife.setX(MEET_X + 74);
      this.husband.setFlipX(false);
      this.wife.setFlipX(false);
    }
  }

  checkEnding(sharedYear) {
    if (sharedYear < 2026 || this.endingStarted) return;
    this.endingStarted = true;
    this.centerText.setText("권영호  +  방은지\n함께 이어갈 모든 내일");
    this.centerText.setPosition(this.cameras.main.scrollX + GAME_WIDTH / 2, this.cameras.main.scrollY + 160);
    this.tweens.add({
      targets: this.centerText,
      alpha: 1,
      duration: 700,
      ease: "Sine.Out"
    });
    this.time.delayedCall(3200, () => {
      this.cameras.main.fadeOut(2600, 21, 23, 27);
    });
  }
}

const config = {
  type: Phaser.AUTO,
  parent: "game",
  width: GAME_WIDTH,
  height: GAME_HEIGHT,
  backgroundColor: "#15171b",
  pixelArt: true,
  roundPixels: true,
  physics: {
    default: "arcade",
    arcade: {
      gravity: { y: GRAVITY_Y },
      debug: false
    }
  },
  scene: [BootScene, TimelineScene],
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
};

new Phaser.Game(config);
