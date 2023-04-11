from dataclasses import dataclass

from skills import FuryPunch, HardShot, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name="Воин",
    max_health=80,
    max_stamina=40,
    attack=0.7,
    stamina=0.9,
    armor=1.2,
    skill=FuryPunch()
)

ThiefClass = UnitClass(
    name="Вор",
    max_health=60,
    max_stamina=30,
    attack=1.5,
    stamina=1.3,
    armor=0.8,
    skill=HardShot()
)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
