from trainer.prep_data_for_training import PrepDataForTrainer

p_trainer = PrepDataForTrainer(
    debug=True,
    data_folder='./trainer/data',
    mandatory_columns=['datasheet'],
    potential_columns=['category', 'sub_category', 'cleaned_text', 'new_score', 'new_label'],
    remove_duplicate_columns=['datasheet']
)
files = p_trainer.load_files()
# merged_df = p_trainer.read_and_merge_files(files)
# # d = merged_df[~merged_df['new_score'].isna()]
# # print('merged_df d', d['new_score'])
# non_duplicate = p_trainer.remove_duplicate(merged_df)
# # d = non_duplicate[~non_duplicate['new_score'].isna()]
# # print('non_duplicate d', d['new_score'])
# p_trainer.save_df(non_duplicate, './trainer/output/test.csv')
# p_trainer.save_df(non_duplicate, './trainer/output/test.xlsx')
#
# train_df = p_trainer.run_preprocess(non_duplicate, stop=None, steps=5)
#
# p_trainer.save_df(train_df, './trainer/output/train.csv')
# p_trainer.save_df(train_df, './trainer/output/train.xlsx')
#
# load_df = p_trainer.load_df('./trainer/output/train.csv')
# rows_count = load_df.shape[0]
# columns_count = load_df.shape[1]
# print('rows_count:', rows_count)
# print('columns_count:', columns_count)
