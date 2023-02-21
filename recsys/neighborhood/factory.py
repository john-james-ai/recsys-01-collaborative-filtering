#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Recommender Systems and Deep Learning in Python                                     #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.6                                                                              #
# Filename   : /recsys/neighborhood/factory.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/recsys-deep-learning-udemy                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday February 4th 2023 02:51:47 pm                                              #
# Modified   : Friday February 17th 2023 02:22:45 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Matrix Factory Module"""
from itertools import combinations

from tqdm import tqdm

from recsys.data.rating import RatingsDataset
from recsys.neighborhood.base import IndexFactory
from recsys.neighborhood.indices import Cooccurrence, Coreference


# ------------------------------------------------------------------------------------------------ #
class CooccurrenceFactory(IndexFactory):
    """Creates a user_item, or an item_user cooccurrence index

    Args:
        ratings (RatingsDataset): Input ratings dataset.
    """

    def __init__(self, ratings: RatingsDataset) -> None:
        super().__init__(ratings=ratings)

    def create_user(self) -> Cooccurrence:
        U = {}
        for useridx in tqdm(self._ratings.users):
            U[useridx] = self._ratings.get_items_rated_user(useridx=useridx)
        index = Cooccurrence(
            index=U, ratings_dataset_name=self._ratings.name, mode=self._ratings.mode, user=True
        )
        return index

    def create_item(self) -> Cooccurrence:
        I = {}  # noqa E741
        for itemidx in tqdm(self._ratings.items):
            I[itemidx] = self._ratings.get_users_rated_item(itemidx=itemidx)
        index = Cooccurrence(
            index=I, ratings_dataset_name=self._ratings.name, mode=self._ratings.mode, user=False
        )
        return index


# ------------------------------------------------------------------------------------------------ #
class CoreferenceFactory(IndexFactory):
    """Constructs user-user and item-item coreference index objects

    Args:
        ratings (RatingsDataset): Input ratings dataset.
    """

    def __init__(self, ratings: RatingsDataset) -> None:
        super().__init__(ratings=ratings)

    def create_user(self) -> Coreference:
        """Constructs index of co-occuring users, i.e. rated same film."""

        UV = {}

        for itemidx in tqdm(self._ratings.items):
            item_ratings = self._ratings.get_item_ratings(itemidx=itemidx)
            for uv_pair in combinations(item_ratings["useridx"].values, 2):
                if UV.get(uv_pair, None) is not None:
                    UV[uv_pair].append(itemidx)
                else:
                    UV[uv_pair] = [itemidx]
            index = Coreference(
                index=UV,
                ratings_dataset_name=self._ratings.name,
                mode=self._ratings.mode,
                user=True,
            )
        return index

    def create_item(self) -> Coreference:
        """Constructs index of co-occuring items, i.e. rated by a user."""

        IJ = {}

        for useridx in tqdm(self._ratings.users):
            user_ratings = self._ratings.get_user_ratings(useridx=useridx)
            for ij_pair in combinations(user_ratings["itemidx"].values, 2):
                if IJ.get(ij_pair, None) is not None:
                    IJ[ij_pair].append(useridx)
                else:
                    IJ[ij_pair] = [useridx]
            index = Coreference(
                index=IJ,
                ratings_dataset_name=self._ratings.name,
                mode=self._ratings.mode,
                user=False,
            )
        return index