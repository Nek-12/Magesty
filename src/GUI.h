#pragma once

#include "Object.h"

//TODO: constructors, rename class & header file
class GUI : private Object {
public:
    GUI() = default;
    void update() override;

protected:
    void onHover();
    void onClick();
    void move() override;

private:
    sf::Sprite altSprite;
    //GUI* pointsTo;
};