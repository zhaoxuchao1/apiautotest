'''
注册的测试脚本(pytest)
'''
from ZongHe.baw import Member, DbOp
from ZongHe.caw import DataRead
import  pytest
# 注册失败
# 测试前置：获取测试数据，数据是列表，通过readyaml读取的
@pytest.fixture(params=DataRead.readyaml("ZongHe/data_case/register_fail.yaml"))
def fail_data(request): # 固定写法
    return request.param
# 注册成功
# 测试前置：获取测试数据，数据是列表，通过readyaml读取的
@pytest.fixture(params=DataRead.readyaml("ZongHe/data_case/register_pass.yaml"))
def pass_data(request):
    return request.param
# 重复注册
@pytest.fixture(params=DataRead.readyaml("ZongHe/data_case/register_repeat.yaml"))
def repeat_data(request):
    return request.param

# 注册失败
def test_register_fail(fail_data,url,baserequests):
    print(f"测试数据为:{fail_data['casedata']}")
    print(f"预期结果为:{fail_data['expect']}")
    # 发送请求
    r = Member.register(url,baserequests,data=fail_data['casedata'])
    # 检查结果
    assert r.json()["status"] == fail_data["expect"]["status"]
    assert r.json()["code"] == fail_data["expect"]["code"]
    assert r.json()["msg"] == fail_data["expect"]['msg']


# 注册成功
def test_register_pass(pass_data,url,db,baserequests):
    print(f"测试数据为:{pass_data['casedata']}")
    print(f"预期结果:{pass_data['expect']}")
    phone = pass_data['casedata']['mobilephone']
    # 初始化环境，确保环境中没有影响本次执行的数据
    DbOp.deleteUser(db, phone)
    # 发送请求
    r = Member.register(url, baserequests, data=pass_data['casedata'])
    # print(r.text)
    # 1.检查响应结果
    assert r.json()["status"] == pass_data["expect"]["status"]
    assert r.json()["code"] == pass_data["expect"]["code"]
    assert r.json()["msg"] == pass_data["expect"]['msg']
    #2. 检查实际有没有注册（1、查数据库2.获取用户列表。3.用注册的用户登录）
    r = Member.getList(url, baserequests)
    assert phone in r.text
    #清理环境，根据手机号删除用户
    DbOp.deleteUser(db,phone)


# 重复注册
def test_register_repeat(repeat_data,url,db,baserequests):
    print(f"测试数据为:{repeat_data['casedata']}")
    print(f"预期结果:{repeat_data['expect']}")

    phone = repeat_data['casedata']['mobilephone']
    # 初始化环境，确保环境中没有影响本次执行的数据
    DbOp.deleteUser(db, phone)
    # 发送请求
    Member.register(url, baserequests, repeat_data['casedata'])
    r1 = Member.register(url, baserequests, repeat_data['casedata'])
    # print(r.text)
    # 1.检查响应结果
    assert r1.json()["status"] == repeat_data["expect"]["status"]
    assert r1.json()["code"] == repeat_data["expect"]["code"]
    assert r1.json()["msg"] == repeat_data["expect"]['msg']
    # 清理环境，根据手机号删除用户
    DbOp.deleteUser(db, phone)
