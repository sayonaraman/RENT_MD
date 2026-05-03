#!/bin/zsh
# Двойной клик из Finder: добавить в тему только новые объявления
# (тему не чистит, seen.json и filtered_ids.json сохраняются).
cd "$(dirname "$0")"
./.venv/bin/python -u scan_rentals.py
echo
echo "=== Готово. Закрой окно или нажми Enter ==="
read
