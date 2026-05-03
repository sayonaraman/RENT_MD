#!/bin/zsh
# Двойной клик из Finder:
#   1. чистит тему 17 в целевой группе
#   2. обнуляет seen.json (filtered_ids.json сохраняется)
#   3. запускает свежий сбор за последние 5 дней по фильтрам
cd "$(dirname "$0")"
./.venv/bin/python -u scan_rentals.py --reset
echo
echo "=== Готово. Закрой окно или нажми Enter ==="
read
