__all__ = ['Campaign', 'MVCampaign']
from datetime import datetime

from sqlalchemy import (Column, BigInteger, String, Boolean, SmallInteger, select, Index, func, join, text, table,
                        DateTime, ForeignKey, Integer, true, false, Float)
from sqlalchemy_utils import ChoiceType

from x_project_adv_worker_db_watcher.choiceTypes import (CampaignType, CampaignPaymentModel, CampaignStylingType,
                                                         CampaignRemarketingType, CampaignRecommendedAlgorithmType)
from .__libs__.sql_view import create_view
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(BigInteger, primary_key=True)
    account = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()), nullable=False)
    payment_model = Column(ChoiceType(CampaignPaymentModel, impl=Integer()), nullable=False)
    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()), nullable=False)
    campaign_style_logo = Column(String, default="", server_default=text("''"))
    campaign_style_head_title = Column(String, default="", server_default=text("''"))
    campaign_style_button_title = Column(String, default="", server_default=text("''"))
    campaign_style_class = Column(String(length=50), default='Block')
    campaign_style_class_recommendet = Column(String(length=50), default='RecBlock')
    utm = Column(Boolean, default=True, server_default=true())
    utm_human_data = Column(Boolean, default=False, server_default=false())
    disable_filter = Column(Boolean, default=False, server_default=false())
    time_filter = Column(Integer, default=0, server_default="0")
    unique_impression_lot = Column(SmallInteger, default=1, server_default='1')
    lot_concurrency = Column(SmallInteger, default=1, server_default='1')
    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()), nullable=False)
    recommended_algorithm = Column(ChoiceType(CampaignRecommendedAlgorithmType, impl=Integer()), nullable=False)
    recommended_count = Column(SmallInteger, default=1, server_default='1')
    thematic_day_new_auditory = Column(SmallInteger, default=10, server_default='10')
    thematic_day_off_new_auditory = Column(SmallInteger, default=10, server_default='10')
    thematic_range = Column(SmallInteger, default=1)
    click_cost = Column(Float, nullable=False)
    impression_cost = Column(Float, nullable=False)
    started_time = Column(DateTime, default=datetime.now)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign',
        select([
            func.count('offer.id').over(partition_by=Campaign.id).label('offer_count'),
            Campaign.id,
            Campaign.account,
            Campaign.campaign_type,
            Campaign.payment_model,
            Campaign.campaign_style,
            Campaign.campaign_style_logo,
            Campaign.campaign_style_head_title,
            Campaign.campaign_style_button_title,
            Campaign.campaign_style_class,
            Campaign.campaign_style_class_recommendet,
            Campaign.utm,
            Campaign.utm_human_data,
            Campaign.disable_filter,
            Campaign.time_filter,
            Campaign.unique_impression_lot,
            Campaign.lot_concurrency,
            Campaign.unique_impression_lot,
            Campaign.remarketing_type,
            Campaign.recommended_algorithm,
            Campaign.recommended_count,
            Campaign.thematic_range,
            Campaign.click_cost,
            Campaign.impression_cost
        ], distinct=Campaign.id).select_from(
            join(Campaign, table('offer'), Campaign.id == text('offer.id_cam'), isouter=True)
        ), is_mat=True)


Index('ix_mv_campaign_id', MVCampaign.id, unique=True)
