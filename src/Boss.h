#pragma once

#include "Entity.h"
#include "Skills.h"

class Boss: private Entity{
public:
    void update() override;
private:
    //TODO: add phases
    //TODO: add container for skills
};