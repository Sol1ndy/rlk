# 땅 위 2초: 물기 한 번(c2T2 가 0 이 되는 틱), 두 틱 뒤 넉백 저항 0(몹 준비가 0.5 로 되돌려 놓으므로)
execute if score @s c2T2 matches 1.. run scoreboard players remove @s c2T2 1
execute if score @s c2T2 matches 0 run function rlk:cm/sb/bite
execute if score @s c2T2 matches 1 run function rlk:cm/c2/first
execute if score @s c2T matches ..0 run function rlk:cm/sb/sink_go
