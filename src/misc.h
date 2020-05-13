#pragma once
#include <fstream>
#include <cstring>
#include <chrono>
#include <iostream>
#include <utility>
#include <filesystem>
#include <SFML/Graphics.hpp>
#include "Data.h"
extern std::string path;
class Log;
extern Log* plog;

struct log_timer { explicit log_timer() noexcept = default; };

//USAGE: plog->put("Message part 1",someString,"message end", ...);
//OR: *plog << Log::timer << "Message:" << msg << [ '\n' or std::endl ];
//NO SPACES REQUIRED

class Log {
public:
    template <typename T>
    Log& operator<<(const T& t) {
        f << t;
        return *this;
    }
    Log& operator<<( log_timer&) {
        f << getCurTime() << " | ";
        return *this;
    }
    Log& operator<<(std::ostream& (*os)(std::ostream&)) {
        f << os;
        return *this;
    }
    static log_timer timer;
    Log() = delete;
    Log(Log const&) = delete; //No copying, no moving!
    void operator=(Log const&) = delete; //No assigning!
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
        f.open(std::filesystem::path(fname), std::fstream::out | std::fstream::trunc | std::fstream::in);
        put("-------------| Log flushed |-------------");
    }
    void print() {
        f.seekg(std::fstream::beg);
        std::cout << f.rdbuf();
        f.seekg(std::fstream::end);
    }
    static char* getCurTime() {
        auto t = std::chrono::system_clock::now();
        std::time_t ttime = std::chrono::system_clock::to_time_t(t);
        return std::ctime(&ttime);
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
    explicit Log(std::string  name) : fname(std::move(name)), f(std::filesystem::path(fname), std::fstream::out | std::fstream::ate) {
        if (!f) throw std::runtime_error("Error opening log file");
        put(" -------------| Started log session |------------- ");
    }
    ~Log() {
        put("-------------| The program was closed |-------------");
    }
    std::string fname;
    std::fstream f;
};

