# A flank punishment: the first types the hint (the first feint adds "대시로 바깥쪽으로"); the second within 30 s shows
# "옆구리 금지 — 머리 정면 · 꼬리 끝" on the sub-line for 5 s.
execute unless score #azFlN mb matches 1.. if score #azPick mb matches 6 run function rlk:mboss/line/say {t:"옆구리는 위험합니다 — 머리 정면 · 꼬리 끝으로 · 대시로 바깥쪽으로",c:"#F2B53A",gap:2,hold:50,snd:2}
execute unless score #azFlN mb matches 1.. unless score #azPick mb matches 6 run function rlk:mboss/line/say {t:"옆구리는 위험합니다 — 머리 정면 · 꼬리 끝으로",c:"#F2B53A",gap:2,hold:50,snd:2}
scoreboard players add #azFlN mb 1
scoreboard players operation #azX mb = #azClk mb
scoreboard players operation #azX mb -= #azFlC mb
execute if score #azFlN mb matches 2.. if score #azX mb matches ..600 run function rlk:mboss/azhdaha/ai/punish_hint
scoreboard players operation #azFlC mb = #azClk mb
