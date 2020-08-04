#!/bin/bash -e

SPEC="spec/files"

checkeq() {
  if res=$(diff "$1" "$2"); then
    echo "[✓]"
  else
    echo "[✗]"
    printf "%s\n" "$res"
    return 1
  fi
}

it() {
  printf "  it %s " "$*"
}

printf "pdfxmeta\n"

it "extracts metadata correctly"
checkeq <(pdfxmeta -p 1 "$SPEC/level2.pdf" "Section") \
        "$SPEC/level2_meta"

it "extracts metadata in auto mode correctly"
checkeq <(pdfxmeta -a 1 -p 1 "$SPEC/level2.pdf" "Section") \
        "$SPEC/level2_meta.toml"

printf "\npdftocgen\n"

it "generates toc for 2 level heading correctly"
checkeq <(pdftocgen "$SPEC/level2.pdf" < "$SPEC/level2_recipe.toml") \
        "$SPEC/level2.toc"

it "generates toc for one page headings correctly"
checkeq <(pdftocgen "$SPEC/onepage.pdf" < "$SPEC/onepage_greedy.toml") \
        "$SPEC/onepage.toc"

it "generates toc for hard mode correctly"
checkeq <(pdftocgen "$SPEC/hardmode.pdf" < "$SPEC/hardmode_recipe.toml") \
        "$SPEC/hardmode.toc"

it "generates readable toc"
checkeq <(pdftocgen -H "$SPEC/level2.pdf" < "$SPEC/level2_recipe.toml") \
        "$SPEC/level2_h.toc"

printf "\npdftocio\n"

tmpdir=$(mktemp -d)

it "adds toc to pdf and prints toc correctly"
checkeq <(pdftocgen "$SPEC/hardmode.pdf" < "$SPEC/hardmode_recipe.toml" | \
          pdftocio -o "$tmpdir/out.pdf" "$SPEC/hardmode.pdf" && \
          pdftocio -p "$tmpdir/out.pdf") \
        "$SPEC/hardmode.toc"

it "prints toc when -p is set"
checkeq <(pdftocio -p "$SPEC/hastoc.pdf" < $SPEC/level2.toc) \
        "$SPEC/hastoc.toc"
