try:
    from sanic import Sanic #导入sanic web的本体
    from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类
    import api as api_main
    # from operation.session import Session
except:
    import autoinstall
    from sanic import Sanic #导入sanic web的本体
    from sanic.response import text,html,json,file,raw,file_stream,redirect,empty #导入sanic web的工具类
    import api as api_main
    # from operation.session import Session #导入会话
config = {'host':'127.0.0.1',
    'api_key':'sxaewezaeqx', #超级管理
    'api_id':'xwezqwxa',
    'port':9000,
    'debug':True,
    'dev':True,
    'admin_path':'admin'
}

def get_or_post(request,key): #如果没有GET参数就用post
    if(request.args.get(key) != None):
        return request.args.get(key)
    elif(request.form.get(key) != None):
        return request.form.get(key)
    return None

app = Sanic("Lstblog_centralized-chat-group-system") #实例化Sanic
# Session(app)

async def favicon(request):
    '''favicon.ico图标'''
    return text('OK!')

async def api(request,name): #API执行函数
    data = api_main.main(request,name)
    ret = data['data']
    for k,v in data['cookie'].items(): #设置cookie
        ret.cookies[k] = v
    print(ret)
    if(data['async']):
        return await ret
    else:
        return ret

app.add_route(api,f'/api/<name:path>',methods=['GET','POST']) #HTTPAPI
app.add_route(favicon, "/favicon.ico",methods=["GET"]) # favicon.ico

if __name__ == "__main__":
    app.run(host=config['host'],port=config['port'],debug=config['debug'],dev=config['dev'])