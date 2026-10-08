# macro: e(Fire/Water/Thunder/Ice/Grass). @s 에 원소 부착. 부착량 = #elU × 0.8(부착세)
# 이미 붙어 있으면 더 클 때만 갱신(감쇠 속도는 처음 부착 때 결정)
scoreboard players set #c tmp 8
scoreboard players operation #new tmp = #elU tmp
scoreboard players operation #new tmp *= #c tmp
scoreboard players operation #new tmp /= #st10 tmp
$execute unless score @s a$(e) matches 1.. run function rlk:element/attach_decay {e:"$(e)"}
$execute if score #new tmp > @s a$(e) run scoreboard players operation @s a$(e) = #new tmp
