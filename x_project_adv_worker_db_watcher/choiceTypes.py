# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from enum import Enum


class ProjectType(Enum):
    Root = 1
    Adload = 2
    Getmyad = 3


class AccountType(Enum):
    Root = 1
    Admin = 2
    Accountant = 3
    SuperManager = 4
    Manager = 5
    Agency = 6
    Customer = 7


class AccountRelationType(Enum):
    none = 1
    agential = 2
    superior = 3
    managerial = 4


class CampaignStylingType(Enum):
    dynamic = 1
    common = 2
    remarketing = 3
    recommended = 4
    style_1 = 5
    style_2 = 6
    style_3 = 7


class CampaignPaymentModel(Enum):
    ppc = 1
    ppi = 2
    auto = 3


class CampaignType(Enum):
    new_auditory = 1
    remarketing = 2
    thematic = 3
    relevant_auditory = 4
    social = 5


class CampaignRemarketingType(Enum):
    offer = 1
    account = 2


class CampaignRecommendedAlgorithmType(Enum):
    none = 0
    always = 1
    descending = 2
    ascending = 3


class OfferType(Enum):
    banner = 1
    teaser = 2


class BlockPatternOrient(Enum):
    horizontal = 1
    vertical = 2
    square = 3


class AMQPStatusType(Enum):
    new = 0
    start = 1
    stop = 2
    update = 3
    freezing = 4
    delete = 5


class CampaignActionType(Enum):
    new = 1
    start = 2
    stop = 3
    edit = 4
    delete = 5
    freezing = 6
    statistic = 7
    offers = 8
    blacklist = 9
    cost = 10
    copy = 11
    limit = 12


class OfferActionType(Enum):
    new = 1
    moderation = 2
    invalid = 3
    start = 4
    stop = 5
    edit = 6
    delete = 7
    statistic = 8
    copy = 9


class SiteActionType(Enum):
    new = 1
    moderation = 2
    invalid = 3
    start = 4
    edit = 5
    delete = 6
    statistic = 7


class BlockActionType(Enum):
    new = 1
    edit = 2
    delete = 3
    statistic = 4
    copy = 5


class BlockType(Enum):
    adaptive = 1
    static = 2