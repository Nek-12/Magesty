#pragma once

#include "Object.h"

class Entity: protected Object { //Something alive
public:
    Entity() = delete;
    explicit Entity(const unsigned max_hp, const float defence = 0): max_hp(max_hp), defence(defence) {}
    //Doesn't override update(), pure virtual
    void kill() {hp = 0;}
    void setHP(int toHP, bool isRelative = false);
    unsigned getHp(){ return hp; }
    unsigned getMaxHp(){ return max_hp; }

protected:
    //Doesnt' override move(), makes it pure virtual
    virtual void AI() = 0;

protected:
    unsigned max_hp;
    unsigned hp = max_hp;
    float defence; //Defines how hp changes with damage
};

