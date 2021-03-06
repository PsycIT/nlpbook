# Reference
# https://gist.github.com/lovit/259bc1d236d78a77f044d638d0df300c?fbclid=IwAR1_KplVF5NzXWVdcb0nNXZYJzJMwLxoZbRM3-wKPLgXqOAZrSt4QcabKg8

# train data download
from Korpora import Korpora
nsmc = Korpora.load("nsmc", force_download=True)

# train data preprocess
save_path = "/Users/david/works/nlpbook/examples/preprocess"
import os
def write_lines(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(f'{line}\n')
train_fpath = os.path.join(save_path, "train.txt")
test_fpath = os.path.join(save_path, "test.txt")
write_lines(train_fpath, nsmc.train.get_all_texts())
write_lines(test_fpath, nsmc.test.get_all_texts())

# train&save BertWordPiece
from tokenizers import BertWordPieceTokenizer
wordpiece_tokenizer = BertWordPieceTokenizer(lowercase=False)
wordpiece_tokenizer.train(
    files=[train_fpath, test_fpath],
    vocab_size=10000,
    min_frequency=1,
)
wordpiece_tokenizer.save_model(save_path)

# BERT tokenization
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained(save_path, do_lower_case=False)
tokenizer.tokenize("안녕하세요")