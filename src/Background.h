#pragma once

#include "Object.h"

class BG : private Object {
public:
    void update() override; //supposedly does nothing?

protected:
    virtual void move();

private:
};