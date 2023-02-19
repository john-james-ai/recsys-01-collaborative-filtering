#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Recommender Systems and Deep Learning in Python                                     #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.6                                                                              #
# Filename   : /tests/test_neighborhood/test_indices.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/recsys-deep-learning-udemy                         #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday February 17th 2023 12:32:15 pm                                               #
# Modified   : Friday February 17th 2023 02:20:06 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

from recsys.neighborhood.factory import CooccurrenceFactory, CoreferenceFactory
from recsys.neighborhood.indices import Coreference, Cooccurrence

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.indices
@pytest.mark.cooccurrence
class TestCoocurrence:  # pragma: no cover
    # ============================================================================================ #
    def test_user(self, ratings, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        factory = CooccurrenceFactory(ratings=ratings)
        index = factory.create_user()
        assert isinstance(index, Cooccurrence)
        assert index.size > 0
        assert len(index) == ratings.n_users
        assert index.mode == "test"

        repo = container.repo.repo()
        repo.reset()
        repo.add(name=index.name, item=index)
        i2 = repo.get(index.name)
        assert i2.size == index.size

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_item(self, ratings, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        factory = CooccurrenceFactory(ratings=ratings)
        index = factory.create_item()
        assert isinstance(index, Cooccurrence)
        assert index.size > 0
        assert len(index) == ratings.n_items
        assert index.mode == "test"

        repo = container.repo.repo()
        repo.add(index.name, item=index)
        i2 = repo.get(index.name)
        assert i2.size == index.size

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)


@pytest.mark.indices
@pytest.mark.coreference
class TestCoreference:  # pragma: no cover
    # ============================================================================================ #
    def test_user(self, ratings, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        factory = CoreferenceFactory(ratings=ratings)
        index = factory.create_user()
        assert isinstance(index, Coreference)
        assert index.size > 0
        assert len(index) > ratings.n_users
        assert index.mode == "test"

        repo = container.repo.repo()
        repo.reset()
        repo.add(index.name, item=index)
        i2 = repo.get(index.name)
        assert i2.size == index.size
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_item(self, ratings, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        factory = CoreferenceFactory(ratings=ratings)
        index = factory.create_item()
        assert isinstance(index, Coreference)
        assert index.size > 0
        assert len(index) > ratings.n_items
        assert index.mode == "test"

        repo = container.repo.repo()
        repo.add(index.name, item=index)
        i2 = repo.get(index.name)
        assert i2.size == index.size
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)
