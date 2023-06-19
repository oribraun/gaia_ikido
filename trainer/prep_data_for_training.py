import pandas as pd
import os

from gaiaframework.base.server.output_logger import OutputLogger

logger = OutputLogger('prep_data_for_training')

class PrepDataForTrainer:
    debug=False
    allow_files = ['.csv', '.xlsx']
    data_folder = './trainer/data'
    base_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    mandatory_columns: list = []
    potential_columns: list = []
    remove_duplicate_columns: list = []
    def __init__(self, allow_files=None, data_folder=None, mandatory_columns=[], potential_columns=[], remove_duplicate_columns=[], debug=False):
        if allow_files:
            self.allow_files = allow_files
        if data_folder:
            self.data_folder = data_folder
        self.mandatory_columns = mandatory_columns
        self.potential_columns = potential_columns
        self.remove_duplicate_columns = remove_duplicate_columns
        self.debug = debug

    def load_files(self):
        data_abs_path = os.path.join(self.base_dir, self.data_folder)
        file_list = os.listdir(data_abs_path)
        end_with = tuple(self.allow_files)
        valid_files = [file for file in file_list if file.endswith(end_with)]
        if self.debug:
            logger.info('load_files', {"valid_files": valid_files})
        return valid_files

    def read_and_merge_files(self, files):
        merged_data = pd.DataFrame()
        for file_name in files:
            file_path = os.path.join(self.base_dir, self.data_folder, file_name)
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                continue
            if self.debug:
                logger.info('read_and_merge_files', {"columns": df.columns})
            if all(col in df.columns for col in self.mandatory_columns):
                selected_columns = self.mandatory_columns.copy()  # Create a copy of mandatory_fields

                # Iterate through potential columns
                for col in self.potential_columns:
                    if col in df.columns:
                        # Clone the existing column
                        selected_columns.append(col)
                    else:
                        # Add a new column with NaN values
                        df[col] = pd.NA
                        selected_columns.append(col)

                merged_data = merged_data.append(df[selected_columns], ignore_index=True)

        if self.debug:
            logger.info('read_and_merge_files', {"merged_data": merged_data})
        return merged_data

    def remove_duplicate(self, df):
        if len(self.remove_duplicate_columns):
            df['non_null_count'] = df.notnull().sum(axis=1)
            df = df.sort_values(by=['non_null_count'], ascending=False)
            df = df.drop('non_null_count', axis=1)
            df.drop_duplicates(subset=self.remove_duplicate_columns, keep='first', inplace=True)
        if self.debug:
            logger.info('remove_duplicate', {"df": df})
        return df

    def save_df(self, df, folder):
        save_path = os.path.join(self.base_dir, folder)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if save_path.endswith('.csv'):
            df.to_csv(save_path, index=False)
        elif save_path.endswith('.xlsx'):
            df.to_excel(save_path, index=False)

