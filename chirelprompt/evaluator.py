import logging
from itertools import chain, product, combinations
from multiprocessing import Pool
from tqdm import tqdm

import torch
import numpy as np
from sklearn.metrics import precision_recall_fscore_support
from sklearn.neural_network import MLPClassifier

from .lm import RelBERT
from .data import get_lexical_relation_data, get_training_data
from .util import Dataset, triplet_loss, fix_seed

__all__ = ['evaluate_classification']


class Evaluate:

    def __init__(self,
                 dataset,
                 shared_config,
                 label_dict,
                 target_relation=None,
                 default_config: bool = False,
                 config=None):
        self.dataset = dataset
        self.label_dict = label_dict
        self.target_relation = target_relation
        if default_config:
            self.configs = [{'random_state': 0}]
        elif config is not None:
            self.configs = [config]
        else:
            learning_rate_init = [0.001, 0.0001, 0.00001]
            # max_iter = [25, 50, 75]
            hidden_layer_sizes = [100, 150, 200]
            self.configs = [{
                'random_state': 0, 'learning_rate_init': i[0], 'hidden_layer_sizes': i[1]} for i in
                            list(product(learning_rate_init, hidden_layer_sizes))]
        self.shared_config = shared_config

    def run_test(self, clf, x, y, per_class_metric: bool = False):
        """ run evaluation on valid or test set """
        y_pred = clf.predict(x)
        p_mac, r_mac, f_mac, _ = precision_recall_fscore_support(y, y_pred, average='macro')
        p_mic, r_mic, f_mic, _ = precision_recall_fscore_support(y, y_pred, average='micro')
        accuracy = sum([a == b for a, b in zip(y, y_pred.tolist())]) / len(y_pred)
        tmp = {
            'accuracy': accuracy,
            'f1_macro': f_mac,
            'f1_micro': f_mic,
            'p_macro': p_mac,
            'p_micro': p_mic,
            'r_macro': r_mac,
            'r_micro': r_mic
        }
        if per_class_metric and self.target_relation is not None:
            for _l in self.target_relation:
                if _l in self.label_dict:
                    p, r, f, _ = precision_recall_fscore_support(y, y_pred, labels=[self.label_dict[_l]])
                    tmp['f1/{}'.format(_l)] = f[0]
                    tmp['p/{}'.format(_l)] = p[0]
                    tmp['r/{}'.format(_l)] = r[0]
        return tmp

    @property
    def config_indices(self):
        return list(range(len(self.configs)))

    def __call__(self, config_id):
        config = self.configs[config_id]
        report = self.shared_config.copy()
        # train
        x, y = self.dataset['train']
        clf = MLPClassifier(**config).fit(x, y)
        report.update({'classifier_config': clf.get_params()})
        # test
        x, y = self.dataset['test']
        tmp = self.run_test(clf, x, y, per_class_metric=True)
        tmp = {'test/{}'.format(k): v for k, v in tmp.items()}
        report.update(tmp)
        if 'val' in self.dataset:
            x, y = self.dataset['val']
            tmp = self.run_test(clf, x, y, per_class_metric=True)
            tmp = {'val/{}'.format(k): v for k, v in tmp.items()}
            report.update(tmp)
        return report


def evaluate_classification(
        relbert_ckpt: str = None,
        batch_size: int = 512,
        target_relation=None,
        cache_dir: str = None,
        random_seed: int = 0,
        config=None):
    fix_seed(random_seed)
    model = RelBERT(relbert_ckpt)
    data = get_lexical_relation_data(cache_dir)
    report = []
    for data_name, v in data.items():
        logging.info('train model with {} on {}'.format(relbert_ckpt, data_name))
        label_dict = v.pop('label')
        dataset = {}
        for _k, _v in v.items():
            x_tuple = [tuple(_x) for _x in _v['x']]
            x = model.get_embedding(x_tuple, batch_size=batch_size)
            x_back = model.get_embedding([(b, a) for a, b in x_tuple], batch_size=batch_size)
            x = [np.concatenate([a, b]) for a, b in zip(x, x_back)]
            dataset[_k] = [x, _v['y']]
        shared_config = {'model': relbert_ckpt, 'label_size': len(label_dict), 'data': data_name}
        # grid serach
        if 'val' not in dataset:
            logging.info('run default config')
            evaluator = Evaluate(dataset, shared_config, label_dict, target_relation=target_relation,
                                 default_config=True)
            report += [evaluator(0)]
        elif config is not None and data_name in config:
            logging.info('run with given config')
            evaluator = Evaluate(dataset, shared_config, label_dict, target_relation=target_relation,
                                 config=config[data_name])
            report += [evaluator(0)]

        else:
            logging.info('run grid search')
            pool = Pool()
            evaluator = Evaluate(dataset, shared_config, label_dict, target_relation=target_relation)
            report += pool.map(evaluator, evaluator.config_indices)
            pool.close()
    del model
    return report

