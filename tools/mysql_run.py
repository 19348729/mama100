import MySQLdb


host="192.168.234.139"
hostname='root@192.168.234.139'
user="mm100"
passwd="mm100"
database="cmdb"
port=3306


db=MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset="utf8")



def conn_mysql(sql):
        global db
        cursor=db.cursor()
        cursor.execute(sql)
        data=cursor.fetchall()
        return data
        db.commit()
	db.close()
conn_mysql('select * from hostpasswd')	
