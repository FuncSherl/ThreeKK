# ThreeKK

message format:
	1.inform msg: 
		--third segment means words to print
	2.heartbeat msg:
		--no information to trans, but to check link status, reply matters
	3.gamestart msg:
		--start seg means the id given to this client, which used to identity if the other order is from yourself
	4.pickhero msg:
		--for client, the third seg means heroes for select, for server, the third seg means hero selected; the third seg forms like:[heroid1, heroid2...]
