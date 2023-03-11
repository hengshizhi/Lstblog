#api回调类

from operation.user import api as user
from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类
from operation.session import session

user = user()
'''
API开发文档:
返回的对象需要是sanic.response里面的
session是会话,它支持会话
返回示例：
{'async':True,'data':file('./data/sanic.json')}
fun:
def helloWorld(get_or_post,session):
    session['aaa'] = get_or_post('lst')
    return {'async':True,
    'data':file('./data/sanic.json')}

apiDict:
这个是一个API的字典:
{'name':API_function}
'''

def helloWorld(get_or_post,s):
    try:lst = int(get_or_post('lst')) #获取http参数
    except:pass
    try:print(s.data['lst']) #如果session里面的lst存在就打印
    except:s.data['lst'] = None #不存在就初始化为None
    if(s.data['lst'] == None):
        s.data['lst'] = lst
    else:
        s.data['lst'] = s.data['lst']*0.8
    return {'async':False,
    'data':text(str(get_or_post('hello'))+'hello world'+str(session)),
    'cookie':{'Session_key':''},'session_odj':s
    }

apiDict = {
    'helloWorld' : helloWorld,
    'login_SendEmainVerification_API' : user.login_SendEmainVerification_API,
    'login_Email_Verifier_API': user.login_Email_Verifier_API
}

def main(request,name):
    '''
    ->
        {'async': False, 
        'data': <HTTPResponse: 200 text/plain; charset=utf-8>,
        'cookie' : {}
        }
    '''
    def rep(session_odj,_async=False,data=text('null'),cookie={}):
         return {'async':_async,
            'data':data,
            'cookie':cookie,
            'session_odj':session_odj
            }
    def get_or_post(key,output=None,request=request): #如果没有GET参数就用post
        '''
        key:需要接收参数的键值
        output:返回格式,如果没有此参数就返回它,默认None
        '''
        if(request.args.get(key) != None):
            return request.args.get(key)
        elif(request.form.get(key) != None):
            return request.form.get(key)
        return output
    def get_session_key(request):
        # cookie_session_key = request.cookies.get("Session_key")
        # if(cookie_session_key == None):
            return get_or_post('SessionKey',request)
        # return cookie_session_key
    session_key = get_or_post('SessionKey')
    # print('cookie_session_key:',session_key)
    session_odj = session(session_key)
    if(session_key == None or session_key == ''):session_odj.create() #创建Session_key
    session_odj.getDB() # 将数据库的session同步到内存
    # try:
    ret = apiDict[name](get_or_post,session_odj,rep)
    session_odj = ret['session_odj'] # 覆写session_odj为更改过的session_odj
    session_odj.refresh() # 提交内存的session
    ret['cookie']['Session_key'] = session_odj.key # 更新cookie的session_key
    return ret
    # except:
    #     return empty(status=404)