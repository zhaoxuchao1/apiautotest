'''
用户模块的接口（注册、登录、充值、用户列表、取现。。。）
'''
# 注册
def register(url,baserequests,data):
    '''
    发送注册接口
    :param url:http://jy001:8081/
    :param baserequests:是BaseRequests的一个实例
    :param data: 注册接口的参数
    :return: 响应信息
    '''
    url = url + "futureloan/mvc/api/member/register"
    r = baserequests.post(url,data=data)
    return r

# 登录
def login(url,baserequests,data):
    url = url + "futureloan/mvc/api/member/login"
    r = baserequests.post(url,data=data)
    return r

# 用户列表
def getList(url,baserequests):
    url =url + "futureloan/mvc/api/member/list"
    r= baserequests.get(url)
    return r

# 测试代码 用完删除
if __name__ == '__main__':
    from ZongHe.caw.BaseRequests import  BaseRequests
    from ZongHe.caw.DataRead import readini
    baserequests = BaseRequests()
    canshu = {"mobilephone": "1372223", "pwd": "123456"}
    # r = register("http://jy001:8081/",baserequests,canshu)
    r = register(readini(r"ZongHe\data_env\env.ini","url"),baserequests,canshu)
    print(r.json())