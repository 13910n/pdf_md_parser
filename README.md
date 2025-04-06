Выводы на данный момент:
- Лучший результат по таблицам: простой pdfplumber с настройкой (иногда таблицу сводит к списку, тогда можно попробовать camelot, он стабильнее, но результаты хуже, чем у сработавшего pdfplubmer)
- Лучший результат по тексту: оценить hybrib вариант против fitz
- Ни один вариант не вышел за 1 гигабайт RAM

Проверить:
- Tesseract + OpenCV для получения таблиц
- Прогнать все вариации настроек pdfplumber для нахождения лучшей композиции
- Найти способ вырезать табличный текст, который собраз fitz, если он будет выбран для текста

Summary по методам таблиц:
- hybrid в данном виде неприменим, часто дробит таблицы
- pdfplumber приоритетен, потому что когда срабатывает, выдаёт хорошие варианты (120kb, 195kb, 215kb, 494kb), плохо работает со вложенными, так как необходимо вырезать None значения (иначе будут сломанные таблицы со множеством пустых ячеек (возможно, подойдёт вариант постобработки таблиц с удалением полупустых колонок))
- camelot хорошо тогда, когда pdfplumber не сработал, так как выдаёт результат стабильнее, но хуже

## Statistics Module

The project includes a statistics module for benchmarking different PDF-to-Markdown conversion implementations:

- `statistics.py`: Runs all PDF-to-Markdown converters and measures:
  - Memory usage (MB)
  - Execution time (seconds)
  - Generates CSV reports and visualizations

### Running Statistics

```bash
python statistics.py
```

This will:
1. Process all PDF files in the `example` directory using each converter
2. Generate CSV files with detailed and summary statistics
3. Create visualizations in the `figures` directory:
   - Boxplots for memory usage and execution time
   - Scatterplots relating file size to memory and time
   - Bar charts with average performance metrics

### Output Files

- `pdf_conversion_stats.csv`: Raw data for all conversions
- `pdf_conversion_stats_summary.csv`: Summary statistics per converter
- `figures/*.png`: Visualization graphics

The statistics help compare the efficiency and resource requirements of different PDF-to-Markdown approaches.
