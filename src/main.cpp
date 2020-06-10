#include "misc.h"
#include "Player.h"
std::string path; //path to the program folder
Data* data = nullptr;
Log* plog = nullptr;
log_timer Log::timer;
int main(int, char** argv)
{
    plog = Log::init("log.txt");
    plog->flush();
    path = argv[0];
    path = path.erase(path.find_last_of('\\') + 1); //Makes 'path' be the path to the app folder, removing program name
    *plog << Log::timer << "The path is" << path << std::endl;

    data = Data::init();
    data->load();
    plog->put("Loaded data from files");

    sf::RenderWindow window(sf::VideoMode(1280, 720), "Ninja");
    window.setVerticalSyncEnabled(true);

    sf::Image icon;
    icon.loadFromFile("./res/icon.png"); //Sets the app icon
    window.setIcon(icon.getSize().x,icon.getSize().y,icon.getPixelsPtr());

    Player::init();
    sf::Texture t1;
    t1.loadFromFile("res/Tiles/tile_01.png");
    Player player(sf::Sprite(t1), 0u, 0u , 0.0f, 100, 10.0f);

    sf::Clock clock;

    while (window.isOpen())
    {

        uint32_t elapsedTime = clock.restart().asMilliseconds();//to measure time between frames
        sf::Event event{};

        while (window.pollEvent(event))
        {
            player.handleEvent();
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        player.Draw(&window);
        window.display();
    }

    data->save();
    plog->put("Successfully reached end of the program");
    return 0;
}