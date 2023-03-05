#储存表结构
import contextlib
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    DateTime,
    String,
)

class BaseMixin:
    """model的基类,所有model都必须继承"""
    id = Column(Integer, primary_key=True)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False, index=True)
    deleted_at = Column(Integer)  # 可以为空, 如果非空, 则为软删
    # 单个对象方法1
    # def to_dict(self):
    #     model_dict = dict(self.__dict__)
    #     del model_dict['_sa_instance_state']
    #     return model_dict
    # Base.to_dict = to_dict # 注意:这个跟使用flask_sqlalchemy的有区别
    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

class User(BaseMixin):
    __tablename__ = "user" #表名
    id = Column(Integer,primary_key=True,nullable=False) #设置主键
    name = Column(String(32),nullable=False) #用户名
    Key = Column(String(64),nullable=False) #密码
    Registration_time = Column(Integer) #注册时间
    postbox = Column(String(64),nullable=False) #邮箱
    nickname = Column(String(32)) #昵称
    Joined = Column(String(32)) #加入的聊天室
    HeadPortrait = Column(String(32)) #头像(url)