# stomp w #azPT 5
playsound minecraft:block.deepslate.step hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
playsound minecraft:entity.ravager.step hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:mboss/azhdaha/p/stomp/ax_w1
