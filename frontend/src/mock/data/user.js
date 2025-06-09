import Mock from 'mockjs';
const users = [];
for (let i = 0; i < 100; i++) {
    let user = {};
    user=Mock.mock({
        orderNum:i+1,
        userid:Mock.Random.guid(),
        username:Mock.Random.last(),
        isable:Mock.Random.integer(0,1).toString(),
        loginTime:Mock.Random.integer(0,20),
        loginDate:Mock.Random.date(),
        creater:Mock.Random.cname(),
        'rolename|1':['admin','超级管理员','用户']
    })
    users.push(user);
}
export {users}