# ThreeKK

## 使用方法
### 服务端
* 直接用python3启动Main中Server/net.py，或者运行Start_Server.bat(Widows)或.sh(Linux)
* 运行后选择每个房间的人数即可启动服务
### 客户端（CMD版本）
* 直接用python3启动Main中UI_Cmd/UI_cmd_main.py，或者运行Start_UI_Cmd.bat(Windows)或.sh(Linux)
* 等待所有玩家连接完成即可启动房间开始游戏
* 游戏出牌方式：牌的表示利用牌前面的序号，目标利用目标中的index，其中牌与目标用'>'分割，各牌及目标之间用',. '都可以分割，eg. 0,1>2,3 出第0和1张牌，目标是2和3号人物
	
## 常见问题
### 1、由于CMD窗口过小，导致刷屏  
* 请将cmd窗口扩展至至**高30字符，宽120字符**(也即windows默认cmd的大小)，Linux下需要拉伸（可以大一些，但是不能小）  
### 2、缺少python3中的库  
* 缺啥补啥:  `pip3 install <packagename>`



## 消息格式 
以下为各个消息及其分别在客户端和server端的字段含义，其中每个消息具有`msg_name`、`myid`、`heros`、`cards`、`start`、`end`、`third`、`forth`、`fifth`、`reply`字段，其中
* msg_name：代表消息类型，在下面详述
* myid、heros、cards：分别代表本人在该场游戏中的id，场上各个玩家的英雄状态，场上各个玩家的牌状态，由于基本上每个消息中含义稳定，不再赘述
* start、end：均为list类型，代表可能用得上的起始人物的id和目标人物id
* third、forth、fifth：根据消息内容变化的字段，含义根据消息类型变化
* reply：标识是否回复，主要用于客户端
*** 
以下说明对各种消息，服务端和客户端分别**收到**该消息的各字段含义

### 1. 'heartbeat' msg
* __Server__：无消息传递，只是check连接状态 
* __Client__：根据reply字段选择是否回复一个同类消息，用于连接检测

### 2. 'playcard' msg：  
* __Server__：收到该消息代表客户端打出牌，其中third为打出的牌list；end为list of牌的目标玩家id
* __Client__：收到消息中，start与end表示打出牌的起点和终点，均为玩家id（不是英雄id）；third字段为list，保存打出的牌；收到消息判断是否是自己打出的牌（start==self.playerid），据此反应不同

### 3. 'judgement' msg:  
* __Server__：  
* __Client__：

### 4. 'getcard' msg:  
* __Server__：  
* __Client__：

### 5. 'roundstart' msg:  
* __Server__：  
* __Client__：

### 6. 'roundend' msg:  
* __Server__：  
* __Client__：

### 7. 'gamestart' msg:  
* __Server__：  
* __Client__：

### 8. 'gameend' msg:  
* __Server__：  
* __Client__：

### 9. 'skillstart' msg:  
* __Server__：  
* __Client__：

**未完Doing...**



## Doing
- [x] 服务端
- [x] UI_CMD版本
- [ ] 使用说明 Doing
- [ ] 更多人物
- [ ] 更多牌类型
- [ ] 其他客户端
