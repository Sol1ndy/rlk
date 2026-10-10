# 사용 불가 안내 (@s = 플레이어, macro: t)
execute unless score #k219 snd matches 1 run function rlk:snd/f242
$title @s actionbar {"text":"$(t)","color":"#E06A5A"}
scoreboard players set @s hudHold 14
