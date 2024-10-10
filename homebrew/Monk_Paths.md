<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hover Pop-Up Text</title>
    <style>
        /* Style for the hoverable text */
        .hover-text {
            position: relative;
            display: inline-block;
            cursor: pointer;
            color: blue;
            text-decoration: underline;
        }

        /* Style for the pop-up text */
        .hover-text .popup-text {
            visibility: hidden;
            width: 160px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 5px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%; /* Position above the text */
            left: 50%;
            margin-left: -80px; /* Center the text */
            opacity: 0; /* Start invisible */
            transition: opacity 0.3s; /* Smooth transition */
            font-size: 12px;
        }

        /* Show the pop-up text on hover */
        .hover-text:hover .popup-text {
            visibility: visible;
            opacity: 1;
        }

        /* Add an arrow below the pop-up text */
        .hover-text .popup-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #555 transparent transparent transparent;
        }
    </style>
</head>

# Monk of Paths

This subclass of Monk focuses on versatility, and taking on specific roles to fill the team's needs, through its usages of Paths.

Keeping a good chunk of the Monk kit the same, mostly tweaking the Ki usage.

<details> 
<ul>
<li>
Any usage of Ki points has been replaced with the Resource system listed below.   
</li>

<li>
replace in Monk: Ki (lvl 2) with the Open Gate Path.
</li>
<li>
remove from Monk: Ki-Fueled Attack (lvl 3), Quickened Healing (lvl 4), Focused Aim (lvl 5).
</li>
<li>
add: Path Training at levels 3, 5, 9, 13, and 18.
</li>
</ul>
<summary><h2>"Patch Notes"</h2></summary>
</details>

## Resource: Ki Points

During the Preparation Phase, the Monk may spend their Ki Points to roll the respective amount of Ki Dice.

The results are stored until the Monk's next Preparation Phase, and can be used any time based on the Action's Keywords.

The Monk may only change from their current Path to another one when they spend at least one Ki Point.

The Monk has Ki points equal to their levels, and can spend any amount of Hit Dice during a Short rest to replenish one Ki Point per Dice spent.

1 Ki Point - 1d12

2 Ki Points - 1d12, 2d6

***


## Paths:

The Monk of Paths begins with the Open Gate Path at level 2, and may learn new Paths with Path Training.

### Open Gate Path

P: All of these effects are usable in all paths.

P: Declared Attacks when unarmed or with Pugilist weapons receive bonuses from your Strength and your Dexterity.

0+: <i><span class="hover-text">Reactive <span class="popup-text">Reactive actions can be taken at any time.</span></span> </i> Add dice result to any Accuracy roll.

4+: <i><span class="hover-text">Reactive <span class="popup-text">Reactive actions can be taken at any time.</span></span> </i> Add any one of your Ability Bonuses to any Damage roll.

9+: _Quick_ Stun melee target.




***

### Boulder's Path

P: All of your Attacks are now Slow.

P: You are unaffected by Crippling effects.

2+: _Quick_ Challenge target in one Ability. Reduce their Damage Resistance by the result.

5+: _Quick_ Charge at target. Land a guaranteed Attack on them.

7+: _Slow_ Attack target. Ignore any Damage Resistance.


***


### Path of the Manyspear 

P: Whenever you Declare an Attack, Queue another Attack at a valid target. 

2+: _Quick_ Until your next Preparation Phase: After an Attack Hits the target, roll the Damage dice again. Treat the sum of these rolls as a separate instance of damage.

4+:  _Slow_ Declare two additional _Slow_ Attacks.

7+: _Quick_ Until your next Preparation Phase: Whenever you Declare an Attack, Queue another Attack at a valid target. This effect is in addition to other instances of this Action, and in addition to Manyspear Path's passive.

10+: _Focus_[^1] Ignore the results of your Ki Dice, including the one spent to use this Action. Treat each of them as though they were a 9.



***


### Path of the Scar Bearer 

P: Increase your Damage Resistance by your highest Ability Bonus.

0+: _Quick_ Gain a number stacks of Grit[^5] equal to one third of the dice used to use this Action, rounded up.

4+: _Concentration_ Unobstructed Enemy is Goaded[^4].

7+: _Lingering_ Each time you are Hit, immediately Hit them.

***



### Path of the Mistdancer 

P: At the end of Each Preparation Phase, gain one point of Elusive[^2].

2+: <i><span class="hover-text">Reactive <span class="popup-text">Reactive actions can be taken at any time.</span></span> </i> Move to a space neighboring an Unobstructed[^3] target. Restore their health equal to an Ability Bonus. Gain one point of Elusive.

5+: <i><span class="hover-text">Reactive <span class="popup-text">Reactive actions can be taken at any time.</span></span> </i> Challenge a target's Dexterity. If you win, Stun them.

9+: _Lingering_ Whenever target would be attacked, you take the damage instead.

***

### Path of the Replenishing Cycle

P: At the end of Each Preparation Phase, regain health equal to the amount of Paths you've learned.

0+: _Slow_ All characters in melee range heal for the result of the dice spent on this Action. 

6+: _Quick_ Spend Hit Dice up to the amount of Paths you've learned. These can either be spent to heal you, or recover Ki Points.

10+: _Lingering_, _Focus_ Treat the dice used to roll this result as though it hadn't been spent. While this effect is active, act as though you were in another Path, including its Passive effects.

[^1]: Focus - Must be the first Declared usage of your Resource Dice.
[^2]: Elusive - Any instance of damage is ignored, and instead removes a point of Elusive.
[^3]: Unobstructed - A character is Unobstructed if you can draw a direct line from your Character to them, with nothing physically blocking this line or stopping sight.
[^4]: Goaded - When a character is Goaded, they must target the one who Goaded them with their Actions. Any movement must resolve with them closer to the one who Goaded them.