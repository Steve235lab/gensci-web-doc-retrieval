let myStorage=(function() {
    function setItem(data) {//存入localStorage方法
        // 存入的参数
        const obj = {
           // name: "",   // 存入的名字
            value: "",   // 存入的值
            expires: "1800000",   // 过期时间
            startTime: new Date().getTime()  //存入的时间
        }
        const options = {};// 将obj 和传进来的params 合并  放到options里面 实现js中浅拷贝
        Object.assign(options, obj, data);
        // 判断用户是否设置了过期时间
        if (options.expires) {
            //  以options.name为key,    options为值放进去
            localStorage.setItem(options.name, JSON.stringify(options));
        } else {
            // 如果 options.expires 没有设置的话， 就判断一下value的类型
            // 注意 我们 的 localStorage 只能存储字符串 像是数组和对象要转换下
            let type = Object.prototype.toString.call(options.value);
            if (type == '[object Object]' || type == '[object Array]') {
                options.value = JSON.stringify(options.value);
            }
            localStorage.setItem(options.name, options.value);
        }
    }
    // 获取数值
    function getItem(name) {
        let item = localStorage.getItem(name);
        // 判断 item 是否存在 
        if (item) {
            // 先将取到的对象 看能转换成object 对象格式，不能就说明不是json字符串形式

            // 如果有expires的值,说明设置了失效时间
            if (item.expires) {
                    // 获取当前时间
                let now = new Date().getTime();
                // 当前的时间和存入时候的时间 进行相减 和过期时间进行比较
                // 大于就说明过期了 清除存储  小于或者等于 就没有过期 
                if (now - item.startTime > item.expires) {
                    localStorage.removeItem(name);
                    return false;  // 返回一个状态值
                } else {
                    //缓存未过期，返回值
                    return item.value;
                }
            } else {
                // 没有设置过期时间，直接返回值
                return item;
            }
        }else{
            return false; // 如果item 值为undefined 则说明没有存储 返回false
        }
    }

    // 移除指定的缓存
    function removeItem(name) {
        localStorage.removeItem(name);
    }
    // 移除所有的存储数据
    function clear() {
        localStorage.clear();
    }
    return {    // 返回 执行接口
        setItem,
        getItem,
        removeItem,
        clear
    }
})();
export default myStorage; //暴露方法