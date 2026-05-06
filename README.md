# Our Timeline

Phaser 3 CDN을 사용하는 GitHub Pages용 단일 `index.html` 게임입니다. 게임 로직, 스타일, 이미지, BGM이 모두 [index.html](index.html)에 data URI로 들어 있습니다.

## 실행

```bash
python3 -m http.server 4173
```

브라우저에서 `http://127.0.0.1:4173`을 엽니다.

## 배포

GitHub 저장소 루트에 [index.html](index.html) 하나를 올린 뒤 Pages source를 `main` 브랜치의 root로 설정하면 됩니다. Phaser 3만 CDN에서 불러오고, 나머지 게임 에셋은 HTML 내부에 포함되어 있습니다.

필수 배포 파일:

- [index.html](index.html)

## 조작

- PC: 권영호 `A` / `D`, 점프 `W`; 방은지 방향키 좌/우, 점프 방향키 위
- 모바일: 화면 좌/우 영역 터치로 이동, 화면 위쪽 터치로 점프
- 합쳐진 뒤에는 화면 좌/우 터치 또는 어느 쪽 이동키로도 함께 이동
- `R`로 재시작

## 적용 내용

- 아기, 학생, 성인 3단계 캐릭터 스프라이트시트
- 연도별 배경 전환: 유년기, 학교, 캠퍼스, 회사, 만남/결혼 숲길
- 기본 BGM과 만남 이후 클라이막스 BGM을 로컬 합성 WAV로 생성해 HTML에 포함
- 이벤트 문구는 화면 고정 HTML 패널로 표시해 점프와 모바일 화면에서 잘리지 않도록 처리
