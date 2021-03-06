import numpy as np

from config import Config
from data import BALANCE_WEIGHTS
from layers import *

cnf = {
    'name': __name__.split('.')[-1],
    'w': 448,
    'h': 448,
    'train_dir': 'data/train_medium',
    'test_dir': 'data/test_medium',
    'batch_size_train': 32,
    'batch_size_test': 8,
    'balance_weights': np.array(BALANCE_WEIGHTS),
    'balance_ratio': 0.975,
    'final_balance_weights':  np.array([1, 2, 2, 2, 2], dtype=float),
    'aug_params': {
        'zoom_range': (1 / 1.15, 1.15),
        'rotation_range': (0, 360),
        'shear_range': (0, 0),
        'translation_range': (-40, 40),
        'do_flip': True,
        'allow_stretch': True,
    },
    'weight_decay': 0.0005,
    'sigma': 0.5,
    'schedule': {
        0: 0.000,
#        150: 0.0003,
#        220: 0.00003,
#        251: 'stop',
        2: 'stop',
    },
}

n = 32

layers = [
    (InputLayer, {'shape': (None, 3, cnf['w'], cnf['h'])}),
    ] + ([(ToCC, {})] if CC else []) + [
    (Conv2DLayer, conv_params(n, filter_size=(5, 5), stride=(2, 2), pad=1, partial_sum=2)),
    (Conv2DLayer, conv_params(n)),
    (MaxPool2DLayer, pool_params()),
    (Conv2DLayer, conv_params(2 * n, filter_size=(5, 5), stride=(2, 2), pad=1, partial_sum=5)),
    (Conv2DLayer, conv_params(2 * n, partial_sum=5)),
    (Conv2DLayer, conv_params(2 * n, partial_sum=5)),
    (MaxPool2DLayer, pool_params()),
    (Conv2DLayer, conv_params(4 * n, partial_sum=3)),
    (Conv2DLayer, conv_params(4 * n, partial_sum=3)),
    (Conv2DLayer, conv_params(4 * n, partial_sum=3)),
    (MaxPool2DLayer, pool_params()),
    (Conv2DLayer, conv_params(8 * n, partial_sum=13)),
    (Conv2DLayer, conv_params(8 * n, partial_sum=13)),
    (Conv2DLayer, conv_params(8 * n, partial_sum=13)),
    (MaxPool2DLayer, pool_params()),
    (Conv2DLayer, conv_params(16 * n, partial_sum=3)),
    (Conv2DLayer, conv_params(16 * n, partial_sum=3)),
    #(MaxPool2DLayer, pool_params(stride=(3, 3))),
    ] + ([(FromCC, {})] if CC else []) + [
    #(RMSPoolLayer, {'pool_size': (3, 3), 'stride': (3, 3)}),
    #(DropoutLayer, {'p': 0.5}),
    #(DenseLayer, dense_params(1024)),
    #(FeaturePoolLayer, {'pool_size': 2}),
    #(DropoutLayer, {'p': 0.5}),
    #(DenseLayer, dense_params(1024)),
    #(FeaturePoolLayer, {'pool_size': 2}),
    (GlobalPoolLayer,{}),
    (DenseLayer, {'num_units': 1}),
]

config = Config(layers=layers, cnf=cnf)
