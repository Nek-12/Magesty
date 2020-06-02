#pragma once
class Data;
extern Data* data;

class Data {
public:
    Data(Data const&) = delete; //No copying, no moving!
    void operator=(Data const&) = delete; //No assigning!

    static Data* init() {
        static Data instance;
        return &instance;
    }

    void load() {}
    void save() {}
private:
    Data() = default;
};
