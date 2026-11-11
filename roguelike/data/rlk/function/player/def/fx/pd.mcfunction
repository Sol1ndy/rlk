# 퍼펙트 닷지 효과 (@s = 플레이어): 화면에 붉은 주황빛(g/title wash, 10틱), 닷지를 시작한 자리(rlk_dgo, 없으면 몸)에 아바타의
# 붉은 잔상(빛나는 테두리만 보이는 마네킹, 팀 rlk_cbred, 8틱 뒤 fx/ghost_out 이 사망 동작 없이 치움)과 붉은 섬광 · 먼지. 소리: 환술사의 거울 이동 · 브리즈 미끄러짐 · 에너지 울림
function rlk:player/def/fx/ovl {g:"wash",in:1,hold:4,out:5,t:10}
execute if entity @e[tag=rlk_dgo,limit=1] at @e[tag=rlk_dgo,limit=1] run function rlk:player/def/fx/pd_at
execute unless entity @e[tag=rlk_dgo,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:player/def/fx/pd_at
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[1f,0.25f,0.15f],scale:1.2f} ~ ~1 ~ 0.35 0.55 0.35 0 12 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.amethyst_block.chime player @a[tag=player] ~ ~ ~ 0.7 0.8
