import pandas as pd
import concurrent.futures
from ludwig.api import LudwigModel

def data_cleaner(filename):
    with open(f'{filename}','r') as f:
        clean_lines = [(line.split()[0][-1],' '.join(line.split()[1:])) for line in f]
    return clean_lines

pool = concurrent.futures.ThreadPoolExecutor(max_workers=20)

clean_reviews = pool.map(data_cleaner, ['test.txt',])
clean_reviews = list(clean_reviews)
clean_reviews = sum(clean_reviews,[])

reviews_df = pd.DataFrame(clean_reviews, columns = ['category','text'])
reviews_df.to_csv('/Users/mdrozdov/Downloads/amazonreviews/clean_train.csv')

reviews_df = pd.read_csv('/Users/mdrozdov/Downloads/amazonreviews/clean_train.csv', usecols = ['category','text'], nrows = 100000)

model_definition = {
    'input_features' : 
    [{'name':'text', 'type':'text', 'level': 'word',
        'encoder': 'parallel_cnn', 'bidirectional':'true'}],
    'output_features':
    [{'name':'category', 'type': 'category'}]
    }


print('creating model')
model = LudwigModel(model_definition)
print('training model')
train_stats = model.train(data_df = reviews_df)
model.close()