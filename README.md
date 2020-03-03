# ThreeKK

## 使用方法
### 服务端
	直接用python3启动Main中Server/net.py，或者运行Start_Server.bat或.sh
	运行后选择每个房间的人数即可启动服务
### 客户端（CMD版本）
	直接用python3启动Main中UI_Cmd/UI_cmd_main.py，或者运行Start_UI_Cmd.bat或.sh
	等待所有玩家连接完成即可启动房间开始游戏

## 消息格式 
以下为各个消息及其分别在客户端和server端的字段含义，其中每个消息具有`msg_name`、`myid`、`heros`、`cards`、`start`、`end`、`third`、`forth`、`fifth`、`reply`字段，其中
* msg_name：代表消息类型，在下面详述
* myid、heros、cards：分别代表本人在该场游戏中的id，场上各个玩家的英雄状态，场上各个玩家的牌状态

### 1. 'heartbeat' msg
* __Server__：no information to trans, but to check link status, reply matters  
* __Client__：

### 2. 'playcard' msg：  
* __Server__：no information to trans, but to check link status, reply matters  
* __Client__：

### 3. 'gamestart' msg:  
* __Server__：no information to trans, but to check link status, reply matters  
* __Client__：

### 4. 'pickhero' msg:  
* __Server__：no information to trans, but to check link status, reply matters  
* __Client__：




## Doing
- [x] 服务端
- [x] UI_CMD版本
- [x] 使用说明
- [ ] 编码
- [ ] 测试
- [ ] 交付
