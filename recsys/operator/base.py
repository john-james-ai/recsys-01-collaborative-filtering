#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Recommender Systems in Python 1: Neighborhood Methods                               #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.6                                                                              #
# Filename   : /recsys/operator/base.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/recsys-01-collaborative-filtering                  #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday February 28th 2023 04:13:11 pm                                              #
# Modified   : Thursday March 9th 2023 08:58:08 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
from typing import Any, Union

from recsys.services.io import IOService


# ------------------------------------------------------------------------------------------------ #
class Operator(ABC):
    """Abstract base class for classes that perform a descrete operation as part of a larger workflow"""

    def __init__(
        self, source: str = None, destination: str = None, force: bool = False, *args, **kwargs
    ) -> None:
        self._source = source
        self._destination = destination
        self._force = force
        self._artifact = None
        self._logger = logging.getLogger(
            f"{self.__module__}.{self.__class__.__name__}",
        )

    @property
    def artifact(self) -> dict:
        """Returns the artifact key value pair to register with MLFlow."""
        return self._artifact

    @abstractmethod
    def execute(self, *args, **kwargs) -> Union[Any, None]:
        """Code from subclass that executes the operation"""

    def _get_data(self, filepath: str) -> Any:
        try:
            return IOService.read(filepath)
        except Exception as e:
            self._logger.error(e)
            raise

    def _put_data(self, filepath: str, data: Any) -> None:
        if filepath is not None:
            IOService.write(filepath=filepath, data=data)

    def _skip(self, endpoint: str) -> bool:
        """Determines of operation should be skipped if endpoint already exists."""
        if endpoint is None:
            return False
        elif self._force is True:
            return False
        elif os.path.isfile(endpoint):
            self._logger.info(f"{self.__class__.__name__} skipped. Endpoint already exists.")
            return True
        elif os.path.isdir(endpoint) and len(os.listdir(endpoint)) > 0:
            self._logger.info(f"{self.__class__.__name__} skipped. Endpoint already exists.")
            return True
        else:
            return False


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Artifact:
    isfile: bool  # Indicates whether the artifact is a file or a directory
    path: str  # The filepath or directory containing the artifacts
    uripath: str  # The directory within the artifact store to place the artifact
