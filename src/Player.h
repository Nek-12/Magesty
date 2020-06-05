#pragma once

#include "Entity.h"
#include "Skills.h"

class Player: private Entity {
public:
    void update() override;

private:
    void (*firstSkill)(const Entity&);//TODO: parameters?
    void (*secondSkill)(const Entity&);
    int movementSpeed;

    //functions for control
    void moveForward();
    void moveBackward();
    void moveRight();
    void moveLeft();
    void dash();
    void slowTime();
};
