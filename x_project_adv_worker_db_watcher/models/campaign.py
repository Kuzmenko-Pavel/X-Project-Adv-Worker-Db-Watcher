__all__ = ['Campaign', 'MVCampaign']
from datetime import datetime

from sqlalchemy import (Column, BigInteger, String, Boolean, SmallInteger, select, Index, text,
                        DateTime, Integer, true, false, Float)
from sqlalchemy_utils import ChoiceType, UUIDType

from x_project_adv_worker_db_watcher.choiceTypes import (CampaignType, CampaignPaymentModel, CampaignStylingType,
                                                         CampaignRemarketingType, CampaignRecommendedAlgorithmType)
from .__libs__.sql_view import create_view
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(BigInteger, primary_key=True)
    id_account = Column(BigInteger, nullable=False)
    guid = Column(UUIDType(binary=True))
    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()), nullable=False)
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
    payment_model = Column(ChoiceType(CampaignPaymentModel, impl=Integer()), nullable=False)
    lot_concurrency = Column(SmallInteger, default=1, server_default='1')
    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()), nullable=False)
    recommended_algorithm = Column(ChoiceType(CampaignRecommendedAlgorithmType, impl=Integer()), nullable=False)
    recommended_count = Column(SmallInteger, default=1, server_default='1')
    thematic_day_new_auditory = Column(SmallInteger, default=10, server_default='10')
    thematic_day_off_new_auditory = Column(SmallInteger, default=10, server_default='10')
    thematic_range = Column(SmallInteger, default=1)
    offer_count = Column(BigInteger)
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
            Campaign.id,
            Campaign.id_account,
            Campaign.guid,
            Campaign.campaign_type,
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
            Campaign.payment_model,
            Campaign.lot_concurrency,
            Campaign.remarketing_type,
            Campaign.recommended_algorithm,
            Campaign.recommended_count,
            Campaign.thematic_range,
            Campaign.offer_count,
            Campaign.click_cost,
            Campaign.impression_cost
        ]).select_from(Campaign), is_mat=True)


Index('ix_mv_campaign_id', MVCampaign.id, unique=True)
