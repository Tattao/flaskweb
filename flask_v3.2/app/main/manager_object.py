import cx_Oracle
import pymysql
import os
#
'''
1.how to import:
import os
import sys
mainpath=os.getcwd()
sys.path.append(mainpath)
from manager import runconn

2.how to use,for a example:
mycode=runconn(usename,passwd,ip,dbname,sid,type,sysname)
mycode=runconn('lhb','a','192.168.8.211','ORA11G','ora11g','oracle','qw')

3.if mycode=:
10086:oracle connect erro
10002:insert into aop_object_score erro
10001:aop_system do not have the syaname
10004:insert into aop_system erro
10005:database name erro
10000:success
'''



def runora(user,passwd,ip,name,ser_name,myconn,sys_id,sysname,type):
    address=ip+'/'+ser_name
    try:
        conn=cx_Oracle.connect(user,passwd,address)
        cur=conn.cursor()
    except:
        code=10086
        return code
        os._exit(0)
    cur.execute("select name from v$database")
    myname=cur.fetchone()[0]
    if myname==name:
        mycur=myconn.cursor()
        mycur.execute("select sysname from aop_system where sysname='%s'"%sysname)
        myname=mycur.fetchone()[0]
        if myname == sysname:
            try:
                mycur.execute("insert into aop_object_score values('%s','%s','%s','%s','%s','%s',NULL,NULL,'%s','%s',NULL)"%(sys_id,sysname,ip,name,sid,type,user,passwd))
                myconn.commit()
            except:
                code=10002
                return code
                os._exit(0)
        else:
            code=10001
            return code
            os._exit(0)

    else:
        code=10005
        return code
        os._exit(0)
    code='10000'
    cur.close()
    conn.close()
    return code
def runconn(user,passwd,ip,name,ser_name,type,sysname,sys_id):
    myconn=pymysql.connect(host='10.87.250.181',port=13306,user='root',password='hzmcmysql',db='hzmc_data')
    mycur=myconn.cursor()
    try:
        mycur.execute("insert into aop_system values('%s','%s',0,0,NULL)"%(sys_id,sysname))
        myconn.commit()
    except pymysql.err.IntegrityError:
        mycode=10004
        return mycode
        os._exit(0)
    if type=='oracle':
        mycode=runora(user,passwd,ip,name,ser_name,myconn,sys_id,sysname,type)
    elif type=='mysql':
        mycode=runmysql(load)
    mycur.close()
    myconn.close()
    return mycode
