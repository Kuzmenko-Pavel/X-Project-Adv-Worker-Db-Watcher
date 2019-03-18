# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from enum import Enum
from enum import EnumMeta


class DefaultEnumMeta(EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        try:
            return EnumMeta.__call__(cls, value, *args, **kwargs)
        except Exception as e:
            return next(iter(cls))

    def __getitem__(cls, name):
        return cls._member_map_[name]


class Language(Enum):
    ru = 1
    uk = 2
    en = 3


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


class PermissionType(Enum):
    full = 1
    write = 2
    read = 3


class AccountRelationType(Enum):
    none = 1
    agential = 2
    superior = 3
    managerial = 4


class FeedType(Enum):
    auto = 1
    yml = 2
    prom = 3
    price = 4
    hotline = 5
    satu = 6


class CampaignStylingType(Enum):
    dynamic = 1
    common = 2
    remarketing = 3
    recommended = 4
    style_1 = 5
    style_2 = 6
    style_3 = 7


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


class AMQPStatusType(Enum):
    new = 0
    start = 1
    stop = 2
    update = 3
    freezing = 4
    delete = 5


class BlockType(Enum):
    adaptive = 1
    static = 2


BlockType.adaptive.label = 'Adaptive'
BlockType.static.label = 'Static'
