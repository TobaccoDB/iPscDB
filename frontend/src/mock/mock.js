import axios from 'axios';
import Mock from 'mockjs'
import MockAdapter from 'axios-mock-adapter';
import { users } from './data/user';
import { sysmenu } from './data/sysmenu';
let _users = users;
export default {
    bootstrap() {
        let mock = new MockAdapter(axios);
        mock.onGet('/user/list').reply(config => {
            let { searchInfo, page = 1 } = config.params;
            let getUsers = _users.filter(user => {
                if (searchInfo && user.username.indexOf(searchInfo) != -1 || user.rolename.indexOf(searchInfo) != -1) return true;
                return false;
            })
            let total = getUsers.length;
            getUsers = getUsers.filter((user, index) => {
                return index < 20 * page && index >= 20 * (page - 1);
            })
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve([200, {
                        users: getUsers,
                        total: total
                    }])
                }, 1000)
            })
        })
        mock.onGet('/user/sysmenu').reply(() => {
            return new Promise((resolve, reject) => {
                resolve([200, { data: sysmenu }])
            })
        })
        mock.onGet('/user/deletUsers').reply((config) => {
            let { delIds } = config.params;
            delIds = delIds.split(',')
            _users = _users.filter(u => !delIds.includes(u.userid));
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve([200, {
                        code: 200,
                        msg: '删除成功'
                    }]),
                        reject([500, {
                            code: 500,
                            msg: '操作失败'
                        }])
                }, 500)

            })
        })
        mock.onGet('/user/editUser').reply((config) => {
            let { userid, username, isable } = config.params;
            _users.forEach(u => {
                if (u.userid == userid) {
                    u.username = username;
                    u.isable = isable;
                }
            })
            return new Promise((resolve, reject) => {
                resolve([200, {
                    code: 200,
                    msg: '修改成功'
                }])
            })
        })
        mock.onGet('user/addUser').reply((config) => {
            debugger
            let { id } = Mock.mock({
                id: Mock.Random.guid()
            })
            let orderNum = _users.length;
            let { username, rolename, isable } = config.params;
            _users.unshift({
                orderNum: ++orderNum,
                userid: id,
                username: username,
                rolename: rolename,
                loginTime: '0',
                loginDate: '',
                creater: localStorage.getItem('ms_username'),
                isable: isable
            });
            return new Promise((resolve, reject) => {
                resolve([200, {
                    msg: '添加成功',
                    code: 200
                }])
            })
        })
        mock.onGet('/user/DeleteOne').reply(config => {
            let { userid } = config.params;
            _users.forEach((item, index) => {
                if (item.userid == userid) {
                    _users.splice(index, 1);
                }
            })
            return new Promise((resolve, reject) => {
                resolve([200, {
                    code: 200,
                    msg: '删除成功'
                }])
            })
        })
    }
}