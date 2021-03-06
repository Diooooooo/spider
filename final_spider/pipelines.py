# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class FinalSpiderPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    def process_item(self, item, spider):
        if item.__class__.__name__ == "SeasonItem":
            query = self.dbpool.runInteraction(self._conditional_insert, item)
        elif item.__class__.__name__ == "SeasonRealItem":
            query = self.dbpool.runInteraction(self._conditional_insert_real, item)
        elif item.__class__.__name__ == "SeasonOldItem":
            query = self.dbpool.runInteraction(self._conditional_insert_old, item)
        elif item.__class__.__name__ == "TeamItem":
            query = self.dbpool.runInteraction(self._conditional_team, item)
        elif item.__class__.__name__ == "ScoreItem":
            query = self.dbpool.runInteraction(self._conditional_score, item)
        elif item.__class__.__name__ == "ScoreSportsmanItem":
            query = self.dbpool.runInteraction(self._conditional_scoreSportsman, item)
        elif item.__class__.__name__ == "SportsmanItem":
            query = self.dbpool.runInteraction(self._conditional_sportsman, item)
        elif item.__class__.__name__ == "RelationItem":
            query = self.dbpool.runInteraction(self._conditional_relation, item)
        elif item.__class__.__name__ == "OddsItem":
            query = self.dbpool.runInteraction(self._conditional_ouzhi, item)
        elif item.__class__.__name__ == "PlanItem":
            query = self.dbpool.runInteraction(self._conditional_zhenx, item)
        elif item.__class__.__name__ == 'PlanRelationItem':
            query = self.dbpool.runInteraction(self._conditional_zhenx_relation, item)
        elif item.__class__.__name__ == 'TechniqueItem':
            query = self.dbpool.runInteraction(self._conditional_jishu, item)
        elif item.__class__.__name__ == 'EventItem':
            query = self.dbpool.runInteraction(self._conditional_event, item)
        elif item.__class__.__name__ == 'EventRealItem':
            query = self.dbpool.runInteraction(self._conditional_event_real, item)
        elif item.__class__.__name__ == 'CountryItem':
            query = self.dbpool.runInteraction(self._conditional_country, item)
        elif item.__class__.__name__ == 'LeagueItem':
            query = self.dbpool.runInteraction(self._conditional_league, item)
        elif item.__class__.__name__ == 'SeasonTypeItem':
            query = self.dbpool.runInteraction(self._conditional_season_type, item)
        elif item.__class__.__name__ == 'SeasonSubTypeItem':
            query = self.dbpool.runInteraction(self._conditional_season_sub_type, item)
        elif item.__class__.__name__ == 'LotteryItem':
            query = self.dbpool.runInteraction(self._conditional_lottery, item)
        elif item.__class__.__name__ == 'NewsItem':
            query = self.dbpool.runInteraction(self._conditional_news, item)
        elif item.__class__.__name__ == 'SeasonTime':
            query = self.dbpool.runInteraction(self._conditional_time, item)
        elif item.__class__.__name__ == 'SportteryItem':
            query = self.dbpool.runInteraction(self._conditional_sporttery, item)
        elif item.__class__.__name__ == 'InfoItem':
            query = self.dbpool.runInteraction(self._conditional_had, item)
        elif item.__class__.__name__ == 'MatchInfoItem':
            query = self.dbpool.runInteraction(self._conditional_matchInfo, item)
        elif item.__class__.__name__ == 'SportteryResult':
            query = self.dbpool.runInteraction(self._conditional_sportteryResult, item)
        elif item.__class__.__name__ == 'LottoResult':
            query = self.dbpool.runInteraction(self._conditional_lottoResult, item)
        elif item.__class__.__name__ == 'LottoResultItem':
            query = self.dbpool.runInteraction(self._conditional_lottoResultItem, item)

        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_country(self, tx, item):
        tx.execute('INSERT INTO qsr_league_country(country_name) VALUES(\"' + item['country']
                   + '\") ON DUPLICATE KEY UPDATE country_name=country_name')

    def _conditional_time(self, tx, item):
        update = 'UPDATE qsr_team_season s SET s.season_playing_time = "' \
                 + str(item['playing']) + '" WHERE s.season_fid = "' + str(item['fid']) + '"'
        tx.execute(update)

    def _conditional_league(self, tx, item):
        tx.execute('INSERT INTO qsr_league(country_id ,lea_name ,lea_full_name, lea_fid) '
                   'SELECT IFNULL(c.country_id, 0), i.league, i.full_name, i.fid '
                   'FROM (SELECT "' + item['country'] + '" AS country, "' + item['league'] + '" AS league, "'
                   + item['full_name'] + '" AS full_name, "' + item['fid'] + '" AS fid) i '
                                                                             'LEFT JOIN qsr_league_country c ON '
                                                                             'c.country_name = i.country '
                                                                             'ON DUPLICATE KEY UPDATE country_id = '
                                                                             'IFNULL(c.country_id, 0), lea_name = '
                                                                             'i.league, '
                                                                             'lea_full_name = i.full_name')

    def _conditional_season_type(self, tx, item):
        tx.execute('INSERT INTO qsr_team_season_type(type_name) VALUES(\"' + item['type']
                   + '\") ON DUPLICATE KEY UPDATE type_name=type_name')

    def _conditional_season_sub_type(self, tx, item):
        tx.execute('INSERT INTO qsr_team_season_sub_type(sub_type_name) VALUES(\"' + item['sub_type']
                   + '\") ON DUPLICATE KEY UPDATE sub_type_name = sub_type_name')

    def _conditional_team(self, tx, item):
        year = item['team_createdate']
        if '年' in year:
            year = str.replace(year, '年', '-')
        if '月' in year:
            year = str.replace(year, '月', '-')
        if '日' in year:
            year = str.replace(year, '日', '')

        count = item['team_home_count']
        if '人' in count:
            count = count[:-1]

        if len(count) == 0:
            count = '0'

        if len(year) > 1:
            # if len(year.split('-')) == 3:
            #     year = year + '00'
            # elif len(year.split('-')) == 2:
            if len(year.split('-')) == 2:
                year = year + '00-00'
            elif len(year.split('-')) == 1:
                year = year + '-00-00'

        insertInto = "INSERT INTO qsr_team (team_name,team_name_en,team_icon,team_createdate," \
                     "team_home,team_home_count,team_country, country_id, team_city,team_price, team_fid) " \
                     "SELECT i.team_name, i.team_name_en, " \
                     "i.team_icon_file_id, i.team_createdate, i.team_home, " \
                     "i.team_home_count, i.team_country, IFNULL(l.country_id, 0), i.team_city, i.team_price, i.team_fid " \
                     "FROM (SELECT \"" + item['team_name'] + "\" AS team_name, \"" + \
                     item['team_name_en'] + "\" AS team_name_en, \"" + item[
                         'icon_url'] + "\" AS team_icon_file_id, \"" + \
                     year + "\" AS team_createdate, \"" + item['team_home'] + \
                     "\" AS team_home, \"" + count + "\" AS team_home_count, \"" + item['team_country'] + \
                     "\" as team_country, \"" + item['team_city'] + "\" AS team_city, \"" + item['team_price'] + \
                     "\" AS team_price, \"" + str(item['team_fid']) + "\" AS team_fid) i " \
                                                                      "LEFT JOIN qsr_league_country l on l.country_name = i.team_country " \
                                                                      "ON DUPLICATE KEY UPDATE team_home = i.team_home, team_name = i.team_name, " \
                                                                      "team_name_en = i.team_name_en,team_icon = i.team_icon_file_id, " \
                                                                      "team_createdate = i.team_createdate, team_home_count= i.team_home_count, " \
                                                                      "team_city = i.team_city, team_price = i.team_price, country_id = IFNULL(l.country_id, 0)"
        if len(year) == 0:
            insertInto = "INSERT INTO qsr_team (team_name,team_name_en,team_icon," \
                         "team_home,team_home_count,team_country,team_city,team_price, team_fid) SELECT i.team_name, i.team_name_en, " \
                         "i.team_icon_file_id, i.team_home, " \
                         "i.team_home_count, i.team_country, i.team_city, i.team_price, i.team_fid " \
                         "FROM (SELECT \"" + item['team_name'] + "\" AS team_name, \"" + \
                         item['team_name_en'] + "\" AS team_name_en, \"" + item[
                             'icon_url'] + "\" AS team_icon_file_id, " \
                                           "\"" + item[
                             'team_home'] + "\" AS team_home, \"" + count + "\" AS team_home_count, \"" + item[
                             'team_country'] + \
                         "\" as team_country, \"" + item['team_city'] + "\" AS team_city, \"" + item['team_price'] + \
                         "\" AS team_price, \"" + str(item['team_fid']) + "\" AS team_fid) i " \
                                                                          "LEFT JOIN qsr_league_country l on l.country_name = i.team_country " \
                                                                          "ON DUPLICATE KEY UPDATE team_name = i.team_name, team_name_en = i.team_name_en, " \
                                                                          "team_icon = i.team_icon_file_id, team_home = i.team_home, team_home_count = i.team_home_count," \
                                                                          "team_country = i.team_country, team_city = i.team_city, team_price = i.team_price, country_id = IFNULL(l.country_id, 0)"
        tx.execute(insertInto)

    def _conditional_insert(self, tx, item):
        insertInto = "INSERT INTO qsr_team_season(lea_id, season_start_play_time, season_team_a, season_team_b, " \
                     "season_gameweek, season_fs_a, season_fs_b, season_year, season_home_team_id, status_id, " \
                     "type_id, sub_type_id, season_fid) SELECT l.lea_id, i.play_time, ta.team_id, tb.team_id, i.gameweek, " \
                     "i.fs_a, i.fs_b, i.year_, ta.team_id, i.status_name, IFNULL(t.type_id, -1), IFNULL(st.sub_type_id, -1), i.season_fid FROM " \
                     "(SELECT \"" + item['league_name'] + "\" AS leaName, \"" + \
                     item['start_time'] + "\" AS play_time, \"" + item['team_a'] + "\" AS team_a, ""\"" + \
                     item['team_b'] + "\" AS team_b, \"" + item['game_week'] + "\" AS gameweek, \"" + \
                     str(item['score_a']) + "\" AS fs_a, \"" + str(item['score_b']) + "\" AS fs_b, \"" + \
                     item['year'] + "\" AS year_, \"" + str(item['status']) + "\" AS status_name, \"" + \
                     item['type_name'] + "\" AS type_name, \"" + item['sub_type_name'] + "\" AS sub_type_name, \"" + \
                     item['fid'] + "\" AS season_fid) i " \
                                  "INNER JOIN qsr_team ta ON ta.team_name = i.team_a " \
                                  "INNER JOIN qsr_team tb ON tb.team_name = i.team_b " \
                                  "LEFT JOIN qsr_team_season_type t ON t.type_name = i.type_name " \
                                  "LEFT JOIN qsr_team_season_sub_type st ON st.sub_type_name = i.sub_type_name " \
                                  "LEFT JOIN qsr_league l ON l.lea_name = i.leaName AND l.enabled = 1 " \
                                  "ON DUPLICATE KEY UPDATE lea_id = IFNULL(l.lea_id, qsr_team_season.lea_id), season_start_play_time = IFNULL(i.play_time, season_start_play_time), " \
                                  "season_team_a=IFNULL(ta.team_id, season_team_a), season_team_b = IFNULL(tb.team_id, season_team_b), season_gameweek = IFNULL(i.gameweek, season_gameweek), " \
                                  "season_fs_a = IFNULL(i.fs_a, season_fs_a), season_fs_b = IFNULL(i.fs_b, season_fs_b), season_year = IFNULL(i.year_, season_year), " \
                                  "season_home_team_id = IFNULL(ta.team_id, season_home_team_id), status_id = IFNULL(i.status_name, status_id)"
        tx.execute(insertInto)

    def _conditional_insert_real(self, tx, item):
        insertInto = "UPDATE qsr_team_season s " \
                     "INNER JOIN (SELECT \"" + item['start_time'] + "\" AS play_time, \"" \
                     + item['team_a'] + "\" AS team_a, \"" + item['team_b'] + "\" AS team_b, \"" \
                     + str(item['status']) + "\" AS status_name, \"" + item['fid'] + "\" AS season_fid, \"" \
                     + str(item['score_a']) + "\" AS fs_a, \"" + str(item['score_b']) + "\" AS fs_b" \
                     ") i ON s.season_fid = i.season_fid " \
                     "INNER JOIN qsr_team a ON i.team_a = a.team_name AND s.season_team_a = a.team_id " \
                     "INNER JOIN qsr_team b ON i.team_b = b.team_name AND s.season_team_b = b.team_id " \
                     "SET s.status_id = i.status_name, " \
                     "season_fs_a = i.fs_a, season_fs_b = i.fs_b"
        tx.execute(insertInto)

    def _conditional_insert_old(self, tx, item):
        old = 'UPDATE qsr_team_season s INNER JOIN (SELECT ' + str(item['fid']) + ' AS fid, ' \
              + str(item['score_a']) + ' AS sa, ' + str(item['score_b']) + ' AS sb, ' \
              + str(item['status']) + ' AS status_id) i ' \
              'ON s.season_fid = i.fid SET s.season_fs_a = i.sa, s.season_fs_b = i.sb, s.status_id = i.status_id'
        tx.execute(old)

    def _conditional_score(self, tx, item):
        insertInto = "INSERT INTO qsr_team_season_ranking_list_item (type_id ,league_id ,league_year ,team_id ," \
                     "item_count ,item_vicotry ,item_deuce ,item_lose ,item_in ,item_out ,item_win ,item_avg_vicotry ," \
                     "item_avg_lose,item_probability_vicotry,item_probability_deuce,item_probability_lose,item_source) " \
                     "SELECT lt.type_id, l.lea_id, i.league_year, t.team_id, i.team_count, i.vicotry, i.deuce, " \
                     "i.lose, i.team_in, i.team_out, i.win, i.avg_vicotry, i.avg_lose, i.p_v, i.p_d, i.p_l, " \
                     "i.team_source FROM (SELECT \"" + item['type_name'] + "\" AS type_name, \"" + item[
                         'league_name'] + "\" AS league_name, \"" + item['league_year'] + "\" AS league_year, \"" + \
                     item[
                         'team_name'] + "\" AS team_name, \"" + item['season_count'] + "\" AS team_count, \"" + item[
                         'season_vicotry'] + "\" AS vicotry, \"" + item['season_deuce'] + "\" AS deuce, \"" + item[
                         'season_lose'] + "\" AS lose, \"" + item['season_in'] + "\" AS team_in, \"" + item[
                         'season_out'] + "\" AS team_out, \"" + item['season_win'] + "\" AS win, \"" + \
                     item['avg_vicotry'] + "\" AS avg_vicotry, \"" + item['avg_lose'] + "\" AS avg_lose, \"" \
                     + item['probability_vicotry'] + "\" as p_v, \"" + item['probability_deuce'] + "\" AS p_d, \"" \
                     + item['probability_lose'] + "\" AS p_l, \"" + item['season_source'] + "\" AS team_source) i " \
                    "INNER JOIN qsr_league l ON l.lea_name = i.league_name " \
                    "INNER JOIN qsr_team t ON t.team_name = i.team_name " \
                    "INNER JOIN qsr_team_season_ranking_list_type lt ON lt.type_name = i.type_name " \
                    "ON DUPLICATE KEY UPDATE item_count = i.team_count, item_vicotry = i.vicotry, " \
                    "item_deuce = i.deuce, item_lose = i.lose, item_in = i.team_in, item_out = i.team_out, " \
                    "item_win = i.win, item_avg_vicotry = i.avg_vicotry, item_avg_lose = i.avg_lose, " \
                    "item_probability_vicotry = i.p_v, item_probability_deuce = i.p_d, " \
                    "item_probability_lose = i.p_l, item_source = i.team_source "
        modify_league = "UPDATE qsr_league e SET e.is_score = 1 WHERE e.lea_name = \"" + item['league_name'] + "\""
        tx.execute(insertInto)
        tx.execute(modify_league)

    def _conditional_scoreSportsman(self, tx, item):
        inertInto = 'INSERT INTO qsr_team_season_ranking_list_item(type_id, league_id, ' \
                    'league_year, team_id, item_count, item_avg_vicotry) ' \
                    'SELECT i.type_id, l.lea_id, i.league_year, t.team_id, i.item_count, i.item_avg_vicotry ' \
                    'FROM (SELECT "' + str(item['type_name']) + '" AS type_id, "' + \
                    str(item['league_name']) +'" AS league_name, "' + str(item['league_year']) + '" AS league_year, "' + \
                    str(item['team_id']) + '" AS team_id, "' + str(item['season_count']) + '" AS item_count, "' + \
                    str(item['avg_vicotry']) + '" AS item_avg_vicotry) i ' \
                    'INNER JOIN qsr_league l on i.league_name = l.lea_name ' \
                    'INNER JOIN qsr_team t ON i.team_id = t.team_fid ' \
                    'INNER JOIN qsr_team_season_ranking_list_type lt ON i.type_id = lt.type_id ' \
                    'ON DUPLICATE KEY UPDATE item_count = i.item_count, item_avg_vicotry = i.item_avg_vicotry'
        tx.execute(inertInto)

    def _conditional_sportsman(self, tx, item):
        number = item['league_sports_number']
        if '号' in number:
            number = number[:-1]
        insertInto = "INSERT INTO qsr_team_sportsman (sports_name,sports_name_en,sports_nickname,sports_number,role_id," \
                     "sports_country,sports_img,sports_birthday,sports_stature,sports_weight,sports_price, sports_fid, country_id) " \
                     "SELECT i.sport_name, i.spsort_name_en, i.sports_nickname, i.sports_number, r.role_id, " \
                     "i.sports_country, i.img_file, i.birthday, i.stature, i.weight, i.price, i.sports_fid, IFNULL(l.country_id, 0) " \
                     "FROM (SELECT \"" + item['league_sports_name'] + "\" AS sport_name, \"" + item[
                         'league_sports_name_en'] \
                     + "\" AS spsort_name_en, \"" + item['league_sports_name'] + "\" AS sports_nickname, \"" \
                     + number + "\" AS sports_number, \"" + item['league_sports_role'] + "\" AS role_name, \"" \
                     + item['league_sports_country'] + "\" AS sports_country, \"" + item[
                         'league_sports_img'] + "\" AS img_file, \"" \
                     + item['league_sports_birthday'] + "\" AS birthday, \"" + item[
                         'league_sports_stature'] + "\" AS stature, \"" \
                     + item['league_sports_weight'] + "\" AS weight, \"" + item[
                         'league_sports_price'] + "\" AS price, \"" + item['sports_fid'] + "\" as sports_fid) i " \
                                                                                           "INNER JOIN qsr_team_sportsman_role r ON r.role_name = i.role_name " \
                                                                                           "LEFT JOIN qsr_league_country l ON l.country_name = i. sports_country " \
                                                                                           "ON DUPLICATE KEY UPDATE sports_name = i.sport_name, sports_name_en = i.spsort_name_en, " \
                                                                                           "sports_nickname = i.sports_nickname, sports_number = i.sports_number, sports_country = i.sports_country," \
                                                                                           "sports_img = i.img_file, sports_birthday = i.birthday, sports_stature = i.stature, sports_weight = i.weight," \
                                                                                           "sports_price = i.price, role_id = r.role_id, country_id = IFNULL(l.country_id, 0)"
        tx.execute(insertInto)

    def _conditional_relation(self, tx, item):
        relation = "INSERT INTO qsr_team_sportsman_relation (team_id,sports_id,role_id) " \
                   "SELECT t.team_id, s.sports_id, r.role_id " \
                   "FROM (SELECT \"" + item['team_fid'] + "\" AS team_fid, \"" \
                   + item['sports_fid'] + "\" AS sports_fid, \"" + item['sports_role'] + "\" AS role_name) i " \
                                                                                         "INNER JOIN qsr_team_sportsman_role r ON r.role_name = i.role_name " \
                                                                                         "INNER JOIN qsr_team t ON t.team_fid = i.team_fid " \
                                                                                         "INNER JOIN qsr_team_sportsman s ON s.sports_fid = i.sports_fid "
        tx.execute(relation)

    def _conditional_ouzhi(self, tx, item):
        insertInto = "INSERT INTO qsr_team_season_lottery_logs( season_id ,type_id ,lottery_win ,lottery_deuce ," \
                     "lottery_lose ,final_win ,final_deuce ,final_lose ) " \
                     "SELECT s.season_id, t.type_id, i.lottery_win, i.lottery_deuce, " \
                     "i.lottery_lose, i.final_win, i.final_deuce, i.final_lose " \
                     "FROM (SELECT \"" + item['league_name'] + "\" AS type_name, \"" \
                     + item['group_name'] + "\" AS group_name, \"" \
                     + item['season_fid'] + "\" AS season_id, \"" + item['league_win'] + "\" AS lottery_win, \"" \
                     + item['league_deuce'] + "\" AS lottery_deuce, \"" + item['league_lose'] + "\" AS lottery_lose, \"" \
                     + item['league_final_win'] + "\" AS final_win, \"" + item[
                         'league_final_deuce'] + "\" AS final_deuce, \"" \
                     + item['league_final_lose'] + "\" AS final_lose) i " \
                                                   "INNER JOIN qsr_team_season s on i.season_id = s.season_fid " \
                                                   "INNER JOIN qsr_team_season_lottery_group g ON g.group_name = i.group_name " \
                                                   "INNER JOIN qsr_team_season_lottery_type t ON t.type_name = i.type_name AND g.group_id = t.group_id " \
                                                   "ON DUPLICATE KEY UPDATE lottery_win = i.lottery_win, lottery_deuce = i.lottery_deuce, " \
                                                   "lottery_lose = i.lottery_lose, final_win = i.final_win, final_deuce = i.final_deuce, final_lose = i.final_lose"
        tx.execute(insertInto)

    def _conditional_jishu(self, tx, item):
        insertInto = "INSERT INTO qsr_team_season_technique(season_id,type_id,team_a,score_a,team_b,score_b) " \
                     "SELECT s.season_id, t.type_id, a.team_id, i.score_a, b.team_id, i.score_b " \
                     "FROM (SELECT \"" + item['season_fid'] + "\" AS fid, \"" + item['league_jishu_name'] + \
                     "\" AS type_name, \"" + item['league_jishu_team_a'] + "\" AS team_a, \"" + item[
                         'league_jishu_team_b'] + \
                     "\" AS team_b, \"" + item['league_jishu_team_a_fs'] + "\" AS score_a, \"" + item[
                         'league_jishu_team_b_fs'] \
                     + "\" AS score_b) i " \
                       "INNER JOIN qsr_team_season_technique_type t ON i.type_name = t.type_name " \
                       "INNER JOIN qsr_team_season s ON s.season_fid = i.fid " \
                       "INNER JOIN qsr_team a ON a.team_name = i.team_a " \
                       "INNER JOIN qsr_team b ON b.team_name = i.team_b " \
                       "ON DUPLICATE KEY UPDATE score_a = IFNULL(i.score_a, qsr_team_season_technique.score_a), score_b = IFNULL(i.score_b, qsr_team_season_technique.score_b)"
        tx.execute(insertInto)

    def _conditional_zhenx(self, tx, item):
        insertInto = "INSERT INTO qsr_team_season_plan ( season_id ,team_id ,plan_name) " \
                     "SELECT s.season_id, IF('left' = i.type_, s.season_team_a, s.season_team_b) team_id, i.plan_name " \
                     "FROM (SELECT \"" + item['season_fid'] + "\" AS fid, \"" + item['type'] + "\" AS type_, \"" \
                     + item['plan'] + "\" AS plan_name) i INNER JOIN qsr_team_season s ON s.season_fid = i.fid" \
                                      " ON DUPLICATE KEY UPDATE plan_name = i.plan_name "
        tx.execute(insertInto)

    def _conditional_zhenx_relation(self, tx, item):
        insertInto = "INSERT INTO qsr_team_season_plan_item ( plan_id ,sportsman_id ,team_id, status_id, enabled) " \
                     "SELECT p.plan_id, m.sports_id, p.team_id, i.status_id, 1 " \
                     "FROM (SELECT \"" + item['season_fid'] + "\" AS fid, \"" \
                     + item['sports_fid'] + "\" AS si_fid, \"" + item['type'] + "\" AS type_, \"" \
                     + item['status_id'] + "\" AS status_id) i " \
                                           "INNER JOIN qsr_team_season s ON i.fid = s.season_fid " \
                                           "INNER JOIN qsr_team_sportsman m ON m.sports_fid = i.si_fid " \
                                           "INNER JOIN qsr_team_season_plan p ON p.season_id = s.season_id " \
                                           "AND p.team_id = IF(i.type_ = 'left', s.season_team_a, s.season_team_b) " \
                                           "ON DUPLICATE KEY UPDATE status_id = i.status_id, enabled = IF(" \
                                           "qsr_team_season_plan_item.item_id, 1, 0) "
        tx.execute(insertInto)

    def _conditional_event_real(self, tx, item):
        real = "UPDATE qsr_team_season_event_temp e INNER JOIN qsr_team_season s ON e.season_id = s.season_id " \
               "SET e.enabled = 0 WHERE s.season_fid = " + item['season_fid']
        tx.execute(real)

    def _conditional_event(self, tx, item):
        if 'player-change' == item['type']:
            if '-' in item['content'].split('~')[0]:
                sp_in = item['content'].split('~')[0].split('-')[0]
                name = item['content'].split('~')[0].split('-')[1]
            else:
                sp_in = '0'
                name = item['content'].split('~')[0]
            if '-' in item['content'].split('~')[1]:
                sp_out = item['content'].split('~')[1].split('-')[0]
                name_out = item['content'].split('~')[1].split('-')[1]
            else:
                sp_out = '0'
                name_out = item['content'].split('~')[1]
            insertInto = "INSERT INTO qsr_team_season_event_temp(season_id, team_id, sportsman_id_in, start_time, type_id, " \
                         "sportsman_name_in, sportsman_id_out, sportsman_name_out, enabled) " \
                         "SELECT s.season_id, IF(i.is_home = 1, s.season_team_a, s.season_team_b), " \
                         "IFNULL(ts.sports_id, 0), i.start_time, t.type_id, " \
                         "IFNULL(ts.sports_name, i.sportsman_name_in), IFNULL(ts2.sports_id, 0), " \
                         "IFNULL(ts2.sports_name, i.sportsman_name_out), 1 " \
                         "FROM (SELECT \"" + item['season_fid'] + "\" AS season_fid, \"" \
                         + item['type'] + "\" AS type_name, \"" + str(item['time']) + "\" AS start_time, \"" \
                         + str(item['is_home']) + "\" AS is_home, \"" + str(sp_in) + "\" AS sp_in, \"" \
                         + str(name) + "\" AS sportsman_name_in, \"" + str(sp_out) + "\" AS sp_out, \"" \
                         + str(name_out) + "\" as sportsman_name_out) i " \
                                           "INNER JOIN qsr_team_season_event_type t ON i.type_name = t.type_name_en " \
                                           "INNER JOIN qsr_team_season s ON i.season_fid = s.season_fid " \
                                           "LEFT JOIN qsr_team_sportsman ts ON ts.sports_fid = i.sp_in " \
                                           "LEFT JOIN qsr_team_sportsman ts2 ON ts2.sports_fid = i.sp_out " \
                                           "ON DUPLICATE KEY UPDATE sportsman_id_in = IFNULL(ts.sports_id, " \
                                           "sportsman_id_in)" \
                                           ", sportsman_name_in = IFNULL(ts.sports_name, i.sportsman_name_in)," \
                                           "sportsman_id_out = IFNULL(ts2.sports_id, 0), " \
                                           "sportsman_name_out = IFNULL(ts2.sports_name, i.sportsman_name_out), " \
                                           "enabled = IF(qsr_team_season_event_temp.event_id, 1, 0) "
            tx.execute(insertInto)
        else:
            if '-' in item['content']:
                sp_in = item['content'].split('-')[0]
                name = item['content'].split('-')[1]
            else:
                sp_in = '0'
                name = item['content']
            insertIntoIn = "INSERT INTO qsr_team_season_event_temp(season_id, team_id, sportsman_id_in, start_time, " \
                           "type_id, sportsman_name_in, enabled) " \
                           "SELECT s.season_id, IF(i.is_home = 1, s.season_team_a, s.season_team_b), " \
                           "IFNULL(ts.sports_id, 0), i.start_time, t.type_id, " \
                           "IFNULL(ts.sports_name, i.sportsman_name_in), 1 " \
                           "FROM (SELECT \"" + str(item['season_fid']) + "\" AS season_fid, \"" \
                           + str(item['type']) + "\" AS type_name, \"" + str(item['time']) + "\" AS start_time, \"" \
                           + str(item['is_home']) + "\" AS is_home, \"" + str(sp_in) + "\" AS sp_in, \"" \
                           + str(name) + "\" AS sportsman_name_in) i " \
                                         "INNER JOIN qsr_team_season_event_type t ON i.type_name = t.type_name_en " \
                                         "INNER JOIN qsr_team_season s ON i.season_fid = s.season_fid " \
                                         "LEFT JOIN qsr_team_sportsman ts ON ts.sports_fid = i.sp_in " \
                                         "ON DUPLICATE KEY UPDATE sportsman_id_in = IFNULL(ts.sports_id, " \
                                         "sportsman_id_in)" \
                                         ", sportsman_name_in = IFNULL(ts.sports_name, i.sportsman_name_in), " \
                                         "enabled = IF(qsr_team_season_event_temp.event_id, 1, 0) "
            tx.execute(insertIntoIn)

    def _conditional_lottery(self, tx, item):
        insertInto = 'INSERT INTO qsr_team_season_sporttery(fid,sporttery_issue,league_id,season_id, status_id, type_id) ' \
                     'SELECT i.fid, i.sporttery_issue, l.lea_id, s.season_id, i.status_id, i.type_id ' \
                     'FROM (SELECT "' + str(item['mid']) + '" AS fid, "' + str(item['issue']) + '" AS sporttery_issue, ' \
                                                                                                '"' + item[
                         'league'] + '" AS league, "' + item['home'] + '" AS home, "' \
                     + item['customer'] + '" AS customer, "' + item['date'] + '" AS _date, "' \
                     + item['time'] + '" AS _time, "' + str(item['result']) + '" AS status_id, "' + str(
            item['type_id']) + '" AS type_id) i ' \
                               'INNER JOIN qsr_team t ON t.team_name = i.home ' \
                               'INNER JOIN qsr_team c ON c.team_name = i.customer ' \
                               'INNER JOIN qsr_league l ON l.lea_name = i.league ' \
                               'INNER JOIN qsr_team_season s ON s.season_team_a = t.team_id ' \
                               'and s.season_team_b = c.team_id ' \
                               'AND s.season_start_play_time = CONCAT(i._date, " ", i._time) AND s.lea_id = l.lea_id ' \
                               'ON DUPLICATE KEY UPDATE fid = i.fid, sporttery_issue = i.sporttery_issue, league_id = ' \
                               'l.lea_id, ' \
                               'season_id = s.season_id, status_id = i.status_id'
        tx.execute(insertInto)

    def _conditional_news(self, tx, item):
        insertInto = 'INSERT INTO qsr_team_season_news (news_title ,news_content ,news_detail ,news_provenance_url ,' \
                     'news_provenance ,editor_create, news_conver) VALUES ("' + item['title'] + '", "' + item[
                         'title'] + '", "' + \
                     item['content'] + '", "' + item['url'] + '", "' + item['source'] + '", "' + item['time'] + '", "' + \
                     item['img'] + '")'
        tx.execute(insertInto)

    def _conditional_sporttery(self, tx, item):
        insertInto = 'INSERT INTO qsr_sporttery(target_id, week, num,sporttery_date,sporttery_time,' \
                     'b_date,status_id,is_hot,l_id,' \
                     'l_cn,h_id,h_cn,a_id,a_cn,index_show,sporttery_show,l_cn_abbr,h_cn_abbr,a_cn_abbr,h_order,' \
                     'a_order,h_id_dc,a_id_dc,l_background_color,weather,weather_city,weather_pic,temperature,' \
                     'last_updated) ' \
                     'SELECT i._id, i._week, i._num, i._date, i._time, i._b_date, i._status, i._hot, i._l_id, ' \
                     'i._l_cn, i._h_id, i._h_cn, i._a_id, i._a_cn, i._index_show, i._show, i._l_cn_abbr, ' \
                     'i._h_cn_abbr, i._a_cn_abbr, i._h_order, i._a_order, i._h_id_dc, i._a_id_dc, ' \
                     'i._l_background_color, i._weather, i._weather_city, i._weather_pic, i._temperature, ' \
                     'i._last_updated FROM (SELECT "' + str(item['id']) + '" AS _id, "' \
                     + str(item['week']) + '" AS _week, "' + str(item['num']) + '" AS _num, "' \
                     + str(item['date']) + '" AS _date, "' + str(item['time']) + '" AS _time, "' \
                     + str(item['b_date']) + '" AS _b_date, "' + str(item['status']) + '" AS _status, "' \
                     + str(item['hot']) + '" AS _hot, "' + str(item['l_id']) + '" AS _l_id, "' \
                     + str(item['l_cn']) + '" AS _l_cn, "' + str(item['h_id']) + '" AS _h_id, "' \
                     + str(item['h_cn']) + '" AS _h_cn, "' + str(item['a_id']) + '" AS _a_id, "' \
                     + str(item['a_cn']) + '" AS _a_cn, "' + str(item['index_show']) + '" AS _index_show, "' \
                     + str(item['show']) + '" AS _show, "' + str(item['l_cn_abbr']) + '" AS _l_cn_abbr, "' \
                     + str(item['h_cn_abbr']) + '" AS _h_cn_abbr, "' + str(item['a_cn_abbr']) + '" AS _a_cn_abbr, "' \
                     + str(item['h_order']) + '" AS _h_order, "' + str(item['a_order']) + '" AS _a_order, "' \
                     + str(item['h_id_dc']) + '" AS _h_id_dc, "' + str(item['a_id_dc']) + '" AS _a_id_dc, "' \
                     + str(item['l_background_color']) + '" AS _l_background_color, "' \
                     + str(item['weather']) + '" AS _weather, "' + str(item['weather_city']) + '" AS _weather_city, "' \
                     + str(item['weather_pic']) + '" AS _weather_pic, "' \
                     + str(item['temperature']) + '" AS _temperature, "' \
                     + str(item['last_updated']) + '" AS _last_updated) i ' \
                     'ON DUPLICATE KEY UPDATE week = i._week, num = i._num, sporttery_date = i._date, ' \
                     'sporttery_time = i._time, ' \
                     'b_date = i._b_date, status_id = i._status, is_hot = i._hot, l_id = i._l_id, l_cn = i._l_cn, ' \
                     'h_id = i._h_id, h_cn = i._h_cn, a_id = i._a_id, a_cn = i._a_cn, index_show = i._index_show,' \
                     'sporttery_show = i._show, l_cn_abbr = i._l_cn_abbr, h_cn_abbr = i._h_cn_abbr, ' \
                     'a_cn_abbr = i._a_cn_abbr, h_order = i._h_order, a_order = i._a_order, h_id_dc = i._h_id_dc,' \
                     'a_id_dc = i._a_id_dc, l_background_color = i._l_background_color, weather = i._weather,' \
                     'weather_city = i._weather_city, weather_pic = i._weather_pic, temperature = i._temperature, ' \
                     'last_updated = i._last_updated'
        tx.execute(insertInto)

    def _conditional_had(self, tx, item):
        insertInto = 'INSERT INTO qsr_sporttery_had ( type_id ,sporttery_id ,a ,d ,h ,goalline ,p_code ,o_type ,p_id,' \
                     'p_status_id ,single ,allup ,fixedodds ,cbt ,had_int ,vbt ,h_trend ,a_trend ,d_trend ,' \
                     'l_trend,expand ) ' \
                     'SELECT i._type_id, i._sporttery_id, i._a, i._d, i._h, i._goalline, i._p_code, i._o_type, ' \
                     'i._p_id, i._p_status_id, i._single, i._allup, i._fixedodds, i._cbt, i._had_int, i._vbt, ' \
                     'i._h_trend, i._a_trend, i._d_trend, i._l_trend, i._expand ' \
                     'FROM (SELECT "' + str(item['type_id']) + '" AS _type_id, "' + str(item['id']) + '" AS _sporttery_id, "' \
                     + str(item['a']) + '" AS _a, "' + str(item['d']) + '" AS _d, "' + str(item['h']) + '" AS _h, "' \
                     + str(item['goalline']) + '" AS _goalline, "' + str(item['p_code']) + '" AS _p_code, "' \
                     + str(item['o_type']) + '" AS _o_type, "' + str(item['p_id']) + '" AS _p_id, "' \
                     + str(item['p_status']) + '" AS _p_status_id, "' + str(item['single']) + '" AS _single, "' \
                     + str(item['allup']) + '" AS _allup, "' + str(item['fixedodds']) + '" AS _fixedodds, "' \
                     + str(item['cbt']) + '" AS _cbt, "' + str(item['int']) + '" AS _had_int, "' + str(item['vbt']) + '" AS _vbt, "' \
                     + str(item['h_trend']) + '" AS _h_trend, "' + str(item['a_trend']) + '" AS _a_trend, "' \
                     + str(item['d_trend']) + '" AS _d_trend, "' + str(item['l_trend']) + '" AS _l_trend, "' \
                     + str(item['expand']) + '" AS _expand) i ' \
                     'ON DUPLICATE KEY UPDATE type_id = i._type_id, sporttery_id = i._sporttery_id, a = i._a, ' \
                     'd = i._d, h = i._d, goalline = i._goalline, p_code = i._p_code, o_type = i._o_type, ' \
                     'p_id = i._p_id, p_status_id = i._p_status_id, single = i._single, allup = i._allup, ' \
                     'fixedodds = i._fixedodds, cbt = i._cbt, had_int = i._had_int, vbt = i._vbt, ' \
                     'h_trend = i._h_trend, a_trend = i._a_trend, d_trend = i._d_trend, l_trend = i._l_trend, ' \
                     'expand = i._expand'
        tx.execute(insertInto)

    def _conditional_matchInfo(self, tx, item):
        insertInto = 'INSERT INTO qsr_sporttery_match(_id, m_id, i_id, prompt, checked) ' \
                     'SELECT i._id, i._mId, i._iId, i._prompt, i._checked ' \
                     'FROM (SELECT "' + str(item['id']) + '" AS _id, "' + str(item['m_id']) + '" AS _mId, "' \
                     + str(item['i_id']) + '" AS _iId, "' + str(item['prompt']) + '" AS _prompt, "' \
                     + str(item['checked']) + '" AS _checked) i ' \
                     'ON DUPLICATE KEY UPDATE _id = i._id, m_id = i._mId, i_id = i._iId, ' \
                     'prompt = i._prompt, checked = i._checked'
        tx.execute(insertInto)

    def _conditional_sportteryResult(self, tx, item):
        insert = 'INSERT INTO qsr_sporttery_result(target_id,type_id,pool_rs,prs_name,goalline,single,odds,' \
                 'description) VALUES ("' + str(item['target_id']) + '", "' + str(item['type_id']) + '", "' \
                 + str(item['pool_rs']) + '", "' + str(item['prs_name']) + '", "' + str(item['goalline']) + '", "' \
                 + str(item['single']) + '", "' + str(item['odds']) + '", "' + str(item['description']) + '"); ' \
                 'UPDATE qsr_sporttery s SET s.status_id = 4 WHERE s.target_id = ' \
                 + str(item['target_id']) + ' AND s.status_id = 2 '
        tx.execute(insert)

    def _conditional_lottoResult(self, tx, item):
        insert = 'INSERT INTO qsr_lottoy_result(type_id, lotto_no,lotto_date,lotto_prize,lotto_sale,lotto_plan,' \
                 'lotto_serial,lotto_number) ' \
                 'VALUES ("' + str(item['type_id']) + '", "' + str(item['no']) + '", "' + str(item['date']) + '", "' \
                 + str(item['prize']) + '", "' + str(item['sale']) + '", "' + str(item['plan']) + '", "' \
                 + str(item['serial']) + '", "' + str(item['number']) + '")'
        tx.execute(insert)

    def _conditional_lottoResultItem(self, tx, item):
        insert = 'INSERT INTO qsr_lottoy_result_item(lotto_type_id,lotto_no,type_id,item_level,' \
                 'item_level_count,item_level_prize,description)' \
                 'VALUES("' + str(item['lt_id']) + '", "' + str(item['no']) + '", "' + str(item['type_id']) + '", "' \
                 + str(item['level']) + '", "' + str(item['count']) + '", "' + str(item['prize']) + '", "' \
                 + str(item['description']) + '")'
        tx.execute(insert)

    def _handle_error(self, failue, item, spider):
        print(item)
        print(spider)
        print('-------------------' + str(failue) + '---------------------------')


class DownloadImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return '/%s' % (image_guid)

    def get_media_requests(self, item, info):
        if item.__class__.__name__ == "TeamItem" or item.__class__.__name__ == "SportsmanItem":
            if item['icon_url'] != '':
                yield Request(item['icon_url'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s' % image_paths)
