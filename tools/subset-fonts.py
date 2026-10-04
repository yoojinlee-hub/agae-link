"""Pretendard 폰트를 페이지에 쓰는 글자만 남겨 작게 만든다.

문구를 바꾼 뒤에 한 번 실행한다. 새 글자가 빠지면 그 글자만 기기 기본 고딕으로 보인다.

필요한 것: Python 3, `pip install fonttools brotli`
실행: python3 tools/subset-fonts.py
  - 처음 실행하면 npm 저장소에서 Pretendard 원본(1.3.9)을 tools/.cache 에 내려받는다.
  - 결과: public/fonts/pretendard-400.woff2, pretendard-700.woff2
"""
import io
import re
import tarfile
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from fontTools import subset

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
CACHE = Path(__file__).resolve().parent / ".cache"
VERSION = "1.3.9"
TARBALL = f"https://registry.npmjs.org/pretendard/-/pretendard-{VERSION}.tgz"
WEIGHTS = {"400": "Pretendard-Regular.woff2", "700": "Pretendard-Bold.woff2"}


class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks = []

    def handle_data(self, data):
        self.chunks.append(data)

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("alt", "aria-label", "title", "content") and value:
                self.chunks.append(value)


def page_text() -> str:
    collector = TextCollector()
    for html in PUBLIC.glob("*.html"):
        collector.feed(html.read_text(encoding="utf-8"))
    text = "".join(collector.chunks)
    # 영문·숫자·기본 기호는 항상 넣는다 (문구를 조금 바꿔도 깨지지 않게)
    ascii_basic = "".join(chr(c) for c in range(0x20, 0x7F))
    extras = "·©…‘’“”–—→↗"
    return "".join(sorted(set(re.sub(r"\s", "", text) + ascii_basic + extras + " ")))


def source_font(filename: str) -> Path:
    path = CACHE / filename
    if path.exists():
        return path
    CACHE.mkdir(parents=True, exist_ok=True)
    print(f"원본 폰트 내려받는 중: {TARBALL}")
    data = urllib.request.urlopen(TARBALL).read()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for name in WEIGHTS.values():
            member = tar.getmember(f"package/dist/web/static/woff2/{name}")
            (CACHE / name).write_bytes(tar.extractfile(member).read())
    return path


def main():
    text = page_text()
    print(f"글자 수: {len(text)}")
    out_dir = PUBLIC / "fonts"
    out_dir.mkdir(parents=True, exist_ok=True)
    for weight, filename in WEIGHTS.items():
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]
        options.name_IDs = ["*"]
        options.name_languages = ["*"]
        options.notdef_outline = True
        font = subset.load_font(str(source_font(filename)), options)
        subsetter = subset.Subsetter(options)
        subsetter.populate(text=text)
        subsetter.subset(font)
        out = out_dir / f"pretendard-{weight}.woff2"
        subset.save_font(font, str(out), options)
        print(f"{out.relative_to(ROOT)}: {out.stat().st_size / 1024:.1f}KB")


if __name__ == "__main__":
    main()
