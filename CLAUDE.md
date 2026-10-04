# agae_diy 링크 페이지

인스타그램 agae_diy 프로필에 거는 링크 페이지. 아개식권 도안(미리캔버스) 사용법, 블로그, 유튜브, 협업 DM으로 연결한다.

## 스택
- 정적 HTML + CSS. 빌드 과정, 패키지, 프레임워크 없음. JS 없음.
- 호스팅: Cloudflare Pages (GitHub 저장소 연결, main에 push하면 자동 배포)
- 주소: https://agae-diy.pages.dev
- 분석: Cloudflare Web Analytics (Pages 설정에서 켬, 코드에 스크립트를 직접 넣지 않음)

## 파일 구조
배포되는 것은 `public/` 폴더뿐이다 (Cloudflare Pages 빌드 출력 디렉터리 = `public`). 문서와 도구는 공개되지 않는다.
```
CLAUDE.md, tasks.md   이 저장소 설명, 작업 목록
tools/subset-fonts.py 폰트 서브셋 다시 만드는 스크립트
public/
  index.html          링크 페이지
  404.html            없는 주소로 들어왔을 때 (Cloudflare Pages가 자동으로 사용)
  styles.css          모든 스타일. 맨 위 :root에 디자인 토큰
  _headers            보안 헤더, 캐시 설정 (Cloudflare Pages 전용)
  robots.txt, sitemap.xml
  favicon.ico, favicon-32.png, apple-touch-icon.png
  fonts/              Pretendard 서브셋 (페이지에 쓰는 글자만, 각 31KB)
  images/             로고, 식권 사진, 사용법 캡처 5장, 공유 이미지(og.jpg)
```

## 로컬에서 보기
`public` 폴더에서 `python -m http.server 8000` 실행 후 http://localhost:8000 (경로가 `/`로 시작해서 파일을 더블클릭하면 스타일이 안 보인다)

## 규칙
- 색, 글자 크기, 간격은 styles.css의 토큰(`--color-*`, `--space-*`, `--font-*`)만 쓴다. 값을 직접 쓰지 않는다.
- 시맨틱 태그 사용: header, main, section, footer. 버튼 역할 링크는 `<a>`, 접기는 `<details>`.
- 외부 링크는 `target="_blank" rel="noopener"`.
- 이미지는 WebP, `width`/`height`와 `alt`를 반드시 적는다. 첫 화면 아래 이미지는 `loading="lazy"`.
- 문구를 바꾸면 폰트 서브셋을 다시 만든다: `python3 tools/subset-fonts.py` (새 글자가 기기 기본 고딕으로 보이는 것을 막기 위해).
- 주소(agae-diy.pages.dev)를 바꾸면 index.html의 canonical·og 태그, 공지 문구, robots.txt, sitemap.xml을 함께 고친다.
- `_headers`의 CSP 때문에 인라인 style 속성과 인라인 script는 동작하지 않는다. 스타일은 styles.css에만 쓴다.

## 금지
- 외부 CDN, 외부 폰트, 외부 스크립트를 추가하지 않는다. (Cloudflare가 넣는 분석 스크립트만 예외)
- 폼, 쿠키, 개인정보 수집 기능을 추가하지 않는다.
- 기획에 없는 기능을 추가하지 않는다.
- 비밀키, 토큰을 코드에 넣지 않는다. (이 사이트는 필요한 비밀키가 없다)

## 문서 위치 (claude.ai 프로젝트 "웹사이트만들기")
- PRD.md: 기능, 화면설계, 예외 상황
- design-system.md: 컬러, 폰트, 간격, 컴포넌트
- content-list.md: 확정 문구, 대체텍스트, 메타데이터
- tone-guide.md: 말투
- asset-license.md: 폰트·이미지 출처
- PROGRESS.md: 진행 현황, 결정 기록

## 운영 원칙
- 유지보수 없이 둔다. 미리캔버스 요소(검색어 agae, 유료 여부)나 링크가 바뀌면 이 페이지도 같이 고친다.
- 되돌리기: Cloudflare Pages > 프로젝트 > Deployments에서 이전 배포의 "Rollback", 또는 `git revert` 후 push.
