#include <SFML/Graphics.hpp>
#include "misc.h"
Log* log = nullptr;
int main()
{

    sf::RenderWindow window(sf::VideoMode(1280, 720), "Ninja");
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        window.draw(shape);
        window.display();
    }

    return 0;
}