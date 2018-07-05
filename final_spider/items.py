# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FinalSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CountryItem(scrapy.Item):
    country = scrapy.Field()


class LeagueItem(scrapy.Item):
    league = scrapy.Field()
    full_name = scrapy.Field()
    country = scrapy.Field()
    fid = scrapy.Field()


class SeasonTypeItem(scrapy.Item):
    type = scrapy.Field()


class SeasonSubTypeItem(scrapy.Item):
    sub_type = scrapy.Field()


class SeasonItem(scrapy.Item):
    game_week = scrapy.Field()
    start_time = scrapy.Field()
    team_a = scrapy.Field()
    team_b = scrapy.Field()
    score_a = scrapy.Field()
    score_b = scrapy.Field()
    status = scrapy.Field()
    league_name = scrapy.Field()
    type_name = scrapy.Field()
    sub_type_name = scrapy.Field()
    fid = scrapy.Field()
    year = scrapy.Field()


class SeasonRealItem(scrapy.Item):
    game_week = scrapy.Field()
    start_time = scrapy.Field()
    team_a = scrapy.Field()
    team_b = scrapy.Field()
    score_a = scrapy.Field()
    score_b = scrapy.Field()
    status = scrapy.Field()
    league_name = scrapy.Field()
    type_name = scrapy.Field()
    sub_type_name = scrapy.Field()
    fid = scrapy.Field()


class SeasonOldItem(scrapy.Item):
    score_a = scrapy.Field()
    score_b = scrapy.Field()
    status = scrapy.Field()
    fid = scrapy.Field()


class TeamItem(scrapy.Item):
    team_fid = scrapy.Field()
    team_name = scrapy.Field()
    team_name_en = scrapy.Field()
    team_nickname = scrapy.Field()
    team_icon = scrapy.Field()
    icon_url = scrapy.Field()
    team_createdate = scrapy.Field()
    team_addr = scrapy.Field()
    team_chief_coach = scrapy.Field()
    team_home = scrapy.Field()
    team_home_count = scrapy.Field()
    team_web = scrapy.Field()
    team_email = scrapy.Field()
    team_country = scrapy.Field()
    team_city = scrapy.Field()
    team_price = scrapy.Field()
    team_best = scrapy.Field()


class ScoreItem(scrapy.Item):
    type_name = scrapy.Field()
    team_name = scrapy.Field()
    season_count = scrapy.Field()
    season_vicotry = scrapy.Field()
    season_deuce = scrapy.Field()
    season_lose = scrapy.Field()
    season_in = scrapy.Field()
    season_out = scrapy.Field()
    season_win = scrapy.Field()
    avg_vicotry = scrapy.Field()
    avg_lose = scrapy.Field()
    probability_vicotry = scrapy.Field()
    probability_deuce = scrapy.Field()
    probability_lose = scrapy.Field()
    season_source = scrapy.Field()
    league_name = scrapy.Field()
    league_year = scrapy.Field()


class ScoreSportsmanItem(scrapy.Item):
    type_name = scrapy.Field()
    league_name = scrapy.Field()
    league_year = scrapy.Field()
    sp_id = scrapy.Field()
    team_id = scrapy.Field()
    season_count = scrapy.Field()
    avg_vicotry = scrapy.Field()


class SportsmanItem(scrapy.Item):
    sports_fid = scrapy.Field()
    league_sports_name = scrapy.Field()
    league_sports_name_en = scrapy.Field()
    league_sports_nickname = scrapy.Field()
    league_sports_number = scrapy.Field()
    league_sports_role = scrapy.Field()
    league_sports_country = scrapy.Field()
    league_sports_img = scrapy.Field()
    icon_url = scrapy.Field()
    league_sports_birthday = scrapy.Field()
    league_sports_stature = scrapy.Field()
    league_sports_weight = scrapy.Field()
    league_sports_price = scrapy.Field()
    league_sports_retire_date = scrapy.Field()


class RelationItem(scrapy.Item):
    team_fid = scrapy.Field()
    sports_fid = scrapy.Field()
    sports_role = scrapy.Field()


class OddsItem(scrapy.Item):
    season_fid = scrapy.Field()
    group_name = scrapy.Field()
    league_name = scrapy.Field()
    league_win = scrapy.Field()
    league_deuce = scrapy.Field()
    league_lose = scrapy.Field()
    league_final_win = scrapy.Field()
    league_final_deuce = scrapy.Field()
    league_final_lose = scrapy.Field()
    league_odds = scrapy.Field()
    league_odds_up = scrapy.Field()
    league_odds_down = scrapy.Field()
    league_final_odds = scrapy.Field()
    league_final_odds_up = scrapy.Field()
    league_final_odds_down = scrapy.Field()


class TechniqueItem(scrapy.Item):
    # 技术统计
    season_fid = scrapy.Field()
    league_jishu_name = scrapy.Field()
    league_jishu_team_a = scrapy.Field()
    league_jishu_team_b = scrapy.Field()
    league_jishu_team_a_fs = scrapy.Field()
    league_jishu_team_b_fs = scrapy.Field()


class PlanItem(scrapy.Item):
    season_fid = scrapy.Field()
    type = scrapy.Field()
    plan = scrapy.Field()


class PlanRelationItem(scrapy.Item):
    season_fid = scrapy.Field()
    type = scrapy.Field()
    sports_fid = scrapy.Field()
    status_id = scrapy.Field()


class EventItem(scrapy.Item):
    season_fid = scrapy.Field()
    is_home = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    content = scrapy.Field()


class EventRealItem(scrapy.Item):
    season_fid = scrapy.Field()
    is_home = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    content = scrapy.Field()


class LotteryItem(scrapy.Item):
    issue = scrapy.Field()
    mid = scrapy.Field()
    league = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    home = scrapy.Field()
    customer = scrapy.Field()
    result = scrapy.Field()
    full = scrapy.Field()
    type_id = scrapy.Field()


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    st = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    img = scrapy.Field()


class SeasonTime(scrapy.Item):
    fid = scrapy.Field()
    playing = scrapy.Field()


class SportteryItem(scrapy.Item):
    id = scrapy.Field()
    week = scrapy.Field()
    num = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    b_date = scrapy.Field()
    status = scrapy.Field()
    hot = scrapy.Field()
    l_id = scrapy.Field()
    l_cn = scrapy.Field()
    h_id = scrapy.Field()
    h_cn = scrapy.Field()
    a_id = scrapy.Field()
    a_cn = scrapy.Field()
    index_show = scrapy.Field()
    show = scrapy.Field()
    l_cn_abbr = scrapy.Field()
    h_cn_abbr = scrapy.Field()
    a_cn_abbr = scrapy.Field()
    h_order = scrapy.Field()
    a_order = scrapy.Field()
    h_id_dc = scrapy.Field()
    a_id_dc = scrapy.Field()
    l_background_color = scrapy.Field()
    weather = scrapy.Field()
    weather_city = scrapy.Field()
    temperature = scrapy.Field()
    weather_pic = scrapy.Field()
    last_updated = scrapy.Field()


class InfoItem(scrapy.Item):
    id = scrapy.Field()
    a = scrapy.Field()
    d = scrapy.Field()
    h = scrapy.Field()
    type_id = scrapy.Field()
    goalline = scrapy.Field()
    p_code = scrapy.Field()
    o_type = scrapy.Field()
    p_id = scrapy.Field()
    p_status = scrapy.Field()
    single = scrapy.Field()
    allup = scrapy.Field()
    fixedodds = scrapy.Field()
    cbt = scrapy.Field()
    int = scrapy.Field()
    vbt = scrapy.Field()
    h_trend = scrapy.Field()
    a_trend = scrapy.Field()
    d_trend = scrapy.Field()
    l_trend = scrapy.Field()
    expand = scrapy.Field()


class MatchInfoItem(scrapy.Item):
    id = scrapy.Field()
    m_id = scrapy.Field()
    i_id = scrapy.Field()
    prompt = scrapy.Field()
    checked = scrapy.Field()
