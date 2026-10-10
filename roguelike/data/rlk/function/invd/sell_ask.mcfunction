scoreboard players set @s pkConf 1
data modify entity @e[tag=rlk_invd_sell,limit=1] text set value {text:" 한 번 더 누르면 판매합니다 ",color:"#E06A5A"}
execute unless score #k72 snd matches 1 run function rlk:snd/f77
