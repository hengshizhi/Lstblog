#用户相关
import time as time
from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类
import random
import string
import random
try:
    from . import config as configs
    from ..mod import md5 as md5
    from .db import mysql as db
    from .mail import mail as mails
except:
    import md5 as md5
    import db.mysql as db
    from mail import mail as mails
    import config as configs
get_session = db.get_session
User = db.table.User
mail = mails()
config = configs.information()
def registered_record(id=time.time(),#设置主键
    name=time.time(),#用户名
    Key=md5.get_md5(''.join(random.sample(string.ascii_letters + string.digits, 20))),#密码
    Registration_time=time.time(),#注册时间
    postbox=False,#邮箱
    nickname=True,#昵称
    Joined=True,#加入的聊天室
    HeadPortrait=True#头像(url)
):
    '''
    添加注册用户记录
    ->
    '''
    if(bool(id) and 
       bool(name) and 
       bool(Key) and 
       bool(Registration_time) and 
       bool(postbox) and
       bool(nickname) and
       bool(Joined) and
       bool(HeadPortrait)
    ):    
        with get_session() as s:
            user = User()
            user.created_at = time.time()
            user.updated_at = time.time()
            user.id = id
            user.name = name
            user.Key = Key
            user.Registration_time = Registration_time
            user.postbox = postbox
            user.nickname = nickname
            user.Joined = Joined
            user.HeadPortrait = HeadPortrait
            s.add(user)
            s.commit()
            return True
            # return {
            #     'new':
            #         [user.id,
            #         user.name,
            #         user.Key,
            #         user.Registration_time,
            #         user.postbox,
            #         user.nickname,
            #         user.Joined,
            #         user.HeadPortrait]
            # }
    else:
        return {'postbox':postbox}
def login_Password_authentication(id=False,name=False,postbox=False,Key=False):
    '''
    登录密码验证,支持：
    id登录:id
    用户名登录:name
    邮箱登录:postbox
    密码:Key
    '''
    with get_session() as s:
        if(id and s.query(User).filter(User.id == id,User.Key == Key).first() != []):
            return True
        elif(name and s.query(User).filter(User.name == name,User.Key == Key).first() != []):
            return True
        elif(postbox and s.query(User).filter(User.postbox == postbox,User.Key == Key).first() != []):
            return True
        else:
            return False
# print(login_Password_authentication(id=True,postbox='3192145045@qq.com',Key='hehheh'))
def get_data(id,name,postbox):
    with get_session() as s:
        try:id_data = s.query(User).filter(User.id == id,User.deleted_at == None).first()
        except:id_data = None
        try:name_data = s.query(User).filter(User.name == name,User.deleted_at == None).first()
        except:name_data = None
        try:postbox_data = s.query(User).filter(User.postbox == postbox,User.deleted_at == None).first()
        except:postbox_data = None
        if(id and id_data != None):data = id_data
        elif(name and name_data != None):data = name_data
        elif(postbox and postbox_data != None):data = postbox_data
        else:return None
        return data.single_to_dict() #将结果转换成dict
class api():
    config = configs.Email_login()
    def login_Verification(self,id=False,name=False,postbox=False): #获取验证码(登录)并且发送
        data = get_data(id,name,postbox)
        Verification = random.randint(1, 5000000) #获取验证码
        # print(data)
        if(data != None):
            try:
                mail.send(self.config.TEMPlate
                        .format(Verification=Verification,
                                nickname = data['nickname'],
                                name = data['name'],
                                websiteName = config.name
                                ),
                        self.config.Theme
                        .format(Verification=random.randint(1, 5000000),
                                nickname = data['nickname'],
                                name = data['name'],
                                websiteName = config.name
                                ),
                        {'nickname':data['name'],'address':data['postbox']})
            except:
                return False #邮件发送失败
        else:
            return None #不存在此用户
        return Verification #成功,返回验证码
    def login_SendEmainVerification_API(get_or_post,session): #发送验证码并且储存验证码的API
        user_name = get_or_post('user_name')
a = api()
print(registered_record(postbox='aaa'))