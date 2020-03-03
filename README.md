# ThreeKK

## 使用方法
### 服务端
	直接用python3启动Main中Server/net.py，或者运行Start_Server.bat或.sh
	运行后选择每个房间的人数即可启动服务
### 客户端（CMD版本）
	直接用python3启动Main中UI_Cmd/UI_cmd_main.py，或者运行Start_UI_Cmd.bat或.sh
	等待所有玩家连接完成即可启动房间开始游戏

## 消息格式 
以下为各个消息及其分别在客户端和server端的字段含义
```
1. 'heartbeat' msg：  
   Server：no information to trans, but to check link status, reply matters  
   Client：
2. 'playcard' msg：  
	test
3. gamestart msg:  
	start seg means the id given to this client, which used to identity if the other order is from yourself
4. pickhero msg:  
	for client, the third seg means heroes for s
```
