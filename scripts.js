// 默认搜索词
const defaultSearchWords = ["特种兵旅游", "村BA", "冰雪大世界", "Citywalk", "MBTI", "盲盒经济", "元宇宙", "ChatGPT", "短视频爆款", "网红景点", "直播带货", "电竞", "汉服热", "剧本杀", "国潮热", "共享经济", "地摊经济", "露营", "围炉煮茶", "飞盘", "NFT", "社交恐惧", "网络热梗", "熬夜党", "打工人", "干饭人", "尾款人", "凡尔赛", "yyds", "绝绝子", "躺平", "内卷", "摆烂", "小镇做题家", "脆皮大学生", "互联网嘴替", "显眼包", "电商大促", "宠物经济", "手账文化", "骑行热", "筋膜枪健身", "无糖饮料潮", "职场PUA", "云养猫", "数字游民", "睡眠经济", "微醺经济", "国潮彩妆", "减肥代餐", "轻食主义", "盲盒玩偶", "炒鞋现象", "古着时尚", "水下摄影", "无人机拍摄", "智能家居", "空气炸锅美食", "破壁机养生", "螺蛳粉效应", "奶茶社交", "打卡文化", "手办收藏", "怀旧零食", "复古游戏", "塔罗牌占卜", "密室逃脱", "轰趴聚会", "自驾游", "亲子游", "毕业旅行", "情侣约会地", "网红民宿", "青年旅社", "胶囊旅馆", "主题餐厅", "屋顶酒吧", "夜市小吃", "早C晚A", "多巴胺穿搭", "松弛感生活", "情绪价值", "搭子社交", "二手交易", "闲置互换", "公益众筹", "环保行动", "低碳生活", "断舍离理念", "收纳技巧", "时间管理", "高效学习", "考证攻略", "考研经验", "留学申请", "职场晋升", "副业兼职", "理财小白", "股票投资", "基金定投", "虚拟货币", "防诈骗指南", "网络安全", "数据隐私", "5G应用", "量子计算", "人工智能发展", "人脸识别技术", "智能家居控制", "智能穿戴设备", "物联网应用", "大数据分析", "云计算服务", "边缘计算概念", "虚拟现实体验", "增强现实游戏", "3D打印技术", "无人机竞速", "机器人竞赛", "航天科普", "卫星发射", "宇宙探索", "天文观测", "流星雨预测", "日食月食现象", "黑洞研究", "外星生命猜想", "陨石收藏", "地理奇观", "世界遗产", "国家公园", "热带雨林探险", "沙漠徒步", "高原旅游", "海滨度假", "滑雪胜地", "温泉疗养", "瀑布景观", "峡谷穿越", "溶洞探秘", "古建筑欣赏", "民俗文化节", "非遗传承", "地方戏曲", "民间手工艺", "剪纸艺术", "皮影戏表演", "木偶戏展示", "民族舞蹈", "传统乐器演奏", "书法绘画展览", "古籍修复", "茶文化传播", "酒文化品鉴", "中医养生", "针灸推拿", "武术健身", "太极文化", "瑜伽修行", "冥想放松", "心理疗愈", "心理咨询", "情感挽回", "恋爱技巧", "婚姻经营", "亲子教育", "早教课程", "儿童玩具推荐", "母婴护理", "老年健康", "养老院选择", "临终关怀", "殡葬改革", "新闻热点", "时事评论", "国际局势", "国内政策", "两会解读", "政府工作报告", "反腐行动", "扫黑除恶", "社会公益", "慈善事业", "志愿者服务", "希望工程", "红十字会", "壹基金", "嫣然天使基金", "环境保护税", "碳交易市场", "垃圾分类政策", "限塑令实施", "水污染治理", "空气污染防治", "土壤修复", "森林保护", "野生动物保护", "海洋保护", "湿地保护", "草原保护", "文物保护", "历史研究", "考古发现", "古墓发掘", "文物修复", "博物馆展览", "美术馆参观", "艺术创作", "文学写作", "诗歌朗诵", "小说阅读", "散文赏析", "戏剧表演", "电影评论", "电视节目推荐", "音乐鉴赏", "演唱会现场", "音乐节狂欢", "舞蹈演出", "杂技表演", "魔术秀", "相声小品", "脱口秀大会", "喜剧综艺", "悲剧艺术", "摄影技巧", "摄影作品赏析", "绘画技巧", "绘画作品欣赏", "雕塑艺术", "工艺美术", "设计理念", "平面设计", "室内设计", "景观设计", "工业设计", "服装设计", "珠宝设计", "动漫制作", "动画电影", "漫画阅读", "游戏设计", "游戏开发", "游戏攻略", "电竞比赛直播", "网络小说", "实体书推荐", "读书俱乐部", "知识付费", "在线教育"];
// 定义倒计时相关的定时器 ID
let countdownIntervalId, countdownTimeoutId;
// 最大搜索次数
let maxStops;
// 下一个要搜索的词
let nextSearchWord = "";
// 搜索开关
let searchToggle = true;
// 是否正在搜索的标志
let isSearching = false;
// 已完成的搜索次数
let completedSearches = 0;
// 总搜索次数，从本地存储获取，如果没有则初始化为 0
let totalSearches = localStorage.getItem("totalSearches")? parseInt(localStorage.getItem("totalSearches")) : 0;
// 是否处于异常模式的标志
let isException = "true" === localStorage.getItem("isException");
// 倒计时的最小和最大时间
let countdownMin = 50;
let countdownMax = 80;
// 本地搜索词文件路径
const hotkeysFilePath = "hotkeys.json";
// 倒计时 worker
let countdownWorker;

// 生成指定范围内的随机整数
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 检测设备类型并设置最大搜索次数
function detectDevice() {
    const userAgent = navigator.userAgent.toLowerCase();
    const isMobile = /iphone|ipad|ipod|android/.test(userAgent);
    const deviceTypeElement = document.getElementById("device-type");
    if (isMobile) {
        deviceTypeElement.textContent = "移动设备";
        localStorage.setItem("maxStops", getRandomInt(22, 26).toString());
    } else {
        deviceTypeElement.textContent = "电脑设备";
        localStorage.setItem("maxStops", getRandomInt(32, 36).toString());
    }
}

// 从本地hotkeys.json文件获取搜索词
async function fetchSearchWords() {
    const allSearchWords = [];
    
    try {
        console.log('开始从本地hotkeys.json文件获取搜索词');
        
        // 使用fetch获取本地的hotkeys.json文件
        const response = await fetch('hotkeys.json', { 
            headers: { 'Cache-Control': 'no-cache' }
        });
        
        if (!response.ok) {
            throw new Error(`本地文件响应状态码: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 处理hotkeys.json文件中的数据
        if (data && Array.isArray(data.titles) && data.titles.length > 0) {
            // 过滤有效的标题
            const validTitles = data.titles.filter(title => title && typeof title === 'string');
            
            if (validTitles.length > 0) {
                console.log(`从本地文件成功获取 ${validTitles.length} 个搜索词`);
                allSearchWords.push(...validTitles);
            } else {
                console.warn('本地文件中没有有效的搜索词');
            }
        } else {
            console.warn('本地文件的数据格式不符合预期:', data);
        }
    } catch (error) {
        console.error('从本地文件获取数据时出错:', error.message || error);
    }
    
    console.log(`本地文件读取完成: 获取到 ${allSearchWords.length} 个搜索词`);
    
    // 只有在成功获取到搜索词时才更新本地存储
    if (allSearchWords.length > 0) {
        const storageData = {
            searchWords: allSearchWords,
            fetchTime: Date.now()
        };
        localStorage.setItem("searchWords", JSON.stringify(storageData));
    }
    
    return allSearchWords;
}

// 检查本地存储的搜索词是否超过 6 小时
function checkSearchWordsValidity() {
    try {
        const storedData = localStorage.getItem("searchWords");
        if (storedData) {
            const parsedData = JSON.parse(storedData);
            if (parsedData && Array.isArray(parsedData.searchWords) && typeof parsedData.fetchTime === 'number') {
                const { searchWords, fetchTime } = parsedData;
                const currentTime = Date.now();
                const oneHoursInMs = 6 * 60 * 60 * 1000;
                if (currentTime - fetchTime < oneHoursInMs && searchWords.length > 0) {
                    return searchWords;
                }
            }
        }
    } catch (error) {
        console.error("检查搜索词有效性时出错:", error);
    }
    return null;
}

// 获取下一个搜索词
async function getNextSearchWord() {
    let searchWords = checkSearchWordsValidity();
    if (!searchWords || searchWords.length === 0) {
        searchWords = await fetchSearchWords();
    }
    
    // 修复：确保在本地文件获取失败或返回空数组时使用默认搜索词
    if (!searchWords || searchWords.length === 0) {
        console.log("本地文件获取搜索词失败，使用默认搜索词");
        return defaultSearchWords[Math.floor(Math.random() * defaultSearchWords.length)];
    }
    
    const randomIndex = getRandomInt(0, searchWords.length - 1);
    nextSearchWord = searchWords.splice(randomIndex, 1)[0];
    const storageData = {
        searchWords,
        fetchTime: localStorage.getItem("searchWords") ? JSON.parse(localStorage.getItem("searchWords")).fetchTime : Date.now()
    };
    localStorage.setItem("searchWords", JSON.stringify(storageData));
    return nextSearchWord;
}

// 在页面上显示当前搜索词
function displaySearchWord(word) {
    document.getElementById("current-search-word").textContent = word;
}

// 添加搜索历史到页面
function addSearchHistory(word, url) {
    const searchHistoryElement = document.getElementById("search-history");
    const historyItems = searchHistoryElement.querySelectorAll(".search-history-item");
    if (historyItems.length >= 2) {
        const iframes = historyItems[1].querySelectorAll("iframe");
        if (iframes.length > 0) {
            historyItems[1].removeChild(iframes[0]);
        }
    }
    const newHistoryItem = document.createElement("div");
    newHistoryItem.className = "search-history-item";
    newHistoryItem.innerHTML = `<p>${word}</p><iframe src="${url}"></iframe>`;
    searchHistoryElement.insertBefore(newHistoryItem, searchHistoryElement.firstChild);
}

// 执行搜索操作
function performSearch(word) {
    const randomString1 = generateRandomString(4);
    const randomString2 = generateRandomString(32);
    let searchUrl;
    if (searchToggle) {
        searchUrl = `https://www.cn.bing.com/search?q=${encodeURIComponent(word)}&form=${randomString1}&pq=${encodeURIComponent(word)}&cvid=${randomString2}`;
    } else {
        searchUrl = `https://www.cn.bing.com/search?q=${encodeURIComponent(word)}&cvid=${randomString2}&FORM=${randomString1}`;
    }
    searchToggle = !searchToggle;
    addSearchHistory(word, searchUrl);
}

// 生成指定长度的随机字符串
function generateRandomString(length) {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

// 启动自动搜索
async function startAutoSearch() {
    if (!isSearching) {
        isSearching = true;
        async function startCountdown() {
            const randomTime = Math.floor(4000 * Math.random()) + 14000;
            let remainingTime = Math.ceil(randomTime / 1000);
            const countdownElement = document.getElementById("countdown-timer");
            nextSearchWord = await getNextSearchWord();
            displaySearchWord(nextSearchWord);
            countdownElement.textContent = remainingTime;
            countdownIntervalId = setInterval(() => {
                remainingTime -= 1;
                countdownElement.textContent = remainingTime;
                if (remainingTime <= 0) {
                    clearInterval(countdownIntervalId);
                }
            }, 1000);
            countdownTimeoutId = setTimeout(() => {
                performSearch(nextSearchWord);
                clearInterval(countdownIntervalId);
                completedSearches++;
                totalSearches++;
                document.getElementById("completed-searches").textContent = completedSearches;
                document.getElementById("total-searches").textContent = totalSearches;
                localStorage.setItem("totalSearches", totalSearches.toString());
                if (totalSearches >= parseInt(localStorage.getItem("maxStops"))) {
                    stopAutoSearch();
                    localStorage.removeItem("totalSearches");
                    setTimeout(() => {
                        window.location.href = "https://lingtu.gitlab.io/";
                    }, 6000);
                } else if (completedSearches % 3 === 0) {
                    setTimeout(() => {
                        window.location.reload();
                    }, 8000);
                } else {
                    startCountdown();
                }
            }, randomTime);
        }
        startCountdown();
    }
}

// 停止自动搜索
function stopAutoSearch() {
    clearInterval(countdownIntervalId);
    clearTimeout(countdownTimeoutId);
    if (countdownWorker) {
        countdownWorker.postMessage({ type: "stop" });
    }
    document.getElementById("countdown-timer").textContent = "已停止";
    isSearching = false;
}

// 初始化倒计时
let initialCountdownInterval;
function initializeCountdown() {
    const countdownElement = document.getElementById("countdown-timer");
    let remainingTime = getRandomInt(countdownMin, countdownMax);
    countdownElement.textContent = remainingTime;
    countdownWorker = new Worker(URL.createObjectURL(new Blob([`
        let intervalId;
        let remainingTime;

        self.onmessage = function(e) {
            const { type, duration } = e.data;

            if (type === 'start') {
                remainingTime = duration;
                intervalId = setInterval(() => {
                    remainingTime -= 1;
                    self.postMessage({ remainingTime });
                    if (remainingTime <= 0) {
                        clearInterval(intervalId);
                        self.postMessage({ type: 'done' });
                    }
                }, 1000);
            } else if (type === 'stop') {
                clearInterval(intervalId);
            }
        };
    `], { type: "application/javascript" })));
    countdownWorker.postMessage({ type: "start", duration: remainingTime });
    countdownWorker.onmessage = function (e) {
        const { remainingTime: newTime, type } = e.data;
        if (type === "done") {
            startAutoSearch();
        } else {
            countdownElement.textContent = newTime;
        }
    };
}

// 页面加载时的操作
if (document.getElementById("total-searches").textContent = totalSearches,
    document.addEventListener("DOMContentLoaded", () => {
        initializeCountdown();
        detectDevice();
    }),
    document.getElementById("deleteDataButton").addEventListener("click", () => {
        localStorage.removeItem("totalSearches");
        localStorage.removeItem("isException");
        localStorage.removeItem("searchWords");
        document.getElementById("total-searches").textContent = "0";
        document.getElementById("completed-searches").textContent = "0";
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    }),
    document.getElementById("start-button").addEventListener("click", startAutoSearch),
    document.getElementById("stop-button").addEventListener("click", stopAutoSearch),
    document.getElementById("exception-button").addEventListener("click", () => {
        if (isException) {
            isException = false;
            localStorage.setItem("isException", "false");
            document.getElementById("exception-button").textContent = "异常模式";
            document.getElementById("exception-button").title = "点击切换到异常模式";
            countdownMin = 50;
            countdownMax = 80;
        } else {
            isException = true;
            localStorage.setItem("isException", "true");
            document.getElementById("exception-button").textContent = "恢复正常";
            document.getElementById("exception-button").title = "点击切换到正常模式";
            countdownMin = 910;
            countdownMax = 930;
        }
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }),
    isException) {
    const exceptionButton = document.getElementById("exception-button");
    exceptionButton.textContent = "恢复正常";
    exceptionButton.title = "点击切换到正常模式";
    countdownMin = 910;
    countdownMax = 930;
}
