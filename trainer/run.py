from trainer.prep_data_for_training import PrepDataForTrainer

p_trainer = PrepDataForTrainer(
    debug=True,
    data_folder='./trainer/data',
    mandatory_columns=['datasheet'],
    potential_columns=['category', 'sub_category', 'cleaned_text', 'new_score', 'new_label'],
    remove_duplicate_columns=['datasheet']
)

non_duplicate = p_trainer.load_df('./trainer/output/test.csv')
train_df = p_trainer.run_preprocess(non_duplicate, stop=None, steps=5, start_from=0)
rows_count = train_df.shape[0]
columns_count = train_df.shape[1]
first_item = train_df.head(1)
last_item = train_df.tail(1)
print('rows_count:', rows_count)
print('columns_count:', columns_count)
print('first_item:', first_item)
print('last_item:', last_item)