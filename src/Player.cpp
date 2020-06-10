#include "Player.h"

void Player::update() {

}

void Player::handleEvent() {
    for (auto i : keyboardKeys)
        if (sf::Keyboard::isKeyPressed(static_cast<sf::Keyboard::Key>(i.first)))
            (this->*i.second)();
}

void Player::moveForward() {
    y -= 10;
}

void Player::moveBackward() {
    y += 10;
}

void Player::moveRight() {
    x += 10;
}

void Player::moveLeft() {
    x -= 10;
}

void Player::dash() {

}

void Player::slowTime() {

}

void Player::attack() {

}

void Player::resetKeys() {
    std::ofstream file("./configs/config.txt", std::ios::trunc);
    file << "moveForward W\n"
        << "moveBackward S\n"
        << "moveLeft A\n"
        << "moveRight D\n"
        << "dash Space\n"
        << "slowTime LShift";
        //<< "attack LClick";

    setKeys();
}

void Player::setKeys() {
    if (!std::ifstream("configs/config.txt")){
        resetKeys();
        return;
    }
    int i = 0;
    std::ifstream file("configs/config.txt");
    std::string str;
    while(file >> str && i < 6){
        file >> str;
        auto it = keys.find(str);
        if(it != keys.end()){
            keyboardKeys[i] = std::make_pair(it->second, methods.at(i));
            i++;
        } else {
            resetKeys();
            return;
        }
    }
}

void Player::init() {
    keys.insert(std::pair<std::string, int8_t>("A", 0));
    keys.insert(std::pair<std::string, int8_t>("B", 1));
    keys.insert(std::pair<std::string, int8_t>("C", 2));
    keys.insert(std::pair<std::string, int8_t>("D", 3));
    keys.insert(std::pair<std::string, int8_t>("E", 4));
    keys.insert(std::pair<std::string, int8_t>("F", 5));
    keys.insert(std::pair<std::string, int8_t>("G", 6));
    keys.insert(std::pair<std::string, int8_t>("H", 7));
    keys.insert(std::pair<std::string, int8_t>("I", 8));
    keys.insert(std::pair<std::string, int8_t>("J", 9));
    keys.insert(std::pair<std::string, int8_t>("K", 10));
    keys.insert(std::pair<std::string, int8_t>("L", 11));
    keys.insert(std::pair<std::string, int8_t>("M", 12));
    keys.insert(std::pair<std::string, int8_t>("N", 13));
    keys.insert(std::pair<std::string, int8_t>("O", 14));
    keys.insert(std::pair<std::string, int8_t>("P", 15));
    keys.insert(std::pair<std::string, int8_t>("Q", 16));
    keys.insert(std::pair<std::string, int8_t>("R", 17));
    keys.insert(std::pair<std::string, int8_t>("S", 18));
    keys.insert(std::pair<std::string, int8_t>("T", 19));
    keys.insert(std::pair<std::string, int8_t>("U", 20));
    keys.insert(std::pair<std::string, int8_t>("V", 21));
    keys.insert(std::pair<std::string, int8_t>("W", 22));
    keys.insert(std::pair<std::string, int8_t>("X", 23));
    keys.insert(std::pair<std::string, int8_t>("Y", 24));
    keys.insert(std::pair<std::string, int8_t>("Z", 25));
    keys.insert(std::pair<std::string, int8_t>("Num0", 26));
    keys.insert(std::pair<std::string, int8_t>("Num1", 27));
    keys.insert(std::pair<std::string, int8_t>("Num2", 28));
    keys.insert(std::pair<std::string, int8_t>("Num3", 29));
    keys.insert(std::pair<std::string, int8_t>("Num4", 30));
    keys.insert(std::pair<std::string, int8_t>("Num5", 31));
    keys.insert(std::pair<std::string, int8_t>("Num6", 32));
    keys.insert(std::pair<std::string, int8_t>("Num7", 33));
    keys.insert(std::pair<std::string, int8_t>("Num8", 34));
    keys.insert(std::pair<std::string, int8_t>("Num9", 35));
    keys.insert(std::pair<std::string, int8_t>("Escape", 36));
    keys.insert(std::pair<std::string, int8_t>("LControl", 37));
    keys.insert(std::pair<std::string, int8_t>("LShift", 38));
    keys.insert(std::pair<std::string, int8_t>("LAlt", 39));
    keys.insert(std::pair<std::string, int8_t>("LSystem", 40));
    keys.insert(std::pair<std::string, int8_t>("RControl", 41));
    keys.insert(std::pair<std::string, int8_t>("RShift", 42));
    keys.insert(std::pair<std::string, int8_t>("RAlt", 43));
    keys.insert(std::pair<std::string, int8_t>("RSystem", 44));
    keys.insert(std::pair<std::string, int8_t>("Menu", 45));
    keys.insert(std::pair<std::string, int8_t>("LBracket", 46));
    keys.insert(std::pair<std::string, int8_t>("RBracket", 47));
    keys.insert(std::pair<std::string, int8_t>("Semicolon", 48));
    keys.insert(std::pair<std::string, int8_t>("Comma", 49));
    keys.insert(std::pair<std::string, int8_t>("Period", 50));
    keys.insert(std::pair<std::string, int8_t>("Quote", 51));
    keys.insert(std::pair<std::string, int8_t>("Slash", 52));
    keys.insert(std::pair<std::string, int8_t>("Backslash", 53));
    keys.insert(std::pair<std::string, int8_t>("Tilde", 54));
    keys.insert(std::pair<std::string, int8_t>("Equal", 55));
    keys.insert(std::pair<std::string, int8_t>("Hyphen", 56));
    keys.insert(std::pair<std::string, int8_t>("Space", 57));
    keys.insert(std::pair<std::string, int8_t>("Enter", 58));
    keys.insert(std::pair<std::string, int8_t>("Backspace", 59));
    keys.insert(std::pair<std::string, int8_t>("Tab", 60));
    keys.insert(std::pair<std::string, int8_t>("PageUp", 61));
    keys.insert(std::pair<std::string, int8_t>("PageDown", 62));
    keys.insert(std::pair<std::string, int8_t>("End", 63));
    keys.insert(std::pair<std::string, int8_t>("Home", 64));
    keys.insert(std::pair<std::string, int8_t>("Insert", 65));
    keys.insert(std::pair<std::string, int8_t>("Delete", 66));
    keys.insert(std::pair<std::string, int8_t>("Add", 67));
    keys.insert(std::pair<std::string, int8_t>("Subtract", 68));
    keys.insert(std::pair<std::string, int8_t>("Multiply", 69));
    keys.insert(std::pair<std::string, int8_t>("Divide", 70));
    keys.insert(std::pair<std::string, int8_t>("Left", 71));
    keys.insert(std::pair<std::string, int8_t>("Right", 72));
    keys.insert(std::pair<std::string, int8_t>("Up", 73));
    keys.insert(std::pair<std::string, int8_t>("Down", 74));
    keys.insert(std::pair<std::string, int8_t>("Numpad0", 75));
    keys.insert(std::pair<std::string, int8_t>("Numpad1", 76));
    keys.insert(std::pair<std::string, int8_t>("Numpad2", 77));
    keys.insert(std::pair<std::string, int8_t>("Numpad3", 78));
    keys.insert(std::pair<std::string, int8_t>("Numpad4", 79));
    keys.insert(std::pair<std::string, int8_t>("Numpad5", 80));
    keys.insert(std::pair<std::string, int8_t>("Numpad6", 81));
    keys.insert(std::pair<std::string, int8_t>("Numpad7", 82));
    keys.insert(std::pair<std::string, int8_t>("Numpad8", 83));
    keys.insert(std::pair<std::string, int8_t>("Numpad9", 84));
    keys.insert(std::pair<std::string, int8_t>("F1", 85));
    keys.insert(std::pair<std::string, int8_t>("F2", 86));
    keys.insert(std::pair<std::string, int8_t>("F3", 87));
    keys.insert(std::pair<std::string, int8_t>("F4", 88));
    keys.insert(std::pair<std::string, int8_t>("F5", 89));
    keys.insert(std::pair<std::string, int8_t>("F6", 90));
    keys.insert(std::pair<std::string, int8_t>("F7", 91));
    keys.insert(std::pair<std::string, int8_t>("F8", 92));
    keys.insert(std::pair<std::string, int8_t>("F9", 93));
    keys.insert(std::pair<std::string, int8_t>("F10", 94));
    keys.insert(std::pair<std::string, int8_t>("F11", 95));
    keys.insert(std::pair<std::string, int8_t>("F12", 96));
    keys.insert(std::pair<std::string, int8_t>("F13", 97));
    keys.insert(std::pair<std::string, int8_t>("F14", 98));
    keys.insert(std::pair<std::string, int8_t>("F15", 99));
    keys.insert(std::pair<std::string, int8_t>("Pause", 100));

    setKeys();
}



