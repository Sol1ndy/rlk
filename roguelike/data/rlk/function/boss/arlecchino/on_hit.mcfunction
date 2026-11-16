# Hook on_hit (@s = body inside combat/apply, before apply_mods; scores only, no recursion): a normal-attack hit
# (기본 공격: #icd 1, not a skill, not a reaction, not an item proc, not true damage; contract §3.5) while 선혈의 충격
# is armed is recorded; the next fight tick resolves it (bond/shock: the break inside a window, else the burst).
execute if score #shock kn matches 1 if score #icd tmp matches 1 unless score #skillDmg tmp matches 1 unless score #tfm tmp matches 1 unless score #sub itv matches 1 unless score #trueDmg tmp matches 1 run scoreboard players set #shk_hit kn 1
