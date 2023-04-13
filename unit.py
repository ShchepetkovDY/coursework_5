from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from random import randint



class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def equip_armor(self, armor: Armor) -> None:
        self.armor = armor

    def _count_damage(self, target: BaseUnit) -> int:
        """
        Эта функция содержит:
        -логику расчета урона игрока,
        -логику расчета брони цели,
        -здесь же происходит уменьшение выносливости атакующего при ударе
        и уменьшение выносливости защищающегося при использовании брони,
        -если у защищающегося нехватает выносливости - его броня игнорируется,
        -после всех расчетов цель получает урон - target.get_damage(damage)
        и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        """
        self.stamina -= self.weapon.stamina_per_hit
        damage = self.weapon.damage * self.unit_class.attack

        if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor

        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> None:
        """
        Метод, описывающий получение урона, и присваивание нового значения параметра self.hp
        """
        if damage >= 0 and self.hp - damage > 0:
            self.hp -= damage
        elif damage >= 0 >= self.hp - damage:
            self.hp = 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку - Навык использован.
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернет нам строку, которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return 'Навык уже был использован'

        result = self.unit_class.skill.use(self, target)
        self._is_skill_used = True
        return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция - удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} "
                f"соперника и наносит {damage} урона."
            )
        return (f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} "
                f"cоперника его останавливает."
                )


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция - удар соперника.
        Должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и "
                f"наносит Вам {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} "
            f"его останавливает."
        )
