import sys
from argparse import ArgumentParser

from core.config import Config
from core.etl.load_data import load_files_to_postgres


def load_dataset(dataset: str) -> None:
    directory_path, file_type, table_name = Config.DATASETS[dataset]
    load_files_to_postgres(
        directory_path=directory_path,
        file_type=file_type,
        table_name=table_name,
    )


def main():
    parser = ArgumentParser(description="Load Data for for a specific dataset.")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help=f"Dataset to process. Options: {', '.join(Config.DATASETS.keys())}"
    )

    args = parser.parse_args()

    if args.dataset not in Config.DATASETS:
        print(f"❌ Invalid dataset '{args.dataset}'. Must be one of: {', '.join(Config.DATASETS.keys())}")
        sys.exit(1)

    print(f"✅ Running pipeline for dataset: {args.dataset} ({Config.DATASETS[args.dataset]})")

    load_dataset(dataset=args.dataset)


if __name__ == "__main__":
    main()
