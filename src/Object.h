#pragma once
#include <utility>

#include "misc.h"

class Object : public sf::Drawable { //any object
public:
    Object() = default; //TODO: Add custom
    Object(sf::Sprite  sprite, const int x, const int y, const float angle = 0.0) :
        sprite(std::move(sprite)), x(x), y(y), angle(angle) {}

    //TODO: Move constructor, copy constructor, operator=?
    ~Object() override = default;

    void draw(sf::RenderTarget &target, sf::RenderStates states) const override; //TODO: Final?
    virtual void update() = 0;

protected: //TODO: protected?
    void setSprite(sf::Sprite& s) { sprite = s; }
    virtual void move() = 0; //logic to handle AI
    void tp(int toX, int toY, bool isRelative = false); //teleport forcibly

protected:
    sf::Sprite sprite;//TODO: container of sprites for animation?
    int x;
    int y;
    float angle;
};

