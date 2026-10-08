# 공허 결정 (공허+바위): 공허 결정이 떨어진다. 주우면 방어막(결정과 같은 양) + 공허 잔향 1칸
scoreboard players set #rdmg tmp 130
scoreboard players operation #rdmg tmp *= #rBase tmp
scoreboard players operation #rdmg tmp /= #100 tmp
scoreboard players set #t tmp 100
scoreboard players operation #t tmp += #emC tmp
scoreboard players operation #rdmg tmp *= #t tmp
scoreboard players operation #rdmg tmp /= #100 tmp
execute if score #rdmg tmp matches ..0 run scoreboard players set #rdmg tmp 1
scoreboard players set @s rxQ 21
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 5
