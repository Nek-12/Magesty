#pragma once
#include "misc.h"

class Object : public sf::Drawable {
public:
    Object() = default;
    Object(const sf::Sprite& sprite, const int x, const int y, const float angle = 0.0) :
        sprite(sprite), x(x), y(y), angle(angle) {}
    //TODO: Move constructor, copy constructor?
    ~Object() override = default;
    void draw(sf::RenderTarget &target, sf::RenderStates states) const() override;
    virtual void update() = 0;
private:
    sf::Sprite sprite;
    int x = 0;
    int y = 0;
    float angle = 0.0;
};
