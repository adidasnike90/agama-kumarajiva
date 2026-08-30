.PHONY: align align-full metadata translate-corpus gold gold11 gold31 web sync-web book-export book publication-audit publication-fix

align:
	python scripts/run.py align --count 10

align-full:
	python scripts/align_corpus.py --start 51 --end 1362 --batch 50

metadata:
	python scripts/build_sc_metadata.py

translate-corpus:
	python scripts/translate_corpus.py --start 51 --end 1362

gold:
	python scripts/apply_gold_sa1_10.py

gold11:
	python scripts/apply_gold_sa11_30.py

gold31:
	python scripts/apply_gold_sa31_50.py

web:
	cd web && npm run dev -- --host 127.0.0.1 --port 5173

sync-web:
	python scripts/sync_web_corpus.py

book-export:
	python scripts/export_book_latex.py

book: book-export
	mkdir -p book/build
	cd book && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex

publication-audit:
	python scripts/publication_corpus.py audit
	python scripts/audit_gold_corpus.py

publication-fix:
	python scripts/publication_corpus.py fix --apply
	python scripts/publication_corpus.py audit
