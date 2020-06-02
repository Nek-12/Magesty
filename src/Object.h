#pragma once
#include <utility>

#include "misc.h"

class Object : public sf::Drawable { //any object
public:
    //Object() = default; TODO: Add custom
    Object(sf::Sprite  sprite, const int x, const int y, const float angle = 0.0) :
        sprite(std::move(sprite)), x(x), y(y), angle(angle) {}
    //TODO: Move constructor, copy constructor, operator=?
    ~Object() override = default;
    void draw(sf::RenderTarget &target, sf::RenderStates states) const override; //TODO: Final?
    virtual void update() = 0;
protected: //TODO: protected?
    void setSprite(sf::Sprite& s) { sprite = s; }
    virtual void move() = 0; //logic to handle AI
    void tp(int toX, int toY, bool isRelative = false) { /*TODO:...*/ } //teleport forcibly
private:
    sf::Sprite sprite;
    int x;
    int y;
    float angle;
};

//TODO: constructors
class GUI : Object {
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

class BG : Object {
public:
    void update() override; //supposedly does nothing?
protected:
    virtual void move();
private:
};

class Entity: Object { //Something alive
public:
    Entity() = delete;
    explicit Entity(const unsigned max_hp, const float defence = 0): max_hp(max_hp) {}
    //Doesn't override update(), pure virtual
    void kill() {hp = 0;}
     void setHP(const int toHP, bool isRelative = false) { /*TODO:...*/ }
protected:
    //Doesnt' override move(), makes it pure virtual
    virtual void AI() = 0;
private:
    unsigned max_hp;
    unsigned hp = max_hp;
    float defence; //Defines how hp changes with damage
};