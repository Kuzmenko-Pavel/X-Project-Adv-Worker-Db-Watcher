from datetime import datetime


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
