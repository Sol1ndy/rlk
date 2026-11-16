# macro: cur. 지난 스캔에서 가졌던 id 를 이번 빠른 스캔이 세지 않았으면 보유 개수 0
$execute unless data storage rlk:scan seen.$(cur) run scoreboard players set @s it_$(cur) 0
