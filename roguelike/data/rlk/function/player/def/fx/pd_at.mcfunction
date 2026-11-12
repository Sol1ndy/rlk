# 퍼펙트 닷지의 잔상 자리(닷지를 시작한 자리): 마네킹 잔상(흰 테두리), 붉은 분홍 줄기가 사방으로 터짐(g/burst), 낮은 붐과 도약의 바람.
# 소리(round W): 환술사의 낮은 붐(81 Hz 중심) + 드래곤 날갯짓(0.6배) + 삼지창 급류(1.3배: 뒤로 넘는 도약의 바람). 예전의 브리즈 미끄러짐은
# 파일이 작아(-34 dB) 묻혔다
execute rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/def/fx/pd_ghost
execute positioned ~ ~1 ~ run function rlk:player/def/fx/g/burst {s:1.0}
particle minecraft:dust_color_transition{from_color:[1f,0.55f,0.65f],to_color:[0.75f,0.1f,0.25f],scale:1.3f} ~ ~1 ~ 0.4 0.7 0.4 0 18 force @a[tag=player]
playsound minecraft:entity.illusioner.mirror_move player @a[tag=player] ~ ~ ~ 1 1.2
playsound minecraft:entity.ender_dragon.flap player @a[tag=player] ~ ~ ~ 1 0.6
playsound minecraft:item.trident.riptide_1 player @a[tag=player] ~ ~ ~ 0.6 1.3
