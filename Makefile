.PHONY: align align-full metadata translate-corpus gold gold11 gold31 web sync-web sync-web-pdfs book-export book book-v2-export book-v2 publication-audit publication-fix v2-order

align:
	python scripts/run.py align --count 10

align-full:
	python scripts/align_corpus.py --start 51 --end 1362 --batch 50

metadata:
	python scripts/build_sc_metadata.py

v2-order:
	python scripts/build_v2_academic_order.py

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
	python scripts/sync_web_v2_order.py
	-python scripts/sync_web_pdfs.py

sync-web-pdfs:
	python scripts/sync_web_pdfs.py

book-export:
	python scripts/export_book_latex.py

book: book-export
	mkdir -p book/build
	cd book && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex
	cd book && xelatex -interaction=nonstopmode -output-directory=build sample_juan01.tex

book-v2-export: v2-order
	python scripts/export_book_v2_latex.py

book-v2: book-v2-export
	mkdir -p book_v2/build
	cd book_v2 && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book_v2 && xelatex -interaction=nonstopmode -output-directory=build main.tex
	cd book_v2 && xelatex -interaction=nonstopmode -output-directory=build main.tex

publication-audit:
	python scripts/publication_corpus.py audit
	python scripts/audit_gold_corpus.py

publication-fix:
	python scripts/publication_corpus.py fix --apply
	python scripts/publication_corpus.py audit
