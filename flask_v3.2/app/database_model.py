from . import db

class aop_system(db.Model):
    __tablename__ = 'aop_system'
    __bind_key__ = 'hzmc_data'

    sys_id = db.Column(db.UnicodeText,primary_key=True)
    sysname = db.Column(db.UnicodeText)
    status = db.Column(db.Integer)
    score = db.Column(db.DECIMAL)


class aop_object_score(db.Model):
    __tablename__ = 'aop_object_score'
    __bind_key__ = 'hzmc_data'

    sys_id = db.Column(db.UnicodeText, primary_key=True)
    object_id = db.Column(db.UnicodeText, primary_key=True)
    object_name = db.Column(db.UnicodeText)
    instance_name = db.Column(db.UnicodeText)
    object_type = db.Column(db.UnicodeText)
    score = db.Column(db.DECIMAL)
    status = db.Column(db.Integer)


class aop_model_score(db.Model):
    __tablename__ = 'aop_model_score'
    __bind_key__ = 'hzmc_data'

    sys_id = db.Column(db.UnicodeText, primary_key=True)
    object_id = db.Column(db.UnicodeText, primary_key=True)
    model_id = db.Column(db.UnicodeText, primary_key=True)
    model_name = db.Column(db.UnicodeText)
    table_name = db.Column(db.UnicodeText)
    #table_name不作为主键。防止model_id冲突
    score = db.Column(db.DECIMAL)

#主页性能图
class hzmc_month(db.Model):
    __tablename__ = 'score_month'
    __bind_key__ = 'hzmc'

    time = db.Column(db.DATETIME,primary_key=True)
    inst_id = db.Column(db.INTEGER,primary_key=True)
    hour = db.Column(db.VARCHAR,primary_key=True)
    score_name = db.Column(db.VARCHAR,primary_key=True)
    base_line = db.Column(db.BIGINT)

#告警
#站点-id;name-监控项;status-统计OK和PROBLEM的数量;value-设备
class zabbix_warning(db.Model):
    __tablename__ = 'zabbix_warning'
    __bind_key__ = 'target_warning'

    time = db.Column(db.VARCHAR)
    id = db.Column(db.VARCHAR,primary_key=True)
    name = db.Column(db.VARCHAR,primary_key=True)
    value = db.Column(db.VARCHAR)
    status = db.Column(db.VARCHAR)


# 全局变量。修改表指向数据库的映射
global tablename
tablename = 'view_flow_parse'


def changeName(name):
    global tablename
    tablename = name


# demo
# class view_flow_parse(db.Model):
#     __tablename__ = tablename
#     __bind_key__ = 'hzmc'
#
#     snap_id = db.Column(db.Integer)
#     start_time = db.Column(db.DATETIME)
#     end_time = db.Column(db.DATETIME, primary_key=True)
#     inst_id = db.Column(db.Integer, primary_key=True)
#     input = db.Column(db.DECIMAL)
#     output = db.Column(db.DECIMAL)


##################
# 新表结构构建如下：
##################
# '指标层次关系表'
class score_dept(db.Model):
    __bind_key__ = 'hzmc'

    tab_name = db.Column(db.VARCHAR(100), primary_key=True)
    tab_level = db.Column(db.Integer)
    metric_name = db.Column(db.VARCHAR(100))
    up_table = db.Column(db.VARCHAR(100))
    stat_type = db.Column(db.VARCHAR(20))


# '上层指标汇总记分规则表'
class score_gen_rule(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    module_name = db.Column(db.VARCHAR(30))
    stat_name = db.Column(db.VARCHAR(30), primary_key=True)
    start_time = db.Column(db.TIME, primary_key=True)
    end_time = db.Column(db.TIME)
    score_rule = db.Column(db.VARCHAR(30))
    value = db.Column(db.BIGINT)


# '数据库分值表'
class score_db(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  ----------------------------------解析分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# 解析分值表
class score_parse(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# 解析cpu得分表
class parse_cpu_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 解析等待得分表
class parse_wait_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 硬解析等待得分表
class parse_hard_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  ----------------------------------执行分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# 执行分值表
class score_exec(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# 执行时间分值表
class exec_time_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 执行等待分值表
class exec_wait_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------物理IO分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# 物理io分值表
class score_pio(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# 物理IO读取响应时间分值表
class pio_rtime_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 物理IO写入响应时间分值表
class pio_wtime_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 直接路径读响应时间分值表
class pio_d_rtime_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 直接路径写响应时间分值表
class pio_d_wtime_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 物理IO请求写入比分值表
class pio_req_write_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------逻辑IO分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# 逻辑io分值表
class score_lio(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# 逻辑IO等待次数分值表
class lio_wait_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 逻辑读命中率分值表
class lio_ratio_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 逻辑读cr分值表
class lio_cr_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------Buffer Cache 分值相关表--------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# Buffer Cache分值表
class score_bc(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# 索引分裂分值表
class bc_idxsplit_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 检查点写入数据分值表
class bc_ckpt_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# LRU链分值表
class bc_lru_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# index failed probes 分值表
class bc_idxfp_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# buffer nowait分值表
class bc_nowait_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------共享池分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# Shared Pool分值表
class score_sp(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# open cursor分值表
class sp_cursor_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# Dictionary Cache Stats分值表
class sp_dict_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# Library Cache Activity分值表
class sp_lca_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# Library Cache Hit分值表
class sp_lcratio_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# 软软解析分值表
class sp_ssparse_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------Redo  分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# Redo 分值表
class score_redo(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# redo 等待次数分值表
class redo_wait_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# log file sync分值表
class redo_lgsync_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# log file parallel write 分值表
class redo_lgwr_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------Undo  分值相关表---------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# undo 分值表
class score_undo(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# undo 等待次数分值表
class undo_wait_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# expired undo blocks stolen from other undo segments 分值表
class undo_expired_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# rollback 分值表
class undo_rollback_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# /*  ---------------------------------------------------------------------------------------------- */
# /*  --------------------------------SQL  分值相关表----------------------------------------------- */
# /*  ---------------------------------------------------------------------------------------------- */

# SQL 分值表
class score_sql(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)


# 耗时长SQL 分值表
class sql_long_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# high cpu SQL 分值表
class sql_cpu_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# high io SQL 分值表
class sql_io_score(db.Model):
    __bind_key__ = 'hzmc'

    inst_id = db.Column(db.INTEGER, primary_key=True)
    snap_id = db.Column(db.INTEGER, primary_key=True)
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)
    score = db.Column(db.BIGINT)
    value = db.Column(db.BIGINT)


# # sql plan 分值表
# class sql_plan_score(db.Model):
#     __bind_key__ = 'hzmc'
#
#     inst_id = db.Column(db.INTEGER, primary_key=True)
#     snap_id = db.Column(db.INTEGER, primary_key=True)
#     start_time = db.Column(db.DATETIME)
#     end_time = db.Column(db.DATETIME)
#     score = db.Column(db.BIGINT)
#     value = db.Column(db.BIGINT)
