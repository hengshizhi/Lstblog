#api回调类

# import operation
from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类
from operation.session import session
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

def helloWorld(get_or_post,session):
    lst = int(get_or_post('lst'))
    try:print(session['lst'])
    except:session['lst'] = None
    if(session['lst'] == None):
        session['lst'] = lst
    else:
        session['lst'] = session['lst']*0.8
    return {'async':False,
    'data':text(str(get_or_post('hello'))+'hello world'+str(session)),
    'cookie':{'Session_key':''}
    }

apiDict = {
    'helloWorld' : helloWorld
}

def main(request,name):
    '''
    ->
        {'async': False, 
        'data': <HTTPResponse: 200 text/plain; charset=utf-8>,
        'cookie' : {}
        }
    '''
    def get_or_post(key): #如果没有GET参数就用post
        if(request.args.get(key) != None):
            return request.args.get(key)
        elif(request.form.get(key) != None):
            return request.form.get(key)
        return None
    cookie_session_key = request.cookies.get("Session_key")
    session_odj = session(cookie_session_key)
    if(cookie_session_key == None or cookie_session_key == ''):session_odj.create() #创建Session_key
    session_odj.get() # 将数据库的session同步到内存
    # try:
    ret = apiDict[name](get_or_post,session_odj.data)
    # Session_key = session_odj.key
    # print(ret)
    session_odj.refresh() # 提交内存的session
    ret['cookie']['Session_key'] = session_odj.key # 更新cookie的session_key
    return ret
    # except:
    #     return empty(status=404)