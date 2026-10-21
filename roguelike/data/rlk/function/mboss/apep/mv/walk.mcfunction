# Side walk at 0.12 b/t across the facing (#apMvD 1 left / -1 right) for 40 t, facing the player.
function rlk:mboss/mv/turn {max:3}
execute if score #apMvD mb matches 1 rotated as @s rotated ~ 0 positioned ^0.12 ^ ^ run function rlk:mboss/apep/u/step_here
execute if score #apMvD mb matches -1 rotated as @s rotated ~ 0 positioned ^-0.12 ^ ^ run function rlk:mboss/apep/u/step_here
execute if score #apMvT mb matches 40.. run function rlk:mboss/apep/play/idle_p1
execute if score #apMvT mb matches 40.. run function rlk:mboss/apep/p/end
