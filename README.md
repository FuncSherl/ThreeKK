# ThreeKK
===========================
## 使用方法
### 服务端
	直接用python3启动Main中Server/net.py，或者运行Start_Server.bat或.sh
	运行后选择每个房间的人数即可启动服务
### 客户端（CMD版本）
	直接用python3启动Main中UI_Cmd/UI_cmd_main.py，或者运行Start_UI_Cmd.bat或.sh
	等待所有玩家连接完成即可启动房间开始游戏
***
## message format:
	1.inform msg:  
		--third segment means words to print  
	2.heartbeat msg:  
		--no information to trans, but to check link status, reply matters  
	3.gamestart msg:
		--start seg means the id given to this client, which used to identity if the other order is from yourself
	4.pickhero msg:
		--for client, the third seg means heroes for select, for server, the third seg means hero selected; the third seg forms like:[heroid1, heroid2...]
