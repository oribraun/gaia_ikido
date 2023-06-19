from trainer.prep_data_for_training import PrepDataForTrainer

p = PrepDataForTrainer(
    debug=True,
    data_folder='./trainer/data',
    mandatory_columns=['datasheet'],
    potential_columns=['category', 'sub_category', 'cleaned_text', 'new_score', 'new_label'],
    remove_duplicate_columns=['datasheet']
)
files = p.load_files()
merged_df = p.read_and_merge_files(files)
# d = merged_df[~merged_df['new_score'].isna()]
# print('merged_df d', d['new_score'])
non_duplicate = p.remove_duplicate(merged_df)
# d = non_duplicate[~non_duplicate['new_score'].isna()]
# print('non_duplicate d', d['new_score'])
p.save_df(non_duplicate, './trainer/output/test.csv')
p.save_df(non_duplicate, './trainer/output/test.xlsx')
