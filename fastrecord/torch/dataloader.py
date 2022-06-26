import os
import random
import itertools
from typing import Union, List, Tuple, Any

import torch
import torch.multiprocessing as multiprocessing
from torch._utils import ExceptionWrapper
import torch.utils.data._utils as _utils
from torch.utils.data import (
    Sampler,
    BatchSampler,
    Dataset as TorchDataset,
    DataLoader as TorchDataLoader,
)
from torch.utils.data.dataloader import _DatasetKind

from fastrecord.io.fileio import FileReader

class Dataset(TorchDataset):

    def __init__(self, filename: str, check_data: bool = True):
        """
        
        Parameters:
        ----------
            filename:      Fastrecord file name
            check_data: validate checksum or not
        """
        self.filename = filename
        self.reader = FileReader(filename, check_data)

    def __len__(self):
        return self.reader.n

    def __getitem__(self, indexes):
        if self.reader is None:
            raise ValueError(
                "reader is not created yet. Please call open() to create a reader"
            )
        if not isinstance(indexes, (list, tuple)):
            raise TypeError("indexes must be a list of index")

        # read raw bytes data form the FFRecord file
        data = self.reader.read(indexes)

        # pass the raw bytes data into the user-defined process function
        return self.process(indexes, data)

    def process(self, indexes: List[int], data: List[bytearray]) -> List[Any]:
        """ process the raw bytes data
        Args:
            indexes: indexes of each sample in one batch
            data:    raw bytes of each sample in one batch
        Return:
            A list of samples.
            It will be passed into collate_fn in Dataloader
        """
        # user-defined method
        raise NotImplementedError



class DataLoader(TorchDataLoader):

    def __init__(self,
                 dataset,
                 batch_size=1,
                 shuffle: bool = False,
                 sampler=None,
                 batch_sampler=None,
                 num_workers: int = 0,
                 collate_fn=None,
                 pin_memory: bool = False,
                 drop_last: bool = False,
                 timeout: float = 0,
                 worker_init_fn=None,
                 generator=None,
                 *,
                 prefetch_factor: int = 2,
                 persistent_workers: bool = False):

        # use fork to create subprocesses
        if num_workers == 0:
            multiprocessing_context = None
        else:
            multiprocessing_context = 'fork'

        super(DataLoader,
              self).__init__(dataset=dataset,
                             batch_size=batch_size,
                             shuffle=shuffle,
                             sampler=sampler,
                             batch_sampler=batch_sampler,
                             num_workers=num_workers,
                             collate_fn=collate_fn,
                             pin_memory=pin_memory,
                             drop_last=drop_last,
                             timeout=timeout,
                             worker_init_fn=worker_init_fn,
                             multiprocessing_context=multiprocessing_context,
                             generator=generator,
                             prefetch_factor=prefetch_factor,
                             persistent_workers=persistent_workers)

        if isinstance(dataset, Dataset):
            self._dataset_kind = _DatasetKind.SliceMap