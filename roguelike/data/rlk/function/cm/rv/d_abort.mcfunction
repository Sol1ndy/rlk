# no clear path / no safe landing (or the mark vanished): no dive this time
function rlk:cm/rv/tgt_kill
tag @s remove rlk_rv_lk
function rlk:cm/rv/idle
scoreboard players set @s cmCd2 40
execute if score @s cmCd matches ..9 run scoreboard players set @s cmCd 10
