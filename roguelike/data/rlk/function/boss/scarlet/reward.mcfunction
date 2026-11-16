# FN-b reward hook (mboss/sp/reward: @s = the player, not positioned; once per kill after the reward title and the level
# up, before the rift collapse; no fight tick any more): the roll / the grant the coda did not reach (a /reload while
# dying), the pending drop at the player (the return point is a checked floor) + its notice, the chat record, the reset.
execute unless score #hrEv hr matches 1..2 run function rlk:boss/scarlet/ev/roll
execute unless score #hrEvDone hr matches 1 run function rlk:boss/scarlet/ev/apply
execute if score #hrEvDrop hr matches 1 at @e[tag=rlk_body,limit=1] run function rlk:items/drop {id:"sword_hwamu"}
execute if score #hrEvDrop hr matches 1 run tellraw @s {text:"[월하의 선물] 보유 칸이 가득 차서 화무십일홍을 발밑에 놓았습니다.",color:"gray"}
function rlk:boss/scarlet/ev/record
function rlk:boss/scarlet/ev/reset
