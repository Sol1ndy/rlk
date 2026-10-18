# Groggy over: re-level (6 t), the core flips to the top (9 t), compact again.
scoreboard players set #fgSt mb 4
scoreboard players set #fgT mb 0
function rlk:mboss/fieldgen/rig/play/recover
function rlk:mboss/fieldgen/rig/look/idle
scoreboard players set #fgCrack mb 0
function rlk:mboss/fieldgen/rig/crack/0
function rlk:mboss/fieldgen/seq_f/recover/begin
function rlk:mboss/fieldgen/hud/refresh
