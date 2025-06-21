import pandas as pd
from pandas import value_counts


class DataService:
    def __init__(self, storage_service):
        self.storage_service = storage_service

    def calculate_basic_stats(self, df):
        stats = {}
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            stats[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'min': df[col].min(),
                'max': df[col].max(),
                'std': df[col].std()
            }

        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            stats[col] = {
                'unique_count': df[col].nunique(),
                'top_value': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'top_value_count': df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
            }

        return stats

    # вычесляет корреляцию
    def calculate_correlation(self, df):
        numeric_cols = df.select_dtyps(include=['number']).columns
        if len(numeric_cols) >= 0:
            return df[numeric_cols].corr().to_dict()
        return None

    # удаление дубликатов
    def clean_data(self, df, params):
        if params.get('remove_duplicates', False):
            df = df.drop_duplicates()

        # обработка пропущенных значений
        missing_values_strategy = params.get('missing_values', 'drop')

        # Удаляет все строки, содержащие пропущенные значения
        if missing_values_strategy == 'drop':
            df = df.dropna()

        # Заполняет пропущенные значения указанным fill_value (по умолчанию 0).
        elif missing_values_strategy == 'fill':
            fill_value = params.get('fill_value', 0)
            df = df.fillna(fill_value)

        # Для числовых колонок заполняет пропущенные значения средним значением по колонке
        elif missing_values_strategy == 'mean':
            for col in df.select_dtyps(include=['number']).columns:
                df[col] = df[col].fillna(df[col].mean())


        return df



















