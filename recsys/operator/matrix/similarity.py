#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Recommender Systems in Python 1: Neighborhood Methods                               #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /recsys/operator/matrix/similarity.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/recsys-01-collaborative-filtering                  #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 9th 2023 04:26:15 pm                                                 #
# Modified   : Saturday March 11th 2023 02:09:52 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Cooccurrence Matrix Factory"""
from datetime import datetime
from typing import Union

import numpy as np
from scipy.sparse import coo_matrix, csc_matrix, csr_matrix

from recsys.data.dataset import Dataset
from recsys.data.matrix import Matrix
from recsys.operator.base import Operator, Artifact

# ------------------------------------------------------------------------------------------------ #


class SimilarityMatrixFactory(Operator):
    """Cooccurrence Matrix Factory

    Args:
        name (str): The name of the interaction matrix
        description (str): Describes the interaction matrix
        metric (str): One of the currently supported similarity metrics. See Notes:
        destination (str): The filepath for persisting the matrix
        dim (str): Either 'u' or 'user' for user dimension, or 'i' or 'item' for item dimension.
        force (bool): Whether to overwrite existing data if it already exists.

    Notes:
        The currently supported similarity metrics and their parameter values are:
            param               metric
            -----     -----------------------
              c       Cosine Similarity
              a       Adjusted Cosine Similarity
              p       Pearson Correlation

        For the metric parameter, only the first letter lower case will be used.
    """

    __dims = {"u": "User", "i": "Item"}
    __metrics = {
        "a": "Adjusted Cosine Similarity",
        "c": "Cosine Similarity",
        "p": "Pearson Correlation",
    }

    def __init__(
        self,
        name: str,
        description: str,
        metric: str,
        destination: str,
        dim: str,
        datasource: str = "movielens25m",
        force: bool = False,
    ) -> None:
        super().__init__(destination=destination, force=force)
        self._name = name
        self._description = description
        self._datasource = datasource

        try:
            self._dim = SimilarityMatrixFactory.__dims[dim[0].lower()]
        except KeyError:
            msg = f"dim parameter value {dim} is not supported. Valid values are: {SimilarityMatrixFactory.__dims}"
            self._logger.error(msg)
            raise ValueError(msg)

        try:
            self._metric = SimilarityMatrixFactory.__metrics[metric[0].lower()]
        except KeyError:
            msg = f"metric parameter value {metric} is not a supported metric. Valid values are: {SimilarityMatrixFactory.__metrics.values()}"
            self._logger.error(msg)
            raise ValueError(msg)

        self._artifact = Artifact(isfile=True, path=self._destination, uripath="matrix")

    def execute(self, data: Dataset, context: dict = None) -> np.array:
        """Creates and persists a cosine similarity matrix object from a Dataset.

        Args:
            data (Matrix): The Interaction Matrix

        """

        if not self._skip(endpoint=self._destination):

            data = data or self._get_data(filepath=self._source)
            matrix = self._get_matrix(data)
            return self._compute_similarity(matrix)
        else:
            return self._get_data(filepath=self._destination)

    def _get_matrix(self, data: Dataset) -> Union[csc_matrix, csr_matrix]:
        """Obtains the sparse matrix based upon the axis and metric"""

        if self._metric[0].lower() == "c":
            centered_by = None
        elif self._dim == "User":
            centered_by = "user"
        else:
            centered_by = "item"

        if self._dim == "User":
            return data.to_csr(centered_by=centered_by)
        else:
            return data.to_csc(centered_by=centered_by).T

    def _compute_similarity(self, matrix: Union[csc_matrix, csr_matrix]) -> Matrix:
        """Computes similarity and returns a coo matrix"""

        started = datetime.now()
        self._logger.debug(f"\nCreating {self._dim} {self._metric} Matrix")

        squared_norm = matrix.multiply(matrix)
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.debug(f"\tComputed element-wise multiplication...{elapsed} seconds elapsed")

        norm = np.array(np.sqrt(squared_norm.sum(axis=1)))[:, 0]
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.debug(f"\tComputed norm...{elapsed} seconds elapsed")

        row_indices, col_indices = matrix.nonzero()
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.debug(f"\tExtracted nnz values...{elapsed} seconds elapsed")

        matrix.data /= norm[row_indices]
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.debug(f"\tComputed element-wise division...{elapsed} seconds elapsed")

        cosine = matrix.dot(matrix.T)
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.debug(f"\tComputed dot product...{elapsed} seconds elapsed")

        cosine = coo_matrix(matrix)
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.debug(f"\tConverted to coo_matrix...{elapsed} seconds elapsed")

        matrix = Matrix(
            name=self._name,
            description=self._description,
            data=cosine,
            datasource=self._datasource,
        )

        self._put_data(filepath=self._destination, data=matrix)
        elapsed = (datetime.now() - started).total_seconds()
        self._logger.info(
            f"Created {self._dim} {self._metric}, {self._name} and stored at {self._destination} in {elapsed} seconds."
        )

        return matrix
