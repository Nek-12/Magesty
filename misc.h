#pragma once
//
// Created by ender on 08-May-20.
//
#include <fstream>
#include <chrono>
#include <iostream>
#include <utility>
class Log;
extern Log* log;

inline char* getCurTime() {
    auto t = std::chrono::system_clock::now();
    std::time_t ttime = std::chrono::system_clock::to_time_t(t);
    return std::ctime(&ttime);
}
//USAGE: log->put("Message part 1",someString,"message end", ...);
//NO SPACES REQUIRED
class Log {
public:
    static Log* init(const std::string& filename) {
        static Log instance(filename);
        return &instance;
    }

    template<typename ...Args>
    void put(const Args& ...args) { //first call

        f << getCurTime() << " | ";
        _put(args...);
    }

    void flush() {
        f.close();
        f.open(fname, std::fstream::out | std::fstream::trunc | std::fstream::in | std::fstream::ate);
        put("LOG FLUSHED");
    }
    void print() {
        f.seekg(std::fstream::beg);
        std::cout << f.rdbuf();
        f.seekg(std::fstream::end);
    }
private:
    template<typename T>
    void _put(const T& msg) { //Last call
        f << msg << std::endl;
    }
    template<typename T, typename ...Args>
    void _put(const T& t, const Args& ...args) { //recursive calls
        f << t << " ";
        _put(args...);
    }
    explicit Log(std::string  name) : fname(std::move(name)), f(fname, std::fstream::out | std::fstream::in | std::fstream::ate) {
        put("Started session");
    }
    std::string fname;
    std::fstream f;
};

