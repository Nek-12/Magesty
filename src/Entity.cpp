#include "Entity.h"

void Entity::setHP(const int toHP, bool isRelative) {
    if (isRelative) {
        if (int(max_hp) - int(hp) < toHP) {//comparison unsigned and signed. checking overheal
            hp = max_hp;
        } else if (toHP + hp <= 0) kill();//checking if entity is alive after receiving hp
        else hp += toHP;
    } else {
        if (toHP <= 0) kill();
        else if (toHP > (int)max_hp) hp = max_hp;
        else hp = toHP;
    }
}
