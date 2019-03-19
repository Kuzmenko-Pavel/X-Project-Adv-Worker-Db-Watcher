from datetime import datetime

from x_project_adv_worker_db_watcher.logger import *
from .adv_settings import AdvSetting
from .block_settings import BlockSetting


def thematic_range(started_time, thematic_day_new_auditory, thematic_day_off_new_auditory):
    range = 0
    now = datetime.now()
    days = (now - started_time).days
    if days > thematic_day_new_auditory:
        thematic_persent = (100.0 / thematic_day_off_new_auditory) * (days - thematic_day_new_auditory)
        if thematic_persent > 90:
            thematic_persent = 90
        range = int(thematic_persent)
    return range


def trim_by_words(text, max_len=None):
    if text is None:
        return ''
    if max_len is None or len(text) <= max_len:
        return text
    trimmed_simple = text[:max_len]
    trimmed_by_words = trimmed_simple.rpartition(' ')[0]
    return u'%s…' % (trimmed_by_words or trimmed_simple)


def __to_int(val):
    if val is None:
        val = 0
    elif isinstance(val, str):
        if val == 'auto':
            val = 0
        elif val == '':
            val = 0
        else:
            val = val.replace('px', '')
            val = val.replace('x', '')
    return int(float(val))


def __to_color(val):
    if isinstance(val, str) and len(val) == 6:
        val = '#' + val
    else:
        val = '#ffffff'
    return val


def __to_str(val):
    return val


def __to_float(val):
    if isinstance(val, float):
        return val
    if isinstance(val, int):
        val = float(val)
    else:
        val = 0.0
    return val


def __to_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        if val in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
            val = True
        else:
            val = False
    elif isinstance(val, int) or isinstance(val, float):
        val = bool(val)
    else:
        val = False
    return val


def create_adv_setting(data, name=None):
    if name is None:
        name = ''
    try:
        adv = AdvSetting()
        adv.width = __to_int(data.get('Advertise', {}).get('width'))
        adv.height = __to_int(data.get('Advertise', {}).get('height'))
        adv.top = __to_int(data.get('Advertise', {}).get('top'))
        adv.left = __to_int(data.get('Advertise', {}).get('left'))
        adv.border_radius = [
            __to_int(data.get('Advertise', {}).get('border_top_left_radius')),
            __to_int(data.get('Advertise', {}).get('border_top_right_radius')),
            __to_int(data.get('Advertise', {}).get('border_bottom_right_radius')),
            __to_int(data.get('Advertise', {}).get('border_bottom_left_radius'))
        ]
        adv.margin = [
            __to_int(data.get('Advertise', {}).get('margin_top')),
            __to_int(data.get('Advertise', {}).get('margin_right')),
            __to_int(data.get('Advertise', {}).get('margin_bottom')),
            __to_int(data.get('Advertise', {}).get('margin_left'))
        ]
        adv.border = __to_int(data.get('Advertise', {}).get('borderWidth%s' % name))
        adv.border_color = __to_color(data.get('Advertise', {}).get('borderColor%s' % name))
        background_color_transparent = data.get('Advertise', {}).get('backgroundColor%sStatus' % name, True)
        adv.background_color = 'transparent' if background_color_transparent else __to_color(
            data.get('Advertise', {}).get('backgroundColor%s' % name)
        )
        hide_header = __to_bool(data.get('%sHeader' % name, {}).get('hide', False))
        if not hide_header:
            adv.header.width = __to_int(data.get('%sHeader' % name, {}).get('width'))
            adv.header.height = __to_int(data.get('%sHeader' % name, {}).get('height'))
            adv.header.top = __to_int(data.get('%sHeader' % name, {}).get('top'))
            adv.header.left = __to_int(data.get('%sHeader' % name, {}).get('left'))
        adv.header.font.size = __to_int(data.get('%sHeader' % name, {}).get('fontSize'))
        adv.header.font.color = __to_color(data.get('%sHeader' % name, {}).get('fontColor'))
        adv.header.font.align = __to_str(data.get('%sHeader' % name, {}).get('align'))
        adv.header.font.weight = __to_int(data.get('%sHeader' % name, {}).get('fontBold'))
        adv.header.font.letter = __to_float(data.get('%sHeader' % name, {}).get('letter_spacing'))
        adv.header.font.line = __to_float(data.get('%sHeader' % name, {}).get('line_height'))
        adv.header.font.variant = __to_bool(data.get('%sHeader' % name, {}).get('font_variant'))
        adv.header.font.decoration = __to_bool(data.get('%sHeader' % name, {}).get('fontUnderline'))
        adv.header.font.family = __to_str(
            data.get('%sHeader' % name, {}).get('fontFamily', 'arial, sans serif'))
        hide_description = __to_bool(data.get('%sDescription' % name, {}).get('hide', False))
        if not hide_description:
            adv.description.width = __to_int(data.get('%sDescription' % name, {}).get('width'))
            adv.description.height = __to_int(data.get('%sDescription' % name, {}).get('height'))
            adv.description.top = __to_int(data.get('%sDescription' % name, {}).get('top'))
            adv.description.left = __to_int(data.get('%sDescription' % name, {}).get('left'))
        adv.description.font.size = __to_int(data.get('%sDescription' % name, {}).get('fontSize'))
        adv.description.font.color = __to_color(data.get('%sDescription' % name, {}).get('fontColor'))
        adv.description.font.align = __to_str(data.get('%sDescription' % name, {}).get('align'))
        adv.description.font.weight = __to_int(data.get('%sDescription' % name, {}).get('fontBold'))
        adv.description.font.letter = __to_float(data.get('%sDescription' % name, {}).get('letter_spacing'))
        adv.description.font.line = __to_float(data.get('%sDescription' % name, {}).get('line_height'))
        adv.description.font.variant = __to_bool(data.get('%sDescription' % name, {}).get('font_variant'))
        adv.description.font.decoration = __to_bool(data.get('%sDescription' % name, {}).get('fontUnderline'))
        adv.description.font.family = __to_str(
            data.get('%sDescription' % name, {}).get('fontFamily', 'arial, sans serif'))
        hide_cost = __to_bool(data.get('%sCost' % name, {}).get('hide', False))
        if not hide_cost:
            adv.cost.width = __to_int(data.get('%sCost' % name, {}).get('width'))
            adv.cost.height = __to_int(data.get('%sCost' % name, {}).get('height'))
            adv.cost.top = __to_int(data.get('%sCost' % name, {}).get('top'))
            adv.cost.left = __to_int(data.get('%sCost' % name, {}).get('left'))
        adv.cost.font.size = __to_int(data.get('%sCost' % name, {}).get('fontSize'))
        adv.cost.font.color = __to_color(data.get('%sCost' % name, {}).get('fontColor'))
        adv.cost.font.align = __to_str(data.get('%sCost' % name, {}).get('align'))
        adv.cost.font.weight = __to_int(data.get('%sCost' % name, {}).get('fontBold'))
        adv.cost.font.letter = __to_float(data.get('%sCost' % name, {}).get('letter_spacing'))
        adv.cost.font.line = __to_float(data.get('%sCost' % name, {}).get('line_height'))
        adv.cost.font.variant = __to_bool(data.get('%sCost' % name, {}).get('font_variant'))
        adv.cost.font.decoration = __to_bool(data.get('%sCost' % name, {}).get('fontUnderline'))
        adv.cost.font.family = __to_str(data.get('%sCost' % name, {}).get('fontFamily', 'arial, sans serif'))
        hide_button = __to_bool(data.get('%sButton' % name, {}).get('hide', False))
        if not hide_button:
            adv.button.width = __to_int(data.get('%sButton' % name, {}).get('width'))
            adv.button.height = __to_int(data.get('%sButton' % name, {}).get('height'))
            adv.button.top = __to_int(data.get('%sButton' % name, {}).get('top'))
            adv.button.left = __to_int(data.get('%sButton' % name, {}).get('left'))
        adv.button.border = __to_int(data.get('%sButton' % name, {}).get('borderWidth'))
        adv.button.border_color = __to_color(data.get('%sButton' % name, {}).get('borderColor'))
        adv.button.border_radius = [
            __to_int(data.get('%sButton' % name, {}).get('border_top_left_radius')),
            __to_int(data.get('%sButton' % name, {}).get('border_top_right_radius')),
            __to_int(data.get('%sButton' % name, {}).get('border_bottom_right_radius')),
            __to_int(data.get('%sButton' % name, {}).get('border_bottom_left_radius'))
        ]
        adv.button.background_color = __to_color(data.get('%sButton' % name, {}).get('backgroundColor'))
        adv.button.font.size = __to_int(data.get('%sButton' % name, {}).get('fontSize'))
        adv.button.font.color = __to_color(data.get('%sButton' % name, {}).get('fontColor'))
        adv.button.font.align = __to_str(data.get('%sButton' % name, {}).get('align'))
        adv.button.font.weight = __to_int(data.get('%sButton' % name, {}).get('fontBold'))
        adv.button.font.letter = __to_float(data.get('%sButton' % name, {}).get('letter_spacing'))
        adv.button.font.line = __to_float(data.get('%sButton' % name, {}).get('line_height'))
        adv.button.font.variant = __to_bool(data.get('%sButton' % name, {}).get('font_variant'))
        adv.button.font.decoration = __to_bool(data.get('%sButton' % name, {}).get('fontUnderline'))
        adv.button.font.family = __to_str(
            data.get('%sButton' % name, {}).get('fontFamily', 'arial, sans serif'))
        hide_image = __to_bool(data.get('%sImage' % name, {}).get('hide', False))
        if not hide_image:
            adv.image.width = __to_int(data.get('%sImage' % name, {}).get('width'))
            adv.image.height = __to_int(data.get('%sImage' % name, {}).get('height'))
            adv.image.top = __to_int(data.get('%sImage' % name, {}).get('top'))
            adv.image.left = __to_int(data.get('%sImage' % name, {}).get('left'))
        adv.image.border = __to_int(data.get('%sImage' % name, {}).get('borderWidth'))
        adv.image.border_color = __to_color(data.get('%sImage' % name, {}).get('borderColor'))
        adv.image.border_radius = [
            __to_int(data.get('%sImage' % name, {}).get('border_top_left_radius')),
            __to_int(data.get('%sImage' % name, {}).get('border_top_right_radius')),
            __to_int(data.get('%sImage' % name, {}).get('border_bottom_right_radius')),
            __to_int(data.get('%sImage' % name, {}).get('border_bottom_left_radius'))
        ]
    except Exception as e:
        logger.error(exception_message(exc=str(e), data=data))
        raise
    return adv


def ad_style(data=None):
    adv_data = None
    if data is not None:
        try:
            adv_data = dict()
            block = BlockSetting()
            block.width = __to_int(data.get('Main', {}).get('width'))
            block.height = __to_int(data.get('Main', {}).get('height'))
            block.border = __to_int(data.get('Main', {}).get('borderWidth'))
            block.border_color = __to_color(data.get('Main', {}).get('borderColor'))
            background_color_transparent = data.get('Main', {}).get('backgroundColorStatus', True)
            block.background_color = 'transparent' if background_color_transparent else __to_color(
                data.get('Main', {}).get('backgroundColor')
            )
            block.border_radius = [
                __to_int(data.get('Main', {}).get('border_top_left_radius')),
                __to_int(data.get('Main', {}).get('border_top_right_radius')),
                __to_int(data.get('Main', {}).get('border_bottom_right_radius')),
                __to_int(data.get('Main', {}).get('border_bottom_left_radius'))
            ]

            block.default_button.block = __to_str(
                data.get('Button', {}).get('content', block.default_button.block))
            block.default_button.ret_block = __to_str(
                data.get('RetButton', {}).get('content', block.default_button.ret_block))
            block.default_button.rec_block = __to_str(
                data.get('RecButton', {}).get('content', block.default_button.rec_block))

            block.header.width = __to_int(data.get('MainHeader', {}).get('width'))
            block.header.height = __to_int(data.get('MainHeader', {}).get('height'))
            block.header.top = __to_int(data.get('MainHeader', {}).get('top'))
            block.header.left = __to_int(data.get('MainHeader', {}).get('left'))

            block.footer.width = __to_int(data.get('MainFooter', {}).get('width'))
            block.footer.height = __to_int(data.get('MainFooter', {}).get('height'))
            block.footer.top = __to_int(data.get('MainFooter', {}).get('top'))
            block.footer.left = __to_int(data.get('MainFooter', {}).get('left'))

            block.default_adv.count_adv = __to_int(data.get('Main', {}).get('itemsNumber'))

            adv_data['block'] = dict(block)
            adv_data['adv'] = dict()
            adv_data['adv']['Block'] = dict(create_adv_setting(data))
            adv_data['adv']['RetBlock'] = dict(create_adv_setting(data, 'Ret'))
            adv_data['adv']['RecBlock'] = dict(create_adv_setting(data, 'Rec'))
        except Exception as e:
            logger.error(exception_message(exc=str(e), data=data))
            raise
    return adv_data
