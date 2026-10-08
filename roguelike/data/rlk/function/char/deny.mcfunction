# 사용 불가 안내 (@s = 플레이어, macro: t)
playsound minecraft:block.note_block.bass master @s ~ ~ ~ 0.6 0.7
$title @s actionbar {"text":"$(t)","color":"#E06A5A"}
scoreboard players set @s hudHold 14
