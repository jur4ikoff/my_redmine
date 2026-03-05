import sys
import os
import subprocess
from pathlib import Path

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

DIRECTORIES = [
    Path(f"{script_dir}/ready"),
    Path(f"{script_dir}/report"),
]


def compress_pdf(input_path: Path) -> bool:
    if not input_path.is_file():
        print(f"Ошибка: файл '{input_path}' не найден или это не файл", file=sys.stderr)
        return False

    if input_path.suffix.lower() != ".pdf":
        print(f"Ошибка: файл '{input_path}' не имеет расширения .pdf", file=sys.stderr)
        return False

    temp_path = input_path.with_name(input_path.stem + "_cleaned.pdf")

    gs_args = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dOptimize=true",
        "-dQUIET",
        "-dBATCH",
        "-dRemoveUnusedFonts=true",
        "-dRemoveUnusedImages=true",
        "-dOptimizeResources=true",
        "-dDetectDuplicateImages",
        "-dCompressFonts=true",
        "-dEmbedAllFonts=true",
        "-dSubsetFonts=true",
        "-dPreserveAnnots=true",
        "-dPreserveMarkedContent=true",
        "-dPreserveOverprintSettings=true",
        "-dPreserveHalftoneInfo=true",
        "-dPreserveOPIComments=true",
        "-dPreserveDeviceN=true",
        "-dMaxInlineImageSize=0",
        f"-sOutputFile={temp_path}",
        str(input_path),
    ]

    try:
        result = subprocess.run(gs_args, capture_output=True)
        if result.returncode != 0:
            print(f"Ошибка очистки файла '{input_path}'", file=sys.stderr)
            if temp_path.exists():
                temp_path.unlink()
            return False
    except FileNotFoundError:
        print(
            "Ошибка: не найдена команда 'gs' (Ghostscript). Убедитесь, что он установлен.",
            file=sys.stderr,
        )
        return False

    orig_size = input_path.stat().st_size
    clean_size = temp_path.stat().st_size
    threshold = orig_size * 0.9

    if clean_size < threshold:
        temp_path.replace(input_path)
        print(f"Очищен: {input_path}")
        return True
    else:
        print(f"Недостаточное сжатие; нетронут: {input_path}")
        temp_path.unlink()
        return False


def main():
    for root_dir in DIRECTORIES:
        if not root_dir.exists():
            print(
                f"Предупреждение: директория '{root_dir}' не существует — пропускаем",
                file=sys.stderr,
            )
            continue

        print(f"Обработка директории: {root_dir}")
        for pdf_file in root_dir.rglob("*.pdf"):
            compress_pdf(pdf_file)


if __name__ == "__main__":
    main()
