# The "first" lines of plan 4.13 typed at the pick (the patterns type none of these).
execute if score #azPick mb matches 2 unless score #azL2 mb = #azPh mb run function rlk:mboss/line/say {t:"갈라져라! 부서져라!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azPick mb matches 2 run scoreboard players operation #azL2 mb = #azPh mb
execute if score #azPick mb matches 3 unless score #azL39 mb matches 1 run function rlk:mboss/line/say {t:"모락스…!! 빚을 청산할 때가 왔다!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azPick mb matches 9 unless score #azL39 mb matches 1 run function rlk:mboss/line/say {t:"모락스…!! 빚을 청산할 때가 왔다!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azPick mb matches 3 run scoreboard players set #azL39 mb 1
execute if score #azPick mb matches 9 run scoreboard players set #azL39 mb 1
execute if score #azPick mb matches 7 unless score #azL7 mb = #azPh mb run function rlk:mboss/line/say {t:"버러지 같은 것들! 교활한 놈!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azPick mb matches 7 unless score #azL7h mb matches 1 run function rlk:mboss/azhdaha/ai/hint_whip
execute if score #azPick mb matches 7 run scoreboard players operation #azL7 mb = #azPh mb
execute if score #azPick mb matches 43..44 unless score #azLT mb matches 1 run function rlk:mboss/line/say {t:"가루로… 만들어주마! 흙으로… 돌아가라!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azPick mb matches 43..44 run scoreboard players set #azLT mb 1
