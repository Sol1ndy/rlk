# @s = 더미 (죽지 않음): 이번 틱에 깎인 체력을 #dd 에 더하고 가득 채움
scoreboard players operation #t lob = @s mhpM
scoreboard players operation #t lob -= @s mhpC
execute if score #t lob matches 1.. run scoreboard players operation #dd lob += #t lob
scoreboard players operation @s mhpC = @s mhpM
data modify entity @s Motion set value [0.0d,0.0d,0.0d]
function rlk:lobby/hbfix
