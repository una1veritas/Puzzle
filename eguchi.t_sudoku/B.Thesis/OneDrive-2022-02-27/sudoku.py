import csv
import numpy as np

from keras.models import Model, load_model
from keras.layers import Conv2D, Input, Concatenate, Flatten, Reshape, Dense, Activation
from keras.utils import plot_model
from keras.preprocessing.image import Iterator


def build_model():
    inp = Input((9, 9, 10))
    x1 = Conv2D(filters=10, kernel_size=(3, 3), strides=(3, 3), padding='valid', activation='relu')(inp)
    x2 = Conv2D(filters=10, kernel_size=(9, 1), padding='valid', activation='relu')(inp)
    x3 = Conv2D(filters=10, kernel_size=(1, 9), padding='valid', activation='relu')(inp)

    x1 = Flatten()(x1)
    x2 = Flatten()(x2)
    x3 = Flatten()(x3)

    x = Concatenate()([x1, x2, x3])
    x = Dense(9 * 9 * 9)(x)
    x = Reshape((9, 9, 9))(x)
    x = Activation('softmax')(x)

    model = Model(inp, x)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    return model


def read_csv(path):
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # first row is header

        quizes = []
        solutions = []
        for quiz, solution in reader:
            quizes.append(quiz)
            solutions.append(solution)
    return quizes, solutions


def construct_board(s, is_solution=False):
    if is_solution:
        board = np.zeros((9, 9, 9), dtype=np.float32)
    else:
        board = np.zeros((9, 9, 10), dtype=np.float32)  # the 10th dim is for empty grid
    for i, ss in enumerate(s):
        board[i // 9, i % 9, int(ss) - 1] = 1.0   # map 1 to 0th, 2 to 1th, ..., 9 to 8th, and 0 to -1th
    return board


class SudokuIterator(Iterator):
    def __init__(self, csv_path, batch_size, shuffle=False, seed=0):
        quizes, solutions = read_csv(csv_path)
        self.x = np.array([construct_board(q) for q in quizes])
        self.y = np.array([construct_board(s, is_solution=True) for s in solutions])

        n = len(self.x)
        self.steps_per_epoch = n // batch_size
        super(SudokuIterator, self).__init__(n, batch_size, shuffle, seed)

    def _get_batches_of_samples(self, index_array):
        batch_x = self.x[index_array]
        batch_y = self.y[index_array]
        return batch_x, batch_y

    def _get_batches_of_transformed_samples(self, index_array):
        return self._get_batches_of_samples(index_array)  # Keras Iterator requirement

    def next(self):
        with self.lock:
            index_array = next(self.index_generator)
        return self._get_batches_of_samples(index_array)


print('building model...')
sudoku_model = build_model()
print('done.')

print('building generator...')
train_gen = SudokuIterator(csv_path='sudoku10000.csv', batch_size=64, shuffle=True)
print('done.')

sudoku_model.fit_generator(train_gen, steps_per_epoch=train_gen.steps_per_epoch, epochs=50)
sudoku_model.save('sudoku_model.h5')
