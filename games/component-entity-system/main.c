#include "stdio.h"

typedef struct
{
    float x;
    float y;
} Displacement;


typedef struct
{
    float x;
    float y;
} Velocity;


typedef struct
{
    char name;
} Appearance;


typedef enum
{
    COMPONENT_NONE=0,
    COMPONENT_DISPLACEMENT = 1<<0,
    COMPONENT_VELOCITY = 1<<1,
    COMPONENT_APPEARANCE = 1 <<2
} Component;


typedef struct
{
    int mask[ENTITY_COUNT];
    Displacement displacement[ENTITY_COUNT];
    Velocity velocity[ENTITY_COUNT];
    Appearance appearance[ENTITY_COUNT];
} World;


unsigned int createEntity(World *world)
{
    unsigned int entity;
    for (entity=0; entity<ENTITY_COUNT; ++entity)
    {
        if (world->mask[entity] == COMPONENT_NONE)
        {
            return (entity);
        }
    }
    printf("Error! No more entities left!\n");
    return(ENTITY_COUNT);
}


void destroyEntity(World *world, unsigned int entity)
{
    world->mask[entity] = COMPONENT_NONE;
}


unsigned int createTree(World *world, float x, float y)
{
    unsigned int entity = createEntity(world);
    world->mask[entity] = COMPONENT_DISPLACEMENT | COMPONENT_APPEARANCE;
    world->displacement[entity].x = x;
    world->displacement[entity].y = y;

    world->appearance[entity].name = "Tree";
    return (entity);

}
