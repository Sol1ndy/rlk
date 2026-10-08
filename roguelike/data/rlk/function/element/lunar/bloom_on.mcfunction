# 달 개화 (@s = 몹): 이름 표시 + 네페르의 풀 이슬 · 기만의 핵(char/nefer/on_lbloom) + 아이템
scoreboard players set #lunRx tmp 25
scoreboard players set @s lnBloom 1
execute if score #charN tmp matches 8 as @a[tag=player,limit=1] run function rlk:char/nefer/on_lbloom
scoreboard players set #lnT tmp 2
function rlk:element/lunar/count
