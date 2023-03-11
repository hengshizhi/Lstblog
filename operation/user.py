#用户相关
import time as time
from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类
import random
import string
import random
from sanic.response import text
# try:
from . import config as configs
from . import md5 as md5
from .db import mysql as db
from .mail import mail as mails
# except:
#     import md5 as md5
#     import db.mysql as db
#     from mail import mail as mails
#     import config as configs
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
    HeadPortrait=True,#头像(url)
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
            return user.id
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
def get_user_data(id=False,name=False,postbox=False):
    '''
    获得用户数据：
    可以传入id,name,postbox
    返回用户数据,格式可以参照user表
    '''
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
    '''
    session['login_status_id'] :用户登录状态，登录的id
    '''
    config = configs.Email_login() # 获取配置
    def registered(self,get_or_post,s,rep):
        # 接收参数:
        name = get_or_post('name',time.time())
        Key = get_or_post('Key',False)
        postbox = get_or_post('postbox',False)
        nickname = get_or_post('nickname',True)
        Joined = get_or_post('Joined',True)
        HeadPortrait = get_or_post('HeadPortrait',True)

        id = registered_record(name=name,
                          Key=Key,
                          postbox=postbox,
                          nickname=nickname,
                          Joined=Joined,
                          HeadPortrait=HeadPortrait
                          ) #注册
        
    def login_SendEmainVerification_API(self,get_or_post,s,rep): #发送验证码并且储存验证码的API
        if(s.get('login_status_id')):return {'async':False,'data':text('Is logged in'),'cookie':{'Session_key':''},'session_odj':s}
        def login_Verification(self,id=False,name=False,postbox=False): #获取验证码(登录)并且发送
            data = get_user_data(id,name,postbox)
            Verification = random.randint(1, 5000000) #获取验证码
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
            return [Verification,data['id']] #成功,返回验证码

        #接收参数
        user_name = get_or_post('user_name',False)
        user_id = get_or_post('user_id',False)
        user_postbox = get_or_post('user_postbox',False)

        # print('AAAAAAAAA:',str(not user_name and not user_postbox and not user_id))

        if(not user_name and not user_postbox and not user_id):
            return {'async':False,
            'data':text('Parameter is not complete'),
            'cookie':{'Session_key':''}
            }

        Verification = login_Verification(self,user_id,user_name,user_postbox) #获取并发送验证码

        s.Set('Verification',Verification[0])
        s.Set('user_id',Verification[1])
        return {'async':False,
        'data':text('OK,ID->'+str(Verification[1])),
        'cookie':{'Session_key':''},
        'session_odj':s
        }
    def login_Email_Verifier_API(self,get_or_post,s,rep):
        # 参数：Verification（验证码）
        GetVerification = get_or_post('Verification') #得到的验证码
        if(str(s.data['Verification']) == str(GetVerification)):
            s.Set('login_status_id',s.data['user_id']) #设置登录状态
            s.delete(['user_id','Verification']) #删除待验证用户id,删除验证码
            print(s.data)
            return {'async':False,
            'data':text('OK,ID->'+str(s.data['login_status_id'])),
            'cookie':{'Session_key':''},
            'session_odj':s
            }
        else:
            return {'async':False,
            'data':text('Verification code error'),
            'cookie':{'Session_key':''},
            'session_odj':s
            }
# a = api()
# print(registered_record(postbox='aaa'))