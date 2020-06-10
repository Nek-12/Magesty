#pragma once

#include <fstream>
#include <map>
#include "Entity.h"
#include "Skills.h"

class Player: protected Entity {
public:
    Player(sf::Sprite s, unsigned int i, unsigned int i1, float d, int i2, float d1):Entity(i2,d1){
        sprite = s;
        x = i;
        y = i1;
        angle = d;
    }
    void Draw(sf::RenderWindow *a){
        sprite.setPosition(x,y);
        a->draw(sprite);
    }

    void update() override;
    static void resetKeys();

    static void init();
    void handleEvent();
    void move(){};
    void AI(){};
private:
    void (*firstSkill)(const Entity&);//TODO: parameters?
    void (*secondSkill)(const Entity&);
    int movementSpeed;

    static void setKeys();

    //functions for control
    void moveForward();
    void moveBackward();
    void moveRight();
    void moveLeft();
    void dash();
    void slowTime();
    void attack();

    inline static std::map<std::string, int8_t> keys;
    inline static std::array<void(Player::*)(), 7> methods{&Player::moveForward,
                                                           &Player::moveBackward,
                                                           &Player::moveLeft,
                                                           &Player::moveRight,
                                                           &Player::dash,
                                                           &Player::slowTime,
                                                           &Player::attack};
    inline static std::array<std::pair<int8_t , void (Player::*)()>, 6> keyboardKeys;
    inline static std::array<std::pair<int8_t , void (Player::*)()>, 1> mouseKeys;
};
