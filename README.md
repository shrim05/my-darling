# Our Timeline

Phaser 3 CDN을 사용하는 GitHub Pages용 단일 `index.html` 게임입니다. 게임 로직, 스타일, 이미지, BGM이 모두 [index.html](index.html)에 data URI로 들어 있습니다.

## 실행

```bash
npm run package:static
npm run serve:static
```

브라우저에서 `http://127.0.0.1:4175`를 엽니다.

## 정적 배포

아래 명령으로 최신 단일 HTML을 생성합니다.

```bash
npm run package:static
```

생성물은 [dist/index.html](dist/index.html)과 링크 공유 썸네일용 [dist/assets/generated/cover.png](dist/assets/generated/cover.png)입니다. GitHub Pages에는 이 두 파일을 같은 경로로 올리면 됩니다.

Phaser 3만 CDN에서 불러오고, 나머지 게임 에셋은 HTML 내부에 포함되어 있습니다.

필수 배포 파일:

- [dist/index.html](dist/index.html)
- [dist/assets/generated/cover.png](dist/assets/generated/cover.png)

카카오톡 같은 링크 미리보기는 `cover.png`를 Open Graph 이미지로 사용합니다. 기본 Pages 주소는 `https://shrim05.github.io/my-darling/`로 잡혀 있습니다. 다른 주소나 커스텀 도메인으로 배포한다면 아래처럼 다시 패키징하세요.

```bash
PUBLIC_URL=https://example.com/my-darling/ npm run package:static
```

## 조작

- PC: 권영호 `A` / `D`, 점프 `W`; 방은지 방향키 좌/우, 점프 방향키 위
- 모바일: 화면 좌/우 영역 터치로 이동, 화면 위쪽 터치로 점프
- 합쳐진 뒤에는 화면 좌/우 터치 또는 어느 쪽 이동키로도 함께 이동
- `R`로 재시작

## 적용 내용

- 아기, 학생, 성인 3단계 캐릭터 스프라이트와 2025년 이후 신랑/신부 복장 전환
- 캐릭터는 현재 1프레임 고정 표시로 적용하며, 걷기 이미지는 나중에 교체할 수 있도록 스프라이트시트 구조를 유지
- 캐릭터 발 위치를 충돌 박스 기준으로 보정해 시작/합류/성장 전환 때 아래로 떨어지는 현상을 줄임
- 연도별 배경 전환: 유년기, 학교, 캠퍼스, 회사, 만남/결혼 숲길
- `The_Amber_Path.mp4` BGM을 data URI로 HTML에 포함
- 이벤트 문구는 화면 고정 HTML 패널로 표시해 점프와 모바일 화면에서 잘리지 않도록 처리
- `artifacts/live-smoke.spec.js`와 `scripts/live_test.py`로 데스크톱/모바일/태블릿 smoke 테스트 가능

## 검증

```bash
npm run package:static
npm run serve:static
TEST_URL=http://127.0.0.1:4175/ npx playwright test artifacts/live-smoke.spec.js
TEST_URL=http://127.0.0.1:4175/ python3 scripts/live_test.py
```
