import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, Flatten, TimeDistributed, Dropout, LSTMCell, RNN, Bidirectional, Concatenate, Layer
from tensorflow.python.keras.utils import tf_utils
from tensorflow.keras.models import load_model

import pandas as pd
import numpy as np
import string
import re

tf.__version__

len_input = 17
len_target = 15
BUFFER_SIZE = 209032
BATCH_SIZE = 64
embedding_dim = 128
units = 64
vocab_in_size = 10295
vocab_out_size = 20152

def load_processed_data(path):
    processed_corpus = []
    with open(path, 'r') as f:
        for line in f:
            processed_corpus.append(line.replace('\n', ''))
    return processed_corpus

# Prepare the ngram dataset
def generate_dataset(num_samples):
    processed_corpus = load_processed_data('./sentences_processed.txt')
    output = []
    for line in processed_corpus[:num_samples]:
        token_list = line
        for i in range(1, len(line)):
            if line[i] == ' ':
                # phrases are limited by min_ngram size
                # x_ngram has size maximum = 80
                # y_ngram is the next n word
                data = []
                max_ngram = 80
                min_x_ngram = 2
                min_y_ngram = 2
                min_y_length = 10

                x_ngram = token_list[:i+1]
                y_ngram = token_list[i+1:]
                y_ngram = y_ngram.rsplit(" ", len(y_ngram.split(" "))-min_y_ngram)[0]

                # if x_ngram is too big cut it
                while (len(x_ngram) > max_ngram):
                    x_ngram = x_ngram[(len(x_ngram)//2):]
                    x_ngram = x_ngram.split(" ", 1)[1]

                # skip iteration if data length is not sufficient
                if (y_ngram == '' or len(x_ngram.split(" ")) < min_x_ngram
                                  or len(y_ngram.split(" ")) < min_y_ngram
                                  or len(y_ngram) < min_y_length):
                    continue

                # prepare data
                x_ngram = '<start> '+ x_ngram + ' <end>'
                y_ngram = '<start> '+ y_ngram + ' <end>'
                data.append(x_ngram)
                data.append(y_ngram)
                output.append(data)
                
    dummy_df = pd.DataFrame(output, columns=['input','output'])
    return output, dummy_df

# This class creates a word -> index mapping (e.g,. "dad" -> 5) and vice-versa 
class LanguageIndex():
    def __init__(self, lang):
        self.lang = lang
        self.word2idx = {}
        self.idx2word = {}
        self.vocab = set()
        self.create_index()

    def create_index(self):
        for phrase in self.lang:
            self.vocab.update(phrase.split(' '))
        self.vocab = sorted(self.vocab)
        self.word2idx["<pad>"] = 0
        self.idx2word[0] = "<pad>"
        for i,word in enumerate(self.vocab):
            self.word2idx[word] = i + 1
            self.idx2word[i+1] = word

def max_length(t):
    return max(len(i) for i in t)

def load_dataset(num_samples):
    pairs, df = generate_dataset(num_samples)
    out_lang = LanguageIndex(sp for en, sp in pairs)
    in_lang = LanguageIndex(en for en, sp in pairs)
    input_data = [[in_lang.word2idx[s] for s in en.split(' ')] for en, sp in pairs]
    output_data = [[out_lang.word2idx[s] for s in sp.split(' ')] for en, sp in pairs]

    # Pad data sequencecs to the max length
    max_length_in, max_length_out = max_length(input_data), max_length(output_data)
    input_data = tf.keras.preprocessing.sequence.pad_sequences(input_data, maxlen=max_length_in, padding="post")
    output_data = tf.keras.preprocessing.sequence.pad_sequences(output_data, maxlen=max_length_out, padding="post")

    return input_data, output_data, in_lang, out_lang, max_length_in, max_length_out, df

def create_dataset():
    num_samples = 200000
    input_data, teacher_data, input_lang, target_lang, len_input, len_target, df = load_dataset(num_samples)
    return input_lang, target_lang

def initialize_model():
    """### Network model"""
    encoder_inputs = Input(shape=(len_input,))
    encoder_emb = Embedding(input_dim=vocab_in_size, output_dim=embedding_dim)

    # Encoder
    encoder_lstm = Bidirectional(LSTM(units=units, return_sequences=True, return_state=True))
    encoder_out, fstate_h, fstate_c, bstate_h, bstate_c = encoder_lstm(encoder_emb(encoder_inputs))
    state_h = Concatenate()([fstate_h,bstate_h])
    state_c = Concatenate()([bstate_h,bstate_c])
    encoder_states = [state_h, state_c]

    # Decoder
    decoder_inputs = Input(shape=(None,))
    decoder_emb = Embedding(input_dim=vocab_out_size, output_dim=embedding_dim)
    decoder_lstm = LSTM(units=units*2, return_sequences=True, return_state=True)
    decoder_lstm_out, _, _ = decoder_lstm(decoder_emb(decoder_inputs), initial_state=encoder_states)
    decoder_d1 = Dense(units, activation="relu")
    decoder_d2 = Dense(vocab_out_size, activation="softmax")
    decoder_out = decoder_d2(Dropout(rate=.5)(decoder_d1(Dropout(rate=.5)(decoder_lstm_out))))

    # Creating model which combines the encoder and the decoder
    model = Model(inputs = [encoder_inputs, decoder_inputs], outputs=decoder_out)
    optimizer = keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=['sparse_categorical_accuracy'])

    # Loading model weight from checkpoints
    model.load_weights("model.h5")

    # Create the encoder model from the tensors we previously declared.
    encoder_model = Model(encoder_inputs, [encoder_out, state_h, state_c])

    # Generate a new set of tensors for our new inference decoder. Note that we are using new tensors, 
    # this does not preclude using the same underlying layers that we trained on. (e.g. weights/biases).
    inf_decoder_inputs = Input(shape=(None,), name="inf_decoder_inputs")

    # We'll need to force feed the two state variables into the decoder each step.
    state_input_h = Input(shape=(units*2,), name="state_input_h")
    state_input_c = Input(shape=(units*2,), name="state_input_c")
    decoder_res, decoder_h, decoder_c = decoder_lstm(
        decoder_emb(inf_decoder_inputs), 
        initial_state=[state_input_h, state_input_c])
    inf_decoder_out = decoder_d2(decoder_d1(decoder_res))
    inf_model = Model(inputs=[inf_decoder_inputs, state_input_h, state_input_c], 
                    outputs=[inf_decoder_out, decoder_h, decoder_c])

    return encoder_model, inf_model

# Converts the given sentence into a vector of word IDs
def sentence_to_vector(sentence, lang):
    pre = sentence
    vec = np.zeros(len_input)
    sentence_list = [lang.word2idx[s] for s in pre.split(' ')]
    for i,w in enumerate(sentence_list):
        vec[i] = w
    return vec

# Predict all sentence with an input string, an encoder model, decoder model
def predict_all(input_sentence):
    sv = sentence_to_vector(input_sentence, input_lang)
    sv = sv.reshape(1,len(sv))
    [emb_out, sh, sc] = encoder_model.predict(x=sv)
    
    i = 0
    start_vec = target_lang.word2idx["<start>"]
    stop_vec = target_lang.word2idx["<end>"]
    
    cur_vec = np.zeros((1,1))
    cur_vec[0,0] = start_vec
    cur_word = "<start>"
    output_sentence = ""

    while cur_word != "<end>" and i < (len_target-1):
        i += 1
        if cur_word != "<start>":
            output_sentence = output_sentence + " " + cur_word
        x_in = [cur_vec, sh, sc]
        [nvec, sh, sc] = inf_model.predict(x=x_in)
        cur_vec[0,0] = np.argmax(nvec[0,0])
        cur_word = target_lang.idx2word[np.argmax(nvec[0,0])]
    return output_sentence

# Predict only the next word
def predict_next(input_sentence):
    sv = sentence_to_vector(input_sentence, input_lang)
    sv = sv.reshape(1,len(sv))
    [_, sh, sc] = encoder_model.predict(x=sv)

    start_vec = target_lang.word2idx["<start>"]    
    cur_vec = np.zeros((1,1))
    cur_vec[0,0] = start_vec

    x_in = [cur_vec, sh, sc]
    [nvec, sh, sc] = inf_model.predict(x=x_in)
    cur_vec[0,0] = np.argmax(nvec[0,0])
    cur_word = target_lang.idx2word[np.argmax(nvec[0,0])]
    return cur_word

def predict(input_seq):
    output = []
    for seq in input_seq:  
        output.append({"Input seq":seq, "Pred. Seq":predict_all(seq)})
    return output

input_lang, target_lang = create_dataset()
encoder_model, inf_model = initialize_model()

if __name__ == '__main__':
    output = predict(["contribute to", "inform on", "lead by british"])
    results_df = pd.DataFrame.from_dict(output) 
    print(results_df.head(len(output)))