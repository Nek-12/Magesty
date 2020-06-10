#include "Object.h"

void Object::draw(sf::RenderTarget& target, sf::RenderStates states) const {

}

void Object::tp(int toX, int toY, bool isRelative) {
    if (isRelative) {
        x += toX;
        y += toY;
    } else {
        x = toX;
        y = toY;
    }
}
