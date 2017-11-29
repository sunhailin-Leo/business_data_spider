import axios from 'axios';

//正常使用
let base = '';

let iaxios = axios.create({
    baseURL: '/v1'
});


//登录
export const requestLogin = params => { return axios.post(`${base}/login`, params).then(res => res.data); };

// 2、获取用户列表
export const getUserList = params => {
    return iaxios.get(`/platform/pageAccount`, { params: params });
};

// 删除用户
export const batchRemoveUser = params => { return axios.get(`${base}/user/batchremove`, { params: params }); };


// 平台板块
// 1、获取平台列表
export const getPlatformPage = params => { return iaxios.get(`/platform/pagePlatform`, { params: params }).then(res => res.data); };

// 2、更新平台状态
export const editPlatformStatus = params => { return iaxios.put('/platform/platformStatus', params).then(res => res.data); };

// 3、添加新平台
export const addPlatform = params => { return iaxios.post('/platform/newPlatform', params).then(res => res.data); };

// 4、删除平台
export const removePlatform = params => { return iaxios.post('/platform/removePlatform', params).then(res => res.data); };

// 爬虫板块
// 1、获取爬虫进度
export const getSpiderProcessInfo = params => {return iaxios.get(`/spider_list`, { params: params}).then(res => res.data); };




