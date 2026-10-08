# 생명의 계약이 0 이 됨 = 해소 (@s = 플레이어)
function rlk:char/bol_clear
function rlk:items/hook/on_bol_clear
# 각인 계약 4개: 해소 뒤 주는 피해 증가
execute if score pact engN matches 4.. run scoreboard players operation #pactT eng = #pactDur tmp
playsound minecraft:block.amethyst_block.resonate master @s ~ ~ ~ 0.5 0.7
