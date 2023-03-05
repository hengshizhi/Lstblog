SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/lstblog' # SQLAlchemy 数据库连接串
SQLALCHEMY_ECHO = True # 是不是要把所执行的SQL打印出来，一般用于调试
SQLALCHEMY_POOL_SIZE = 1 # 连接池大小
SQLALCHEMY_POOL_MAX_SIZE = 100 # 连接池最大的大小
SQLALCHEMY_POOL_RECYCLE = 100 # 多久时间回收连接