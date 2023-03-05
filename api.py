#api回调类

import operation
from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类

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
    session['aaa'] = get_or_post('lst')
    return {'async':False,
    'data':text(str(get_or_post('hello'))+'hello world'+str(session))}

apiDict = {
    'helloWorld' : helloWorld
}

def main(request,name):
    def get_or_post(key): #如果没有GET参数就用post
        if(request.args.get(key) != None):
            return request.args.get(key)
        elif(request.form.get(key) != None):
            return request.form.get(key)
        return None
    # try:
    return apiDict[name](get_or_post,request.ctx.session)
    # except:
    #     return empty(status=404)