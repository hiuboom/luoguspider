# 


| 这个作业属于哪个课程 | [2023秋-福州大学软件工程](https://bbs.csdn.net/forums/fzusdn-0831) |
| :------------------: | :----------------------------------------------------------: |
|  这个作业要求在哪里  | [2023秋软工实践个人作业二](https://bbs.csdn.net/topics/617213407) |
|    这个作业的目标    | 掌握pyhton语言，学会requests请求，tkinter GUI设计，JSON解码，申请使用copliot和其他AI使用 |
|         学号         |                          102102128                           |

### **[Github代码仓库](https://github.com/hiuboom/luoguspider)**

### 主界面
运行mainGui.py进入主界面

![img](https://img-community.csdnimg.cn/images/53bbe796c9704664bc64cb43c048aec9.png "#left")

### 爬虫界面

![img](https://img-community.csdnimg.cn/images/3c0e8e88fdc7424881f536c30b39c337.png "#left")

- **爬取题目实时显示：（速度挺快，可鼠标滚轮查看进度)**

![img](https://img-community.csdnimg.cn/images/e863f840f6f64747a8d6041f289d7aff.png "#left")

- **爬取题解：同上**

![img](https://img-community.csdnimg.cn/images/d2af13af266c43279fc2333222b65fba.png "#left")

### 搜题界面：


![img](https://img-community.csdnimg.cn/images/d209e83e8a8d4d72ab3240c3d92aa48d.png "#left")


- **筛选结果(要获取全部文件直接筛选无需选择标签、难度、关键词)**


![img](https://img-community.csdnimg.cn/images/1897685598994358b90b903ce27a1bad.png "#left")

- **直接点击查看题目或题解**


![img](https://img-community.csdnimg.cn/images/da7cec591ebe4dc6889cc254cd8d3998.png "#left")


![img](https://img-community.csdnimg.cn/images/7ab5b36dd3734fdc83cdcd5933d357b5.png "#left")

- **文件以md形式存储在./luogu/**


#### AIGC表格

|       子任务       |         预估哪些部分使用AIGC         | 实际中哪些部分使用AIGC |
| :----------------: | :----------------------------------: | :--------------------: |
|    爬取题目内容    |   获取解析网页源数据   |         有         |
|    爬取题目题解    |      预防反爬措施      |  有  |
| 爬取题目标签和难度 |   定位题目标签和难度   |  有  |
|     GUI可视化      |     设置窗口大小，按键文本框逻辑     |         AI很快形成框架         |
| 数据处理存储与搜索 | 设置json存储格式，进行清楚数据与保存 |         有         |

#### PSP表格

| PSP 阶段 | 具体任务 | 预估时间（分钟） | 实际时间（分钟） |
|:--------:|:-------:|:---------------:|:---------------:|
| Planning | 计划    |  60             |  60             |
| Design   | 设计    |  120            |  120             |
| Coding   | 编码    |  900            |  900            |
| Testing  | 测试    |  90            |  90            |
| Reporting| 报告    |  30             |  30             |
| Total    | 总计    |     1200        |   1200            |

### 注意事项

cookie可能失效了
替换自己的cookie
复制题解需要**登录**账号，这**非常重要！**

### 针对反爬机制

- **先前使用PlantomJS+selumium，效果有点不尽人意，使用了requests和 fake_useragent生成随机头，不知为何就没怎么封我了，本来设置了休眠但50个题感觉没必要**

## 总结

有些步骤参考我的童鞋们，ai很好用，检索能力较强，规范代码也腻害，代码在个人厂库。
